from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardRenderTests(TestCase):
    def test_dashboard_renders_with_static_banner(self):
        user = get_user_model().objects.create_user(username="consultor")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertContains(response, "Panel 360")
        self.assertContains(response, "dashboard-top.svg")
