import streamlit as st
import pandas as pd 
import datetime 
from streamlit import session_state as state
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from langchain.utilities import WikipediaAPIWrapper
import wikipedia
import os 

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"] 


df = pd.read_csv('statsdf.csv')

# st.title('We help you plan a digital nomad break')
# st.subheader('Where would you like to go?')
st.set_page_config(layout="wide")

def filter_data(selected_countries, max_rent, filters):
    # If countries are selected, filter by them; otherwise, include all countries
    if selected_countries:
        filtered_data = df[
            (df['Country'].isin(selected_countries)) &
            (df['Median Rent'] <= max_rent)
        ]
    else:
        filtered_data = df[df['Median Rent'] <= max_rent]

    # Apply additional filters based on user input
    for key, value in filters.items():
        if value != "All":
            # Make sure both the key (column name) and value exist in the dataframe before filtering
            if key in df.columns and value in df[key].unique():
                filtered_data = filtered_data[filtered_data[key] == value]

    return filtered_data

# Function to display countries in a grid layout
def display_countries(result):
    # Number of columns
    columns = 3

        # CSS for the border
    border_css = """
    <style>
        .border-box {
            border: 2px solid #000;
            padding: 15px;
            margin: 10px;
            text-align: center;
        }
    </style>
    """

    st.markdown(border_css, unsafe_allow_html=True)

    # Iterate through the results and display them in a grid
    for index in range(0, len(result), columns):
        # Create a row with specified number of columns
        cols = st.columns(columns)
        for col, i in zip(cols, range(index, min(index + columns, len(result)))):
            City = result.iloc[i]['City']
            Country = result.iloc[i]['Country']
            # col.markdown(f"**{City}, {Country}**")
            monthly_rent = result.iloc[i]['Median Rent']
            # col.markdown(f"Monthly Rent: ${monthly_rent}")

            content = f"""
            <div class="border-box">
                <strong>{City}, {Country}</strong><br>
                Monthly Rent: ${monthly_rent}
            </div>
            """
            col.markdown(content, unsafe_allow_html=True)
            # You can replace the following line with actual URLs for images from your dataframe or elsewhere
            # image_url = f"https://example.com/{City}.jpg"
            # col.image(image_url, caption=City)
            # col.image(caption=City)



# Load CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('style.css')

# Title and Subheader
# st.markdown('# ✨ Digital Nomad Destination Finder')
st.markdown("<h1 style='text-align: center;'>✨ Digital Nomad Destination Finder</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>✨ We help plan an itinerary for your nomad travels 🌎</h4>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
# st.markdown('We help plan an itinerary for your nomad travels 🌎')

# Sidebar Filters
st.sidebar.header('Additional filters for more tailored results 🎛️')
filter_options = ['All', 'low', 'moderate', 'moderately high', 'high']
filters = {
    'Quality of Life Index': st.sidebar.selectbox('Quality of Life (e.g., WiFi) 📶', options=filter_options),
    'Purchasing Power Index': st.sidebar.selectbox('Purchasing Power 🛡️', options=filter_options),
    'Safety Index': st.sidebar.selectbox('Safety (e.g., Cleanliness) 🧼', options=filter_options),
    'Health Care Index': st.sidebar.selectbox('Health Care (e.g., Community) 👥', options=filter_options), 
}

# User Inputs in Columns
col1, col2 = st.columns([2, 2])

with col1:
    selected_countries = st.multiselect('Select the countries you want to spend time in 🗺️', df['Country'].unique())
    # selected_timeframe = st.date_input('Select the timeframe you want to be a digital nomad 📅', min_value=datetime.date.today())

with col2:
    max_rent = st.number_input('Choose a maximum $USD amount to pay for rent per month 💵', min_value=0, value=2000)

# Button and Results
if st.button('Find Destinations 🚀'):
    st.markdown("<br>", unsafe_allow_html=True)
    result = filter_data(selected_countries, max_rent, filters)
    if result.empty:
        st.markdown('❌ No destinations found based on your criteria.')
    else:
        display_countries(result)
        # st.markdown(f"Selected Timeframe: {selected_timeframe.strftime('%Y-%m-%d')} 🗓️")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center;'>✈️ Let's plan an itinerary for your nomad travels  </h4>", unsafe_allow_html=True)

st.markdown(
    '''
    <style>
        .center-image {
            display: flex;
            justify-content: center;
        }
    </style>
    <p></p>
    <p></p>
    <body>
        <header>
            <div>
                <div class="center-image">
                <h1>🌎 🗺️</h1>
                </div>
            </div>
        </header>
    </body>
    ''',
    unsafe_allow_html=True
)
from langchain.llms import OpenAI 

llm = OpenAI(temperature = 0.9)
from langchain.prompts import PromptTemplate 

# User Inputs in Columns
col1, col2 = st.columns([2, 2])

def get_cities_by_selected_countries(selected_countries):
    selected_cities = df[df['Country'].isin(selected_countries)]['City'].unique()
    default_option = None
    selected_cities = [default_option] + selected_cities
    return selected_cities

with col1:
    default_option = None
    city_options = [default_option] + df['City'].unique().tolist()
    city = st.selectbox('Select the city you want to spend time in 🗺️', city_options)
   
with col2:
    timespan = st.number_input('How many days would you like to spend here ?', min_value=1, max_value=60, value=10)

print(city)

prompt = PromptTemplate(input_variables = ["city", 'timespan'], 
                        template = """I want to spend {timespan} days in {city} as a digital nomad. I will be working remotely 
                        for my current company, hence I need recommendations for: 1 monthly coworking space, 3 cafes and
                        2-3 potential tourist attractions I can visit or activities I can do.""")

# llm(prompt.format(city = city, timespan = timespan))

if st.button('Generate Itineary 🚀'):
    st.markdown("<br>", unsafe_allow_html=True)
    result = llm(prompt.format(city = city, timespan = timespan))

    st.text_area("Here's what we recommend:", result, height = 10)
        # st.markdown(f"Selected Timeframe: {selected_timeframe.strftime('%Y-%m-%d')} 🗓️")
