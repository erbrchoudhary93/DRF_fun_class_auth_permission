
from core.views import PersonAPI, index,people, PeopleViewSet,RegisterAPI,LoginAPI
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls

urlpatterns = [
    path('',include(router.urls)),
    path('index/', index),
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('person/', people),
    path('persons/', PersonAPI.as_view()),
    
]
