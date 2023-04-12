import streamlit as st
from transformers import pipeline
import time


def main():
    st.title("😃 Sentiment Analyzer 😣")
    st.write("*Note: it will take up to 30 seconds to run the app.*")

    form = st.form(key="sentiment-form")
    user_input = form.text_area("Enter your text")
    submit = form.form_submit_button("Submit")

    if submit:
        classifier = pipeline("sentiment-analysis")
        result = classifier(user_input)[0]
        label = result["label"]
        score = result["score"]
        with st.spinner("Wait for it..."):
            time.sleep(1)
        if label == "POSITIVE":
            st.success(f"{label} sentiment (score: {score})")
        else:
            st.error(f"{label} sentiment (score: {score})")


if __name__ == "__main__":
    main()
