import requests
import json
import os
import time
from openai import OpenAI
import BeliefsAndOpinions
import re

client = OpenAI(
    api_key="xxx"
)

ThomAIs_on = False
guest = True
ThomasContent = ''
relevantKeys = []
streaming_response = None

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
                                        "content": "Be aware of the following ideas, findings, references, and arguments; use their style of speaking and argumentation: " + ThomasContent})
            input.append({"role": "assistant",
                                    "content": "I will use these ideas where relevant, and will follow the style of thinking and argumentation. I will talkabout them as if they were my papers, essays, or thinking"})
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
    response = client.responses.create(
        model="gpt-5",
        input=input,
        stream=True
    )
    streaming_response = response
    return "Streaming started in background, waiting for completed response..."

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
                 "content": "Summarize, reporting where relevant the content and academic references given in the following text. in at most 750 words what is relevant from the following text to the query, " + query + ": " + full}
            ]
            response = query_AI(input)
            ThomasContent += response
        else:
            ThomasContent += full
    return ThomasContent
