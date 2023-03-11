from flask import Flask, jsonify, request
import socket
import requests
app = Flask(__name__)


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    # get parameters USE "request.args.get('xxx')"
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if hostname and fs_port and number and as_ip and as_port:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        # Send message
        req = "TYPE=A,NAME={},VALUE={},TTL=10"
        msg = req.format(hostname,ip).encode()
        s.sendto(msg, (as_ip, as_port)) 

        # Receive message
        data = s.recv(4096).decode()
        value = data.split(",")[2]
        ip = value.split("=")[1]

        # Close connection
        s.close()
        # Request
        ans = requests.get("http://{}:{}/fibonacci?number={}".format(ip, fs_port, number))
        return jsonify(ans), 200
    else:
        # missing params, server should return 400
        # to return json, need to improt jsonify from flask
        # format: jsonify(data), 200
        return jsonify("MISSING PARAMS"), 400

        

# TYPE,NAME,VALUE,TTL

app.run(host='0.0.0.0',
        port=8080,
        debug=True)