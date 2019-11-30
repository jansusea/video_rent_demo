from flask_jsglue import JSGlue
import random
from uuid import uuid1
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/videorent?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

js_glue = JSGlue()
js_glue.init_app(app)  # 让js文件中可以使用url_for方法
# results = []
# chars = 'ABCDEFGHIJKLMNOPQRSTUVWSYZ'
# results.append({'name': 'vue.js+flask+element-ui简易Demo', 'flag': 'true'})
# results.append({'name': '代码请戳github', 'flag': 'true', 'url': 'https://github.com/qianbin01/Vue-flask'})
# for i in range(5):
#     results.append({'name': random.choice(chars), 'index': str(uuid1())})

parser = reqparse.RequestParser()


class Customer(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    phoneNumber = db.Column(db.String(20), unique=True)
    deposit = db.Column(db.String(10))
    comment = db.Column(db.String(50))

    def __init__(self, customer_id=None, customer_name=None, customer_phone=None, customer_deposit="0", comment=""):
        self.id = customer_id
        self.name = customer_name
        self.phoneNumber = customer_phone
        self.deposit = customer_deposit
        self.comment = comment

    def get_id(self):
        return str(self.id)

    # 打印对象的内容
    def __repr__(self):
        return '<User %r,%r,%r,%r >' % self.name, self.phoneNumber, self.deposit, self.comment


class Video(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    format = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(256))
    comment = db.Column(db.String(256))

    def __init__(self, video_id=None, video_format=None, video_name=None, video_description="", comment=""):
        self.id = video_id
        self.format = video_format
        self.name = video_name
        self.description = video_description
        self.comment = comment

    def get_id(self):
        return str(self.id)

    # 打印对象的内容
    def __repr__(self):
        return '<User %r,%r,%r,%r,%r >' % (self.id, self.name, self.format, self.description, self.comment)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'format': self.format,
            'description': self.description,
            'comment': self.comment,
        }


class Rental(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    rental_datetime = db.Column(db.TIMESTAMP, unique=True)
    return_datetime = db.Column(db.TIMESTAMP, unique=True)
    customer_id = db.Column(db.String(20))
    video_id = db.Column(db.String(20))
    status = db.Column(db.String(10))
    comment = db.Column(db.String(256))

    def __init__(self, rental_id=None, rental_datetime=None, return_datetime=None, customer_id="", video_id="",
                 status="", comment=""):
        self.id = rental_id
        self.rental_datetime = rental_datetime
        self.return_datetime = return_datetime
        self.customer_id = customer_id
        self.video_id = video_id
        self.status = status
        self.comment = comment

    def get_id(self):
        return str(self.id)

    # 打印对象的内容
    def __repr__(self):
        return '<User %r,%r,%r,%r >' % self.name, self.format, self.description, self.comment


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_data')
def get_base_data():
    data = db.session.query(Video).all()
    dict1 = []
    for item in data:
        dict1.append(item.to_json())

    return jsonify({'results': dict1})


@app.route('/add', methods=['POST'])
def add():
    # name = request.json.get('name')

    # post_data = request.get_json()
    # print(post_data)
    parser.add_argument("format")
    parser.add_argument("name")
    parser.add_argument("description")
    args = parser.parse_args()
    video_format = args['format']
    video_name = args['name']
    video_description = args['description']
    video = Video(video_format=video_format,
                  video_name=video_name,
                  video_description=video_description)
    db.create_all()  # In case user table doesn't exists already. Else remove it.
    db.session.add(video)
    db.session.commit()

    # results.append({'name': name, 'index': str(uuid1())})  # uuid让index不唯一，实际开发中可以通过数据库的id来代替
    return jsonify({'message': '添加成功！'}), 200


@app.route('/update', methods=['PUT'])
def update():
    parser.add_argument("id", type=int)
    parser.add_argument("name", type=str)
    parser.add_argument("format", type=str)
    parser.add_argument("description", type=str)
    args = parser.parse_args()

    item_id = args.get('id')
    new_name = args.get('name')
    new_format = args.get('format')
    new_description = args.get('description')
    video = db.session.query(Video).filter_by(id=item_id).first()

    # 将要修改的值赋给title
    if video is not None:
        video.name = new_name
        video.format = new_format
        video.description = new_description

        db.session.commit()
    else:
        print("the video is None,update error")
    return jsonify({"message": "修改成功！"})


@app.route('/delete', methods=['DELETE'])
def delete():
    parser.add_argument("id", type=str, location='args')
    args = parser.parse_args()
    raw_id = args.get('id')
    video = db.session.query(Video).filter_by(id=raw_id).first()
    if video is not None:
        db.session.delete(video)
        db.session.commit()
    else:
        print("the video is None,delete error")
    return jsonify({'message': '删除成功！'})


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
