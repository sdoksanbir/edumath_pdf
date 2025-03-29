from django.contrib import admin
from .models import CustomUser, Subject, Grade


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("tc_no", "first_name", "last_name", "user_type", "grade", "subject", "payment_status")
    search_fields = ("tc_no", "first_name", "last_name", "email", "phone_number")
    list_filter = ("user_type", "grade", "subject", "payment_status")
    ordering = ("first_name", "last_name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "category")
