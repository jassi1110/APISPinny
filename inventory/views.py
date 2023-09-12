from django.shortcuts import render
from django.db.models import Avg,Count,Sum
from .models import Box,CustomUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .services import queryString
from datetime import date, timedelta
from .serializer import BoxCreateSerializer,BoxReadSerializer,BoxUpdateSerializer,UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.
A1 = 100
V1 = 1000
L1 = 100
L2 = 50

@api_view(['POST'])
def userAuthorization(request):

    try:
        user = CustomUser.objects.get(username=request.data['username'])
        tokenObj,user = Token.objects.get_or_create(user=user)
        return Response({"success":True,"Authtoken":str(tokenObj)},status=200)
    except CustomUser.DoesNotExist:
        serializer = UserSerializer(data=request.data)
        if  not serializer.is_valid():
            return Response({"success":False,"Error":serializer.errors})
        serializer.save()
        user = CustomUser.objects.get(username=serializer.data['username'])
        tokenObj,user = Token.objects.get_or_create(user=user)
        return Response({"success":True,"Authtoken":str(tokenObj)},status=200)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createBox(request):
    try:
        user = request.user
        if user.is_user_staff:
            avgs = Box.objects.aggregate(Avg('area'),Avg('volume'))
            avgsArea = 0 if avgs['area__avg']==None else avgs['area__avg']
            avgsVolume = 0 if avgs['volume__avg']==None else avgs['volume__avg']
            newArea = request.data['length']*request.data['breadth']/2
            newVolume = request.data['length']*request.data['breadth']*request.data['height']/2
            today = date.today()
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            weekBoxes = Box.objects.filter(created_at__gte=start,created_at__lte=end).values('creator_id').annotate(count_value=Count('creator'))
            staffWeekBoxesQuery = weekBoxes.filter(creator_id=request.user.id)
            staffWeekBoxes = 0 if not staffWeekBoxesQuery else staffWeekBoxesQuery[0]['count_value']
            totalWeekBoxes = 0 if not weekBoxes else weekBoxes.aggregate(total_count = Sum('count_value'))['total_count']
            
            if newArea + avgsArea > A1 or newVolume + avgsVolume > V1 or totalWeekBoxes + 1 > L1 or staffWeekBoxes + 1 > L2:
                return Response({"success":False,"message":"Storage Full"},status=200)
            
            request.data['creator'] = user.id
            serializer = BoxCreateSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer)
                serializer.save()
            return Response({"success":True,"data":serializer.data},status=200)
        else:
            return Response({"success":False,"message":"You are not eligible to enter inventory"},status=200)
    except Exception as e:
        error_message = "Object not found."
        return Response({"error": str(e) or error_message}, status=500)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listBoxes(request):
    query_params_dict = request.GET.dict()

    boxes = Box.objects.filter(queryString(query_params_dict))
    serializer = BoxReadSerializer(boxes,context={'request': request},many=True)
    res = [ele for ele in ({key: val for key, val in sub.items() if val}
                       for sub in serializer.data) if ele]
    return Response({"data":res},status=200)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listMyBoxes(request):
    # user = CustomUser.objects.get(id=1)
    query_params_dict = request.GET.dict()

    boxes = request.user.box_set.filter(queryString(query_params_dict))
    serializer = BoxReadSerializer(boxes,context={'request': request},many=True)
    res = [ele for ele in ({key: val for key, val in sub.items() if val}
                       for sub in serializer.data) if ele]
    return Response({"data":res},status=200)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateBox(request):
    try:
        user = request.user
        boxInstance = Box.objects.filter(id = request.data['id'])[0]
        if user.is_user_staff and boxInstance:
            avgs = Box.objects.exclude(id = request.data['id']).aggregate(Avg('area'),Avg('volume'))
            avgsArea = 0 if avgs['area__avg']==None else avgs['area__avg']
            avgsVolume = 0 if avgs['volume__avg']==None else avgs['volume__avg']
            newArea = request.data['length']*request.data['breadth']/2
            newVolume = request.data['length']*request.data['breadth']*request.data['height']/2
            
            if newArea + avgsArea > A1 or newVolume + avgsVolume > V1:
                return Response({"success":False,"message":"Storage Full"},status=200)
            
            serializer = BoxUpdateSerializer(boxInstance,data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response({"success":True,"message":"Data Updated Successfully","data":serializer.data},status=200)
        else:
            return Response({"success":False,"message":"You are not eligible to update inventory"},status=200)
    except Exception as e:
        error_message = "Object not found."
        return Response({"error": str(e) or error_message}, status=500)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteBox(request):
    try:
        user = request.user
        if user.is_user_staff:
            box = Box.objects.get(id=request.data['id'])
            if box.creator.id == user.id:
                box.delete()
                return Response({"success":True,"message":"Box deleted Successfully"},status=200)
            else:
                return Response({"success":False,"message":"You are not eligible to delete box"},status=404)
    except Exception as e:
        error_message = "Error raised"
        return Response({"error": str(e) or error_message}, status=500)