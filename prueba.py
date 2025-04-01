import streamlit as st
import pandas as pd

df = pd.read_excel(r"C:\Users\1069657\OneDrive - Home Depot Mexico S.A. de C.V\One Page\data.xlsx")

def main():
    st.header("One Page")
    st.dataframe(df)

main()