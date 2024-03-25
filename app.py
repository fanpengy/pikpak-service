from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from urllib.parse import urljoin
from lxml import html
import json
from utils.HttpUtils import client, r_client, EnvTest
import os
load_dotenv()
from utils.SQLHelper import sqlHelper, task_test
app = Flask(__name__)
CORS(app)
PARSER = html.HTMLParser(encoding="UTF-8")
scheduler = BackgroundScheduler()
scheduler.add_job(task_test, 'interval', seconds=300)

scheduler.start()

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

@app.route('/r_test', methods=['GET'])
def test_r():
    id = request.args.get('id')
    url = os.environ.get('archivement.content.url.r').format(content_id=id)
    resp = r_client.get(url, timeout=10)
    if resp.ok:
        return resp.json()
    else:
        return jsonify(resp.status_code)
    
@app.route('/lib_test', methods=['GET'])
def test_lib():
    id = request.args.get('id')
    url_base = os.environ.get('archivement.content.url.lib.base')
    url_postfix = os.environ.get('archivement.content.url.lib.search')
    url = url = urljoin(url_base, url_postfix.format(keyword=id))
    resp = client.get(url, timeout=10)
    if resp.ok:
        page = html.fromstring(html=resp.content, parser=PARSER)
        title_select = os.environ.get("archivement.content.select.lib.title")
        return jsonify(page.cssselect(title_select)[0].text)
    else:
        return jsonify(resp.status_code)
    
@app.route('/danyu_test', methods=['GET'])
def test_danyu():
    id = request.args.get('id')
    url = os.environ.get('archivement.content.url.danyu').format(content_id=id)
    resp = client.get(url, timeout=10)
    if resp.ok:
        page = html.fromstring(html=resp.content, parser=PARSER)
        title_select = os.environ.get("archivement.content.select.danyu.title")
        return jsonify(page.cssselect(title_select)[0].text)
    else:
        return jsonify(resp.status_code)
    

@app.route('/db_test', methods=['GET'])
def test_db():
    id = request.args.get('id')
    url = os.environ.get('archivement.content_id.url.db').format(dvd_id=id)
    resp = client.get(url, timeout=10)
    if resp.ok:
        page = html.fromstring(html=resp.content, parser=PARSER)
        table_select = os.environ.get('archivement.content.select.db.table')
        tds = page.cssselect(table_select)
        texts = list(map(lambda td: td.text_content(), tds))
        index = -1
        for i, text in enumerate(texts):
            if text == 'Content ID:':
                index = i
                break
        if index and index != -1 and len(texts) > index + 1 and texts[index + 1]:
            return texts[index + 1]
        else:
            return 'haha'
    else:
        return jsonify(resp.status_code)
    
@app.route('/jm_test', methods=['GET'])
def test_jm():
    id = request.args.get('id')
    url = os.environ.get('actress.content.url.jm').format(name=id)
    resp = client.get(url, timeout=10)
    if resp.ok:
        page = html.fromstring(html=resp.content, parser=PARSER)
        name_select = os.environ.get('actress.content.select.jm.name')
        return jsonify(page.cssselect(name_select)[0].text)
    else:
        return jsonify(resp.status_code)
    
@app.route('/env_test', methods=['GET'])
def test_env():
    prefix = os.environ.get('prefix')
    postfix = EnvTest.postfix

    return f'{prefix}.{postfix}'