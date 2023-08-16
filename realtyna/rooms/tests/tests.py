from django.test import TestCase
from ..models import Room
from rest_framework import status
from django.test import TestCase
from ..serializer import RoomSerializer
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


class GetAllAvailableRoomsViewSetTest(TestCase):
    """Test module for GET all Available Rooms API"""

    def setUp(self):
        room_1 = Room.objects.create(title="twin", number=3)
        ReservedRoom.objects.create(
            room=room_1, owner="tony", checking_date = datetime.datetime.now(),
            checkout_date = datetime.datetime.now()+ datetime.timedelta(days=1)
        )

    def test_get_all_available_room(self):
        factory = APIRequestFactory()
        view = AvailableRoomsViewSet.as_view()
        request = factory.get(
            "AvailableRoomsViewSet",
            {"checking_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "checkout_date" :( datetime.datetime.now()+ datetime.timedelta(days=1)).strftime("%Y-%m-%d")}
            # {"date": str(datetime.datetime.now().strftime("%Y-%m-%d"))},
        )
        response = view(
            request,
        )
        reserved_room_id = (
            ReservedRoom.objects.filter(
                checking_date__gte = datetime.datetime.now(),
                checkout_date__lte = datetime.datetime.now()+ datetime.timedelta(days=1) ,            )
            .all()
            .values("room")
        )
        available_room_query = Room.objects.exclude(id__in=reserved_room_id).all()
        serializer = RoomSerializer(available_room_query, many=True)
        self.assertEqual(serializer.data, response.data.get("results"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
