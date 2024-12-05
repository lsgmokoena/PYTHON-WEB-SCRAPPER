import requests  # Import the requests library to make HTTP requests
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing
import pandas as pd  # Import pandas for handling data and saving to CSV
import matplotlib.pyplot as plt  # Import matplotlib for data visualization (if needed later)

def fetch_data(url):
    """
    Fetch HTML content from the given URL.
    This function makes an HTTP request to the URL and returns the HTML content.
    """
    try:
        print(f"Fetching data from {url}...")  # Print a message indicating we are fetching data from the URL
        response = requests.get(url)  # Send GET request to the URL
        response.raise_for_status()  # Raise an exception if the request was unsuccessful (e.g., 404 or 500 error)
        return response.text  # Return the HTML content of the page
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")  # Print an error message if the request fails
        return None  # Return None if the request fails

def parse_data(html):
    """
    Parse HTML and extract the required data.
    In this case, we extract all hyperlinks (<a> tags).
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content with BeautifulSoup
        # Find all <a> tags, which represent hyperlinks in the HTML
        links = soup.find_all('a')  # Extract all <a> tags from the page
        return links  # Return the list of all <a> tags found
    except Exception as e:
        print(f"Error parsing data: {e}")  # Print an error message if parsing fails
        return None  # Return None if parsing fails

def save_to_csv(data, filename):
    """
    Save the extracted data to a CSV file.
    This function takes the extracted data and saves it as a CSV file in the specified path.
    """
    try:
        # Convert the data into a pandas DataFrame (this is used to structure the data)
        df = pd.DataFrame(data, columns=['Link'])  # Create a DataFrame with one column called 'Link'
        df.to_csv(filename, index=False)  # Save the DataFrame to a CSV file without the index
        print(f"Data saved to {filename}")  # Print a success message
    except Exception as e:
        print(f"Error saving data to CSV: {e}")  # Print an error message if saving fails

def main():
    # Website URL to scrape (this URL is for demonstration purposes)
    url = 'https://quotes.toscrape.com/'  # URL of the website to scrape
    html = fetch_data(url)  # Call the fetch_data function to get the HTML content of the page
    
    if html:  # Check if HTML content was successfully fetched
        links = parse_data(html)  # Call the parse_data function to extract links from the HTML
        if links:  # Check if any links were found
            # Extract the 'href' attribute from each <a> tag (the actual link)
            link_data = [{'Link': link.get('href')} for link in links if link.get('href')]  # Create a list of dictionaries with links
            save_to_csv(link_data, 'data/links.csv')  # Save the extracted links to a CSV file
        else:
            print("No data to save")  # Print a message if no links were found
    else:
        print("Failed to retrieve the HTML content")  # Print a message if the HTML content could not be fetched

if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly
