from django.db import models

# Create your models here.
class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name1 = models.CharField(max_length=50)
    name2 = models.CharField(max_length=50)
    mat = models.CharField(max_length=100)

    def __str__(self):
        return self.name1 + ' vs. ' + self.name2