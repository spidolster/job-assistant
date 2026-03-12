import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from job_assistant.backend.main import app


class TestPhase3API(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    @patch('job_assistant.backend.main.get_api_key', return_value='dummy')
    @patch('job_assistant.backend.main.get_resume_text_from_db', return_value='resume text')
    @patch('job_assistant.backend.main.analyze_resume_vs_jd', return_value='Match Score: 85%')
    @patch('job_assistant.backend.main.extract_company_and_role', return_value={'company': 'Acme', 'role': 'Data Analyst'})
    @patch('job_assistant.backend.main.extract_match_score', return_value=85)
    @patch('job_assistant.backend.main.extract_salary_range', return_value='Rp10.000.000 - Rp15.000.000')
    @patch('job_assistant.backend.main.save_application', return_value=123)
    def test_analyze_success(
        self,
        _save_application,
        _extract_salary,
        _extract_score,
        _extract_company,
        _analyze,
        _resume_text,
        _api_key,
    ):
        payload = {
            'jd_text': 'Some JD text',
            'provider': 'openai',
            'model_name': 'gpt-4o-mini',
            'resume_id': 1,
            'save_to_tracker': True,
        }

        response = self.client.post('/analyze', json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body['company'], 'Acme')
        self.assertEqual(body['role'], 'Data Analyst')
        self.assertEqual(body['match_score'], 85)
        self.assertEqual(body['tracker_id'], 123)

    @patch('job_assistant.backend.main.get_api_key', return_value='')
    def test_analyze_requires_api_key(self, _api_key):
        response = self.client.post(
            '/analyze',
            json={'jd_text': 'JD text', 'provider': 'openai', 'resume_text': 'resume text'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('API key', response.json()['detail'])


if __name__ == '__main__':
    unittest.main()
