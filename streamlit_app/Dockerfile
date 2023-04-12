FROM python:3.8.15

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./credentials/cloudstorage.json .

WORKDIR /app

EXPOSE 8501

COPY . .

CMD streamlit run app.py