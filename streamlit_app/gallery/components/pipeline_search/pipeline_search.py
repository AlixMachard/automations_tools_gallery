import streamlit as st
from pymongo import MongoClient
import yaml
from utils.pipeline_reader import (
    visualize_pipeline,
)
import ast
import json
import time
import requests


@st.experimental_singleton
def init_connection():
    return MongoClient(
        "mongodb+srv://history-preprod:hBI17uXkZvAFMU24@d-zoov-preprod.chg35.mongodb.net/?retryWrites=true&w=majority&authMechanism=DEFAULT"
    )


# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def get_data(corpus, search_query):
    client = init_connection()
    automation_db = client["automation"]
    pipelines_collection = automation_db["pipelines"]
    if corpus == "Name":
        query = {"id": {"$regex": search_query}}
    elif corpus == "Module":
        query = {"stages.module.name": {"$regex": search_query}}

    items = pipelines_collection.find(query)
    items = list(items)  # make hashable for st.experimental_memo
    return items


def main():
    st.title("📊 Pipelines search engine")
    _, c, _ = st.columns((1, 3, 1))

    if "query" in st.session_state:
        query = c.text_input(
            label="query", value=st.session_state["query"], label_visibility="hidden"
        )
    else:
        query = c.text_input(label="query", label_visibility="hidden")
    corpus = st.radio("corpus", ["Module", "Name"], label_visibility="hidden")
    if len(query) > 0:
        ###### Bert
        # if corpus == "Name":
        #     sentences = []
        #     client = init_connection()
        #     sentences = client["automation"]["pipelines"].find({}).distinct("name")

        #     sentences = list(set(sentences))
        #     sentences = [s for s in sentences if s]
        #     result_sentences = requests.post(
        #         "http://localhost:5454/text_similarity",
        #         params={
        #             "sentences": json.dumps(sentences),
        #             "query": query,
        #         },
        #     )
        #     result_sentences = ast.literal_eval(json.loads(result_sentences.text))
        #     with st.spinner("Wait for it..."):
        #         time.sleep(1)
        #     if len(result_sentences) == 2:
        #         st.markdown(
        #             f"Did you mean **{result_sentences[0]}** or **{result_sentences[1]}** ?"
        #         )
        #     elif len(result_sentences) == 1:
        #         st.markdown(f"Did you mean **{result_sentences[0]}** ?")
        ######
        toggle_key = 0
        items = get_data(corpus, query)

        for item in items:
            with st.expander(f"{item['name']}"):

                # pipeline = yaml.safe_load(item)
                with st.expander("Display graph"):
                    # st.write(pipeline)
                    params, nodes, return_value = visualize_pipeline(item)
                with st.expander("Module parameters"):
                    for param, node in zip(params, nodes):
                        if node.id == return_value:
                            if param != []:
                                st.markdown(f"**{node.label}**")
                                st.write(
                                    [{p.get("name"): p.get("value")} for p in param]
                                )
                            else:
                                st.markdown(f"💔 **{node.label}** has no parameter")
                with st.expander("Pipeline settings"):
                    st.markdown(f"**Sealed**: {item['sealed']}")
                    st.markdown(f"**Enabled**: {item['enabled']}")
                    st.markdown(f"**Actions enabled**: {item['actions_enabled']}")

            toggle_key += 1
        # st.write(items)
        # for item in items:
        #     st.write(f"{item['name']}")


if __name__ == "__main__":
    main()
