import pandas as pd
import re

# Path to the dataset
data_path = "../data/raw/BooksDataset.csv"

# Load the dataset
df = pd.read_csv(data_path)

# Debug: Display initial columns and first few rows
print("Initial dataset preview:")
print(df.head())

# 1. Remove redundant quotation marks
df = df.replace(r'"', '', regex=True)

# 2. Clean the 'Authors' column
df['Authors'] = df['Authors'].str.replace(r'^By ', '', regex=True)

# 3. Parse 'Category' column into a list of categories
if 'Category' in df.columns:
    df['Category'] = df['Category'].apply(
        lambda x: [cat.strip() for cat in str(x).split(',')] if pd.notnull(x) else []
    )

# 4. Extract numeric values from 'Price'
if 'Price' in df.columns:
    df['Price'] = df['Price'].str.extract(r'(\d+\.\d+)').astype(float)

# 5. Convert 'Publish Date' to a datetime object
if 'Publish Date' in df.columns:
    df['Publish Date'] = pd.to_datetime(
        df['Publish Date'].str.strip(),
        errors='coerce',
        format='%A, %B %d, %Y'
    )

# 6. Normalize text fields to clean extra spaces or odd formatting
def clean_text(value):
    if isinstance(value, str):
        return re.sub(r'\s+', ' ', value.strip())
    return value

for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].apply(clean_text)

# 7. Drop rows with missing critical fields
required_columns = ['Title', 'Authors', 'Category']
df = df.dropna(subset=required_columns)

# Debug: Display cleaned data sample
print("Cleaned dataset preview:")
print(df.head())

# Save the cleaned dataset
cleaned_data_path = "../data/processed/BooksDataset_cleaned.csv"
df.to_csv(cleaned_data_path, index=False)

print(f"Cleaned dataset saved to: {cleaned_data_path}")
