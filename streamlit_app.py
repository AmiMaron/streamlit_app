import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
data = pd.read_excel("updated_categories_reviews_corrected.xlsx")

# Title of the dashboard
st.title('Amazon Seller Dashboard')

# Sidebar for user inputs
st.sidebar.header('User Input Features')
selected_category = st.sidebar.selectbox('Select Product Category', data['product_category'].unique())

# Filter data based on selected category
filtered_data = data[data['product_category'] == selected_category]

# Show filtered data
st.write("Filtered Data:", filtered_data)

# Display statistics
st.write("Statistics of Ratings:", filtered_data['rate'].describe())

# Visualization of rating distribution
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='rate', ax=ax)
ax.set_title('Distribution of Ratings')
st.pyplot(fig)

# Pie chart of review categories
fig, ax = plt.subplots()
filtered_data['review_category'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
ax.set_title('Pie Chart of Review Categories')
ax.set_ylabel('')  # Hide the y-label
st.pyplot(fig)

# Product counts per category
fig, ax = plt.subplots()
sns.countplot(data=data, x='product_category', ax=ax)
ax.set_title('Number of Products per Category')
plt.xticks(rotation=45)
st.pyplot(fig)
