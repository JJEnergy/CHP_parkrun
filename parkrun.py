import requests
import pandas as pd
import streamlit as st
url=st.text_input("Enter the URL to download data:",value = "https://www.parkrun.org.uk/cannonhill/results/614/")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Read the HTML content into a DataFrame
    dfs = pd.read_html(response.content)
    
    # Assuming the table you want is the first one
    parkrun_df = dfs[0]
    
    # Save the DataFrame to an Excel file
    parkrun_df.to_excel("parkrun_data.xlsx", index=False)
    
    st.write("Data saved to parkrun_data.xlsx")
else:
    st.write("Failed to download data. Status code:", response.status_code)
    
# Read the Excel file
parkrun_df = pd.read_excel("parkrun_data.xlsx")

# Extract total participants from the last row of the "Position" column
total_participants = parkrun_df['Position'].iloc[-1]

club1 = "Bournville Harriers"
club2 = "Kings Heath Running Club"

club1_participants = parkrun_df[parkrun_df['Club'] == club1].shape[0]
club2_participants = parkrun_df[parkrun_df['Club'] == club2].shape[0]


st.write("Total parkrun participants at Cannon Hill Park this morning:",total_participants)
st.write(f"Number of participants from {club1}: {club1_participants}")
st.write(f"Number of participants from {club2}: {club2_participants}")

# Filter the data for Bournville Harriers and Kings Heath Running Club
bournville_df = parkrun_df[parkrun_df['Club'] == 'Bournville Harriers']
kings_heath_df = parkrun_df[parkrun_df['Club'] == 'Kings Heath Running Club']

# Create Excel writer object
with pd.ExcelWriter('parkrun_filtered_data.xlsx') as writer:
    # Write Bournville Harriers data to sheet1
    bournville_df[['Position', 'Club']].to_excel(writer, sheet_name='Bournville Harriers', index=False)
    
    # Write Kings Heath Running Club data to sheet2
    kings_heath_df[['Position', 'Club']].to_excel(writer, sheet_name='Kings Heath Running Club', index=False)

print("Filtered data saved to parkrun_filtered_data.xlsx")

parkrun_df = pd.read_excel("parkrun_data.xlsx")

# Filter the data for Bournville Harriers and Kings Heath Running Club
bournville_df = parkrun_df[parkrun_df['Club'] == 'Bournville Harriers']
kings_heath_df = parkrun_df[parkrun_df['Club'] == 'Kings Heath Running Club']

# Calculate the score for each position
bournville_df['Score'] = total_participants+1 - bournville_df['Position']
kings_heath_df['Score'] = total_participants+1 - kings_heath_df['Position']

# Calculate total score for each club
bournville_score = bournville_df['Score'].sum()
kings_heath_score = kings_heath_df['Score'].sum()

st.write("Bournville Harriers score:", bournville_score)
st.write("Kings Heath Running Club score:", kings_heath_score)