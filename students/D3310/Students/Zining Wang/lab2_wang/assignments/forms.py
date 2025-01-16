# # assignments/forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import Submission

# # 注册用户的表单
# class RegistrationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# # 提交作业的表单
# class SubmissionForm(forms.ModelForm):
#     class Meta:
#         model = Submission
#         fields = ['content']


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Submission, Homework

# 注册用户的表单
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# 提交作业的表单
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['content']

# 作业的表单
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'teacher', 'description', 'due_date', 'penalty']
