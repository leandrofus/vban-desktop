import threading
import sys
import os
from flask import Flask, request, jsonify, render_template
from vban_config import config, save_config

vban_callback = None

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

template_dir = os.path.join(base_path, "templates")
static_dir = os.path.join(base_path, "static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/vban/status", methods=["GET"])
def status():
    running = vban_callback() if vban_callback else False
    return jsonify({"status": "running" if running else "stopped", **config})

@app.route("/vban/start", methods=["POST"])
def start_vban():
    data = request.json or {}
    config.update({
        "host": data.get("host", config["host"]),
        "port": str(data.get("port", config["port"])),
        "stream": data.get("stream", config["stream"]),
        "vban_path": data.get("vban_path", config["vban_path"]),
        "mode": data.get("mode", config.get("mode", "receiver"))
    })
    save_config()
    if vban_callback:
        threading.Thread(
            target=vban_callback,
            args=(config["host"], config["port"], config["stream"], config["vban_path"], config["mode"]),
            daemon=True
        ).start()
    return jsonify({"status": "started", **config})

@app.route("/vban/stop", methods=["POST"])
def stop_vban():
    if vban_callback:
        vban_callback(stop=True)
    return jsonify({"status": "stopped"})

def run_webserver(host="127.0.0.1", port=5000, callback=None):
    global vban_callback
    vban_callback = callback
    app.run(host=host, port=port, threaded=True)
