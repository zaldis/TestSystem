from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout_then_login
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls.base import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.views import View

from core.models import Comment, Test, UserDetail
from .forms import CommentForm, ProfileForm
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

    def get_queryset(self):
        result = super().get_queryset().order_by('-creation_date')

        search = self.request.GET.get('search', '')
        result = result.filter(title__icontains=search)

        is_passed = self.request.GET.get('is_passed', 'off') == 'on'
        if is_passed:
            result = result.filter(passes__gte=1)

        sort_by_asc = self.request.GET.get('sort', 'off') == 'on'
        if sort_by_asc:
            result = result.order_by('creation_date')

        return result


class MyTestDetailsView(LoginRequiredMixin, DetailView):
    model = Test
    context_object_name = 'test'
    template_name = 'accounts/test_details.html'

    def get_context_data(self, **kwargs):
        comments = self.object.comment_set.all().order_by('-creation_date')
        context = super().get_context_data(**kwargs)
        context['comments'] = comments
        return context


class CommentView(LoginRequiredMixin, FormView):
    form_class = CommentForm
    success_url = '/accounts/profile'
    template_name = 'accounts/test_details.html'

    def form_valid(self, form):
        super().form_valid(form)
        Comment.objects.create(
            test_id=form.cleaned_data['test_id'],
            text=form.cleaned_data['text']
        )

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        test_id = self.request.POST['test_id']
        return redirect(
            reverse('mytest_details', args=(test_id, ))
        )


def logout(request):
    return logout_then_login(request)


def register_view(request):
    return HttpResponse('Registration ...')
