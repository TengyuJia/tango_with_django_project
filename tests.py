from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Test case for user registration functionality
class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        # Test successful user registration
        response = self.client.post(reverse('rango:register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home page
        self.assertTrue(User.objects.filter(username='testuser').exists())  # User created

    def test_user_registration_with_mismatched_passwords(self):
        # Test registration with mismatched passwords
        response = self.client.post(reverse('rango:register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'securepassword123',
            'password2': 'mismatchedpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on registration page
        self.assertFalse(User.objects.filter(username='testuser').exists())  # User not created

    def test_user_registration_with_existing_username(self):
        # Test registration with existing username
        User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword123')
        response = self.client.post(reverse('rango:register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        })
        self.assertEqual(response.status_code, 200)  # Stay on registration page
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)  # User not duplicated

# Test case for user login functionality
class UserLoginTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword123')

    def test_user_login(self):
        # Test successful user login
        response = self.client.post(reverse('rango:login'), {
            'username': 'testuser',
            'password': 'securepassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home page
        self.assertTrue(self.client.login(username='testuser', password='securepassword123'))  # User logged in

    def test_user_login_with_wrong_password(self):
        # Test login with wrong password
        response = self.client.post(reverse('rango:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertFalse(self.client.login(username='testuser', password='wrongpassword'))  # User not logged in

    def test_user_login_with_nonexistent_user(self):
        # Test login with non-existent username
        response = self.client.post(reverse('rango:login'), {
            'username': 'nonexistentuser',
            'password': 'securepassword123'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertFalse(self.client.login(username='nonexistentuser', password='securepassword123'))  # User not logged in

# Test case for user logout functionality
class UserLogoutTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword123')

    def test_user_logout(self):
        # Test user logout
        self.client.login(username='testuser', password='securepassword123')
        response = self.client.get(reverse('rango:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to home page
        self.assertFalse(self.client.session.get('_auth_user_id'))  # User logged out

# Test case for user password change functionality
class UserPasswordChangeTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword123')

    def test_user_password_change(self):
        # Test successful password change
        self.client.login(username='testuser', password='securepassword123')
        response = self.client.post(reverse('rango:change_password'), {
            'old_password': 'securepassword123',
            'new_password1': 'newsecurepassword123',
            'new_password2': 'newsecurepassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home page
        self.assertTrue(self.client.login(username='testuser', password='newsecurepassword123'))  # Password updated