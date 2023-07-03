from rest_framework import serializers
from .models import  Case, Task, Function, CaseTaskDetail, TaskOutput, FunctionParameterToPass


class CaseSearlizer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'


class TaskSearlizer(serializers.ModelSerializer):
    function_name = serializers.SerializerMethodField()
    function_id = serializers.SerializerMethodField()

    def get_function_name(self, obj):
        return Function.objects.get(name = obj.function).name
    
    def get_function_id(self, obj):
        return Function.objects.get(name=obj.function).id

    class Meta:
        model = Task
        fields = '__all__'


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = '__all__'


class CaseTaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseTaskDetail
        fields = '__all__'


class TaskOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskOutput
        fields = '__all__'


class FunctionParameterToPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionParameterToPass
        fields = '__all__'
