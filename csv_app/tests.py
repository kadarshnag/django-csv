from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import User
import io, csv

class CSVUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_csv_upload(self):
        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(["name", "email", "age"])
        writer.writerow(["John Doe", "john@example.com", "25"])
        csv_data.seek(0)

        csv_file = SimpleUploadedFile("test.csv", csv_data.getvalue().encode('utf-8'), content_type="text/csv")
        response = self.client.post('/api/upload/', {'file': csv_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
