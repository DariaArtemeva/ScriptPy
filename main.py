import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
units_available_df = pd.read_csv("market-units-available-anonymized.csv")
raw_sales_df = pd.read_csv("market-units-raw-sales-anonymized.csv")

# Clean and structure
##Deleting columns with a lot of missing values
columns_to_drop = units_available_df.columns[units_available_df.isnull().mean() > 0.9]
units_available_df = units_available_df.drop(columns=columns_to_drop)

## Converting string columns to number format
def convert_columns_to_numeric(df, columns):
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

columns_to_convert_units_available = ['balcony_area', 'bath_area', 'bath_full_area', 'bath_half_area', 'bedroom_area']
units_available_df = convert_columns_to_numeric(units_available_df, columns_to_convert_units_available)

columns_to_convert_raw_sales = ['price', 'exterior_area', 'garden_area', 'terrace_area', 'balcony_area']
raw_sales_df = convert_columns_to_numeric(raw_sales_df, columns_to_convert_raw_sales)

## Handling missing values
units_available_df.fillna({'price': 0, 'price_real': 0, 'total_area': 0}, inplace=True)
raw_sales_df.fillna({'price': 0, 'floor_area': 0}, inplace=True)

# Analysis
## developer who sold the most units overall and provide a summary of their sales performance
top_developer = raw_sales_df.groupby('developer_name')['external_id'].count().sort_values(ascending=False).head(1)

##  top 5 projects with the highest number of units sold
top_projects = raw_sales_df.groupby('project_name')['external_id'].count().sort_values(ascending=False).head(5)

# Visualization
## Distribution of properties by the number of rooms
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.countplot(data=raw_sales_df, x='layout', order = raw_sales_df['layout'].value_counts().index)
plt.title('Distribution of properties by the number of rooms')
plt.xlabel('Number of rooms')
plt.ylabel('Number of properties')
plt.show()

## Top 5 projects
plt.figure(figsize=(10, 6))
top_projects_data = raw_sales_df[raw_sales_df['project_name'].isin(top_projects.index)]
sns.countplot(data=top_projects_data, x='project_name', order = top_projects.index)
plt.title('Sales of top 5 projects')
plt.xlabel('Name of project')
plt.ylabel('Number of sales')
plt.xticks(rotation=45)
plt.show()

print("Developer with the most sales:", top_developer)
print("Top 5 projects by number of sales:\n", top_projects)
