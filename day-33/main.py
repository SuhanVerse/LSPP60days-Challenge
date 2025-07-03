import pandas as pd
import os

def main():
    csv_path = "/home/xlegion/RUST/LSPP60days-Challenge/day-32/data/music.csv"
    df = pd.read_csv(csv_path)
    print("== Raw Data ==")
    print(df, "\n")

    # 2. Introduce example issues (for demonstration)
    #    - Add a duplicate row
    #    - Add a row with missing genre
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)  # duplicate of first row
    df.loc[len(df)] = ["New Song", "Unknown Artist", None, 2025]  # missing genre
    print("== After Inserting Duplicate & Missing ==")
    print(df, "\n")

    # 3. Identify duplicates
    dup_mask = df.duplicated(subset=["track_name", "artist", "year"])
    print("Duplicates found:")
    print(df[dup_mask], "\n")

    # 4. Drop duplicates
    df_clean = df.drop_duplicates(subset=["track_name", "artist", "year"])
    print("== After Dropping Duplicates ==")
    print(df_clean, "\n")

    # 5. Identify missing values
    print("Missing values per column:")
    # 6. Handle missing genres: fill with 'Unknown'
    df_clean.loc[:, "genre"] = df_clean["genre"].fillna("Unknown")
    print("== After Filling Missing Genres ==")
    print(df_clean, "\n")

    # 7. Convert 'year' to integer (ensure type)
    df_clean.loc[:, "year"] = df_clean["year"].astype(int)
    print("Year column dtype after conversion:", df_clean["year"].dtype, "\n")
    df_clean["year"] = df_clean["year"].astype(int)
    print("Year column dtype after conversion:", df_clean["year"].dtype, "\n")

    # 8. Filter: keep songs from 2000 onward
    df_filtered = df_clean[df_clean["year"] >= 2000]
    print("== Songs from Year ≥ 2000 ==")
    # 9. Save cleaned data
    out_path = "data/clean_music.csv"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df_filtered.to_csv(out_path, index=False)
    print(f"Cleaned data saved to {out_path}")

if __name__ == "__main__":
    main()
