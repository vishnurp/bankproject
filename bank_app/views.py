import os

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.core.mail import send_mail

def registration(request):
    if request.method=='POST':
        datas=regform(request.POST,request.FILES)
        if datas.is_valid():
            fn=datas.cleaned_data['fname']
            ln=datas.cleaned_data['lname']
            un=datas.cleaned_data['uname']
            em=datas.cleaned_data['email']
            ph=datas.cleaned_data['phone']
            ac=int("15"+str(ph))

            im=datas.cleaned_data['image']
            p=datas.cleaned_data['pin']
            rp=datas.cleaned_data['repin']
            if p==rp:
                b=regmodel(fname=fn,lname=ln,uname=un,email=em,phone=ph,image=im,pin=p,balance=0,ac_num=ac)
                b.save()
                subject= "Your account has been created"
                message= f"Your new account number is {ac}"
                email_from = "rpvichu65@gmail.com"
                email_to = em
                send_mail(subject,message,email_from,[email_to])
                return redirect(login)
            else:
                return HttpResponse("Pin does not match...")
        else:

            return HttpResponse("Registration failed")
    return render(request,'reg.html')


def login(request):
    if request.method=='POST':
        a=logform(request.POST)
        if a.is_valid():
            unm=a.cleaned_data['uname']
            pl=a.cleaned_data['pin']
            b=regmodel.objects.all()
            for i in b:
               if i.uname==unm and i.pin==pl:
                   request.session['id']=i.id
                   # return HttpResponse('Login success')
                   return redirect(profile)
            else:
                return HttpResponse('login failed')
    return render(request,'index.html')

def forgot_password(request):
    a = regmodel.objects.all()
    if request.method == 'POST':
        em = request.POST.get('email')
        # ac = request.POST.get('ac_num')
        for i in a:
            if (i.email == em ) :
                id = i.id
                subject = "password change"
                message = f'http://127.0.0.1:8000/bank_app/change/{id}'
                frm ="rpvichu65@gmail.com"
                to = em
                send_mail(subject,message,frm,[to])
                return HttpResponse("check mail")
        else:
            return HttpResponse("sorry")
    return render(request,'forgotpassword.html')

def change_password(request,id):
    a = regmodel.objects.get(id=id)
    if request.method =='POST':
        p1 = request.POST.get('pin')
        p2 = request.POST.get('repin')
        if p1 == p2:
            a.pin = p1
            a.save()
            return HttpResponse("Password changed")
        else:
            return HttpResponse("Sorry")
    return render(request,'change.html')





def profile(request):
    try:
       id1=request.session['id']
       a=regmodel.objects.get(id=id1)
       img=str(a.image).split('/')[-1]
       return render(request,'profile.html',{'a':a,'img':img})
    except:
        return redirect(login)


def editdet(request,id):
    a=regmodel.objects.get(id=id)
    if request.method=='POST':
        a.fname=request.POST.get('fname')
        a.lname=request.POST.get('lname')
        a.email=request.POST.get('email')
        a.phone=request.POST.get('phone')
        a.save()
        return redirect(profile)
    return render(request,'editdetails.html',{'a':a})

def edimage(request,id):
    a=regmodel.objects.get(id=id)
    im=str(a.image).split('/')[-1]
    if request.method=='POST':
        if len(request.FILES) != 0:
            if len(a.image) !=0:
                os.remove(a.image.path)
            a.image=request.FILES['image']
        a.save()
        return redirect(profile)
    return render(request,'editimage.html',{'a':a,'im':im})

def addmoney(request,id):
    x=regmodel.objects.get(id=id)
    if request.method=='POST':
        am=request.POST.get('amount')
        request.session['am']=am
        request.session['ac']=x.ac_num
        b=addamount(amount=am,uid=request.session['id'])
        b.save()

        x.balance+=int(am)
        x.save()
        pin=request.POST.get('pin')
        if int(pin)==x.pin :
            return  redirect(success)
        else:
            return HttpResponse('amount added failed')
    return render(request,'addamount.html')


def success(request):
    am= request.session['am']
    ac=request.session['ac']
    return render(request, 'success.html',{'am':am,'ac':ac})

def withdrawmoney(request,id):
    a=regmodel.objects.get(id=id)
    if request.method=='POST':
        amt=request.POST.get('withdrawamt')
        request.session['amt']=amt
        w=withdraw(withdrawamt=amt,uid=request.session['id'])
        w.save()

        if a.balance >= int(amt):
            a.balance -= int(amt)
            a.save()
            pin = request.POST.get('pin')
            if int(pin)==a.pin :
                return redirect(debit)
                # return HttpResponse('Amount debited successfully')
            else:
                return HttpResponse('pin ERROR')
        else:
            return HttpResponse("Sorry you have not enough money")
    return render(request,'withrdraw.html')

def debit(request):
    amt=request.session['amt']
    ac = request.session['ac']
    return render(request,'debit.html',{'amt':amt,'ac':ac})



def checkbalance(request,id):
    b=regmodel.objects.get(id=id)
    if request.method=='POST':
        pin = request.POST.get('pin')
        balance=b.balance
        request.session['bal']=balance
        request.session['ac'] = b.ac_num
        if int(pin)==b.pin :
            return redirect(balancedisplay)
        else:
            return HttpResponse("PIN error")
    return render(request,'balance.html')

def balancedisplay(request):
    bal = request.session['bal']
    ac = request.session['ac']
    return render(request, 'balancedisplay.html', {'balance': bal, 'ac': ac})


def ministatement(request,id):
    a=regmodel.objects.get(id=id)
    pin=request.POST.get('pin')

    if request.method=='POST':
        if int(pin)==a.pin:
            depdetails=request.POST.get('choice')
            if depdetails=='am':
                return redirect(depmini)
            elif depdetails=='withdraw':
                return redirect(withmini)
        else:
            return HttpResponse("PIN ERROR")
    return render(request,'ministatement.html')

def depmini(request):
    a=addamount.objects.all()
    id=request.session['id']
    return render(request,'depositstatement.html',{'a':a,'id':id})

def withmini(request):
    a=withdraw.objects.all()
    id =request.session['id']
    return render(request,'withdrawstatement.html',{'a':a,'id':id})



def news(request):
    if request.method=='POST':
        a=newsform(request.POST)
        if a.is_valid():
            tp=a.cleaned_data['topic']
            cnt=a.cleaned_data['content']
            b=newsmodel(topic=tp,content=cnt)
            b.save()
            return redirect(newsdisadmin)
            # return HttpResponse("ADDED SUCCESSFULLY")
        else:
            return HttpResponse("FAILED")
    return render(request,'news.html')

def newsdisplay(request):
    x=newsmodel.objects.all()

    return render(request,'newsdisplay.html',{'x':x})

def newsdisadmin(request):
    y = newsmodel.objects.all()
    return render(request,'adminnewsdisplay.html',{'y':y})

def newsedit(request,id):
    a= newsmodel.objects.get(id=id)
    if request.method=='POST':
        if request.POST.get('content')=='':
            a.save()
        else:
             a.topic=request.POST.get('topic')
        a.content=request.POST.get('content')
        a.save()
        return redirect(newsdisadmin)
    return render(request,'newsedit.html',{'a':a})

def deletenews(request,id):
    a= newsmodel.objects.get(id=id)
    a.delete()
    return redirect(newsdisadmin)

from django.contrib import messages
def wish(request,id):

    a=newsmodel.objects.get(id=id)
    wish=wishlist.objects.all()
    for i in wish:
        if i.newsid==a.id and i.uid == request.session['id']:

            return HttpResponse('item already in wishlist')
    b=wishlist(topic=a.topic,content=a.content,date=a.date,newsid=a.id,uid=request.session['id'])
    b.save()
    return HttpResponse("added to wishlist")

def wishlistpg(request):
    a= wishlist.objects.all()
    id=request.session['id']
    return render(request,'wishlist.html',{'a':a,'id':id})
def wishremove(request,id):
    a=wishlist.objects.get(id=id)
    a.delete()
    return redirect(wishlistpg)


from django.contrib.auth import authenticate
def loginadmin(request):
    if request.method=='POST':
        a= adminlogform(request.POST)
        if a.is_valid():
            us=a.cleaned_data['username']
            ps=a.cleaned_data['password']
            user=authenticate(request,username=us,password=ps)
            if user is not None:
                return redirect(admindis)

            else:
                return HttpResponse("LOGIN FAILED")
    return render(request,'adminlogin.html')

def admindis(request):
    return render(request,'admindispla.html')




def tablesearch(request):
    return render(request,'tablesearch.html')


from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect(login)

def cashsendingview(request,id):
    c = regmodel.objects.get(id=id)
    if request.method=="POST":
        datas=cashsendform(request.POST)
        request.session['balance'] = c.balance
        if datas.is_valid():
            acname=datas.cleaned_data['name']
            acno=datas.cleaned_data['ac_num']
            amnt=datas.cleaned_data['amount']
            b=regmodel.objects.all()
            for i in b:
                if acname == i.uname and acno == i.ac_num:

                    request.session['id1']=i.id
                    if c.balance>=int(amnt):
                        c.balance-=int(amnt)
                        c.save()
                        i.balance+=int(amnt)
                        print(i.balance,i.uname,amnt)
                        print(c.balance,c.uname,amnt)
                        i.save()
                        return redirect(sendsuccess)
                    else:
                        return HttpResponse('no balance')
            else:
                    print(i.uname)
                    return HttpResponse('failed')

    return render(request,'transfer.html',{'datas':c})

def sendsuccess(request):
    amt = request.POST.get('amount')
    return render(request,'sendsuccess.html',{'a':amt})














# Create your views here.
