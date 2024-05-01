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

# Show filtered data for selected category
st.write("Data for Selected Category:", filtered_data)

# Display statistics for selected category
st.write("Statistics of Ratings for Selected Category:", filtered_data['rate'].describe())

# Urgent items (minimum rating) across all categories
urgent_items = data[data['rate'] == data['rate'].min()]
st.subheader('Most Urgent Items Across All Categories')
st.write(urgent_items)

# Visualization of rating distribution for selected category
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='rate', ax=ax)
ax.set_title('Distribution of Ratings for Selected Category')
st.pyplot(fig)

# Pie chart of review categories for selected category
fig, ax = plt.subplots()
filtered_data['review_category'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
ax.set_title('Pie Chart of Review Categories for Selected Category')
ax.set_ylabel('')  # Hide the y-label
st.pyplot(fig)

# Product counts per category
fig, ax = plt.subplots()
sns.countplot(data=data, x='product_category', ax=ax)
ax.set_title('Number of Products per Category')
plt.xticks(rotation=45)
st.pyplot(fig)
