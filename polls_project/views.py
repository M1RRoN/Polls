from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from polls.models import Poll


class HomeView(View):
    template_name = 'base.html'

    def get(self, request):
        polls = Poll.objects.all()
        return render(request, self.template_name, {'polls': polls})