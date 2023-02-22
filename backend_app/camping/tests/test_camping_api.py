"""
Test Camping API
"""

from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse

from core.models import Camping

from camping.serializers import CampingOutSerializer


def create_user(**kwargs):
    """
    create user
    Param: email, password, extra..

    return: user Object
    """

    email = kwargs.pop("email", "user@example.com")
    password = kwargs.pop("password", "test123!@#")

    user = get_user_model().objects.create_user(email, password, **kwargs)
    if user is None:
        raise ValueError("user is None")
    return user


def create_camping(user, **kwargs):
    """
    create camping
    Param: title, review,
        - to be: visited_at, tags,

    Return:
        - Camping Object
    """

    title = kwargs.pop("title", "sample Title")
    review = kwargs.pop("review", "sample review")

    kwargs["title"] = title
    kwargs["review"] = review

    camping = Camping.objects.create(user=user, **kwargs)
    if camping is None:
        raise ValueError("camping is None")
    return camping


CAMPING_URL = reverse("camping:camping-list")


def detail_url(camping_id):
    return reverse("camping:camping-detail", args=[camping_id])


class PublicCampingTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()

    def test_raise_error_when_unautorization_user_request_camping_api(self):
        res = self.client.get(CAMPING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCampingTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_all_camping_list_by_owner(self):
        """작성자가 작성한 모든 캠핑 리스트를 보여줘야함"""
        create_camping(user=self.user)
        create_camping(user=self.user)

        res = self.client.get(CAMPING_URL)  # [(camping_object1), (camping_object2)]
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        camping = Camping.objects.filter(user=self.user)
        self.assertEqual(len(camping), 2)

    def test_get_camping_list_limited_user(self):
        """다른사람이 작성한 캠핑리스트는 보여지지 않아야함"""
        other_user = create_user(email="other@example.com")
        create_camping(user=other_user)

        res = self.client.get(CAMPING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        camping = Camping.objects.filter(user=self.user)
        exists = camping.exists()
        self.assertFalse(exists)

    def test_get_detail_camping(self):
        """camping 상세조회"""
        camping = create_camping(user=self.user)
        url = detail_url(camping.id)

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = CampingOutSerializer(camping)
        self.assertEqual(serializer.data, res.data)

    def test_create_camping_on_validated_data(self):
        """올바른 데이터에 대해서 camping object가 만들어져야함"""
        payload = dict(
            title="some title",
            review="some review",
        )

        res = self.client.post(CAMPING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        camping = get_object_or_404(Camping, user=self.user)

        for key, value in payload.items():
            self.assertTrue(getattr(camping, key), value)

    def test_create_camping_on_invalid_data(self):
        """올바르지 않은 데이터는 error"""
        payload = dict(
            title="",
        )

        res = self.client.post(CAMPING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_camping_update(self):
        """캠핑 object 전체 업데이트"""
        camping = create_camping(user=self.user)

        payload = dict(
            title="new title",
            review="new review",
        )

        url = detail_url(camping.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # db refresh
        camping.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(getattr(camping, key), value)

        self.assertEqual(camping.user, self.user)

    def test_full_camping_update_request_invalid_user_raise_error(self):
        """인증되지 않는 유저가 수정시 메시지 에러"""
        other_user = create_user(email="other@example.com")
        camping = create_camping(user=other_user)

        payload = dict(
            title="new title",
            review="new review",
        )

        url = detail_url(camping.id)

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_camping_update(self):
        """캠핑 object 부분 업데이트"""
        camping = create_camping(user=self.user)
        payload = dict(review="new review")

        url = detail_url(camping.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        camping.refresh_from_db()
        self.assertEqual(camping.review, payload["review"])

    def test_partial_camping_update_invalid_user_raise_error(self):
        """인증되지 않는 유저가 수정시 메시지 에러"""
        other_user = create_user(email="other@example.com")
        camping = create_camping(user=other_user)

        payload = dict(
            title="new title",
        )

        url = detail_url(camping.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_login_user_successful(self):
        """로그인 유저에 대해서 삭제 요청"""
        camping = create_camping(user=self.user)

        url = detail_url(camping.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Camping.objects.filter(user=self.user).exists()
        self.assertFalse(exists)

    def test_delete_other_user_raise_error(self):
        """다른 유저가 삭제요청하면 에러"""
        other_user = create_user(email="other@example.com")
        camping = create_camping(user=other_user)

        url = detail_url(camping.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Camping.objects.filter(id=camping.id).exists())
