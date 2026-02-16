import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# Create charts dir to place the graph plots
Path(r'charts').mkdir(exist_ok=True)

# Create data dir to place the dataset
Path(r'data').mkdir(exist_ok=True)

# Load the dataset
df = pd.read_csv('data/health_fitness_tracking_365days.csv')

# Define font styles for plots
font1 = {'family':'serif','color':'blue','size':12}
font2 = {'family':'serif','color':'darkred','size':10}

# 1. Scatter plot to show relationship between exercise minutes and calories burned
def gen_scatter_plot():
    # Sort values so the line plot makes sense
    df_sorted = df.sort_values("exercise_minutes")

    plt.figure(figsize=(8, 6))
    plt.scatter(df_sorted["exercise_minutes"], df_sorted["calories_burned"])
    plt.xlabel('Exercise Minutes', fontdict = font2)
    plt.ylabel('Calories Burned', fontdict = font2)
    plt.title("Relationship: Exercise Minutes vs Calories Burned", fontdict = font1)
    plt.savefig('charts/scatter_exercise_calories.png')
    print(f'scatter_exercise_calories.png saved to charts directory')


# 2. Do men vs women differ in exercise minutes or calories burned?
def gen_bar_chart():
    gender_group = df.groupby("gender")[["exercise_minutes", "calories_burned"]].mean()

    x = np.arange(len(gender_group))  # gender positions
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width/2, gender_group["exercise_minutes"], width, label="Exercise Minutes")
    ax.bar(x + width/2, gender_group["calories_burned"], width, label="Calories Burned")

    ax.set_xticks(x)
    ax.set_xticklabels(gender_group.index)
    ax.set_xlabel("Gender", fontdict = font2)
    ax.set_ylabel("Average Value", fontdict = font2)
    ax.set_title("Gender Differences: Exercise Minutes vs Calories Burned", font1)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig('charts/bar_exercise_cal.png')
    print(f'bar_exercise_cal.png saved to charts directory')


# 3. Does more sleep reduce stress level? (Correlation Heatmap)?
def gen_correlation_heatmap():
    numeric_cols = ['steps', 'heart_rate_avg', 'sleep_hours', 'calories_burned', 'exercise_minutes', 'stress_level', 'weight_kg', 'bmi']
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots()
    cax = ax.matshow(corr, cmap="coolwarm")
    fig.colorbar(cax)
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=90)
    ax.set_yticklabels(numeric_cols)
    ax.set_title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig('charts/correlation_heatmap.png')
    print(f'correlation_heatmap.png saved to charts directory')

# 4. Relationship: Heart rate vs Exercise minutes (Bubble chart)
def gen_bubble_chart():
    fig, ax = plt.subplots()
    ax.scatter(
        df["exercise_minutes"],
        df["heart_rate_avg"],
        s=df["calories_burned"] / 10,   # scale bubble size
        alpha=0.4
    )

    ax.set_xlabel("Exercise Minutes")
    ax.set_ylabel("Average Heart Rate")
    ax.set_title("Heart Rate vs Exercise Minutes (Bubble size = Calories Burned)")
    plt.savefig('charts/bubble_cart_heart_rate.png')
    print(f'bubble_cart_heart_rate.png saved to charts directory')

# 5. Distribution of BMI categories (Pie chart)
def pie_chart_bmi():
    def bmi_category(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    df["bmi_category"] = df["bmi"].apply(bmi_category)
    bmi_counts = df["bmi_category"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(bmi_counts, labels=bmi_counts.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("BMI Category Distribution")
    plt.savefig('charts/bmi_category_distribution.png')
    print(f'bmi_category_distribution.png saved to charts directory')

# Generate all plots sequentially
print("")
gen_scatter_plot()
gen_bar_chart()
gen_correlation_heatmap()
gen_bubble_chart()
pie_chart_bmi()

print("")
print("*" * 60)
print(f"All done. Please check the graphs under /charts directory.")
print("*" * 60)
