from django import forms
from .models import DiaryEntry, Contact
from django.core.exceptions import ValidationError


class DiaryEntryForm(forms.ModelForm):
    """Класс формы модели "Запись в дневнике"."""
    reminder_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False,
                                        label='Напомнить')

    class Meta:
        """Класс для изменения поведения полей формы модели "Запись в дневнике"."""
        model = DiaryEntry
        fields = ['title', 'reminder_date', 'picture', 'text']

    def clean_reminder_date(self):
        """Метод проверки поля "Дата напоминания" формы модели "Запись в дневнике"."""
        cleaned_diary_entry_pk = self.instance.pk
        reminder_date = self.cleaned_data.get('reminder_date')

        if DiaryEntry.objects.filter(reminder_date=reminder_date).exclude(id=cleaned_diary_entry_pk).exists() \
                and not None:
            raise ValidationError('Данное время уже занято другой записью.')
        return reminder_date

    def __init__(self, *args, **kwargs):
        """Инициализирует поля формы"""
        super(DiaryEntryForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите заголовок записи'})
        self.fields['reminder_date'].widget.attrs.update({'class': 'form-control',
                                                         'aria-label': 'Напомнить'})
        self.fields['picture'].widget.attrs.update({'class': 'form-control', 'type': 'file', 'id': 'formFile'})
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1",
                                                'rows': "4", 'placeholder': 'Введите текст записи'})


class ContactForm(forms.ModelForm):
    """Класс формы модели "Контакты"."""
    class Meta:
        """Класс для изменения поведения полей формы модели "Запись в дневнике"."""
        model = Contact
        fields = '__all__'


class DateForm(forms.Form):
    """Класс формы для дат."""
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
