from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from personal_diary.forms import DiaryEntryForm, DateForm
from personal_diary.models import DiaryEntry
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime


@method_decorator(cache_page(60 * 1), name='dispatch')
class DiaryEntryListView(LoginRequiredMixin, ListView):
    """Класс представления вида Generic для эндпоинта списка записей в дневнике."""

    paginate_by = 10
    model = DiaryEntry
    template_name = 'diary_entries.html'
    context_object_name = 'diary_entries'

    def get_queryset(self):
        """Метод для изменения запроса к базе данных по объектам модели "Запись в дневнике"."""
        return DiaryEntry.objects.filter(owner=self.request.user)


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
        return super().form_valid(form)


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


class HomePageView(LoginRequiredMixin, ListView):
    """Класс представления вида Generic для эндпоинта главной страницы."""

    paginate_by = 10
    model = DiaryEntry
    template_name = "home.html"
    context_object_name = 'diary_entries'

    def get_context_data(self, **kwargs):
        """Метод для изменения информации выводимой в представлении."""
        context_data = super().get_context_data(**kwargs)
        context_data["count_entries"] = len(DiaryEntry.objects.filter(updated_at=datetime.date.today()))
        return context_data

    def get_queryset(self):
        """Метод для изменения запроса к базе данных по объектам модели "Запись в дневнике"."""
        return DiaryEntry.objects.filter(owner=self.request.user)


def choice_date(self, request):
    """Метод запроса POST для вывода отфильтрованной информации по записям по выбранной дате."""

    if request.method == 'POST':
        form = DateForm(request.POST or None)
        if form.is_valid():
            selected_date = form.cleaned_data.get('datepicker')
            return redirect('personal_diary:home', kwargs=selected_date)
    else:
        form = DateForm()
    return render(request, 'home.html', {'form': form})


class SearchEntries(LoginRequiredMixin, View):
    """Класс представления вида View для эндпоинта поиска по записям пользователя."""

    paginate_by = 10
    model = DiaryEntry
    template_name = 'diary_entries.html'
    context_object_name = 'diary_entries'

    def get(self, request, *args, **kwargs):
        """Метод запроса GET для вывода отфильтрованной ключевому слову запроса информации по записям."""
        context = {}
        search_query = request.GET.get('search_query')
        user_entries = DiaryEntry.objects.filter(owner=self.request.user)
        if search_query is not None:
            diary_entries = user_entries.filter(
                 Q(title__icontains=search_query) | Q(text__icontains=search_query)).\
                order_by('updated_at')

            context['last_search_query'] = '?search_query=%s' % search_query
            current_page = Paginator(diary_entries, 10)

            page = request.GET.get('page')
            try:
                context['diary_entries'] = current_page.page(page)
            except PageNotAnInteger:
                context['diary_entries'] = current_page.page(1)
            except EmptyPage:
                context['diary_entries'] = current_page.page(current_page.num_pages)
            return diary_entries
        else:
            context['last_search_query'] = '?search_query=%s' % search_query
            current_page = Paginator(user_entries, 10)

            page = request.GET.get('page')
            try:
                context['diary_entries'] = current_page.page(page)
            except PageNotAnInteger:
                context['diary_entries'] = current_page.page(1)
            except EmptyPage:
                context['diary_entries'] = current_page.page(current_page.num_pages)

        return render(request, template_name=self.template_name, context=context)
