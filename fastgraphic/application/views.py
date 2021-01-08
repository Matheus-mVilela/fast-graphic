from django import shortcuts, views


class HelloWorldView(views.View):
    def get(self, request):
        return shortcuts.render(
            request, 'my-folder/home.html', context={'user': request.user}
        )


# Create your views here.
