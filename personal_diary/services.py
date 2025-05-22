from django.core.cache import cache
from jotter.settings import CACHE_ENABLED
from personal_diary.models import DiaryEntry


def get_mailing_from_cache():
    """Получение данных по записям из кэша, если кэш пуст берем из БД."""
    if not CACHE_ENABLED:
        return DiaryEntry.objects.all()
    key = "mailing_list"
    cache_data = cache.get(key)
    if cache_data is not None:
        return cache_data
    cache_data = DiaryEntry.objects.all()
    cache.set(key, cache_data)
    return cache_data
