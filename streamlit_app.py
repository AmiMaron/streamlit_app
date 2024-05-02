import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the Excel file
data = pd.read_excel("updated_categories_reviews_corrected.xlsx")

# Safe division function
def safe_divide(numerator, denominator):
    return numerator / denominator if denominator else 0

# Calculate component scores with safe division
data['actuality_score'] = data.apply(lambda x: safe_divide(x['negative_rates_past_30_days'], x['num_of_negativ_rates']), axis=1)
data['quantity_score'] = 0.5 * data['negative_rates_past_30_days']
data['negativity_score'] = data['num_of_negativ_rates'] * (5 - data['rate_average'])

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

# Start Streamlit app
st.title('Amazon Seller Dashboard')
st.write('This dashboard highlights products with urgent need for attention based on a sophisticated urgency score.')

# Filter and display the top 5 urgent products
top_urgent_products = data.nlargest(5, 'urgency_score')

# Display the filtered data with urgency scores
st.subheader('Top 5 Urgent Products Overview')
st.dataframe(top_urgent_products[['product_name', 'product_category', 'num_of_negativ_rates', 'rate_average', 'negative_rates_past_30_days', 'urgency_score']])


# Extend the dropdown options with 'All Categories'
categories = ['All Categories'] + list(data['product_category'].unique())
selected_category = st.selectbox('Select Product Category', options=categories)

# Filter the data based on the selected category
if selected_category != 'All Categories':
    filtered_data = data[data['product_category'] == selected_category]
else:
    filtered_data = data  # Use the whole dataset if 'All Categories' is selected

# Selection of product category
# selected_category = st.selectbox('Select Product Category', options=data['product_category'].unique()) #?
# filtered_data = data[data['product_category'] == selected_category] #?

# Bar plot for average urgency score by selected product category
avg_urgency = filtered_data.groupby('review_category')['urgency_score'].mean().reset_index()
fig = px.bar(avg_urgency, x='review_category', y='urgency_score', title='Average Urgency Score by Review Category in Selected Product Category')
st.plotly_chart(fig)

# Interactive heatmap of urgency scores across product and review categories
heatmap_data = data.pivot_table(index='product_category', columns='review_category', values='urgency_score', aggfunc='mean')
fig = px.imshow(heatmap_data, labels=dict(x="Review Category", y="Product Category", color="Average Urgency Score"), title='Heatmap of Urgency Scores')
st.plotly_chart(fig)

# Average urgency score by product category
category_avg_urgency = data.groupby('product_category')['urgency_score'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='product_category', y='urgency_score', data=category_avg_urgency, ax=ax)
plt.xticks(rotation=45)
plt.xlabel('Product Category')
plt.ylabel('Average Urgency Score')
st.pyplot(fig)

# Average urgency score by review category
review_category_avg_urgency = data.groupby('review_category')['urgency_score'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='review_category', y='urgency_score', data=review_category_avg_urgency, ax=ax)
plt.xticks(rotation=45)
plt.xlabel('Review Category')
plt.ylabel('Average Urgency Score')
st.pyplot(fig)

