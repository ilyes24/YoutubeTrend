from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import FormView

from users.forms import LogoutForm


@login_required(login_url='/login/')
def home(request):
    ctx = {}
    return render(request, 'home.html', context=ctx)


@login_required(login_url='/login/')
def logoutnow(request):

    logout(request)
    return HttpResponseRedirect(reverse('Home'))


class LogoutView(FormView):
    form_class = LogoutForm
    template_name = "registration/logout.html"

    def form_valid(self, form):
        logout(self.request)
        return HttpResponseRedirect(reverse('Home'))


