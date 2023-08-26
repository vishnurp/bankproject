from django.db import models

# Create your models here.
class regmodel(models.Model):
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    uname=models.CharField(max_length=30)
    email=models.EmailField()
    phone=models.IntegerField()
    image=models.FileField(upload_to='bank_app/static')
    pin=models.IntegerField()
    balance=models.IntegerField()
    ac_num=models.IntegerField()



class addamount(models.Model):
    uid=models.IntegerField()
    amount=models.IntegerField()
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.uid)

class withdraw(models.Model):
    uid=models.IntegerField()    # NEWLY ADDED
    withdrawamt = models.IntegerField()
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.uid)

class newsmodel(models.Model):
    topic=models.CharField(max_length=50)
    content=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)


class wishlist(models.Model):
    uid=models.IntegerField()
    newsid=models.IntegerField()
    topic = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    date = models.DateField()








