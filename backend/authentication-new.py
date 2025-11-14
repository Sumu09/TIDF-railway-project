from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib
import jwt
from datetime import datetime, timedelta, date, time
from functools import wraps
import re

# ------------------- APP CONFIG -------------------

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/train2'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root2:root#123@localhost/train2'
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

def serialize_result(rows):
    """
    Serializes database results, converting special types to strings.
    Handles datetime objects and byte arrays.
    """
    for row in rows:
        for key in row:
            # Convert date, time, and timedelta objects to string format
            if isinstance(row[key], (datetime, date, time, timedelta)):
                row[key] = str(row[key])
            # Convert byte arrays (like from BLOBs or certain string types) to UTF-8 strings
            elif isinstance(row[key], (bytes, bytearray)):
                row[key] = row[key].decode('utf-8')
    return rows

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
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    zone = db.Column(db.String(100))

    def to_dict(self):
        return {
            'SL_No': self.SI_No,
            'Station_Name': self.Station_Name,
            'Station_Code': self.Station_Code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'zone': self.zone
        }


@app.route('/stations', methods=['GET'])
def show_stations():
    stations = Station.query.all()
    return jsonify({
        'status': 'success',
        'stations': [station.to_dict() for station in stations]
    }), 200

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
        return jsonify({'error': 'This phone number is already registered. Please log in or use a different number.'}), 409

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
        return jsonify({'error': 'Signup failed due to a server error. Please try again later or contact support.'}), 500

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


# Updated Report model to match the current MySQL schema
class Report(db.Model):
    __tablename__ = 'report'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Train_Name = db.Column(db.String(100))
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
    Case_ID = db.Column(db.Integer)
    Image_Link = db.Column(db.String(255))
    Ph_No = db.Column(db.BigInteger)
    zone = db.Column(db.String(100))
    # Add any new columns as needed

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
            'Status': "Finished" if self.Status else "Unfinished",
            'Report_Remark': self.Report_Remark,
            'Station_Code': self.Station_Code,
            'Case_ID': self.Case_ID,
            'Image_Link': self.Image_Link,
            'Ph_No': self.Ph_No,
            'zone': self.zone
        }



# Updated FinalReport model to match the current MySQL schema
class FinalReport(db.Model):
    __tablename__ = 'final_report'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Train_Name = db.Column(db.String(100))
    Report_ID = db.Column(db.String(20), unique=True)
    Wagon_No = db.Column(db.Integer)
    Coach_Position = db.Column(db.Integer)
    Door_No = db.Column(db.Integer)
    Camera_No = db.Column(db.Integer)
    Date = db.Column(db.Date)
    Time = db.Column(db.Time)
    Status = db.Column(db.Boolean)
    Report_Remark = db.Column(db.Text)
    Station_Code = db.Column(db.String(20))
    Station_Name = db.Column(db.String(100))
    Case_ID = db.Column(db.Integer)
    Image_Link = db.Column(db.String(255))
    Ph_No = db.Column(db.BigInteger)
    User_Name = db.Column(db.String(100))
    User_Age = db.Column(db.Integer)
    User_Email = db.Column(db.String(100))

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
            'Status': "Finished" if self.Status else "Unfinished",
            'Report_Remark': self.Report_Remark,
            'Station_Code': self.Station_Code,
            'Station_Name': self.Station_Name,
            'Case_ID': self.Case_ID,
            'Image_Link': self.Image_Link,
            'Ph_No': self.Ph_No,
            'User_Name': self.User_Name,
            'User_Age': self.User_Age,
            'User_Email': self.User_Email
        }


class PendingCases(db.Model):
    __tablename__ = 'pending_cases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train = db.Column(db.String(50))
    status = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'train': self.train,
            'status': self.status
        }


# ------------------- ROUTES -------------------



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

# ------------------- MERGED BACKEND ENDPOINTS -------------------

@app.route('/train-report/week', methods=['GET'])
def train_report_by_week():
    try:
        from sqlalchemy import text, func
        # Use SQLAlchemy to execute raw SQL for complex queries
        query = text("""
            SELECT
                WEEK(Date, 1) AS Week, Date, Time, Train_Name,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report ORDER BY Date DESC
        """)
        result = db.session.execute(query)
        rows = [dict(row._mapping) for row in result]
        return jsonify({"status": "success", "data": serialize_result(rows)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/train-report/month', methods=['GET'])
def train_report_by_month():
    try:
        from sqlalchemy import text
        query = text("""
            SELECT
                MONTH(Date) AS Month, Date, Time, Train_Name,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report ORDER BY Date DESC
        """)
        result = db.session.execute(query)
        rows = [dict(row._mapping) for row in result]
        return jsonify({"status": "success", "data": serialize_result(rows)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/train-report/year', methods=['GET'])
def train_report_by_year():
    try:
        from sqlalchemy import text
        query = text("""
            SELECT
                YEAR(Date) AS Year, Date, Time, Train_Name,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report ORDER BY Date DESC
        """)
        result = db.session.execute(query)
        rows = [dict(row._mapping) for row in result]
        return jsonify({"status": "success", "data": serialize_result(rows)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/report-summary/weekly', methods=['GET'])
def weekly_summary():
    try:
        from sqlalchemy import text
        query = text("""
            SELECT COUNT(*) AS Finished_Reports FROM final_report
            WHERE Status = 1 AND YEARWEEK(Date, 1) = YEARWEEK(CURDATE(), 1)
        """)
        result = db.session.execute(query)
        row = result.fetchone()
        return jsonify({"status": "success", "data": dict(row._mapping)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/report-summary/monthly', methods=['GET'])
def monthly_summary():
    try:
        from sqlalchemy import text
        query = text("""
            SELECT COUNT(*) AS Finished_Reports FROM final_report
            WHERE Status = 1 AND YEAR(Date) = YEAR(CURDATE()) AND MONTH(Date) = MONTH(CURDATE())
        """)
        result = db.session.execute(query)
        row = result.fetchone()
        return jsonify({"status": "success", "data": dict(row._mapping)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/report-summary/yearly', methods=['GET'])
def yearly_summary():
    try:
        from sqlalchemy import text
        query = text("""
            SELECT COUNT(*) AS Finished_Reports FROM final_report
            WHERE Status = 1 AND YEAR(Date) = YEAR(CURDATE())
        """)
        result = db.session.execute(query)
        row = result.fetchone()
        return jsonify({"status": "success", "data": dict(row._mapping)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/reports/by-week', methods=['GET'])
def reports_by_week():
    try:
        from sqlalchemy import text
        query = text("""
            SELECT
                WEEK(Date, 1) AS Week,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Unfinished' END AS Report_Status,
                COUNT(*) AS Total_Reports
            FROM final_report
            GROUP BY WEEK(Date, 1), Status ORDER BY Week
        """)
        result = db.session.execute(query)
        rows = [dict(row._mapping) for row in result]
        return jsonify({"status": "success", "data": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/update-remark', methods=['POST'])
def update_remark():
    try:
        data = request.get_json()
        date = data.get("Date")
        train_name = data.get("Train_Name")
        new_remark = data.get("Remarks")

        if not (date and train_name):
            return jsonify({"status": "error", "message": "Missing date or train name"}), 400

        # Update using SQLAlchemy ORM
        report = FinalReport.query.filter_by(Date=date, Train_Name=train_name).first()
        if report:
            report.Report_Remark = new_remark
            db.session.commit()
            return jsonify({"status": "success", "message": "Remark updated"})
        else:
            return jsonify({"status": "error", "message": "Report not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)})

@app.route('/cases/month', methods=['GET'])
def cases_by_month():
    try:
        from sqlalchemy import text
        query = text("""
        SELECT
            SI_No,
            DATE_FORMAT(Date, '%Y-%m-%d') AS Date,
            Train_Name,
            TIME_FORMAT(Time, '%h:%i %p') AS Time,
            Case_ID,
            Report_Remark AS Remarks,
            CASE
                WHEN Status = 1 THEN 'Closed'
                WHEN Status = 0 THEN 'Open'
                ELSE 'Unknown'
            END AS Case_Status,
            MONTH(Date) AS Month
        FROM final_report
        ORDER BY Month
        """)
        result = db.session.execute(query)
        rows = [dict(row._mapping) for row in result]
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/cases/week', methods=['GET'])
def cases_by_week():
    try:
        from sqlalchemy import text
        query = text("""
        SELECT
            SI_No,
            DATE_FORMAT(Date, '%Y-%m-%d') AS Date,
            Train_Name,
            TIME_FORMAT(Time, '%h:%i %p') AS Time,
            Case_ID,
            Report_Remark AS Remarks,
            CASE
                WHEN Status = 1 THEN 'Closed'
                WHEN Status = 0 THEN 'Open'
                ELSE 'Unknown'
            END AS Case_Status,
            WEEK(Date, 1) AS Week
        FROM final_report
        ORDER BY Week
        """)
        result = db.session.execute(query)
        rows = [dict(row._mapping) for row in result]
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/cases/year', methods=['GET'])
def cases_by_year():
    try:
        from sqlalchemy import text
        query = text("""
        SELECT
            SI_No,
            DATE_FORMAT(Date, '%Y-%m-%d') AS Date,
            Train_Name,
            TIME_FORMAT(Time, '%h:%i %p') AS Time,
            Case_ID,
            Report_Remark AS Remarks,
            CASE
                WHEN Status = 1 THEN 'Closed'
                WHEN Status = 0 THEN 'Open'
                ELSE 'Unknown'
            END AS Case_Status,
            YEAR(Date) AS Year
        FROM final_report
        ORDER BY Year
        """)
        result = db.session.execute(query)
        rows = [dict(row._mapping) for row in result]
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/report-summary/daily', methods=['GET'])
def report_summary_daily():
    try:
        from sqlalchemy import text
        query = text("""
        SELECT
            DATE_FORMAT(Date, '%Y-%m-%d') AS Date,
            SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Processed,
            SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Pending
        FROM final_report
        GROUP BY Date
        ORDER BY Date
        """)
        result = db.session.execute(query)
        rows = [dict(row._mapping) for row in result]
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/pending')
def get_pending():
    try:
        # Use SQLAlchemy ORM
        pending_cases = PendingCases.query.all()
        table_rows = [[case.id, case.status, case.train] for case in pending_cases]
        return jsonify({'reports': table_rows})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/zones', methods=['GET'])
def get_zones():
    zones = db.session.query(Station.zone).distinct().all()
    # Flatten and remove None
    zone_list = [z[0] for z in zones if z[0]]
    return jsonify(zone_list)

# ------------------- MAIN -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("✅ All endpoints are now active - authentication and merged backend combined!")
    app.run(host='0.0.0.0', port=5000, debug=True)
