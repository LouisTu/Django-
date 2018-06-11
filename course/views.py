from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic.base import TemplateResponseMixin


from .forms import CreateCourseForm, CreateLessonForm
from .models import Course
from .models import Lesson


class AboutView(TemplateView):
    template_name = "course/about.html"


class CourseListView(ListView):
    model = Course
    #queryset = Course.objects.filter(username="TuChiaYu")
    context_object_name = "courses"
    template_name = 'course/course_list.html'

    # def get_queryset(self):
    #     qs = super(user=User.objects.filter(username="TuChiaYu"))


class UserMixin:

    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin):
    model = Course
    login_url = "/account/login/"


class UserLessonMixin(UserMixin):
    model = Lesson
    login_url = "/account/login/"


class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = 'course/manage/manage_course_list.html'


class CreateCourseView(UserCourseMixin, CreateView):
    fields = ['title', 'overview']
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form":form})


class DeleteCourseView(UserCourseMixin, DeleteView):
    template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy("course:manage_course")

    # 出现问题：找不到这个文件夹 course/course_confirm_delete.html
    # def dispatch(self, *args, **kargs):
    #     resp = super(DeleteCourseView, self).dispatch(*args, **kargs)
    #     if self.request.is_ajax():
    #         response_data = {"resule": "ok"}
    #         return HttpResponse(json.dumps(request_data), content_type="application/json")
    #     else:
    #         return resp


class DeleteLessonView(UserLessonMixin, DeleteView):
    template_name = 'course/manage/delete_lesson_confirm.html'
    success_url = reverse_lazy("course:manage_course")


class CreateLessonView(LoginRequiredMixin, View):
    model = Lesson
    login_url = "/account/login/"

    def get(self, request, *args, **kwargs):
        form = CreateLessonForm(user=self.request.user)
        return render(request, "course/manage/create_lesson.html", {"form":form})

    def post(self, request, *args, **kwargs):
        form = CreateLessonForm(self.request.user, request.POST, request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")


class ListLessonView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = "course/manage/list_lesson.html"

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        return self.render_to_response({'course':course})


class ShowLessonView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = "course/show_lesson.html"

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        return self.render_to_response({'course':course})


class DetailLessonView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = "course/manage/detail_lesson.html"

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        return self.render_to_response({"lesson":lesson})