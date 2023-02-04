import os
import sys
from typing import Dict

import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from bemyguest.participant import Participant
from bemyguest.websites.connections import get_cached_grades_df

st.markdown(
    """<style>
              div[data-baseweb="select"] {direction: RTL;}
              div[class="stSlider"] {direction: RTL;}
              div[class="stNumberInput"] {direction: RTL;}
              div[class="row-widget stRadio"] {direction: RTL;}
              div[class="row-widget stSelectbox"] {direction: RTL;}
              div[data-testid="stMarkdownContainer"] {direction: RTL;}
              </style>""",
    unsafe_allow_html=True,
)

st.title("Final Grade Computation")

grades_df = get_cached_grades_df()

group_num = st.radio("מה מספר הקבוצה?", grades_df["group_num"].astype(int).sort_values().unique())
group_grades_df = grades_df[grades_df["group_num"] == group_num]

host_num = group_grades_df["host_name"].nunique()
is_couples = 2 if len(group_grades_df["host_name"].iloc[0].split(',')) == 2 else 1
if host_num * (host_num-1) * is_couples != len(group_grades_df):
    st.error("לא כל המשתתפים הגישו ניקוד!")
    # st.stop()

graders = [Participant(name, is_grader=True, is_gradee=False) for name in group_grades_df["grader_name"].unique()]
gradees = [Participant(name, is_grader=False, is_gradee=True) for name in group_grades_df["host_name"].unique()]

# calculate grades using $graders and $gradees
for p in graders:
    p_grades = group_grades_df[group_grades_df["grader_name"] == p.name]

    def build_grades_dict(col_name: str) -> Dict[Participant, int]:
        return {
            p_o: p_grades[p_grades["host_name"] == p_o.name][col_name].iloc[0]
            for p_o in gradees
            if len(p_grades[p_grades["host_name"] == p_o.name]) != 0
        }

    p.food_grades = build_grades_dict("food_grade")
    p.hagasha_grades = build_grades_dict("hagasha_grade")
    p.hospitality_grades = build_grades_dict("host_grade")
    p.general_grades = build_grades_dict("general_grade")


def display_grades(norm_grades_f, grades_attr_name) -> None:  # type: ignore
    """Displays normalized and non-normalized grades for a category."""
    st.subheader(f"{grades_attr_name} grades")
    grades = pd.DataFrame(
        {
            p.name: [
                p.__dict__[f"{grades_attr_name}_grades"][p_o]
                if (p_o in p.__dict__[f"{grades_attr_name}_grades"])
                else 0.0
                for p_o in gradees
            ]
            for p in graders
        },
        index=[p.name for p in gradees],
    )
    grades["total_score"] = grades.sum(axis=1)
    st.table(grades)
    st.text("Normalized:")
    norm_grades = pd.DataFrame(
        {p.name: [norm_grades_f(p)[p_o] if (p_o in norm_grades_f(p)) else 0.0 for p_o in gradees] for p in graders},
        index=[p.name for p in gradees],
    )
    norm_grades["total_score"] = norm_grades.sum(axis=1)

    st.table(norm_grades)

    return norm_grades["total_score"]

st.subheader('שים לב שהציונים המכריעים המשוקללים נמצאים למטה')
enter()
enter()

norm_food_grades = display_grades(Participant.norm_food_grades, "food")
norm_hagasha_grades = display_grades(Participant.norm_hagasha_grades, "hagasha")
norm_hospitality_grades = display_grades(Participant.norm_hospitality_grades, "hospitality")
norm_general_grades = display_grades(Participant.norm_general_grades, "general")

st.subheader("שקלול ציונים לפי 0.2 לכל קטגוריה ספציפית ו-0.4 לקטגוריה הכללית")
st.table((norm_food_grades + norm_hagasha_grades + norm_hospitality_grades) * 0.2 + norm_general_grades * 0.4)

st.subheader("Reported grades - for review")
st.table(group_grades_df)
