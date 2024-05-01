import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
data = pd.read_excel("updated_categories_reviews_corrected.xlsx")

# Filtering out the products with poor reviews
threshold_rating = 2  # Threshold for average rating to consider as bad
urgent_products = data[(data['rate_average'] <= threshold_rating) & (data['num_of_rates'] > 20)]

# Starting Streamlit app
st.title('Amazon Seller Dashboard')
st.write('This dashboard highlights products with urgent need for attention based on customer reviews.')

# Display the filtered data
st.subheader('Urgent Products')
st.dataframe(urgent_products)

# Create a histogram of average rates for urgent products
st.subheader('Distribution of Average Ratings for Urgent Products')
fig, ax = plt.subplots()
sns.histplot(urgent_products['rate_average'], bins=5, kde=False, ax=ax)
plt.xlabel('Average Rating')
plt.ylabel('Number of Products')
st.pyplot(fig)

# Generate a countplot by product category for urgent products
st.subheader('Count of Urgent Products by Category')
fig, ax = plt.subplots()
sns.countplot(x='product_category', data=urgent_products, ax=ax)
plt.xticks(rotation=45)
plt.ylabel('Number of Products')
st.pyplot(fig)

# Final notes and suggestions section
st.subheader('Recommendations for Improvement')
st.write('Products listed here should be reviewed for potential improvements or further customer feedback analysis to understand the specific issues.')
