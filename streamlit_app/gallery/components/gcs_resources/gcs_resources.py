import streamlit as st
import os
import streamlit.components.v1 as components
from google.cloud import storage
import json
import time
import requests
import ast

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/cloudstorage.json"
# os.environ[
#     "GOOGLE_APPLICATION_CREDENTIALS"
# ] = "/home/alixmachard/workspace/dirty/aTg/streamlit_app/credentials/cloudstorage.json"
BUCKET_NAME = "datacenter_shared_datas"
EMAILS_TEMPLATES_PATH = "/templates/"


def main():
    st.title("☁️ List resources on Google Cloud Storage")

    try:
        # Instantiates a client
        storage_client = storage.Client(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
        scenario_list = storage_client.list_blobs(
            BUCKET_NAME,
            prefix=f"data-storage/crm/templates/fr/",
        )
        with st.form("gcs_resources", clear_on_submit=False):
            locale = st.text_input("Locale", placeholder="fr")
            scenario = st.text_input("Scenario", placeholder="welcome_confirmation")
            version = st.text_input("Version", placeholder="prod_1.1")

            if st.form_submit_button("Load resources"):
                files = storage_client.list_blobs(
                    BUCKET_NAME,
                    prefix=f"data-storage/crm/templates/{locale}/{scenario}/{version}",
                )
                result = [
                    f"{file.name.split('/')[-2]} -> {file.name.split('/')[-1]}"
                    for file in files
                    if file.name.split("/")[-1] != ""
                ]
                if result == []:
                    sentences = []
                    for f in scenario_list:
                        sentences.append(f.name.split("/")[4])

                    sentences = list(set(sentences))
                    sentences = [s for s in sentences if s]
                    result_sentences = requests.post(
                        "http://bert:5454/text_similarity",
                        params={
                            "sentences": json.dumps(sentences),
                            "query": scenario,
                        },
                    )
                    result_sentences = ast.literal_eval(
                        json.loads(result_sentences.text)
                    )
                    with st.spinner("Wait for it..."):
                        time.sleep(1)
                    st.markdown("💔 Oops an error occurred...")
                    if len(result_sentences) == 2:
                        st.markdown(
                            f"Did you mean **{result_sentences[0]}** or **{result_sentences[1]}** ?"
                        )
                    elif len(result_sentences) == 1:
                        st.markdown(f"Did you mean **{result_sentences[0]}** ?")
                elif len(result) <= 1:
                    st.write(result)
                    expander_name = "✨ Show template"
                else:
                    st.write(result)
                    expander_name = "✨ Show templates"

                with st.expander(expander_name):
                    string_template = ""
                    bucket = storage_client.bucket(BUCKET_NAME)

                    files = storage_client.list_blobs(
                        BUCKET_NAME,
                        prefix=f"data-storage/crm/templates/{locale}/{scenario}/{version}",
                    )
                    urls = []
                    for file in files:
                        string_template = ""
                        if ".html" in file.name:
                            blob = bucket.blob(file.name)
                            with blob.open("r") as f:
                                string_template += f.read()
                            urls.append(string_template)

                    for url in urls:
                        components.html(url, height=700, scrolling=True)

    except Exception as e:
        print(e)
        st.write("💔 Bad things happened")


if __name__ == "__main__":
    main()
