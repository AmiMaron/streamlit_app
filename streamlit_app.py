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

# plotting the 5 worst rated products
def plot_worst_rated(data):
    # Plotting the 5 worst rated products
    worst_rated = data.sort_values(by='rating (mean)').head(5)
    plt.figure(figsize=(10, 5))
    plt.barh(worst_rated['title'], worst_rated['rating (mean)'], color='skyblue')
    plt.title('5 Worst Rated Products')
    plt.xlabel('Rating')
    plt.ylabel('Product')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    return plt

# Get the most popular category from the "dominant_category" column
st.subheader("Most Popular Category")
most_popular_category = data["dominant_category"].mode()[0]
st.write(f"The most popular category is: {most_popular_category}")
plot_worst_rated(data)
