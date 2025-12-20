from django import forms
from .models import Homework, Submission, Subject

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'classes', 'title', 'description', 'deadline', 'max_score']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'classes': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'classes': 'Классы (можно выбрать несколько)',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Автоматически установить преподавателя
        if user:
            self.instance.teacher = user


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['answer_text']
        widgets = {
            'answer_text': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Введите ваш ответ на задание...'
            }),
        }
        labels = {
            'answer_text': 'Ваш ответ',
        }


class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'teacher_comment', 'status']
        widgets = {
            'teacher_comment': forms.Textarea(attrs={'rows': 4}),
            'grade': forms.NumberInput(attrs={
                'min': 0, 
                'max': 100,
                'placeholder': 'От 0 до 100'
            }),
        }
        labels = {
            'grade': 'Оценка (0-100)',
            'teacher_comment': 'Комментарий',
            'status': 'Статус работы',
        }


class HomeworkSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по названию или описанию...',
            'class': 'form-control'
        })
    )
    subject = forms.ModelChoiceField(
        queryset=None,  # Будет установлено в __init__
        required=False,
        label='Предмет',
        empty_label='Все предметы',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        required=False,
        label='Статус',
        choices=[
            ('', 'Все'),
            ('upcoming', 'Предстоящие'),
            ('overdue', 'Просроченные'),
            ('submitted', 'Сданные'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.all()