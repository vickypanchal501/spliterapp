from django.shortcuts import redirect
from django.urls import reverse

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Redirect authenticated users away from login and signup pages
            if request.path in [reverse('Login'), reverse('Signup')]:
                return redirect('Main')  # Change 'home' to the desired URL

        elif  not request.user.is_staff and request.path not in [reverse('Login'), reverse('Signup'), reverse('index'), ]:
            return redirect('index')
        response = self.get_response(request)
        return response
