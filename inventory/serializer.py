from rest_framework import serializers
from .models import Box,CustomUser
from rest_framework.authtoken.models import Token

class BoxCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Box
        fields = ['length','breadth','height','creator']
    
    def create(self,validated_data):
        area = validated_data['length']*validated_data['breadth']
        volume = validated_data['length']*validated_data['breadth']*validated_data['height']
        creator = CustomUser.objects.get(username=validated_data.pop('creator'))
        boxes = Box(length=validated_data['length'],breadth=validated_data['breadth'],height=validated_data['height'],area=area,volume=volume,created_by=creator.username)
        boxes.creator = creator
        boxes.save()
        return boxes
    
class BoxReadSerializer(serializers.ModelSerializer):

    created_by = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Box
        fields = ['length','breadth','height','created_by','area','volume','updated_at']
    
    def get_created_by(self, obj):
        user =  self.context['request'].user
        if user.is_user_staff:
            return obj.created_by
        return None

    def get_updated_at(self, obj):
        user =  self.context['request'].user
        if user.is_user_staff:
            return obj.updated_at

        return None

class BoxUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Box
        fields = ['length','breadth','height']

    def update(self,instance,validated_data):
        area = validated_data['length']*validated_data['breadth']
        volume = validated_data['length']*validated_data['breadth']*validated_data['height']
        # box = Box.objects.get(id=validated_data['id'])
        instance.length = validated_data['length']
        instance.breadth = validated_data['breadth']
        instance.height = validated_data['height']
        instance.area = area
        instance.volume = volume
        instance.save()
        return instance
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['username','password','is_user_staff']
    
    def create(self, validated_data):
        user = CustomUser.objects.create(username=validated_data['username'])
        user.is_user_staff = validated_data['is_user_staff']
        user.set_password(validated_data['password'])
        user.save()
        return user
        
