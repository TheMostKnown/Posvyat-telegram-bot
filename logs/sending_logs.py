def sending_logs() -> list:
    main = open('/code/logs/main.log', 'r').read()
    django_request = open('/code/logs/django_request.log', 'r').read()
    main = main[-2000:]
    django_request = django_request[-2000:]

    return [main, django_request]



