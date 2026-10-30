import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Employee Analysis Dashboard", layout="wide")
st.title("Employee Data Analytics Dashboard")

# Cleaned data load
df = pd.read_csv(r"C:\Users\Admin\clean_data.csv")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Average Salary by Department")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    dept_sal = df.groupby('department')['salary'].mean().reset_index()
    sns.barplot(data=dept_sal, x='department', y='salary', ax=ax1, palette="Blues_r")
    ax1.set_ylabel("Average Salary (INR)")
    st.pyplot(fig1)

with col2:
    st.subheader("2. Salary Variation Across Cities")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x='city', y='salary', ax=ax2, palette="Blues_r")
    ax2.set_ylabel("Salary (INR)")
    st.pyplot(fig2)