from flask import Flask, render_template, jsonify, url_for, request
from flask_jsglue import JSGlue
import random
from uuid import uuid1

app = Flask(__name__)
js_glue = JSGlue()
js_glue.init_app(app)  # 让js文件中可以使用url_for方法
results = []
chars = 'ABCDEFGHIJKLMNOPQRSTUVWSYZ'
results.append({'name': 'vue.js+flask+element-ui简易Demo', 'flag': 'true'})
results.append({'name': '代码请戳github', 'flag': 'true', 'url': 'https://github.com/qianbin01/Vue-flask'})
for i in range(5):
    results.append({'name': random.choice(chars), 'index': str(uuid1())})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_data')
def get_base_data():
    return jsonify({'results': results})


@app.route('/add', methods=['POST'])
def add():
    name = request.json.get('name')
    results.append({'name': name, 'index': str(uuid1())})  # uuid让index不唯一，实际开发中可以通过数据库的id来代替
    return jsonify({'message': '添加成功！'}), 200


@app.route('/update', methods=['PUT'])
def update():
    name = request.json.get('name')
    index = request.json.get('index')
    for item in results:
        if item['index'] == index:
            item['name'] = name
            break
    return jsonify({'message': '编辑成功！'}), 200


@app.route('/delete', methods=['DELETE'])
def delete():
    name = request.args.get('name')
    index = request.args.get('index')
    results.remove({'name': name, 'index': index})
    return jsonify({'message': '删除成功！'}), 200


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
