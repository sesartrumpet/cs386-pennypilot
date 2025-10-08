using Godot;

public partial class FlockTrigger : Area2D
{
    [Export] public NodePath FlockPath;
    [Export] public int WaveCount = 15;

    private Flock _flock;

    public override void _Ready()
    {
        _flock = GetNode<Flock>(FlockPath);
        BodyEntered += OnBodyEntered;
    }

    private void OnBodyEntered(Node body)
    {
        if (body.IsInGroup("player"))
        {
            _flock.SpawnWave(WaveCount);
            QueueFree(); // trigger once
        }
    }
}