from django.http.response import Http404, HttpResponse
from core.models import Test, UserDetail
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, ListView
from django.views import View

from .forms import ProfileForm
from .mixins import ClientZoneMixin


class HomeView(TemplateView):
    template_name = 'home.html'


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile.html'
    success_url = '/accounts/profile'
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        details = UserDetail.objects.get(user=self.request.user)
        context['user_details'] = details
        return context

    def form_valid(self, form):
        user = self.request.user
        user_details = user.userdetail_set.first()

        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        user_details.about_me = form.cleaned_data['about_me']
        user_details.birthday = form.cleaned_data['birthday']
        user_details.profile_img = form.cleaned_data['profile_img'] or user_details.profile_img
        user_details.save()

        return super().form_valid(form)


class ProfileMediaView(LoginRequiredMixin, View):
    def get(self, request, name):
        user_detals = request.user.userdetail_set.first()
        profile_img = user_detals.profile_img
        if name in profile_img.name:
            test_file = open(profile_img.file.name, 'rb')
            response = HttpResponse(content=test_file)
            response['Content-Type'] = 'image'
            return response
        raise Http404("You don't have permissions to others profile data")


class MyTestsView(LoginRequiredMixin, ClientZoneMixin, ListView):
    model = Test
    context_object_name = 'tests'
    template_name = 'accounts/mytests.html'


def logout(request):
    return logout_then_login(request)


def register_view(request):
    return HttpResponse('Registration ...')
