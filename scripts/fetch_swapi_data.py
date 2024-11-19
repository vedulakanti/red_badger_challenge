import requests
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://swapi.dev/api/"


def fetch_data(endpoint):
    data = []
    url = f"{BASE_URL}{endpoint}"
    while url:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            result = response.json()
            data.extend(result['results'])
            url = result.get('next')
            logging.info(f"Fetched {len(result['results'])} records from {endpoint}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from {url}: {e}")
            break
    return data


def save_data(data, filename):
    if not data:
        logging.warning(f"No data to save for {filename}")
        return
    try:
        df = pd.DataFrame(data)
        df.to_csv(f"../data/swapi/{filename}", index=False)
        logging.info(f"Data saved to data/{filename}")
    except Exception as e:
        logging.error(f"Error saving data to {filename}: {e}")


if __name__ == "__main__":
    logging.info("Starting data fetching process...")
    characters = fetch_data("people/")
    save_data(characters, "characters.csv")

    species = fetch_data("species/")
    save_data(species, "species.csv")

    planets = fetch_data("planets/")
    save_data(planets, "planets.csv")
