from flask import Flask, render_template, request, jsonify
import funcs as funcsLib
import time

app = Flask(__name__)

verbose0 = False
queue_fn = "streaming.txt"
interface_list = {}
timeout_queue = 120

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/init', methods=['GET', 'POST'])
def init():
    ID = request.form["ID"]
    interface_list[ID] = funcsLib.AIInterface()
    setInUse()
    return ""

@app.route('/cleanup', methods=['GET', 'POST'])
def cleanup():
    ID = request.form["ID"]
    interface_list.pop(ID, None)
    setNotInUse()
    return ""

@app.route('/relevanceScans', methods=['GET', 'POST'])
def relevanceScans():
    funcs = interface_list[request.form["ID"]]
    response = 'Not executed (mode)'
    if 'ThomAIs' in request.form:
        if request.form["ThomAIs"] == '1':
            if 'query' in request.form:
                query = request.form['query']
                if len(query) > 0:
                    try:
                        response_list = funcs.fThomasAIs_relevanceScans(query)
                        response = str(response_list)
                    except:
                        response = "Not executed (query)"
    if len(response) == 0:
        response = " "
    jsonResp = {"response": response}
    return jsonify(jsonResp)

@app.route('/setThomasContent', methods=['GET', 'POST'])
def setThomasContent():
    funcs = interface_list[request.form["ID"]]
    response = ' '
    if 'ThomAIs' in request.form:
        if request.form["ThomAIs"] == '1':
            if 'query' in request.form:
                query = request.form['query']
                if len(query) > 0:
                    try:
                        funcs.fThomasAIs_createInput(query)
                        response = "1"
                    except:
                        response = "0"
    if len(response) == 0:
        response = " "
    jsonResp = {"response": response}
    return jsonify(jsonResp)

@app.route('/fetch_info', methods=['GET', 'POST'])
def f_fetch():
    funcs = interface_list[request.form["ID"]]
    debug_str = ''
    query = ''
    if 'Forget' in request.form:
        if request.form["Forget"] == '1':
            debug_str = debug_str + 'Memory wiped. '
            funcs.conversation_memory = None
    funcs.ThomAIs_on = False
    if 'ThomAIs' in request.form:
        if request.form["ThomAIs"] == '1':
            funcs.ThomAIs_on = True
            debug_str = debug_str + 'ThomAIs activated. '
    if 'query' in request.form:
        try:
            definitions = request.form['definitions']
            data = request.form['data']
        except:
            definitions = ""
            data = ""
        query = request.form['query']
        if len(query) == 0:
            response = "No query."
        else:
            try:
                input = funcs.create_input(query, definitions, data)
                if len(input) > 0:
                    try:
                        response = funcs.query_AI_stream(input)
                    except:
                        response = "Error at query_AI"
                    funcs.conversation_memory.append({'role': "user", 'content': query})
                    # funcs.conversation_memory.append({'role': "assistant", 'content': response})
                else:
                    response = "Error - possibly too much data for guest account."
                query = ''
            except:
                response = "An error occurred while accessing the AI model - please try again."
            debug_str = debug_str + query + ". "
    else:
        response = "Waiting for query."
        definitions = ''
        data = ''
    if verbose0:
        response = "Debug info: " + debug_str + ". " + response
    if len(response) == 0:
        response = "No response."
    jsonResp = {"response": response}
    return jsonify(jsonResp)

@app.route('/check_stream', methods=['GET', 'POST'])
def check_stream():
    completed_str = "0"
    response = ""
    debug_str = ''
    try:
        funcs = interface_list[request.form["ID"]]
        n_tokens = 10
        for s in funcs.streaming_response:
            debug_str += s.type
            if "response.output_text.done" in s.type:
                completed_str = "1"
                response = s.text
                funcs.conversation_memory.append({'role': "assistant", 'content': response})
                break
            if hasattr(s, 'delta'):
                funcs.streaming_str += s.delta
            n_tokens -= 1
            if n_tokens <= 0:
                response = funcs.streaming_str
                break
    except:
        pass
    #response += debug_str
    jsonResp = {"response": response, "completed": completed_str}
    return jsonResp

@app.route('/relevanceScansLoop', methods=['GET', 'POST'])
def relevanceScansLoop():
    funcs = interface_list[request.form["ID"]]
    if 'ThomAIs' not in request.form:
        jsonResp = {"response": "1", "rel_id": "-1", "score": "-1"}
        return jsonResp
    if request.form["ThomAIs"] != '1':
        jsonResp = {"response": "1", "rel_id": "-1", "score": "-1"}
        return jsonResp
    query = request.form['query']
    if funcs.rel_id >= len(funcsLib.BeliefsAndOpinions.Abstr):
        funcs.fThomasAIs_createInput(query)
        funcs.relevanceScans_init()
        score = "0"
        response = "1"
    else:
        score = funcs.relevanceScans_iter(query)
        response = "0"
    jsonResp = {"response": response, "rel_id": str(funcs.rel_id - 1), "score": score}
    return jsonResp

def setInUse():
    try:
        with open(queue_fn, "a") as text_file:
            current_timestamp = time.time()
            text_file.writelines([str(current_timestamp) + "\n"])
    except:
        pass
    return ""

def setNotInUse():
    try:
        with open(queue_fn, "a") as text_file:
            text_file.writelines(["0\n"])
    except:
        pass
    return ""

@app.route('/check_queue', methods=['GET', 'POST'])
def check_queue():
    if request.form["accesscode"] in funcsLib.AccessCodes:
        status = "0"
    else:
        status = "0"
        try:
            with open(queue_fn, "r") as text_file:
                status = text_file.readlines()
                if len(status) == 0:
                    status = "0"
                else:
                    status = status[-1].strip()
                    if status != "0":
                        last_timestamp = float(status)
                        current_timestamp = time.time()
                        if (current_timestamp - last_timestamp) > timeout_queue:
                            status = "0"
                        else:
                            status = "1"
        except:
            status = "0"
    if len(status) == 0:
        status = " "
    jsonResp = {"response": status}
    return jsonResp
