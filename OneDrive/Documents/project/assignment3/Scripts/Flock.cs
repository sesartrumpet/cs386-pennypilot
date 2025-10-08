using Godot;
using System.Collections.Generic;

public partial class Flock : Node2D
{
    [Export] public PackedScene BoidScene;
    [Export] public int Count = 60;

    [Export] public Rect2 Bounds = new Rect2(Vector2.Zero, new Vector2(0, 0)); // auto-fill if zero
    [Export] public NodePath PlayerPath;
    [Export] public float ChaseRadius = 240f;
    [Export] public float ChaseSeconds = 6f;
    [Export] public float SeekWeight = 1.2f;

    public readonly List<Boid> Boids = new List<Boid>();

    public bool SeekEnabled { get; private set; }
    public Vector2 SeekTarget { get; private set; }

    private Node2D _player;
    private float _chaseTimer;

    public override void _Ready()
    {
        if (Bounds.Size == Vector2.Zero) // fill to viewport if left at zero
            Bounds = new Rect2(Vector2.Zero, GetViewportRect().Size);

        if (PlayerPath != null && !PlayerPath.IsEmpty)
            _player = GetNodeOrNull<Node2D>(PlayerPath);

        SpawnFlock();
    }

    private void SpawnFlock()
    {
        if (BoidScene == null)
        {
            GD.PushWarning("BoidScene is not set on Flock.");
            return;
        }

        var rng = new RandomNumberGenerator();
        rng.Randomize();

        for (int i = 0; i < Count; i++)
        {
            var b = (Boid)BoidScene.Instantiate();
            AddChild(b);

            var pos = new Vector2(
                rng.RandfRange(Bounds.Position.X, Bounds.End.X),
                rng.RandfRange(Bounds.Position.Y, Bounds.End.Y)
            );
            b.GlobalPosition = pos;

            var vel = Vector2.FromAngle(rng.RandfRange(0, Mathf.Tau)) * rng.RandfRange(60, 140);
            b.Initialize(this, vel);

            Boids.Add(b);
        }
    }

    public override void _PhysicsProcess(double delta)
    {
        float dt = (float)delta;

        // Start chase if player close to any boid
        if (_player != null)
        {
            float minD = float.MaxValue;
            foreach (var b in Boids)
            {
                float d = b.GlobalPosition.DistanceTo(_player.GlobalPosition);
                if (d < minD) minD = d;
            }
            if (minD < ChaseRadius)
                StartChase(_player.GlobalPosition);
        }

        if (SeekEnabled)
        {
            _chaseTimer -= dt;
            if (_player != null) SeekTarget = _player.GlobalPosition; // keep target live
            if (_chaseTimer <= 0f) StopChase();
        }
    }

    public void StartChase(Vector2 target)
    {
        SeekEnabled = true;
        SeekTarget = target;
        _chaseTimer = ChaseSeconds;
    }

    public void StopChase()
    {
        SeekEnabled = false;
    }

    // Call this from events (e.g., door opens) to add a burst of boids
    public void SpawnWave(int extra = 20)
    {
        if (BoidScene == null) return;

        var rng = new RandomNumberGenerator();
        rng.Randomize();

        for (int i = 0; i < extra; i++)
        {
            var b = (Boid)BoidScene.Instantiate();
            AddChild(b);

            var pos = new Vector2(
                rng.RandfRange(Bounds.Position.X, Bounds.End.X),
                rng.RandfRange(Bounds.Position.Y, Bounds.End.Y)
            );
            b.GlobalPosition = pos;

            var vel = Vector2.FromAngle(rng.RandfRange(0, Mathf.Tau)) * rng.RandfRange(80, 160);
            b.Initialize(this, vel);

            Boids.Add(b);
        }
    }
}