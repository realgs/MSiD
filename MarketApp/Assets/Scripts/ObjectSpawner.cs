using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectSpawner : MonoBehaviour
{
    [SerializeField]
    private ObjectPooler pooler;
    [SerializeField]
    private float startingOffsetX, minSpawnY, maxSpawnY, gapSize, distanceToNext;
    [SerializeField]
    private float gameSpeed;
    [SerializeField]
    private Color colorA, colorB;

    private float timeElapsed;
    private float distanceSinceLastSpawn = 0f;

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

        GameObject lowerObstacle = pooler.GetGameObject();
        lowerObstacle.transform.position = new Vector2(startingOffsetX, point - sizeY / 2 - gapSize / 2f);
        lowerObstacle.GetComponent<Rigidbody2D>().velocity = Vector2.left * gameSpeed;
        lowerObstacle.GetComponent<SpriteRenderer>().color = color;
        lowerObstacle.SetActive(true);
    }

    private void Update()
    {
        timeElapsed += Time.deltaTime;
        if(gameSpeed * timeElapsed - distanceSinceLastSpawn > distanceToNext)
        {
            distanceSinceLastSpawn = gameSpeed * timeElapsed;
            Spawn();
        }
    }
}
