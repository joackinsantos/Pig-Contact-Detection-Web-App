from django.db import models

# Create your models here.
class NameTester(models.Model):
    name=models.CharField(max_length=100)
    des=models.TextField()
    def __str__(self) -> str:
        return super().__str__()