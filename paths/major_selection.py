import streamlit as st

class MajorSelection:
    def __init__(self, parent, df) -> None:

        self.sidebar(df)
        self.mainpage(df)

    def sidebar(self, df):
        with st.sidebar:
            if "major_selction_box_state" not in st.session_state:
                st.session_state["major_selction_box_state"] = df[df.columns[0]].loc[0]

            st.selectbox("What major do you want to specialize in",
                         options=df[df.columns[0]],
                         index=df[df.columns[0]].values.tolist().index(
                             st.session_state["major_selction_box_state"]),
                         key="major_selction_box_key",
                         on_change=self.major_selction_box_fun,
                         help="Choose the Major you want to be enrolled in"
                         )

            if "major_selction_number_state" not in st.session_state:
                st.session_state["major_selction_number_state"] = 2.

            st.number_input(
                "What is you current cumulative GPA",
                min_value=0.,
                max_value=4.,
                step=0.01,
                value=st.session_state["major_selction_number_state"],
                key="major_selction_number_key",
                on_change=self.major_selction_slider_fun,
                help="""Type in your current cumulative GPA.\
                This can be found in your transcript stated as c.GPA
                """
            )

    def major_selction_box_fun(self):
        st.session_state["major_selction_box_state"] = st.session_state["major_selction_box_key"]

    def major_selction_slider_fun(self):
        st.session_state["major_selction_number_state"] = st.session_state["major_selction_number_key"]

    def mainpage(self, df):
        st.info(
            "You have chosen to specialize in **{}**\
            with a c.GPA of **{}**".format(
                st.session_state["major_selction_box_state"],
                st.session_state["major_selction_number_state"]
            )
        )

        st.write(f"{st.session_state['major_selction_box_state']} major has the following requirements")

        sel_maj_req_list = df["Major requirements"].loc[df["Majors"] == st.session_state["major_selction_box_state"]].values[0]
