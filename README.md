
# CS:GO Professional Player Analytics

An interactive data analytics dashboard built using Python,
pandas, Plotly, and Streamlit.

## Project Objective

To analyse historical professional CS:GO player statistics,
identify performance trends, compare players, and present
findings using interactive charts.

## Dataset

- 811 professional CS:GO players
- 41 columns
- 53 countries represented
- Historical player performance statistics

## Data Cleaning

- Identified 297 missing team values
- Replaced missing teams with "Unknown"
- Converted headshot percentages into numerical values
- Recalculated kill/death difference
- Checked for duplicate player records

## Dashboard Features

1. Player Overview
2. Combat Performance Analysis
3. Weapon and Playstyle Analysis
4. Player Comparison

## Technologies Used

- Python
- pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Jupyter Notebook

## Running the Project

Install dependencies:

pip install -r requirements.txt

Launch the dashboard:

streamlit run app.py

## Limitations

The dataset contains historical player statistics.
Team information may be missing or outdated.
The project does not analyse individual tournament results.
