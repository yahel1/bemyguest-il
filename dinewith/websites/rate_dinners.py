import os
import sys
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dinewith.websites.utils import convert_to_rtl, flatten, enter, write_grades
from dinewith.websites.utils import ParticipantDF

st.markdown("""<style>
              div[data-baseweb="select"] {direction: RTL;}
              div[class="stSlider"] {direction: RTL;}
              div[class="stNumberInput"] {direction: RTL;}
              div[class="row-widget stRadio"] {direction: RTL;}
              div[class="row-widget stSelectbox"] {direction: RTL;}
            div[data-testid="stMarkdownContainer"] {direction: RTL;}
              </style>""", unsafe_allow_html=True)

df = ParticipantDF.get_df()
groups_num = df['group'].max()


st.title("הגשת ציונים - בואו לאכול עם חברים שלי 5!")

st.markdown(convert_to_rtl('כל הכבוד! התארחתם בארוחה בבואו לאכול עם חברים שלי :) עכשיו נשאר לנקד אותה! '),
            unsafe_allow_html=True)
st.markdown(convert_to_rtl(' הציונים הם בין 1-10 כאשר: <br>  1=אוכל צבא<br>  10=חוויה אנטרופולוגית לא מהעולם הזה'),
            unsafe_allow_html=True)
st.markdown(convert_to_rtl(' זוגות, תגישו פעמיים- כל אחד עבור עצמו. <br> <br>'
                           '  זכרו כי לא ניתן לשנות ציונים בדיעבד, '
                           'ככה שאם תיתנו 10 למשתתפ.ת ואחריה יבוא מישהו מדהים עוד יותר לא תוכלו לתת לו יותר מ10.'
                           '  <br><br>'), unsafe_allow_html=True)

group_num = st.radio("מה מספר הקבוצה? (לפי הקבוצה בוואטסאפ)", df['group'].astype(int).unique())

name_cols = ['name1', 'name2'] if all(df[df['group'] == group_num]['format'] != 'יחידים+') else ['name1']
participants_names = df[df['group'] == group_num][name_cols].dropna().values
grader_name = st.selectbox("מה השם שלך?", options=flatten(participants_names))
host_name = st.selectbox("מי המארחים?", options=[', '.join(host) for host in participants_names.tolist()])

enter()

food_grade = st.radio(
    'ציון לאוכל :fork_and_knife:',
    options=range(1, 11), horizontal=True,
    format_func=lambda x: x if ((x != 1) and (x != 10)) else ('אוכל צבא' if x == 1 else 'חוויה לא מהעולם הזה'))
enter()

hagasha_grade = st.radio(
    'ציון להגשה :art:',
    options=range(1, 11), horizontal=True,
    format_func=lambda x: x if ((x != 1) and (x != 10)) else ('אוכל צבא' if x == 1 else 'OCD'))
enter()

host_grade = st.radio(
    'ציון לאירוח :tropical_drink:',
    options=range(1, 11), horizontal=True,
    format_func=lambda x: x if ((x != 1) and (x != 10)) else ('אוכל צבא' if x == 1 else 'קרוז תענוגות'))
enter()

general_grade = st.radio(
    'ציון כללי :female-cook: :male-cook:',
    options=range(1, 11), horizontal=True,
    format_func=lambda x: x if ((x != 1) and (x != 10)) else ('אוכל צבא' if x == 1 else 'וואו'))

enter()
enter()

st.markdown(convert_to_rtl('שימו לב שאחרי הגשה אין שינויים, רוצים להגיש?'), unsafe_allow_html=True)
with st.form('submission'):
    submitted = st.form_submit_button(label='Submit')
    if submitted:
        write_grades(group_num=group_num, grader_name=grader_name, host_name=host_name,
                     food_grade=food_grade, hagasha_grade=hagasha_grade,
                     host_grade=host_grade, general_grade=general_grade)

