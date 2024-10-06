from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    

    path('', views.home, name='home'),
    path('auth/',views.auth,name='auth'),
    path('about/',views.about,name="about"),
    path('act/',views.act,name='act'),
    path('scene/',views.scene,name="scene"),
    path('upload/',views.upload,name="upload"),
    path('learning/',views.learning,name="learning"),
    path('detect-scene/', views.detect, name='detect'),
    path('liveemotion/', views.liveemotion, name='liveemotion'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)