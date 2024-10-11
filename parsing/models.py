from django.db import models
from django.contrib.auth.models import User


class SavedGoods(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    price = models.CharField(max_length=255, db_index=True) 
    url = models.CharField(max_length=255, db_index=True)
    image = models.CharField(max_length=600, db_index=True, default='https://st4.depositphotos.com/14953852/22772/v/450/depositphotos_227725020-stock-illustration-image-available-icon-flat-vector.jpg')