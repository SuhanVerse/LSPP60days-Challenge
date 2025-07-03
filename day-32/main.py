import pandas as pd
def main():
    csv_path = "/home/xlegion/RUST/LSPP60days-Challenge/day-32/data/music.csv"
    df = pd.read_csv(csv_path)

    print()
    print("== DataFrame Head ==")
    print(df.head(), "\n")

    print("== DataFrame Info ==")
    df.info()
    print()

    print("== DataFrame Shape ==")
    print(df.shape, "\n")

    print("== Summary Statistics ==")
    # Only numeric columns will show up here
    print(df.describe(), "\n")

    # 3. Show column names and dtypes
    print("== Columns & dtypes ==")
    for col, dtype in df.dtypes.items():
        print(f" - {col}: {dtype}")

if __name__ == "__main__":
    main()
    print()