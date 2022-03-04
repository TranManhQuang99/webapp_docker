from rest_framework import serializers
from .models import Employee


class GetaAllEmployeeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        fields = "__all__"
        
        