from django.contrib import admin
from django.urls import path, include
from pdf_editor import views

urlpatterns = [
path('admin/', admin.site.urls),
]