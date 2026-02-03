from flask import Flask, jsonify, request
from fetchAllPublicRepos import fetch_all_repos
import asyncio
import json
import csv

app = Flask(__name__)

@app.route("/api/repos/<string:org>", methods=["GET"])
async def fetchAllRepos(org):
    limit = request.args.get("limit", 5)
    response = await fetch_all_repos(org, int(limit))
    print(response)
    return response

@app.route("/api/quotes", methods=["POST"])
def addQuote():
    jsonReq = request.get_json()
    
    with open("quote.json", "r+") as file:
        data = file.read()
        file.seek(0)
        data = json.loads(data)
        data.get("quotes", []).append(jsonReq)
        file.write(json.dumps(data, check_circular=True))
        file.truncate()

    return jsonify({"message": "Successfully written to file"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)