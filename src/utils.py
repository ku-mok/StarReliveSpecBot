import pandas as pd


def df_all_row_to_str(df: pd.DataFrame):
    text = "```\n"
    for row in df.itertuples():
        text += f"{row[1]}|{row[2]}|{row[3]}\n"
    text += "```"
    return text


def df_two_row_to_str(df: pd.DataFrame):
    text = "```\n"
    for row in df.itertuples():
        text += f"{row[2]}|{row[3]}\n"
    text += "```"
    return text
