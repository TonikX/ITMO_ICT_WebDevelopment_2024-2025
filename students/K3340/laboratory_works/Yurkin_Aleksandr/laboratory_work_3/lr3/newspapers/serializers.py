from rest_framework import serializers
from .models import Editor, Newspaper, PrintShop, PostOffice, Distribution

class EditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = '__all__'

class NewspaperSerializer(serializers.ModelSerializer):
    editor = EditorSerializer(read_only=True)
    editor_id = serializers.PrimaryKeyRelatedField(
        queryset=Editor.objects.all(), source='editor', write_only=True
    )

    class Meta:
        model = Newspaper
        fields = '__all__'

class PrintShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintShop
        fields = '__all__'

class PostOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOffice
        fields = '__all__'

class DistributionSerializer(serializers.ModelSerializer):
    postoffice = PostOfficeSerializer(read_only=True)
    postoffice_id = serializers.PrimaryKeyRelatedField(
        queryset=PostOffice.objects.all(), source='postoffice', write_only=True
    )
    newspaper = NewspaperSerializer(read_only=True)
    newspaper_id = serializers.PrimaryKeyRelatedField(
        queryset=Newspaper.objects.all(), source='newspaper', write_only=True
    )
    printshop = PrintShopSerializer(read_only=True)
    printshop_id = serializers.PrimaryKeyRelatedField(
        queryset=PrintShop.objects.all(), source='printshop', write_only=True
    )

    class Meta:
        model = Distribution
        fields = '__all__'
