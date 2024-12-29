from django.db.models import Count, Prefetch
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from alpinist_club_app.models import Mountain, Club, Alpinist, Ascending, AscendingGroup, AlpinistInGroup
from alpinist_club_app.serializers import MountainSerializer, ClubSerializer, AlpinistSerializer, \
    AlpinistCreateSerializer, AscendingSerializer, AscendingCreateSerializer, AscendingGroupSerializer, \
    AscendingGroupCreateSerializer, AscendingGroupUpdateSerializer, AlpinistInGroupCreateSerializer, \
    AlpinistInGroupSerializer, AlpinistInGroupCreateWithGroupSerializer, AlpinistInGroupUpdateSerializer, \
    AscendingUpdateSerializer, AlpinistMountainCountSerializer, MountainReportSerializer


class MountainAPIVIew(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MountainSerializer

    def get(self, request):
        mountains = Mountain.objects.all()
        serializer = MountainSerializer(mountains, many=True)
        return Response({"Mountains": serializer.data})

    def post(self, request):
        name = request.data['name']
        height = request.data['height']
        country = request.data['country']
        district = request.data['district']
        mountain = dict(name=name, height=height, country=country, district=district)
        serializer = MountainSerializer(data=mountain)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Mountain created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MountainUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Mountain.objects.all()
    serializer_class = MountainSerializer
    lookup_field = 'id'


class MountainRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Mountain.objects.all()
    serializer_class = MountainSerializer
    lookup_field = 'id'


class ClubAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClubSerializer

    def get(self, request):
        clubs = Club.objects.all()
        serializer = ClubSerializer(clubs, many=True)
        return Response({"Clubs": serializer.data})


class AlpinistAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AlpinistCreateSerializer

    def get(self, request):
        alpinists = Alpinist.objects.all()
        serializer = AlpinistSerializer(alpinists, many=True)
        return Response({"Alpinists": serializer.data})

    def post(self, request):
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        patronymic = request.data['patronymic']
        club = request.data['club']
        alpinist = dict(first_name=first_name, last_name=last_name, patronymic=patronymic, club=club)
        serializer = AlpinistCreateSerializer(data=alpinist)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Alpinist '{}' created succesfully.".format(alpinist['first_name'])},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlpinistUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Alpinist.objects.all()
    serializer_class = AlpinistCreateSerializer
    lookup_field = 'id'


class AlpinistRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AlpinistSerializer
    queryset = Alpinist.objects.all()
    lookup_field = 'id'


class AscendingAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AscendingCreateSerializer

    def get(self, request):
        ascendings = Ascending.objects.all()
        serializer = AscendingSerializer(ascendings, many=True)
        return Response({"Ascendings": serializer.data})

    def post(self, request):
        description = request.data['description']
        planned_start_date = request.data['planned_start_date']
        planned_end_date = request.data['planned_end_date']
        mountain = request.data['mountain']

        ascending = dict(description=description, planned_start_date=planned_start_date,
                         planned_end_date=planned_end_date, mountain=mountain)
        serializer = AscendingCreateSerializer(data=ascending)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Ascending created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AscendingRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AscendingSerializer
    queryset = Ascending.objects.all()


class AscendingUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Ascending.objects.all()
    serializer_class = AscendingUpdateSerializer
    lookup_field = 'id'


class AscendingGroupAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AscendingGroupCreateSerializer

    def get(self, request):
        ascendings_group = AscendingGroup.objects.all()
        serializer = AscendingGroupSerializer(ascendings_group, many=True)
        return Response({"Ascending group": serializer.data})

    def post(self, request):
        ascending = request.data['ascending']
        ascending_group = dict(ascending=ascending)
        serializer = AscendingGroupCreateSerializer(data=ascending_group)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Ascending Group created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AscendingGroupRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AscendingGroupSerializer
    queryset = AscendingGroup.objects.all()
    lookup_field = 'id'


class AscendingGroupUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AscendingGroupUpdateSerializer
    queryset = AscendingGroup.objects.all()
    lookup_field = 'id'


class AlpinistInGroupAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AlpinistInGroupCreateSerializer

    def get(self, request, group_id):
        alpinists = AlpinistInGroup.objects.filter(ascending_group_id=group_id)
        serializer = AlpinistInGroupSerializer(alpinists, many=True)
        return Response({"Alpinists": serializer.data})

    def post(self, request, group_id):
        alpinist = request.data.get('alpinist')
        alpinist_in_group = dict(alpinist=alpinist, ascending_group_id=group_id)
        serializer = AlpinistInGroupCreateWithGroupSerializer(data=alpinist_in_group)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Alpinist was added to the group"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlpinistInGroupUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AlpinistInGroupUpdateSerializer
    queryset = AlpinistInGroup.objects.all()


class AlpinistInGroupRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AlpinistInGroupSerializer
    queryset = AlpinistInGroup.objects.all()


class AlpinistsAscendingInPeriodView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AlpinistSerializer

    @swagger_auto_schema(
        operation_description="Get information about alpinists, who were ascending in this room in specific period.",
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Start of period",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="End of period",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval", schema=AlpinistSerializer),
        }
    )
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        ascendings = Ascending.objects.filter(fact_start_date__gte=start_date, fact_end_date__lte=end_date)
        alpinists = set()
        for ascending in ascendings:
            ascending_group = AscendingGroup.objects.get(ascending=ascending)
            members = ascending_group.members.all()
            alpinists.update(members)
        serializer = AlpinistSerializer(alpinists, many=True)
        return Response({"Alpinists": serializer.data})


class AscendingsInPeriodView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AlpinistSerializer

    @swagger_auto_schema(
        operation_description="Get information about ascendings in specific period.",
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Start of period",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="End of period",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval", schema=AscendingSerializer),
        }
    )
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        ascendings = Ascending.objects.filter(fact_start_date__gte=start_date, fact_end_date__lte=end_date)
        serializer = AscendingSerializer(ascendings, many=True)
        return Response({"Ascendings": serializer.data})


class CountOfAlpinistsOnMountainsView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mountains_with_climber_count = Mountain.objects.annotate(
            total_climbers=Count('ascending__ascendinggroup__members', distinct=True)
        )

        data = [
            {
                "mountain": mountain.name,
                "total_climbers": mountain.total_climbers or 0
            }
            for mountain in mountains_with_climber_count
        ]

        return Response(data)


class MountainsWithoutAscendingsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MountainSerializer

    def get(self, request):
        mountains = Mountain.objects.filter(ascending__isnull=True)
        serializer = MountainSerializer(mountains, many=True)
        return Response(serializer.data)


class AlpinistMountainAscendingsView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        alpinist_ascendings = (
            AlpinistInGroup.objects
            .values('alpinist', 'ascending_group_id__ascending__mountain__name')
            .annotate(total_ascendings=Count('ascending_group_id'))
        )

        data = [
            {
                "alpinist": Alpinist.objects.get(id=entry['alpinist']),
                "mountain": entry['ascending_group_id__ascending__mountain__name'],
                "total_ascendings": entry['total_ascendings'],
            }
            for entry in alpinist_ascendings
        ]
        serializer = AlpinistMountainCountSerializer(data, many=True)
        return Response(serializer.data)


class ReportAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get report about ascendings in specific period.",
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Start of period",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="End of period",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval", schema=AscendingSerializer),
        }
    )

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')


        if not start_date or not end_date:
            return Response({"detail": "Both start_date and end_date are required."}, status=status.HTTP_400_BAD_REQUEST)

        mountains = Mountain.objects.filter(
            ascending__ascendinggroup__ascending__planned_start_date__gte=start_date,
            ascending__ascendinggroup__ascending__planned_end_date__lte=end_date
        ).distinct()

        report_data = []

        for mountain in mountains:
            ascending_groups = AscendingGroup.objects.filter(
                ascending__mountain=mountain,
                ascending__planned_start_date__gte=start_date,
                ascending__planned_end_date__lte=end_date
            ).order_by('ascending__planned_start_date')

            group_info = []
            for group in ascending_groups:
                member_count = AlpinistInGroup.objects.filter(ascending_group_id=group).count()

                success_count = AlpinistInGroup.objects.filter(ascending_group_id=group, result='s').count()
                failure_count = AlpinistInGroup.objects.filter(ascending_group_id=group, result='f').count()
                emergency_count = AlpinistInGroup.objects.filter(ascending_group_id=group, result='e').count()

                group_info.append({
                    'group': AscendingGroupSerializer(group).data,
                    'member_count': member_count,
                    'success_count': success_count,
                    'failure_count': failure_count,
                    'emergency_count': emergency_count,
                })

            report_data.append({
                'mountain': MountainSerializer(mountain).data,
                'groups': group_info,
            })

        return Response(report_data, status=status.HTTP_200_OK)