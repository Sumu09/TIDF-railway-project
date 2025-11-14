from django.shortcuts import render
from datetime import datetime

# from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist


# @login_required
def root_page_view(request):
    try:
        return render(request, 'index.html')
        # return render(request, 'pages/station-admin/station-admin.html', {'user_type': 'StationAdmin'})

    except TemplateDoesNotExist:
        return render(request, 'pages-404.html')


# @login_required
def dynamic_pages_view(request, template_name):
    # Add logic to map template_name to the correct file
    template_map = {
        'index': 'index.html',
        'auth-login': 'pages/auth-login.html',
        'auth-signup': 'pages/auth-signup.html',
        #
        'ground-staff': 'pages/ground-staff/ground-staff.html',
        'train-report': 'pages/ground-staff/train-report.html',
        #
        'station-admin': 'pages/station-admin/station-admin.html',
        'apps-calendar': 'pages/station-admin/apps-calendar.html',
        'calendar': 'pages/station-admin/calendar.html',
        'current-pending': 'pages/station-admin/current-pending.html',
        #
        'zonal-head': 'pages/zonal-head/zonal-head.html',
        #
        'pages-404': 'pages/pages-404.html',
        # add more as needed
    }
    template_path = template_map.get(template_name, f'pages/{template_name}.html')

    # Determine user type based on template_name
    context = {}
    if template_name == 'station-admin' or template_name == 'apps-calendar' or template_name == 'current-pending':
        context['user_type'] = 'station-admin'
    elif template_name == 'ground-staff' or template_name == 'train-report':
        context['user_type'] = 'ground-staff'
    elif template_name == 'zonal-head':
        context['user_type'] = 'zonal-head'

    try:
        return render(request, template_path, context)
    except TemplateDoesNotExist:
        return render(request, 'pages-404.html')
