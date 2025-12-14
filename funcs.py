import requests
import json
import os
import time
from openai import OpenAI
import base64
import BeliefsAndOpinions
import re

client = OpenAI(
    api_key="xxx"
)
AccessCodes = ["xxx"]

ThomAIs_on = False
guest = True
ThomasContent = ''
relevantKeys = []
rel_id = 0
streaming_response = None
streaming_str = ''

def create_input(query, memory0=None, definitions="", data=""):
    global ThomasContent
    global ThomAIs_on
    input = [
        {"role": "user", "content": "I am a researcher and need accurate and considerate responses. However, always answer quickly enough."},
        {"role": "assistant", "content": "I will answer within 18 seconds. Given that, I will provide accurate and nuanced responses, focused on being based on clear evidence and referring to any relevant theories or data."},
    ]
    if ThomAIs_on:
        if len(ThomasContent) > 0:
            input.append({"role": "user",
                                        "content": "Be aware of the following ideas, findings, references, and arguments; refer to them where relevant to the query; use their style of speaking and argumentation: " + ThomasContent})
            input.append({"role": "assistant",
                                    "content": "I will use these ideas where relevant, and will follow the style of thinking and argumentation. I will talk about them as if they were my papers, essays, or thinking"})
    if len(definitions) > 0:
        input.append({"role": "user", "content": "Use the following definitions of terms: " + definitions})
        input.append({"role": "assistant", "content": "I will make sure to apply these definitions in any relevant responses."})
    if len(data) > 0:
        input.append({"role": "user", "content": "Use the following information where relevant when answering questions: " + data})
        input.append({"role": "assistant", "content": "I will check whether this information is relevant and use it if so."})
    if not memory0 is None:
        for mem0 in memory0:
            if len(mem0["content"]) > 0 and not mem0 is None:
                input.append(mem0)
    input.append({"role": "user", "content": query})
    return input

def query_AI_chat(input):
    response = client.chat.completions.create(
        model="gpt-5",
        messages=input,
        max_completion_tokens=1000
    )
    return response.choices[0].message.content

def query_AI(input):
    response = client.responses.create(
        model="gpt-5",
        input=input
    )
    return response.output_text

def query_AI_stream(input):
    global streaming_response
    global streaming_str
    streaming_str = ''
    response = client.responses.create(
        model="gpt-5",
        input=input,
        stream=True
    )
    streaming_response = response
    return "Streaming initiated, waiting for responses..."

def fThomasAIs_relevanceScans(query):
    global relevantKeys
    relevantKeys = []
    topics = BeliefsAndOpinions.Abstr.keys()
    for topic in topics:
        abstr = BeliefsAndOpinions.Abstr[topic]
        input = [
            {"role": "user", "content": "Respond with only a digit from 0 to 10. On a scale from 0 to 9, with 0 being not at all relevant and 9 being extremely relevant, how relevant is the following text to the query, " + query + ": " + abstr}
        ]
        response = query_AI(input)
        try:
            digits = re.findall(r'\d+', response)
            if len(digits) > 0:
                score = int(digits[0])
            else:
                score = 9
        except:
            score = 9
        #print(response + " " + str(score))
        if score > 1:
            relevantKeys.append(topic)
    return relevantKeys

def fThomasAIs_createInput(query):
    global ThomasContent
    global relevantKeys
    ThomasContent = ''
    for topic in relevantKeys:
        full = BeliefsAndOpinions.Full[topic]
        useQueriedSummmary = False
        if useQueriedSummmary:
            input = [
                {"role": "user",
                 "content": "Summarize, reporting where relevant the content and academic references given in the following text, in at most 750 words what is relevant from the following text to the query, " + query + ": " + full}
            ]
            response = query_AI(input)
            ThomasContent += response
        else:
            ThomasContent += full
    return ThomasContent

def relevanceScans_init():
    global relevantKeys
    global rel_id
    relevantKeys = []
    rel_id = 0

def relevanceScans_iter(query):
    global relevantKeys
    global rel_id
    topics = BeliefsAndOpinions.Abstr.keys()
    topic = list(topics)[rel_id]
    abstr = BeliefsAndOpinions.Abstr[topic]
    input = [
        {"role": "user", "content": "Respond with only a digit from 0 to 10. On a scale from 0 to 9, with 0 being not at all relevant and 9 being extremely relevant, how relevant is the following text to the query, " + query + ": " + abstr}
    ]
    response = query_AI(input)
    try:
        digits = re.findall(r'\d+', response)
        if len(digits) > 0:
            score = int(digits[0])
        else:
            score = 9
    except:
        score = 9
    #print(response + " " + str(score))
    if score > 1:
        relevantKeys.append(topic)
    rel_id += 1
    return score

def generate_image(prompt):
    prompt = """
    A children's book drawing of a veterinarian using a stethoscope to 
    listen to the heartbeat of a baby otter.
    """

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    # Save the image to a file
    with open("image.png", "wb") as f:
        f.write(image_bytes)
