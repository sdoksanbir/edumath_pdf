from django import forms

from users.models import Subject, Grade


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        labels = {
            'name': 'Branş',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.fields['name'].required = True

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

    def clean_name(self):
        name = self.cleaned_data.get("name").strip()

        # Boş olup olmadığını kontrol et
        if not name:
            raise forms.ValidationError("Branş adı boş bırakılamaz!")

        # Aynı isimde bir branş var mı?
        if Subject.objects.filter(name=name):
            raise forms.ValidationError("Bu branş zaten kayıtlı.")

        return self.format_name(name)




class SubjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        labels = {
            'name': 'Branş',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.fields['name'].required = True

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

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError("Branş alanı boş bırakılamaz!")
        # Güncelleme sırasında kendisini hariç tut
        if Subject.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Bu branş zaten kayıtlı.")

        return self.format_name(name)


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name','category']
        labels = {
            'name': 'Eğitim Düzeyi',
            'category': 'Alanı',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'select2 form-control'}),
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            if field_name == "category":
                self.fields[field_name].widget.attrs.update({'class': 'select2 form-control'})

        self.fields['name'].required = True
        self.fields['category'].required = False




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

    def clean_name(self):
        name = self.cleaned_data.get('name','').strip()
        if not name:
            raise forms.ValidationError("Branş alanı boş bırakılamaz!")
        name = self.format_name(name)
        # Güncelleme sırasında kendisini hariç tut
        if Grade.objects.filter(name=name):
            raise forms.ValidationError('Bu eğitim düzeyi zaten kayıtlı')

        return self.format_name(name)


class GradeUpdateForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name','category']
        labels = {
            'name': 'Eğitim Düzeyi',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            if field_name == "category":
                self.fields[field_name].widget.attrs.update({'class': 'select2 form-control'})
        self.fields['name'].required = True

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

    def clean_name(self):
        name = self.cleaned_data.get('name','').strip()
        if not name:
            raise forms.ValidationError("Branş alanı boş bırakılamaz!")

        # Güncelleme sırasında kendisini hariç tut
        if Grade.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Bu branş zaten kayıtlı.")

        return self.format_name(name)
