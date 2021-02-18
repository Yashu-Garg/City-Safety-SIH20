from django.shortcuts import render,redirect
from . import forms
from . import models
from .DataAnalytics import datafile
from django.contrib import messages
from django.utils import timezone,datetime_safe
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail,EmailMultiAlternatives
import simplejson as json
from twilio.rest import Client
from django.utils.timezone import activate
from BaitRescrusers import settings
import datetime
from django.utils.timezone import utc
from rest_framework import viewsets
from .serializers import API
import pytz
from datetime import datetime
activate(settings.TIME_ZONE)
# Create your views here.
class PeopleView(viewsets.ModelViewSet):
    queryset=models.People.objects.all()
    serializer_class=API


def home(request):
    # if request.user.is_authenticated:
    #     messages.info(request, 'Logged in')
    if request.method == 'POST':
        data = request.POST['district']
        print(data)
        if data=='1':
            return redirect('/')
        return redirect('district/' + data + '/')
    else:
        district = datafile.getdistrict()
        district.sort()
        print("home",request.get_host())
    return render(request,'specific_home.html',{'list': district})

def Register(request):
    if request.method=="POST":
        Android = False
        for keys in request.POST:
            if keys == 'app':
                Android = True
                break
        print(request.body)
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['EmailId']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.info(request, 'Registration Successfull')
            if Android:
                return JsonResponse({'Status': "Signed Up"})
            else:
                return redirect('/')

        if Android:
            return JsonResponse({'Status': "Invalid Content"})
        else:
            return render(request, 'register.html', {"form": form})
    else:
        form=forms.RegisterForm
        return render(request,'register.html',{'form':form})

def Login(request):
    if request.method == 'POST':
        Android = False
        for keys in request.POST:
            if keys == 'app':
                Android = True
                break
        print(Android)
        form = forms.LoginForm(request.POST)
        print(request.POST)
        if form.is_valid():
            email = form.cleaned_data['EmailId']
            password = form.cleaned_data['password']
            #print(form)
            # messages.info(request, 'user' + email + password)
            current_user = authenticate(username=email, password=password)

            print('current user',current_user)
            if current_user is not None:
                messages.info(request, 'Login Successful')
                login(request, current_user)
                print('Login at 16 jan',current_user)

                if Android:
                    return JsonResponse({'Status':"Logged in","sessionid":request.session.session_key,"EmailId":current_user.EmailId})
                else:
                    return redirect('/')
            else:
                if Android:
                    return JsonResponse({'Status': "Invalid Username/Password"})
                else:
                    messages.info(request, 'Invalid Username/Password')
        else:
            if Android:
                return JsonResponse({'Status': 'Invalid form'})
            else:
                messages.info(request,'Invalid form')
                return render(request, 'login.html', {"form": form})

    form=forms.LoginForm
    return render(request,'login.html',{'form':form})


def Logout(request):
    logout(request)
    return redirect('/login/')

def SaveLocation(request):
    if request.method=='POST':
        data=request.POST
        print(data)
        coordinates=[float(data['lat']),float(data['lng'])]
        current_user=models.People.objects.get(EmailId=request.user.EmailId)
        if len(coordinates)!=2:
            current_user.Latitude=99.9
            current_user.Longitude=1729 #For Debugging
            current_user.City='Jalandhar'
            #current_user.LocationDateTime(datetime.now())
            print('something just happened')
        else:
            current_user.Latitude = coordinates[0]
            current_user.Longitude = coordinates[1]
            current_user.City = 'Jalandhar'
            current_user.LocationDateTime=datetime.now()
            #current_user.LocationDateTime(timezone.now)
            print("User is changed accordingly")
            current_user.save()
            dict = {'status': 'success'}
            return HttpResponse(json.dumps(dict), content_type='application/json')

        #coordinates=[1,2]
        print(coordinates)
        return render(request, 'maps.html', {"lat": coordinates[0], "lng": coordinates[1]})
    else:
        return render(request,'test.html')

def UpTest(request):
    if request.method=='POST':
        data=request.POST
        print('in uptest',data)
    return redirect('/')


def Map(request):
    if request.user.is_authenticated:
        #Here everything with that location pie charts dangerous would come
        city='CP Jalandhar'
        analysis=datafile.yashu('CP JALANDHAR', gender=request.user.gender)
        chart = analysis['loc']
        url = request.get_host()+'/maps/' + request.user.EmailId + '/'
        email_message=analysis['msg']+'\n'+ url + '\n'+analysis['number']
        data = []
        for x in chart:
            data.append(x)
        data.pop()
        print(data)
        # labels=['MURDER','RAPE','THEFT','ACCIDENT','ROBBERY']
        labels = ["MURDER"]

        dangerous=True
        if dangerous==False:
            print('dangerous',dangerous)
            subject="Automated message By django"
            message=email_message
            from_email='ashishjain0338@gmail.com'
            print(request.user.EmailId)
            # to_list=[request.user.EmailId]
            to_list = ['ashishjain0338@gmail.com']
            var=send_mail(subject,message,from_email,to_list,fail_silently=True)
            print('Check Email Status',var)
            #For text Messages we need to put Twilio Credential in Private Section
            # accountSid = 'Private'
            # authToken = 'Private'
            # twilioClient = Client(accountSid, authToken)
            # myTwilioNumber = 'Private'
            # destCellPhone = request.user.ContactNumber
            # if len(destCellPhone)!=13:
            #     destCellPhone = 'Private'
            #     message='Not a valid number to send the message.\nThe number given is'+request.user.ContactNumber
            #     print('here')
            # myMessage = twilioClient.messages.create(body=message, from_=myTwilioNumber,
            #                                          to=destCellPhone)
            # print('Text Status', myMessage.status)

        return render(request, 'maps.html', {"lat": request.user.Latitude, "lng": request.user.Longitude,
                                             "data": data, "labels": labels,'user':request.user})
    else:
        messages.info(request, 'Please first login to continue')
        return redirect('/login/')

def MainDistress(request,user_id):
    print("Im in Main Distress",user_id)
    count_request=models.PersonInNeed.objects.filter(person__EmailId__contains=user_id).count()
    print(count_request)
    if count_request!=0:
        if count_request==1:
            current_user=models.PersonInNeed.objects.get(person__EmailId__contains=user_id)
            current_user.Longitude = request.user.Longitude
            current_user.Latitude = request.user.Latitude
            current_user.City = 'Jalandhar' #replace this with request.user.City
            current_user.Added_at = datetime.now()
            current_user.save()
        else:
            print("Error how can two same distress can be stored at the database")

        print("Need to update this")
    else:
        persons=models.PersonInNeed()
        persons.person=request.user
        persons.Longitude=request.user.Longitude
        persons.Latitude=request.user.Latitude
        persons.City=request.user.City
        persons.Added_at=datetime.now()
        print(persons.save())
        print(persons)
    return render(request,'distress.html',{'user':current_user})

def Police(request):
    if request.user.is_authenticated:
        info=models.PersonInNeed.objects.all()
        for x in info:
            print(x.Longitude,x.Latitude)
            print(x.person.RecoveryNumber)
        return render(request,'police.html',{"data":info})
    else:
        messages.info(request,'Please Login To continue')
        return redirect('/login/')

def District(request,dis):
    if request.method=='POST':
        data = request.POST['district']
        print(data)
        if data=='1':
            return redirect('/district/' + dis + '/')
        return redirect('/district/' + data + '/')

    district = datafile.getdistrict()
    district.sort()

    analysis = datafile.yashu(dis, gender='M')
    chart = analysis['loc']
    data = []
    for x in chart:
        data.append(x)
    data.pop()
    print(data)

    return render(request,'district.html',{'data':data,'district':dis,'list':district})

def AndroidDistrict(request,dis):
    #if request.method=='POST':
        #data = request.POST['district']
        #print(data)
        #if data=='1':
            #return redirect('/district/' + dis + '/')
        #return JsonResponse({'data':data,'district':dis,'labels':['MURDER','RAPE','THEFT','ACCIDENT','ROBBERY']})

    district = datafile.getdistrict()
    district.sort()

    analysis = datafile.yashu(dis, gender='M')
    chart = analysis['loc']
    danger = analysis['danger']
    danger=1
    print('danger',danger)
    data = []
    for x in chart:
        data.append(x)
    data.pop()
    #print(data)
    return JsonResponse({'data':data,'danger':int(danger),'district':dis,'labels':['MURDER','RAPE','THEFT','ACCIDENT','ROBBERY']})

def Test(request):
    if request.method=='POST':
        print("Data Posted in test")
        data = request.POST
        print('files', request.FILES)
        key=False
        for keys in request.FILES.keys():
            key=keys
        if key:
            data1=request.FILES[key]
            # user=models.Audio()
            # user.aud=data1
            # user.name='testset'
            # user.save()
            current_user=models.PersonInNeed.objects.get(person__EmailId__contains=key)
            current_user.audio = data1
            current_user.save()
            print("Audio got and Saved!!!!!!!!!!!!!!")
            print('files',data1)
            print(data)
        return JsonResponse({'test':True})
    else:
        # print(datetime.now())
        # print("Get Request in test")
        # current_user=models.Audio.objects.get(name='testlast')
        # print(current_user.aud.url[10:])
        # # return JsonResponse({'test': True,'url':current_user.audio.url})
        # return render(request,'free.html',{'audio':current_user.aud.url[10:]})
        return JsonResponse({'data':'something'})

def trackandroidlocation(request):
    Status='404'
    if request.method=='POST':
        print('datta',request.POST)
        print("\n")
        print("Tracking  :  "+request.POST['email'])
        print("Coordinates are   :   "+request.POST['Longitude']+", "+request.POST['Latitude'])
        print("Address is   :   "+request.POST['Address'])
        print("\n")
        data=request.POST
        user_id = data['email']
        current_user=models.People.objects.get(EmailId=user_id)
        current_user.Longitude = float(data['Longitude'])
        current_user.Latitude = float(data['Latitude'])
        current_user.City = 'Jalandhar'#data['city']  # replace this with request.user.City
        current_user.Address = data['Address']
        current_user.LocationDateTime = datetime.now() #datetime.datetime.utcnow().replace(tzinfo=utc)
        current_user.save()
        if current_user.City=='Jalandhar' and Status=='404':
            pass
        else:
            city = 'CP Jalandhar'
            analysis = datafile.yashu('CP JALANDHAR', gender=current_user.gender)
            chart = analysis['loc']
            url = 'localhost:8000/maps/' + request.user.EmailId + '/'
            # url='https://www.google.com/search?q=books&oq=books&aqs=chrome..69i57j0l6j69i61.3591j0j7&sourceid=chrome&ie=UTF-8'
            email_message = analysis['msg'] + '\n' + url + '\n' + analysis['number']
            dangerous = True
            if dangerous == False:
                subject = "Automated message By django"
                message = email_message
                from_email = 'ashishjain0338@gmail.com'
                print(current_user.EmailId)
                if Status=='404':
                    to_list = ['ashishjain0338@gmail.com']
                else:
                    to_list = [current_user.EmailId]
                # to_list = ['pjain0338@gmail.com']
                var = send_mail(subject, message, from_email, to_list, fail_silently=True)
                print('Check Email Status', var)
                # For text Messages we need to put Twilio Credential in Private Section
                # accountSid = 'Private'
                # authToken = 'Private'
                # twilioClient = Client(accountSid, authToken)
                # myTwilioNumber = 'Private'
                # destCellPhone = request.user.ContactNumber
                # if len(destCellPhone)!=13:
                #     destCellPhone = 'Private'
                #     message='Not a valid number to send the message.\nThe number given is'+request.user.ContactNumber
                #     print('here')
                # myMessage = twilioClient.messages.create(body=message, from_=myTwilioNumber,
                #                                          to=destCellPhone)
                # print('Text Status', myMessage.status)

    return JsonResponse({"Gettin Location":"Yes"})

def distresssignal(request):
    if request.method=='POST':
        print("#################################################")
        print("EMERGENCY DISTRESS SIGNAL")
        print("#################################################")
        print("Tracking  :  "+request.POST['email'])
        print("Coordinates are   :   "+request.POST['Longitude']+", "+request.POST['Latitude'])
        print("Address is   :   "+request.POST['Address'])
        # print("Content is   :   " + request.POST['Content'])
        print("#################################################")
        print("HELP NEEDED URGENTLY")
        print("#################################################")
        data=request.POST
        print('data',data)
        print('files',request.FILES)
        user_id = data['email']
        count_request = models.PersonInNeed.objects.filter(person__EmailId__contains=user_id).count()
        print(count_request)
        print('hey',type(float(data['Longitude'])))
        if count_request != 0:
            if count_request == 1:
                current_user = models.PersonInNeed.objects.get(person__EmailId__contains=user_id)
                current_user.Longitude = float(data['Longitude'])
                current_user.Latitude = float(data['Latitude'])
                current_user.City = 'Jalandhar'  # replace this with request.user.City
                current_user.Address=data['Address']
                # current_user.Added_at = datetime.datetime.utcnow().replace(tzinfo=utc)
                current_user.Added_at = datetime.now()
                # current_user.audio = request.FILES['uploadedfile']
                current_user.save()
            else:
                print("Error how can two same distress can be stored at the database")
            print("Need to update this")
        else:
            persons = models.PersonInNeed()
            persons.person = models.People.objects.get(EmailId=user_id)
            persons.Longitude = float(data['Longitude'])
            persons.Latitude = float(data['Latitude'])
            persons.City = 'Jalandhar'
            persons.Address=data['Address']
            # persons.Added_at = datetime.datetime.utcnow().replace(tzinfo=utc)
            persons.Added_at = datetime.now()
            # persons.audio = request.FILES['uploadedfile']
            datetime.now()
            print(persons.save())
            print(persons)

        activate(settings.TIME_ZONE)
        current_user = models.People.objects.get(EmailId=user_id)
        # data = models.PersonInNeed.objects.get(person__EmailId=user_id)
        # now = datetime.datetime.utcnow().replace(tzinfo=utc)
        # print(data.Added_at, now)

    return JsonResponse({"Gettin Location":"Yes"})

def AndroidMaps(request):
    print('in Android maps')
    return render(request,'AndroidMaps.html')