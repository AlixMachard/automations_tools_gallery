from fastapi import FastAPI
import uvicorn
from sentence_transformers import SentenceTransformer, util
import numpy as np
import json
import torch

app = FastAPI()


def bert_model():
    model = SentenceTransformer("distilbert-base-nli-mean-tokens")
    return model


@app.post("/text_similarity")
def get_text_similarity(sentences, query):
    model = bert_model()
    model = model.to("cpu")
    top_k = 2
    result = []
    sentences = json.loads(sentences)
    corpus_embeddings = model.encode(sentences)
    sentence_embedding = model.encode(query)

    cos_scores = util.pytorch_cos_sim(sentence_embedding, corpus_embeddings)[0]

    # top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
    top_results = torch.topk(cos_scores, k=top_k)

    for score, idx in zip(top_results[0], top_results[1]):
        print(sentences[idx], f"(Score: {score[idx]:.4f})")
        result.append(sentences[idx])
    return json.dumps(result)


# get_text_similarity(json.dumps(["hello", "hola"]), "hello")

uvicorn.run(app, host="0.0.0.0", port=5454)
