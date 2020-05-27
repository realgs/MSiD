using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
public class PlayerController : MonoBehaviour
{
    [SerializeField]
    private float jumpForce;
    [SerializeField]
    private string obstacleString, scoreString;
    private new Rigidbody2D rigidbody;
    private ScoreManager scoreManager;
    private GameManager gameManager;

    private void Awake()
    {
        rigidbody = GetComponent<Rigidbody2D>();
        scoreManager = FindObjectOfType<ScoreManager>();
        gameManager = FindObjectOfType<GameManager>();
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if(collision.CompareTag(obstacleString))
        {
            Death();
        }
        else if(collision.CompareTag(scoreString))
        {
            scoreManager.UpdateScore();
        }
    }

    private void Update()
    {
        if(Input.GetButtonDown("Jump"))
        {
            rigidbody.AddForce(Vector2.up * jumpForce);
        }
    }

    private void Respawn()
    {
        transform.position = Vector2.zero;
        rigidbody.velocity = Vector2.zero;
    }

    private void Death()
    {
        transform.position = Vector2.zero;
        rigidbody.velocity = Vector2.zero;
        gameManager.GameOver();
    }
}
