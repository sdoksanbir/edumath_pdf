from django import forms
from users.models import CustomUser, Grade


class StudentForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'tc_no', 'phone_number', 'grade']
        labels = {
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'email': 'E-Posta',
            'tc_no': 'TC Kimlik No',
            'phone_number': 'Telefon Numarası',
            'grade': 'Sınıf',
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            if field_name == "grade":
                self.fields[field_name].widget.attrs.update({'class': 'select2 form-control'})
            if field_name == "phone_number":
                self.fields[field_name].widget.attrs.update({'class': 'phone-inputmask form-control'})


        # Zorunlu alanlar
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['tc_no'].required = True
        self.fields['phone_number'].required = True
        self.fields['grade'].required = True

        if 'password1' in self.fields:
            del self.fields['password1']
        if 'password2' in self.fields:
            del self.fields['password2']

    grade = forms.ModelChoiceField(
        queryset= Grade.objects.all(),  # Veritabanındaki tüm branşları getir
        empty_label="Sınıf Seçin",  # Varsayılan olarak gösterilecek metin
        label='Sınıf',
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    def format_name(self, name):
        name = name.strip()  # Baştaki ve sondaki boşlukları temizle
        name = name.lower()  # Küçük harfe çevir
        words = name.split()  # İsmi kelimelere ayır
        formatted_words = []

        for word in words:
            # Eğer kelimenin ilk harfi 'i' ise, 'İ' yap
            if word[0] == 'i':
                word = 'İ' + word[1:]
            formatted_words.append(word[:1].upper() + word[1:])  # Her kelimenin ilk harfini büyüt
        return " ".join(formatted_words)  # Tekrar birleştir ve döndür

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        return self.format_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        return self.format_name(last_name)

    def clean_tc_no(self):
        tc_no = self.cleaned_data.get('tc_no')
        if not tc_no.isdigit() or len(tc_no) != 11:
            raise forms.ValidationError("TC Kimlik Numarası 11 haneli ve yalnızca rakamlardan oluşmalıdır.")
        if CustomUser.objects.filter(tc_no=tc_no).exists():
            raise forms.ValidationError("Bu TC Kimlik Numarası zaten kayıtlı.")
        return tc_no

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 14:
            raise forms.ValidationError("Telefon numarasını hatalı girdiniz")
        return phone_number


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'tc_no', 'phone_number', 'grade']
        labels = {
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'email': 'E-Posta',
            'tc_no': 'TC Kimlik No',
            'phone_number': 'Telefon Numarası',
            'grade': 'Sınıf',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            if field_name == "grade":
                self.fields[field_name].widget.attrs.update({'class': 'select2 form-control'})
            if field_name == "phone_number":
                self.fields[field_name].widget.attrs.update({'class': 'phone-inputmask form-control'})

        # Zorunlu alanlar
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['grade'].required = True

        # Şifre alanlarını kaldır
        if 'password1' in self.fields:
            del self.fields['password1']
        if 'password2' in self.fields:
            del self.fields['password2']

    grade = forms.ModelChoiceField(
        queryset = Grade.objects.all(),  # Veritabanındaki tüm branşları getir
        empty_label = "Sınıf Seçin",  # Varsayılan olarak gösterilecek metin
        label='Sınıf'
    )

    def format_name(self, name):
        name = name.strip()  # Baştaki ve sondaki boşlukları temizle
        name = name.casefold()  # Unicode uyumlu küçük harfe çevir
        words = name.split()  # İsmi kelimelere ayır
        formatted_words = [word[:1].upper() + word[1:] for word in words]  # Her kelimenin ilk harfini büyüt
        return " ".join(formatted_words)  # Tekrar birleştir ve döndür

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        return self.format_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        return self.format_name(last_name)

    def clean_tc_no(self):
        tc_no = self.cleaned_data.get('tc_no')
        if not tc_no.isdigit() or len(tc_no) != 11:
            raise forms.ValidationError("TC Kimlik Numarası 11 haneli ve yalnızca rakamlardan oluşmalıdır.")
        return tc_no

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 14:
            raise forms.ValidationError("Telefon numarasını hatalı girdiniz")
        return phone_number