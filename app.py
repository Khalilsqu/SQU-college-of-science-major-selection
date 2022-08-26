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


sheet_url = st.secrets["private_gsheets_url1"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')


@st.cache(allow_output_mutation=True)
def convert_to_df():
    df = pd.DataFrame(rows)
    df.columns = df.columns.str.replace('_', ' ').str.strip()
    df['Majors'] = df['Majors'].str.strip()
    df["Major requirements"] = df["Major requirements"].str[1:-1].str.split(
        ',').apply(lambda x: [i.strip() for i in x])

    df["Major minimum requirement"] = df["Major minimum requirement"].str[1:-1].str.split(',').apply(
        lambda x: dict(zip([m.split(":")[0] for m in x] , [m.split(":")[1] for m in x])))

    introductory_courses = list(set(df["Major requirements"].sum()))

    introductory_courses = pd.Series(introductory_courses, name="Introductory Courses")

    return df, introductory_courses


class MainApp:

    def __init__(self) -> None:
        self.df, introductory_courses = convert_to_df()

        if "introductory_courses" not in st.session_state:
            st.session_state["introductory_courses"] = introductory_courses

        with st.sidebar:
            options = [
                "Major Selection",
                "Major Choice",
                "Major Vacancies",
                "About"
            ]
            # cols = st.columns(5)
            # with cols[2]:
            #     st.image("Sultan_Qaboos_University_Logo.png", width=50)
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
        elif option_menu_selc == "Major Vacancies":
            pass
        elif option_menu_selc == "About":
            pass


if __name__ == "__main__":
    MainApp()
