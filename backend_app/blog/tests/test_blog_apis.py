from django.contrib.auth import get_user_model
from django.urls import reverse

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Blog
from django.shortcuts import get_object_or_404

from blog.serializers import BlogOutSerializer


def create_user(**kwargs):
    email = kwargs.pop("email", "test@example.com")
    password = kwargs.pop("password", "test123!@#")

    user = get_user_model().objects.create_user(email, password, **kwargs)
    if not user:
        raise ValueError("user 만들기 실패 ㅅㄱ")
    return user

def create_blog(user, **kwargs):
    title = kwargs.pop("title", "sample title")
    content = kwargs.pop("content", "sample content")

    kwargs["title"] = title
    kwargs["content"] = content

    blog = Blog.objects.create(user=user, **kwargs)
    if blog is None:
        raise ValueError("Blog 만들기 실패 ㅅㄱ")
    return blog


BLOG_URL = reverse("blog:blog-list")
def detail_url(blog_id):
    return reverse("blog:blog-detail", args=[blog_id])


class PublicBlogApisTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()

    def test_get_blog_api_raise_error_when_invalid_user_request(self):
        res = self.client.get(BLOG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateBlogApisTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_all_blog_list_successful(self):
        """인증된 모든 유저에 대해서 모든 블로그 리스트 조회"""
        create_blog(self.user)
        create_blog(self.user)

        res = self.client.get(BLOG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 2)

    def test_get_blog_list_limited_user(self) -> None:
        """본인이 소유한 모든 블로그 리스트 조회"""
        other_user = create_user(email="other@example.com")
        create_blog(user=other_user)
        

        res = self.client.get(BLOG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        blog = Blog.objects.filter(user=self.user)
        self.assertFalse(blog.exists())

    def test_get_blog_one(self) -> None:
        """작성한 글 한개 조회"""
        blog = create_blog(self.user)


        url = detail_url(blog.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        blog = get_object_or_404(Blog, user=self.user)
        serializer = BlogOutSerializer(blog)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(blog.user, self.user)

    def test_create_blog_validated_data(self) -> None:
        """올바른 데이터에 대해서 블로그 생성"""
        payload = dict(
            title = "sample title",
            content = "content",
        )
        res = self.client.post(BLOG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_put_blog_validated_data(self) -> None:
        """유효한 데이터에 대해서 전체 업데이트"""
        blog = create_blog(self.user)

        payload = dict(
            title="new title",
            content="new content"
        )

        url = detail_url(blog.id)

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        blog.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(getattr(blog, key), value)
        

    def test_put_blog_invalid_user_raise_error(self) -> None:
        """다른 유저가 수정하려 하면 error"""
        other_user = create_user(email="other@example.com")
        blog = create_blog(other_user)

        payload = dict(
            title="new title",
            content="new content"
        )

        url = detail_url(blog.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_blog_validated_data(self) -> None:
        """유효한 데이터에 대해서 부분 업데이트"""
        blog = create_blog(self.user)

        payload = dict(            
            content="new content"
        )

        url = detail_url(blog.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        blog.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(getattr(blog, key), value)
        
    def test_patch_blog_invalid_user_raise_error(self) -> None:
        """다른 유저가 수정하려 하면 error"""
        other_user = create_user(email="other@example.com")
        blog = create_blog(other_user)

        payload = dict(
            content="new content"
        )

        url = detail_url(blog.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_blog_validated_data(self) -> None:
        """유효한 요청이면 삭제"""
        blog = create_blog(self.user)

        url = detail_url(blog.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Blog.objects.filter(user=self.user).exists()
        self.assertFalse(exists)

    def test_delete_blog_invalid_user_raise_error(self) -> None:
        """유효한 요처잉 아니면 삭제 실패"""
        other_user = create_user(email="other@example.com")
        blog = create_blog(other_user)

        url = detail_url(blog.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        exists = Blog.objects.filter(user=other_user).exists()
        self.assertTrue(exists)
    


    
        
        