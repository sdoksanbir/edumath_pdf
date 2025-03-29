from django.shortcuts import render, redirect
from .models import UserPDF

# Create your views here.
def upload_pdf(request):
    if request.method == 'POST':
        for file in request.FILES.getlist('pdf_files'):
            UserPDF.objects.create(user=request.user, pdf_file=file)
        return redirect('pdf_list')
    return render(request, 'backend/pdf_editor/upload_pdf.html')


