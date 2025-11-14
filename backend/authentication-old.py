from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib
import jwt
from datetime import datetime, timedelta
from functools import wraps
import re

# ------------------- APP CONFIG -------------------

app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/train2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/train2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'greeva-train-jwt-secret-key-2024-production-secure-12345'  # Strong secret key for JWT

db = SQLAlchemy(app)

# ------------------- UTILITIES -------------------

def hash_password_sha1(password):
    return hashlib.sha1(password.encode()).hexdigest()

def is_valid_phone(phone):
    return str(phone).isdigit() and len(str(phone)) == 10

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# ------------------- TOKEN VALIDATOR -------------------

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
                # print(token)  # Debugging: print the token
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Signup.query.get(data['user_id'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid or expired', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)
    return decorated

# ------------------- MODELS -------------------



# ------------------- ROUTES -------------------

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the JWT-Protected Train API!"})


class Station(db.Model):
    __tablename__ = 'station'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Station_Name = db.Column(db.String(100))
    Station_Code = db.Column(db.String(20), unique=True)

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Station_Name': self.Station_Name,
            'Station_Code': self.Station_Code
        }


@app.route('/stations')
def show_stations():
    stations = Station.query.all()
    return jsonify([station.to_dict() for station in stations])

# ------------------- SIGNUP -------------------


class Signup(db.Model):
    __tablename__ = 'signup'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Ph_No = db.Column(db.BigInteger, unique=True)
    Station_Code = db.Column(db.String(20), db.ForeignKey('station.Station_Code'), nullable=True)
    Type_of_User = db.Column(db.String(50))
    Password = db.Column(db.String(100))
    Name = db.Column(db.String(100))

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Ph_No': self.Ph_No,
            'Station_Code': self.Station_Code,
            'Type_of_User': self.Type_of_User,
            'Name': self.Name
        }


@app.route('/signup', methods=['POST'])
def create_signup():
    data = request.get_json()

    phone = data.get('Ph_No')
    password = data.get('Password')
    name = data.get('Name')
    station_code = data.get('Station_Code')
    user_type = data.get('Type_of_User')

    if not is_valid_phone(phone):
        return jsonify({'error': 'Phone number must be a 10-digit number.'}), 400

    if not is_valid_password(password):
        return jsonify({
            'error': 'Password must be at least 8 characters and include an uppercase, lowercase, digit, and special character.'
        }), 400

    if Signup.query.filter_by(Ph_No=phone).first():
        return jsonify({'error': 'Phone number already registered.'}), 409

    hashed_password = hash_password_sha1(password)

    try:
        new_user = Signup(
            Ph_No=phone,
            Station_Code=station_code,
            Type_of_User=user_type,
            Password=hashed_password,
            Name=name
        )
        db.session.add(new_user)
        db.session.commit()

        # Use consistent JWT token generation (same as login)
        token = jwt.encode({
            'user_id': new_user.SI_No,
            'exp': datetime.utcnow() + timedelta(hours=2)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': new_user.to_dict(),
            'access_token': token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Signup failed: {str(e)}"}), 500

# ------------------- LOGIN -------------------

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone = data.get("Ph_No")
    password = data.get("Password")

    user = Signup.query.filter_by(Ph_No=phone).first()

    if user and user.Password == hash_password_sha1(password.strip()):
        try:
            token = jwt.encode({
                'user_id': user.SI_No,
                'exp': datetime.utcnow() + timedelta(hours=2)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            if isinstance(token, bytes):
                token = token.decode('utf-8')

            return jsonify({
                "status": "success",
                "message": f"Welcome {user.Name}!",
                "access_token": token,
                "user": user.to_dict()
            }), 200
        except Exception as e:
            return jsonify({'error': f"Token generation failed: {str(e)}"}), 500

    return jsonify({
        "status": "error",
        "message": "Invalid phone number or password"
    }), 401


# ------------------- TRAIN DATA (PROTECTED) -------------------



class Goodstrain:
    pass  # Dummy class to avoid breaking references, but not a model



@app.route('/trains', methods=['GET'])
@token_required
def get_trains(current_user):
    # Only show trains/reports for the user's station
    station_name = None
    trains = []
    if current_user.Station_Code:
        station = Station.query.filter_by(Station_Code=current_user.Station_Code).first()
        if station:
            station_name = station.Station_Name
        # Query reports for this station only
        trains = Report.query.filter_by(Station_Code=current_user.Station_Code).all()
    else:
        # If user has no station, show all trains (fallback)
        trains = Report.query.all()
    now = datetime.now().strftime('%I:%M %p')
    train_list = []
    for train in trains:
        train_dict = train.to_dict()
        train_dict['time'] = train.Time.strftime('%I:%M %p') if train.Time else now
        # For compatibility with frontend, add sl_no, name, report_id, status
        train_dict['sl_no'] = train.SI_No
        train_dict['name'] = train.Train_Name
        train_dict['report_id'] = train.Report_ID
        train_dict['status'] = "Finished" if train.Status else "Unfinished"
        train_list.append(train_dict)

    return jsonify({
        'trains': train_list,
        'station_name': station_name,
    }), 200



# ------------------- PROFILE (PROTECTED) -------------------

@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        "status": "success",
        "user": current_user.to_dict()
    })

# ------------------- TRAIN REPORT (PROTECTED) -------------------


class Report(db.Model):
    __tablename__ = 'report'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Train_Name = db.Column(db.String(50))
    Report_ID = db.Column(db.String(20), unique=True)
    Wagon_No = db.Column(db.Integer)
    Coach_Position = db.Column(db.Integer)
    Door_No = db.Column(db.Integer)
    Camera_No = db.Column(db.Integer)
    Date = db.Column(db.Date)
    Time = db.Column(db.Time)
    Status = db.Column(db.Boolean)
    Report_Remark = db.Column(db.Text)
    Station_Code = db.Column(db.String(20), db.ForeignKey('station.Station_Code'))
    Case_ID = db.Column(db.Integer, unique=True)
    Image_Link = db.Column(db.String(255))
    Ph_No = db.Column(db.BigInteger)

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Train_Name': self.Train_Name,
            'Report_ID': self.Report_ID,
            'Wagon_No': self.Wagon_No,
            'Coach_Position': self.Coach_Position,
            'Door_No': self.Door_No,
            'Camera_No': self.Camera_No,
            'Date': self.Date.isoformat() if self.Date else None,
            'Time': self.Time.isoformat() if self.Time else None,
            'Status': "Closed" if self.Status else "Open",
            'Report_Remark': self.Report_Remark,
            'Station_Code': self.Station_Code,
            'Case_ID': self.Case_ID,
            'Image_Link': self.Image_Link,
            'Ph_No': self.Ph_No
        }



@app.route('/reports', methods=['GET'])
def get_reports():
    reports = Report.query.all()
    return jsonify([report.to_dict() for report in reports])


# Endpoint for train report by Report_ID (single definition)
@app.route('/train-report', methods=['GET'])
@token_required
def train_report(current_user):
    report_id = request.args.get('id')
    if report_id:
        report = Report.query.filter_by(Report_ID=report_id).first()
    else:
        # If no id provided, return the first report (by SI_No)
        report = Report.query.order_by(Report.SI_No.asc()).first()
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    return jsonify(report.to_dict())




@app.route('/trains/<report_id>', methods=['PATCH'])
@token_required
def update_train(current_user, report_id):
    data = request.get_json()
    new_name = data.get('name')
    report = Report.query.filter_by(Report_ID=report_id).first()
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    report.Train_Name = new_name
    report.Status = True  # Mark as finished
    db.session.commit()
    return jsonify({'success': True, 'updated_report': report.to_dict()})


# ------------------- MAIN -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True)