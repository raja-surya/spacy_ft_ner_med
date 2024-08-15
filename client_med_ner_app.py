
# Streamlit Client App for Med NER. 
# This sends an user input text to a Fastapi server to get back the extracted entities.

import streamlit as st
import requests
import streamlit.components.v1 as components
import pandas as pd

# Reference links :-
# https://discuss.streamlit.io/t/st-session-state-widget-cannot-be-modified-after-the-widget-with-key-widget-is-instantiated/48491
# https://discuss.streamlit.io/t/clear-input-box-after-hitting-enter/33824
# https://discuss.streamlit.io/t/st-form-getting-displayed-before-st-title/40768/6

#print("\n\nOut here in the beginning")

# Initialize the session state values.

if "ent_dict_list" not in st.session_state:
    #print("Initializing...")
    # User input
    st.session_state.user_input = ""
    # Var to store the entities of multiple docs as a list of dictionaries
    st.session_state.ent_dict_list = []
    # Dictionary of entities from current doc
    st.session_state.ent_dict = dict()
    # html var to store the displacy output of current doc
    st.session_state.html = ""
        
st.title("Bio-Med Named Entity Recognition") 
st.subheader("A Spacy based App to extract Bio-Medical entities from docs")
st.text_area('Enter Text to Scan - You may copy paste from test_medical_txt file..', key='text_area')


# Callback method to extract entities from a doc pasted in a text area, when button is submitted

def analyze_input():    
    
    # Get the user input from the text area widget.
    st.session_state.user_input = st.session_state.text_area
    
    # If no input by user, return
    if len(st.session_state.user_input.strip()) == 0:
        return
    
    # Once the submit button is pressed, this will clear the text area widget.
    # This changing of widget value is allowed only in a callback. 
    # So we had to have this method as callback.
    st.session_state.text_area = ''
    
    # If fastapi server is running on local host
    #response = requests.post("http://localhost:8080/ner_extract", \
    #                                     json={'text':st.session_state.user_input})
    
    # If fastapi server is running in a container deployed in AWS Fargate (ECS)
    #response = requests.post("http://54.92.198.5:8080/ner_extract", \
    #                                     json={'text':st.session_state.user_input})
   
    # If fastapi server is running in a container deployed in AWS App runner
    response = requests.post("https://up729q6xda.us-east-1.awsapprunner.com/ner_extract", \
                                         json={'text':st.session_state.user_input})
           
    #print(response.json())  
    st.session_state.ent_dict = response.json()['ent_dict']
    
    # https://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json
    for key in st.session_state.ent_dict:
        st.session_state.ent_dict[key] = [tuple(inner_list) for inner_list in st.session_state.ent_dict[key]]
    
    #print(st.session_state.ent_dict)
    
    # For displacy output
    st.session_state.html = response.json()['html_content']
    
    # Append the entity dictionary of this doc to the master doc list.
    st.session_state.ent_dict_list.append(st.session_state.ent_dict)
    


# Function to convert a list to a comma-separated string
def list_to_comma_separated_string(lst):
    if len(lst) > 0:
        return ', '.join(map(str, lst))

# Method to convert the master list of doc dict to a pandas df and 
#  display it as a Streamlit table.
def consolidate():
    results_df = pd.DataFrame(st.session_state.ent_dict_list)
    df_comma_separated = results_df.fillna("").applymap(list_to_comma_separated_string)
    st.table(df_comma_separated)


button1 = st.button("Scan Doc and Show Details", on_click = analyze_input)
button2 = st.button("Show Displacy Output of Doc")
button3 = st.button("Show Table of Scanned Docs")

# This was needed separately to display the results below the text area.
#  Otherwise if this code is in callback, it was printing on the top of the page.
if button1:
    for label, value in st.session_state.ent_dict.items():
        st.write(label, '-' * 10, *value)
    
if button2:
    components.html(st.session_state.html, height=300, scrolling=True)

if button3:
    consolidate()