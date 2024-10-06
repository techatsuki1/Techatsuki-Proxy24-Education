from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path("register/", views.register, name="register"),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/',views.profile,name="profile"),
    path('profile-photo/',views.profilephoto,name="profilephoto"),
    path('accountsecurity/',views.accountsecurity,name="accountsecurity"),
    path('close-account/',views.closeaccount,name="closeaccount"),
    path('editnotification/',views.editnotification,name="editnotification"),
    path('privacy/',views.privacy,name="privacy"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('tutors/',views.tutor_list, name='tutor_list'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)