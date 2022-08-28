import streamlit as st
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import plotly.express as px


config = {
    'toImageButtonOptions': {
        'format': 'svg',  # one of png, svg, jpeg, webp
        'filename': 'major selection',
        'height': None,
        'width': None,
        'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
    },
    "displaylogo": False,
}


class MajorVacancies:

    def __init__(self, parent=None) -> None:
        self.parent = parent

        st.session_state['major_vacancies_sheet'] = st.session_state[
            'major_vacancies_sheet'].sort_values(
                by="Major").reset_index(drop=True)

        st.session_state['major_vacancies_sheet'].index += 1
        float_col = st.session_state['major_vacancies_sheet'].select_dtypes(include=[
                                                                            'float64'])

        for col in float_col.columns.values:
            st.session_state['major_vacancies_sheet'][col] = \
                st.session_state['major_vacancies_sheet'][col].astype('int64')

        self.setup_sidebar()

        if ("major_slection_key" in st.session_state) & ("cohor_slide_state" in st.session_state):
            remaining_seat = \
                st.session_state[
                    'major_vacancies_sheet'].loc[
                    st.session_state['major_vacancies_sheet']["Major"] == st.session_state["major_slection_key"]
                ][str(st.session_state["cohor_slide_state"])].values[0]

            if remaining_seat == 0:
                st.info(f"There is no remaining seats in\
                     **{st.session_state['major_slection_key']}**\
                         for cohort **{st.session_state['cohor_slide_state']}**")

                lottie_coding2 = self.parent.load_lottiefile("images/sad.json")
                st_lottie(
                    lottie_coding2,
                    height=150,
                    width=150,
                    key=None,
                )
                st.write(f"Check with another major")
            else:
                if remaining_seat == 1:
                    st.info(f"There is only **{remaining_seat}** \
                        remaining seat in **{st.session_state['major_slection_key']}** \
                            for cohort **{st.session_state['cohor_slide_state']}**")
                else:
                    st.info(f"There are **{remaining_seat}** \
                        remaining seats in **{st.session_state['major_slection_key']}** \
                            for cohort **{st.session_state['cohor_slide_state']}**")
                lottie_coding3 = self.parent.load_lottiefile(
                    "images/apply_major.json")
                lottie_coding4 = self.parent.load_lottiefile(
                    "images/apply_major2.json")
                st.write(
                    "Go and apply. Visit assistant dean office for undergraduate studies in the college of science")
                cols = st.columns(2)
                with cols[0]:
                    st_lottie(
                        lottie_coding4,
                        height=300,
                        width=300,
                        key=None,
                    )
                with cols[1]:
                    st_lottie(
                        lottie_coding3,
                        height=300,
                        width=300,
                        key=None,
                    )

        st.markdown("---")

        st.success("Data below show major vacancies")

        st.dataframe(st.session_state['major_vacancies_sheet'])

        fig = go.Figure()

        for row in range(len(st.session_state['major_vacancies_sheet'])):
            fig.add_trace(go.Scatter(
                x=st.session_state['major_vacancies_sheet'].columns[2:],
                y=st.session_state['major_vacancies_sheet'].iloc[row, 2:],
                name=st.session_state['major_vacancies_sheet'].iloc[row, 1]
            )
            )

        fig.update_layout(title='Line Plots of Major Vacancies',
                          xaxis_title='Year',
                          yaxis_title='Vacancy number')

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=config
        )

        fig = go.Figure()

        for row in range(len(st.session_state['major_vacancies_sheet'])):
            fig.add_trace(
                go.Bar(
                    x=st.session_state['major_vacancies_sheet'].columns[2:],
                    y=st.session_state['major_vacancies_sheet'].iloc[row, 2:],
                    name=st.session_state['major_vacancies_sheet'].iloc[row, 1],
                    text=st.session_state['major_vacancies_sheet'].iloc[row, 2:].replace(
                        0, ""),
                    hoverinfo="x+y+name",
                    textposition="outside"
                )
            )

        fig.update_layout(title='Bar Plots of Major Vacancies',
                          xaxis_title='Year',
                          yaxis_title='Vacancy number')

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=config
        )
        df = st.session_state['major_vacancies_sheet'].drop(
            "Department", axis=1)
        df = df.melt(id_vars=["Major"],
                     var_name="Year",
                     value_name="Seats")

        st.write('Pie Chart of Major Vacancies')

        fig = px.sunburst(
            df,
            path=['Year', 'Major', "Seats"],
            width=700, height=700
        )

        fig.update_layout(

            margin=dict(l=0, r=10, t=0, b=0)
        )
        fig.update_traces(
            hovertemplate="%{id}"
        )

        st.plotly_chart(
            fig,
            config=config,
            use_container_width=True,
        )

    def cohor_slide_fun(self):
        st.session_state["cohor_slide_state"] = int(
            st.session_state["cohor_slide_key"])

    def major_slection_fun(self):
        st.session_state["major_slection_state"] = st.session_state["major_slection_key"]

    def setup_sidebar(self):
        with st.sidebar:

            if "cohor_slide_state" not in st.session_state:
                st.session_state["cohor_slide_state"] = int(
                    st.session_state['major_vacancies_sheet'].columns[2:][0])
            st.slider("What is your cohort",
                      min_value=int(
                          st.session_state['major_vacancies_sheet'].columns[2:][0]),
                      max_value=int(
                          st.session_state['major_vacancies_sheet'].columns[2:][-1]),
                      value=st.session_state["cohor_slide_state"],
                      step=1,
                      key="cohor_slide_key",
                      on_change=self.cohor_slide_fun,
                      help="This is the year you joined SQU"
                      )

            if "major_slection_state" not in st.session_state:
                st.session_state["major_slection_state"] = st.session_state['major_vacancies_sheet']['Major'].iloc[0]

            st.selectbox(
                "What you want to major in",
                options=st.session_state['major_vacancies_sheet']['Major'],
                index=(
                    st.session_state['major_vacancies_sheet']['Major'].values.tolist().index(
                        st.session_state["major_slection_state"]
                    )
                ),
                key="major_slection_key",
                on_change=self.major_slection_fun,
            )
