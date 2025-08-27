from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Title=models.CharField(max_length=100)
    Description=models.TextField(blank=True)
    Isdone=models.BooleanField(default=False)
    due_date=models.DateField()
    updated_at=models.DateTimeField(auto_now=True)
    created_date=models.DateTimeField(auto_now_add=True)
    priority = models.CharField(
        max_length=10,
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        default='Medium'
    )
    def __str__(self):
        return f"{self.Title[:10]} -{self.priority}"
