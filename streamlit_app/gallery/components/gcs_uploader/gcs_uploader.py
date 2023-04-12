import streamlit as st
import os
from google.cloud import storage


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/cloudstorage.json"
# os.environ[
#     "GOOGLE_APPLICATION_CREDENTIALS"
# ] = "/home/alixmachard/workspace/dirty/aTg/streamlit_app/credentials/cloudstorage.json"
BUCKET_NAME = "datacenter_shared_datas"
EMAILS_TEMPLATES_PATH = "/templates/"


def main():
    st.title("📁 Upload to Google Cloud Storage")
    storage_client = storage.Client(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

    version = st.text_input("Version")

    if st.button("Upload to GCS"):
        try:
            # st.write(st.session_state.catch_rand)
            bucket = storage_client.get_bucket(BUCKET_NAME)
            blob = bucket.blob(
                f"/data-storage/crm/templates/fr/demo_r_d/{version}/index2.html"
            )
            st.write(blob)
            st.write(
                "Successfully uploaded ",
                blob.upload_from_filename(
                    filename="/home/alixmachard/workspace/dirty/streamlit_app/templates/index2.html"
                ),
            )

        except:
            st.write("💔 Nothing to upload on gcs")


if __name__ == "__main__":
    main()
