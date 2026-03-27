import logging
import time

from accounts.models import UserProfile
from core.models import School

slow_logger = logging.getLogger("slow_requests")


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


class SchoolContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        school = None
        if request.user.is_authenticated:
            profile = UserProfile.objects.select_related("school").filter(user=request.user).first()
            if profile and profile.school_id:
                school = profile.school
        if school is None:
            school_id = request.session.get("school_id")
            if school_id:
                school = School.objects.filter(id=school_id, is_active=True).first()
        request.current_school = school
        return self.get_response(request)


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        response["X-Response-Time-Ms"] = str(elapsed_ms)
        threshold = 500.0
        if elapsed_ms >= threshold:
            slow_logger.warning(
                "slow_request method=%s path=%s status=%s duration_ms=%s user=%s",
                request.method,
                request.path,
                response.status_code,
                elapsed_ms,
                request.user.username if request.user.is_authenticated else "anonymous",
            )
        return response
