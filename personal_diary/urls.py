from django.urls import path
from personal_diary.apps import PersonalDiaryConfig
from personal_diary.views import DiaryEntryListView, DiaryEntryDetailView, DiaryEntryCreateView, \
    DiaryEntryUpdateView, DiaryEntryDeleteView, SearchEntries, HomePageView, choice_date


app_name = PersonalDiaryConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('choice-date/', choice_date, name='choice_date'),
    path('diary-entries/', DiaryEntryListView.as_view(), name='diary_entries'),
    path('diary-entry/<int:pk>/', DiaryEntryDetailView.as_view(), name='diary_entry'),
    path('diary-entry/new/', DiaryEntryCreateView.as_view(), name='adding_diary_entry'),
    path('diary-entry/<int:pk>/edit/', DiaryEntryUpdateView.as_view(), name='editing_diary_entry'),
    path('diary-entry/<int:pk>/delete/', DiaryEntryDeleteView.as_view(), name='deleting_diary_entry'),
    path('seached-entries/', SearchEntries.as_view(), name='search_entries'),
]
