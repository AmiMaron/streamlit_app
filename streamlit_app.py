import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    # Load the data from CSV
    data = pd.read_csv("amazon_reviews_processed.csv")  # Update the path to your CSV file
    return data

def plot_rating_distribution(data):
    # Plotting the distribution of ratings
    plt.figure(figsize=(10, 5))
    plt.hist(data['rating (mean)'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    return plt

def main():
    st.title("Data Analysis App")
    
    data = load_data()
    
    st.write("## Rating Distribution")
    fig = plot_rating_distribution(data)
    st.pyplot(fig)
    
    st.write("## Most Popular Categories")
    popular_categories = data['dominant_category'].value_counts().head(10)  # You can adjust the number for top N categories
    st.table(popular_categories)

if __name__ == "__main__":
    main()
