from rest_framework import serializers
from .models import Editor, Newspaper, PrintShop, PostOffice, PrintRun, Delivery

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

class PrintRunSerializer(serializers.ModelSerializer):
    newspaper = NewspaperSerializer(read_only=True)
    newspaper_id = serializers.PrimaryKeyRelatedField(
        queryset=Newspaper.objects.all(), source='newspaper', write_only=True
    )
    printshop = PrintShopSerializer(read_only=True)
    printshop_id = serializers.PrimaryKeyRelatedField(
        queryset=PrintShop.objects.all(), source='printshop', write_only=True
    )

    class Meta:
        model = PrintRun
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    print_run = PrintRunSerializer(read_only=True)
    print_run_id = serializers.PrimaryKeyRelatedField(
        queryset=PrintRun.objects.all(), source='print_run', write_only=True
    )
    post_office = PostOfficeSerializer(read_only=True)
    post_office_id = serializers.PrimaryKeyRelatedField(
        queryset=PostOffice.objects.all(), source='post_office', write_only=True
    )
    printshop = PrintShopSerializer(read_only=True)
    printshop_id = serializers.PrimaryKeyRelatedField(
        queryset=PrintShop.objects.all(), source='printshop', write_only=True
    )

    class Meta:
        model = Delivery
        fields = '__all__'