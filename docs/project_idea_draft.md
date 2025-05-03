# Gift Recommender

## One Liner Description:

Suggest gift ideas from Amazon for a friend using conversation history


## Outcome / Goal

* Gradio  interface to do this
OR * A web app that does this with UI


## Requirements / Features

1. User should be able to import chat history from -
    a. Whatsapp export chat
    b. Messenger
    c. More later

2. The system should provide gift ideas.

3. Based on #2, the system should provide amazon product links.


## Working Mechanism / Architecture

* Upload chat history .txt file
* Chunk
* For each chunk, apply prompts to identify interests, complaints
* Aggreegate all chunk outputs into one text
* Apply another prompt to connect to amazon-mcp to get product results - using langchain mcp




### Prompt Ideas


## User Workflows

* 



## Tech Stack


1. Frontend with react
2. Backend with python FastAPI 
3. Langchain
4. OpenAI, claude




