from flask_jsglue import JSGlue
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Api

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/videorent?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

js_glue = JSGlue()
js_glue.init_app(app)  # 让js文件中可以使用url_for方法

parser = reqparse.RequestParser()


class Customer(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    phone = db.Column(db.String(20), unique=True)
    deposit = db.Column(db.String(10))
    comment = db.Column(db.String(50))

    def __init__(self, customer_id=None, customer_name=None, customer_phone=None, customer_deposit="0", comment=""):
        self.id = customer_id
        self.name = customer_name
        self.phone = customer_phone
        self.deposit = customer_deposit
        self.comment = comment

    def get_id(self):
        return str(self.id)

    # 打印对象的内容
    def __repr__(self):
        return '<Customer %r,%r,%r,%r,%r >' % (self.id, self.name, self.phone, self.deposit, self.comment)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'deposit': self.deposit,
            'comment': self.comment,
        }


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
        return '<Video %r,%r,%r,%r,%r >' % (self.id, self.name, self.format, self.description, self.comment)

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
    rental_time = db.Column(db.TIMESTAMP, unique=True)
    return_time = db.Column(db.TIMESTAMP, unique=True)
    customer_id = db.Column(db.String(20))
    video_id = db.Column(db.String(20))
    status = db.Column(db.String(10))
    comment = db.Column(db.String(256))

    def __init__(self, rental_id=None, rental_time=None, return_time=None, customer_id="", video_id="",
                 status="", comment=""):
        self.id = rental_id
        self.rental_time = rental_time
        self.return_time = return_time
        self.customer_id = customer_id
        self.video_id = video_id
        self.status = status
        self.comment = comment

    def get_id(self):
        return str(self.id)

    # 打印对象的内容
    def __repr__(self):
        return '<Rental $r,%r,%r,%r,%r,%r,%r>' % (self.id, self.rental_time, self.return_time, self.customer_id,
                                                  self.video_id, self.status, self.comment)

    def to_json(self):
        return {
            'id': self.id,
            'rental_time': self.rental_time,
            'return_time': self.return_time,
            'customer_id': self.customer_id,
            'video_id': self.video_id,
            'status': self.status,
            'comment': self.comment,
        }


class RentalRelation:
    def __init__(self, rental_id, video_id, video_name, video_description, customer_id, customer_name,
                 customer_phone, status,
                 rental_time, return_time, comment=None):
        self.id = rental_id
        self.video_id = video_id
        self.video_name = video_name
        self.video_description = video_description
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.status = status
        self.rental_time = rental_time
        self.return_time = return_time

    # 打印对象的内容
    def __repr__(self):
        return '<RentalRelation $r,%r,%r,%r,%r,%r,%r,%r>' % (self.id, self.video_id, self.video_name, self.video_description,
                                                       self.customer_id, self.customer_name, self.customer_phone,
                                                             self.status,
                                                          self.rental_time, self.return_time)

    def to_json(self):
        return {
            'id': self.id,
            'video_id': self.video_id,
            'video_name': self.video_name,
            'video_description': self.video_description,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'status': self.status,
            'rental_time': self.rental_time,
            'return_time': self.return_time,
        }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_data')
def get_base_data():
    data = db.session.query(Video, Customer, Rental).filter(Rental.video_id == Video.id, Rental.customer_id ==
                                                            Customer.id).all()
    dict1 = []
    for item in data:
        format_rental_time = item.Rental.rental_time.strftime("%Y.%m.%d-%H:%M:%S")
        format_return_time = item.Rental.return_time.strftime("%Y.%m.%d-%H:%M:%S")
        rental_relation_item = RentalRelation(item.Rental.id, item.Video.id, item.Video.name, item.Video.description,
                                              item.Customer.id, item.Customer.name, item.Customer.phone,
                                              item.Rental.status, format_rental_time, format_return_time)
        dict1.append(rental_relation_item.to_json())

    return jsonify({'results': dict1})


@app.route('/get_video_data')
def get_video_data():
    parser.add_argument("id", type=str)
    args = parser.parse_args()

    item_id = args.get('id')
    if item_id is None:
        data = db.session.query(Video).all()
    else:
        data = db.session.query(Video).filter(Video.id == item_id).all()
    dict1 = []
    for item in data:
        video_item = Video(item.id, "", item.name, item.description, "")
        dict1.append(video_item.to_json())

    return jsonify({'results': dict1})


@app.route('/get_customer_data')
def get_customer_data():
    parser.add_argument("id", type=str)
    args = parser.parse_args()

    item_id = args.get('id')
    if item_id is None:
        data = db.session.query(Customer).all()
    else:
        data = db.session.query(Customer).filter(Customer.id == item_id).all()

    dict1 = []
    for item in data:
        customer_item = Customer(item.id, item.name, item.phone, item.deposit,
                                 item.comment)
        dict1.append(customer_item.to_json())

    return jsonify({'results': dict1})


@app.route('/add_video', methods=['POST'])
def add_video():
    parser.add_argument("name")
    parser.add_argument("description")
    parser.add_argument("comment")
    args = parser.parse_args()
    video_name = args['name']
    video_description = args['description']
    comment = args['comment']

    db.create_all()  # In case user table doesn't exists already. Else remove it.
    video_data = db.session.query(Video).filter(Video.name == video_name).all()

    if len(video_data) == 0:
        video = Video(video_name=video_name, video_description=video_description, comment=comment)
        db.session.add(video)
        db.session.commit()
        return jsonify({'message': '添加成功！'}), 200
    else:
        return jsonify({'message': '添加失败！该影片已经存在'}), 400


@app.route('/add_customer', methods=['POST'])
def add_customer():
    parser.add_argument("phone")
    parser.add_argument("name")
    parser.add_argument("deposit")
    parser.add_argument("comment")
    args = parser.parse_args()
    customer_phone = args['phone']
    customer_name = args['name']
    customer_deposit = args['deposit']
    comment = args['comment']

    db.create_all()  # In case user table doesn't exists already. Else remove it.
    customer_data = db.session.query(Customer).filter(Customer.name == customer_name,
                                                      Customer.phone == customer_phone).all()

    if len(customer_data) == 0:
        customer = Customer(customer_phone=customer_phone, customer_name=customer_name,
                            customer_deposit=customer_deposit, comment=comment)
        db.session.add(customer)
        db.session.commit()
        return jsonify({'message': '添加成功！'}), 200
    else:
        return jsonify({'message': '添加失败！该会员已经存在'}), 400


@app.route('/add_rental', methods=['POST'])
def add_rental():
    parser.add_argument("video_name")
    parser.add_argument("video_description")
    parser.add_argument("customer_phone")
    parser.add_argument("customer_name")
    parser.add_argument("rental_time")
    parser.add_argument("return_time")
    parser.add_argument("comment")
    args = parser.parse_args()
    video_name = args['video_name']
    customer_phone = args['customer_phone']
    customer_name = args['customer_name']
    rental_time = args['rental_time']
    return_time = args['return_time']
    comment = args['comment']

    db.create_all()  # In case user table doesn't exists already. Else remove it.
    video_data = db.session.query(Video).filter(Video.name == video_name).first()
    customer_data = db.session.query(Customer).filter(Customer.name == customer_name, Customer.phone ==
                                                      customer_phone).first()

    if video_data is not None and customer_data is not None:
        rental = Rental(rental_time=rental_time, return_time=return_time, customer_id=customer_data.id,
                        video_id=video_data.id, status=str(1))
        db.session.add(rental)
        db.session.commit()
        return jsonify({'message': '添加成功！'}), 200
    else:
        if video_data is None:
            return jsonify({'message': '添加失败！这里没有该影片'}), 400
        else:
            return jsonify({'message': '添加失败！这里没有该会员'}), 400


@app.route('/update_rental', methods=['PUT'])
def update_rental():
    parser.add_argument("id", type=int)
    parser.add_argument("video_name", type=str)
    parser.add_argument("customer_name", type=str)
    parser.add_argument("customer_phone", type=str)
    parser.add_argument("rental_time", type=str)
    parser.add_argument("return_time", type=str)
    parser.add_argument("status", type=str)
    parser.add_argument("comment", type=str)
    args = parser.parse_args()

    item_id = args.get('id')
    update_video_name = args.get('video_name')
    update_customer_name = args.get('customer_name')
    update_customer_phone = args.get('customer_phone')
    update_rental_time = args.get('rental_time')
    update_return_time = args.get('return_time')
    update_status = args.get('status')
    update_comment = args.get('comment')

    video = db.session.query(Video).filter_by(name=update_video_name).first()
    customer = db.session.query(Customer).filter_by(name=update_customer_name, phone=update_customer_phone).first()
    rental = db.session.query(Rental).filter_by(id=item_id).first()

    # 将要修改的值赋给title
    if rental is not None and video is not None and customer is not None:
        rental.customer_id = customer.id
        rental.video_id = video.id
        rental.return_time = update_return_time
        rental.rental_time = update_rental_time
        rental.status = update_status
        rental.comment = update_comment

        db.session.commit()
    else:
        print("the rental is None,update error")
    return jsonify({"message": "修改成功！"})


@app.route('/delete_rental', methods=['DELETE'])
def delete_rental():
    parser.add_argument("id", type=str, location='args')
    args = parser.parse_args()
    raw_id = args.get('id')
    rental = db.session.query(Rental).filter_by(id=raw_id).first()

    if rental is not None:
        db.session.delete(rental)
        db.session.commit()
    else:
        print("the rental is None,delete error")
    return jsonify({'message': '删除成功！'})


@app.route('/delete_video', methods=['DELETE'])
def delete_video():
    parser.add_argument("id", type=str, location='args')
    args = parser.parse_args()
    raw_id = args.get('id')
    video = db.session.query(Video).filter_by(id=raw_id).first()
    rental = db.session.query(Rental).filter_by(video_id=raw_id, status=1).first()
    if video is not None and rental is None:
        db.session.delete(video)
        db.session.commit()
        return jsonify({'message': '删除成功！'}),200
    else:
        print("the video is None,delete error")
        return jsonify({'message': '影片不存在或者还有人租赁该影片没有归还'}), 403


@app.route('/delete_customer', methods=['DELETE'])
def delete_customer():
    parser.add_argument("id", type=str, location='args')
    args = parser.parse_args()
    raw_id = args.get('id')
    customer = db.session.query(Customer).filter_by(id=raw_id).first()
    rental = db.session.query(Rental).filter_by(customer_id=raw_id, status=1).first()
    if customer is not None and rental is None:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': '删除成功！'})
    else:
        print("the customer is None,delete error")
        return jsonify({'message': '会员不存在，或者还有会员租赁还影片！'}), 403


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
