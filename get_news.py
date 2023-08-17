import pandas as pd 
import numpy as np
import json
from newsapi import NewsApiClient
import os 

NEWSAPI = os.getenv('NEWS')

df = pd.read_csv("statsdf.csv")

# Initialize the client with your API key
newsapi = NewsApiClient(api_key=NEWSAPI)

# Define a function to fetch top 3 headlines for a given country code
def fetch_headlines(country_code):
    try:
        response = newsapi.get_top_headlines(language='en', country=country_code.lower(), page_size=3)
        if response['status'] == 'ok':
            return [(article['title'], article['description'], article['url']) for article in response['articles']]
    except Exception as e:
        print(f"Error fetching articles for {country_code}: {e}")
    return []

# Read the CSV to get the unique countries and their codes
unique_countries = pd.read_csv("unique_countries.csv")

# Fetch the top 3 articles for each country and store in a dataframe
all_articles = []

for _, row in unique_countries.iterrows():
    country = row['Country']
    country_code = row['Country Code']
    
    articles = fetch_headlines(country_code)
    for title, description, url in articles:
        all_articles.append({
            'Country': country,
            'Country Code': country_code,
            'Article Title': title,
            'Article Description': description,
            'Article URL': url
        })

# Convert the collected articles to a dataframe
df_articles = pd.DataFrame(all_articles)

# Save the dataframe to a CSV (optional)
df_articles.to_csv("top_articles_per_country.csv", index=False)

print("Fetching complete. Data saved to top_articles_per_country.csv.")



