from fastapi import FastAPI
import numpy as np
import re
import uvicorn
import json
import pandas as pd, numpy as np
from transformers import CLIPProcessor, CLIPModel

app = FastAPI()


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def load():
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

    df = {
        0: pd.read_csv("./data.csv"),
        1: pd.read_csv("./data2.csv"),
    }

    embeddings = {
        0: np.load("./embeddings.npy"),
        1: np.load("./embeddings2.npy"),
    }

    # image_data_df["image"] = image_data_df["link"].apply(get_image)

    # embeddings = get_all_images_embedding(image_data_df, "image")

    for k in [0, 1]:
        embeddings[k] = embeddings[k] / np.linalg.norm(
            embeddings[k], axis=1, keepdims=True
        )
    return model, processor, df, embeddings


model, processor, df, embeddings = load()
source = {0: "\nSource: Unsplash", 1: "\nSource: The Movie Database (TMDB)"}


def compute_text_embeddings(list_of_strings):
    inputs = processor(text=list_of_strings, return_tensors="pt", padding=True)
    result = model.get_text_features(**inputs).detach().numpy()
    return result / np.linalg.norm(result, axis=1, keepdims=True)


@app.get("/clip_search")
def image_search(query, corpus, n_results=24):
    n_results = 24
    positive_embeddings = None

    def concatenate_embeddings(e1, e2):
        if e1 is None:
            return e2
        else:
            return np.concatenate((e1, e2), axis=0)

    splitted_query = query.split("EXCLUDING ")
    dot_product = 0
    k = 0 if corpus == "Unsplash" else 1
    if len(splitted_query[0]) > 0:
        positive_queries = splitted_query[0].split(";")
        for positive_query in positive_queries:
            match = re.match(r"\[(Movies|Unsplash):(\d{1,5})\](.*)", positive_query)
            if match:
                corpus2, idx, remainder = match.groups()
                idx, remainder = int(idx), remainder.strip()
                k2 = 0 if corpus2 == "Unsplash" else 1
                positive_embeddings = concatenate_embeddings(
                    positive_embeddings, embeddings[k2][idx : idx + 1, :]
                )
                if len(remainder) > 0:
                    positive_embeddings = concatenate_embeddings(
                        positive_embeddings, compute_text_embeddings([remainder])
                    )
            else:
                positive_embeddings = concatenate_embeddings(
                    positive_embeddings, compute_text_embeddings([positive_query])
                )
        dot_product = embeddings[k] @ positive_embeddings.T
        dot_product = dot_product - np.median(dot_product, axis=0)
        dot_product = dot_product / np.max(dot_product, axis=0, keepdims=True)
        dot_product = np.min(dot_product, axis=1)

    if len(splitted_query) > 1:
        negative_queries = (" ".join(splitted_query[1:])).split(";")
        negative_embeddings = compute_text_embeddings(negative_queries)
        dot_product2 = embeddings[k] @ negative_embeddings.T
        dot_product2 = dot_product2 - np.median(dot_product2, axis=0)
        dot_product2 = dot_product2 / np.max(dot_product2, axis=0, keepdims=True)
        dot_product -= np.max(np.maximum(dot_product2, 0), axis=1)

    results = np.argsort(dot_product)[-1 : -n_results - 1 : -1]

    to_return = []
    for r in results:
        to_return.append(
            (
                df[k].iloc[r]["path"],
                df[k].iloc[r]["tooltip"] + source[k],
                r,
            )
        )
    return json.dumps(to_return, cls=NpEncoder)


# if __name__ == "__main__":
uvicorn.run(app, host="0.0.0.0", port=5555)
