import django_filters
from django import forms
from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field('status').related_model.objects.all(),
        empty_label='---------',
        label='Статус'
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field('executor').related_model.objects.all(),
        empty_label='---------',
        label='Исполнитель'
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field('labels').related_model.objects.all(),
        empty_label='---------',
        label='Метка'
    )

    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label='Только свои задачи',
        widget=forms.CheckboxInput
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
