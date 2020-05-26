using UnityEngine;
using System.Collections.Generic;

public class ObjectSpawner : MonoBehaviour
{
    [SerializeField]
    private ObjectPooler pooler;
    [SerializeField]
    private float gameSpeed, startingOffsetX, minSpawnY, maxSpawnY, gapSize, distanceToNext, despawnPoint;
    [SerializeField]
    private Color colorA, colorB;

    private float timeElapsed;
    private float distanceSinceLastSpawn = 0f;
    private List<Transform> spawnedObjects = new List<Transform>();

    private void Spawn()
    {
        float point = Mathf.PerlinNoise(timeElapsed, timeElapsed * gameSpeed);
        Color color;
        if (point < 0.5f) color = colorA;
        else color = colorB;

        point = minSpawnY + (maxSpawnY - minSpawnY) * point;

        GameObject upperObstacle = pooler.GetGameObject();
        float sizeY = upperObstacle.transform.localScale.y;
        upperObstacle.transform.position = new Vector2(startingOffsetX, sizeY/2 + point + gapSize / 2f);
        upperObstacle.GetComponent<Rigidbody2D>().velocity = Vector2.left * gameSpeed;
        upperObstacle.GetComponent<SpriteRenderer>().color = color;
        upperObstacle.SetActive(true);
        upperObstacle.transform.GetChild(0).gameObject.SetActive(true);

        GameObject lowerObstacle = pooler.GetGameObject();
        lowerObstacle.transform.position = new Vector2(startingOffsetX, point - sizeY / 2 - gapSize / 2f);
        lowerObstacle.GetComponent<Rigidbody2D>().velocity = Vector2.left * gameSpeed;
        lowerObstacle.GetComponent<SpriteRenderer>().color = color;
        lowerObstacle.SetActive(true);

        spawnedObjects.Add(lowerObstacle.transform);
        spawnedObjects.Add(upperObstacle.transform);
    }

    private void Despawn()
    {
        List<Transform> toDespawn = new List<Transform>();
        foreach(Transform t in spawnedObjects)
        {
            if(t.position.x <= despawnPoint)
            {
                toDespawn.Add(t);
            }
        }

        foreach(Transform t in toDespawn)
        {
            t.GetChild(0).gameObject.SetActive(false);
            t.gameObject.SetActive(false);
            spawnedObjects.Remove(t);
        }
    }

    private void Update()
    {
        timeElapsed += Time.deltaTime;
        if(gameSpeed * timeElapsed - distanceSinceLastSpawn > distanceToNext)
        {
            distanceSinceLastSpawn = gameSpeed * timeElapsed;
            Spawn();
        }
        Despawn();
    }

    public void Restart()
    {
        foreach(Transform t in spawnedObjects)
        {
            t.GetChild(0).gameObject.SetActive(false);
            t.gameObject.SetActive(false);
        }
        spawnedObjects.Clear();
        timeElapsed = 0f;
        distanceSinceLastSpawn = 0f;
    }
}
