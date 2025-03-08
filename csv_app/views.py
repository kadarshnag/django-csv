from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv
import io
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Upload a CSV file with user details.\n\n"
                              "**CSV Format:**\n"
                              "- `name`: Required, must be a non-empty string.\n"
                              "- `email`: Required, must be a valid email address.\n"
                              "- `age`: Required, must be a number between 0 and 120.",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Upload a CSV file with columns: name, email, age.",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="CSV processed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "summary": openapi.Schema(type=openapi.TYPE_OBJECT),
                        "errors": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                    },
                ),
            ),
            400: "Invalid file type or CSV format",
        },
    )
    def post(self, request):
        file = request.FILES.get("file")

        if not file or not file.name.endswith(".csv"):
            return Response({"error": "Oops! This doesn't look like a CSV file. Please upload a valid CSV file."}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = io.StringIO(file.read().decode("utf-8"))
        reader = csv.DictReader(decoded_file)

        if not reader.fieldnames or set(reader.fieldnames) != {"name", "email", "age"}:
            return Response(
                {"error": "Your file is missing some required columns. Please make sure it has 'name', 'email', and 'age'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_records, invalid_records = 0, 0
        errors = []
        seen_emails = set()
        users_to_create = []

        for row in reader:
            name, email, age = row.get("name", "").strip(), row.get("email", "").strip(), row.get("age", "").strip()

            if not name:
                errors.append({"row": row, "error": "A name is required. Please provide one."})
                invalid_records += 1
                continue

            if not email:
                errors.append({"row": row, "error": "Email is missing. Please enter a valid email address."})
                invalid_records += 1
                continue

            if email in seen_emails:
                errors.append({"row": row, "error": f"The email '{email}' appears more than once in the file. Each email must be unique."})
                invalid_records += 1
                continue

            try:
                validate_email(email)
            except ValidationError:
                errors.append({"row": row, "error": f"'{email}' is not a valid email address. Please check and try again."})
                invalid_records += 1
                continue

            if not age:
                errors.append({"row": row, "error": "Age is missing. Please provide a valid number."})
                invalid_records += 1
                continue

            try:
                age = int(age)
                if not (0 <= age <= 120):
                    raise ValueError
            except ValueError:
                errors.append({"row": row, "error": f"The age '{age}' is not valid. Age must be between 0 and 120."})
                invalid_records += 1
                continue

            if User.objects.filter(email=email).exists():
                errors.append({"row": row, "error": f"The email '{email}' is already in our database. Duplicate entries are not allowed."})
                invalid_records += 1
                continue

            seen_emails.add(email)
            users_to_create.append(User(name=name, email=email, age=age))
            valid_records += 1

        if users_to_create:
            User.objects.bulk_create(users_to_create)
        message = (
            "Upload complete! "
            f"We successfully saved {valid_records} new users."
            if valid_records
            else "Unfortunately, no valid records were found."
        )

        return Response(
            {
                "message": message,
                "summary": {
                    "total_saved": valid_records,
                    "total_rejected": invalid_records,
                },
                "errors": errors[:10],
            },
            status=status.HTTP_200_OK,
        )
