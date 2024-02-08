# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import subprocess
def install_openpyxl():
    try:
        subprocess.run(["pip", "install", "openpyxl"])
        print("openpyxl installed sucessfully!")
    except Exception as e:
        print(f"Error installing openpyxl: {e}")
#install openpyxl
install_openpyxl()
import streamlit as st, pandas as pd

from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hot Throw Testing")



#Define function to check for a hyphen, then only return strings with hyphen
hyphen = '-'

def hyphen_string(value):
    if hyphen in value:
        return (value.split(hyphen)[0])
    else:
        return ''
# Define function to split strings and convert to integers.
def split_str(df_name):
    new_df = df_name.copy()
    new_df['HTS_split'] = df_name['HTS'].apply(hyphen_string)
    new_df['HTS'] = pd.to_numeric(new_df['HTS_split'], errors='coerce')
    return new_df.drop(columns=['HTS_split'])
#function to calculate average HTS for each person
def P_Average_HTS(df_name):
    # Group the data by 'Name' and 'Fragrance'.
  grouped_df = df_name.groupby(['Name', 'Fragrance'])

  # Calculate the average 'HTS' for each grouping of 'Name' and 'Fragrance'.
  average_hts = grouped_df['HTS'].mean()

  # Create a new DataFrame with the results.
  data = pd.DataFrame({'Name': average_hts.index.get_level_values(0),
                       'Fragrance': average_hts.index.get_level_values(1),
                       'Average_HTS': average_hts})
  def reformat(df_name):
      #rename columns, then drop them and reset index to clean up df
      df_name = df_name.rename(columns={'Fragrance': 'Frag', 'Name': 'Person'})
      df_name = df_name.drop(['Person', 'Frag'], axis=1)
      df_name = df_name.reset_index()
      return df_name

  data = reformat(data)
  return data

#function to calculate average HTS and group by whatever column you call for
def Average_HTS(df_name,name):
        Avg_HTS = df_name[df_name['Fragrance'].str.strip() == name]['HTS'].mean()
        return Avg_HTS

def run_Personal_average():
    Personal = P_Average_HTS(New_excel)
    st.write("Running Personal HT Average")
    st. write(Personal)
def run_HT_average():
    HT_average = Average_HTS(New_excel,name)
    st.write("Running HT Average")
    st. write(HT_average)

#run the function

st.title('Hot Throw Testing')
# Create a file uploader widget
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
excel = pd.DataFrame()
# Check if a file was uploaded
if uploaded_file is not None:
    # Read the uploaded file into a pandas DataFrame
    excel = pd.read_excel(uploaded_file,dtype=str,skiprows=2)

  # Check if the required columns exist in the DataFrame
    required_columns = ['Name', 'Door', 'Hot Throw Score', 'Fragrance']
    if not set(required_columns).issubset(excel.columns):
        st.error("The uploaded file does not contain the required columns.")
        st.stop()

    # Select the required columns
    excel = excel[required_columns]

    # Rename the 'Hot Throw Score' column to 'HTS'
    excel = excel.rename(columns={'Hot Throw Score': 'HTS'})

    # ***NEW***Remove rows with NaN values
    excel = excel.dropna()
    unique_name = excel['Fragrance'].unique()
    name = st.selectbox("Name of Fragrance to Analyze", unique_name)
    New_excel = pd.DataFrame()
    New_excel = split_str(excel)
    New_excel['Fragrance'] = New_excel['Fragrance'].astype(str)
    #apply functions to dataframes
    if st.button("Display Monday.com Data"):
        st.header("Monday.com Data")
        st.write(New_excel)

    st.title("Run Hot Throw Analysis")
#Buttoms to run functions for Personal and Fragrance Hot throw
    if st.button("Fragrance Hot Throw Average"):
        HT_AVG = Average_HTS(New_excel,name)
        st.write("Hot Throw Average for", name,"is",HT_AVG)

# create button to run Personal Average
    if st.button("Personal Hot Throw Average"):
        run_Personal_average()
else: st.write("Upload your Excel Document to Start")




