from api_gateway import server
import os

server.run(host="0.0.0.0", port=8080, ssl_context="adhoc")