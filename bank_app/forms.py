from django import forms

class regform(forms.Form):
    fname=forms.CharField(max_length=50)
    lname=forms.CharField(max_length=50)
    uname=forms.CharField(max_length=30)
    email=forms.EmailField()
    phone=forms.IntegerField()
    image=forms.FileField()
    pin=forms.IntegerField()
    repin=forms.IntegerField()

class logform(forms.Form):
    uname=forms.CharField(max_length=30)
    pin=forms.IntegerField()

class newsform(forms.Form):
    topic=forms.CharField(max_length=50)
    content=forms.CharField(max_length=200)


class adminlogform(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=20)

class cashsendform(forms.Form):
    name = forms.CharField(max_length=20)
    ac_num = forms.IntegerField()
    amount = forms.IntegerField()
