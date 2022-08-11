from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework import status
from .models import Person
from core.serializers1 import PeopleSerializers,RegisterSerializer,LoginSerializer
from rest_framework import viewsets

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action


#Authenticate and permission API
class RegisterAPI(APIView):
    
    def post(self,request):
        data = request.data
        serializers =RegisterSerializer(data=data)
        
        if not serializers.is_valid():
            return Response({
                'status':False,
                'message':serializers.errors
                },status.HTTP_400_BAD_REQUEST)
        serializers.save()
        return Response({
            'ststus':True,
            'message':"User Created"
            },status.HTTP_201_CREATED)
        
        
        
        
class LoginAPI(APIView):
    def post(self,request):
        data = request.data
        serializers=LoginSerializer(data=data)
        
        if not serializers.is_valid():
            return Response({
                'status':False,
                'message':serializers.errors
                },status.HTTP_400_BAD_REQUEST)
            
        user = authenticate(username=serializers.data['username'],password=serializers.data['password'])
        if not user:
            return Response({
                'status':False,
                'message':'Invalid credentials'
                },status.HTTP_400_BAD_REQUEST)
            
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'ststus':True,
            'message':"User login",
            'token':str(token)
            },status.HTTP_201_CREATED) 
                
       


# Viewset based API
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializers
    queryset = Person.objects.all()
    # http_method_names=['get','post','put','patch','delete']
    
    # add search function
    def list(self ,request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
            
            
        serializer = PeopleSerializers(queryset,many=True)
        return Response({'status':200 ,'data':serializer.data},status=status.HTTP_204_NO_CONTENT)
    
    # @action(detail=False, methods=['post'])
    @action(detail=True, methods=['post'])
    # def send_mail_to_person(self, request):
    def send_mail_to_person(self, request,pk):
        obj=Person.objects.get(pk=pk)
        serializer = PeopleSerializers(obj)
        print(pk)
        return Response({
            'status':True, 
            'message':'email send successfully',
            'data':serializer.data
            })
  
    

#class Based view
class PersonAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            print(request.user)
            obj= Person.objects.all() 
            # obj= Person.objects.filter(color__isnull=False) 
            page=request.GET.get('page',1)
            pag_size=3
            
            paginator = Paginator(obj,pag_size)
            
            print(paginator.page(page))
            serializer=PeopleSerializers(paginator.page(page),many=True)  # data is more then one we pass many
            return Response(serializer.data)
        except Exception as e:
            return Response({
                    'status':False,
                    'message':'Invalid Page'
                    })
    
       

    def post(self,request):
        data=request.data
        serializer = PeopleSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

    def put(self,request):
        data=request.data
        obj= Person.objects.get(id=data['id'])
        serializer = PeopleSerializers(obj,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
    def patch(self,request):
        data=request.data
        obj= Person.objects.get(id=data['id'])
        serializer = PeopleSerializers(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    

    def delete(self,request):
        data=request.data
        obj= Person.objects.get(id=data['id'])
        obj.delete()
        return Response ({'message':'person deleted'})

# function Based View
@api_view(['GET','POST','PUT'])
def index(request):
    cources = {
        'course_name':'python',
        'learn':['flask','django','Fastapi'],
        'Course_provider':'Scaller'
        }
    
    if request.method == 'GET':
        print(request.GET.get('search'))
        
        print("You hit a get method")
        return Response (cources)
    elif request.method == 'POST':
        data= request.data
        print("You hit a POST method")
        print(data)
        return Response (cources)
    elif request.method == 'PUT':
        print("You hit a PUT method")
        return Response (cources)
    
    
@api_view(['GET','POST','PUT','PATCH','DELETE'])   
def people(request):
    if request.method=="GET":
        obj= Person.objects.filter(color__isnull=False) 
        serializer=PeopleSerializers(obj,many=True)  # data is more then one we pass many
        return Response(serializer.data)
    
    elif request.method=="POST":
        data=request.data
        serializer = PeopleSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method=='PUT': # Not support partial update data
        data=request.data
        obj= Person.objects.get(id=data['id'])
        serializer = PeopleSerializers(obj,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
        
    elif request.method=='PATCH':  # update support partial data
        data=request.data
        obj= Person.objects.get(id=data['id'])
        serializer = PeopleSerializers(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    else:
        data=request.data
        obj= Person.objects.get(id=data['id'])
        obj.delete()
        return Response ({'message':'person deleted'})
        
        
        
    
