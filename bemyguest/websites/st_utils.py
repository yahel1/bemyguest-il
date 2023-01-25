from datetime import datetime

import pandas as pd
import streamlit as st

from bemyguest.websites.connections import get_grades_df, write_to_grades_sheet


def enter():
    st.markdown("<br>", unsafe_allow_html=True)


def convert_to_rtl(x: str) -> str:
    rtl_x = f""" <p style="font-family:sans-serif; font-size: 42px;"> <div dir="rtl"> {x} </div> </p>"""
    return rtl_x


def get_grade(label: str, best_option: str) -> int:
    x = st.radio(
        label,
        options=range(1, 11),
        horizontal=True,
        format_func=lambda x: x if ((x != 1) and (x != 10)) else ("אוכל צבא" if x == 1 else best_option),
    )
    enter()
    return x


def write_grades(**kwargs):
    existing_df = get_grades_df()
    df = pd.DataFrame.from_dict({k: [v] for k, v in kwargs.items()})
    df["submit_time"] = datetime.now()
    is_row_exist = (existing_df["grader_name"] == kwargs["grader_name"]) & (
        existing_df["host_name"] == kwargs["host_name"]
    )
    if is_row_exist.any():
        st.title("כבר הגשת למארחים האלו!")
    elif kwargs["grader_name"] in kwargs["host_name"]:
        st.title("אתה לא יכול לנקד את עצמך!")
    else:
        write_to_grades_sheet(df)
        st.title("הציונים הוגשו!")
