from datetime import datetime

import pandas as pd
import os
import streamlit as st

from dinewith.websites.connections import get_participant_df, get_grades_df, write_to_grades_sheet

dir_path = os.path.dirname(__file__)
file_path = os.path.join(dir_path, 'grades_final.csv')
hebrew_encoding = 'utf-8'


def enter():
    st.markdown('<br>', unsafe_allow_html=True)


class ParticipantDF:
    heb2eng_cols = {'קבוצה': 'group',
                    'הפורמט בו תרצו להשתתף': 'format',
                    'שם משתתפ.ת 1': 'name1',
                    'שם משתתפ.ת 2 (אם אתם מעוניינים להגיע כזוג)': 'name2'}

    @classmethod
    def get_empty_df(cls) -> pd.DataFrame:
        participant_cols = [*cls.heb2eng_cols.values()]
        return pd.DataFrame(columns=participant_cols)

    @classmethod
    def get_df(cls) -> pd.DataFrame:
        participant_cols = [*cls.heb2eng_cols.keys()]

        df = get_participant_df()
        df = df[participant_cols]
        df.rename(
            columns=cls.heb2eng_cols, inplace=True
        )
        is_valid_row = pd.to_numeric(df['group'], errors='coerce').notnull()
        df = df[is_valid_row]
        df['name2'] = df.apply(lambda row: None if row['format'] == 'יחידים+' else row['name2'], axis=1)
        return df


def convert_to_rtl(x: str) -> str:
    rtl_x = f''' <p style="font-family:sans-serif; font-size: 42px;"> <div dir="rtl"> {x} </div> </p>'''
    return rtl_x


def flatten(l):
    return [item for sublist in l for item in sublist]


def write_grades(**kwargs):
    existing_df = get_grades_df()
    df = pd.DataFrame.from_dict({k: [v] for k, v in kwargs.items()})
    df['submit_time'] = datetime.now()
    is_row_exist = (existing_df['grader_name'] == kwargs['grader_name']) & (existing_df['host_name'] == kwargs['host_name'])
    if is_row_exist.any():
        st.title('כבר הגשת למארחים האלו!')
    elif kwargs['grader_name'] in kwargs['host_name']:
        st.title('אתה לא יכול לנקד את עצמך!')
    else:
        write_to_grades_sheet(df)
        st.title('הציונים הוגשו!')


