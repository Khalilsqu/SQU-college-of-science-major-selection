
from streamlit_lottie import st_lottie

class MajorChoice:
    def __init__(self, parent) -> None:
        lottie_coding = parent.load_lottiefile("images/under-construction-1.json")
        st_lottie(
        lottie_coding,
        height=600,
        width=600,
        key=None,
    )