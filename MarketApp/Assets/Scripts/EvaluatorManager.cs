using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class EvaluatorManager : MonoBehaviour
{
    [SerializeField]
    private ObjectPooler evaWalletValuesPool;
    [SerializeField]
    private TextMeshProUGUI totalTxt;

    private Evaluator evaluator;
    private List<GameObject> spawnedObjs = new List<GameObject>();
    private string totalValueTxt;
    private List<string> valTxts;
    private ObjectSpawner objectSpawner;

    private void Awake()
    {
        evaluator = FindObjectOfType<Evaluator>();
        objectSpawner = FindObjectOfType<ObjectSpawner>();
    }

    public void RefreshValues()
    {
        ParseGeneratedVals(evaluator.UpdateOrderBooks());
        objectSpawner.SetData(valTxts, totalValueTxt);
        UpdateEvaluateDisplay();
    }

    private void ParseGeneratedVals(List<string> generated)
    {
        totalValueTxt = generated[generated.Count - 1];
        generated.Remove(totalValueTxt);
        valTxts = generated;
    }

    private void UpdateEvaluateDisplay()
    {
        foreach (GameObject obj in spawnedObjs)
            obj.SetActive(false);

        totalTxt.text = totalValueTxt;

        foreach(string s in valTxts)
        {
            GameObject obj = evaWalletValuesPool.GetGameObject();
            obj.transform.GetChild(0).GetComponent<TextMeshProUGUI>().text = s;
            obj.SetActive(true);
            spawnedObjs.Add(obj);
        }
    }
}
