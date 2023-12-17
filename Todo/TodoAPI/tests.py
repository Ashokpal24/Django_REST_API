import email
from urllib import response
from .models import UserProfile
from rest_framework.test import APIClient,APITestCase
from rest_framework import status

class UserTestCase(APITestCase):
    def setUp(self):
        self.client=APIClient()
        self.user=UserProfile.objects.create(name="Edward",email="Edward24Kenway@gmail.com")
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
        self.assertEqual(UserProfile.objects.count(),3)
        self.assertEqual(UserProfile.objects.get(id=2).name,"Jaz")

    def test_get_user(self):
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_user_by_id(self):
        new_url=self.url+"1"
        response=self.client.get(new_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_update_user(self):    
        new_url=self.url+"1"
        new_data={
            "name":"Jaz Kanway",
            "email":"Jaz11Kanway@gmail.com"
        }
        response=self.client.put(new_url,new_data)
        print(UserProfile.objects.all())
        self.assertEqual(UserProfile.objects.count(),1)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
