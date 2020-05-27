using UnityEngine;
[RequireComponent(typeof(UIManager))]
public class ScoreManager : MonoBehaviour
{
    private int currentScore, highScore;
    private UIManager UIManager;

    private void Awake()
    {
        highScore = PlayerPrefs.GetInt("highscore", 0);
        UIManager = GetComponent<UIManager>();
    }

    private void Start()
    {
        UIManager.SetHighScore(highScore);
    }

    public void UpdateScore()
    {
        currentScore += 1;
        UIManager.SetScore(currentScore);
    }

    public void RoundOver()
    {
        if(currentScore > highScore)
        {
            highScore = currentScore;
            PlayerPrefs.SetInt("highscore", highScore);
            UIManager.SetHighScore(highScore);
        }
        UIManager.DisplayGameOver(currentScore, highScore);
        currentScore = 0;
        UIManager.SetScore(currentScore);
    }
}
