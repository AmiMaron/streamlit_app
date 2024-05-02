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

# Assuming 'review_category' is available in the data
if 'review_category' not in data.columns:
    data['review_category'] = pd.Series(['Category 1', 'Category 2', 'Category 3']).take(np.random.randint(0, 3, size=len(data)))

# Start Streamlit app
st.title('Amazon Seller Dashboard')
st.write('This dashboard highlights products with urgent need for attention based on a sophisticated urgency score.')

# Selection of product category
selected_category = st.selectbox('Select Product Category', options=data['product_category'].unique())
filtered_data = data[data['product_category'] == selected_category]

# Bar plot for average urgency score by selected product category
avg_urgency = filtered_data.groupby('review_category')['urgency_score'].mean().reset_index()
fig = px.bar(avg_urgency, x='review_category', y='urgency_score', title='Average Urgency Score by Review Category in Selected Product Category')
st.plotly_chart(fig)

# Interactive heatmap of urgency scores across product and review categories
heatmap_data = data.pivot_table(index='product_category', columns='review_category', values='urgency_score', aggfunc='mean')
fig = px.imshow(heatmap_data, labels=dict(x="Review Category", y="Product Category", color="Average Urgency Score"), title='Heatmap of Urgency Scores')
st.plotly_chart(fig)

# Time series analysis of urgency scores (assuming date field 'review_date' is available)
if 'review_date' in data.columns:
    data['date'] = pd.to_datetime(data['review_date'])
    time_series_data = data.groupby(data['date'].dt.to_period("M"))['urgency_score'].mean()
    fig, ax = plt.subplots()
    time_series_data.plot(kind='line', ax=ax)
    plt.xlabel('Month')
    plt.ylabel('Average Urgency Score')
    plt.title('Trend of Urgency Scores Over Time')
    st.pyplot(fig)

# Recommendations section
st.subheader('Recommendations for Improvement')
st.write('Review the products listed here to identify potential quality issues or to improve customer service responses to negative feedback.')
