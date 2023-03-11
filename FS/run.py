from flask import Flask, jsonify, request
import socket
import requests
app = Flask(__name__)


def fibonacci_of(n):
    if n in {0, 1}:  # Base case
        return n
    return fibonacci_of(n - 1) + fibonacci_of(n - 2)  # Recursive case
@app.route("/fibonacci",methods=['GET'])
def fibo():
    # get parameters USE "request.args.get('xxx')"
    number = request.args.get('number')
    if not number:
        return jsonify("Bad Format"), 400
    else:
        ans = fibonacci_of(int(number))
        return jsonify(ans), 200



@app.route('/register', methods=['PUT'])
def register():
    # get parameters USE "request.args.get('xxx')"
    hostname = request.args.get('hostname')
    ip = request.args.get('ip')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    if hostname and ip and as_ip and as_port:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        # Send message
        req = "TYPE=A,NAME={}"
        msg = req.format(hostname).encode()
        s.sendto(msg, (as_ip, as_port)) 

        # Receive message
        data = s.recv(4096).decode()

        # Close connection
        s.close()
        # Request
        if(data == "Finish Registration"):
            return jsonify("success"), 201
        else:
            return jsonify("fail"), 500
    else:
        # missing params, server should return 400
        # to return json, need to improt jsonify from flask
        # format: jsonify(data), 200
        return jsonify("MISSING PARAMS"), 400

        

# TYPE,NAME,VALUE,TTL

app.run(host='0.0.0.0',
        port=9090,
        debug=True)