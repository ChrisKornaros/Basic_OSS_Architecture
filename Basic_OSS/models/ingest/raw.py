# Import the required dependencies
import requests
import duckdb
import pandas as pd
from datetime import datetime, timedelta


def read_api_key(file_path):
    """
    Reads the API key from a file.

    Args:
        file_path (str): Path to the file containing the API key.

    Returns:
        str: The API key.
    """
    with open(file_path, "r") as file:
        return file.read().strip()


def construct_url(api_key, start_date, end_date):
    """
    Constructs the API URL.

    Args:
        api_key (str): The API key.
        start_date (str): The start date for the API query.
        end_date (str): The end date for the API query.

    Returns:
        str: The constructed API URL.
    """
    return f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}"


def fetch_data(url):
    """
    Fetches data from the API.

    Args:
        url (str): The API URL.

    Returns:
        dict: The JSON response from the API.

    Raises:
        Exception: If the API request fails.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}")


def process_data(data, date):
    """
    Processes the API response data.

    Args:
        data (dict): The JSON response from the API.
        date (str): The date for which to process the data.

    Returns:
        DataFrame: The processed data as a pandas DataFrame.
    """
    return pd.json_normalize(data["near_earth_objects"][date])


def store_data_in_duckdb(con, data):
    """
    Stores the processed data in DuckDB.

    Args:
        con (duckdb.DuckDBPyConnection): The DuckDB connection.
        data (DataFrame): The processed data.
    """
    con.sql("""
        CREATE TABLE IF NOT EXISTS asteroids AS
        SELECT * EXCLUDE(nasa_jpl_url, close_approach_data, 'links.self')
        , unnest(close_approach_data, recursive := true)
        FROM data
    """)


def main():
    """
    Main function to execute the data ingestion process.
    """
    api_key_path = "/Users/chriskornaros/Documents/local-scripts/.api_keys/nasa/key.txt"
    api_key = read_api_key(api_key_path)
    start_date = datetime.strptime("1900-01-01", "%Y-%m-%d")
    end_date = datetime.today()

    con = duckdb.connect("test.duckdb")

    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=7)
        url = construct_url(
            api_key, current_date.strftime("%Y-%m-%d"), next_date.strftime("%Y-%m-%d")
        )

        try:
            data = fetch_data(url)
            for date in data["near_earth_objects"]:
                flat_data = process_data(data, date)
                store_data_in_duckdb(con, flat_data)
        except Exception as e:
            print(
                f"Failed to fetch data for {current_date.strftime('%Y-%m-%d')} to {next_date.strftime('%Y-%m-%d')}: {e}"
            )

        current_date = next_date

    con.close()


if __name__ == "__main__":
    main()
