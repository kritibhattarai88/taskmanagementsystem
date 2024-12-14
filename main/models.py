from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    STATUS_CHOICES =[
    ('not_started','Not started'),
    ('in_progress','In progress'),
    ('completed','Completed'),
]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    description=models.TextField()
    start_date=models.DateField(null=True, blank=True)
    end_date=models.DateField(null=True, blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='not_started')
     
    is_deleted = models.BooleanField(default=False)
    delete_time = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    
class Assign_task(models.Model):
    STATUS_CHOICES =[
    ('not_started','Not started'),
    ('in_progress','In progress'),
    ('completed','Completed'),
]
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='not_started')
    due_date=models.DateField(null=True, blank=True)
    assign_to = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='assigned_tasks'
    )
    
    assigned_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tasks_assigned_by', 
        null=True
    )
    

    is_deleted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    
    def __str__(self) -> str:
        return self.title