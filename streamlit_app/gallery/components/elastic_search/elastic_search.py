import streamlit as st
from typing import Optional
from elasticsearch import Elasticsearch
import time


def index_search(
    es,
    index: str,
    keywords: str,
    filters: Optional[str],
    from_i: Optional[int],
    size: Optional[int],
) -> dict:
    """ """
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": keywords,
                            "fields": ["content"],
                            "default_operator": "AND",
                        }
                    }
                ],
            }
        },
        "highlight": {
            "pre_tags": ["<b>"],
            "post_tags": ["</b>"],
            "fields": {"content": {}},
        },
        # "from": from_i,
        # "size": size,
        # "aggs": {
        #     "tags": {"terms": {"field": "tags"}},
        #     "match_count": {"value_count": {"field": "_id.keyword"}},
        # },
    }
    if filters is not None:
        body["query"]["bool"]["filter"] = {"terms": {"tags": [filters]}}

    res = es.search(index=index, body=body)
    return res


def main():
    es = Elasticsearch(
        ["https://localhost:9200"],
        ca_certs=False,
        verify_certs=False,
        http_auth=("elastic", "wY7Gwy_R*-_KlyyHtV1S"),
    )

    st.title("🔎 Search engine")
    _, c, _ = st.columns((1, 3, 1))
    c.write("Enter your query and hit enter 👇")
    if "query" in st.session_state:
        query = c.text_input(
            label="query", value=st.session_state["query"], label_visibility="hidden"
        )
    else:
        query = c.text_input(label="query", label_visibility="hidden")
    if len(query) > 0:

        res = index_search(
            es=es, index="medium", keywords=query, filters=None, from_i=0, size=2
        )
        with st.spinner("Wait for it..."):
            time.sleep(1)
        # string = ""

        if res["hits"]["hits"] != []:
            for r in res["hits"]["hits"]:
                string = ""
                tags = r["_source"]["tags"]
                st.markdown(f"**{r['_source']['title']}**")
                st.caption(f"**{', '.join(tags)}**")
                for s in r["_source"]["content"].split(".")[:5]:
                    string += s + "."
                string += ".."
                st.markdown(string)
        else:
            st.write("💔 No result found")


if __name__ == "__main__":
    main()
