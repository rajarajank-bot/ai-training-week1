import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# 1. Dataset read pannunga (Ungal CSV file path/name)
file_path = r"C:\Users\Admin\Desktop\employees.csv"
df = pd.read_csv(file_path)

# Summary: Before cleaning
before_rows = len(df)
before_missing = int(df.isnull().sum().sum())
before_duplicates = int(df.duplicated().sum())

# 2. Duplicates remove panna
df = df.drop_duplicates().reset_index(drop=True)

# 3. Text standardise (Trim & Title case)
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].astype(str).str.strip().str.title()

# 4. Data types fix panna
for col in df.columns:
    col_l = col.lower()
    if 'date' in col_l or 'join' in col_l or 'dob' in col_l:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    elif df[col].dtype == 'object' and df[col].nunique() < 20:
        df[col] = df[col].astype('category')

# 5. Missing values handle panna
for col in df.columns:
    if df[col].isnull().sum() > 0:
        if df[col].dtype.name in ['int64', 'float64']:
            df[col] = df[col].fillna(df[col].median())
        elif df[col].dtype.name in ['object', 'category']:
            mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
            df[col] = df[col].fillna(mode_val)
        elif 'datetime' in df[col].dtype.name:
            df[col] = df[col].bfill().ffill()

# 6. Outlier detection (IQR Rule) & clip
for col in df.select_dtypes(include=[np.number]).columns:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    df[col] = np.clip(df[col], q1 - 1.5 * iqr, q3 + 1.5 * iqr)

# Summary: After cleaning
summary_df = pd.DataFrame({
    'Metric': ['Rows', 'Missing Values', 'Duplicates'],
    'Before': [before_rows, before_missing, before_duplicates],
    'After': [len(df), int(df.isnull().sum().sum()), int(df.duplicated().sum())]
})

print("--- SUMMARY TABLE ---")
print(summary_df.to_string(index=False))

# 7. Local CSV save
df.to_csv("clean_data.csv", index=False)
print("\n'clean_data.csv' saved!")

# 8. PostgreSQL-kku push panna (Database: project_db)
# "YOUR_PASSWORD" edathula unga postgres password pottukonga
db_url = "postgresql://postgres:raja@localhost:5432/project_db"
engine = create_engine(db_url)

# Cleaned data-vai 'cleaned_employee_data' table-aga save seigirom
df.to_sql('cleaned_employee_data', engine, if_exists='replace', index=False)
print("Data successfully loaded into PostgreSQL database ('project_db')!")
db_url = "postgresql+psycopg://postgres:raja@localhost:5432/project_db"