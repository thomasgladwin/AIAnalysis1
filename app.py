from flask import Flask, render_template, request, jsonify
import funcs

app = Flask(__name__)

conversation_memory = []
verbose0 = False

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global conversation_memory
    debug_str = ''
    query = ''
    if 'Forget' in request.form:
        if request.form["Forget"] == 'valForget':
            debug_str = debug_str + 'Memory wiped. '
            conversation_memory = []
    if 'ThomAIs' in request.form:
        if request.form["ThomAIs"] == 'valThomAIs':
            funcs.ThomAIs_on = funcs.ThomAIs_on == False
            if funcs.ThomAIs_on:
                debug_str = debug_str + 'ThomAIs activated. '
            else:
                debug_str = debug_str + 'ThomAIs deactivated. '
    if 'query' in request.form:
        definitions = request.form['definitions']
        data = request.form['data']
        query = request.form['query']
        if len(query) == 0:
            response = "No query."
        else:
            try:
                input = funcs.create_input(query, conversation_memory, definitions, data)
                if len(input) > 0:
                    response = funcs.query_AI(input)
                    conversation_memory.append({'role': "user", 'content': query})
                    conversation_memory.append({'role': "assistant", 'content': response})
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
    if funcs.ThomAIs_on:
        ThomAIs_onoffStr = "On"
    else:
        ThomAIs_onoffStr = "Off"
    return render_template('index.html', query=query, response=response, definitions=definitions, data=data, ThomAIs_onoff=ThomAIs_onoffStr)

@app.route('/fetch_info', methods=['GET', 'POST'])
def f_fetch():
    global conversation_memory
    debug_str = ''
    query = ''
    if 'Forget' in request.form:
        if request.form["Forget"] == '1':
            debug_str = debug_str + 'Memory wiped. '
            conversation_memory = []
    if 'ThomAIs' in request.form:
        if request.form["ThomAIs"] == '1':
            funcs.ThomAIs_on = funcs.ThomAIs_on == False
            if funcs.ThomAIs_on:
                debug_str = debug_str + 'ThomAIs activated. '
            else:
                debug_str = debug_str + 'ThomAIs deactivated. '
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
                    response = funcs.query_AI(input)
                    conversation_memory.append({'role': "user", 'content': query})
                    conversation_memory.append({'role': "assistant", 'content': response})
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
