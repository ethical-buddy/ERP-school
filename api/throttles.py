from rest_framework.throttling import ScopedRateThrottle


class AuthTokenThrottle(ScopedRateThrottle):
    scope = "auth_token"
