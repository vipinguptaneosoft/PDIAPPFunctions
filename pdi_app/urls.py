from django.urls import path
from .views import (CaseListAPI, CaseListDetailAPI, FunctionListAPI, AddTaskToCaseAPI, FunctionDetailViaCase,
                    StepTaskAPI, DeleteCaseAPI, DeleteFunctionAPI, ExecuteStepsAPI, ChangeSequenceAPI,
                    GetInfo, EditTaskDetail, DeleteTaskData, GetMultipleInput, CheckMultipleInput, GetFunctionViaID,
                    GetExternalConfig, GetTaskData)

urlpatterns = [
    path('add_task/', AddTaskToCaseAPI.as_view()),
    path('cases/', CaseListAPI.as_view()),
    path('cases/<int:pk>/', CaseListDetailAPI.as_view()),
    path('cases/<int:case_id>/task/<int:task_id>/', FunctionDetailViaCase.as_view()),
    path('task/<int:id>/', GetTaskData.as_view()),
    path('function_detail/', FunctionListAPI.as_view()),
    path('add_step_task/', StepTaskAPI.as_view()),
    path('delete_case/', DeleteCaseAPI.as_view()),
    path('delete_task/', DeleteFunctionAPI.as_view()),
    path('execute_functions/', ExecuteStepsAPI.as_view()),
    path('change_sequence/<int:id1>/<int:id2>/', ChangeSequenceAPI.as_view()),
    path('get_info/', GetInfo.as_view()),
    path('edit_task_detail/', EditTaskDetail.as_view()),
    path('delete_task_data/', DeleteTaskData.as_view()),
    path('get_multiple_input/', GetMultipleInput.as_view()),
    path('check_for_multiple_input/', CheckMultipleInput.as_view()),
    path('get_function_via_id/', GetFunctionViaID.as_view()),
    path('get_external_config/', GetExternalConfig.as_view()),
]
