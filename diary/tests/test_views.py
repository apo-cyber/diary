from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from diary.models import Diary

class LoggedInTestCase(TestCase):
    def setUp(self):

        self.password = 'apopo1129'
        self.test_user = get_user_model().objects.create_user(
            username='kuzuha',
            email='kuzuha@gmail.com',
            password=self.password
        )
        self.client.login(email=self.test_user.email, password=self.password)

class TestDiaryCreateView(LoggedInTestCase):

    def test_create_diary(self):
        params = {'title': 'テストタイトル', 'content': '本文', 'photo1': '', 'photo2': '', 'photo3': ''}
        response = self.client.post(reverse_lazy('diary:diary_create'), params)
        self.assertRedirects(response, reverse_lazy('diary:diary_list'))
        self.assertEqual(Diary.objects.filter(title='テストタイトル').count(), 1)

    def test_create_diary_faild(self):
        response = self.client.post(reverse_lazy('diary:diary_create'))
        self.assertFormError(response, 'form', 'title', 'このフィールドは必須です。')

class TestDiaryUpdateView(LoggedInTestCase):

    def test_diary_success(self):
        diary = Diary.objects.create(user=self.test_user, title='タイトル編集前')
        params = {'title': 'タイトル編集後'}
        response = self.client.post(reverse_lazy('diary:diary_update', kwargs={'pk': diary.pk}), params)
        self.assertRedirects(response, reverse_lazy('diary:diary_detail', kwargs={'pk': diary.pk}))
        self.assertEqual(Diary.objects.get(pk=diary.pk).title, 'タイトル編集後')

    def test_diary_faild(self):
        response = self.client.post(reverse_lazy('diary:diary_update', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

class TestDiaryDeleteView(LoggedInTestCase):

    def test_diary_success(self):
        diary = Diary.objects.create(user=self.test_user, title='タイトル')
        response = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': diary.pk}))
        self.assertRedirects(response, reverse_lazy('diary:diary_list'))
        self.assertEqual(Diary.objects.filter(pk=diary.pk).count(), 0)

    def test_diary_failure(self):
        response = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)
