import logging

logger = logging.getLogger(__name__)


class LogCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            print(f"CSRF Debug: Referer: {request.META.get('HTTP_REFERER')}, Origin: {request.META.get('HTTP_ORIGIN')}, Host: {request.get_host()} other headers: {request.headers}")
        response = self.get_response(request)
        return response
