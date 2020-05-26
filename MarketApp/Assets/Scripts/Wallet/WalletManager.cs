using UnityEngine;
using System.Collections.Generic;
using TMPro;
using UnityEngine.UI;
using System.IO;
using System;

public class WalletManager : MonoBehaviour
{
    [SerializeField]
    private ObjectPooler walletValuesPool;
    [SerializeField]
    private Transform valuesContainer;
    [SerializeField]
    private TMP_InputField nameTxt, amountTxt;

    private Dictionary<string, double> walletValues;

    private void Awake()
    {
        Deserialize();
    }

    public void AddValue()
    {
        string name = nameTxt.text;
        double amount = double.Parse(amountTxt.text, System.Globalization.CultureInfo.InvariantCulture.NumberFormat);
        if (amount <= 0) return;
        if (walletValues.ContainsKey(name)) DeleteValue(name);
        walletValues.Add(name, amount);
        CreateValueObject(name, amount);
        nameTxt.text = "";
        amountTxt.text = "";
        Serialize();
    }

    private void CreateValueObject(string name, double amount)
    {
        Transform walletValue = walletValuesPool.GetGameObject().transform;
        walletValue.GetChild(0).GetComponent<TextMeshProUGUI>().text = name;
        walletValue.GetChild(1).GetComponent<TextMeshProUGUI>().text = amount.ToString("0.########");
        walletValue.GetChild(2).GetComponent<Button>().onClick.RemoveAllListeners();
        walletValue.GetChild(2).GetComponent<Button>().onClick.AddListener(delegate { DeleteValue(name); });
        walletValue.gameObject.SetActive(true);
    }

    private void DeleteValue(string name)
    {
        walletValues.Remove(name);
        for(int i=0; i<valuesContainer.childCount; i++)
        {
            Transform nextChild = valuesContainer.GetChild(i);
            if (nextChild.GetChild(0).GetComponent<TextMeshProUGUI>().text.Equals(name))
            {
                nextChild.gameObject.SetActive(false);
            }
        }
        Serialize();
    }

    private void Deserialize()
    {
        try
        {
            var f_fileStream = File.OpenRead(@"walletData.data");
            var f_binaryFormatter = new System.Runtime.Serialization.Formatters.Binary.BinaryFormatter();
            walletValues = (Dictionary<string, double>)f_binaryFormatter.Deserialize(f_fileStream);
            f_fileStream.Close();
            foreach(KeyValuePair<string, double> keyValuePair in walletValues)
            {
                Debug.Log(keyValuePair);
                CreateValueObject(keyValuePair.Key, keyValuePair.Value);
            }
        }
        catch (Exception ex)
        {
            Debug.LogError(ex.StackTrace);
            walletValues = new Dictionary<string, double>();
        }
    }

    private void Serialize()
    {
        try
        {
            var f_fileStream = new FileStream(@"walletData.data", FileMode.Create, FileAccess.Write);
            var f_binaryFormatter = new System.Runtime.Serialization.Formatters.Binary.BinaryFormatter();
            f_binaryFormatter.Serialize(f_fileStream, walletValues);
            f_fileStream.Close();
        }
        catch (Exception ex)
        {
            Debug.LogError(ex.StackTrace);
        }
    }
}
