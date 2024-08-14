FROM python:3.8.5

WORKDIR /app

COPY ./requirements.txt requirements.txt
COPY ./server_med_ner_app.py server_med_ner_app.py

RUN pip install -r requirements.txt 
    
EXPOSE 8080

CMD python server_med_ner_app.py
