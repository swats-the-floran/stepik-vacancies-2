import os
import django
from datetime import date

os.environ["DJANGO_SETTINGS_MODULE"] = 'stepik_vacancies.settings'
django.setup()

from vacancies.models import Vacancy, Company, Specialty
from vacancies.data import vacancies, companies, specialties


def populate():
    for company_ in companies:
        Company.objects.create(**company_)

    for specialty_ in specialties:
        Specialty.objects.create(**specialty_)

    for vacancy_ in vacancies:
        vacancy_['specialty'] = Specialty.objects.get(code=vacancy_['specialty'])
        vacancy_['company'] = Company.objects.get(name=vacancy_['company'])
        vacancy_['published_at'] = date(*[int(i) for i in vacancy_['published_at'].split('-')])
        Vacancy.objects.create(**vacancy_)


if __name__ == '__main__':
    populate()
