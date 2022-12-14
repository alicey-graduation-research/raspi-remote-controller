from flask import Flask, jsonify, request
from dotenv import load_dotenv
from irrp import IRRP
import subprocess
import sys
import os

load_dotenv()
SEND_PIN = int(os.getenv('SEND_PIN'))
REC_PIN = int(os.getenv('REC_PIN'))

subprocess.call("rm -rf /var/run/*")
subprocess.call("pigpiod")
ir = IRRP(file="test", post=130, no_confirm=True)
app = Flask("simple-iot-server")

@app.route("/")
def top():
    return jsonify({'status':'ok'}), 200

@app.route("/api/send")
def send_ir():
    try:
        playback(get_id(request.args))
        return jsonify({'status':'done'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status':'error'}), 500

@app.route("/api/rec")
def rec_ir():
    try:
        record(get_id(request.args))
        return jsonify({'status':'done'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status':'error'}), 500

@app.route("/send-test/")
def send_test():
    try:
        playback("air:on")
        return jsonify({'status':'done'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status':'error'}), 500

@app.route("/rec-test/")
def rec_test():
    try:
        record("air:on")
        return jsonify({'status':'done'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status':'error'}), 500

# @app.route("/temp/", methods=["GET","POST"])
# def temp():
#     if request.method == 'GET':
#         return jsonify({'status':'ok'}), 200
#     elif request.method == 'POST':
#         return jsonify({'status':'ok'}), 200

def get_params(req):
    hw = str(req.get('hw'))
    func = str(req.get('func'))
    return hw, func

def get_id(req):
    hw, func = get_params(req)
    return f"{hw}:{func}"

def record(id):
    ir.Record(GPIO=REC_PIN, ID=id)

def playback(id):
    ir.Playback(GPIO=SEND_PIN, ID=id)

def cleanup():
    ir.stop()

def main():
    try:
        app.run(host='0.0.0.0', port=80, threaded=False)
    finally:
        cleanup()

if __name__ == '__main__':
    main()

def sig_handler(signum, frame) -> None:
    cleanup()
    sys.exit(1)

# ir.Playback(GPIO=23, ID="air:on")