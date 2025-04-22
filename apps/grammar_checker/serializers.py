from rest_framework import serializers
from .models import GrammarCheck

class GrammarCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarCheck
        fields = ['id', 'original_text', 'refined_text', 'created_at']
        read_only_fields = ['refined_text', 'created_at']

class GrammarRefinementSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)