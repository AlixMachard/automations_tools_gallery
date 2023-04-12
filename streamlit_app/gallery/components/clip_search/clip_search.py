import streamlit as st
import ast
import requests
from st_clickable_images import clickable_images
import json
import time


def main():
    st.title("🖼️ Text to image search")

    _, c, _ = st.columns((1, 3, 1))
    c.write("Enter your query and hit enter 👇")
    if "query" in st.session_state:
        query = c.text_input(
            label="query", value=st.session_state["query"], label_visibility="hidden"
        )
    else:
        query = c.text_input(label="query", label_visibility="hidden")
    corpus = st.radio("corpus", ["Unsplash", "Movies"], label_visibility="hidden")
    if len(query) > 0:
        results = requests.get(
            "http://clip_container:5555/clip_search",
            params={"query": query, "corpus": corpus},
        )
        results = ast.literal_eval(json.loads(results.text))

        with st.spinner("Wait for it..."):
            time.sleep(1)
        clicked = clickable_images(
            [result[0] for result in results],
            titles=[result[1] for result in results],
            div_style={
                "display": "flex",
                "justify-content": "center",
                "flex-wrap": "wrap",
            },
            img_style={"margin": "2px", "height": "200px"},
        )
        if clicked >= 0:
            change_query = False
            if "last_clicked" not in st.session_state:
                change_query = True
            else:
                if clicked != st.session_state["last_clicked"]:
                    change_query = True
            if change_query:
                st.session_state["query"] = f"[{corpus}:{results[clicked][2]}]"
                st.experimental_rerun()


if __name__ == "__main__":
    main()
