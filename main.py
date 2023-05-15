from api_gateway import server

server.run(host="0.0.0.0", port=5000, ssl_context="adhoc")