from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import BlogTag

TAG_URL = reverse("blog:blogtag-list")


def create_user(**kwargs):
    email = kwargs.pop("email", "user@example.com")
    password = kwargs.pop("password", "test123!@#")

    user = get_user_model().objects.create_user(email, password, **kwargs)
    if not user:
        raise ValueError("user 생성 실패 ㅅㄱ")
    return user


def create_tag(user, **kwargs):
    if "name" not in kwargs.keys():
        kwargs["name"] = "sample_tag"

    blog = BlogTag.objects.create(user=user, **kwargs)
    if not blog:
        raise ValueError("BlogTag 생성 실패 ㅅㄱ!!")
    return blog


class PublicBlogTagAPIsTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def get_tag_list_when_an_unauthenticated_user_request_raise_error(self):
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBlogTagAPIsTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_all_blogtag_lists_created_by_the_authentication(self):
        """인증유져가 요청하면 본인이 작성한 모든 태그 리스트 조회"""
        create_tag(self.user, name="tag1")
        create_tag(self.user, name="tag2")

        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 2)

    def test_get_tag_list_only_for_limited_users(self):
        """제한된 유저에게만 태그 리스트 조회"""
        other_user = create_user(email="other@example.com")

        create_tag(self.user, name="haha")
        create_tag(other_user, name="hoho")

        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0].get("name"), "haha")
        self.assertEqual(len(res.data), 1)

    def test_successful_when_the_authenticated_user_modifies_the_tag(self):
        """인증유져가 태그 수정시 성공"""
        pass

    def test_failed_when_an_authenticated_user_modifies_another_user_tag(self):
        """인증유져가 다른유져의 태그 수정시 실패"""
        pass

    def test_successful_when_the_authenticated_user_patch_the_tags(self):
        """인증유져가 태그 일부 수정시 성공"""
        pass

    def test_failure_when_authentication_user_modifies_other_user_tags(self):
        """인증유져가 다른유져의 태그 일부 수정시 실패"""
        pass

    def test_successful_when_the_authentication_user_requests_to_delete_his_or_her_own_tag(
        self,
    ):
        """인증유져가 본인 태그 삭제 요청시 성공"""
        pass

    def test_failure_when_the_authentication_user_requests_to_delete_other_tags(self):
        """인증유져가 다른 태그 삭제 요청시 실패"""

    def test_generate_a_blogtag_when_requested_with_valid_data(self):
        """정상적인 데이터로 요청하면 모델 생성"""
        pass
