import requests
import json
import os

ENV_VARS_Saved = {
    "INFERENCE_URL": "https://eu.inference.heroku.com",
    "INFERENCE_KEY": "xxx",
    "INFERENCE_MODEL_ID": "claude-4-sonnet"
}

ENV_VARS = {
    "INFERENCE_URL": "",
    "INFERENCE_KEY": "",
    "INFERENCE_MODEL_ID": ""
}

def parse_chat_output(response):
    """
    Parses and prints the API response for the chat completion request.

    Parameters:
        - response (requests.Response): The response object from the API call.
    """
    if response.status_code == 200:
        result = response.json()
        output =  result["choices"][0]["message"]["content"]
    else:
        output =  "Request failed. " + str(response.status_code) + ". " + response.text
    return output

def generate_chat_completion(payload):
    """
    Generates a chat completion using the Stability AI Chat Model.

    Parameters:
        - payload (dict): dictionary containing parameters for the chat completion request

    Returns:
        - Prints the generated chat completion.
    """
    # Set headers using the global API key
    HEADERS = {
        "Authorization": f"Bearer {ENV_VARS['INFERENCE_KEY']}",
        "Content-Type": "application/json"
    }
    endpoint_url = ENV_VARS['INFERENCE_URL'] + "/v1/chat/completions"
    response = requests.post(endpoint_url, headers=HEADERS, data=json.dumps(payload))

    return parse_chat_output(response=response)

def query_AI(query, memory0=None, definitions="", data=""):
    payload = {
        "model": ENV_VARS["INFERENCE_MODEL_ID"],
        "messages": [
            {"role": "user", "content": "I am a researcher and need accurate and considerate responses."},
            {"role": "assistant", "content": "I will provide accurate amd nuanced responses, focused on being based on clear evidence and referring to any relevant theories or data."},
        ],
        "temperature": 0.5,
        "max_tokens": 1000,
        "stream": False
    }
    if len(data) > 0:
        payload["messages"].append({"role": "user", "content": "Use the following information where relevant when answering questions: " + data})
        payload["messages"].append({"role": "assistant", "content": "I will check whether this information is relevant and use it if so."})
    if not memory0 is None:
        for mem0 in memory0:
            if len(mem0["content"]) > 0 and not mem0 is None:
                payload["messages"].append(mem0)
    if len(definitions) > 0:
        payload["messages"].append({"role": "user", "content": "Use the following definitions of terms: " + definitions})
        payload["messages"].append({"role": "assistant", "content": "I will make sure to apply these definitions in any relevant responses."})
    payload["messages"].append({"role": "user", "content": query})
    output = generate_chat_completion(payload)
    return output
