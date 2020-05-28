using System.IO;
using System.Net;
using UnityEngine;
using System.Collections.Generic;
using TMPro;
using System.Globalization;

public class Evaluator : MonoBehaviour
{

    [System.Serializable]
    private class Response<T>
    {
        public string success;
        public string message;
        public List<T> result;
    }

    [System.Serializable]
    private class CurrencyClass
    {
        public string Currency;
    }

    [System.Serializable]
    private class OrderBook
    {
        public string Quantity;
        public string Rate;
    }

    private TMP_Dropdown TMP_Dropdown;
    private string baseValue = "USD";
    private Dictionary<string, List<OrderBook>> allOrderBooks = new Dictionary<string, List<OrderBook>>();
    private Dictionary<string, double> walletValues;
    private List<string> generatedEvaluation = new List<string>();

    private void Awake()
    {
        TMP_Dropdown = FindObjectOfType<TMP_Dropdown>();
    }

    private Response<T> MakeRequest<T>(string url)
    {
        HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
        HttpWebResponse response = (HttpWebResponse)request.GetResponse();
        StreamReader reader = new StreamReader(response.GetResponseStream());
        string jsonResponse = reader.ReadToEnd();
        Response<T> info = JsonUtility.FromJson<Response<T>>(jsonResponse);
        return info;
    }

    public void SetBaseValue()
    {
        baseValue = TMP_Dropdown.options[TMP_Dropdown.value].text;
    }

    public void SetWalletValues(Dictionary<string, double> walletValues)
    {
        this.walletValues = walletValues;
    }

    public List<string> UpdateOrderBooks()
    {
        allOrderBooks.Clear();
        generatedEvaluation.Clear();
        double totalWalletValue = 0d;
        foreach (KeyValuePair<string, double> keyValuePair in walletValues)
        {
            double worth;
            if (baseValue.Equals(keyValuePair.Key))
                worth = keyValuePair.Value;
            else
            {
                GetOrderBook(keyValuePair.Key);
                worth = EvaluateValue(keyValuePair.Key);
            }
            totalWalletValue += worth;
            generatedEvaluation.Add(string.Format("Your {0}{1} is worth {2}{3}", keyValuePair.Value, keyValuePair.Key, worth.ToString("0.########"), baseValue));
        }
        generatedEvaluation.Add(string.Format("Your wallet is worth {0}{1}", totalWalletValue.ToString("0.########"), baseValue));
        return generatedEvaluation;
    }

    public List<string> GetAvailableCurrencies()
    {
        Response<CurrencyClass> response = MakeRequest<CurrencyClass>("https://api.bittrex.com/api/v1.1/public/getcurrencies");
        if (response.success.Equals("false"))
        {
            Debug.LogError("Can't fetch info!");
        }
        List<string> output = new List<string>(response.result.Count);
        foreach(CurrencyClass c in response.result)
        {
            output.Add(c.Currency);
        }
        return output;
    }

    private void GetOrderBook(string currency)
    {
        string url = string.Format("https://api.bittrex.com/api/v1.1/public/getorderbook?market={0}-{1}&type=buy", baseValue, currency);
        Response<OrderBook> response = MakeRequest<OrderBook>(url);
        if (response.success.Equals("false")) Debug.LogError("Can't fetch info!");
        if (allOrderBooks.ContainsKey(currency)) allOrderBooks[currency] = response.result;
        else allOrderBooks.Add(currency, response.result);
    }

    private double EvaluateValue(string currency)
    {
        double amount = walletValues[currency];
        double money = 0d;
        List<OrderBook> sells = allOrderBooks[currency];
        for(int i = 0; i<sells.Count; i++)
        {
            double.TryParse(sells[i].Quantity, NumberStyles.Float, NumberFormatInfo.InvariantInfo, out double sellAmount);
            double.TryParse(sells[i].Rate, NumberStyles.Float, NumberFormatInfo.InvariantInfo, out double sellRate);
            if (amount >= sellAmount) 
            {
                money += sellAmount * sellRate;
                amount -= sellAmount;
            }
        }
        return money;
    }
}
