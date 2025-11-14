
from rest_framework import serializers
from .models import Station, Signup, Report, FinalReport, PendingCases

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class FinalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalReport
        fields = '__all__'

class PendingCasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingCases
        fields = '__all__'
