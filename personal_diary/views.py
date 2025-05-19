from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from personal_diary.forms import DiaryEntryForm
from personal_diary.models import DiaryEntry
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class DiaryEntryListView(LoginRequiredMixin, ListView):
    """Класс представления вида Generic для эндпоинта списка записей в дневнике."""
    paginate_by = 4
    model = DiaryEntry
    template_name = 'diary_entries.html'
    context_object_name = 'diary_entries'

    def get_queryset(self, *args, **kwargs):
        """Метод для изменения запроса к базе данных по объектам модели "Запись в дневнике"."""
        return super().get_queryset().filter(owner=self.request.user)


@method_decorator(cache_page(60 * 1), name='dispatch')
class DiaryEntryDetailView(LoginRequiredMixin, DetailView):
    """Класс представления вида Generic для эндпоинта просмотра записи в дневнике."""
    model = DiaryEntry
    template_name = 'diary_entry.html'

    def get_object(self, queryset=None):
        """Метод проверки на доступ к объекту "Запись в дневнике"."""
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise PermissionDenied
        return self.object


class DiaryEntryCreateView(LoginRequiredMixin, CreateView):
    """Класс представления вида Generic для эндпоинта создания записи в дневнике."""
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = 'adding_diary_entry.html'
    success_url = reverse_lazy('personal_diary:diary_entries')

    def form_valid(self, form):
        """Метод вносит изменение в переданную после проверки на валидацию форму создания "Запись в дневнике"."""
        diary_entry = form.save()
        diary_entry.owner = self.request.user
        diary_entry.save()


class DiaryEntryUpdateView(LoginRequiredMixin, UpdateView):
    """Класс представления вида Generic для эндпоинта изменения записи в дневнике."""
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = 'editing_diary_entry.html'

    def get_object(self, queryset=None):
        """Метод проверки на доступ к объекту "Запись в дневнике"."""
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise PermissionDenied
        return self.object

    def get_success_url(self, **kwargs):
        """Метод переадресации пользователя после выполнения данного представления."""
        return reverse('personal_diary:diary_entry', args=[self.kwargs.get('pk')])


class DiaryEntryDeleteView(LoginRequiredMixin, DeleteView):
    """Класс представления вида Generic для эндпоинта удаления записи в дневнике."""
    model = DiaryEntry
    template_name = 'diary_entry_confirm_delete.html'
    success_url = reverse_lazy('personal_diary:diary_entries')

    def get_object(self, queryset=None):
        """Метод проверки на доступ к объекту "Запись в дневнике"."""
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise PermissionDenied
        return self.object
