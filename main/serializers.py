from rest_framework import serializers
from .models import User, Habit, HabitCompleteDate
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password']

  
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email']


class HabitCompleteDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitCompleteDate
        fields = ['id', 'complete_date', 'habit']

class HabitDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitCompleteDate
        fields = ['id', 'complete_date']

    def create(self, validated_data):
        habit_id = self.context['habit_id']
        return HabitCompleteDate.objects.create(habit_id=habit_id, **validated_data)


class HabitSerializer(serializers.ModelSerializer):
    habit_complete_dates = HabitDateSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Habit
        fields = ['id', 'habit', 'user_id', 'created', 'updated', 'habit_complete_dates']

class PostHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['habit']

    def create(self, validated_data):
        user = self.context['user']
        return Habit.objects.create(user_id=user, **validated_data)

