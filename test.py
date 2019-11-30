from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/videorent?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
    format = db.Column(db.String(10))
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
        # return '<User %r,%r,%r,%r >' % self.name self.format, self.description, self.comment
        return '<User %r >' % self.name

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

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'format': self.format,
            'description': self.description,
            'comment': self.comment,
        }


# @app.cli.command()
# @click.option('--drop', is_flag=True, help='Create after drop.')
# def initdb(drop):
#     """Initialize the database."""
#     if drop:
#         db.drop_all()
#     db.create_all()
#     click.echo('Initialized database.')
parser = reqparse.RequestParser()


class HelloWorld(Resource):
    def post(self):
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

        # 格式化jsonify不能是对象
        return video.__str__(), 201

    def get(self):
        data = db.session.query(Video).all()
        dict1 = []
        for i in data:
            dict1.append(i.to_json())

        print(data)
        return jsonify(dict1)

    def put(self):
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

    def delete(self):
        parser.add_argument("name", type=str, location='args')
        args = parser.parse_args()
        print(args)
        name = args.get('name')
        # index = request.args.get('index')
        video = db.session.query(Video).filter_by(name=name).first()
        if video is not None:
            db.session.delete(video)
            db.session.commit()
        else:
            print("the video is None,delete error")
        return jsonify({'message': '删除成功！'})


api.add_resource(HelloWorld, '/get')


def serialize(model):
    from sqlalchemy.orm import class_mapper
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


@app.route('/')
def index():
    # form = DeleteNoteForm()
    # notes = Note.query.all()
    return "hello world!"


@app.route('/add', methods=['GET', 'POST'])
def add():
    get_data = request.args  # 利用request对象获取GET请求数据
    print('获取的GET数据为：', get_data)  # 打印获取到的GET数据 ImmutableMultiDict([('username', '456456'), ('password', '667788')])
    post_data = request.form  # 利用request对象获取POST请求数据
    print('获取的POST数据为：', post_data)  # 打印获取到的POST请求 ImmutableMultiDict([])
    username = request.args.get('username')  # 使用args获取get请求数据
    password = request.args.get('password')
    print(username, password)  # 456456 667788
    return '这是测试页面'

    # if form.validate_on_submit():
    #     body = form.body.data
    #     note = Note(body=body)
    #     db.session.add(note)
    #     db.session.commit()
    #     flash('Your note is saved.')
    #     return redirect(url_for('index'))
    # return render_template('new_note.html', form=form)


# @app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
# def edit_note(note_id):
#     form = EditNoteForm()
#     note = Note.query.get(note_id)
#     if form.validate_on_submit():
#         note.body = form.body.data
#         db.session.commit()
#         flash('Your note is updated.')
#         return redirect(url_for('index'))
#     form.body.data = note.body  # preset form input's value
#     return render_template('edit_note.html', form=form)
#
#
# @app.route('/delete/<int:note_id>', methods=['POST'])
# def delete_note(note_id):
#     form = DeleteNoteForm()
#     if form.validate_on_submit():
#         note = Note.query.get(note_id)
#         db.session.delete(note)
#         db.session.commit()
#         flash('Your note is deleted.')
#     else:
#         abort(400)
#     return redirect(url_for('index'))


# # Forms
# class NewNoteForm(FlaskForm):
#     body = TextAreaField('Body', validators=[DataRequired()])
#     submit = SubmitField('Save')
#
#
# class EditNoteForm(FlaskForm):
#     body = TextAreaField('Body', validators=[DataRequired()])
#     submit = SubmitField('Update')
#
#
# class DeleteNoteForm(FlaskForm):
#     submit = SubmitField('Delete')
# test_user = User1(8, '123', '123', 'xiaozhi')
# db.create_all()  # In case user table doesn't exists already. Else remove it.
# db.session.add(test_user)
# db.session.commit()


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True, index=True)
#     body = db.Column(db.Text)
#
#
# admin = User('ssss', 'admin@example.com')
# #
# # db.create_all()  # In case user table doesn't exists already. Else remove it.
# #
# db.session.add(admin)
# #
# db.session.commit()  # This is needed to write the changes to database
#
# User.query.all()
#
# User.query.filter_by(username='admin').first()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)