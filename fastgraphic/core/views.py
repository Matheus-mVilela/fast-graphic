from django.contrib.auth import views as views_auth


class LoginView(views_auth.LoginView):
    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin/'
        return '/'
