import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
data = pd.read_excel("updated_categories_reviews_corrected.xlsx")

# Calculate new component scores
data['actuality_score'] = data['negative_rates_past_30_days'] / data['num_of_rates']
data['quantity_score'] = data['negative_rates_past_30_days']
data['negativity_score'] = 5 - data['rate_average']  # Assuming rate_average is on a scale of 1 to 5

# Assign weights
weight_actuality = 0.4
weight_quantity = 0.4
weight_negativity = 0.2

# Calculate new urgency score
data['urgency_score'] = (data['actuality_score'] * weight_actuality) + \
                        (data['quantity_score'] * weight_quantity) + \
                        (data['negativity_score'] * weight_negativity)

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
