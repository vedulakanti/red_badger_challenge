import pandas as pd
from utils.utils import preprocess_scripts


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
