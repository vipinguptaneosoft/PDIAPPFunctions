#imports
import uuid
import pandas
import pickle
import os
import inspect
import shutil


#Django Imports
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

#App imports
from .models import (
    Case, 
    Task, 
    Function, 
    CaseTaskDetail, 
    FunctionParameterToPass, 
    TaskOutput
)
from .serializer import (
    CaseSearlizer, 
    TaskSearlizer, 
    FunctionSerializer, 
    CaseTaskDetailSerializer
)

#Function imports
from function_details.main import get_input_data
from function_details.reader_api import get_input_data2
from function_details.cycle_time_custom import get_cycle_time
from function_details.get_calculated_features import get_calc_cols
from function_details.get_process_data import get_process_data
from function_details.get_runs4 import get_run_number
from function_details.get_slopes2 import get_slopes
from function_details.limit import get_limit_flags
from function_details.get_rolling_data import get_rolling_data
from function_details.get_daily_average import get_daily_average
from function_details.split_data_v2 import generate_splits
from function_details.for_testing import for_tessting
from function_details.data_split import data_split
from function_details.drop_nan_splits import remove_nan_on_y
from function_details.drop_limit import drop_limit
from function_details.drop_nan import drop_nan
from function_details.remove_toggle  import  remove_toggel
from  function_details.fill_columns import backfill_columns
from function_details.merged import merge_dataframes
from function_details.fetch_data import fetch_data


@method_decorator(csrf_exempt, name='dispatch')
class CaseListAPI(APIView):

    def get(self, request):
        case_data = CaseSearlizer(
            Case.objects.filter(status=True), many=True).data
        return render(request, 'case.html', {"cases": case_data})

    def post(self, request):
        
        name = request.data['name']
        description = request.data['description']
        case_serial = CaseSearlizer(
            data={"name":  name, "description": description})
        if case_serial.is_valid():
            case_serial.save()
            return redirect('/cases')
        else:
            return JsonResponse({"msg": "not OK"}, status=400)


class CaseListDetailAPI(APIView):
    def get(self, request, pk):
        task_data = TaskSearlizer(Task.objects.filter(
                            case=pk).order_by('sequence'), many=True).data
        total_functions = FunctionSerializer(
                            Function.objects.all(),many=True).data

        return render(request, 'case_detail.html', {"data":  task_data, "total_function": total_functions,'case_id': pk})

    def put(self, request, pk):
        case_obj = Case.objects.get(id=pk)
        case_serial = CaseSearlizer(
            case_obj, data=dict(request.data), partial=True)
        if case_serial.is_valid():
            case_serial.save()
            return redirect(f'/cases/{pk}')
        else:
            return JsonResponse({"msg": "not ok"}, status=400)

    def delete(self, request, pk):
        case_obj = Case.objects.get(id=pk)
        case_serial = CaseSearlizer(
            case_obj, data={"status": False}, partial=True)
        if case_serial.is_valid():
            case_serial.save()
            return redirect(f'/cases/{pk}')
        else:
            return JsonResponse({"msg": "not ok"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class FunctionListAPI(APIView):
    def get(self, request):
        function_data = FunctionSerializer(
            Function.objects.all(), many=True).data
        return JsonResponse(function_data, safe=False)

    def post(self, request):
        function_serial = FunctionSerializer(data=dict(request.data))
        if function_serial.is_valid():
            function_serial.save()
            return JsonResponse({"msg": "saved"}, status=200)
        else:
            return JsonResponse({"msg": "not OK"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class AddTaskToCaseAPI(APIView):
    def post(self, request):
        case_id = request.data['case_id']
        function_id = request.data['fid']
        alias = request.data['alias']
        data = {
            "case": int(case_id),
            "alias": alias,
            "function": int(function_id),
            "unique_id": uuid.uuid4().hex,
            "custom_input_value": request.data['input_files'],
            "external_config": request.data['external_config']
        }
        task_serial = TaskSearlizer(data=data)
        if task_serial.is_valid():
            task_serial.save()
            status=200
        else:
            status=400
        return JsonResponse(data={}, status=status)


class FunctionDetailViaCase(APIView):

    def get(self, request, case_id, task_id):
        function_id = request.GET['function']
        task_id = task_id
        case_id = case_id
        function_obj = Function.objects.filter(id=function_id).first()
        task_obj = Task.objects.filter(case=case_id).order_by('sequence')

        case_task_detail = CaseTaskDetail.objects.filter(
            case=case_id, task=task_id, function=function_id)

        if not function_obj or not Task.objects.filter(id=task_id, case=case_id, function=function_id).first():
            return redirect(f'/cases/{case_id}')

        config_list = []
        if function_obj.config:
            config_list = function_obj.config.keys()
        case_function_detail_data = CaseTaskDetailSerializer(
            case_task_detail, many=True).data
        task_content_data = [{"id": task['id'], "data":list(
            task['data'].values())} for task in case_function_detail_data]

        config_list_serial = FunctionSerializer(
            function_obj).data.get("config")
        task_data = TaskSearlizer(task_obj, many=True).data
        total_functions = FunctionSerializer(
            Function.objects.all(),
            many=True).data
        if config_list_serial:
            table_tag = "<table style='border: 1px solid black;'><tr>"

            for i in config_list_serial:
                table_tag += f"<th style='border: 1px solid black;'> {i}</th>"
            table_tag += "</tr>"

            for i in task_content_data:
                table_tag += '<tr>'
                for j in i:
                    table_tag += f"<td style='border: 1px solid black;'> {j} </td>"
                table_tag += '</tr>'
        else:
             table_tag = ""
        task_obj = Task.objects.get(id=task_id)
        output_path = f'./output/{task_obj.case.id}/{task_obj.sequence}{task_obj.function.name}/'
        if os.path.exists(output_path):
            total_files = os.listdir(output_path)
            for files in total_files:
                file = pandas.read_csv(f"{output_path}{files}")
                if isinstance(file, pandas.DataFrame):
                     file.to_csv(f'{files}.csv')
        return render(request, 'case_detail.html', {"total_function": total_functions, "data": task_data, 'task_id': task_id, 'function_id': function_id, 'case_id': case_id, "table_tag": table_tag, 'function_config': config_list_serial, "headers": list(config_list), "task_content_data": task_content_data})


class GetExternalConfig(APIView):
    def get(self, request):
        function_id = request.GET.get('function_id')
        external_config = Function.objects.get(id=function_id).external_config
        return JsonResponse(external_config, safe=False)
    

@method_decorator(csrf_exempt, name='dispatch')
class StepTaskAPI(APIView):
    def post(self, request):
        request_data = dict(request.data)

        case_task_detail = {}
        del request_data["csrfmiddlewaretoken"]
        case_task_detail["function"] = request_data.pop("function_id")[0]
        case_task_detail["case"] = request_data.pop("case_id")[0]
        case_task_detail["task"] = request_data.pop("task_id")[0]
        for field in request_data:
            request_data[field] = request_data[field][0]
        case_task_detail["data"] = request_data

        case_function_serial = CaseTaskDetailSerializer(data=case_task_detail)
        case_function_serial.is_valid(raise_exception=True)
        case_function_serial.save()

        return redirect(request.META['HTTP_REFERER'])


@method_decorator(csrf_exempt, name='dispatch')
class DeleteCaseAPI(APIView):

    def post(self, request):
        try:
            case_obj = Case.objects.get(id=request.POST.get("case_id"))
            case_obj.status = False
            case_obj.save()
            return redirect('/cases')
        except:
            return redirect('/cases')


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFunctionAPI(APIView):

    def delete_tasks(self, task_id):
        tasks = Task.objects.get(id=task_id)
        if tasks.input_function:
            self.delete_tasks(tasks.input_function.id)
        tasks.delete()

    def post(self, request):
        try:
            tasks = Task.objects.get(id=request.POST.get("function_id"))
            tasks.delete()
            return redirect(f'/cases/{request.POST.get("case_id")}')
        except Exception as e:
            return JsonResponse({"msg": "Somethig went wrong"}, status=400)


class ExecuteStepsAPI(APIView):

    def call_merge_dataframes(self, request, function_obj, input_dataframe, task):
        task_detail_data = CaseTaskDetailSerializer(CaseTaskDetail.objects.filter(task=task.id), many=True).data

        more_input_params =  FunctionParameterToPass.objects.filter(function = task.function.id)
        input_dict = {}
        for values in task_detail_data:
            for param in more_input_params:
                if param.dict_config:
                    temp = {}
                    for key, val in param.dict_config.items():
                        if task.function.config[val] == 'number':
                            temp[values['data'][key]] = int(values['data'][val])
                        else:
                            temp[values['data'][key]] = values['data'][val]
                    input_dict[param.output_key] = temp
                elif param.list_config:
                    input_dict[param.output_key] = self.get_list_config_values(param, task)
                elif param.single_config:
                    input_dict[param.output_key] = values['data'][param.input_key]
                elif param.input_type == "external":
                    input_dict[param.output_key] = request.GET.get(param.input_key)
            # response = self.call_functions(input_dataframe[0][0], input_dataframe[0][1], **input_dict)
            response = function_obj(input_dataframe[0][0], input_dataframe[1][0],**input_dict)
            # FOLDER_PATH = f'./output/{task.case.id}/{task.sequence}{task.function.name}/'
            FOLDER_PATH = f'./output/{task.case.id}/'
            self.save_output_into_pickel(FOLDER_PATH, task.unique_id, response)

    def save_output_into_pickel(self, folder_path, name, response):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if isinstance(response, list) or isinstance(response, tuple):
            response[0].to_csv(f"{folder_path}{response[1]}.csv")
        elif isinstance(response, pandas.DataFrame):
            response.to_csv(f"{folder_path}{name}.csv")
        else:
            pickle.dump(response, open(f"{folder_path}{name}.p", "wb"))

    def call_get_slopes(self, function_obj, input_dataframe, task, request):
        task_detail_data = CaseTaskDetailSerializer(CaseTaskDetail.objects.filter(task=task.id), many=True).data

        more_input_params =  FunctionParameterToPass.objects.filter(function = task.function.id)
        for values in range(len(task_detail_data)):
            input_dict = {}
            for param in more_input_params:
                if param.dict_config:
                    temp = {}
                    for key, val in param.dict_config.items():
                        if task.function.config[val] == 'number':
                            temp[task_detail_data[values]['data'][key]] = int(task_detail_data[values]['data'][val])
                        else:
                            temp[task_detail_data[values]['data'][key]] = task_detail_data[values]['data'][val]
                    input_dict[param.output_key] = temp
                elif param.list_config:
                    input_dict[param.output_key] = self.get_list_config_values(param, task)
                elif param.single_config:
                    input_dict[param.output_key] = task_detail_data[0]['data'][param.input_key]
                elif param.input_type == "external":
                    input_dict[param.output_key] = request.GET.get(param.input_key)

            response, name = function_obj(input_dataframe[0][0],**input_dict)

            # FOLDER_PATH = f'./output/{task.case.id}/{task.sequence}{task.function.name}/'
            FOLDER_PATH = f'./output/{task.case.id}/{task.function.name}/'
            self.save_output_into_pickel(FOLDER_PATH, name, response)

    def call_generate_splits(self, function_obj):
        response = function_obj()
        return response
    
    def call_remove_nan_on_y(self, function_obj, input_dataframe, task):
        input_dict = {i:i for i in input_dataframe[0]}
        response = function_obj(input_dict)
        for name in response:
            # FOLDER_PATH = f'./output/{task.case.id}/{task.sequence}{task.function.name}/'
            FOLDER_PATH = f'./output/{task.case.id}/'
            self.save_output_into_pickel(FOLDER_PATH, name, response)

    def fill_parameters(self, params, data):
        temp_dict = {}
        if isinstance(params.config, dict):
            for key, value in params.config.items():
                temp_dict[key] = data[value]
        if isinstance(params.config, list):
            temp_dict[data[params.config[0]]] = data[params.config[1]]

        return temp_dict

    def get_dict_config_values(self, param, task):
        param_data = {}
        
        task_detail_data = CaseTaskDetailSerializer(CaseTaskDetail.objects.filter(task=task.id), many=True).data
        for values in task_detail_data:
            for key, val in param.dict_config.items():
                if task.function.config[val] == 'number':
                    param_data[values['data'][key]] = int(values['data'][val])
                else:
                    param_data[values['data'][key]] = values['data'][val]
        return param_data
    
    def get_list_config_values(self, param, task):
        param_data = []
        task_detail_data = CaseTaskDetailSerializer(CaseTaskDetail.objects.filter(task=task.id), many=True).data
        for values in task_detail_data:
            temp = values['data'][param.input_key]
            param_data.append(temp)
        return param_data

    def get_single_config_values(self, param, task):
        task_detail_data = CaseTaskDetailSerializer(CaseTaskDetail.objects.filter(task=task.id), many=True).data
        for values in task_detail_data:
            temp = values['data'][param.input_key]
            return temp
    
    def get_input_params(self, request, task):
        payload = {}
        more_input_params = FunctionParameterToPass.objects.filter(function = task.function.id)

        for param in more_input_params:
            if param.dict_config:
                payload[param.output_key] = self.get_dict_config_values(param, task)
            elif param.list_config:
                payload[param.output_key] = self.get_list_config_values(param, task)
            elif param.single_config:
                payload[param.output_key] = self.get_single_config_values(param, task)
            elif param.input_type == "external":
                payload[param.output_key] = request.GET.get(param.input_key)
        return payload

    def call_functions(self, payload, input_dataframe,function_obj):
        response = None
        function_actual_params = inspect.getfullargspec(function_obj).args
        if function_actual_params:
            if payload:
                if isinstance(input_dataframe, tuple):
                    input_dataframe = input_dataframe[0]
                if isinstance(input_dataframe, pandas.DataFrame) or isinstance(input_dataframe, str):
                    response = function_obj(input_dataframe, **payload)
                else:
                    response = function_obj(**payload)
            else:
                if isinstance(input_dataframe, pandas.DataFrame) or isinstance(input_dataframe, str):
                    response = function_obj(input_dataframe)
        else:
            response = function_obj()
        return response

    def get(self, request):
        case_id = request.GET.get("case")
        tasks_to_execute = Task.objects.filter(
            case=case_id).order_by('sequence')
        if os.path.exists(f'./output/{case_id}'):
            shutil.rmtree(f'./output/{case_id}')

        for task in range(len(tasks_to_execute)):
            input_dataframe, payload = None, {}
            print("*******************************************************")
            print(tasks_to_execute[task].id, tasks_to_execute[task].function.name)
            print("*******************************************************")
            if tasks_to_execute[task].custom_input_value and task!=0:
                INPUT_FOLDER_PATH = f'./output/{case_id}'

                if tasks_to_execute[task].custom_input_value: 
                    multiple_input_list = tasks_to_execute[task].custom_input_value.split(',')[:-1]
                    input_dataframe = []
                    for i in multiple_input_list:
                        file = pandas.read_csv(f"{INPUT_FOLDER_PATH}/{i}", index_col=[0])
                        input_dataframe.append([file,  i])
                else:
                    task_obj = Task.objects.get(unique_id=tasks_to_execute[task].input_function)
                    input_dataframe = pandas.read_csv(f"{INPUT_FOLDER_PATH}{task_obj.unique_id}.csv")
            
            function_obj = eval(tasks_to_execute[task].function.name)
            if tasks_to_execute[task].function.name == 'remove_nan_on_y':
                self.call_remove_nan_on_y(function_obj, input_dataframe, tasks_to_execute[task])
                continue
            if tasks_to_execute[task].function.name == 'merge_dataframes':
                self.call_merge_dataframes(request, function_obj, input_dataframe, tasks_to_execute[task])
                continue
            payload = self.get_input_params(request, tasks_to_execute[task])
            if tasks_to_execute[task].external_config:
                for key, value in tasks_to_execute[task].external_config.items():
                    payload[key] = value

            if isinstance(input_dataframe, list) or isinstance(input_dataframe, tuple):
                for dataframe in input_dataframe:
                    name = tasks_to_execute[task].unique_id

                    response =  self.call_functions(payload, dataframe[0], function_obj)
                    name = tasks_to_execute[task].unique_id
                    if len(response)>1 and not isinstance(response, pandas.DataFrame):
                        name = response[1]
                    FOLDER_PATH = f'./output/{tasks_to_execute[task].case.id}/'
                    if tasks_to_execute[task].function.name  == 'get_slopes':
                        self.save_output_into_pickel(FOLDER_PATH, name, response)
                        FOLDER_PATH += f'/{tasks_to_execute[task].function.name}/'
                    self.save_output_into_pickel(FOLDER_PATH, name, response)
            else:
                response =  self.call_functions(payload, input_dataframe, function_obj)
                name = tasks_to_execute[task].unique_id
                FOLDER_PATH = f'./output/{tasks_to_execute[task].case.id}/'
                self.save_output_into_pickel(FOLDER_PATH, name, response)

        if isinstance(response, tuple):
            response = response[0]
        if isinstance(response, pandas.DataFrame):
            response = response.to_html()
        return JsonResponse({"data": response}, safe=False)





@method_decorator(csrf_exempt, name='dispatch')
class ChangeSequenceAPI(APIView):

    def get(self, request, id1, id2):

        task_object1 = Task.objects.get(id=id1)
        task_object2 = Task.objects.get(id=id2)

        task_object1.sequence, task_object2.sequence = task_object2.sequence, task_object1.sequence

        task_object2.save()
        task_object1.save()

        return JsonResponse({"msg": "Success"}, status=200)


class GetInfo(APIView):

    def get(self, request):
        data = request.GET
        task_detail_id = request.GET.get('task_detail_id')
        case_id = request.GET.get('case_id')
        function_id = request.GET.get('function_id')
        task_id = request.GET.get('task_id')
        case_task_obj = CaseTaskDetail.objects.get(id=task_detail_id)
        case_task_serial_data = CaseTaskDetailSerializer(case_task_obj).data

        function_config = FunctionSerializer(case_task_obj.function).data.get("config")
        task_detail_id = data.get('task_details_id')
        body = ""
        for key, val in case_task_serial_data['data'].items():
            type_of_input = function_config[key]
            if function_config[key].lower() =='dataframe':
                body +='<label>'+key+'</label>' + \
                        '<select id="merge_function_input_'+key+'" name="function_input" onchange="check_for_multiple_input_in_merge('+case_id+', '+key+')" class="form-control form-select" style="width:100%">'+\
                        '<option value="">-------</option>'
                for d in Function.objects.all():
                    body += '<option value='+ d.id+ '>'+ d.alias+'</option>' 
                body += '</select><select id="merge_input_dataframe_'+key+'" name="input_dataframe" class="form-control form-select disable_class" required disabled style="width:100%">'+\
                        '<option>---------</option></select>'
            else:
                body += '<label>' + key + '</label>'+'<input type="' + type_of_input + \
                    '" class="form-control form-control-modern"' + \
                        'name="' + key + '" value="'+val+'" />'
        body += f'''
                <input type="hidden" class="form-control form-control-modern"
                name="task_details_id" required value="{case_task_serial_data['id']}" />
                <input type="hidden" class="form-control form-control-modern"
                        name="function_id" required value="{ function_id }" />
                <input type="hidden" class="form-control form-control-modern"
                        name="case_id" required value="{ case_id }" />
                <input type="hidden" class="form-control form-control-modern"
                        name="task_id" required value="{ task_id }" /> 
                '''
        footer = f"""
            <button type="button" class="btn btn-secondary"
                data-dismiss="modal">Cancel</button>
            <button type="submit" class="btn btn-primary">Add</button>
        """
        return JsonResponse({"body": body, "footer": footer})


class EditTaskDetail(APIView):

    def post(self, request):
        data = request.data.dict()
        case_id = data.pop('case_id')
        task_id = data.pop('task_id')
        function_id = data.pop('function_id')
        task_detail_id = data.pop('task_details_id')
        data.pop('csrfmiddlewaretoken')

        task_detail_obj = CaseTaskDetail.objects.get(id=task_detail_id)
        task_detail_serial = CaseTaskDetailSerializer(
            task_detail_obj, data={"data": data}, partial=True)
        if task_detail_serial.is_valid():
            task_detail_serial.save()
        else:
            print(task_detail_serial.errors)
        return redirect(("/cases/"+case_id+"/task/"+task_id+"/?function="+function_id))


class DeleteTaskData(APIView):
    def post(self, request):
        case_id = request.POST.get('case_id')
        task_id = request.POST.get('task_id')
        function_id = request.POST.get('function_id')
        CaseTaskDetail.objects.get(
            id=request.POST.get('task_detail_id')).delete()
        return redirect("/cases/"+case_id+"/task/"+task_id+"/?function="+function_id)


class GetMultipleInput(APIView):
    def get(self, request):
        return_data = []
        task_output_queryset = TaskOutput.objects.filter(case=request.GET.get('case_id'))
        for i in task_output_queryset:
            return_data.append(i.task.alias)
        return JsonResponse(return_data, safe=False)


class CheckMultipleInput(APIView):
    def get(self, request):
        case_id = request.GET.get('case')
        task_id = request.GET.get('function')
        task_obj = Task.objects.get(id=task_id)
        FOLDER_PATH = f'./output/{case_id}/'
        return_file_name = []
        if task_obj.function.name == 'get_slopes':
            FOLDER_PATH = FOLDER_PATH + f'{task_obj.function.name}'

            if os.path.exists(FOLDER_PATH):
                file_names= os.listdir(FOLDER_PATH)
            
            for file in file_names:
                return_file_name.append(file)

        elif os.path.exists(FOLDER_PATH):
            file_names= os.listdir(FOLDER_PATH)
            for file in file_names:
                if file.startswith(f'{task_obj.unique_id}'):
                    return_file_name.append(file)

        return JsonResponse(data=return_file_name, safe=False)


class GetFunctionViaID(APIView):
    def get(self,  request):
        return JsonResponse(TaskSearlizer(Task.objects.get(id=request.GET.get('function_id'))).data, status=200)


class GetTaskData(APIView):
    def get(self, request, id):
        task_obj = Task.objects.get(id=id)
        case_id = request.GET.get('case_id')
        task_data = TaskSearlizer(task_obj, many=True).data

        total_functions = FunctionSerializer(
            Function.objects.all(),
            many=True).data

        return render(request, 'case_detail.html', {"total_function": total_functions, "data": task_data, 'task_id': task_id, 'function_id': function_id, 'case_id': case_id, "table_tag": table_tag, 'function_config': config_list_serial, "headers": list(config_list), "task_content_data": task_content_data})
