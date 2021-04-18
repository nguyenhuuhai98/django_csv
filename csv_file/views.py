import csv

from io import TextIOWrapper
from time import strftime

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from csv_file.models import User


class CSVHandleView(APIView):
    def post(self, request, *args, **kwargs):
        if 'file' in request.FILES:
            # Handling csv file before save to database
            form_data = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
            csv_file = csv.reader(form_data)
            next(csv_file)  # Skip read csv header

            users_list = []

            for line in csv_file:
                user = User()
                user.first_name = line[0]
                user.last_name = line[1]
                user.email = line[2]
                user.phone_number = line[3]
                user.address = line[4]
                users_list.append(user)

            # Save to database
            User.objects.bulk_create(users_list)

        return Response({
            'message': 'Import done!'
        })

    def get(self, request, *args, **kwargs):
        headers = ['First Name', 'Last Name', 'Email', 'Phone Number', 'Address']
        file_name = f"users_{strftime('%Y-%m-%d-%H-%M')}"

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{file_name}.csv"'

        writer = csv.writer(response)
        writer.writerow(headers)

        users = User.objects.values('first_name', 'last_name', 'email', 'phone_number', 'address')

        for user in users:
            line = []
            for row in user.values():
                line.append(row)
            writer.writerow(line)

        return response
