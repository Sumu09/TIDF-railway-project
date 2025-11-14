from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Report, Station, Signup
from .serializers import ReportSerializer
from django.shortcuts import get_object_or_404
import datetime

# Helper to get current user from JWT
def get_current_user(request):
    auth = JWTAuthentication()
    user_auth_tuple = auth.authenticate(request)
    if user_auth_tuple is not None:
        user, _ = user_auth_tuple
        return user
    return None

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trains(request):
    """Equivalent to /trains (JWT protected)"""
    user = request.user
    # Assuming user is linked to Signup via OneToOne or ForeignKey
    try:
        signup = Signup.objects.get(ph_no=user.username)  # username is phone number
    except Signup.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    station_name = None
    if signup.station_code:
        station = Station.objects.filter(station_code=signup.station_code.station_code).first()
        if station:
            station_name = station.station_name
        trains = Report.objects.filter(station_code=signup.station_code)
    else:
        trains = Report.objects.all()
    now = datetime.datetime.now().strftime('%I:%M %p')
    train_list = []
    for train in trains:
        train_dict = ReportSerializer(train).data
        train_dict['time'] = train.time.strftime('%I:%M %p') if train.time else now
        train_dict['sl_no'] = train.si_no
        train_dict['name'] = train.train_name
        train_dict['report_id'] = train.report_id
        train_dict['status'] = "Finished" if train.status else "Unfinished"
        train_list.append(train_dict)
    return Response({
        'trains': train_list,
        'station_name': station_name,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def train_report(request):
    """Equivalent to /train-report (JWT protected)"""
    report_id = request.GET.get('id')
    if report_id:
        report = Report.objects.filter(report_id=report_id).first()
    else:
        report = Report.objects.order_by('si_no').first()
    if not report:
        return Response({'error': 'Report not found'}, status=404)
    return Response(ReportSerializer(report).data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_train(request, report_id):
    """Equivalent to /trains/<report_id> (PATCH, JWT protected)"""
    report = get_object_or_404(Report, report_id=report_id)
    new_name = request.data.get('name')
    if not new_name:
        return Response({'error': 'Missing train name'}, status=400)
    report.train_name = new_name
    report.status = 1  # Mark as finished
    report.save()
    return Response({'success': True, 'updated_report': ReportSerializer(report).data})

from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def serialize_result(rows, columns):
    result = []
    for row in rows:
        item = {}
        for idx, col in enumerate(columns):
            value = row[idx]
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            item[col] = value
        result.append(item)
    return result

@api_view(['GET'])
def report_summary_weekly(request):
    """Equivalent to /report-summary/weekly"""
    try:
        with connection.cursor() as cursor:
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
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return Response({"status": "success", "data": serialize_result(rows, columns)})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def report_summary_monthly(request):
    """Equivalent to /report-summary/monthly"""
    try:
        with connection.cursor() as cursor:
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
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return Response({"status": "success", "data": serialize_result(rows, columns)})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def report_summary_yearly(request):
    """Equivalent to /report-summary/yearly"""
    try:
        with connection.cursor() as cursor:
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
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return Response({"status": "success", "data": serialize_result(rows, columns)})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def cases_by_week(request):
    """Equivalent to /cases/week"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    SI_No,
                    DATE_FORMAT(Date, '%%Y-%%m-%%d') AS Date,
                    Train_Name,
                    TIME_FORMAT(Time, '%%h:%%i %%p') AS Time,
                    Case_ID,
                    Report_Remark AS Remarks,
                    CASE
                        WHEN Status = 1 THEN 'Closed'
                        WHEN Status = 0 THEN 'Open'
                        ELSE 'Unknown'
                    END AS Case_Status
                FROM final_report
                WHERE YEARWEEK(Date, 1) = YEARWEEK(CURDATE(), 1)
                ORDER BY Date DESC, Time DESC;
            """)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return Response({"status": "success", "data": serialize_result(rows, columns)})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def cases_by_month(request):
    """Equivalent to /cases/month"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    SI_No,
                    DATE_FORMAT(Date, '%%Y-%%m-%%d') AS Date,
                    Train_Name,
                    TIME_FORMAT(Time, '%%h:%%i %%p') AS Time,
                    Case_ID,
                    Report_Remark AS Remarks,
                    CASE
                        WHEN Status = 1 THEN 'Closed'
                        WHEN Status = 0 THEN 'Open'
                        ELSE 'Unknown'
                    END AS Case_Status
                FROM final_report
                WHERE YEAR(Date) = YEAR(CURDATE()) AND MONTH(Date) = MONTH(CURDATE())
                ORDER BY Date DESC, Time DESC;
            """)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return Response({"status": "success", "data": serialize_result(rows, columns)})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def cases_by_year(request):
    """Equivalent to /cases/year"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    SI_No,
                    DATE_FORMAT(Date, '%%Y-%%m-%%d') AS Date,
                    Train_Name,
                    TIME_FORMAT(Time, '%%h:%%i %%p') AS Time,
                    Case_ID,
                    Report_Remark AS Remarks,
                    CASE
                        WHEN Status = 1 THEN 'Closed'
                        WHEN Status = 0 THEN 'Open'
                        ELSE 'Unknown'
                    END AS Case_Status
                FROM final_report
                WHERE YEAR(Date) = YEAR(CURDATE())
                ORDER BY Date DESC, Time DESC;
            """)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return Response({"status": "success", "data": serialize_result(rows, columns)})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def reports_by_week(request):
    """Equivalent to /reports/week"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    WEEK(Date, 1) AS Week,
                    COUNT(*) AS Total_Reports,
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Finished,
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Pending
                FROM report
                GROUP BY Week
                ORDER BY Week;
            """)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return Response({"status": "success", "data": serialize_result(rows, columns)})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def reports_by_month(request):
    """Equivalent to /reports/month"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    MONTH(Date) AS Month,
                    COUNT(*) AS Total_Reports,
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Finished,
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Pending
                FROM report
                GROUP BY Month
                ORDER BY Month;
            """)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return Response({"status": "success", "data": serialize_result(rows, columns)})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def reports_by_year(request):
    """Equivalent to /reports/year"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    YEAR(Date) AS Year,
                    COUNT(*) AS Total_Reports,
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Finished,
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Pending
                FROM report
                GROUP BY Year
                ORDER BY Year;
            """)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return Response({"status": "success", "data": serialize_result(rows, columns)})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)