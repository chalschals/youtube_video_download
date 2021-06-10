from django.db import models

# Create your models here.


class Youtube(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=2250)
    sourcttype = models.CharField(max_length=20)
    resolution = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
