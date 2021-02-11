from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout_then_login
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.views import View

from core.models import Answer, Comment, Question, Test, UserDetail
from .forms import CommentForm, ProfileForm, QuestionForm, QuestionFormSet, TestForm
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


class MyTestCreateView(LoginRequiredMixin, FormView):
    template_name = 'accounts/create_test.html'
    form_class = TestForm

    def get_success_url(self):
        test_id = self._create_test_with_default_questions()
        return reverse('question_list', args=(test_id, ))

    def _create_test_with_default_questions(self):
        form = self.get_form(); form.is_valid()
        test = Test.objects.create(**form.cleaned_data)

        for _ in range(5):
            question = Question.objects.create(test=test, question='Default question')
            for _ in range(4):
                answer = Answer.objects.create(question=question, text=f'Default answer{_}')
            answer.is_correct = True
            answer.save()

        return test.id


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'accounts/question_list.html'

    def get_queryset(self):
        test_id = self.kwargs['pk']
        return Question.objects.filter(test_id=test_id)

    def post(self, request, pk):
        test = Test.objects.get(id=pk)
        question = Question.objects.create(test=test, question='Default question')
        for _ in range(4):
            answer = Answer.objects.create(question=question, text=f'Default answer{_}')
        answer.is_correct = True
        answer.save()

        return HttpResponseRedirect(request.path_info)

    def get(self, request, pk):
        if request.GET.get('create-test', 'off') == 'on':
            test = Test.objects.get(id=pk)
            test.state = Test.TestState.CREATED
            test.save()
            return HttpResponseRedirect(reverse('mytest_details', args=[pk]))
        return super().get(request, pk)


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'accounts/question_details.html'
    pk_url_kwarg = 'question_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        answers = question.answer_set.all()

        context['answers'] = answers
        return context

    def post(self, request, pk, *args, **kwargs):
        question = self.get_object()

        question.question = request.POST['question']

        for field, value in request.POST.items():
            if 'answer' in field:
                answer_id = field.split('answer-')[-1]
                answer = Answer.objects.get(id=answer_id)
                answer.text = value
                answer.is_correct = request.POST['correct'] == str(answer.id)
                answer.save()

        question.save()
        return HttpResponseRedirect(reverse('question_list', args=[pk]))



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
