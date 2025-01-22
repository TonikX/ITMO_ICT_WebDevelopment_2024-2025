import random

from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView, \
    ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Workout, Done, Comment, Routine, Favorite
from .permissions import IsAuthorOrReadOnly
from .serializers import WorkoutDetailSerializer, WorkoutListSerializer, CommentListSerializer, RoutineSerializer, \
    RoutineListSerializer, CustomUserSerializer


# Create your views here.
class IndexView(APIView):
    def get(self, request):
        return Response({"Everything": "workouts"})


class ListCreateWorkouts(ListCreateAPIView):
    queryset = Workout.objects.all()

    def get_serializer_class(self):
        # sleep(2)
        if self.request.method == 'POST':
            return WorkoutDetailSerializer
        return WorkoutListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class canEdit(APIView):
    def get(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        return Response(workout.author == request.user)


class WorkoutDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]


class MarkWorkoutDoneApiView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(False)

        workout = get_object_or_404(Workout, pk=pk)
        done_obj = Done.objects.filter(user=self.request.user, workouts=workout)

        if done_obj.exists():
            return Response(True)
        return Response(False)

    def post(self, request, pk, *args, **kwargs):
        workout = get_object_or_404(Workout, pk=pk)
        user = request.user

        done_obj, created = Done.objects.get_or_create(user=user, workouts=workout)

        if not created:
            done_obj.delete()
            return Response({"Success": f"Marked {workout.title} workout as not done"})
        return Response({"detail": f"Workout {workout.title} marked as done."})


class MarkWorkoutFavoriteApiView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(False)

        workout = get_object_or_404(Workout, pk=pk)
        fav_obj = Favorite.objects.filter(user=self.request.user, workouts=workout)

        if fav_obj.exists():
            return Response(True)
        return Response(False)

    def post(self, request, pk, *args, **kwargs):
        workout = get_object_or_404(Workout, pk=pk)
        user = request.user

        fav_obj, created = Favorite.objects.get_or_create(user=user, workouts=workout)

        if not created:
            fav_obj.delete()
            return Response({"Success": f"Marked {workout.title} workout as not favorite"})
        return Response({"detail": f"Workout {workout.title} marked as favorite"})


class RandomWorkoutView(RetrieveAPIView):
    serializer_class = WorkoutDetailSerializer

    def get_object(self):
        workout_ids = Workout.objects.values_list('id', flat=True)
        if not workout_ids:
            raise NotFound("No workouts available.")
        random_id = random.choice(workout_ids)
        return Workout.objects.get(id=random_id)


class CommentListView(ListCreateAPIView):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        workout = get_object_or_404(Workout, pk=self.kwargs['pk'])
        return Comment.objects.filter(workout=workout)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, workout=get_object_or_404(Workout, pk=self.kwargs['pk']))


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Comment.objects.all()


class RoutineListView(ListCreateAPIView):
    serializer_class = RoutineSerializer
    queryset = Routine.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RoutineSerializer
        return RoutineListSerializer


class RoutineDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoutineSerializer
    queryset = Routine.objects.all()
    permission_classes = [IsAuthorOrReadOnly]


class AccountView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


class AccountDoneWorkoutView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkoutListSerializer

    def get_queryset(self):
        return Workout.objects.filter(done__user=self.request.user).distinct()


class AccountFavoriteWorkoutView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkoutListSerializer

    def get_queryset(self):
        return Workout.objects.filter(favorite__user=self.request.user).distinct()


class AccountCommentsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentListSerializer

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class AccountPosts(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkoutDetailSerializer

    def get_queryset(self):
        return Workout.objects.filter(author=self.request.user).distinct()