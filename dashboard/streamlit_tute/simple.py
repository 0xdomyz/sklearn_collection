import pandas as pd
import streamlit as st


def get_df():
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [10, 20, 30, 40]})
    return df


"""
# My first app
Here's our first attempt at using data to create a table:
"""

df = get_df()
st.line_chart(df)
number = st.slider("Pick a number", 0, 100)
