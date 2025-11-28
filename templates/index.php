<?php
    // require("logging_passwords.php");
    $servername = "mysql.tegladwin.com";
    $username = "thomasgladwin";
    $password = "te6dhfloor";
    $db_name = "tegladwin_db";

    // Create connection
    $conn = new mysqli($servername, $username, $password);

    // Check connection
    if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }
?>
<!doctype html>
<script>
    function disableButton() {
        var btn = document.getElementById('btn');
        btn.disabled = true;
        btn.innerText = 'Waiting...'
        resptext0.innerText = 'Waiting...'
    }
</script>
<html>
    <head>
        <title>AI test 0.1 (PHP)</title>
    </head>
    <body>
        <div style="width: 100%;">
                <div style="width: 50%; float: left;">
                    <form action="index" method="POST" onsubmit='disableButton()'>
                        More information on <a href="https://github.com/thomasgladwin/AIAnalysis1">GitHub</a>.
                        <h1>Credentials</h1>
                        INFERENCE_URL: <input type="text" id="INFERENCE_URL" name="INFERENCE_URL" value = "">
                        <br>INFERENCE_KEY: <input type="text" id="INFERENCE_KEY" name="INFERENCE_KEY" value = "">
                        <br>INFERENCE_MODEL_ID: <input type="text" id="INFERENCE_MODEL_ID" name="INFERENCE_MODEL_ID" value = "">
                        <h1>Definitions</h1>
                        <textarea rows=3 cols=80 name="definitions" style="width: 80%;">{{ definitions }}</textarea>
                        <h1>Data</h1>
                        <textarea rows=3 cols=80 name="data" style="width: 80%;">{{ data }}</textarea>
                        <h1>Query</h1>
                        <textarea rows=3 cols=80 name="query" style="width: 80%;">{{ query }}</textarea>
                        <p><input type="checkbox" id="Forget" name="Forget" value="valForget">Forget prior conversation</p>
                        <p><input type="checkbox" id="ThomAIs" name="ThomAIs" value="valThomAIs">Toggle ThomAIs mode. Currently: {{ ThomAIs_onoff }}</p>
                        <p><button id='btn'>Submit</button></p>
                    </form>
                </div>
                <div style="margin-left: 50%;">
                    <h1>Response</h1>
                    <div id ='resptext0' style="white-space: pre-wrap;">{{ response }}</div>
                    <p><hr></p>
                </div>
            </div>
    </body>
</html>
