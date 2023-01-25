import pandas as pd

from bemyguest.websites.connections import get_participant_df


class ParticipantDF:
    heb2eng_cols = {
        "קבוצה": "group",
        "הפורמט בו תרצו להשתתף": "format",
        "שם משתתפ.ת 1": "name1",
        "שם משתתפ.ת 2 (אם אתם מעוניינים להגיע כזוג)": "name2",
    }

    @classmethod
    def get_empty_df(cls) -> pd.DataFrame:
        participant_cols = [*cls.heb2eng_cols.values()]
        return pd.DataFrame(columns=participant_cols)

    @classmethod
    def get_df(cls) -> pd.DataFrame:
        participant_cols = [*cls.heb2eng_cols.keys()]

        df = get_participant_df()
        df = df[participant_cols]
        df.rename(columns=cls.heb2eng_cols, inplace=True)
        is_valid_row = pd.to_numeric(df["group"], errors="coerce").notnull()
        df = df[is_valid_row]
        df["name2"] = df.apply(lambda row: None if row["format"] == "יחידים+" else row["name2"], axis=1)
        return df


def flatten(l):
    return [item for sublist in l for item in sublist]
