import requests

def get_names_by_date(api_url, target_date, output_file):
    """Function to get the names off the google sheets for the given date"""
    try:
        # Call the Google App Script web app
        response = requests.get(api_url, params={'date': target_date})
        response.raise_for_status()

        # Parse the names from the response
        names = response.json()

        # Truncate names to 30 characters
        truncated_names = [name[:28] for name in names]

        # Save the names to a text file
        with open(output_file, 'w') as file:
            file.write("\n".join(truncated_names))

        #print(f"Filtered names have been saved to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_names_from_file(filename):
    """
    Reads names from a file, each name on a new line, and returns them as a list.

    :param filename: The name of the file containing names.
    :return: A list of names.
    """
    try:
        with open(filename, 'r') as file:
            # Read lines, strip newline characters, and return as a list
            names = [line.strip() for line in file.readlines()]
        return names
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

