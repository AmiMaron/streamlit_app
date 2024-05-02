import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
data = pd.read_excel("updated_categories_reviews_corrected.xlsx")

# Safe division function
def safe_divide(numerator, denominator):
    return numerator / denominator if denominator else 0

# Calculate component scores with safe division
data['actuality_score'] = data.apply(lambda x: safe_divide(x['negative_rates_past_30_days'], x['num_of_negativ_rates']), axis=1)
data['quantity_score'] = data['negative_rates_past_30_days']
data['negativity_score'] = 5 - data['rate_average']

# Assign weights
weight_actuality = 0.3
weight_quantity = 0.4
weight_negativity = 0.3

# Calculate new urgency score
data['urgency_score'] = (data['actuality_score'] * weight_actuality) + \
                        (data['quantity_score'] * weight_quantity) + \
                        (data['negativity_score'] * weight_negativity)

# Normalize urgency_score to be between 0 and 1
data['urgency_score'] = (data['urgency_score'] - data['urgency_score'].min()) / \
                        (data['urgency_score'].max() - data['urgency_score'].min())

# Filter and display the top 5 urgent products
top_urgent_products = data.nlargest(5, 'urgency_score')

# Start Streamlit app
st.title('Amazon Seller Dashboard')
st.write('This dashboard highlights products with urgent need for attention based on a sophisticated urgency score.')

# Display the filtered data with urgency scores
st.subheader('Top 5 Urgent Products Overview')
st.dataframe(top_urgent_products[['product_name', 'product_category', 'num_of_negativ_rates', 'rate_average', 'negative_rates_past_30_days', 'urgency_score']])

# Create a histogram of urgency scores
st.subheader('Distribution of Urgency Scores')
fig, ax = plt.subplots()
sns.histplot(data['urgency_score'], bins=10, kde=False, ax=ax)
plt.xlabel('Urgency Score')
plt.ylabel('Number of Products')
st.pyplot(fig)

# Generate a countplot by product category for top urgent products
st.subheader('Count of Top Urgent Products by Category')
fig, ax = plt.subplots()
sns.countplot(x='product_category', data=top_urgent_products, ax=ax)
plt.xticks(rotation=45)
plt.ylabel('Number of Products')
st.pyplot(fig)

# Recommendations section
st.subheader('Recommendations for Improvement')
st.write('Review the products listed here to identify potential quality issues or to improve customer service responses to negative feedback.')
