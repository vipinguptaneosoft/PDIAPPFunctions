from django.contrib import admin
from .models import Case, Task, Function, CaseTaskDetail, FunctionParameterToPass,  TaskOutput

admin.site.register(Case)
admin.site.register(Task)
admin.site.register(Function)
admin.site.register(CaseTaskDetail)
admin.site.register(FunctionParameterToPass)
admin.site.register(TaskOutput)