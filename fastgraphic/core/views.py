from django.contrib.auth import views as views_auth


class LoginView(views_auth.LoginView):
    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin/'
        return '/'


def handler404(request, *args, **argv):
    return render(request, '404.html', status=404)


def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)

