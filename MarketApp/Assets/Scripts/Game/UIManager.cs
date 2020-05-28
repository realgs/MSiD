using UnityEngine;
using TMPro;

[RequireComponent(typeof(GameManager))]
public class UIManager : MonoBehaviour
{
    [SerializeField]
    private string highScoreTxtPrefix, currentScorePrefix;
    [SerializeField]
    private TextMeshProUGUI currentScoreTxt, highScoreTxt;
    [SerializeField]
    private GameObject gameOverScreen, gameUI;
    private TextMeshProUGUI endScoreTxt, endHighScoreTxt;

    private GameManager GameManager;

    private void Awake()
    {
        GameManager = GetComponent<GameManager>();
        endScoreTxt = gameOverScreen.transform.GetChild(0).GetComponent<TextMeshProUGUI>();
        endHighScoreTxt = gameOverScreen.transform.GetChild(1).GetComponent<TextMeshProUGUI>();
    }

    public void SetHighScore(int score)
    {
        if (score == 0) return;
        highScoreTxt.text = highScoreTxtPrefix + score;
    }

    public void SetScore(int score)
    {
        currentScoreTxt.text = score.ToString();
    }

    public void DisplayGameOver(int score, int highScore)
    {
        gameUI.SetActive(false);
        SetHighScore(highScore);
        endScoreTxt.text = currentScorePrefix + score.ToString();
        endHighScoreTxt.text = highScoreTxtPrefix + highScore.ToString();
        gameOverScreen.SetActive(true);
    }
}
