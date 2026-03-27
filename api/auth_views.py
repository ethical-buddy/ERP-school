from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .throttles import AuthTokenThrottle


class TokenObtainPairThrottledView(TokenObtainPairView):
    throttle_classes = [AuthTokenThrottle]


class TokenRefreshThrottledView(TokenRefreshView):
    throttle_classes = [AuthTokenThrottle]
