from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Model, CharField, ForeignKey, IntegerField, DateField, TextField, ImageField, OneToOneField

from stepik_vacancies.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(Model):
    name = CharField(max_length=256)
    location = CharField(max_length=128)
    logo = ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, null=True)
    description = CharField(max_length=2048)
    employee_count = IntegerField()
    owner = OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='company')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Specialty(Model):

    def __str__(self):
        return self.title

    code = CharField(max_length=128)
    title = CharField(max_length=256)
    picture = ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, null=True)

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Vacancy(Model):
    title = CharField(max_length=256)
    specialty = ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = CharField(max_length=2048)
    description = CharField(max_length=2048)
    salary_min = IntegerField()
    salary_max = IntegerField()
    published_at = DateField()

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Application(Model):
    written_username = CharField(max_length=256)
    written_phone = CharField(max_length=15)
    written_cover_letter = TextField(max_length=2048)
    vacancy = ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='applications')

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


class Resume(models.Model):

    class GradeChoices(models.TextChoices):
        INTERN = 'IN', 'Интерн'
        JUNIOR = 'JN', 'Джуниор'
        MIDDLE = 'MD', 'Мидл'
        SENIOR = 'SN', 'Синьор'
        LEAD = 'LD', 'Лид'

    class StatusChoices(models.TextChoices):
        YES = 'YS', 'Ищу работу'
        NO = 'NO', 'Не ищу работу'
        MAYBE = 'MB', 'Рассматриваю предложения'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    status = models.CharField(max_length=32)
    salary = models.IntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='resume')
    grade = models.CharField(max_length=8)
    education = models.TextField(max_length=1024)
    experience = models.TextField(max_length=2048, null=True)
    portfolio = models.CharField(max_length=256, null=True)

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
