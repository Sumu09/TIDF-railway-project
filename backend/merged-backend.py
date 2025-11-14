# Merged Flask Backend for Station Admin, Calendar, and Cases
# This single file combines the logic from index.py, apps-calendar.py, and casespending_json.py

from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from datetime import datetime, date, time, timedelta

# ------------------------------------
# ✅ 1. APP INITIALIZATION
# ------------------------------------
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for the entire app

# -----------------------------------
# ✅ 2. DATABASE CONFIGURATION
# (Unified function for the entire application)
# ------------------------------------
def get_mysql_connection():
    """
    Creates and returns a connection to the MySQL database.
    """
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',  # Replace with your actual password if different
        database='train2'
    )

# ------------------------------------
# ✅ 3. SERIALIZER UTILITY
# (Combined function to handle all necessary data types)
# ------------------------------------
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

# ------------------------------------
# ✅ 4. API ROUTES
# (All unique routes from the three files are merged below)
# ------------------------------------

# --- Main Health Check Route ---
@app.route('/')
def home():
    """
    A simple health check endpoint to confirm the server is running.
    """
    return jsonify({"message": "🚆 Merged Flask Backend is Running Successfully!"})

# --- Routes from index.py ---

@app.route('/train-report/week', methods=['GET'])
def train_report_by_week():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                WEEK(Date, 1) AS Week, Date, Time, Train_Name,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report ORDER BY Date DESC;
        """)
        return jsonify({"status": "success", "data": serialize_result(cursor.fetchall())})
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
                MONTH(Date) AS Month, Date, Time, Train_Name,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report ORDER BY Date DESC;
        """)
        return jsonify({"status": "success", "data": serialize_result(cursor.fetchall())})
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
                YEAR(Date) AS Year, Date, Time, Train_Name,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report ORDER BY Date DESC;
        """)
        return jsonify({"status": "success", "data": serialize_result(cursor.fetchall())})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/report-summary/weekly', methods=['GET'])
def weekly_summary():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT COUNT(*) AS Finished_Reports FROM final_report
            WHERE Status = 1 AND YEARWEEK(Date, 1) = YEARWEEK(CURDATE(), 1);
        """)
        return jsonify({"status": "success", "data": cursor.fetchone()})
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
            SELECT COUNT(*) AS Finished_Reports FROM final_report
            WHERE Status = 1 AND YEAR(Date) = YEAR(CURDATE()) AND MONTH(Date) = MONTH(CURDATE());
        """)
        return jsonify({"status": "success", "data": cursor.fetchone()})
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
            SELECT COUNT(*) AS Finished_Reports FROM final_report
            WHERE Status = 1 AND YEAR(Date) = YEAR(CURDATE());
        """)
        return jsonify({"status": "success", "data": cursor.fetchone()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/reports/by-week', methods=['GET'])
def reports_by_week():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                WEEK(Date, 1) AS Week,
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Unfinished' END AS Report_Status,
                COUNT(*) AS Total_Reports
            FROM final_report
            GROUP BY WEEK(Date, 1), Status ORDER BY Week;
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
            UPDATE final_report SET Report_Remark = %s WHERE Date = %s AND Train_Name = %s
        """, (new_remark, date, train_name))
        conn.commit()
        return jsonify({"status": "success", "message": "Remark updated"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

# --- Routes from apps-calendar.py ---

# @app.route('/cases/month', methods=['GET'])
# def cases_by_month():
#     try:
#         conn = get_mysql_connection()
#         cursor = conn.cursor(dictionary=True)
#         query = """
#         SELECT
#             SI_No, DATE_FORMAT(Date, '%Y-%m-%d') AS Date, Train_Name,
#             TIME_FORMAT(Time, '%h:%i %p') AS Time, Case_ID, Report_Remark AS Remarks,
#             CASE WHEN Status = 1 THEN 'Closed' ELSE 'Open' END AS Case_Status
#         FROM final_report ORDER BY Date DESC;
#         """
#         cursor.execute(query)
#         return jsonify({"status": "success", "data": serialize_result(cursor.fetchall())})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})
#     finally:
#         cursor.close()
#         conn.close()

# 🚨 CASES BY MONTH
@app.route('/cases/month', methods=['GET'])
def cases_by_month():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
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
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()

# 🚨 CASES BY WEEK
@app.route('/cases/week', methods=['GET'])
def cases_by_week():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
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
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()

# 🚨 CASES BY YEAR
@app.route('/cases/year', methods=['GET'])
def cases_by_year():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
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
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()

# 🚨 DAILY REPORT SUMMARY (Processed vs Pending)
@app.route('/report-summary/daily', methods=['GET'])
def report_summary_daily():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            DATE_FORMAT(Date, '%Y-%m-%d') AS Date,
            SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Processed,
            SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Pending
        FROM final_report
        GROUP BY Date
        ORDER BY Date;
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()


# @app.route('/cases/week', methods=['GET'])
# def cases_by_week():
#     try:
#         conn = get_mysql_connection()
#         cursor = conn.cursor(dictionary=True)
#         query = """
#         SELECT
#             SI_No, DATE_FORMAT(Date, '%Y-%m-%d') AS Date, Train_Name,
#             TIME_FORMAT(Time, '%h:%i %p') AS Time, Case_ID, Report_Remark AS Remarks,
#             CASE WHEN Status = 1 THEN 'Closed' ELSE 'Open' END AS Case_Status
#         FROM final_report ORDER BY Date DESC;
#         """
#         cursor.execute(query)
#         return jsonify({"status": "success", "data": serialize_result(cursor.fetchall())})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})
#     finally:
#         cursor.close()
#         conn.close()

# @app.route('/cases/year', methods=['GET'])
# def cases_by_year():
#     try:
#         conn = get_mysql_connection()
#         cursor = conn.cursor(dictionary=True)
#         query = """
#         SELECT
#             SI_No, DATE_FORMAT(Date, '%Y-%m-%d') AS Date, Train_Name,
#             TIME_FORMAT(Time, '%h:%i %p') AS Time, Case_ID, Report_Remark AS Remarks,
#             CASE WHEN Status = 1 THEN 'Closed' ELSE 'Open' END AS Case_Status
#         FROM final_report ORDER BY Date DESC;
#         """
#         cursor.execute(query)
#         return jsonify({"status": "success", "data": serialize_result(cursor.fetchall())})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})
#     finally:
#         cursor.close()
#         conn.close()

# @app.route('/report-summary/daily', methods=['GET'])
# def report_summary_daily():
#     try:
#         conn = get_mysql_connection()
#         cursor = conn.cursor(dictionary=True)
#         query = """
#         SELECT
#             DATE_FORMAT(Date, '%Y-%m-%d') AS Date,
#             SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Processed,
#             SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Pending
#         FROM final_report GROUP BY Date ORDER BY Date;
#         """
#         cursor.execute(query)
#         return jsonify({"status": "success", "data": serialize_result(cursor.fetchall())})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})
#     finally:
#         cursor.close()
#         conn.close()

# --- Routes from casespending_json.py ---

@app.route('/pending')
def get_pending():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        # Assuming 'pending_cases' is the correct table name
        cursor.execute("SELECT id, train, status FROM pending_cases;")
        data = cursor.fetchall()
        table_rows = [[row['id'], row['status'], row['train']] for row in serialize_result(data)]
        return jsonify({'reports': table_rows})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# ------------------------------------
# ✅ 5. MAIN EXECUTION BLOCK
# ------------------------------------
if __name__ == '__main__':
    print("✅ All endpoints are now active.")
    app.run(port=5001, debug=True)
