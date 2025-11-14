from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('report-summary/weekly/', views.report_summary_weekly, name='report-summary-weekly'),
    path('report-summary/monthly/', views.report_summary_monthly, name='report-summary-monthly'),
    path('report-summary/yearly/', views.report_summary_yearly, name='report-summary-yearly'),

    path('cases/week/', views.cases_by_week, name='cases-by-week'),
    path('cases/month/', views.cases_by_month, name='cases-by-month'),
    path('cases/year/', views.cases_by_year, name='cases-by-year'),

    path('reports/week/', views.reports_by_week, name='reports-by-week'),
    path('reports/month/', views.reports_by_month, name='reports-by-month'),
    path('reports/year/', views.reports_by_year, name='reports-by-year'),
]
