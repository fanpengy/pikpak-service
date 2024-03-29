from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import json
load_dotenv()
from utils.SQLHelper import sqlHelper
app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['GET'])
def search():
    id = request.args.get('id')
    sql = "select * from shares where dvd_id like '" + id + "%%'"
    result = sqlHelper.get_list(sql)
    response = make_response(jsonify(result))
    return response

@app.route('/new_share', methods=['POST'])
def new_share():
    name = request.json.get("name")
    link = request.json.get("link")
    sql = 'insert into shares(dvd_id, share_link) values(%s, %s)'
    row_id = sqlHelper.insert(sql, name, link)
    response = make_response(jsonify(row_id))
    return response
