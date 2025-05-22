from django.contrib import admin
from .models import DiaryEntry, Contact


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'updated_at', 'reminder_date', 'owner__email',)
    list_filter = ('title', 'updated_at', 'reminder_date', 'owner__email',)
    search_fields = ('title', 'updated_at', 'reminder_date', 'owner__email',)

    def get_owner_email(self, obj):
        return obj.owner.email if obj.owner else "Нет данных"

    get_owner_email.short_description = 'E-mail пользователя'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'legal_address', 'mailing_address', 'email', 'tel')
    list_filter = ('id', 'mailing_address',)
    search_fields = ('legal_address', 'mailing_address', 'email', 'tel')
