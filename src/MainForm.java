import javax.swing.*;
import java.awt.*;

public class MainForm {
    private JButton showBtn;
    private JPanel mainPanel;
    private JTextField textField1, textField4, textField2;
    private JTextArea textArea1;
    private JRadioButton bitBayRadioButton, bittrexRadioButton, tradingviewRadioButton1, allRadioButton;

    public MainForm() {
        showBtn.addActionListener(e -> {

        });

        bitBayRadioButton.addActionListener(e -> {
            bitBayRadioButton.setSelected(true);
            bittrexRadioButton.setSelected(false);
            tradingviewRadioButton1.setSelected(false);
            allRadioButton.setSelected(false);
        });

        bittrexRadioButton.addActionListener(e -> {
            bittrexRadioButton.setSelected(true);
            bitBayRadioButton.setSelected(false);
            tradingviewRadioButton1.setSelected(false);
            allRadioButton.setSelected(false);
        });

        tradingviewRadioButton1.addActionListener(e -> {
            tradingviewRadioButton1.setSelected(true);
            bitBayRadioButton.setSelected(false);
            bittrexRadioButton.setSelected(false);
            allRadioButton.setSelected(false);
        });

        allRadioButton.addActionListener(e -> {
            allRadioButton.setSelected(true);
            bitBayRadioButton.setSelected(false);
            bittrexRadioButton.setSelected(false);
            tradingviewRadioButton1.setSelected(false);
        });
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
        mainPanel.setLayout(new com.intellij.uiDesigner.core.GridLayoutManager(5, 4, new Insets(0, 0, 0, 0), -1, -1));
        mainPanel.setBackground(new Color(-2165249));
        final JLabel label1 = new JLabel();
        label1.setText("Podaj walutę bazową");
        mainPanel.add(label1, new com.intellij.uiDesigner.core.GridConstraints(0, 0, 1, 2, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_NONE, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, new Dimension(214, 16), null, 0, false));
        textField1 = new JTextField();
        mainPanel.add(textField1, new com.intellij.uiDesigner.core.GridConstraints(0, 2, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_HORIZONTAL, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_WANT_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, new Dimension(150, -1), null, 0, false));
        textArea1 = new JTextArea();
        textArea1.setForeground(new Color(-2956545));
        mainPanel.add(textArea1, new com.intellij.uiDesigner.core.GridConstraints(0, 3, 5, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_CENTER, com.intellij.uiDesigner.core.GridConstraints.FILL_BOTH, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_WANT_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_WANT_GROW, new Dimension(300, 300), new Dimension(150, 50), null, 0, false));
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
        mainPanel.add(showBtn, new com.intellij.uiDesigner.core.GridConstraints(3, 2, 2, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_CENTER, com.intellij.uiDesigner.core.GridConstraints.FILL_HORIZONTAL, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_SHRINK | com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, null, null, 0, false));
        bitBayRadioButton = new JRadioButton();
        bitBayRadioButton.setBackground(new Color(-2165249));
        bitBayRadioButton.setForeground(new Color(-16777216));
        bitBayRadioButton.setSelected(true);
        bitBayRadioButton.setText("BitBay");
        mainPanel.add(bitBayRadioButton, new com.intellij.uiDesigner.core.GridConstraints(3, 0, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_NONE, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_SHRINK | com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, null, null, 0, false));
        bittrexRadioButton = new JRadioButton();
        bittrexRadioButton.setBackground(new Color(-2165249));
        bittrexRadioButton.setForeground(new Color(-16777216));
        bittrexRadioButton.setText("Bittrex");
        mainPanel.add(bittrexRadioButton, new com.intellij.uiDesigner.core.GridConstraints(4, 0, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_NONE, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_SHRINK | com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, null, null, 0, false));
        tradingviewRadioButton1 = new JRadioButton();
        tradingviewRadioButton1.setBackground(new Color(-2165249));
        tradingviewRadioButton1.setForeground(new Color(-16777216));
        tradingviewRadioButton1.setText("Tradingview");
        mainPanel.add(tradingviewRadioButton1, new com.intellij.uiDesigner.core.GridConstraints(3, 1, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_NONE, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_SHRINK | com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, null, null, 0, false));
        allRadioButton = new JRadioButton();
        allRadioButton.setBackground(new Color(-2165249));
        allRadioButton.setForeground(new Color(-16777216));
        allRadioButton.setText("All");
        mainPanel.add(allRadioButton, new com.intellij.uiDesigner.core.GridConstraints(4, 1, 1, 1, com.intellij.uiDesigner.core.GridConstraints.ANCHOR_WEST, com.intellij.uiDesigner.core.GridConstraints.FILL_NONE, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_SHRINK | com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_CAN_GROW, com.intellij.uiDesigner.core.GridConstraints.SIZEPOLICY_FIXED, null, null, null, 0, false));
    }

    /**
     * @noinspection ALL
     */
    public JComponent $$$getRootComponent$$$() {
        return mainPanel;
    }

}
