# from django.urls import path
# from matcher import views
#
# urlpatterns = [
#     # path("parse-resume/", views.parse_resume, name="parse_resume"),
#     path('parse-resume/', views.parse_resume, name='parse_resume'),
# ]

# urls.py
from django.shortcuts import render
from django.urls import path
from matcher import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('upload-resume/', views.upload_resume, name='upload_resume'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# path('', views.home, name='home'),
#                   path('upload-resume/', views.upload_and_process_resume, name='upload_resume'),