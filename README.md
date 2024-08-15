Fine-tune a Spacy NER Model on a Custom (Bio-medical ) Dataset & Deploy it in a Web App on AWS cloud - An End-to-end Project.
Learnings in NLP, NER, Spacy, Hugging Face, Streamlit, FastAPI, AWS App Runner, AWS Fargate

Spacy-NER-FineTune-Blurb.ipynb - Fine tuning a Spacy model on a bio-medical dataset "Blurb".

push_model_to_hf.ipynb - Push the fine-tuned model to Hugging Face hub.

client_med_ner_app.py - Streamlit client App to collect user input text and send it to server.

server_med_ner_app.py - FastAPI server App to receive the user input text, call the Spacy model to perform NER and send the result back to the client.

Dockerfile - Dockerfile for containerization of the server app.

requirements.txt - Packages to be installed in the container.

Deploy_Steps_AWS_App_Runner.txt - Steps to follow for deploying the server app on AWS App Runner.

test_medical_text.txt - Some bio-med text from the test dataset that can be used for testing the project.
