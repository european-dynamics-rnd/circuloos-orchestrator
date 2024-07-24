"""
to start the server (remember to fully qualify the path):
`flask --app .\src\mock_RAMP\RAMP_service.py run`
"""

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.post("/fetch_new_supplier")
def materialize_query():
    print(f'request: {request.data}')
    if request.is_json:
        query = request.get_json()
        print(f'querying RAMP database for new suppliers with the attributes described in the query')
        results = jsonify('...this is a json with the company ids in RAMP...')
        return results, 201
    return {"error": "Request must be JSON"}, 415


