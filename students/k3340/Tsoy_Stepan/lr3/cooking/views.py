from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, RetrieveAPIView, \
    ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cooking.models import Meal, Step, Comment, Like
from cooking.permissions import IsAuthorOrReadonly, IsMealAuthorOrReadonly
from cooking.serializers import MealListSerializer, MealCreateSerializer, MealDetailSerializer, StepSerializer, \
    CommentSerializer, UserSerializer, LikeSerializer


class CustomMealPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


# Create your views here.
class index(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'message': 'Hello, World!',
            'authenticated?': request.user.is_authenticated,
            'staff?': request.user.is_staff,
        }, status=200)


class MealListCreateAPIView(ListCreateAPIView):
    queryset = Meal.objects.all()
    pagination_class = CustomMealPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'headline']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MealListSerializer
        return MealCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ingredients = serializer.validated_data.get("ingredients", [])
        serializer.validated_data["ingredients"] = list(map(str, ingredients))

        serializer.validated_data["author"] = request.user

        meal = serializer.save()

        return Response(MealDetailSerializer(meal).data, status=201)


class MealDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadonly]
    queryset = Meal.objects.all()
    serializer_class = MealDetailSerializer
    lookup_field = 'pk'


class StepListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsMealAuthorOrReadonly]
    serializer_class = StepSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['meal'] = get_object_or_404(Meal, pk=self.kwargs['pk'])

        step = serializer.save()

        return Response(StepSerializer(step).data, status=201)

    def get_queryset(self):
        return Step.objects.filter(meal_id=self.kwargs['pk'])


class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(meal_id=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        if Comment.objects.filter(meal_id=self.kwargs['pk'], author=request.user).exists():
            return Response("You already have a comment", status=409)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['author'] = request.user
        serializer.validated_data['meal'] = get_object_or_404(Meal, pk=self.kwargs['pk'])

        comment = serializer.save()
        return Response(CommentSerializer(comment).data, status=201)


class LikeView(APIView):
    def get(self, request, pk):
        obj, status = Like.objects.get_or_create(meal_id=pk, user=request.user)

        return Response(obj.status, 200)

    def post(self, request, pk):
        obj, status = Like.objects.get_or_create(meal_id=pk, user=request.user)
        obj.status = not obj.status
        obj.save()

        return Response(obj.status, 200)


class AccountView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MyRecipesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MealListSerializer
    pagination_class = CustomMealPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'headline']

    def get_queryset(self):
        return Meal.objects.filter(author=self.request.user)


class MyCommentsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class MyLikesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user, status=True)


class can_edit(APIView):
    def get(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Meal, pk=pk)
        return Response(recipe.author == request.user or request.user.is_superuser, 200)
