from django.db.models import Count, F, Q
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Owner, Dog, Show, Participation, Expert, Grade
from .serializers import (
    OwnerSerializer, DogSerializer, ShowSerializer,
    ParticipationSerializer, ExpertSerializer, GradeSerializer
)


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['last_name', 'first_name', 'patronymic', 'contact_info']
    ordering_fields = ['last_name', 'first_name']

    @action(detail=True, methods=['get'])
    def rings(self, request, pk=None):
        owner = self.get_object()
        participations = Participation.objects.filter(
            dog__owner=owner,
            medical_exam_passed=True,
            payment_made=True
        ).select_related('show', 'dog')

        data = []
        for participation in participations:
            show = participation.show
            ring_info = show.ring_schedule
            data.append({
                'show_name': show.name,
                'dog_name': participation.dog.name,
                'ring_info': ring_info,
            })
        return Response(data)


class DogViewSet(viewsets.ModelViewSet):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'breed', 'owner__first_name', 'owner__last_name', 'club_name']
    ordering_fields = ['age', 'name']

    @action(detail=True, methods=['post'])
    def disqualify(self, request, pk=None):
        dog = self.get_object()
        dog.disqualified = True
        dog.save()
        return Response({'status': f'Собака {dog.name} дисквалифицирована'})

    @action(detail=False, methods=['get'])
    def by_club(self, request):
        club_name = request.query_params.get('club_name')
        if club_name:
            breeds = Dog.objects.filter(club_name=club_name).values('breed').distinct()
            return Response({'club_name': club_name, 'breeds': list(breeds)})
        else:
            return Response({'status': 'Параметр "club_name" обязателен'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def disqualified_count(self, request):
        count = Dog.objects.filter(disqualified=True).count()
        return Response({'disqualified_dogs_count': count})

    @action(detail=False, methods=['get'])
    def participants_by_breed(self, request):
        participants = Participation.objects.filter(
            medical_exam_passed=True,
            payment_made=True
        ).values('dog__breed').annotate(count=Count('dog')).order_by('-count')
        return Response(list(participants))


class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'type', 'location', 'sponsor']
    ordering_fields = ['date', 'name']

    @action(detail=True, methods=['post'])
    def add_expert(self, request, pk=None):
        show = self.get_object()
        expert_id = request.data.get('expert_id')
        try:
            expert = Expert.objects.get(id=expert_id)
            show.experts.add(expert)
            return Response({'status': f'Эксперт {expert.first_name} {expert.last_name} добавлен к выставке {show.name}'})
        except Expert.DoesNotExist:
            return Response({'status': 'Эксперт не найден'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_expert(self, request, pk=None):
        show = self.get_object()
        expert_id = request.data.get('expert_id')
        try:
            expert = Expert.objects.get(id=expert_id)
            show.experts.remove(expert)
            return Response({'status': f'Эксперт {expert.first_name} {expert.last_name} удален с выставки {show.name}'})
        except Expert.DoesNotExist:
            return Response({'status': 'Эксперт не найден'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        show = self.get_object()
        participations = Participation.objects.filter(show=show)
        total_participants = participations.count()
        breeds = participations.values('dog__breed').distinct()
        breed_counts = participations.values('dog__breed').annotate(count=Count('dog__breed'))
        medals_by_breed = participations.values('dog__breed', 'medal').annotate(count=Count('medal'))

        data = {
            'total_participants': total_participants,
            'breeds': list(breeds),
            'participants_by_breed': list(breed_counts),
            'medals_by_breed': list(medals_by_breed),
        }
        return Response(data)


class ParticipationViewSet(viewsets.ModelViewSet):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['dog__name', 'show__name', 'participation_type']
    ordering_fields = ['created_at']

    @action(detail=False, methods=['get'])
    def ring_by_owner(self, request):
        owner_id = request.query_params.get('owner_id')
        if owner_id:
            participations = Participation.objects.filter(
                dog__owner__id=owner_id,
                medical_exam_passed=True,
                payment_made=True
            ).select_related('show', 'dog')

            data = []
            for participation in participations:
                show = participation.show
                ring_info = show.ring_schedule
                data.append({
                    'show_name': show.name,
                    'dog_name': participation.dog.name,
                    'ring_info': ring_info,
                })
            return Response(data)
        else:
            return Response({'status': 'Параметр "owner_id" обязателен'}, status=status.HTTP_400_BAD_REQUEST)


class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['last_name', 'first_name', 'club_name']
    ordering_fields = ['last_name', 'first_name']

    @action(detail=False, methods=['get'])
    def by_breed(self, request):
        breed = request.query_params.get('breed')
        if breed:
            experts = Expert.objects.filter(rings_assigned__icontains=breed)
            serializer = self.get_serializer(experts, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'Параметр "breed" обязателен'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def replace(self, request, pk=None):
        expert = self.get_object()
        new_expert_id = request.data.get('new_expert_id')
        show_id = request.data.get('show_id')
        try:
            new_expert = Expert.objects.get(id=new_expert_id)
            show = Show.objects.get(id=show_id)
            show.experts.remove(expert)
            show.experts.add(new_expert)
            return Response({
                'status': f'Эксперт {expert.first_name} {expert.last_name} заменен на {new_expert.first_name} {new_expert.last_name} в выставке {show.name}'
            })
        except (Expert.DoesNotExist, Show.DoesNotExist):
            return Response({'status': 'Эксперт или выставка не найдены'}, status=status.HTTP_404_NOT_FOUND)


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['expert__first_name', 'expert__last_name', 'participation__dog__name']
    ordering_fields = ['score']

    @action(detail=False, methods=['get'])
    def top_dogs(self, request):
        grades = Grade.objects.values(
            'participation__dog__breed',
            'participation__dog__name'
        ).annotate(
            total_score=Count('score')
        ).order_by('-total_score')

        return Response(list(grades))
