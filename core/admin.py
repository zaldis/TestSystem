from core.models import Answer, Question, Test, TestResult, UserDetail
from django.contrib import admin


class TestResultAdmin(admin.TabularInline):
    model = TestResult
    can_delete = False
    readonly_fields = ['test', 'corrects', 'total', 'percent', 'passed_date']
    ordering = ('-passed_date', )

    def has_add_permission(self, request, obj=None):
        return False

    def percent(self, obj):
        return f'{100 * obj.corrects / obj.total}%'


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    inlines = [TestResultAdmin, ]
