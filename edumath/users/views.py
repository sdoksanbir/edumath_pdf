import random
import string
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login

from .forms.parameters_form import SubjectForm, SubjectUpdateForm, GradeForm, GradeUpdateForm
from .forms.student_form import StudentForm, StudentUpdateForm
from .forms.teacher_form import TeacherForm, TeacherUpdateForm
from .forms.manager_form import ManagerForm, ManagerUpdateForm
from django.utils.text import slugify
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Grade, Subject


def generate_random_password(length=8):
    """ Rastgele şifre oluşturur (Harf + Rakam kombinasyonu) """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_unique_username(tc_no):
    base_username = slugify(tc_no)  # TC'yi güvenli hale getir
    username = base_username
    counter = 1

    while CustomUser.objects.filter(username=username).exists():
        username = f"{base_username}_{counter}"  # Eğer aynı kullanıcı adı varsa sayıyla değiştir
        counter += 1

    return username


def home(request):
    students = CustomUser.objects.filter(user_type='student')
    teachers = CustomUser.objects.filter(user_type='teacher')
    ctx = {'students': students, 'teachers': teachers}
    return render(request, 'backend/panel.html',ctx)


def teacher_list(request):
    teachers = CustomUser.objects.filter(user_type='teacher')
    return render(request, 'backend/users/teacher_list.html', {'teachers': teachers})


def student_list(request):
    grades = Grade.objects.all()
    students = CustomUser.objects.filter(user_type='student')
    return render(request, 'backend/users/student_list.html', {'students': students, 'grades': grades})


def manager_list(request):
    managers = CustomUser.objects.filter(user_type='manager')
    return render(request, 'backend/users/manager_list.html', {'managers': managers})


def register_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.user_type = "teacher"  # Kullanıcı türünü öğretmen olarak ayarla
            teacher.username = generate_unique_username(teacher.tc_no)  # Kullanıcı adını otomatik ata
            random_password = generate_random_password()  # Rastgele şifre oluştur
            teacher.set_password(random_password)  # Şifreyi hashle
            teacher.save()
            messages.success(request, "Öğretmen kaydı başarıyla oluşturuldu.")
            return redirect("register_teacher")  # Kayıt sonrası yönlendirme
        else:
            messages.error(request, "LÜTFEN FORMDAKİ HATALARI DÜZELTİN.", extra_tags='danger')
    else:
        form = TeacherForm()

    return render(request, "backend/users/register_teacher.html", {"form": form})


def update_teacher(request, pk):
    teacher = get_object_or_404(CustomUser, pk=pk, user_type="teacher")
    if request.method == "POST":
        form = TeacherUpdateForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Öğretmen bilgileri başarıyla güncellendi.")
            return redirect("teacher_list")  # Öğretmen listesi sayfasına yönlendirme
        else:
            messages.error(request, "LÜTFEN FORMDAKİ HATALARI DÜZELTİN.", extra_tags="danger")
    else:
        form = TeacherUpdateForm(instance=teacher)

    return render(request, "backend/users/teacher_update.html", {"form": form, "teacher": teacher})


@csrf_exempt
def delete_teacher(request, teacher_id):
    try:
        teacher = CustomUser.objects.get(id=teacher_id, user_type='teacher')
        teacher.delete()
        return JsonResponse({'status': 'success', 'message': 'Öğretmen başarıyla silindi.'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Öğretmen bulunamadı.'}, status=404)


@csrf_exempt
def update_teacher_status(request, teacher_id):
    if request.method == 'POST':
        try:
            teacher = CustomUser.objects.get(id=teacher_id, user_type='teacher')
            data = json.loads(request.body)  # JSON verisini alıyoruz
            status = data.get('status')

            if status == 'active':
                teacher.is_active = True
            elif status == 'inactive':
                teacher.is_active = False
            else:
                return JsonResponse({'status': 'error', 'message': 'Geçersiz durum.'}, status=400)

            teacher.save()  # Değişikliği kaydediyoruz
            return JsonResponse({'status': 'success', 'message': 'Öğretmen durumu başarıyla güncellendi.'})

        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Öğretmen bulunamadı.'}, status=404)


def register_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user_type = "student"  # Kullanıcı türünü öğretmen olarak ayarla
            student.username = generate_unique_username(student.tc_no)  # Kullanıcı adını otomatik ata
            random_password = generate_random_password()  # Rastgele şifre oluştur
            student.set_password(random_password)  # Şifreyi hashle
            student.save()
            messages.success(request, "Öğrenci kaydı başarıyla oluşturuldu.")
            return redirect("register_student")  # Kayıt sonrası yönlendirme
        else:
            messages.error(request, "LÜTFEN FORMDAKİ HATALARI DÜZELTİN.", extra_tags='danger')
    else:
        form = StudentForm()

    return render(request, "backend/users/register_student.html", {"form": form})


def update_student(request, pk):
    student = get_object_or_404(CustomUser, pk=pk, user_type="student")
    if request.method == "POST":
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Öğrenci bilgileri başarıyla güncellendi.")
            return redirect("student_list")  # Öğrenci listesi sayfasına yönlendirme
        else:
            messages.error(request, "LÜTFEN FORMDAKİ HATALARI DÜZELTİN.", extra_tags="danger")
    else:
        form = StudentUpdateForm(instance=student)

    return render(request, "backend/users/student_update.html", {"form": form, "student": student})


@csrf_exempt
def delete_student(request, student_id):
    try:
        student = CustomUser.objects.get(id=student_id, user_type='student')
        student.delete()
        return JsonResponse({'status': 'success', 'message': 'Öğrenci başarıyla silindi.'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Öğrenci bulunamadı.'}, status=404)


@csrf_exempt
def update_student_status(request, student_id):
    if request.method == 'POST':
        try:
            student = CustomUser.objects.get(id=student_id, user_type='student')
            data = json.loads(request.body)  # JSON verisini alıyoruz
            status = data.get('status')

            if status == 'active':
                student.is_active = True
            elif status == 'inactive':
                student.is_active = False
            else:
                return JsonResponse({'status': 'error', 'message': 'Geçersiz durum.'}, status=400)

            student.save()  # Değişikliği kaydediyoruz
            return JsonResponse({'status': 'success', 'message': 'Öğrenci durumu başarıyla güncellendi.'})

        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Öğrenci bulunamadı.'}, status=404)


def register_manager(request):
    if request.method == "POST":
        form = ManagerForm(request.POST)
        if form.is_valid():
            manager = form.save(commit=False)
            manager.user_type = "manager"  # Kullanıcı türünü yönetici olarak ayarla
            manager.is_superuser = True
            manager.username = generate_unique_username(manager.tc_no)  # Kullanıcı adını otomatik ata
            random_password = generate_random_password()  # Rastgele şifre oluştur
            manager.set_password(random_password)  # Şifreyi hashle
            manager.save()
            messages.success(request, "Yönetici kaydı başarıyla oluşturuldu.")
            return redirect("register_manager")  # Kayıt sonrası yönlendirme
        else:
            messages.error(request, "LÜTFEN FORMDAKİ HATALARI DÜZELTİN.", extra_tags='danger')
    else:
        form = StudentForm()

    return render(request, "backend/users/register_manager.html", {"form": form})


def update_manager(request, pk):
    manager = get_object_or_404(CustomUser, pk=pk, user_type="manager")
    if request.method == "POST":
        form = ManagerUpdateForm(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            messages.success(request, "Yönetici bilgileri başarıyla güncellendi.")
            return redirect("manager_list")  # Yönetici listesi sayfasına yönlendirme
        else:
            messages.error(request, "LÜTFEN FORMDAKİ HATALARI DÜZELTİN.", extra_tags="danger")
    else:
        form = ManagerUpdateForm(instance=manager)

    return render(request, "backend/users/manager_update.html", {"form": form, "manager": manager})


@csrf_exempt
def delete_manager(request, manager_id):
    try:
        manager = CustomUser.objects.get(id=manager_id, user_type='manager')
        manager.delete()
        return JsonResponse({'status': 'success', 'message': 'Yönetici başarıyla silindi.'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Yönetici bulunamadı.'}, status=404)


@csrf_exempt
def update_manager_status(request, manager_id):
    if request.method == 'POST':
        try:
            manager = CustomUser.objects.get(id=manager_id, user_type='manager')
            data = json.loads(request.body)  # JSON verisini alıyoruz
            status = data.get('status')

            if status == 'active':
                manager.is_active = True
            elif status == 'inactive':
                manager.is_active = False
            else:
                return JsonResponse({'status': 'error', 'message': 'Geçersiz durum.'}, status=400)

            manager.save()  # Değişikliği kaydediyoruz
            return JsonResponse({'status': 'success', 'message': 'Yönetici durumu başarıyla güncellendi.'})

        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Yönetici bulunamadı.'}, status=404)


def parameters(request):
    subjectForm = SubjectForm()
    subjects = Subject.objects.all()
    gradeForm = GradeForm()
    grades = Grade.objects.all()
    return render(request, 'backend/parameters/parameters.html',
                  {'subjectForm': subjectForm, 'subjects': subjects, 'gradeForm': gradeForm, 'grades': grades})



def subject_save(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.save()
            messages.success(request, "Branş bilgisi başarıyla kaydedildi.")
            return redirect("subject_save")  # Başarılı kayıt sonrası sayfa yenileme
        else:
            messages.error(request, "LÜTFEN AŞAĞIDAKİ HATALARI DÜZELTİNİZ.", extra_tags="danger")
            subjectForm = form  # Hatalı formu tekrar gönderiyoruz
    else:
        subjectForm = SubjectForm()  # GET isteğinde formu sıfırdan oluştur

    subjects = Subject.objects.all()
    gradeForm = GradeForm()
    grades = Grade.objects.all()

    return render(request, "backend/parameters/parameters.html", {
        "subjectForm": subjectForm,
        "subjects": subjects,
        "gradeForm": gradeForm,
        "grades": grades
    })


def subject_update(request, subject_pk):
    subject = get_object_or_404(Subject, id=subject_pk)
    if request.method == "POST":
        form = SubjectUpdateForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Branş bilgisi başarıyla güncellendi.')
            return redirect("parameters")
        else:
            messages.error(request, "LÜTFEN AŞAĞIDAKİ HATALARI DÜZELTİNİZ.", extra_tags='danger')
            subjectForm = form
            subjects = Subject.objects.all()
            return render(request, 'backend/parameters/parameters.html',
                          {'subjectForm': subjectForm, 'subjects': subjects})
    subjectForm = SubjectUpdateForm(instance=subject)
    subjects = Subject.objects.all()
    grades = Grade.objects.all()
    gradeForm = GradeForm()
    subject_update_id =subject_pk
    return render(request, 'backend/parameters/subject_update.html',
                  {'subjectForm': subjectForm, 'subject': subject, 'subjects': subjects, 'gradeForm': gradeForm,
                   'grades': grades, 'subject_update_id': subject_update_id})



def subject_delete(request, subject_pk):
    if request.method == "POST":
        try:
            # request.body'den JSON verisini alıyoruz
            data = json.loads(request.body)

            # JSON verisinden item_update_id'yi alıyoruz
            item_update_id = data.get("item_update_id")
            if item_update_id is None:
                return JsonResponse({"message": "item_update_id parametresi eksik."}, status=400)

            # Grade modelinden öğe alıyoruz
            subject = get_object_or_404(Subject, pk=subject_pk)
            print(item_update_id)
            print(subject.id)
            # Eğer item_update_id ile grade.id eşleşiyorsa, silme işlemi engellenir
            if item_update_id and subject.id == int(item_update_id):  # item_update_id'yi tam sayı olarak karşılaştır
                return JsonResponse({'message': 'Bu öğe düzenleniyor, silinemez.'}, status=400)

            # Grade öğesini siliyoruz
            subject.delete()

            return JsonResponse({"success": True, "message": "Branş başarıyla silindi!"})

        except json.JSONDecodeError:
            return JsonResponse({"message": "Geçersiz JSON verisi."}, status=400)

    return JsonResponse({"success": False, "message": "Geçersiz istek!"}, status=400)


def grade_save(request):
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.save()
            messages.success(request, "Eğitim düzeyi bilgisi başarıyla kaydedildi.")
            return redirect("grade_save")  # Başarılı kayıt sonrası sayfa yenileme
        else:
            messages.error(request, "LÜTFEN AŞAĞIDAKİ HATALARI DÜZELTİNİZ.", extra_tags="danger")
            gradeForm = form  # Hatalı formu tekrar gönderiyoruz
    else:
        gradeForm = GradeForm()  # GET isteğinde formu sıfırdan oluştur

    subjects = Subject.objects.all()
    subjectForm = SubjectForm()
    grades = Grade.objects.all()

    return render(request, "backend/parameters/parameters.html", {
        "subjectForm": subjectForm,
        "subjects": subjects,
        "gradeForm": gradeForm,
        "grades": grades
    })

def grade_update(request, grade_pk):
    grade = get_object_or_404(Grade, id=grade_pk)
    if request.method == "POST":
        form = GradeUpdateForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Branş bilgisi başarıyla güncellendi.')
            return redirect("parameters")  # Başarıyla güncellendikten sonra yönlendirme
        else:
            messages.error(request, "LÜTFEN AŞAĞIDAKİ HATALARI DÜZELTİNİZ.", extra_tags='danger')
            # Hatalı formu yeniden gönder
            gradeForm = form
            grades = Grade.objects.all()
            subjectForm = SubjectForm()
            subjects = Subject.objects.all()
            return render(request, 'backend/parameters/parameters.html', {
                'gradeForm': gradeForm,  # Hatayı içeren formu gönderiyoruz
                'grades': grades,
                'subjectForm': subjectForm,
                'subjects': subjects
            })
    else:
        gradeForm = GradeUpdateForm(instance=grade)  # GET isteği durumunda formu doldur

    # **Tüm verilere ihtiyacın olduğu için hepsini şablona gönderiyoruz**
    subjectForm = SubjectForm()
    subjects = Subject.objects.all()
    grades = Grade.objects.all()
    return render(request, 'backend/parameters/grade_update.html', {
        'subjectForm': subjectForm,
        'subjects': subjects,
        'gradeForm': gradeForm,
        'grades': grades,
        'grade': grade,
        'grade_update_id': grade_pk  # grade_pk'yi şablona gönderiyoruz
    })


def grade_delete(request, grade_pk):
    if request.method == "POST":
        try:
            # request.body'den JSON verisini alıyoruz
            data = json.loads(request.body)

            # JSON verisinden item_update_id'yi alıyoruz
            item_update_id = data.get("item_update_id")
            if item_update_id is None:
                return JsonResponse({"message": "item_update_id parametresi eksik."}, status=400)

            # Grade modelinden öğe alıyoruz
            grade = get_object_or_404(Grade, pk=grade_pk)

            # Eğer item_update_id ile grade.id eşleşiyorsa, silme işlemi engellenir
            if item_update_id and grade.id == int(item_update_id):  # item_update_id'yi tam sayı olarak karşılaştır
                return JsonResponse({'message': 'Bu öğe düzenleniyor, silinemez.'}, status=400)

            # Grade öğesini siliyoruz
            grade.delete()

            return JsonResponse({"success": True, "message": "Eğitim düzeyi başarıyla silindi!"})

        except json.JSONDecodeError:
            return JsonResponse({"message": "Geçersiz JSON verisi."}, status=400)

    return JsonResponse({"success": False, "message": "Geçersiz istek!"}, status=400)