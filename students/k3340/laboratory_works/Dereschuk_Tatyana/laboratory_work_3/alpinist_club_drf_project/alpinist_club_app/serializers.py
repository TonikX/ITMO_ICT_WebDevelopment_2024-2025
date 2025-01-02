from rest_framework import serializers

from alpinist_club_app.models import Mountain, Club, Alpinist, Ascending, AscendingGroup, AlpinistInGroup


class MountainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mountain
        fields = '__all__'


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'


class AlpinistSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Alpinist
        fields = '__all__'


class AlpinistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alpinist
        fields = '__all__'


class AscendingSerializer(serializers.ModelSerializer):
    mountain = MountainSerializer(read_only=True)

    class Meta:
        model = Ascending
        fields = '__all__'


class AscendingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ascending
        fields = ['fact_start_date', 'fact_end_date']


class AscendingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ascending
        fields = ['description', 'planned_start_date', 'planned_end_date', 'mountain']


class AscendingGroupSerializer(serializers.ModelSerializer):
    ascending = AscendingSerializer(read_only=True)
    members = AlpinistSerializer(many=True, read_only=True)

    class Meta:
        model = AscendingGroup
        fields = '__all__'


class AscendingGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AscendingGroup
        fields = ['ascending']


class AscendingGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AscendingGroup
        fields = ['group_result', 'description_of_result']


class AlpinistInGroupSerializer(serializers.ModelSerializer):
    ascending_group = AscendingGroupSerializer(read_only=True)
    alpinist = AlpinistSerializer(read_only=True)

    class Meta:
        model = AlpinistInGroup
        fields = '__all__'


class AlpinistInGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlpinistInGroup
        fields = ['alpinist']

class AlpinistInGroupCreateWithGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlpinistInGroup
        fields = ['alpinist', 'ascending_group_id']


class AlpinistInGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlpinistInGroup
        fields = ['result', 'emergency_situations']


class AlpinistMountainCountSerializer(serializers.ModelSerializer):
    total_ascendings = serializers.IntegerField()
    mountain = serializers.CharField()
    alpinist = AlpinistSerializer(read_only=True)

    class Meta:
        model = AlpinistInGroup
        fields = ['alpinist', 'mountain', 'total_ascendings']


class AscendingGroupReportSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()

    def get_members_count(self, obj):
        return obj.members.count()

    class Meta:
        model = AscendingGroup
        fields = ['ascending', 'members_count']

class AscendingReportSerializer(serializers.ModelSerializer):
    ascending_groups = AscendingGroupReportSerializer(many=True, read_only=True)

    class Meta:
        model = Ascending
        fields = ['mountain', 'planned_start_date', 'planned_end_date', 'ascending_groups']

class MountainReportSerializer(serializers.ModelSerializer):
    ascendings = AscendingReportSerializer(many=True, read_only=True)

    class Meta:
        model = Mountain
        fields = ['name', 'ascendings']