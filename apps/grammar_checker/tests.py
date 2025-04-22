# apps/grammar_checker/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import GrammarCheck
from unittest.mock import patch

User = get_user_model()

class GrammarCheckerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create a sample grammar check
        self.grammar_check = GrammarCheck.objects.create(
            original_text="This is test text with errors.",
            refined_text="This is test text without errors."
        )
        
        self.refine_url = reverse('grammarchecker-refine')
        
    def test_list_grammar_checks(self):
        response = self.client.get('/api/v1/grammar/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    @patch('apps.grammar_checker.services.OpenAIService.refine_text')
    def test_refine_text(self, mock_refine_text):
        mock_refine_text.return_value = "Refined text example."
        
        data = {'text': 'Text with grammatical errors.'}
        response = self.client.post(self.refine_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['refined_text'], "Refined text example.")
        self.assertEqual(GrammarCheck.objects.count(), 2)
        
        mock_refine_text.assert_called_once_with('Text with grammatical errors.')