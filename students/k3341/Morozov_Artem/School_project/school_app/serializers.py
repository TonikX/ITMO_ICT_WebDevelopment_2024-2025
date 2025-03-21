from rest_framework import serializers

from school_app.models import Group, Subject, Room, Teacher, Schedule, HomeTeacher, Student, LessonGrades, QuarterGrades


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    subject = SubjectSerializer()
    room = RoomSerializer()
    group = GroupSerializer()

    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class HomeTeacherSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    group = GroupSerializer()

    class Meta:
        model = HomeTeacher
        fields = '__all__'


class HomeTeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeTeacher
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class LessonGradesSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    schedule = ScheduleSerializer()

    class Meta:
        model = LessonGrades
        fields = '__all__'


class LessonGradesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonGrades
        fields = '__all__'


class LessonGradesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonGrades
        fields = 'grade'


class QuarterGradesSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = QuarterGrades
        fields = '__all__'


class QuarterGradesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterGrades
        fields = '__all__'


class QuarterGradesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterGrades
        fields = ['grade']


class SubjectTeacherCountSerializer(serializers.ModelSerializer):
    teacher_count = serializers.IntegerField()

    class Meta:
        model = Subject
        fields = ['subject_name', 'teacher_count']


class SubjectQuarterReportSerializer(serializers.ModelSerializer):
    average_grade = serializers.FloatField()
    total_students = serializers.IntegerField()

    class Meta:
        model = Subject
        fields = ['subject_name', 'average_grade', 'total_students']


class ClassReportSerializer(serializers.Serializer):
    class_name = serializers.CharField()
    class_teacher = serializers.CharField()
    total_students = serializers.IntegerField()
    subjects = SubjectQuarterReportSerializer(many=True)
