from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse

class AuthRequiredMiddleware(MiddlewareMixin):
    #@method_decorator(login_required(login_url='/login'))

    def process_request(self, request):
        if (request.path == reverse('cas_ng_login') or request.path == reverse('cas_ng_logout')): 
            return None
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('cas_ng_login')) # or http response
        return None

