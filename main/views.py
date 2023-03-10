from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import User, Habit, HabitCompleteDate
from .serializers import UserSerializer, UserHabitSerializer, AdminHabitSerializer, HabitCompleteDateSerializer, PostHabitSerializer, HabitDateSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
import calendar
from pprint import pprint

# Create your views here.

class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = User.objects.get(id=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class HabitViewSet(ModelViewSet):
    serializer_class = AdminHabitSerializer
    permission_classes = [IsAdminUser]
    queryset = Habit.objects.all()


class UserHabitsViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]

    def get_serializer_context(self):
        return {'user': self.request.user.id}
    
    def get_queryset(self):
        user = self.request.user.id
        queryset = Habit.objects.filter(user=user)

        date = self.request.query_params.get('date')
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        habit_status = self.request.query_params.get('status')

        if date is not None and habit_status is not None:
            if habit_status == 'complete':
                queryset = queryset.filter(habit_complete_dates__complete_date=date).distinct()
            elif habit_status == 'incomplete':
                queryset = queryset.exclude(habit_complete_dates__complete_date=date)

        elif month is not None and year is not None:
            month = int(month)
            year = int(year)
            start_date = f'{year}-{month}-01'
            (first_weekday, last_day_of_month) = calendar.monthrange(year, month)
            end_date = f'{year}-{month}-{last_day_of_month}'

            queryset = queryset.filter(habit_complete_dates__complete_date__gte=start_date, habit_complete_dates__complete_date__lte=end_date).distinct()

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostHabitSerializer
        return UserHabitSerializer

    def create(self, request, *args, **kwargs):
        serializer = PostHabitSerializer(data=request.data, context={'user': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        habit = serializer.save()
        serializer = UserHabitSerializer(habit)
        return Response(serializer.data)


class UserHabitsAdminViewSet(ModelViewSet):
    serializer_class = AdminHabitSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Habit.objects.filter(user=self.kwargs['user_pk'])


class HabitCompleteDateViewSet(ModelViewSet):
    queryset = HabitCompleteDate.objects.all()
    serializer_class = HabitCompleteDateSerializer
    permission_classes = [IsAdminUser]


class UserHabitDatesViewSet(ModelViewSet):
    serializer_class = HabitDateSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        habit_id = self.kwargs['habit_pk']
        queryset =  HabitCompleteDate.objects.filter(habit=habit_id)

        date = self.request.query_params.get('date')

        if date is not None:
            queryset = queryset.filter(habit=habit_id ,complete_date=date)

        return queryset

    def get_serializer_context(self):
        return {'habit_id': self.kwargs['habit_pk']}



class UserCompleteDatesViewSet(ModelViewSet):
    serializer_class = HabitCompleteDateSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.id
        queryset =  HabitCompleteDate.objects.filter(habit__user=user)

        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        if month is not None and year is not None:
            month = int(month)
            year = int(year)
            start_date = f'{year}-{month}-01'
            (first_weekday, last_day_of_month) = calendar.monthrange(year, month)
            end_date = f'{year}-{month}-{last_day_of_month}'

            queryset = queryset.filter(complete_date__gte=start_date, complete_date__lte=end_date)

        return queryset


