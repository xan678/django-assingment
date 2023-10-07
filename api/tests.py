# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import UserProfile
from api.models import Post
from user.utils import create_jwt_token


class PostViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserProfile.objects.create_user(email='ravibhushan29@gmail.com',
                                                    password='testpassword@123')
        # Generate JWT token and set Authorization header
        token = create_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')
        self.url = reverse('posts')  # assuming name='post-list' for PostView url
        self.post_data = {
            'content': 'This is a post content.'
        }

    def test_create_post(self):
        response = self.client.post(self.url, self.post_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Post.objects.filter(content='This is a post content.').exists())

    def test_get_posts(self):
        Post.objects.create(user=self.user, content='Post 1')
        Post.objects.create(user=self.user, content='Post 2')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)


class PostDetailViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserProfile.objects.create_user(email='ravibhushan29@gmail.com',
                                                    password='testpassword@123')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(user=self.user, content='Sample post')
        self.url = reverse('detail_post', kwargs={'pk': self.post.pk})  # assuming name='post-detail' for PostDetailView url

    def test_get_post_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['content'], 'Sample post')

    def test_update_post(self):
        updated_data = {
            'content': 'Updated content'
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.content, 'Updated content')

    def test_delete_post(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
