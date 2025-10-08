using Godot;

public partial class Player : CharacterBody2D
{
    [Export] public float Speed = 260f;

    public override void _PhysicsProcess(double delta)
    {
        Vector2 input = Vector2.Zero;
        input.X = Input.GetActionStrength("ui_right") - Input.GetActionStrength("ui_left");
        input.Y = Input.GetActionStrength("ui_down") - Input.GetActionStrength("ui_up");
        if (input.Length() > 1f) input = input.Normalized();

        Velocity = input * Speed;
        MoveAndSlide();

        if (Velocity.LengthSquared() > 1e-3f)
            Rotation = Velocity.Angle();
    }
}