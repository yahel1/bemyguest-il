import os
import sys

import streamlit as st

from bemyguest.websites.st_utils import convert_to_rtl, enter, get_grade, write_grades
from bemyguest.websites.utils import flatten, ParticipantDF

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

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

df = ParticipantDF.get_df()

st.title("הגשת ציונים - בואו לאכול עם חברים שלי 5!")

st.markdown(
    convert_to_rtl("כל הכבוד! התארחתם בארוחה בבואו לאכול עם חברים שלי :) עכשיו נשאר לנקד אותה! "),
    unsafe_allow_html=True,
)
st.markdown(
    convert_to_rtl(" הציונים הם בין 1-10 כאשר: <br>  1=אוכל צבא<br>  10=חוויה אנטרופולוגית לא מהעולם הזה"),
    unsafe_allow_html=True,
)
st.markdown(
    convert_to_rtl(
        " זוגות, תגישו פעמיים- כל אחד עבור עצמו. <br> <br>"
        "  זכרו כי לא ניתן לשנות ציונים בדיעבד, "
        "ככה שאם תיתנו 10 למשתתפ.ת ואחריה יבוא מישהו מדהים עוד יותר לא תוכלו לתת לו יותר מ10."
        "  <br><br>"
    ),
    unsafe_allow_html=True,
)

group_num = st.radio("מה מספר הקבוצה? (לפי הקבוצה בוואטסאפ)", df["group"].astype(int).unique())

name_cols = ["name1", "name2"] if all(df[df["group"] == group_num]["format"] != "יחידים+") else ["name1"]
participants_names = df[df["group"] == group_num][name_cols].dropna().values

grader_name = st.selectbox("מה השם שלך?", options=flatten(participants_names))
host_name = st.selectbox("מי המארחים?", options=[", ".join(host) for host in participants_names.tolist()])

enter()

food_grade = get_grade(label="ציון לאוכל :fork_and_knife:", best_option="חוויה לא מהעולם הזה")
hagasha_grade = get_grade(label="ציון להגשה :art:", best_option="OCD")
host_grade = get_grade(label="ציון לאירוח :tropical_drink:", best_option="קרוז תענוגות")
general_grade = get_grade(label="ציון כללי :female-cook: :male-cook:", best_option="וואו")

enter()

st.markdown(convert_to_rtl("שימו לב שאחרי הגשה אין שינויים, רוצים להגיש?"), unsafe_allow_html=True)
with st.form("submission"):
    submitted = st.form_submit_button(label="Submit")
    if submitted:
        write_grades(
            group_num=group_num,
            grader_name=grader_name,
            host_name=host_name,
            food_grade=food_grade,
            hagasha_grade=hagasha_grade,
            host_grade=host_grade,
            general_grade=general_grade,
        )
