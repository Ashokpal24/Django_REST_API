from urllib import response
from .models import UserProfile
from rest_framework.test import APIClient,APITestCase
from rest_framework import status

class UserTestCase(APITestCase):
    def setUp(self):
        self.client=APIClient()
        self.data=[
            {
                "name":"Jaz",
                "email":"Jaz11greed@gmail.com"
            },
            {
                "name":"Jade",
                "email":"Jade77gasper@gmail.com"
            }
        ]
        self.url="/api/"


    def test_create_user(self):
        for new_data in self.data:
            data=new_data
            response=self.client.post(self.url,data)
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(),2)
        self.assertEqual(UserProfile.objects.get(id=1).name,"Jaz")

    def test_get_user(self):
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    