# Day 34: Exploratory Data Analysis on clean_music.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    csv_path = "data/clean_music.csv"
    df = pd.read_csv(csv_path)
    
    print() 
    print("== DataFrame Head ==")
    print(df.head(), "\n")

    print("== DataFrame Info ==")
    df.info()
    print()

    print("== Numeric Summary ==")
    print(df.describe(), "\n")

    print("== Categorical Summary ==")
    print(df.describe(include=['object']), "\n")

    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x='year', bins=10, kde=True)
    plt.title("Distribution of Release Years")
    plt.xlabel("Year")
    plt.ylabel("Count")
    hist_path = "plots/year_distribution.png"
    plt.tight_layout()
    plt.savefig(hist_path)
    print(f"Saved histogram to {hist_path}")
    plt.close()

    plt.figure(figsize=(8, 4))
    genre_counts = df['genre'].value_counts()
    sns.barplot(x=genre_counts.index, y=genre_counts.values)
    plt.title("Songs by Genre")
    plt.xlabel("Genre")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha='right')
    bar_path = "plots/genre_counts.png"
    plt.tight_layout()
    plt.savefig(bar_path)
    print(f"Saved bar chart to {bar_path}")
    plt.close()
    
    df['title_length'] = df['track_name'].str.len()
    plt.figure(figsize=(8, 4))
    sns.scatterplot(data=df, x='year', y='title_length', hue='genre', palette='tab10')
    plt.title("Year vs. Title Length")
    plt.xlabel("Year")
    plt.ylabel("Title Length (chars)")
    scatter_path = "plots/year_vs_length.png"
    plt.tight_layout()
    plt.savefig(scatter_path)
    print(f"Saved scatter plot to {scatter_path}")
    plt.close()

if __name__ == "__main__":
    os.makedirs("plots", exist_ok=True)
    main()
