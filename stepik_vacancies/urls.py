"""stepik_vacancies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from stepik_vacancies import settings
from vacancies.views import AboutProject
from vacancies.views import CompaniesElement
from vacancies.views import CompaniesList
from vacancies.views import LogIn
from vacancies.views import LogOut
from vacancies.views import MainPage
from vacancies.views import MyCompany
from vacancies.views import MyCompanyCreate
from vacancies.views import MyCompanyVacanciesCreate
from vacancies.views import MyCompanyVacanciesElement
from vacancies.views import MyCompanyVacanciesList
from vacancies.views import MyResume
from vacancies.views import MyResumeCreate
from vacancies.views import Register
from vacancies.views import Search
from vacancies.views import SentApplication
from vacancies.views import VacanciesElement
from vacancies.views import VacanciesList
from vacancies.views import VacanciesListBySpecialty

urlpatterns = [
    # main
    path('', MainPage.as_view(), name='main_page'),
    path('about/', AboutProject.as_view(), name='about_page'),
    path('login/', LogIn.as_view(), name='login_page'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register_page'),
    path('search/', Search.as_view(), name='search'),
    # vacancies
    path('vacancies/', VacanciesList.as_view(), name='vacancies_list'),
    path('vacancies/<int:vacancy_id>/', VacanciesElement.as_view(), name='vacancies_element'),
    # path('vacancies/<int:vacancy_id>/edit/', VacanciesElementEdit.as_view(), name='vacancies_element_edit'),
    path('vacancies/<int:vacancy_id>/sent/', SentApplication.as_view(), name='vacancies_sent_application'),
    path('vacancies/cat/<str:specialty_code>/', VacanciesListBySpecialty.as_view(), name='vacancies_list_by_specialty'),
    # companies
    path('companies/', CompaniesList.as_view(), name='companies_list'),
    path('companies/<int:company_id>/', CompaniesElement.as_view(), name='companies_element'),
    # mycompany
    path('mycompany/', MyCompany.as_view(), name='my_company'),
    path('mycompany/create/', MyCompanyCreate.as_view(), name='my_company_create'),
    path('mycompany/vacancies/', MyCompanyVacanciesList.as_view(), name='my_company_vacancies_list'),
    path('mycompany/vacancies/create', MyCompanyVacanciesCreate.as_view(), name='my_company_vacancies_create'),
    path('mycompany/vacancies/<int:vacancy_id>/', MyCompanyVacanciesElement.as_view(),
         name='my_company_vacancies_element'),
    # myresume
    path('myresume/', MyResume.as_view(), name='my_resume'),
    path('myresume/create/', MyResumeCreate.as_view(), name='my_resume_create'),
    # admin
    path('admin/', admin.site.urls),
]

# media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
