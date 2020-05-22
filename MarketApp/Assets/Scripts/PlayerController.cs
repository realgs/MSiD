using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
public class PlayerController : MonoBehaviour
{
    [SerializeField]
    private float jumpForce;
    [SerializeField]
    private string obstacleString;
    private new Rigidbody2D rigidbody;

    private void Awake()
    {
        rigidbody = GetComponent<Rigidbody2D>();
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if(collision.CompareTag(obstacleString))
        {
            Death();
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

    }
}
