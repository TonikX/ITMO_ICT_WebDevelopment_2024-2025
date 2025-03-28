from datetime import timedelta, datetime
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from django.db.models import Q
from django.db.models import Count, Subquery
from rest_framework.views import APIView

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class HallListView(generics.ListAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer


class HallRetrieveView(generics.RetrieveAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer


class HallUpdateView(generics.UpdateAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer


class HallCreateView(generics.CreateAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer


class CopyListView(generics.ListAPIView):
    queryset = Copy.objects.all()
    serializer_class = CopySerializer


class CopyRetrieveView(generics.RetrieveAPIView):
    queryset = Copy.objects.all()
    serializer_class = CopySerializer


class CopyUpdateView(generics.UpdateAPIView):
    queryset = Copy.objects.all()
    serializer_class = CreateCopySerializer


class CopyCreateView(generics.CreateAPIView):
    queryset = Copy.objects.all()
    serializer_class = CreateCopySerializer


class ReaderListView(generics.ListAPIView):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer


class ReaderRetrieveView(generics.RetrieveAPIView):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer


class ReaderUpdateView(generics.UpdateAPIView):
    queryset = Reader.objects.all()
    serializer_class = CreateReaderSerializer


class ReaderCreateView(generics.CreateAPIView):
    queryset = Reader.objects.all()
    serializer_class = CreateReaderSerializer

class ReaderRetrieveAssignmentsView(generics.ListAPIView):
    serializer_class = AssignmentShortSerializer

    def get_queryset(self):
        reader_id = self.kwargs['pk']
        assignment = Assignment.objects.filter(Q(reader__pk=reader_id) & Q(date_returned__isnull=True))
        return assignment


class ReadersRetrieveDebtorView(generics.ListAPIView):
    serializer_class = AssignmentDebtorSerializer

    def get_queryset(self):
        time = datetime.now()
        time -= timedelta(days=30)
        assignments = Assignment.objects.filter(date_assigned__lt=time)
        return assignments



class YoungReadersCountView(APIView):
    def get(self, request):
        time = datetime.now() - timedelta(days=365.25 * 20)
        readers = Reader.objects.filter(birth_date__gt=time).count()

        response = {'Readers under 20': readers}
        return Response(response)


class ReadersEducationCountView(APIView):
    def get(self, request):
        education = [{'education': cur[0]} for cur in Reader.EDUCATIONS]
        serializer = EducationSerializer(data=education, many=True)

        if serializer.is_valid():
            response = {'Education percentage': serializer.data}
            return Response(response)
        else:
            return Response(serializer.errors, status=400)

class AssignmentListView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class AssignmentRetrieveView(generics.RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class AssignmentUpdateView(generics.UpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = CreateAssignmentSerializer


class AssignmentCreateView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = CreateAssignmentSerializer