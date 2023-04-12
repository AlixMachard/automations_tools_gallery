import streamlit as st

from gallery import apps
from gallery.components import (
    html_builder,
    gcs_resources,
    gcs_uploader,
    pipeline_graph,
    pipeline_reader,
    clip_search,
    sentiment_analysis,
    elastic_search,
    pipeline_search,
)
from gallery.utils.page import page_group


def main():

    page = page_group("p")

    with st.sidebar:
        st.title("🎈 Tools")

        with st.expander("✨ Apps", True):
            with st.expander("HTML", False):
                page.item("Template builder", html_builder.html_builder_app)
            with st.expander("GCS", False):
                page.item("GCS Resources", gcs_resources.gcs_resources)
                page.item("GCS Uploader", gcs_uploader.gcs_uploader)
            with st.expander("Pipeline", False):
                page.item("Pipeline Builder", pipeline_graph.pipeline_graph)
                page.item("Pipeline Reader", pipeline_reader.pipeline_reader)
                page.item("Pipeline Search Engine", pipeline_search.pipeline_search)
            with st.expander("Misc", False):
                page.item("CLIP Search", clip_search.clip_search)
                page.item("Sentiment analyzer", sentiment_analysis.sentiment_analysis)
                page.item("Search engine", elastic_search.elastic_search)

    page.show()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Automations tools gallery by Alix", page_icon="🎈", layout="wide"
    )
    main()
