from rest_framework_nested import routers
from . import views
from django.urls import path, include

router = routers.DefaultRouter()

router.register('users', views.UserViewSet)
router.register('habits', views.HabitViewSet, basename='habits')
router.register('habitcompletedates', views.HabitCompleteDateViewSet)
router.register('users/me/habits', views.UserHabitsViewSet, basename='user-habits')

users_router = routers.NestedDefaultRouter(router, 'users', lookup='user')
users_router.register('habits', views.UserHabitsAdminViewSet, basename='user-habits-admin')

habits_router = routers.NestedDefaultRouter(router, 'users/me/habits', lookup='habit')
habits_router.register('dates', views.UserHabitDatesViewSet, basename='user-habit-dates')

urlpatterns = router.urls  + users_router.urls + habits_router.urls