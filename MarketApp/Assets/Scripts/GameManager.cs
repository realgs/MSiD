using UnityEngine;

[RequireComponent(typeof(ScoreManager))]
[RequireComponent(typeof(UIManager))]
public class GameManager : MonoBehaviour
{
    private ScoreManager ScoreManager;
    private UIManager UIManager;
    [SerializeField]
    private ObjectSpawner obstacleSpawner;

    private bool isPaused = false;

    private void Awake()
    {
        ScoreManager = GetComponent<ScoreManager>();
        UIManager = GetComponent<UIManager>();
    }

    public void Start()
    {
        Time.timeScale = 0f;
    }

    public void StartGame()
    {
        Time.timeScale = 1f;
        obstacleSpawner.Restart();
        isPaused = false;
    }

    public void PauseGame()
    {
        isPaused = !isPaused;
        if (isPaused) Time.timeScale = 0f;
        else Time.timeScale = 1f;
    }

    public void EndGame()
    {
        Time.timeScale = 0f;
        isPaused = false;
    }

    public void GameOver()
    {
        ScoreManager.RoundOver();
        EndGame();
    }
}
