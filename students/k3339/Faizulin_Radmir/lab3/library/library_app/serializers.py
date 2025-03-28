from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'author']

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'


class CopySerializer(serializers.ModelSerializer):
    book = BookSerializer()
    hall = HallSerializer()
    class Meta:
        model = Copy
        fields = '__all__'


class CreateCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = '__all__'

class CopyShortSerializer(serializers.ModelSerializer):
    book = BookShortSerializer()
    class Meta:
        model = Copy
        fields = ['book']

class ReaderSerializer(serializers.ModelSerializer):
    hall = HallSerializer()
    education = serializers.CharField(source='get_education_display')

    class Meta:
        model = Reader
        fields = '__all__'


class CreateReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'


class EducationSerializer(serializers.Serializer):
    education = serializers.CharField()
    education_name = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()

    def get_education_name(self, object):
        return dict(Reader.EDUCATIONS).get(object['education'], object['education'])

    def get_percentage(self, object):
        readers_cnt = Reader.objects.count()
        education_cnt = Reader.objects.filter(education=object['education']).count()
        return (education_cnt / readers_cnt) * 100

    def create(self, validated_data):
        pass


class ReaderShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ['name', 'second_name', 'surname']


class AssignmentSerializer(serializers.ModelSerializer):
    copy = CopySerializer()
    reader = ReaderSerializer()

    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentShortSerializer(serializers.ModelSerializer):
    copy = CopyShortSerializer()

    class Meta:
        model = Assignment
        fields = ['copy']


class AssignmentDebtorSerializer(serializers.ModelSerializer):
    reader = ReaderShortSerializer()

    class Meta:
        model = Assignment
        fields = ['reader']


class CreateAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'