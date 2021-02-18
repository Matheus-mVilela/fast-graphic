from django.contrib.auth import views as views_auth
from django.shortcuts import render


class LoginView(views_auth.LoginView):
    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin/'
        return '/'


def handler404(request, exception):
    return render(request, 'error/404.html', status=404)


def handler500(request):
    return render(request, 'error/500.html', status=500)
