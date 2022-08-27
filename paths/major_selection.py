import streamlit as st
import pandas as pd
from annotated_text import annotated_text
from streamlit_lottie import st_lottie


class MajorSelection:
    def __init__(self, parent, df) -> None:

        self.parent = parent

        self.sidebar(df)
        self.mainpage(df)

    def sidebar(self, df):
        with st.sidebar:
            if "major_selction_box_state" not in st.session_state:
                st.session_state["major_selction_box_state"] = df['Majors'].loc[0]

            st.selectbox("What major do you want to specialize in",
                         options=df['Majors'],
                         index=df['Majors'].values.tolist().index(
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
                """,
                format="%.2f"
            )

    def major_selction_box_fun(self):
        st.session_state["major_selction_box_state"] = st.session_state["major_selction_box_key"]
        if "satify_chxbox_state" in st.session_state:
            st.session_state["satify_chxbox_state"] = False

    def major_selction_slider_fun(self):
        st.session_state["major_selction_number_state"] = st.session_state["major_selction_number_key"]

    def mainpage(self, df):
        st.info(
            "You have chosen to specialize in **{}**\
            with a c.GPA of **{:.2f}**".format(
                st.session_state["major_selction_box_state"],
                st.session_state["major_selction_number_state"]
            )
        )

        st.write(
            f"##### **{st.session_state['major_selction_box_state']}** major has the following requirements")

        st.markdown("---")

        sel_maj_req_list = df["Major requirements"].loc[df["Majors"]
                                                        == st.session_state["major_selction_box_state"]].values[0]

        sel_maj_req_list_min = df["Major minimum requirement"].loc[df["Majors"]
                                                                  == st.session_state["major_selction_box_state"]].values[0]

        sel_maj_req_list_min["LANC2058"] = "D"

        sel_maj_req_list_min = {
            "Compulsory course": sel_maj_req_list_min.keys(),
            "Minimum required grade": sel_maj_req_list_min.values()
        }

        df_min_req = pd.DataFrame.from_dict(sel_maj_req_list_min)
        df_min_req.index +=1

        df_min_req = df_min_req.transpose()

        numb_course_required = len(sel_maj_req_list)

        st.write("##### 1. Required Courses")
        annotated_text(
            "Before applying to ",
            (
                st.session_state['major_selction_box_state'],
                df['Department'][df["Majors"] ==
                                    st.session_state['major_selction_box_state']] + " Department",
                '#afa',
                'red'
            ),
            " you must have completed these compulsory courses successfully"
        )

        df_required_courses = pd.DataFrame(
            sel_maj_req_list,
            columns=['Compulsory course'],
            index=[i + 1 for i in range(numb_course_required)]
        )

        st.dataframe(df_min_req.style.applymap
                     (lambda x: 'background-color : yellow' if x == "LANC2058" else ''))

        df_required_courses = df_required_courses.transpose()

        introductory_courses_list = st.session_state["introductory_courses"][
            ~st.session_state["introductory_courses"].isin(
                df_required_courses.transpose()['Compulsory course'])
        ]

        introductory_courses_list = introductory_courses_list.reset_index(
            drop=True)
        introductory_courses_list.index += 1


        if numb_course_required == 3:
            st.write(
                "Additionally you must have successfully completed at least **ONE** course from the following introductory courses with \
                    a minimum grade of D")
            st.dataframe(pd.DataFrame(introductory_courses_list).transpose())
        if numb_course_required == 2:
            st.write(
                "Additionally you must have successfully completed at least **TWO** courses from the following introductory courses with \
                    a minimum grade of **D** in each course")
            st.dataframe(pd.DataFrame(introductory_courses_list).transpose())

        if "satify_chxbox_state" not in st.session_state:
            st.session_state["satify_chxbox_state"] = False

        col1, col2 = st.columns([3, 1])

        with col1:

            st.checkbox(
                f"Do you satisfy these course requirements to major in {st.session_state['major_selction_box_state']}",
                value=st.session_state["satify_chxbox_state"],
                key="satify_chxbox_key",
                on_change=self.satify_chxbox_fun,
                help="Tick mark this box if you have completed all required courses"

                )
        with col2:
            lottie_coding1 = self.parent.load_lottiefile("images\\checkmark.json")
            st_lottie(
            lottie_coding1,
            height=100,
            width=80,
            key=None,
        )
        with st.expander("More information"):
            st.write("If not sure about whether you completed course requirement or not. Visit this \
                 [site](https://www.squ.edu.om/science/Academic-Programs/Undergraduate) for more clarification \
            ")

        st.markdown("---")
        st.write("##### 2. Required c.GPA")

        minimum_cgpa_major = df["Cumulative GPA requirement"].loc[df["Majors"] == st.session_state['major_selction_box_state']]

        st.info(f"The required cumulative GPA to specialize in \
            **{st.session_state['major_selction_box_state']}** is **{minimum_cgpa_major.values[0]:0.2f}**")

        if st.session_state["major_selction_number_state"] >= minimum_cgpa_major.values[0]:
            if st.session_state["satify_chxbox_state"]:
                st.success(f"Congratulation. You can apply for {st.session_state['major_selction_box_state']}")

                st.write(f"Please send an email to Dr/Prof. \
                    **{df['Representative'][df['Majors'] == st.session_state['major_selction_box_state']].values[0]}**\
                         at {df['Representative Email'][df['Majors'] == st.session_state['major_selction_box_state']].values[0]} \
                            for further inquiries")
                if "show balloons" in st.session_state:
                    if st.session_state["show balloons"]:
                        st.balloons()
                st.session_state["show balloons"] = False
                lottie_coding3 = self.parent.load_lottiefile("images\\76212-student-transparent.json")
                st_lottie(
                lottie_coding3,
                height=600,
                width=600,
                key=None,
            )
            else:
                st.error(f"Unfortunately. You cannot apply to {st.session_state['major_selction_box_state']} \
                    since you have not completed the required courses. Keep Studying!")
                st.session_state["show balloons"] = True

                lottie_coding3 = self.parent.load_lottiefile("images\completecourses.json")
                st_lottie(
                lottie_coding3,
                height=600,
                width=600,
                key=None,
            )
        else:
            st.error(f"Unfortunately. You cannot apply to {st.session_state['major_selction_box_state']} \
                    since your c.GPA is lower than {minimum_cgpa_major.values[0]}. Study Harder")
            st.session_state["show balloons"] = True
            lottie_coding2 = self.parent.load_lottiefile("images\\studyharder.json")
            st_lottie(
            lottie_coding2,
            height=600,
            width=600,
            key=None,
        )

    def satify_chxbox_fun(self):
        st.session_state["satify_chxbox_state"] = st.session_state["satify_chxbox_key"]
