
from rest_framework import serializers
from .models import  Person , Color
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username= serializers.CharField()
    email = serializers.EmailField()
    password= serializers.CharField()

    def validate(self,data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('Username is already exist')
    
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('Email is already exist')
        return data
    def create(self,validatd_data):
        user = User.objects.create(username=validatd_data['username'],email=validatd_data['email'])
        user.set_password(validatd_data['password'])
        print(validatd_data)
        user.save()
        return validatd_data
        
    
class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password= serializers.CharField()
    


class ColorSerializers(serializers.ModelSerializer):
    class Meta:
        
        model = Color
        fields = '__all__'
        # fields = ['color_name']

class PeopleSerializers(serializers.ModelSerializer):
    # color = ColorSerializers()
    # country = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        # fields = ['name','age','id']
        fields = '__all__'
        # depth=1
        # fields = ['name']
        
    # def get_country(self,obj):
    #     color_obj = Color.objects.get(id=obj.color.id)
    #     return { 'color_nam':color_obj.color_name,'hex_code':'#000'}
        
    # # data validation
    def validate(self, data):
        
        special_charactor = "+-*/!@#$%^&?:;<>="
        if any (c in special_charactor for c in data['name']):
            raise serializers.ValidationError("Name can not contain special charactor")
        if data.get('age') and data['age'] < 18 :
            raise serializers.ValidationError("age Should be grater then 18")
        else:
            return data
        
        
        
    