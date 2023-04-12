FROM python:3.8.15

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
EXPOSE 5555

COPY ./data/data.csv .

COPY ./data/data2.csv .

COPY ./embeddings/embeddings.npy .

COPY ./embeddings/embeddings2.npy .

COPY /clip_search_api.py ./

CMD ["python", "./clip_search_api.py"]