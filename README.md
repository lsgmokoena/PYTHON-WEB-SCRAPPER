Web Scraping and Sentiment Analysis App
Overview
This Web Scraping and Sentiment Analysis App is designed to fetch, analyze, and visualize quotes from a website. It scrapes data from the Quotes to Scrape website and performs sentiment analysis on the quotes using the TextBlob library. The app then saves the data to a CSV file and generates visualizations to help understand the sentiment distribution of the quotes.

Features:
Web Scraping: Extracts quotes, authors, and tags from the Quotes to Scrape website.
Sentiment Analysis: Analyzes the sentiment of the scraped quotes (positive, negative, neutral) using the TextBlob library.
Data Storage: Saves the scraped quotes and sentiment analysis results in a CSV file.
Visualization: Generates a bar chart to visualize the sentiment distribution of the quotes.
GUI Interface: Built using Tkinter, allowing users to trigger the web scraping and visualization process from a simple graphical interface.
Installation
Prerequisites
Ensure you have the following installed:

Python 3.x
Tkinter (comes pre-installed with Python)
Required Python libraries: requests, beautifulsoup4, pandas, textblob, matplotlib
Install Dependencies
You can install the required libraries using pip:

bash
Copy code
pip install requests beautifulsoup4 pandas textblob matplotlib
Usage
Running the Application
Clone the repository or download the project files to your local machine.

bash
Copy code
git clone https://github.com/lsgmokoena/PYTHON-WEB-SCRAPPER.git
Navigate to the project folder in your terminal and run the script:

bash
Copy code
python main.py
A Tkinter window will appear with a button to start the scraping and visualizing process.

Click the "Start Scraping and Visualizing" button to begin the process. The app will:

Fetch data from the Quotes to Scrape website.
Perform sentiment analysis on each quote.
Save the results to a CSV file (data/quotes_with_sentiments.csv).
Display a bar chart visualizing the sentiment distribution (positive, negative, neutral).
Code Breakdown
1. Fetching Data
The fetch_data(url) function fetches the HTML content of the webpage at the specified URL using the requests library.

python
Copy code
def fetch_data(url):
    """Fetch HTML content from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
2. Parsing Data
The parse_data(html) function uses BeautifulSoup to parse the HTML and extract quotes, authors, and tags.

python
Copy code
def parse_data(html):
    """Parse HTML and extract quotes, authors, and tags."""
    soup = BeautifulSoup(html, 'html.parser')
    quotes_data = []
    quote_blocks = soup.find_all('div', class_='quote')
    for block in quote_blocks:
        quote_text = block.find('span', class_='text').get_text(strip=True)
        author = block.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in block.find_all('a', class_='tag')]
        quotes_data.append({'Quote': quote_text, 'Author': author, 'Tags': ", ".join(tags)})
    return quotes_data
3. Sentiment Analysis
The analyze_sentiments(data) function uses the TextBlob library to analyze the sentiment of each quote.

python
Copy code
def analyze_sentiments(data):
    """Perform sentiment analysis on the quotes."""
    for item in data:
        text = item['Quote']
        sentiment = TextBlob(text).sentiment.polarity
        sentiment_label = 'Neutral'
        if sentiment > 0:
            sentiment_label = 'Positive'
        elif sentiment < 0:
            sentiment_label = 'Negative'
        
        item['Sentiment'] = sentiment_label
        item['Score'] = sentiment
    return data
4. Data Visualization
The visualize_data(filename) function reads the CSV file and visualizes the sentiment distribution using Matplotlib.

python
Copy code
def visualize_data(filename):
    """Visualize sentiment analysis results."""
    df = pd.read_csv(filename)
    sentiment_counts = df['Sentiment'].value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sentiment_counts.plot(kind='bar', color=['green', 'red', 'blue'], alpha=0.7)
    
    ax.set_title('Sentiment Analysis of Quotes')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Number of Quotes')
    ax.set_xticks(range(len(sentiment_counts)))
    ax.set_xticklabels(sentiment_counts.index, rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    return fig
Troubleshooting
Issue: "Permission Denied" Error when Adding Files:
Make sure that no file is open in another application (like Excel or PowerPoint) while trying to add it to Git. Close any open files, especially temporary ones like ~$ files, and try again.
Issue: Visualization not showing:
If you're running the app in a non-GUI environment (e.g., in a headless server), Matplotlib might not be able to render the visualization properly. Ensure you're running the app on a local machine with GUI support.
License
This project is licensed under the MIT License - see the LICENSE file for details.
