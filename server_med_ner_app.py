# Fastapi server App for Med NER. 
# This receives an user input text from a client, calls Spacy model to extract entities,
#   and returns the entities back to the client.
#import fastapi
from fastapi import FastAPI, Request
import uvicorn
import spacy
from spacy import displacy
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

# This "/" route is just to test the fast api server is up and running.
@app.get("/")
def read_root():
#    return "Hello World"
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI HTML Response</title>
    </head>
    <body>
        <h1>Hello !</h1>
        <p>This is a sample HTML response from MED NER FastAPI server.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

## You should download and install your Spacy model from huggingface hub to load it.
## You can get the below code by clicking "Use this model" on this url 
# https://huggingface.co/<you-user-name>/<specific-model-name>

# The following pip install is taken care by Dockerfile for containerization.
#!pip install https://huggingface.co/rajaramsblr/en_med_ner_pipeline/resolve/main/en_med_ner_pipeline-any-py3-none-any.whl
nlp_ner = spacy.load("en_med_ner_pipeline")

# Main method to receive the post request from the client, extract entities from the text received.
@app.post("/ner_extract")
async def read_predict(request: Request):
    data = await request.json()
    ent_dict = dict()
    
    #print("Server received :" + data)
    if 'text' in data:
        user_input = data['text']
    
    #print("Server received :" + user_input)
    
    # Call the NER model for entities extraction.
    doc = nlp_ner(user_input)
    
    for entity in doc.ents:
    
        # If the entity label (e.g B-Protein) is already present, append this 
        #   new value to the same entity list.
        if entity.label_ in ent_dict.keys():
            
            # Entities are stored in a list of tuples (entity name, Occurence count)
            ent_lst = [tup[0] for tup in ent_dict[entity.label_]]
            
            # If it is a newly found entity ( e.g 'lymphocytes' )
            if str(entity) not in ent_lst:
                tup = (str(entity),1)
                ent_dict[entity.label_].append(tup)
                
            # If it is already present entity, increment it's occurence count by 1.
            else:
                for i, tup in enumerate(ent_dict[entity.label_]):
                    if tup[0] == str(entity):
                        #print(tup[0])
                        ent_dict[entity.label_][i] = (tup[0], tup[1]+1)
                        
                
        # If it is a new entity label, create a list with the value found. 
        else:
            #print("Here1")
            tup = (str(entity), 1)
            ent_dict[entity.label_] = list([tup])
    
    # For each NER label, sort the entities list in the descending order of their counts of occurence
    ent_dict = {k: sorted(v, key=lambda x: x[1], reverse = True) \
                                 for k, v in ent_dict.items()}
    
    # HTML content for displacy output.
    html_content = displacy.render(doc, style="ent", jupyter=False)
    
    #print(ent_dict)
    #print(html_content)
    response_data = {
        "html_content": html_content,
        #"original_text": text,
        "ent_dict": ent_dict
    }
    
    #print(response_data)
    #return response_data
    return JSONResponse(content=response_data)
    
    
if __name__ == "__main__":
    uvicorn.run("server_med_ner_app:app", host = '0.0.0.0', port = 8080, reload = True)
