""" Bolsa de empleo middleware"""
# Django
from django.shortcuts import redirect
from django.urls import reverse

class PersonCompletationMiddleware:

    def  __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_anonymous:
            if not request.user.is_staff:
                person = request.user.person
                #if not person.picture or not person.phone_number or not person.direction:
                if not person.phone_number:
                    if request.path not in [reverse('update_person'), reverse('log_out')]:
                        return redirect('update_person')
            
        response = self.get_response(request)
        return response
    