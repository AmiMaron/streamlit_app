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
category_options = ['All Categories'] + list(data['product_category'].unique())
selected_category = st.sidebar.selectbox('Select Product Category', category_options)

# Filter data based on selected category
if selected_category != 'All Categories':
    filtered_data = data[data['product_category'] == selected_category]
else:
    filtered_data = data

# Show filtered data
st.write(f"Data for {selected_category}:", filtered_data)

# Display statistics of ratings
st.write(f"Statistics of Ratings for {selected_category}:", filtered_data['rate'].describe())

# Urgent items (minimum rating) across all categories
urgent_items = data[data['rate'] == data['rate'].min()]
st.subheader('Most Urgent Items Across All Categories')
st.write(urgent_items)

# Visualization of rating distribution
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='rate', ax=ax)
ax.set_title(f'Distribution of Ratings for {selected_category}')
st.pyplot(fig)

# Pie chart of review categories
fig, ax = plt.subplots()
filtered_data['review_category'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
ax.set_title(f'Pie Chart of Review Categories for {selected_category}')
ax.set_ylabel('')  # Hide the y-label
st.pyplot(fig)

# Product counts per category
if selected_category == 'All Categories':
    fig, ax = plt.subplots()
    sns.countplot(data=data, x='product_category', ax=ax)
    ax.set_title('Number of Products per Category')
    plt.xticks(rotation=45)
    st.pyplot(fig)
