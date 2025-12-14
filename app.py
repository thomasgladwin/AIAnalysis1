from flask import Flask, render_template, request, jsonify
import funcs
import time

app = Flask(__name__)

conversation_memory = []
verbose0 = False
queue_fn = "streaming.txt"

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/relevanceScans', methods=['GET', 'POST'])
def relevanceScans():
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
    jsonResp = {"response": response}
    return jsonify(jsonResp)

@app.route('/setThomasContent', methods=['GET', 'POST'])
def setThomasContent():
    response = ''
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
    jsonResp = {"response": response}
    return jsonify(jsonResp)

@app.route('/fetch_info', methods=['GET', 'POST'])
def f_fetch():
    global conversation_memory
    debug_str = ''
    query = ''
    if 'Forget' in request.form:
        if request.form["Forget"] == '1':
            debug_str = debug_str + 'Memory wiped. '
            conversation_memory = []
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
                input = funcs.create_input(query, conversation_memory, definitions, data)
                if len(input) > 0:
                    try:
                        response = funcs.query_AI_stream(input)
                    except:
                        response = "Error at query_AI"
                    conversation_memory.append({'role': "user", 'content': query})
                    # conversation_memory.append({'role': "assistant", 'content': response})
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
    global conversation_memory
    completed_str = "0"
    response = ""
    debug_str = ''
    try:
        n_tokens = 10
        for s in funcs.streaming_response:
            debug_str += s.type
            if "response.output_text.done" in s.type:
                completed_str = "1"
                response = s.text
                conversation_memory.append({'role': "assistant", 'content': response})
                break
            if hasattr(s, 'delta'):
                funcs.streaming_str += s.delta
            n_tokens -= 1
            if n_tokens <= 0:
                response = funcs.streaming_str
                break
    except:
        response = ""
    # response += debug_str
    jsonResp = {"response": response, "completed": completed_str}
    return jsonResp

@app.route('/relevanceScansLoop', methods=['GET', 'POST'])
def relevanceScansLoop():
    if 'ThomAIs' not in request.form:
        jsonResp = {"response": "1", "rel_id": "-1", "score": "-1"}
        return jsonResp
    if request.form["ThomAIs"] != '1':
        jsonResp = {"response": "1", "rel_id": "-1", "score": "-1"}
        return jsonResp
    query = request.form['query']
    if funcs.rel_id >= len(funcs.BeliefsAndOpinions.Abstr):
        funcs.fThomasAIs_createInput(query)
        funcs.relevanceScans_init()
        score = 0
        response = "1"
    else:
        score = funcs.relevanceScans_iter(query)
        response = "0"
    jsonResp = {"response": response, "rel_id": str(funcs.rel_id - 1), "score": str(score)}
    return jsonResp

@app.route('/setInUse', methods=['GET', 'POST'])
def setInUse():
    try:
        with open(queue_fn, "a") as text_file:
            current_timestamp = time.time()
            text_file.writelines([str(current_timestamp) + "\n"])
    except:
        pass
    return ""

@app.route('/setNotInUse', methods=['GET', 'POST'])
def setNotInUse():
    try:
        with open(queue_fn, "a") as text_file:
            text_file.writelines(["0\n"])
    except:
        pass
    return ""

@app.route('/check_queue', methods=['GET', 'POST'])
def check_queue():
    if request.form["accesscode"] in funcs.AccessCodes:
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
                        if (current_timestamp - last_timestamp) > 30:
                            status = "0"
                        else:
                            status = "1"
        except:
            pass
    jsonResp = {"response": status[-1], "access": request.form["accesscode"]}
    return jsonResp
