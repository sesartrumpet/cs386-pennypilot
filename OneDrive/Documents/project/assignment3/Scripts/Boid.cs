using Godot;
using System.Collections.Generic;

public partial class Boid : Node2D
{
    [Export] public float MaxSpeed = 180f;
    [Export] public float MaxForce = 120f;

    [Export] public float SeparationRadius = 32f;
    [Export] public float AlignmentRadius = 64f;
    [Export] public float CohesionRadius = 64f;

    [Export] public float SeparationWeight = 1.5f;
    [Export] public float AlignmentWeight = 1.0f;
    [Export] public float CohesionWeight = 1.0f;
    [Export] public float BoundsPadding = 32f;

    public Vector2 Velocity;
    private Vector2 _acc;
    private Flock _flock;

    public void Initialize(Flock flock, Vector2 initialVel)
    {
        _flock = flock;
        Velocity = initialVel;
    }

    public override void _PhysicsProcess(double delta)
    {
        float dt = (float)delta;
        _acc = Vector2.Zero;

        // Core boids behaviors
        _acc += Separation() * SeparationWeight;
        _acc += Alignment() * AlignmentWeight;
        _acc += Cohesion() * CohesionWeight;

        // Keep inside bounds
        _acc += KeepInBounds();

        // Optional: seek a target (e.g., player) during a chase window
        if (_flock.SeekEnabled)
            _acc += Seek(_flock.SeekTarget) * _flock.SeekWeight;

        // Integrate
        Velocity += _acc * dt;
        if (Velocity.Length() > MaxSpeed) Velocity = Velocity.Normalized() * MaxSpeed;

        GlobalPosition += Velocity * dt;
        if (Velocity.LengthSquared() > 1e-3f) Rotation = Velocity.Angle();
        QueueRedraw();
    }

    private Vector2 Seek(Vector2 target)
    {
        var desired = target - GlobalPosition;
        if (desired == Vector2.Zero) return Vector2.Zero;

        desired = desired.Normalized() * MaxSpeed;
        var steer = desired - Velocity;
        steer = steer.LimitLength(MaxForce);
        return steer;
    }

    private Vector2 Separation()
    {
        Vector2 steer = Vector2.Zero;
        int count = 0;

        foreach (var other in _flock.Boids)
        {
            if (other == this) continue;
            float d = GlobalPosition.DistanceTo(other.GlobalPosition);
            if (d > 0 && d < SeparationRadius)
            {
                // steer away stronger when closer
                var diff = (GlobalPosition - other.GlobalPosition).Normalized() / Mathf.Max(d, 0.001f);
                steer += diff;
                count++;
            }
        }

        if (count > 0)
        {
            steer /= count;
            steer = steer.Normalized() * MaxSpeed - Velocity;
            steer = steer.LimitLength(MaxForce);
        }
        return steer;
    }

    private Vector2 Alignment()
    {
        Vector2 sum = Vector2.Zero;
        int count = 0;

        foreach (var other in _flock.Boids)
        {
            if (other == this) continue;
            float d = GlobalPosition.DistanceTo(other.GlobalPosition);
            if (d < AlignmentRadius)
            {
                sum += other.Velocity;
                count++;
            }
        }

        if (count > 0)
        {
            var avg = (sum / count);
            if (avg.Length() > 0.001f) avg = avg.Normalized() * MaxSpeed;
            return (avg - Velocity).LimitLength(MaxForce);
        }
        return Vector2.Zero;
    }

    private Vector2 Cohesion()
    {
        Vector2 center = Vector2.Zero;
        int count = 0;

        foreach (var other in _flock.Boids)
        {
            if (other == this) continue;
            float d = GlobalPosition.DistanceTo(other.GlobalPosition);
            if (d < CohesionRadius)
            {
                center += other.GlobalPosition;
                count++;
            }
        }

        if (count > 0)
        {
            center /= count;
            return Seek(center);
        }
        return Vector2.Zero;
    }

    private Vector2 KeepInBounds()
    {
        var rect = _flock.Bounds;
        var steer = Vector2.Zero;
        float pad = BoundsPadding;

        if (GlobalPosition.X < rect.Position.X + pad) steer.X = MaxForce;
        else if (GlobalPosition.X > rect.End.X - pad) steer.X = -MaxForce;

        if (GlobalPosition.Y < rect.Position.Y + pad) steer.Y = MaxForce;
        else if (GlobalPosition.Y > rect.End.Y - pad) steer.Y = -MaxForce;

        return steer;
    }

    public override void _Draw()
    {
        // Simple white triangle pointing +X in local space
        var pts = new Vector2[]
        {
            new Vector2(10, 0),
            new Vector2(-8, 5),
            new Vector2(-8, -5)
        };
        var cols = new Color[] { Colors.White, Colors.White, Colors.White };
        DrawPolygon(pts, cols);
    }
}