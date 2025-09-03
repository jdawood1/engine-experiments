using UnityEngine;
using TMPro;

[RequireComponent(typeof(Rigidbody))]
public class PlayerController : MonoBehaviour
{
    [SerializeField] float moveSpeed = 6f;
    [SerializeField] float rotateSpeed = 120f;
    [SerializeField] TMP_Text hudText;   // drag a TMP Text here

    Rigidbody rb;
    int collisions;
    float fwd, turn;
    float hudTimer;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
        rb.interpolation = RigidbodyInterpolation.Interpolate;
        rb.collisionDetectionMode = CollisionDetectionMode.Continuous;
        rb.constraints = RigidbodyConstraints.FreezeRotationX | RigidbodyConstraints.FreezeRotationZ;
    }

    void Update()
    {
        turn = Input.GetAxisRaw("Horizontal");
        fwd  = Input.GetAxisRaw("Vertical");
        transform.Rotate(0f, turn * rotateSpeed * Time.deltaTime, 0f);

        hudTimer += Time.unscaledDeltaTime;
        if (hudText && hudTimer >= 0.2f)
        {
            float planar = new Vector3(rb.linearVelocity.x, 0f, rb.linearVelocity.z).magnitude;
            hudText.text = $"Speed: {planar:0.0}   Collisions: {collisions}";
            hudTimer = 0f;
        }
    }

    void FixedUpdate()
    {
        Vector3 vel = transform.forward * (fwd * moveSpeed);
        vel.y = rb.linearVelocity.y;
        rb.linearVelocity = vel;
    }

    void OnCollisionEnter(Collision _) => collisions++;
}

