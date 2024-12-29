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


def process_data(data):
    """
    Processes the API response data.

    Args:
        data (dict): The JSON response from the API.

    Returns:
        DataFrame: The processed data as a pandas DataFrame.
    """
    all_data = []
    for date in data["near_earth_objects"]:
        flat_data = pd.json_normalize(data["near_earth_objects"][date])
        all_data.append(flat_data)

    if all_data:
        final_data = pd.concat(all_data, ignore_index=True)
    else:
        final_data = pd.DataFrame()

    return final_data


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
    Returns a single DataFrame object.
    """
    api_key_path = "/Users/chriskornaros/Documents/local-scripts/.api_keys/nasa/key.txt"
    api_key = read_api_key(api_key_path)

    # Define the start date and end date for the 7-day window
    start_date = datetime.strptime("1900-01-01", "%Y-%m-%d")
    end_date = start_date + timedelta(days=7)

    url = construct_url(
        api_key, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    )

    try:
        data = fetch_data(url)
        final_data = process_data(data)
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        final_data = pd.DataFrame()

    # Open a connection to the persistent database
    con = duckdb.connect("test.duckdb")

    # Store the data in DuckDB
    store_data_in_duckdb(con, final_data)

    # Verify the data was stored correctly
    result = con.sql("SELECT * FROM asteroids").fetchdf()
    print(result)

    # Close the connection
    con.close()

    return final_data


if __name__ == "__main__":
    df = main()
    print(df)
