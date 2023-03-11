import socket

server_port = 53533  # The port used by the server
# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.bind('', server_port)        

maps = {} # To record the mappings for hostname-ip 
while True:
    # Receive message
    data, client_ad = s.recv(4096).decode()

    if "VALUES" in data:
        # Registration
        print("This is a registration")
        hostname = data.split(",")[1].split("=")[1]
        ip = data.split(",")[2].split("=")[1]
        maps[hostname] = ip
        # Finish registration, return "success"
        s.sendto("success".encode(), client_ad)
    else: 
        # Query
        print("This is a query")
        # Check if documented
        hostname = data.split(",")[1].split("=")[1]
        if(hostname in maps):
            msg = "TYPE=A,NAME={},VALUE={},TTL=10".format(hostname,maps[hostname])
            s.sendto(msg.encode(), client_ad)
            
