from flask import Flask, render_template, request
import funcs

app = Flask(__name__)

conversation_memory = []
verbose0 = False
accesslist = ["xxx", "xxx", "xxx", "xxx"]

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global conversation_memory
    debug_str = ''
    if 'INFERENCE_URL' in request.form:
        if len(request.form["INFERENCE_URL"]) > 0:
            funcs.ENV_VARS["INFERENCE_URL"] = request.form["INFERENCE_URL"]
            funcs.ENV_VARS["INFERENCE_KEY"] = request.form["INFERENCE_KEY"]
            funcs.ENV_VARS["INFERENCE_MODEL_ID"] = request.form["INFERENCE_MODEL_ID"]
            debug_str = debug_str + request.form["INFERENCE_URL"] + ". "
    else:
        if "access" in request.args:
            user = request.args.get("access")
            if user in accesslist:
                funcs.ENV_VARS["INFERENCE_URL"] = funcs.ENV_VARS_Saved["INFERENCE_URL"]
                funcs.ENV_VARS["INFERENCE_KEY"] = funcs.ENV_VARS_Saved["INFERENCE_KEY"]
                funcs.ENV_VARS["INFERENCE_MODEL_ID"] = funcs.ENV_VARS_Saved["INFERENCE_MODEL_ID"]
    if 'Forget' in request.form:
        if request.form["Forget"] == 'valForget':
            debug_str = debug_str + 'Memory wiped. '
            conversation_memory = []
    if 'query' in request.form:
        definitions = request.form['definitions']
        data = request.form['data']
        query = request.form['query']
        if len(query) == 0:
            response = "No query."
        else:
            response = funcs.query_AI(query, conversation_memory, definitions, data)
            conversation_memory.append({'role': "user", 'content': query})
            conversation_memory.append({'role': "assistant", 'content': response})
            debug_str = debug_str + query + ". "
    else:
        response = "Waiting for query."
        definitions = ''
        data = ''
    if verbose0:
        response = "Debug info: " + debug_str + ". " + response
    return render_template('index.html', response=response, definitions=definitions, data=data)

