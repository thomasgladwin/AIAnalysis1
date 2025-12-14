import requests
import json
import os
import time
from openai import OpenAI
import base64
import BeliefsAndOpinions
import re

api_key = "xxx"
AccessCodes = ["xxx"]

class AIInterface():
    ThomAIs_on = False
    guest = True
    ThomasContent = ''
    relevantKeys = []
    rel_id = 0
    streaming_response = None
    streaming_str = ''
    conversation_memory = []

    client = OpenAI(
        api_key=api_key
    )

    def create_input(self, query, definitions="", data=""):
        input = [
            {"role": "user", "content": "I am a researcher and need accurate and considerate responses. However, always answer quickly enough."},
            {"role": "assistant", "content": "I will answer within 18 seconds. Given that, I will provide accurate and nuanced responses, focused on being based on clear evidence and referring to any relevant theories or data."},
        ]
        if self.ThomAIs_on:
            if len(self.ThomasContent) > 0:
                input.append({"role": "user",
                                            "content": "Be aware of the following ideas, findings, references, and arguments; refer to them where relevant to the query; use their style of speaking and argumentation: " + self.ThomasContent})
                input.append({"role": "assistant",
                                        "content": "I will use these ideas where relevant, and will follow the style of thinking and argumentation. I will talk about them as if they were my papers, essays, or thinking"})
        if len(definitions) > 0:
            input.append({"role": "user", "content": "Use the following definitions of terms: " + definitions})
            input.append({"role": "assistant", "content": "I will make sure to apply these definitions in any relevant responses."})
        if len(data) > 0:
            input.append({"role": "user", "content": "Use the following information where relevant when answering questions: " + data})
            input.append({"role": "assistant", "content": "I will check whether this information is relevant and use it if so."})
        if len(self.conversation_memory) > 0:
            for mem0 in self.conversation_memory:
                if len(mem0["content"]) > 0 and not mem0 is None:
                    input.append(mem0)
        input.append({"role": "user", "content": query})
        return input

    def query_AI_chat(self, input):
        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=[input],
            max_completion_tokens=1000
        )
        return response.choices[0].message.content

    def query_AI(self, input):
        response = self.client.responses.create(
            model="gpt-5",
            input=input
        )
        return response.output_text

    def query_AI_stream(self, input):
        self.streaming_str = ''
        response = self.client.responses.create(
            model="gpt-5",
            input=input,
            stream=True
        )
        self.streaming_response = response
        return "Streaming initiated, waiting for responses..."

    def fThomasAIs_createInput(self, query):
        self.ThomasContent = ''
        for topic in self.relevantKeys:
            full = BeliefsAndOpinions.Full[topic]
            useQueriedSummmary = False
            if useQueriedSummmary:
                input = [
                    {"role": "user",
                     "content": "Summarize, reporting where relevant the content and academic references given in the following text, in at most 750 words what is relevant from the following text to the query, " + query + ": " + full}
                ]
                response = self.query_AI(input)
                self.ThomasContent += response
            else:
                self.ThomasContent += full
        return self.ThomasContent

    def relevanceScans_init(self):
        self.relevantKeys = []
        self.rel_id = 0

    def relevanceScans_iter(self, query):
        topics = BeliefsAndOpinions.Abstr.keys()
        topic = list(topics)[self.rel_id]
        abstr = BeliefsAndOpinions.Abstr[topic]
        input = [
            {"role": "user", "content": "Respond with only a digit from 0 to 10. On a scale from 0 to 9, with 0 being not at all relevant and 9 being extremely relevant, how relevant is the following text to the query, " + query + ": " + abstr}
        ]
        response = self.query_AI(input)
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
            self.relevantKeys.append(topic)
        self.rel_id += 1
        return response # str(score)
