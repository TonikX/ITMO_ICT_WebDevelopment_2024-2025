Для учителя доступны следующие разделы:

- В разделе "Оценивание" учитель может видеть присланные на проверку задания, которые создавал этот учитель, и переходить к их оцениванию.
- В разделе "Создать задание" учитель может создать новое задание, заполнив соответствующую форму, а это задания увидят все ученики класса, которому было выдано это задание.

При этом ученик не имеет доступа к этим разделам.

views.py
```python
def teachers_list(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login-user')

    schooluser = get_object_or_404(SchoolUser, user=request.user)

    grades = Grade.objects.select_related('task_id').filter(
        number__isnull=True,
        task_id__teacher_id=schooluser.id
    ).order_by('task_id__due_date')

    return render(request, 'teachers_list.html', {
        'schooluser': schooluser,
        'grades': grades
    })


def teachers_submit(request, grade_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login-user')

    grade = get_object_or_404(Grade, id=grade_id)
    schooluser = get_object_or_404(SchoolUser, user=request.user)

    if grade.task_id.teacher_id.id != schooluser.id or grade.number is not None:
        return redirect('teachers-list')

    if request.method == 'POST':
        form = TeachersSubmissionForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.save()
            return redirect('teachers-list')
    else:
        form = TeachersSubmissionForm()

    return render(request, 'teachers_submit.html', {
        'schooluser': schooluser,
        'form': form,
        'grade': grade
    })


def teachers_create(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login-user')

    schooluser = get_object_or_404(SchoolUser, user=request.user)

    if request.method == 'POST':
        form = TeachersCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.teacher_id = schooluser
            task.save()
            return redirect('teachers-list')
    else:
        form = TeachersCreateForm()

    return render(request, 'teachers_create.html', {
        'schooluser': schooluser,
        'form': form
    })
```