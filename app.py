import streamlit as st
from streamlit_option_menu import option_menu

from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd

from paths.major_selection import MajorSelection

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)


@st.cache
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

@st.cache
def convert_to_df():
    df = pd.DataFrame(rows)
    df.columns = df.columns.str.replace('_',' ')
    df["Major requirements"] = df["Major requirements"].str[1:-1].str.split(',')
    return df

class MainApp:

    def __init__(self) -> None:
        self.df = convert_to_df()
        self.df.to_csv("khalil.csv", index=False)
        with st.sidebar:
            options = [
                "Major Selection",
                "Major Choice",
                "Major Availability",
                "About"
            ]
            cols = st.columns(5)
            with cols[2]:
                st.image("Sultan_Qaboos_University_Logo.png", width=50)
            option_menu_selc = option_menu(
                menu_title="College of Science",
                options=options,
                icons=[
                    "shuffle",
                    "diagram-3-fill",
                    "bar-chart-line",
                    "file-person"
                ],
                menu_icon="mortarboard-fill",
                default_index=0

            )

        self.go_to_page(option_menu_selc)

    def go_to_page(self, option_menu_selc):
        if option_menu_selc == "Major Selection":
            MajorSelection(self, self.df)
        elif option_menu_selc == "Major Choice":
            pass
        elif option_menu_selc == "Major Availability":
            pass
        elif option_menu_selc == "About":
            pass


if __name__ == "__main__":
    MainApp()
