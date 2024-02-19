from django.utils import timezone
from django.utils.translation import activate

class UserTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'timezone' in request.session:
            timezone.activate(request.session['timezone'])
        if 'language' in request.session:
            activate(request.session['language'])
        response = self.get_response(request)
        return response