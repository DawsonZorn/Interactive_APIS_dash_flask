import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import requests

# Initialize the Dash app
app = dash.Dash(__name__)

# Fetch the 311 call wait times data from the City of Winnipeg Open Data Portal
url = "https://data.winnipeg.ca/resource/vrzk-mj7v.json"
response = requests.get(url)
data = response.json()  # Parse JSON response into a Python list

# Convert data into a DataFrame
df = pd.DataFrame(data)

# Debug: print out first few rows to check data
print("First few rows of raw data:", df.head())

# Select relevant columns and handle any missing values by filling with placeholders
df = df[['timestamp', 'wait_time', 'talk_time', 'wait_time_seconds', 'talk_time_seconds']]
df.fillna({'wait_time': 'N/A', 'talk_time': 'N/A', 'wait_time_seconds': 0, 'talk_time_seconds': 0}, inplace=True)

# Convert 'timestamp' to datetime for proper time series plotting
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Ensure numeric columns are properly converted
df['wait_time_seconds'] = pd.to_numeric(df['wait_time_seconds'], errors='coerce').fillna(0)
df['talk_time_seconds'] = pd.to_numeric(df['talk_time_seconds'], errors='coerce').fillna(0)

# Debug: print out cleaned data to check for missing or incorrect values
print("Cleaned data:", df.head())

# Create a line chart to show wait times over time
fig = px.line(
    df,
    x='timestamp',
    y='wait_time_seconds',
    title='311 Call Wait Times Over Time',
    labels={'timestamp': 'Timestamp', 'wait_time_seconds': 'Wait Time (Seconds)'}
)

# Create the app layout
app.layout = html.Div([
    html.H1("City of Winnipeg 311 Call Wait Times"),

    # Display the data as a table
    dash_table.DataTable(
        id='table',
        columns=[
            {"name": col, "id": col} for col in df.columns
        ],
        data=df.to_dict('records'),
        style_table={'height': '400px', 'overflowY': 'auto'},
    ),

    # Display the wait time as a line graph
    dcc.Graph(
        id='wait-time-graph',
        figure=fig
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
