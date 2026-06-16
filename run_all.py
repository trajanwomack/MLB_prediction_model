import subprocess

steps = [
 
    "team_hitting.py",
  
    "player_pitching.py",
    "team_features.py",
    "game_level.py",
    "game_dataset_builder.py",

    "model_training.py"
]

for step in steps:
    print(f"\nRunning {step}...")
    subprocess.run(["python", step], check=True)

print("\nPipeline complete.")