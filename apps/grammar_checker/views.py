# apps/grammar_checker/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import GrammarCheck
from .serializers import GrammarCheckSerializer, GrammarRefinementSerializer
from .services import OpenAIService
from rest_framework.permissions import IsAuthenticated

class GrammarCheckerViewSet(viewsets.ModelViewSet):
    queryset = GrammarCheck.objects.all().order_by('-created_at')
    serializer_class = GrammarCheckSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def refine(self, request):
        serializer = GrammarRefinementSerializer(data=request.data)
        
        if serializer.is_valid():
            text = serializer.validated_data['text']
            
            try:
                # Call OpenAI API
                service = OpenAIService()
                refined_text = service.refine_text(text)
                
                # Save the check to the database
                grammar_check = GrammarCheck.objects.create(
                    original_text=text,
                    refined_text=refined_text
                )
                
                return Response({
                    'id': grammar_check.id,
                    'original_text': grammar_check.original_text,
                    'refined_text': grammar_check.refined_text,
                    'created_at': grammar_check.created_at
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        # Override create to automatically refine text
        instance = serializer.save()
        
        try:
            service = OpenAIService()
            refined_text = service.refine_text(instance.original_text)
            instance.refined_text = refined_text
            instance.save()
        except Exception as e:
            # Log the error but allow creation to proceed
            print(f"Error refining text: {str(e)}")