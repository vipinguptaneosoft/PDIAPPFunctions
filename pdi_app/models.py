from django.db import models

# Create your models here.


#Model for Cases
class Case(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    

    def __str__(self) -> str:
        return self.name


# Model for Function Config
class Function(models.Model):
    name = models.TextField()
    config = models.JSONField(blank=True, null=True)
    external_config = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


#Tasks in perticular Cases
class Task(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    alias = models.TextField(default='Alias', unique=True)
    unique_id = models.TextField()
    input_function = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_custom_input = models.BooleanField(default=False)
    custom_input_value = models.TextField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    external_config = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.alias+"==>"+ self.unique_id
    
    def save(self, *args, **kwargs):
        if not self.sequence:
            try:
                self.sequence = int(Task.objects.latest('sequence').sequence) + 1
            except:
                try:
                    self.sequence = int(Task.objects.latest('id').id) +1
                except:
                    self.sequence = 1
        super(Task, self).save(*args, **kwargs)


# Config of each Task.
class CaseTaskDetail(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    function = models.ForeignKey(Function,on_delete=models.CASCADE)
    data = models.JSONField()

    def __str__(self) -> str:
        return str(self.task.unique_id)  +"==>" + self.function.name


# For saving the Output for each task
class TaskOutput(models.Model):
    OUTPUT_TYPE = (
        ('dataframe', 'dataframe'),
        ('files', 'files')
    )
    case = models.ForeignKey(Case, on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    output = models.JSONField(blank=True, null=True)
    output_type = models.CharField(choices=OUTPUT_TYPE, max_length=10, default='dataframe')

    def __str__(self) -> str:
        return str(self.task.unique_id)  +"==>" + self.function.name


# Parameters of the functions
class FunctionParameterToPass(models.Model):
    inputType = (
        ('internal', "internal"),
        ('external', "external")
    )

    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    output_key = models.TextField(blank=True, null=True)
    input_key = models.TextField(blank=True, null=True)
    dict_config = models.JSONField(blank=True, null=True)
    list_config = models.TextField(blank=True, null=True)
    single_config = models.TextField(blank=True, null=True)
    function_input = models.ForeignKey(TaskOutput, blank=True, null=True, on_delete=models.CASCADE, related_name='function_input')
    is_multiple = models.BooleanField(default=False)
    multiple_input = models.JSONField(blank=True, null=True)
    output_type = models.CharField(blank=True, null=True, max_length=10)
    input_type = models.CharField(choices=inputType, default="internal", max_length=10)

    def __str__(self) -> str:
        return self.function.name+"====>"+self.output_key
