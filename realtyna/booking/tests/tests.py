import datetime
from django.test import TestCase
from ..models import  Room
from rest_framework import status
from django.test import TestCase
from ..views import *
from rest_framework.test import APIRequestFactory


class ReservedRoomTest(TestCase):
    def setUp(self):
        room_1 = Room.objects.create(title="twin", number=3)
        room_2 = Room.objects.create(title="double", number=1)
        ReservedRoom.objects.create(
            room=room_1,
            owner="tony",
            date=datetime.datetime.now() + datetime.timedelta(days=1),
        )
        ReservedRoom.objects.create(
            room=room_2,
            owner="mohammad",
            date=datetime.datetime.now() + datetime.timedelta(days=1),
        )

    def test_create_reservation(self):
        reservation_1 = ReservedRoom.objects.get(owner="tony")
        reservation_2 = ReservedRoom.objects.get(owner="mohammad")
        room_1 = Room.objects.get(title="twin")
        room_2 = Room.objects.get(title="double")
        self.assertEqual(str(reservation_1.room.id), str(room_1.id))
        self.assertEqual(str(reservation_2.room.id), str(room_2.id))



class GetAllReservedRoomsViewSetTest(TestCase):
    """Test module for GET all reservation API"""

    def setUp(self):
        room_1 = Room.objects.create(title="twin", number=3)
        room_2 = Room.objects.create(title="double", number=1)
        ReservedRoom.objects.create(
            room=room_1,
            owner="tony",
            date=datetime.datetime.now() + datetime.timedelta(days=1),
        )
        ReservedRoom.objects.create(
            room=room_2,
            owner="mohammad",
            date=datetime.datetime.now() + datetime.timedelta(days=1),
        )

    def test_get_all_reservation(self):
        factory = APIRequestFactory()
        view = ReservedRoomsViewSet.as_view({"get": "list"})
        request = factory.get("ReservedRoomsViewSet")
        rooms = ReservedRoom.objects.all()
        response = view(request)
        serializer = ReservedRoomSerializer(rooms, many=True)
        self.assertEqual(serializer.data, response.data.get("results"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookingRoomsViewSetTest(TestCase):
    """Test module for book the room  API"""

    def setUp(self):
        room_1 = Room.objects.create(title="twin", number=3)

    def test_get_all_available_room(self):
        room_1 = Room.objects.get(title="twin")
        factory = APIRequestFactory()
        view = BookingRoomsViewSet.as_view()
        request = factory.post(
            "BookingRoomsViewSet",
            {
                "date": str(datetime.datetime.now().strftime("%Y-%m-%d")),
                "owner": "reza",
                "room": str(room_1.id),
            },
        )
        response = view(
            request,
        )

        reserved_room = ReservedRoom.objects.get(
            date=str(datetime.datetime.now().strftime("%Y-%m-%d")),
            owner="reza",
            room=str(room_1.id),
        )
        serializer = ReservedRoomSerializer(reserved_room)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
