from django.db import models

# Create your models here.


class AuthTokens(models.Model):
    class Meta:
        db_table = 'ins_auth_tokens'

    access_token = models.TextField(null=True, db_column="auth_access_token")
    refresh_token = models.TextField(null=True, db_column="auth_refresh_token")
    created_at = models.DateTimeField(auto_now_add=True)
    