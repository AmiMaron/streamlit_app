import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv("amazon_reviews_processed.csv")

# Plot the distribution of the "rating (mean)" column
st.subheader("Distribution of Ratings")
fig, ax = plt.subplots()
data["rating (mean)"].plot.hist(bins=20, ax=ax)
ax.set_title("Distribution of Ratings")
ax.set_xlabel("Rating (mean)")
ax.set_ylabel("Count")
st.pyplot(fig)

# Get the most popular category from the "dominant_category" column
st.subheader("Most Popular Category")
most_popular_category = data["dominant_category"].mode()[0]
st.write(f"The most popular category is: {most_popular_category}")

# Calculate the worst products based on rating and number of reviews
st.subheader("5 Worst Rated Products")
data['weighted_rating'] = data['rating (mean)'] * data['number of reviews']
worst_products = data.nsmallest(5, 'weighted_rating')[['title', 'rating (mean)', 'number of reviews']]
fig, ax = plt.subplots()
ax.barh(worst_products['title'], worst_products['weighted_rating'], color='red')
ax.set_title("5 Worst Rated Products")
ax.set_xlabel("Weighted Rating")
ax.set_ylabel("Product Title")
st.pyplot(fig)
