""" mock data """
''' Вакансии '''

vacancies = [

    {
        'title': 'Разработчик на Python',
        'specialty': 'backend',
        'company': 'staffingsmarter',
        'skills': 'терпимость, смирение',
        'salary_min': '100000',
        'salary_max': '150000',
        'published_at': '2020-03-11',
        'description': 'Потом добавим',
    },
    {
        'title': 'Разработчик в проект на Django',
        'specialty': 'backend',
        'company': 'swiftattack',
        'skills': 'умение спать на работе незаметно',
        'salary_min': '80000',
        'salary_max': '90000',
        'published_at': '2020-03-11',
        'description': 'Потом добавим'
    },
    {
        'title': 'Разработчик на Swift в аутсорс компанию',
        'specialty': 'backend',
        'company': 'swiftattack',
        'skills': 'коммуникабельность, стрессоустойчивость',
        'salary_min': '120000',
        'salary_max': '150000',
        'published_at': '2020-03-11',
        'description': 'Потом добавим'
    },
    {
        'title': 'Мидл программист на Python',
        'specialty': 'backend',
        'company': 'workiro',
        'skills': 'умение работать за еду, коммуникабельность',
        'salary_min': '80000',
        'salary_max': '90000',
        'published_at': '2020-03-11',
        'description': 'Потом добавим'
    },
    {
        'title': 'Питонист в стартап',
        'specialty': 'backend',
        'company': 'primalassault',
        'skills': 'умение работать за еду, умение спать на работе незаметно',
        'salary_min': '120000',
        'salary_max': '150000',
        'published_at': '2020-03-11',
        'description': 'Потом добавим'
    }

]

''' Компании '''

companies = [

    {
        'name': 'workiro',
        'location': 'london',
        'logo': 'company_images/logo1.png',
        'description': 'the best company in the world',
        'employee_count': 10000
    },
    {
        'name': 'rebelrage',
        'location': 'sealand',
        'logo': 'company_images/logo2.png',
        'description': 'the worst company in the world',
        'employee_count': 1
    },
    {
        'name': 'staffingsmarter',
        'location': 'tagil',
        'logo': 'company_images/logo3.png',
        'description': 'the mediocrest company in the world',
        'employee_count': 5
    },
    {
        'name': 'evilthreat',
        'location': 'usa',
        'logo': 'company_images/logo4.png',
        'description': 'be evil is our motto',
        'employee_count': 1000000
    },
    {
        'name': 'hirey',
        'location': 'moscow',
        'logo': 'company_images/logo5.png',
        'description': 'we hire people wooo',
        'employee_count':54
    },
    {
        'name': 'swiftattack',
        'location': 'holy terra',
        'logo': 'company_images/logo6.png',
        'description': 'for emperor!!!1111',
        'employee_count': 1000000000
    },
    {
        'name': 'troller',
        'location': 'internet',
        'logo': 'company_images/logo7.png',
        'description': 'we troll people. that\'s it',
        'employee_count': 1000
    },
    {
        'name': 'primalassault',
        'location': 'location',
        'logo': 'company_images/logo8.png',
        'description': 'description',
        'employee_count': 0
    },

]

''' Категории '''

specialties = [

    {
        'code': 'frontend',
        'title': 'Фронтенд',
        'picture': 'specialty_images/specty_frontend.png'
    },
    {
        'code': 'backend',
        'title': 'Бэкенд',
        'picture': 'specialty_images/specty_backend.png'
    },
    {
        'code': 'gamedev',
        'title': 'Геймдев',
        'picture': 'specialty_images/specty_gamedev.png'
    },
    {
        'code': 'devops',
        'title': 'Девопс',
        'picture': 'specialty_images/specty_devops.png'
    },
    {
        'code': 'design',
        'title': 'Дизайн',
        'picture': 'specialty_images/specty_design.png'
    },
    {
        'code': 'products',
        'title': 'Продукты',
        'picture': 'specialty_images/specty_products.png'
    },
    {
        'code': 'management',
        'title': 'Менеджмент',
        'picture': 'specialty_images/specty_management.png'
    },
    {
        'code': 'testing',
        'title': 'Тестирование',
        'picture': 'specialty_images/specty_testing.png'
    }
]
