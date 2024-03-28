from django.db import models
from django.contrib.auth.models import User

class SavedGoods(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    price = models.CharField(max_length=255, db_index=True)
    url = models.CharField(max_length=255, db_index=True)
   