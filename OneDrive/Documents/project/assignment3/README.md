# Assignment 3 — Boids Flocking (Godot 4 .NET, C#)

This submission implements Craig Reynolds’ **Boids** algorithm (separation, alignment, cohesion) in **Godot 4 .NET (C#)**, demonstrates it in a small playable scene, and explains how flocking improves game feel.

## How to Run
1. Place the `assignment3/` folder in your Godot project root (same folder as `project.godot`).
2. Open **`assignment3/Scenes/Main.tscn`** and press **Play**.
3. Controls: **Arrow keys / WASD** move the player.
4. When the player gets close, the flock **chases** for a few seconds, then returns to ambient flocking. Enter the round **DoorTrigger** to spawn a new wave.

> If you only want the agents: use `assignment3/Scenes/Boid.tscn` and add a `Flock` node (script) to your scene, set BoidScene and PlayerPath.

## Files
- `assignment3/Scripts/Boid.cs` — Single agent with **Separation / Alignment / Cohesion**, bounds steering, optional seek.
- `assignment3/Scripts/Flock.cs` — Spawns and manages the flock. Adds a **timed chase** mechanic and **event-driven wave spawning**.
- `assignment3/Scripts/FlockTrigger.cs` — Optional one-shot **Area2D** that spawns a boid wave when the player enters.
- `assignment3/Scripts/Player.cs` — Simple top‑down player (**CharacterBody2D**) to demonstrate interactions.
- `assignment3/Scenes/Boid.tscn` — Minimal boid scene (Node2D + Boid.cs).
- `assignment3/Scenes/Main.tscn` — Example scene wiring **Player + Flock + Trigger** (ready to run).

## Algorithm Coverage (Requirement 1)
This implementation follows Reynolds’ Boids model:
- **Separation:** steer away from nearby neighbors within `SeparationRadius` (inverse distance weighting).
- **Alignment:** steer toward the average heading (velocity) of neighbors within `AlignmentRadius`.
- **Cohesion:** steer toward the average position of neighbors within `CohesionRadius`.
- **Integration limits:** `MaxSpeed` and `MaxForce` clamp velocity and steering.
- **Environment:** simple bounds steering keeps agents on-screen.

All weights/radii are exported for easy tuning in the Inspector.

## Demonstration / Game Integration (Requirement 2)
The **Main.tscn** scene shows a playable *micro‑game*:
- The **flock** idles with natural motion (ambient depth).
- When the **player** gets within `ChaseRadius` of any boid, the flock **seeks** the player for `ChaseSeconds`, then relaxes.
- Crossing the **DoorTrigger** spawns a **wave** of new boids (event-driven content).

These elements satisfy “integrate into your game **or** develop a new game demo.”

## README Explanation (Requirement 3)
**Design impact:**
- **Readable group motion:** Flocking naturally conveys intent (approach/avoid) without UI.
- **Pacing:** The timed chase creates short tension spikes and release, supporting game rhythm.
- **Systemic variety:** Event-based spawns let level scripts adjust challenge and visual density on the fly.
- **Ambient life:** Idle flocking adds background motion and a sense of place.

**Tuning defaults:**
- SeparationWeight **1.5**, AlignmentWeight **1.0**, CohesionWeight **1.0**  
- Radii: Separation **32**, Alignment/Cohesion **64**  
- MaxSpeed **180**, MaxForce **120**  
Adjust to fit your art scale and player speed.

## Notes
- Built for **Godot 4.x .NET**. For **Godot 3.x Mono**, replace:
  - `Instantiate()` → `Instance()`
  - `LimitLength()` → `Clamped()`
  - Scene file `format=2` instead of `format=3`

---

## References (optional citations)
- Craig W. Reynolds, “**Flocks, Herds, and Schools: A Distributed Behavioral Model**,” *SIGGRAPH '87*.  
- “**Boids**,” *Wikipedia*, https://en.wikipedia.org/wiki/Boids (overview of separation, alignment, and cohesion).