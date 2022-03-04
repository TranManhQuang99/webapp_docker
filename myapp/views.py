
from unicodedata import name
from django.shortcuts import render,redirect
from .models import Employee
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Employee
# from myapp.forms import DataForm
import xlwt
import csv
import pymongo
from django.conf import settings
import re
from django.core.paginator import Paginator
from .forms import EmployeeForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import GetaAllEmployeeSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import requests
import json

# from myapp.documents import PostDocument

my_client = pymongo.MongoClient(settings.DB_NAME)

dbname = my_client['123a']
collection_name = dbname["myapp_employee"]
global employee
employee = Employee.objects.all()



@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    if request.method == 'GET':
        tutorials = Employee.objects.all()
        
        title = request.GET.get('Key_word', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = GetaAllEmployeeSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = GetaAllEmployeeSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Employee.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    try: 
        tutorial = Employee.objects.get(pk=pk) 
    except Employee.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = GetaAllEmployeeSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = GetaAllEmployeeSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def tutorial_list_published(request):
    tutorials = Employee.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = GetaAllEmployeeSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    


def welcome(request):
    return render(request, 'data.html', {'employee': employee})

def form(request):
    
    return render(request, 'form.html')

def pagination(request):
    collection_name.find().sort('time',pymongo.DESCENDING)
    paginator = Paginator(employee, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'data.html', context={'employee':page_obj})


def search(request):
    page_number = request.GET.get('page')
    if not page_number:
        global employee_search
        global social_network
        social_network = request.POST.get('Social_Network', "")
        key = request.POST.get('Key_word', "")

        # names = request.POST.get('Names', "")
        # re_pat = re.compile(str(social_network))
        # re_pat1 = re.compile(str(key))

        # if ( not social_network and key == ''):
        #     myquery = {"Social_Network": {"$regex": re_pat}}
            
        # elif(key != None and social_network != ""):
        #     myquery = {"Social_Network":{"$regex": re_pat},"Key_word":{"$regex": re_pat1}}
            
        # elif(social_network != None and social_network == "" and key != None):
        #     myquery = {"Key_word": {"$regex": re_pat1}}
            
        # myquery = {"Social_Network":{"$regex": re_pat},"Key_word":{"$regex": re_pat1}}
        # mydoc = collection_name.find(myquery)
        # print("mydoc", mydoc)
        
        # employee = []
        # for i in mydoc:
        #     employee.append(i)
        # print(len(employee))s
        employee_search = Employee.objects.filter(Social_Network__icontains=social_network, Key_word__icontains=key)

    paginator = Paginator(employee_search,20)
    page_obj = paginator.get_page(page_number)
    return render(request, 'data.html', {'choice':social_network ,'employee':page_obj})

def search1(request):
    page_number = request.GET.get('page')
    if not page_number:
        global employee_search
        global Names
        Names = request.POST.get('Names', "")
        post = request.POST.get('post', "")
        employee_search = Employee.objects.filter(Names__icontains= Names, post__icontains=post)
        
    paginator = Paginator(employee_search,20)
    page_obj = paginator.get_page(page_number)
    return render(request, 'data.html', {'employee':page_obj})

def export_excel(request):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Id', 'Social_Network', 'Key_word', 'Names', 'Link_post', 'post', 'comment', 'device','location','time']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()

    rows = Employee.objects.all().values_list('Id', 'Social_Network', 'Key_word', 'Names', 'Link_post', 'post', 'comment', 'device','location','time')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Id', 'Social_Network', 'Key_word', 'Names', 'Link_post', 'post', 'comment', 'device','location','time'])

    users = Employee.objects.all().values_list('Id', 'Social_Network', 'Key_word', 'Names', 'Link_post', 'post', 'comment', 'device','location','time')
    for user in users:
        writer.writerow(user)

def elasticsearch():
    
    url = "http://10.0.8.114:9200/monstache_test/_search"

    payload = json.dumps({
    "query": {
        "match": {
        "post": "AI"
        }
    },
    "size": 100
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    hits = json.loads(response.text)
    data = (hits['hits']['hits'])

    for i in data:
        print(i['_source'])

# def search_elas(request):
    
#     q = request.GET.get("q")
    
#     if q:
#         posts = PostDocument.search().query("match",title=q)
#     else:
#         posts = ""
        
#     return render(request,"search.html",{"employee":employee})