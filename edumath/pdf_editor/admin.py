from django.contrib import admin
from .models import UserPDF

@admin.register(UserPDF)
class UserPDFAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'uploaded_at')
    list_filter = ('user',)