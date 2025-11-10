import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Function to describe DataFrame
def describe_df(df, name):
    print(f"DataFrame: {name}")
    print(df.head(), "\n")
    
    nulls = df.isnull().sum()[df.isnull().sum() > 0]
    print(f"Null values in {name} DataFrame:")
    print(nulls if not nulls.empty else "No null values found.")
    
    print(f"Duplicate rows in {name} DataFrame: {df.duplicated().sum()}")
    print("-" * 60)

# Load and describe World Happiness dataset
df_world_happiness = pd.DataFrame(pd.read_csv('data/WorldHappiness_Corruption_2015_2020.csv'))
describe_df(df_world_happiness, "World Happiness")

# Select relevant columns for analysis
df_world_happiness = df_world_happiness[['Country', 'Year', 'happiness_score', 'gdp_per_capita', 'cpi_score','continent','health']]

# Basic statistical description
print("------------------------ Statistical Description of World Happiness Data ------------------------")
print(df_world_happiness.describe())

# Group by continent and calculate mean values for selected columns
print("------------------------ Ordered (by happiness_score) Mean Values by Continent ------------------------")
print(df_world_happiness.groupby('continent')[['happiness_score', 'cpi_score', 'gdp_per_capita']].mean().sort_values(by='happiness_score', ascending=False))

#Prepare correlation matrix
corr = df_world_happiness[['happiness_score','gdp_per_capita','cpi_score','health']].corr()

#Create two side-by-side subplots
fig, axes = plt.subplots(1, 2, figsize=(12,5))

#Left plot Heatmap
sns.heatmap(
    corr.where(~np.eye(corr.shape[0], dtype=bool)),
    annot=True,
    fmt=".2f",
    cmap="crest",
    linewidths=0.5,
    cbar_kws={'label': 'Correlation Coefficient'},
    ax=axes[0]
)
axes[0].set_title("Correlation between Key Socio-Economic Factors", fontsize=10)
axes[0].tick_params(axis='x', rotation=45)

#Right plot Stripplot with Boxplot overlay
sns.boxplot(data=df_world_happiness, x='continent', y='happiness_score', color='white', fliersize=0, ax=axes[1])
sns.stripplot(data=df_world_happiness, x='continent', y='happiness_score', jitter=True, alpha=0.6, palette='crest', ax=axes[1])

axes[1].set_title("Individual Country Happiness by Continent", fontsize=11, pad=10)
axes[1].set_xlabel("")
axes[1].set_ylabel("Happiness Score")
sns.despine(ax=axes[1])

plt.tight_layout()
plt.show()

# Filter for 2020 data first
df_2020 = df_world_happiness[df_world_happiness['Year'] == 2020].copy()

# Compute GDP per happiness ratio
df_2020['gdp_per_happiness'] = df_2020['gdp_per_capita'] / df_2020['happiness_score']

# Scatter plot CPI vs GDP/Happiness
sns.scatterplot(
    data=df_2020,
    x='cpi_score',
    y='gdp_per_happiness',
    hue='continent',
    alpha=0.75,
    edgecolor='white',
    linewidth=0.7,
    s=100,
    palette='Set2'
)

plt.title("GDP Efficiency vs Corruption (2020)", fontsize=14, pad=15, weight='bold')
plt.xlabel("Corruption Perception Index (CPI) – higher = less corruption", fontsize=11)
plt.ylabel("GDP per Happiness Unit", fontsize=11)
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.3)
sns.despine()
plt.show()