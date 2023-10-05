import streamlit as st
import pandas as pd
import numpy as np

st.title('Cd')

st.subheader('C')

dropdown_values = [
    'AUS', 
    'IAH', 
    'PHX', 
    'SFO'
]

option = st.sidebar.selectbox(
   label="Region",
   options=dropdown_values
)

st.sidebar.subheader('Capabilities')

toggle_25mph = st.sidebar.toggle(
    label='25 MPH',
    value=True
)

toggle_UPL = st.sidebar.toggle(
    label='UPL',
    value=True
)

toggle_Reverse = st.sidebar.toggle(
    label='Reverse',
    value=False
)

toggle_Uturn = st.sidebar.toggle(
    label='U-Turn',
    value=False
)

df1 = pd.DataFrame({'City': dropdown_values})
df2 = pd.DataFrame({'Capability': ['25 MPH', 'UPL', 'Reverse', 'U-Turn']})

result = pd.merge(df1, df2, how='cross')

c = []

if toggle_25mph: c.append('25 MPH')
if toggle_UPL: c.append('UPL')
if toggle_Reverse: c.append('Reverse')
if toggle_Uturn: c.append('U-Turn')

result = result[(result['City'] == option) & (result['Capability'].isin(c))]

st.dataframe(
    result,
    hide_index=True
)
