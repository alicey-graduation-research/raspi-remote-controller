from flask import Flask, jsonify, request
from irrp import IRRP
import sys

ir = IRRP(file="test", post=130, no_confirm=True)
app = Flask("simple-iot-server")

@app.route("/")
def top():
    return jsonify({'status':'ok'}), 200

@app.route("/send-test/")
def send_test():
    try:
        ir.Playback(GPIO=23, ID="air:on")
        return jsonify({'status':'done'}), 200
    except:
        return jsonify({'status':'error'}), 500

@app.route("/rec-test/")
def rec_test():
    try:
        ir.Record(GPIO=22, ID="air:on")
        return jsonify({'status':'done'}), 200
    except:
        return jsonify({'status':'error'}), 500

# @app.route("/temp/", methods=["GET","POST"])
# def temp():
#     if request.method == 'GET':
#         return jsonify({'status':'ok'}), 200
#     elif request.method == 'POST':
#         return jsonify({'status':'ok'}), 200

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