from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic
from polls.models import Poll


class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        polls = Poll.objects.all()
        return render(request, self.template_name, {'polls': polls})


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
