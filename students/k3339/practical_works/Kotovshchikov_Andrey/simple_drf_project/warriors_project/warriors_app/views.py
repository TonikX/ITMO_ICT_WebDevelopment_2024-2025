from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from warriors_app.models import Warrior, Skill
from warriors_app.serializers import (
    ProfessionSerializer,
    SkillSerializer,
    WarriorDetailSerializer,
    WarriorSerializer,
    WarriorWithProfessionSerializer,
    WarriorWithSkillSerializer,
)


class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorWithProfessionView(generics.ListAPIView):
    serializer_class = WarriorWithProfessionSerializer
    queryset = Warrior.objects.select_related("profession").all()


class WarriorWithSkillView(generics.ListAPIView):
    serializer_class = WarriorWithSkillSerializer
    queryset = Warrior.objects.prefetch_related("skill").all()


class WarriorDetailView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = WarriorDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        warrior = (
            Warrior.objects.select_related("profession")
            .prefetch_related("skill")
            .filter(id=self.kwargs[self.lookup_field])
            .first()
        )

        if warrior is None:
            raise NotFound()

        return warrior


class ProfessionCreateView(APIView):
    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionSerializer(data=profession)

        serializer.is_valid(raise_exception=True)
        profession_saved = serializer.save()

        return Response(
            data={
                "Success": f"Profession '{profession_saved.title}' created succesfully."
            }
        )


class SkillView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(data={"skills": serializer.data})

    def post(self, request):
        skill = request.data.get("skill")
        serializer = SkillSerializer(data=skill)

        serializer.is_valid(raise_exception=True)
        saved_skill = serializer.save()

        return Response(
            data={
                "Success": f"skill '{saved_skill.title}' created succesfully.",
            }
        )
