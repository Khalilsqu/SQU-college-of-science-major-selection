import streamlit as st
from streamlit_option_menu import option_menu
import json

from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd

from paths.major_selection import MajorSelection
from paths.major_vacancies import MajorVacancies
from paths.major_choice import MajorChoice

st.set_page_config(
            "Major Selection",
            page_icon="🎓",
            layout="wide",
        )

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
            content:'Made by Khalil Al Hooti'; 
            visibility: visible;
            display: block;
            position: relative;
            #background-color: red;
            padding: 5px;
            top: 2px;
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)


@st.cache
def downloadingGoogleSheet(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


sheet_url = st.secrets["private_gsheets_url1"]
rows = downloadingGoogleSheet(f'SELECT * FROM "{sheet_url}"')

sheet_url2 = st.secrets["private_gsheets_url2"]
rows2 = downloadingGoogleSheet(f'SELECT * FROM "{sheet_url2}"')


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

@st.cache(allow_output_mutation=True)
def convert_to_df_major_vacancies():
    df = pd.DataFrame(rows2)

    keys = df.columns[2:]
    values = df.columns[2:].str[1:]
    df = df.rename(
        columns=dict(zip(keys, values))
    )

    df.columns = df.columns.str.strip()

    return df


class MainApp:

    def __init__(self) -> None:
        
        self.df, introductory_courses = convert_to_df()
        if "major_vacancies_sheet" not in st.session_state: 
            st.session_state['major_vacancies_sheet'] = convert_to_df_major_vacancies()

        if "introductory_courses" not in st.session_state:
            st.session_state["introductory_courses"] = introductory_courses

        with st.sidebar:
            options = [
                "Major Selection",
                "Major Choice",
                "Major Vacancies"
            ]
            option_menu_selc = option_menu(
                menu_title="College of Science",
                options=options,
                icons=[
                    "shuffle",
                    "diagram-3-fill",
                    "bar-chart-line"
                ],
                menu_icon="mortarboard-fill",
                default_index=0

            )

        self.go_to_page(option_menu_selc)

    def go_to_page(self, option_menu_selc):
        if option_menu_selc == "Major Selection":
            MajorSelection(self, self.df)
        elif option_menu_selc == "Major Choice":
            MajorChoice(self)
        elif option_menu_selc == "Major Vacancies":
            MajorVacancies(self)
            
    def load_lottiefile(self, filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)


if __name__ == "__main__":
    MainApp()
