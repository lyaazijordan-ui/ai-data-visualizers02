import pandas as pd

def analyze_data(df):
    insights = []
    num = df.select_dtypes(include="number")

    if not num.empty:
        insights.append(f"Average: {num.mean().mean():.2f}")
        insights.append(f"Max: {num.max().max():.2f}")
        insights.append(f"Min: {num.min().min():.2f}")

    return insights

def ask_ai(df, question):
    if "average" in question.lower():
        return df.select_dtypes(include="number").mean().to_dict()
    elif "max" in question.lower():
        return df.select_dtypes(include="number").max().to_dict()
    else:
        return "I can answer basic data questions (avg, max, min)"
