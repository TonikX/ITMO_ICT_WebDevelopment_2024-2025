from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PrintShop, Newspaper, PrintRun, Delivery
from .serializers import PrintShopSerializer, NewspaperSerializer, PrintRunSerializer, DeliverySerializer


# Newspaper API
class NewspaperList(APIView):
    def get(self, request):
        queryset = Newspaper.objects.all()
        serializer = NewspaperSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewspaperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewspaperDetail(APIView):
    def get(self, request, pk):
        try:
            newspaper = Newspaper.objects.get(pk=pk)
            serializer = NewspaperSerializer(newspaper)
            return Response(serializer.data)
        except Newspaper.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            newspaper = Newspaper.objects.get(pk=pk)
            newspaper.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Newspaper.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# PrintShop API
class PrintShopList(APIView):
    def get(self, request):
        queryset = PrintShop.objects.all()
        serializer = PrintShopSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PrintShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrintShopDetail(APIView):
    def get(self, request, pk):
        try:
            printshop = PrintShop.objects.get(pk=pk)
            serializer = PrintShopSerializer(printshop)
            return Response(serializer.data)
        except PrintShop.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            printshop = PrintShop.objects.get(pk=pk)
            printshop.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PrintShop.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# PrintRun API
class PrintRunList(APIView):
    def get(self, request):
        queryset = PrintRun.objects.all()
        serializer = PrintRunSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PrintRunSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrintRunDetail(APIView):
    def get(self, request, pk):
        try:
            printrun = PrintRun.objects.get(pk=pk)
            serializer = PrintRunSerializer(printrun)
            return Response(serializer.data)
        except PrintRun.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            printrun = PrintRun.objects.get(pk=pk)
            printrun.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PrintRun.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# Delivery API
class DeliveryList(APIView):
    def get(self, request):
        queryset = Delivery.objects.all()
        serializer = DeliverySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryDetail(APIView):
    def get(self, request, pk):
        try:
            delivery = Delivery.objects.get(pk=pk)
            serializer = DeliverySerializer(delivery)
            return Response(serializer.data)
        except Delivery.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            delivery = Delivery.objects.get(pk=pk)
            delivery.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Delivery.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
