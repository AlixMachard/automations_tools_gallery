import streamlit as st
import streamlit.components.v1 as components
from streamlit_ace import st_ace
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
from utils.html_text_extractor import text_extractor_from_html


def main():
    st.title("📝 HTML builder")

    uploaded_file = st.file_uploader(" ")
    c1, c2 = st.columns([3, 1])

    if uploaded_file is not None:

        final_text = ""
        for line in uploaded_file:
            final_text += line.decode()

        st.session_state.catch_rand = final_text

        c2.subheader("Parameters")

        with c1.expander("Code", True):
            content = st_ace(
                value=st.session_state.catch_rand,
                language=c2.selectbox(
                    "Language mode", options=["python", "html"], index=1
                ),
                theme="dracula",
                font_size=c2.slider("Font size", 5, 24, 14),
                tab_size=c2.slider("Tab size", 1, 8, 4),
                show_gutter=c2.checkbox("Show gutter", value=True),
                auto_update=c2.checkbox("Auto update", value=True),
                readonly=c2.checkbox("Read-only", value=False),
                min_lines=45,
                key="ace",
                height=500,
            )
            st.download_button(
                "Save modifications",
                data=content,
                file_name="index.html",
            )
        st.session_state.catch_rand = content

        with c1.expander("Extract text only", False):
            try:
                df = text_extractor_from_html(st.session_state.catch_rand)
                st.markdown(f"**Title :** {df['title'][0]}")
                st.markdown(f"**Preview :** {df['preview'][0]}")
                st.markdown(f"**Body title :** {df['h1_title'][0]}")
                st.markdown(f"**Body :** {df[1][0]}")
            except:
                st.write("💔 No text to extract")
        with c1.expander("✨ Show template", False):
            components.html(st.session_state.catch_rand, height=700, scrolling=True)
    else:
        with c1.expander("Build template", False):
            content = st_ace(
                language=c2.selectbox(
                    "Language mode", options=["python", "html"], index=1
                ),
                theme="dracula",
                font_size=c2.slider("Font size", 5, 24, 14),
                tab_size=c2.slider("Tab size", 1, 8, 4),
                show_gutter=c2.checkbox("Show gutter", value=True),
                auto_update=c2.checkbox("Auto update", value=True),
                readonly=c2.checkbox("Read-only", value=False),
                min_lines=45,
                key="ace",
                height=500,
            )
            if content == "":  # Ne marche pas
                title = st.text_input("Enter template title and press enter 👇")
                if title:
                    st.download_button(
                        "Download template file",
                        data=content,
                        file_name=f"{title}.html" or "index.html",
                    )
            else:
                st.write("💔 Nothing to save")


if __name__ == "__main__":
    main()
