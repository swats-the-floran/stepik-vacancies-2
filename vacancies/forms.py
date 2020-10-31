from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea, FileInput, ModelChoiceField
from vacancies.models import Company, Application, Vacancy, Specialty, Resume


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        widgets = {'written_cover_letter': Textarea()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False


class MyCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'location', 'description', 'employee_count', 'logo')
        widgets = {
            'description': Textarea(),
            'logo': FileInput(attrs={
                'class': 'custom-file-input',
                'id': 'inputGroupFile01',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['logo'].required = False


class LogInForm(forms.Form):

    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(label='Пароль', max_length=150, widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False


class RegisterForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False


class ResumeForm(forms.ModelForm):

    status = forms.ChoiceField(choices=Resume.StatusChoices.choices)
    grade = forms.ChoiceField(choices=Resume.GradeChoices.choices)
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all())

    class Meta:
        model = Resume
        fields = ('name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio')
        widgets = {'status': forms.Select(), 'grade': forms.Select(), 'specialty': forms.Select()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False


class VacancyForm(forms.ModelForm):

    specialty = ModelChoiceField(queryset=Specialty.objects.all())

    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max')
        widgets = {'description': Textarea(), 'skills': Textarea(attrs={'rows': 3}), 'specialty': forms.Select()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False


class SearchForm(forms.Form):

    search_string = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control col-md-12",
                'type': "search",
                'placeholder': 'Найти работу или стажировку',
                'aria-label': 'Найти работу или стажировку',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
