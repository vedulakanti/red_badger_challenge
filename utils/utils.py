import csv
import pandas as pd
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def preprocess_scripts(file_path, movie_name):
    """
    Preprocess the script file and extract character and dialogue data.
    """
    try:
        rows = []

        # Attempt to open and process the file
        with open(file_path, "r") as f:
            reader = csv.reader(f, delimiter=" ", quotechar='"', skipinitialspace=True)
            next(reader)  # Skip the header row
            for row in reader:
                # Ensure the row has at least 3 columns
                if len(row) >= 3:
                    rows.append({"character": row[1], "dialogue": row[2]})
                else:
                    logging.warning(f"Malformed row skipped in file {file_path}: {row}")

        # If no valid rows were found
        if not rows:
            logging.warning(f"No valid rows found in file {file_path}.")
            return pd.DataFrame()

        # Convert to a DataFrame
        data = pd.DataFrame(rows)
        data["movie"] = movie_name
        data["word_count"] = data["dialogue"].apply(lambda x: len(str(x).split()))
        return data

    except FileNotFoundError as e:
        logging.error(f"File not found: {file_path}. Error: {e}")
        return pd.DataFrame()

    except csv.Error as e:
        logging.error(f"CSV parsing error in file: {file_path}. Error: {e}")
        return pd.DataFrame()

    except Exception as e:
        logging.error(f"Unexpected error processing file {file_path}. Error: {e}")
        return pd.DataFrame()

