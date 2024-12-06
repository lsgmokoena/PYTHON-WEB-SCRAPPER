import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import os

def fetch_data(url):
    """Fetch HTML content from the given URL."""
    try:
        print(f"Fetching data from {url}...")
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_data(html):
    """Parse HTML and extract quotes, authors, and tags."""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        quotes_data = []

        # Extract all quote blocks
        quote_blocks = soup.find_all('div', class_='quote')
        for block in quote_blocks:
            quote_text = block.find('span', class_='text').get_text(strip=True)
            author = block.find('small', class_='author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in block.find_all('a', class_='tag')]
            quotes_data.append({'Quote': quote_text, 'Author': author, 'Tags': ", ".join(tags)})

        return quotes_data
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None

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

def save_to_csv(data, filename):
    """Save quotes and sentiment analysis results to a CSV file."""
    if not data:
        print("No data to save.")
        return

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

def visualize_data(filename):
    """Visualize sentiment analysis results."""
    try:
        df = pd.read_csv(filename)
        sentiment_counts = df['Sentiment'].value_counts()

        # Plot a bar chart
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
    except Exception as e:
        print(f"Error visualizing data: {e}")
        return None

def update_status(status_message):
    """Update the status text on the GUI."""
    status_label.config(text=status_message)

def show_visualization_in_gui(fig):
    """Display the Matplotlib figure in the Tkinter window."""
    if fig:
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

def start_scraping_and_visualizing():
    """Run the entire process of scraping, analysis, saving, and visualizing."""
    try:
        url = 'https://quotes.toscrape.com/'  # Website URL
        update_status("Fetching data from the website...")
        html = fetch_data(url)
        if html:
            quotes_data = parse_data(html)
            if quotes_data:
                analyzed_data = analyze_sentiments(quotes_data)
                save_to_csv(analyzed_data, 'data/quotes_with_sentiments.csv')
                update_status("Data saved. Visualizing data...")

                fig = visualize_data('data/quotes_with_sentiments.csv')
                if fig:
                    show_visualization_in_gui(fig)
                    update_status("Visualization complete.")
                else:
                    update_status("Error visualizing data.")
            else:
                update_status("No quotes found.")
        else:
            update_status("Failed to fetch HTML content.")
    except Exception as e:
        update_status(f"An error occurred: {e}")

# Tkinter setup
window = tk.Tk()
window.title("Web Scraping and Sentiment Analysis")
window.geometry("800x600")

# Button to start the scraping, analysis, and visualization process
start_button = tk.Button(window, text="Start Scraping and Visualizing", command=start_scraping_and_visualizing)
start_button.pack(pady=20)

# Status label
status_label = tk.Label(window, text="Waiting to start...", width=50, height=4)
status_label.pack(pady=10)

# The commented-out email function code
# def send_email(subject, body):
#     import smtplib
#     from email.mime.text import MIMEText
#     from email.mime.multipart import MIMEMultipart
#     
#     sender_email = "your_email@example.com"
#     receiver_email = "receiver_email@example.com"
#     password = "your_password"
#     
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))
#     
#     try:
#         server = smtplib.SMTP('smtp.example.com', 587)
#         server.starttls()
#         server.login(sender_email, password)
#         text = msg.as_string()
#         server.sendmail(sender_email, receiver_email, text)
#         server.quit()
#         print("Email sent successfully.")
#     except Exception as e:
#         print(f"Error sending email: {e}")
# 
# # Uncomment below to call the send_email function if needed
# # send_email("Test Subject", "Test Body")

# Run the Tkinter event loop
window.mainloop()
