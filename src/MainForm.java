import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;

public class MainForm {
    private JButton showBtn, getDataButton, showInfoButton;
    private JPanel mainPanel;
    private JTextField textField1, textField4, textField2;
    private JTextArea textArea1;

    public MainForm() {
        showInfoButton.addActionListener(e -> {
            textArea1.selectAll();
            textArea1.replaceSelection("");
            try {
                showData(textField4.getText() + textField1.getText());
            } catch (FileNotFoundException ex) {
                ex.printStackTrace();
            }
        });

        showBtn.addActionListener(e -> {
            if (textField2.getText().equals("")) {
                textArea1.setText("Brak informacji o ilosci zasob");
            } else {
                try {
                    textArea1.selectAll();
                    textArea1.replaceSelection("");
                    sortResources();
                } catch (FileNotFoundException ex) {
                    ex.printStackTrace();
                }
            }
        });

        getDataButton.addActionListener(e -> {
            URL url = null;
            try {
                url = new URL("https://bitbay.net/API/Public/" + textField4.getText() + textField1.getText() + "/orderbook.json");
                if (checkSource(url)) {
                    url = new URL("https://www.bitstamp.net/api/order_book/" + textField4.getText() + textField1.getText());
                    if (checkSource(url)) textArea1.setText("Brak informacji o zasobach");
                    else setData(getJString(url));
                } else {
                    setData(getJString(url));
                }
            } catch (IOException | ParseException ex) {
                ex.printStackTrace();
            }
        });
    }

    private boolean checkSource(URL url) throws IOException {
        HttpURLConnection huc = (HttpURLConnection) url.openConnection();
        huc.setRequestMethod("GET");
        huc.connect();
        int responseCode = huc.getResponseCode();
        return responseCode == HttpURLConnection.HTTP_NOT_FOUND;
    }

    private String getJString(URL url) throws IOException {
        URLConnection connection = url.openConnection();
        connection.connect();
        BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        StringBuilder sb = new StringBuilder();
        String content;
        while ((content = br.readLine()) != null) {
            sb.append(content).append("\n");
        }
        br.close();
        return sb.toString();
    }

    private void showData(String string) throws FileNotFoundException {
        JSONParser jsonParser = new JSONParser();
        FileReader reader = new FileReader("finance.json");
        Object obj = null;
        try {
            obj = jsonParser.parse(reader);
        } catch (IOException | ParseException e) {
            e.printStackTrace();
        }
        JSONObject finance = (JSONObject) obj;

        assert finance != null;
        if (finance.containsKey(textField4.getText() + textField1.getText())) {
            JSONArray resources = (JSONArray) finance.get(textField4.getText() + textField1.getText());
            JSONObject bidsObj = (JSONObject) resources.get(0);
            JSONObject asksObj = (JSONObject) resources.get(1);
            JSONArray bids = (JSONArray) bidsObj.get("bids");
            JSONArray asks = (JSONArray) asksObj.get("asks");

            int countOrders = 50;
            countOrders = Math.min(countOrders, bids.size());
            for (int i = 0; i < countOrders; i++) {
                textArea1.append("Bids - " + bids.get(i) + " | Asks - " + asks.get(i) + "\n");
            }
        } else {
            textArea1.setText("nie ma informacji o wartości wprowadzanego zasobu");
        }
    }

    private void sortResources() throws FileNotFoundException {
        JSONParser jsonParser = new JSONParser();
        FileReader reader = new FileReader("finance.json");
        Object obj = null;
        try {
            obj = jsonParser.parse(reader);
        } catch (IOException | ParseException e) {
            e.printStackTrace();
        }
        JSONObject finance = (JSONObject) obj;

        if (finance.containsKey(textField4.getText() + textField1.getText())) {
            JSONArray sortObj = (JSONArray) ((JSONObject) ((JSONArray) finance.get(textField4.getText() + textField1.getText())).get(1)).get("asks");
            int sz = sortObj.size();
            double[][] ar = new double[sortObj.size()][2];

            for (int i = 0; i < sz; i++) {
                ar[i][0] = Double.parseDouble(((JSONArray) (sortObj.get(i))).get(0).toString());
                ar[i][1] = Double.parseDouble(((JSONArray) (sortObj.get(i))).get(1).toString());
            }

            double[] arr = new double[sortObj.size()];
            for (int i = 0; i < sz; i++) {
                arr[i] = (1 / ar[i][1]) * ar[i][0];
                System.out.println(ar[i][0] + " | " + ar[i][1] + " -> " + arr[i]);
            }

            for (int i = 0; i < sz; i++) {
                for (int j = 0; j < sz - 1; j++) {
                    if (arr[j] < arr[j + 1]) {
                        double tmp = arr[j + 1];
                        arr[j + 1] = arr[j];
                        arr[j] = tmp;


                        double a0 = ar[j + 1][0];
                        double a1 = ar[j + 1][1];

                        ar[j + 1][0] = ar[j][0];
                        ar[j + 1][1] = ar[j][1];

                        ar[j][0] = a0;
                        ar[j][1] = a1;
                    }
                }
            }
            System.out.println("\n\n\n");

            double count = Double.parseDouble(textField2.getText());
            double sum = 0;
            int o = 0;
            for (int i = 0; i < arr.length; i++) {
                if (count - ar[i][1] > 0) {
                    sum += ar[i][0];
                    count -= ar[i][1];
                } else {
                    break;
                }
            }
            textArea1.setText("Proponujemy  - " + textField2.getText() + "\nsprzedano na " + sum + "\n" + count + " zostalo");
        }
    }

    private void setData(String json) throws ParseException, FileNotFoundException {
        if (json != null) {
            JSONParser parser = new JSONParser();
            JSONObject jsonObject = (JSONObject) parser.parse(json);
            JSONArray bids = (JSONArray) jsonObject.get("bids");
            JSONArray asks = (JSONArray) jsonObject.get("asks");

            JSONObject obj = new JSONObject();
            JSONArray list = new JSONArray();
            JSONObject bidsToSave = new JSONObject();
            bidsToSave.put("bids", bids);
            JSONObject asksToSave = new JSONObject();
            asksToSave.put("asks", asks);
            list.add(bidsToSave);
            list.add(asksToSave);
            obj.put(textField4.getText() + textField1.getText(), list);

            File fileCheck = new File("finance.json");
            if (fileCheck.length() != 0) {
                JSONParser jsonParser = new JSONParser();
                FileReader reader = new FileReader("finance.json");
                Object oldObj = null;
                try {
                    oldObj = jsonParser.parse(reader);
                } catch (IOException | ParseException e) {
                    e.printStackTrace();
                }
                JSONObject old = (JSONObject) oldObj;
                assert old != null;
                old.put(textField4.getText() + textField1.getText(), list);
                try (FileWriter file = new FileWriter("finance.json")) {
                    file.write(old.toJSONString());
                    textArea1.setText("Dane zostaly zapisane");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            } else {
                try (FileWriter file = new FileWriter("finance.json", true)) {
                    file.write(obj.toJSONString());
                    textArea1.setText("Dane zostaly zapisane");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("MSiD Lab 5");
        frame.setContentPane(new MainForm().mainPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }

    {
// GUI initializer generated by IntelliJ IDEA GUI Designer
// >>> IMPORTANT!! <<<
// DO NOT EDIT OR ADD ANY CODE HERE!
        $$$setupUI$$$();
    }

    /**
     * Method generated by IntelliJ IDEA GUI Designer
     * >>> IMPORTANT!! <<<
     * DO NOT edit this method OR call it in your code!
     *
     * @noinspection ALL
     */
    private void $$$setupUI$$$() {
        mainPanel = new JPanel();
        mainPanel.setLayout(new com.intellij.uiDesigner.core.GridLayoutManager(4, 4, new Insets(0, 0, 0, 0), -1, -1));
        mainPanel.setBackground(new Color(-2165249));
        final JLabel label1 = new JLabel();
        label1.setText("Podaj walutę bazową");
        mainPanel.add(label1, new com.intellij.uiDesigner.core.GridConstraints(0, 0, 1, 2, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_NONE, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, new Dimension(214, 16), null, 0, false));
        textField1 = new JTextField();
        mainPanel.add(textField1, new com.intellij.uiDesigner.core.GridConstraints(0, 2, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_HORIZONTAL, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_WANT_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, new Dimension(150, -1), null, 0, false));
        final JLabel label2 = new JLabel();
        label2.setText("Podaj dane o posiadanych zasobach (jaki zasób) ");
        mainPanel.add(label2, new com.intellij.uiDesigner.core.GridConstraints(1, 0, 1, 2, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_NONE, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, new Dimension(214, 16), null, 0, false));
        textField4 = new JTextField();
        mainPanel.add(textField4, new com.intellij.uiDesigner.core.GridConstraints(1, 2, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_HORIZONTAL, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_WANT_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, new Dimension(150, -1), null, 0, false));
        final JLabel label3 = new JLabel();
        label3.setText("Podaj dane o posiadanych zasobach (jaka ilość)");
        mainPanel.add(label3, new com.intellij.uiDesigner.core.GridConstraints(2, 0, 1, 2, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_NONE, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, new Dimension(214, 16), null, 0, false));
        textField2 = new JTextField();
        mainPanel.add(textField2, new com.intellij.uiDesigner.core.GridConstraints(2, 2, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_HORIZONTAL, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_WANT_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, new Dimension(150, -1), null, 0, false));
        showBtn = new JButton();
        showBtn.setText("Show");
        mainPanel.add(showBtn, new com.intellij.uiDesigner.core.GridConstraints(3, 2, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_CENTER, com.intellij.uiDesigner.core.GridConstraints.FILL_HORIZONTAL, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_SHRINK | com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, null, null, 0, false));
        getDataButton = new JButton();
        getDataButton.setText("Get data");
        mainPanel.add(getDataButton, new com.intellij.uiDesigner.core.GridConstraints(3, 0, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_CENTER, com.intellij.uiDesigner.core.GridConstraints.FILL_HORIZONTAL, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_SHRINK | com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, null, null, 0, false));
        final JScrollPane scrollPane1 = new JScrollPane();
        mainPanel.add(scrollPane1, new com.intellij.uiDesigner.core.GridConstraints(0, 3, 4, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_CENTER, com.intellij.uiDesigner.core.GridConstraints.FILL_BOTH, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_SHRINK | com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_WANT_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_SHRINK | com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_WANT_GROW, new Dimension(300, 300), null, null, 0, false));
        textArea1 = new JTextArea();
        textArea1.setBackground(new Color(-6767427));
        textArea1.setForeground(new Color(-16777216));
        textArea1.setText("");
        scrollPane1.setViewportView(textArea1);
        showInfoButton = new JButton();
        showInfoButton.setText("Show info");
        mainPanel.add(showInfoButton, new com.intellij.uiDesigner.core.GridConstraints(3, 1, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_CENTER, com.intellij.uiDesigner.core.GridConstraints.FILL_HORIZONTAL, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_SHRINK | com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, null, null, 0, false));
    }

    /**
     * @noinspection ALL
     */
    public JComponent $$$getRootComponent$$$() {
        return mainPanel;
    }

}