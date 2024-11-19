import pandas as pd
import ast
import csv

def preprocess_scripts(file_path, movie_name):
    """
    Preprocess the script file and extract character and dialogue data.
    """
    rows = []
    with open(file_path, "r") as f:
        reader = csv.reader(f, delimiter=" ", quotechar='"', skipinitialspace=True)
        next(reader)  # Skip the header row
        for row in reader:
            rows.append({"character": row[1], "dialogue": row[2]})
    
    # Convert to a DataFrame
    data = pd.DataFrame(rows)
    data["movie"] = movie_name
    data["word_count"] = data["dialogue"].apply(lambda x: len(str(x).split()))
    return data

def map_characters_to_planets(characters_file, scripts_file):
    """
    Map characters to their home planets and calculate screen time by planet.
    """
    # Load characters data
    characters = pd.read_csv(characters_file)

    # Load and combine movie scripts
    scripts = pd.concat(
        [
            preprocess_scripts("data/sw_scripts/SW_EpisodeIV.txt", "Episode IV"),
            preprocess_scripts("data/sw_scripts/SW_EpisodeV.txt", "Episode V"),
            preprocess_scripts("data/sw_scripts/SW_EpisodeVI.txt", "Episode VI"),
        ]
    )

    print(scripts["character"].unique())
    characters["name"] = characters["name"].str.upper()
    print(characters["name"].unique())
    # Map characters to their homeworlds
    character_homeworld_map = characters.set_index("name")["homeworld"].to_dict()
    scripts["homeworld"] = scripts["character"].map(character_homeworld_map)

    print(scripts["character"].unique())

    # Group by homeworld and calculate total screen time (word count)
    planet_screen_time = scripts.groupby("character")["word_count"].sum().sort_values(ascending=False)

    # Return top 5 planets by screen time
    top_5_planets = planet_screen_time.head(5)
    return top_5_planets

if __name__ == "__main__":
    # Assuming files are in the 'data/' folder
    top_planets = map_characters_to_planets("data/swapi/characters.csv", "data/sw_scripts/scripts_combined.csv")
    print("Top 5 Planets by Screen Time:")
    print(top_planets)
