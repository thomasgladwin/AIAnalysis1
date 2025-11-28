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

def create_input(query, memory0=None, definitions="", data=""):
    input = [
        {"role": "user", "content": "I am a researcher and need accurate and considerate responses."},
        {"role": "assistant", "content": "I will provide accurate amd nuanced responses, focused on being based on clear evidence and referring to any relevant theories or data."},
    ]
    if ThomAIs_on:
        ThomasContent = fThomasAIs(query)
        input.append({"role": "user",
                                    "content": "Be aware of the following ideas, findings, references, and arguments; use their style of speaking and argumentation: " + ThomasContent})
        input.append({"role": "assistant",
                                "content": "I will use these ideas where relevant, and will follow the style of thinking and argumentation."})
    if len(data) > 0:
        input.append({"role": "user", "content": "Use the following information where relevant when answering questions: " + data})
        input.append({"role": "assistant", "content": "I will check whether this information is relevant and use it if so."})
    if not memory0 is None:
        for mem0 in memory0:
            if len(mem0["content"]) > 0 and not mem0 is None:
                input.append(mem0)
    if len(definitions) > 0:
        input.append({"role": "user", "content": "Use the following definitions of terms: " + definitions})
        input.append({"role": "assistant", "content": "I will make sure to apply these definitions in any relevant responses."})
    input.append({"role": "user", "content": query})
    return input

def query_AI_chat(input):
    response = client.chat.completions.create(
        model="gpt-5",
        messages=input,
        max_completion_tokens=1000
    )
    return response.choices[0].message

def query_AI(input):
    response = client.responses.create(
        model="gpt-5",
        input=input
    )
    return response.output_text

def fThomasAIs(query):
    ThomasContent = ''
    for iTopic in range(len(BeliefsAndOpinions.topics)):
        abstr = BeliefsAndOpinions.Abstr[BeliefsAndOpinions.topics[iTopic]]
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
        print(response + " " + str(score))
        if score > 1:
            ThomasContent += BeliefsAndOpinions.Full[BeliefsAndOpinions.topics[iTopic]]
    return ThomasContent
