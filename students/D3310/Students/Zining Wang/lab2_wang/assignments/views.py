# # from django.shortcuts import render, redirect
# # from django.contrib.auth.forms import UserCreationForm
# # from django.contrib.auth.models import User
# # from django.contrib.auth.decorators import login_required
# # from django.http import HttpResponse
# # from .models import Homework, Submission
# # from .forms import HomeworkForm, SubmissionForm


# # # 用户注册视图
# # def register(request):
# #     if request.method == 'POST':
# #         form = UserCreationForm(request.POST)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('login')  # 注册成功后重定向到登录页
# #     else:
# #         form = UserCreationForm()
# #     return render(request, 'register.html', {'form': form})


# # # 作业列表视图（仅供已登录用户访问）
# # @login_required
# # def homework_list(request):
# #     homeworks = Homework.objects.all()  # 获取所有作业
# #     return render(request, 'homework_list.html', {'homeworks': homeworks})


# # # 显示成绩表（管理员/教师查看所有学生的成绩）
# # @login_required
# # def grade_table(request):
# #     if not request.user.is_superuser:
# #         return HttpResponse("You are not authorized to view this page.", status=403)
    
# #     submissions = Submission.objects.all()  # 获取所有学生提交的作业
# #     return render(request, 'grade_table.html', {'submissions': submissions})


# # # 创建新作业（仅允许管理员/教师）
# # @login_required
# # def create_homework(request):
# #     if not request.user.is_superuser:
# #         return HttpResponse("You are not authorized to create homework.", status=403)

# #     if request.method == 'POST':
# #         form = HomeworkForm(request.POST)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('homework_list')  # 创建作业后跳转到作业列表页面
# #     else:
# #         form = HomeworkForm()
# #     return render(request, 'create_homework.html', {'form': form})


# # # 提交作业（学生提交作业）
# # @login_required
# # def submit_homework(request, homework_id):
# #     homework = Homework.objects.get(id=homework_id)
# #     if request.method == 'POST':
# #         form = SubmissionForm(request.POST)
# #         if form.is_valid():
# #             submission = form.save(commit=False)
# #             submission.homework = homework
# #             submission.student = request.user
# #             submission.save()
# #             return redirect('homework_list')  # 提交作业后跳转回作业列表
# #     else:
# #         form = SubmissionForm()
# #     return render(request, 'submit_homework.html', {'form': form, 'homework': homework})


# # views.py

# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from .models import Homework, Submission, Teacher
# from .forms import HomeworkForm, SubmissionForm
# from django.core.paginator import Paginator
# from django.db.models import Q


# # 用户注册视图
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # 注册成功后重定向到登录页
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})


# # def homework_list(request):
# #     homeworks = Homework.objects.all()  # 获取所有作业
# #     return render(request, 'homework_list.html', {'homeworks': homeworks})


# # 作业列表视图（仅供已登录用户访问）
# @login_required
# def homework_list(request):
#     # 获取所有作业
#     homeworks = Homework.objects.all()  # 这应该返回一个 QuerySet 对象

#     # 搜索功能
#     search_query = request.GET.get('search', '')
#     if search_query:
#         homeworks = homeworks.filter(description__icontains=search_query)

#     # 分页功能
#     paginator = Paginator(homeworks, 10)  # 每页显示 10 个作业
#     page_number = request.GET.get('page')
#     homeworks_page = paginator.get_page(page_number)

#     return render(request, 'homework_list.html', {'homeworks': homeworks_page})


# # 显示成绩表（管理员/教师查看所有学生的成绩）
# @login_required
# def grade_table(request):
#     if not request.user.is_superuser:
#         return HttpResponse("You are not authorized to view this page.", status=403)
    
#     submissions = Submission.objects.all()  # 获取所有学生提交的作业
#     return render(request, 'grade_table.html', {'submissions': submissions})


# # 创建新作业（仅允许管理员/教师）
# @login_required
# def create_homework(request):
#     if not request.user.is_superuser:
#         return HttpResponse("You are not authorized to create homework.", status=403)

#     if request.method == 'POST':
#         form = HomeworkForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('homework_list')  # 创建作业后跳转到作业列表页面
#     else:
#         form = HomeworkForm()
#     return render(request, 'create_homework.html', {'form': form})


# # 提交作业（学生提交作业）
# @login_required
# def submit_homework(request, homework_id):
#     homework = Homework.objects.get(id=homework_id)
#     if request.method == 'POST':
#         form = SubmissionForm(request.POST)
#         if form.is_valid():
#             submission = form.save(commit=False)
#             submission.homework = homework
#             submission.student = request.user
#             submission.save()
#             return redirect('homework_list')  # 提交作业后跳转回作业列表
#     else:
#         form = SubmissionForm()
#     return render(request, 'submit_homework.html', {'form': form, 'homework': homework})


# # 老师名单页面
# @login_required
# def teacher_list(request):
#     # 获取所有老师信息
#     teachers = Teacher.objects.all()  # 获取所有教师
#     return render(request, 'teacher_list.html', {'teachers': teachers})


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Homework, Submission, Teacher
from .forms import HomeworkForm, SubmissionForm
from django.core.paginator import Paginator
from django.db.models import Q

# 用户注册视图
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 注册成功后重定向到登录页
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 作业列表视图（仅供已登录用户访问）
@login_required
def homework_list(request):
    homeworks = Homework.objects.all()  # 获取所有作业

    # 搜索功能
    search_query = request.GET.get('search', '')
    if search_query:
        homeworks = homeworks.filter(description__icontains=search_query)

    # 分页功能
    paginator = Paginator(homeworks, 10)  # 每页显示 10 个作业
    page_number = request.GET.get('page')
    homeworks_page = paginator.get_page(page_number)

    return render(request, 'homework_list.html', {'homeworks': homeworks_page})

# 作业的详细信息页面
@login_required
def homework_detail(request, homework_id):
    try:
        homework = Homework.objects.get(id=homework_id)
    except Homework.DoesNotExist:
        return HttpResponse("Homework not found.", status=404)

    return render(request, 'homework_detail.html', {'homework': homework})

# 老师名单页面
@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()  # 获取所有教师
    return render(request, 'teacher_list.html', {'teachers': teachers})

# 显示成绩表（管理员/教师查看所有学生的成绩）
@login_required
def grade_table(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not authorized to view this page.", status=403)
    
    submissions = Submission.objects.all()  # 获取所有学生提交的作业
    return render(request, 'grade_table.html', {'submissions': submissions})

# 创建新作业（仅允许管理员/教师）
@login_required
def create_homework(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not authorized to create homework.", status=403)

    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homework_list')  # 创建作业后跳转到作业列表页面
    else:
        form = HomeworkForm()
    return render(request, 'create_homework.html', {'form': form})

# 提交作业（学生提交作业）
@login_required
def submit_homework(request, homework_id):
    homework = Homework.objects.get(id=homework_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.homework = homework
            submission.student = request.user
            submission.save()
            return redirect('homework_list')  # 提交作业后跳转回作业列表
    else:
        form = SubmissionForm()
    return render(request, 'submit_homework.html', {'form': form, 'homework': homework})
