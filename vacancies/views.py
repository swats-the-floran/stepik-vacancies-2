from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.db.models import Count

from stepik_vacancies.settings import PROJECT_NAME, MEDIA_URL
from vacancies.forms import ApplicationForm, LogInForm, RegisterForm, MyCompanyForm, VacancyForm, ResumeForm, SearchForm
from vacancies.models import Vacancy, Company, Specialty, Application, Resume


###############################################################################
#                                   main                                      #
###############################################################################


def define_context(request, **kwargs):

    context = {
        'project_name': PROJECT_NAME,
        'media_url': MEDIA_URL,
        'previous_page': request.META.get('HTTP_REFERER')
    }

    if request.user.is_authenticated:
        full_name = request.user.get_full_name()
        context['username'] = full_name if full_name != '' else request.user.username

    return {**context, **kwargs}


class MainPage(View):

    def get(self, request):

        search_form = SearchForm()

        context = define_context(
            request,
            specialties=Specialty.objects.annotate(count=Count('vacancies')),
            companies=Company.objects.annotate(count=Count('vacancies')),
            search_form=search_form,
        )

        return render(request, 'vacancies/index.html', context=context)

    def post(self, request):

        search_form = SearchForm(request.POST)
        search_string = search_form.data.get('search_string')

        if search_form.is_valid() and search_string is not None:
            return redirect(f"{reverse('search')}?s={search_string}")
        else:
            context = define_context(
                request,
                title_prefix='Вакансии',
                vacancies={},
                search_form=search_form,
            )
            return render(request, 'vacancies/search.html', context=context)

        return redirect()


class AboutProject(View):

    def get(self, request):

        return HttpResponse('Здесь будет страница о проекте.')


class LogIn(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('/')

        context = define_context(
            request,
            login_form=LogInForm(),
        )

        return render(request, 'vacancies/login.html', context=context)

    def post(self, request):

        login_form = LogInForm(request.POST)

        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                login_form.add_error('username', 'Авторизация не завершена. Логин или пароль указаны неверно.')
                return render(request, 'vacancies/login.html', {'login_form': login_form})
        else:
            return render(request, 'vacancies/login.html', {'login_form': login_form})


class LogOut(View):

    def get(self, request):
        logout(request)
        return redirect('/')


class Register(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('/')

        context = define_context(request, register_form=RegisterForm())
        return render(request, 'vacancies/register.html', context=context)

    def post(self, request):

        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return redirect(reverse('login_page'))
        else:
            context = define_context(request, register_form=register_form)
            return render(request, 'vacancies/register.html', context=context)


class Search(View):

    def find(self, request):

        search_string = request.GET.get('s')
        all_vacancies = {}
        if search_string is not None:
            vacancies_by_title = Vacancy.objects.filter(title__icontains=search_string)
            vacancies_by_company = Vacancy.objects.filter(company__name__icontains=search_string)
            vacancies_by_skills = Vacancy.objects.filter(skills__icontains=search_string)
            vacancies_by_description = Vacancy.objects.filter(description__icontains=search_string)

            all_vacancies = vacancies_by_title | vacancies_by_company | vacancies_by_skills | vacancies_by_description

        context = define_context(
            request,
            title_prefix='Вакансии',
            vacancies=all_vacancies,
            search_form=SearchForm(),
        )

        return context

    def get(self, request):

        return render(request, 'vacancies/search.html', context=self.find(request))

    def post(self, request):

        search_form = SearchForm(request.POST)
        search_string = search_form.data.get('search_string')

        if search_form.is_valid() and search_string is not None:
            return redirect(f"{reverse('search')}?s={search_string}")
        else:
            context = define_context(
                request,
                title_prefix='Вакансии',
                vacancies={},
                search_form=search_form,
            )
            return render(request, 'vacancies/search.html', context=context)


###############################################################################
#                               vacancies                                     #
###############################################################################


class VacanciesElement(View):

    def get(self, request, vacancy_id):

        vacancy_obj = get_object_or_404(Vacancy, id=vacancy_id)

        context = define_context(
            request,
            title_prefix=vacancy_obj.title,
            vacancy=vacancy_obj,
            company=vacancy_obj.company,
        )

        if request.user.is_authenticated:
            context['application_form'] = ApplicationForm()

        return render(request, 'vacancies/vacancy.html', context=context)

    def post(self, request, vacancy_id):

        application_form = ApplicationForm(request.POST)

        if application_form.is_valid():
            application_form = application_form.save(commit=False)
            application_form.user = request.user
            application_form.vacancy = Vacancy.objects.get(id=vacancy_id)
            application_form.save()

            return redirect(reverse('vacancies_sent_application', kwargs={'vacancy_id': vacancy_id}))
        else:
            vacancy_obj = get_object_or_404(Vacancy, id=vacancy_id)

            context = define_context(
                request,
                title_prefix=vacancy_obj.title,
                vacancy=vacancy_obj,
                company=vacancy_obj.company,
                application_form=application_form,
            )

            return render(request, 'vacancies/vacancy.html', context=context)


class SentApplication(View):

    def get(self, request, vacancy_id):
        context = define_context(
            request,
            title_prefix='Отклик отправлен',
            vacancy_id=vacancy_id,
        )

        return render(request, 'vacancies/sent.html', context=context)


class VacanciesList(View):

    def get(self, request):

        context = define_context(
            request,
            title_prefix='Все вакансии',
            specialty_title='ВСЕ ВАКАНСИИ',
            vacancies=Vacancy.objects.all(),
        )

        return render(request, 'vacancies/vacancies.html', context=context)


class VacanciesListBySpecialty(View):

    def get(self, request, specialty_code):

        specialty_obj = get_object_or_404(Specialty, code=specialty_code)

        context = define_context(
            request,
            title_prefix=specialty_obj.title,
            specialty_title=specialty_obj.title,
            vacancies=specialty_obj.vacancies.all(),
        )

        return render(request, 'vacancies/vacancies.html', context=context)


###############################################################################
#                               companies                                     #
###############################################################################


class CompaniesElement(View):

    def get(self, request, company_id):

        company_obj = get_object_or_404(Company, id=company_id)
        vacancies = Vacancy.objects.filter(company=company_obj)

        context = define_context(
            request,
            title_prefix=company_obj.name,
            vacancies=vacancies,
            company=company_obj,
        )

        return render(request, 'vacancies/company.html', context=context)


class CompaniesList(View):

    def get(self, request):

        return HttpResponse('Здесь будет список компаний.')


###############################################################################
#                               my company                                    #
###############################################################################


class MyCompany(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))

        company_obj = Company.objects.filter(owner=request.user).first()

        if company_obj is None:
            return redirect(reverse('my_company_create'))

        my_company_form = MyCompanyForm(instance=company_obj)

        context = define_context(
            request,
            title_prefix='Моя компания',
            company=company_obj,
            my_company_form=my_company_form,
        )

        return render(request, 'vacancies/company-edit.html', context=context)

    def post(self, request):

        company_obj = Company.objects.get(owner=request.user)
        my_company_form = MyCompanyForm(request.POST, request.FILES, instance=company_obj)

        if my_company_form.is_valid():
            my_company_form = my_company_form.save(commit=False)
            my_company_form.owner = request.user
            my_company_form.save()

            context = define_context(
                request,
                title_prefix='Моя компания',
                company=company_obj,
                my_company_form=MyCompanyForm(instance=company_obj),
                updated=True,
            )

            return render(request, 'vacancies/company-edit.html', context=context)
        else:
            context = define_context(
                request,
                title_prefix='Моя компания',
                company=company_obj,
                my_company_form=my_company_form,
            )
            return render(request, 'vacancies/company-edit.html', context=context)


class MyCompanyCreate(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))

        company_obj = Company.objects.filter(owner=request.user).first()

        if company_obj is not None:
            return redirect(reverse('my_company'))

        context = define_context(
            request,
            title_prefix='Создание компании',
            my_company_form=MyCompanyForm(),
        )

        return render(request, 'vacancies/company-create.html', context=context)

    def post(self, request):

        my_company_form = MyCompanyForm(request.POST, request.FILES)

        if my_company_form.is_valid():
            my_company_form = my_company_form.save(commit=False)
            my_company_form.owner = request.user
            my_company_form.save()
            return redirect(reverse('my_company'))
        else:
            context = define_context(
                request,
                title_prefix='Создание компании',
                my_company_form=my_company_form,
            )
            return render(request, 'vacancies/company-create.html', context=context)


class MyCompanyVacanciesCreate(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))

        company_obj = Company.objects.filter(owner=request.user).first()

        if company_obj is None:
            return redirect(reverse('my_company_create'))

        context = define_context(
            request,
            title_prefix='Создание вакансии',
            vacancy_form=VacancyForm(),
        )

        return render(request, 'vacancies/vacancy-edit.html', context=context)

    def post(self, request):

        vacancy_form = VacancyForm(request.POST)
        company_obj = Company.objects.filter(owner=request.user).first()

        if vacancy_form.is_valid():
            vacancy_form = vacancy_form.save(commit=False)
            vacancy_form.company = company_obj
            vacancy_form.owner = request.user
            vacancy_form.published_at = datetime.today()
            vacancy_form.save()
            return redirect(reverse('my_company_vacancies_list'))
        else:
            context = define_context(
                request,
                title_prefix='Создание вакансии',
                my_company_form=vacancy_form,
            )
            return render(request, 'vacancies/company-create.html', context=context)


class MyCompanyVacanciesElement(View):

    def get(self, request, vacancy_id):

        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))

        company_obj = Company.objects.filter(owner=request.user).first()
        if company_obj is None:
            return redirect(reverse('my_company_create'))

        vacancy_obj = Vacancy.objects.filter(id=vacancy_id, company=company_obj).first()
        if vacancy_obj is None:
            return redirect(reverse('my_company_vacancies_create'))

        context = define_context(
            request,
            title_prefix=vacancy_obj.title,
            vacancy=vacancy_obj,
            applications=Application.objects.filter(vacancy=vacancy_obj),
            vacancy_form=VacancyForm(instance=vacancy_obj),
        )

        return render(request, 'vacancies/vacancy-edit.html', context=context)

    def post(self, request, vacancy_id):

        vacancy_obj = Vacancy.objects.get(id=vacancy_id)
        company_obj = Company.objects.get(owner=request.user)

        vacancy_form = VacancyForm(request.POST, instance=vacancy_obj)

        if vacancy_form.is_valid():
            vacancy_form = vacancy_form.save(commit=False)
            vacancy_form.company = company_obj
            vacancy_form.save()

            context = define_context(
                request,
                title_prefix=vacancy_obj.title,
                vacancy=vacancy_obj,
                applications=Application.objects.filter(vacancy=vacancy_obj),
                vacancy_form=VacancyForm(instance=vacancy_obj),
                updated=True,
            )

            return render(request, 'vacancies/vacancy-edit.html', context=context)
        else:
            applications_qs = Application.objects.filter(vacancy=vacancy_obj)

            context = define_context(
                request,
                title_prefix=vacancy_obj.title,
                vacancy=vacancy_obj,
                applications=applications_qs,
                vacancy_form=vacancy_form,
            )

            return render(request, 'vacancies/vacancy-edit.html', context=context)


class MyCompanyVacanciesList(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))

        company_obj = Company.objects.filter(owner=request.user).first()
        if company_obj is None:
            return redirect(reverse('my_company_create'))

        vacancies = Vacancy.objects.filter(company=company_obj).annotate(apps_count=Count('applications'))

        context = define_context(
            request,
            title_prefix='Мои вакансии',
            specialty_title='МОИ ВАКАНСИИ',
            vacancies=vacancies,
            company=company_obj,
        )

        return render(request, 'vacancies/vacancy-list.html', context=context)


###############################################################################
#                                  resumes                                    #
###############################################################################


class MyResume(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))

        resume_obj = Resume.objects.filter(user=request.user).first()

        if resume_obj is None:
            return redirect(reverse('my_resume_create'))

        resume_form = ResumeForm(instance=resume_obj)

        context = define_context(
            request,
            title_prefix='Моё резюме',
            resume_form=resume_form,
        )

        return render(request, 'vacancies/resume-edit.html', context=context)

    def post(self, request):

        resume_obj = Resume.objects.filter(user=request.user).first()
        resume_form = ResumeForm(request.POST, request.FILES, instance=resume_obj)

        if resume_form.is_valid():
            resume_form = resume_form.save(commit=False)
            resume_form.user = request.user
            resume_form.save()

            context = define_context(
                request,
                title_prefix='Моё резюме',
                resume_form=ResumeForm(instance=resume_obj),
                updated=True,
            )

            return render(request, 'vacancies/resume-edit.html', context=context)
        else:
            context = define_context(
                request,
                title_prefix='Моё резюме',
                resume_form=resume_form,
                updated=True,
            )
            return render(request, 'vacancies/resume-edit.html', context=context)


class MyResumeCreate(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))

        resume_obj = Resume.objects.filter(user=request.user).first()

        if resume_obj is not None:
            return redirect(reverse('my_resume'))

        context = define_context(
            request,
            title_prefix='Создание резюме',
            resume_form=ResumeForm(),
        )

        return render(request, 'vacancies/resume-create.html', context=context)

    def post(self, request):

        resume_form = ResumeForm(request.POST, request.FILES)

        if resume_form.is_valid():
            resume_form = resume_form.save(commit=False)
            resume_form.user = request.user
            resume_form.save()
            return redirect(reverse('my_resume'))
        else:
            context = define_context(
                request,
                title_prefix='Моё резюме',
                resume_form=resume_form,
                updated=True,
            )
            return render(request, 'vacancies/resume-edit.html', context=context)
