from django.db import models

# Create your models here.


class Users(models.Model):
    class Meta:
        db_table = 'users'
    
    user_id = models.BigAutoField(primary_key=True)
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
