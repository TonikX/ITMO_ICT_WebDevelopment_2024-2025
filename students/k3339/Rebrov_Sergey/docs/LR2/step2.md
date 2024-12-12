Для ученика доступны следующие разделы:

- В разделе "Задания" ученик может видеть текущие невыполненные задания и переходить к их выполнению.
- В разделе "Оценки" ученик может видеть таблицу со своими оценками по предметам, а также оценки своих одноклассников.

При этом учитель не имеет доступа к этим разделам.

views.py
```python
def homework_list(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login-user')

    schooluser = get_object_or_404(SchoolUser, user=request.user)

    tasks = Task.objects.select_related('discipline_id', 'class_id') \
        .filter(class_id=schooluser.class_id) \
        .exclude(grade__schooluser_id=schooluser.id)  \
        .order_by('due_date')

    return render(request, 'homework_list.html', {
        'schooluser': schooluser,
        'tasks': tasks
    })


def homework_submit(request, task_id):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login-user')

    task = get_object_or_404(Task, id=task_id)
    schooluser = get_object_or_404(SchoolUser, user=request.user)

    if task.class_id != schooluser.class_id or Grade.objects.filter(task_id=task_id, schooluser_id=schooluser.id).exists():
        return redirect('homework-list')

    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.schooluser_id = schooluser
            grade.task_id = task
            grade.save()
            return redirect('homework-list')
    else:
        form = HomeworkSubmissionForm()

    return render(request, 'homework_submit.html', {
        'schooluser': schooluser,
        'form': form,
        'task': task
    })


def grade_table(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login-user')

    current_schooluser = get_object_or_404(SchoolUser, user=request.user)
    classmates = SchoolUser.objects.filter(class_id=current_schooluser.class_id, user__is_staff=False)
    disciplines = Discipline.objects.filter(task__grade__schooluser_id__class_id=current_schooluser.class_id).distinct()

    table = []

    for schooluser in classmates:
        row = [f"{schooluser.user.first_name} {schooluser.user.last_name}"]

        for discipline in disciplines:
            schooluser_grades = Grade.objects.filter(schooluser_id=schooluser, task_id__discipline_id=discipline)

            if schooluser_grades.exists():
                row.append(', '.join([str(grade.number if grade.number is not None else 'н') for grade in schooluser_grades]))
            else:
                row.append('Нет оценок')

        table.append(row)

    return render(request, 'grade_table.html', {
        'schooluser': current_schooluser,
        'table': table,
        'disciplines': disciplines
    })
```