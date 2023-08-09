from django.test import TestCase
from ..models import  Room
from rest_framework import status
from django.test import TestCase
from ..serializer import  RoomSerializer
from ..views import *
from rest_framework.test import APIRequestFactory


class RoomTest(TestCase):
    """Test module for room model"""

    def setUp(self):
        Room.objects.create(title="twin", number=3)
        Room.objects.create(title="double", number=1)

    def test_creation_room(self):
        room_1 = Room.objects.get(title="twin")
        room_2 = Room.objects.get(title="double")
        self.assertEqual(room_1.number, 3)
        self.assertEqual(room_2.number, 1)

class GetAllRoomTest(TestCase):
    """Test module for GET all rooms API"""

    def setUp(self):
        room_1 = Room.objects.create(title="twin", number=3)
        room_2 = Room.objects.create(title="double", number=1)

    def test_get_all_rooms(self):
        factory = APIRequestFactory()
        view = RoomsViewSet.as_view({"get": "list"})
        request = factory.get("RoomsViewSet")
        rooms = Room.objects.all()
        response = view(request)
        serializer = RoomSerializer(rooms, many=True)
        self.assertEqual(serializer.data, response.data.get("results"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
