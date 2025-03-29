from django.db import models

from django.db import models
from users.models import CustomUser  # CustomUser'ı doğrudan import edin

class UserPDF(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # users.CustomUser'a bağlı
    pdf_file = models.FileField(upload_to='user_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.pdf_file.name}"

