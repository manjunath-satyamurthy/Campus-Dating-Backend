import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from models import AppUser
from dbapi import *


@csrf_exempt
def login(request):
    if request.method == 'POST':
        print "here"
        data = json.loads(request.POST['data'])
        userId, password = data['userId'], data['password']
        users = AppUser.objects.filter(user_Id=userId, password=password).all()
        if users.count() > 0:
            user = users[0]
            response =  HttpResponse(json.dumps({
                'status': 'success',
                'firstName': user.firstname,
                'lastName': user.lastname,
                'age': user.age,
                'sex': user.sex,
                'height': user.height,
                'bodyType': user.body_type,
                'fromAge': user.from_age,
                'toAge': user.to_age,
                'partner': user.partner,
                'partnerHeight': user.partner_height,
                'partnerBodyType': user.partner_body_type,
                }))
            response["Access-Control-Allow-Origin"] = "*"
            return response

        response = HttpResponse(json.dumps({
            'status': 'failed'
            }))
        response["Access-Control-Allow-Origin"] = "*"
        return response


@csrf_exempt
def upload_photo(request):
    if request.method == 'POST':
        photo = request.FILES['photo']
        user_Id = request.POST['userId']
        print photo

        user = AppUser.objects.filter(user_Id=user_Id)[0]
        user.upload_photo(photo)
        user.save()
        return  HttpResponse(json.dumps({
                'status': 'success'
                }))


@csrf_exempt
def update_info(request):
    if request.method == 'POST':
        data = json.loads(request.POST['data'])
        user_id = data['user_id']
        user = AppUser.objects.filter(user_Id=user_id)[0]
        user.update(
            data['userAge'], data['userSex'], data['userHeight'],
            data['userBody'], data['fromAge'], data['toAge'],
            data['partnerValue'], data['heightValue'], 
            data['bodyValue']
            )
        response =  HttpResponse(json.dumps({
            'status': 'success'
            }))
        response["Access-Control-Allow-Origin"] = "*"
        return response


@csrf_exempt
def get_matches(request):
    if request.method == 'POST':
        data = json.loads(request.POST['data'])
        user_id = data['user_id']
        partner = data['partner']
        matches = AppUser.objects.filter(sex=partner).filter(~Q(user_Id=user_id)).all()
        tdcards = []
        for match in matches:
            tdcard = {}
            tdcard['imageUrl'] = match.photo.url
            tdcard['name'] = match.firstname+" "+match.lastname
            tdcard['sex'] = match.sex
            tdcard['age'] = match.age
            print tdcard['name']
            tdcards.append(tdcard)

        response =  HttpResponse(json.dumps({
            'status': 'success',
            'data': tdcards
            }))
        response["Access-Control-Allow-Origin"] = "*"
        return response

@csrf_exempt
def likes(request):
    if request.method == 'POST':
        data = json.loads(request.POST['data'])
        isMatch = is_match_existing(data['user_Id'], data['likes'])

        update_likes(data['user_Id'], data['likes'], isMatch)

        response_data = {}
        if isMatch:
            response_data['match'] = 'True'
            response_data['userId'] = data['user_Id']
            response_data['likes'] = data['likes']
        else:
            response_data['match'] = 'False'

        response = HttpResponse(json.dumps(response))
        response["Access-Control-Allow-Origin"] = "*"
        return response

