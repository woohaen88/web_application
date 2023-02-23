from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from core.models import Blog, CampingTag, BlogTag


def create_user(**kwargs):
    email = kwargs.pop("email", "test@example.com")
    password = kwargs.pop("password", "test123!@#")

    user = get_user_model().objects.create_user(email, password, **kwargs)
    if not user:
        raise ValueError("User 객체 만드는데 실패함 ㅅㄱ")
    return user


class ModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user()

    def test_create_user_successful(self):
        email = "user@example.com"
        password = "test123!@#"
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_without_email_raise_error(self):
        email = ""
        password = "test123!@#"

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, password)

    def test_create_superuser(self):
        email = "admin@admin.com"
        password = "test123!@#"

        admin_user = get_user_model().objects.create_superuser(email, password)

        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_create_blog(self):
        title = "sample title"
        content = "sample content"
        kwargs = dict()

        blog = Blog.objects.create(
            user=self.user, title=title, content=content, **kwargs
        )
        self.assertEqual(str(blog), blog.title)

    def test_create_blog_tag(self):
        name = "tag1"
        blog_tag = BlogTag.objects.create(name=name)

        self.assertEqual(str(blog_tag), name)

    def test_creat_camping_tag(self):
        name = "tag1"
        camping_tag = CampingTag.objects.create(name=name)

        self.assertEqual(str(camping_tag), name)
