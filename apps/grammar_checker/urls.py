# apps/grammar_checker/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GrammarCheckerViewSet

router = DefaultRouter()
router.register('', GrammarCheckerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]