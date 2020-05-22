using System.Collections.Generic;
using UnityEngine;

public class ObjectPooler : MonoBehaviour
{
    [SerializeField]
    private GameObject prefab;
    private List<GameObject> objectsPool = new List<GameObject>();

    private GameObject FindGameObject()
    {
        foreach(GameObject obj in objectsPool)
        {
            if (!obj.activeSelf) return obj;
        }

        return CreateNewObject();
    }

    private GameObject CreateNewObject()
    {
        return Instantiate(prefab, transform);
    }

    public GameObject GetGameObject()
    {
        return FindGameObject();
    }
}
