from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.utils import timezone
from accounts.decorators import teacher_required, student_required
from .models import Homework, Submission, Class, Subject
from .forms import HomeworkForm, SubmissionForm, GradeSubmissionForm, HomeworkSearchForm
from collections import defaultdict


@login_required
def homework_list(request):
    '''Список домашних заданий с поиском и пагинацией'''
    user = request.user
    
    if user.profile.is_student:
        student_classes = user.student_classes.all()
        homeworks = Homework.objects.filter(classes__in=student_classes).distinct()
    else:
        homeworks = Homework.objects.filter(teacher=user)
    
    search_form = HomeworkSearchForm(request.GET)
    
    search_query = request.GET.get('search', '')
    if search_query:
        homeworks = homeworks.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    subject_id = request.GET.get('subject', '')
    if subject_id:
        homeworks = homeworks.filter(subject_id=subject_id)
    
    status = request.GET.get('status', '')
    if status == 'upcoming':
        homeworks = homeworks.filter(deadline__gt=timezone.now())
    elif status == 'overdue':
        homeworks = homeworks.filter(deadline__lte=timezone.now())
    elif status == 'submitted' and user.profile.is_student:
        submitted_hw_ids = Submission.objects.filter(
            student=user
        ).values_list('homework_id', flat=True)
        homeworks = homeworks.filter(id__in=submitted_hw_ids)
    
    homeworks = homeworks.order_by('-created_at')
    
    paginator = Paginator(homeworks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if user.profile.is_student:
        submitted_ids = Submission.objects.filter(
            student=user
        ).values_list('homework_id', flat=True)
        
        for hw in page_obj:
            hw.is_submitted = hw.id in submitted_ids
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'search_query': search_query,
    }
    
    return render(request, 'homework/homework_list.html', context)


@login_required
def homework_detail(request, pk):
    '''Детальная страница домашнего задания'''
    homework = get_object_or_404(Homework, pk=pk)
    user = request.user
    
    if user.profile.is_student:
        student_classes = user.student_classes.all()
        if not homework.classes.filter(id__in=student_classes).exists():
            messages.error(request, 'У вас нет доступа к этому заданию.')
            return redirect('homework:list')
    elif user.profile.is_teacher:
        if homework.teacher != user:
            messages.error(request, 'У вас нет доступа к этому заданию.')
            return redirect('homework:list')
    
    submission = None
    if user.profile.is_student:
        try:
            submission = Submission.objects.get(homework=homework, student=user)
        except Submission.DoesNotExist:
            pass
    
    context = {
        'homework': homework,
        'submission': submission,
    }
    
    return render(request, 'homework/homework_detail.html', context)


@teacher_required
def homework_create(request):
    '''Создание домашнего задания (только учитель)'''
    if request.method == 'POST':
        form = HomeworkForm(request.POST, user=request.user)
        if form.is_valid():
            homework = form.save()
            messages.success(request, 'Домашнее задание успешно создано!')
            return redirect('homework:detail', pk=homework.pk)
    else:
        form = HomeworkForm(user=request.user)
    
    return render(request, 'homework/homework_form.html', {
        'form': form,
        'title': 'Создать домашнее задание'
    })


@teacher_required
def homework_update(request, pk):
    '''Редактирование домашнего задания (только учитель-создатель)'''
    homework = get_object_or_404(Homework, pk=pk)
    
    if homework.teacher != request.user:
        messages.error(request, 'Вы не можете редактировать чужое задание.')
        return redirect('homework:detail', pk=pk)
    
    if request.method == 'POST':
        form = HomeworkForm(request.POST, instance=homework, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Домашнее задание обновлено!')
            return redirect('homework:detail', pk=homework.pk)
    else:
        form = HomeworkForm(instance=homework, user=request.user)
    
    return render(request, 'homework/homework_form.html', {
        'form': form,
        'title': 'Редактировать задание',
        'homework': homework
    })


@teacher_required
def homework_delete(request, pk):
    '''Удаление домашнего задания (только учитель-создатель)'''
    homework = get_object_or_404(Homework, pk=pk)
    
    if homework.teacher != request.user:
        messages.error(request, 'Вы не можете удалить чужое задание.')
        return redirect('homework:detail', pk=pk)
    
    if request.method == 'POST':
        homework.delete()
        messages.success(request, 'Домашнее задание удалено.')
        return redirect('homework:list')
    
    return render(request, 'homework/homework_confirm_delete.html', {
        'homework': homework
    })


@student_required
def submit_homework(request, pk):
    '''Сдача домашнего задания (только студент)'''
    homework = get_object_or_404(Homework, pk=pk)
    user = request.user
    
    # Проверка доступа
    student_classes = user.student_classes.all()
    if not homework.classes.filter(id__in=student_classes).exists():
        messages.error(request, 'У вас нет доступа к этому заданию.')
        return redirect('homework:list')
    
    # Проверка что уже не сдано
    if Submission.objects.filter(homework=homework, student=user).exists():
        messages.warning(request, 'Вы уже сдали это задание.')
        return redirect('homework:detail', pk=pk)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.homework = homework
            submission.student = user
            submission.save()
            messages.success(request, 'Задание успешно сдано!')
            return redirect('homework:detail', pk=homework.pk)
    else:
        form = SubmissionForm()
    
    context = {
        'form': form,
        'homework': homework,
    }
    
    return render(request, 'homework/submit_homework.html', context)


@login_required
def submission_list(request):
    '''Список сданных работ'''
    user = request.user
    
    if user.profile.is_student:
        # Студент видит свои работы
        submissions = Submission.objects.filter(student=user)
    else:
        # Учитель видит работы по своим заданиям
        submissions = Submission.objects.filter(homework__teacher=user)
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        submissions = submissions.filter(
            Q(homework__title__icontains=search_query) |
            Q(student__username__icontains=search_query) |
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query)
        )
    
    # Фильтр по статусу
    status = request.GET.get('status', '')
    if status:
        submissions = submissions.filter(status=status)
    
    submissions = submissions.order_by('-submitted_at')
    
    # Пагинация
    paginator = Paginator(submissions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'submissions': submissions,
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'homework/submission_list.html', context)


@teacher_required
def grade_submission(request, pk):
    '''Оценивание работы (только учитель)'''
    submission = get_object_or_404(Submission, pk=pk)
    
    # Проверка что это работа по заданию этого учителя
    if submission.homework.teacher != request.user:
        messages.error(request, 'Вы не можете оценить эту работу.')
        return redirect('homework:submission_list')
    
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f'Работа оценена! Итоговый балл: {submission.final_score()}')
            return redirect('homework:submission_list')
    else:
        form = GradeSubmissionForm(instance=submission)
    
    context = {
        'form': form,
        'submission': submission,
        'penalty': submission.calculate_penalty(),
    }
    
    return render(request, 'homework/grade_submission.html', context)


@login_required
def my_grades(request):
    if request.user.profile.is_teacher:
        return redirect("homework:grades_table")

    submissions = (
        Submission.objects
        .filter(student=request.user, grade__isnull=False)
        .select_related("homework__subject")
    )

    subjects_map = defaultdict(list)

    for submission in submissions:
        subjects_map[submission.homework.subject].append(submission.grade)

    subjects_data = []
    for subject, grades in subjects_map.items():
        subjects_data.append({
            "subject": subject,
            "grades": grades,
            "average": round(sum(grades) / len(grades), 2) if grades else None
        })

    return render(
        request,
        "homework/my_grades.html",
        {"subjects_data": subjects_data}
    )


@login_required
def grades_table(request):
    user = request.user

    class_id = request.GET.get("class_id")
    subject_id = request.GET.get("subject_id")

    student_class = None
    subject = None

    if class_id:
        student_class = Class.objects.filter(id=class_id).first()

    if subject_id:
        subject = Subject.objects.filter(id=subject_id).first()

    # Доступ
    if user.profile.is_teacher:
        available_classes = Class.objects.filter(
            homeworks__teacher=user
        ).distinct()

        available_subjects = Subject.objects.filter(
            homeworks__teacher=user
        ).distinct()
        
        # Если класс не выбран, берём первый доступный
        if not student_class:
            student_class = available_classes.first()
    else:
        # Студент видит только свой класс
        student_class = user.student_classes.first()
        if not student_class:
            messages.warning(request, 'Вы не привязаны к классу.')
            return redirect('homework:list')
        
        available_classes = []
        available_subjects = Subject.objects.filter(
            homeworks__classes=student_class  # ← Исправлено
        ).distinct()

    homeworks = []
    table_data = []

    if student_class:
        # Фильтруем домашки по классу
        homeworks = Homework.objects.filter(
            classes=student_class  # ← Исправлено (было student_class)
        )
        
        # Дополнительно фильтруем по предмету если выбран
        if subject:
            homeworks = homeworks.filter(subject=subject)
        
        homeworks = homeworks.order_by('created_at')

        # Получаем студентов класса
        students = student_class.students.all().order_by('last_name', 'first_name')

        # Формируем таблицу
        for student in students:
            row = {
                'student': student,
                'grades': [],
                'total': 0,
                'count': 0,
            }

            for hw in homeworks:
                try:
                    submission = Submission.objects.get(homework=hw, student=student)
                    score = submission.final_score()
                    
                    # Рассчитываем пороги для цветов
                    threshold_high = hw.max_score * 0.8
                    threshold_medium = hw.max_score * 0.5
                    
                    if score is not None:
                        if score >= threshold_high:
                            color_class = 'excellent'
                        elif score >= threshold_medium:
                            color_class = 'good'
                        else:
                            color_class = 'poor'
                    else:
                        color_class = 'none'
                    
                    row['grades'].append({
                        'submission': submission,
                        'score': score,
                        'color_class': color_class,
                    })
                    
                    if score is not None:
                        row['total'] += score
                        row['count'] += 1
                        
                except Submission.DoesNotExist:
                    row['grades'].append(None)

            # Средний балл
            row['average'] = round(row['total'] / row['count'], 2) if row['count'] > 0 else 0
            table_data.append(row)

    context = {
        "student_class": student_class,
        "subject": subject,
        "available_classes": available_classes,
        "available_subjects": available_subjects,
        "homeworks": homeworks,
        "table_data": table_data,
    }

    return render(request, "homework/grades_table.html", context)