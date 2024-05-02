import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
data = pd.read_excel("updated_categories_reviews_corrected.xlsx")

# Normalize the 'num_of_rates' and 'negative_rates_past_30_days'
data['norm_num_of_rates'] = data['num_of_rates'] / data['num_of_rates'].max()
data['norm_negative_rates'] = data['negative_rates_past_30_days'] / data['negative_rates_past_30_days'].max()

# Calculate urgency score with arbitrary weights for demonstration
weight_negative = 0.5
weight_num_rates = 0.3
weight_rate_average = 0.2
data['urgency_score'] = (data['norm_negative_rates'] * weight_negative) + \
                        (data['norm_num_of_rates'] * weight_num_rates) + \
                        ((5 - data['rate_average']) * weight_rate_average)

# Filter for high urgency products
urgent_threshold = data['urgency_score'].quantile(0.75)  # Adjust threshold as necessary
urgent_products = data[data['urgency_score'] >= urgent_threshold]

# Start Streamlit app
st.title('Amazon Seller Dashboard')
st.write('This dashboard highlights products with urgent need for attention based on a sophisticated urgency score.')

# Display the filtered data with urgency scores
st.subheader('Urgent Products Overview')
st.dataframe(urgent_products[['product_name', 'product_category', 'num_of_rates', 'rate_average', 'negative_rates_past_30_days', 'urgency_score']])

# Create a histogram of urgency scores
st.subheader('Distribution of Urgency Scores')
fig, ax = plt.subplots()
sns.histplot(urgent_products['urgency_score'], bins=10, kde=False, ax=ax)
plt.xlabel('Urgency Score')
plt.ylabel('Number of Products')
st.pyplot(fig)

# Generate a countplot by product category for urgent products
st.subheader('Count of Urgent Products by Category')
fig, ax = plt.subplots()
sns.countplot(x='product_category', data=urgent_products, ax=ax)
plt.xticks(rotation=45)
plt.ylabel('Number of Products')
st.pyplot(fig)

# Recommendations section
st.subheader('Recommendations for Improvement')
st.write('Review the products listed here to identify potential quality issues or to improve customer service responses to negative feedback.')
