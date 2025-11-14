from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime, date, time, timedelta
from flask import request

app = Flask(__name__)
CORS(app)

# ------------------------------------
# ✅ DATABASE CONFIG
# ------------------------------------
def get_mysql_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='train2'
    )

# ------------------------------------
# ✅ SERIALIZER UTILS
# ------------------------------------
def serialize_result(rows):
    for row in rows:
        for key in row:
            if isinstance(row[key], (datetime, date, time, timedelta)):
                row[key] = str(row[key])
            elif isinstance(row[key], (bytes, bytearray)):
                row[key] = row[key].decode()
    return rows

# ------------------------------------
# 🚆 TRAIN REPORT ROUTES
# ------------------------------------

@app.route('/train-report/week', methods=['GET'])
def train_report_by_week():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                WEEK(Date, 1) AS Week,
                Date,
                Time,
                Train_Name,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report
            ORDER BY Week;
        """)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/train-report/month', methods=['GET'])
def train_report_by_month():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                MONTH(Date) AS Month,
                Date,
                Time,
                Train_Name,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report
            ORDER BY Month;
        """)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/train-report/year', methods=['GET'])
def train_report_by_year():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                YEAR(Date) AS Year,
                Date,
                Time,
                Train_Name,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report
            ORDER BY Year;
        """)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

# ------------------------------------
# 📋 FINAL REPORT SUMMARY ROUTES
# ------------------------------------

@app.route('/report-summary/weekly', methods=['GET'])
def weekly_summary():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                YEAR(Date) AS Year,
                WEEK(Date) AS Week,
                COUNT(*) AS Finished_Reports
            FROM final_report
            WHERE Status = 1
            GROUP BY YEAR(Date), WEEK(Date)
            ORDER BY Year, Week;
        """)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/report-summary/monthly', methods=['GET'])
def monthly_summary():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                YEAR(Date) AS Year,
                MONTH(Date) AS Month,
                COUNT(*) AS Finished_Reports
            FROM final_report
            WHERE Status = 1
            GROUP BY YEAR(Date), MONTH(Date)
            ORDER BY Year, Month;
        """)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/report-summary/yearly', methods=['GET'])
def yearly_summary():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                YEAR(Date) AS Year,
                COUNT(*) AS Finished_Reports
            FROM final_report
            WHERE Status = 1
            GROUP BY YEAR(Date)
            ORDER BY Year;
        """)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

# ------------------------------------
# 🚨 CASES ROUTES
# ------------------------------------

@app.route('/cases/week', methods=['GET'])
def cases_by_week():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
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
            ORDER BY Week;
        """)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/cases/month', methods=['GET'])
def cases_by_month():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
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
            ORDER BY Month;
        """)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/cases/year', methods=['GET'])
def cases_by_year():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
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
            ORDER BY Year;
        """)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

# ------------------------------------
# 🚨 REPORT STATUS BREAKDOWN ROUTES
# ------------------------------------

@app.route('/reports/by-week', methods=['GET'])
def reports_by_week():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                WEEK(Date, 1) AS Week,
                CASE
                    WHEN Status = 1 THEN 'Finished'
                    ELSE 'Unfinished'
                END AS Report_Status,
                COUNT(*) AS Total_Reports
            FROM final_report
            GROUP BY WEEK(Date, 1), Status
            ORDER BY Week;
        """)
        return jsonify({"status": "success", "data": cursor.fetchall()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/update-remark', methods=['POST'])
def update_remark():
    try:
        data = request.get_json()
        date = data.get("Date")
        train_name = data.get("Train_Name")
        new_remark = data.get("Remarks")

        if not (date and train_name):
            return jsonify({"status": "error", "message": "Missing date or train name"}), 400

        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE final_report
            SET Report_Remark = %s
            WHERE Date = %s AND Train_Name = %s
        """, (new_remark, date, train_name))
        conn.commit()

        return jsonify({"status": "success", "message": "Remark updated"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()


@app.route('/')
def home():
    return jsonify({"message": "🚆 Mega Flask Backend is Running!"})

# ------------------------------------
# 🏁 MAIN RUN
# ------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
