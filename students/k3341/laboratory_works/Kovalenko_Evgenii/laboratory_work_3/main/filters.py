import django_filters
from .models import Group, Student, Teacher, Subject, Schedule, Grade


class GroupFilter(django_filters.FilterSet):
    course = django_filters.NumberFilter(field_name='course')
    course_min = django_filters.NumberFilter(field_name='course', lookup_expr='gte')
    course_max = django_filters.NumberFilter(field_name='course', lookup_expr='lte')

    class Meta:
        model = Group
        fields = ['course']


class StudentFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    group = django_filters.NumberFilter(field_name='group_id')
    status = django_filters.CharFilter(field_name='status')
    course = django_filters.NumberFilter(field_name='group__course')

    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'group', 'status', 'course']


class TeacherFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    position = django_filters.CharFilter(lookup_expr='icontains')
    has_classroom = django_filters.BooleanFilter(
        field_name='classroom',
        lookup_expr='isnull',
        exclude=True
    )

    class Meta:
        model = Teacher
        fields = ['last_name', 'first_name', 'position']


class SubjectFilter(django_filters.FilterSet):
    subject_name = django_filters.CharFilter(lookup_expr='icontains')
    subject_code = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Subject
        fields = ['subject_name', 'subject_code']


class ScheduleFilter(django_filters.FilterSet):
    group = django_filters.NumberFilter(field_name='group_id')
    teacher = django_filters.NumberFilter(field_name='teacher_id')
    subject = django_filters.NumberFilter(field_name='subject_id')
    day_of_week = django_filters.NumberFilter(field_name='day_of_week')
    semester = django_filters.NumberFilter(field_name='semester')
    academic_year = django_filters.NumberFilter(field_name='academic_year')

    class Meta:
        model = Schedule
        fields = ['group', 'teacher', 'subject', 'day_of_week', 'semester', 'academic_year']


class GradeFilter(django_filters.FilterSet):
    student = django_filters.NumberFilter(field_name='student_id')
    subject = django_filters.NumberFilter(field_name='subject_id')
    teacher = django_filters.NumberFilter(field_name='teacher_id')
    semester = django_filters.NumberFilter(field_name='semester')
    academic_year = django_filters.NumberFilter(field_name='academic_year')
    grade_value_min = django_filters.NumberFilter(field_name='grade_value', lookup_expr='gte')
    grade_value_max = django_filters.NumberFilter(field_name='grade_value', lookup_expr='lte')

    class Meta:
        model = Grade
        fields = ['student', 'subject', 'teacher', 'semester', 'academic_year']