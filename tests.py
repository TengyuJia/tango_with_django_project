from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        # 测试用户注册
        response = self.client.post(reverse('rango:register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        })
        self.assertEqual(response.status_code, 302)  # 重定向到首页
        self.assertTrue(User.objects.filter(username='testuser').exists())  # 用户已创建

    def test_user_registration_with_mismatched_passwords(self):
        # 测试用户注册时密码不匹配
        response = self.client.post(reverse('rango:register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'securepassword123',
            'password2': 'mismatchedpassword'
        })
        self.assertEqual(response.status_code, 200)  # 仍然在注册页面
        self.assertFalse(User.objects.filter(username='testuser').exists())  # 用户未创建

    def test_user_registration_with_existing_username(self):
        # 测试用户注册时用户名已存在
        User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword123')
        response = self.client.post(reverse('rango:register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        })
        self.assertEqual(response.status_code, 200)  # 仍然在注册页面
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)  # 用户未重复创建



class UserLoginTest(TestCase):
    def setUp(self):
        # 创建一个测试用户
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword123')

    def test_user_login(self):
        # 测试用户登录
        response = self.client.post(reverse('rango:login'), {
            'username': 'testuser',
            'password': 'securepassword123'
        })
        self.assertEqual(response.status_code, 302)  # 重定向到首页
        self.assertTrue(self.client.login(username='testuser', password='securepassword123'))  # 用户已登录

    def test_user_login_with_wrong_password(self):
        # 测试用户登录时密码错误
        response = self.client.post(reverse('rango:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # 仍然在登录页面
        self.assertFalse(self.client.login(username='testuser', password='wrongpassword'))  # 用户未登录

    def test_user_login_with_nonexistent_user(self):
        # 测试用户登录时用户名不存在
        response = self.client.post(reverse('rango:login'), {
            'username': 'nonexistentuser',
            'password': 'securepassword123'
        })
        self.assertEqual(response.status_code, 200)  # 仍然在登录页面
        self.assertFalse(self.client.login(username='nonexistentuser', password='securepassword123'))  # 用户未登录

class UserLogoutTest(TestCase):
    def setUp(self):
        # 创建一个测试用户
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword123')

    def test_user_logout(self):
        # 测试用户登出
        self.client.login(username='testuser', password='securepassword123')
        response = self.client.get(reverse('rango:logout'))
        self.assertEqual(response.status_code, 302)  # 重定向到首页
        self.assertFalse(self.client.session.get('_auth_user_id'))  # 用户已登出



class UserPasswordChangeTest(TestCase):
    def setUp(self):
        # 创建一个测试用户
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword123')

    def test_user_password_change(self):
        # 测试用户修改密码
        self.client.login(username='testuser', password='securepassword123')
        response = self.client.post(reverse('rango:change_password'), {
            'old_password': 'securepassword123',
            'new_password1': 'newsecurepassword123',
            'new_password2': 'newsecurepassword123'
        })
        self.assertEqual(response.status_code, 302)  # 重定向到首页
        self.assertTrue(self.client.login(username='testuser', password='newsecurepassword123'))  # 用户已更新密码