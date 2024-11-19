import pandas as pd
import logging
import ast  

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def calculate_human_proportion(characters_file, species_file):
    try:
        characters = pd.read_csv(characters_file)
        species = pd.read_csv(species_file)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return None
    except pd.errors.EmptyDataError as e:
        logging.error(f"Empty data error: {e}")
        return None

    characters['species_url'] = characters['species'].apply(
            lambda x: ast.literal_eval(x)[0] if pd.notnull(x) and ast.literal_eval(x) else None
        )
    species_map = {s['url']: s['name'] for _, s in species.iterrows()}
    characters['species_name'] = characters['species_url'].map(species_map)

  

    human_count = (characters['species_name'] == 'Human').sum()
    non_human_count = len(characters) - human_count

    total = human_count + non_human_count
    if total == 0:
        logging.warning("No characters found for analysis.")
        return None

    proportions = {
        "human_proportion": human_count / total,
        "non_human_proportion": non_human_count / total,
    }
    logging.info(f"Proportions calculated: {proportions}")
    return proportions


if __name__ == "__main__":
    logging.info("Starting analysis process...")
    proportions = calculate_human_proportion("data/swapi/characters.csv", "data/swapi/species.csv")
    if proportions:
        logging.info(f"Human vs Non-Human Proportions: {proportions}")
