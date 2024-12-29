from rest_framework import serializers

from head_teacher_app import models


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    assigned_room_id = serializers.PrimaryKeyRelatedField(queryset=models.Room.objects.all(), source="assigned_room", allow_null=True)
    assigned_room = RoomSerializer(read_only=True)

    class Meta:
        model = models.Teacher
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = "__all__"


class ClassSerializer(serializers.ModelSerializer):
    homeroom_teacher_id = serializers.PrimaryKeyRelatedField(queryset=models.Teacher.objects.all(), source="homeroom_teacher")
    homeroom_teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = models.Class
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    student_class_id = serializers.PrimaryKeyRelatedField(queryset=models.Class.objects.all(), source="student_class")
    student_class = ClassSerializer(read_only=True)

    class Meta:
        model = models.Student
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    student_class_id = serializers.PrimaryKeyRelatedField(queryset=models.Class.objects.all(), source="student_class")
    student_class = ClassSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=models.Subject.objects.all(), source="subject")
    subject = SubjectSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(queryset=models.Teacher.objects.all(), source="teacher")
    teacher = TeacherSerializer(read_only=True)
    room_number_id = serializers.PrimaryKeyRelatedField(queryset=models.Room.objects.all(), source="room_number")
    room_number = RoomSerializer(read_only=True)

    class Meta:
        model = models.Schedule
        fields = "__all__"


class GradeSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(queryset=models.Student.objects.all(), source="student")
    student = StudentSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=models.Subject.objects.all(), source="subject")
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = models.Grade
        fields = "__all__"


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
