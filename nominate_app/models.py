from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=300, blank=False)
    email = models.CharField(max_length=300, blank=False)
    designation = models.CharField(max_length=300, blank=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.ename

class Roles(models.Model):
    name = models.CharField(max_length=300, blank=False)
    hierarchy_level = models.IntegerField(default=1, blank=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.name

class User_Role(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        db_table = 'user_role'