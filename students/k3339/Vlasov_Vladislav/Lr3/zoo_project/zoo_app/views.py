from django.db.models import Count, Sum, Value
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from .models import *
from .serializers import *


class CountPetsInDepartAPIView(APIView):
    def get(self, request):
        departs = Pet.objects.values("valliere__building__depart").annotate(Count("number"))
        serializer = CountPetsInDepartSerializer(departs, many=True)
        return Response({"PetsInDepart": serializer.data})
    

class GetPetsAPIView(ListAPIView):
   serializer_class = PetSerializer
   queryset = Pet.objects.all()


class GetPetsInCommunalAPIView(ListAPIView):
   serializer_class = PetSerializer
   queryset = Pet.objects.filter(valliere__is_commun=True)


class GetPetsTogetherAPIView(ListAPIView):
   serializer_class = PetSerializer
   def get_queryset(self):
        pk = self.kwargs.get('pk')
        building = Pet.objects.get(number=pk).valliere.building.id
        return Pet.objects.filter(valliere__building__id=building).exclude(number=pk)
   

class GetEmptyValliersAPIView(ListAPIView):
    serializer_class = ValliereSerializer
    queryset = Valliere.objects.annotate(Count("pets")).filter(pets__count=0)


class GetPetsStateRent(APIView):
    def get(self, request):
        rents = Pet.objects.filter(is_rented="in").values("rent_pet__zoo").annotate(Count("number"), costs=Sum("rent_pet__price"))
        serializer = RentPetSummarySerializer(rents, many=True)
        return Response({"RentedPets": serializer.data})


class CreatePetAPIView(CreateAPIView):
    serializer_class = PetCreateSerializer
    queryset = Pet.objects.all()


class DeletePetAPIView(DestroyAPIView):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()


class UpdatePetAPIView(UpdateAPIView):
    serializer_class = PetCreateSerializer
    queryset = Pet.objects.all()

class GetReportOutRentAPIView(APIView):
    def get(self, request):
        pets_outrent_type = Pet.objects.filter(is_rented="out").values("animal_type").annotate(count_type=Count("number"), costs_type=Sum("rent_pet__price"))
        pets_outrent_zoo = Pet.objects.filter(is_rented="out").values("rent_pet__zoo").annotate(costs_zoo=Sum("rent_pet__price"))
        pets_outrent_all = Pet.objects.filter(is_rented="out").aggregate(num_all=Count("number"), cost_all=Sum("rent_pet__price"))

        #print(pets_outrent_report)
        serializer1 = RentOutTypePetSummarySerializer(pets_outrent_type, many=True)
        serializer2 = RentOutZooPetSummarySerializer(pets_outrent_zoo, many=True)
        serializer3 = RentOutAllPetSummarySerializer(pets_outrent_all)

        return Response({"RentedPets1": serializer1.data, "RentedPets2": serializer2.data, "RentedPets3": serializer3.data})
    

class ListDietAPIView(ListAPIView):
    serializer_class = DietSerializer
    queryset = Diet.objects.all()

class CreateDietAPIView(CreateAPIView):
    serializer_class = DietCudSerializer
    queryset = Diet.objects.all()


class DeleteDietAPIView(DestroyAPIView):
    serializer_class = DietCudSerializer
    queryset = Diet.objects.all()


class UpdateDietAPIView(UpdateAPIView):
    serializer_class = DietCudSerializer
    queryset = Diet.objects.all()


class ListHabitedAPIView(ListAPIView):
    serializer_class = HabitedSerializer
    queryset = Habited.objects.all()

class CreateHabitedAPIView(CreateAPIView):
    serializer_class = HabitedSerializer
    queryset = Habited.objects.all()


class DeleteHabitedAPIView(DestroyAPIView):
    serializer_class = HabitedSerializer
    queryset = Habited.objects.all()


class UpdateHabitedAPIView(UpdateAPIView):
    serializer_class = HabitedSerializer
    queryset = Habited.objects.all()


class ListProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()