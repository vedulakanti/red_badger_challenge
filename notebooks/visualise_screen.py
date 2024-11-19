# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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


def load_and_merge_data(characters_file, script_files):
    """
    Load characters and scripts, preprocess, and merge data for analysis.
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

    # Map characters to their homeworlds
    characters["name"] = characters["name"].str.upper()
    character_homeworld_map = characters.set_index("name")["homeworld"].to_dict()
    scripts["homeworld"] = scripts["character"].map(character_homeworld_map)

    return scripts

# File paths and movie details
characters_file = "data/swapi/characters.csv"
script_files = [
    {"path": "data/sw_scripts/SW_EpisodeIV.txt", "name": "Episode IV"},
    {"path": "data/sw_scripts/SW_EpisodeV.txt", "name": "Episode V"},
    {"path": "data/sw_scripts/SW_EpisodeVI.txt", "name": "Episode VI"},
]

# Load and merge data
scripts = load_and_merge_data(characters_file, script_files)

# Group by movie and homeworld to calculate total word count
planet_screen_time = scripts.groupby(["movie", "character"])["word_count"].sum().reset_index()

# Replace NaN homeworlds with "Unknown"
planet_screen_time["character"].fillna("Unknown", inplace=True)

# Pivot data for easier plotting
pivot_data = planet_screen_time.pivot(index="movie", columns="character", values="word_count").fillna(0)

# Plot the data
plt.figure(figsize=(14, 8))
pivot_data.plot(kind="bar", stacked=True, figsize=(14, 8), colormap="tab20")
plt.title("Screen Time by Planet Across Movies", fontsize=16)
plt.xlabel("Movie", fontsize=12)
plt.ylabel("Total Word Count (Screen Time)", fontsize=12)
plt.legend(title="Planet of Origin", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("screen_time.png")
plt.show()

