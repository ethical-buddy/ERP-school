from accounts.models import UserProfile
from rest_framework.exceptions import PermissionDenied


class SchoolScopedQuerysetMixin:
    school_field = "school"

    def get_user_school(self):
        if self.request.user.is_superuser:
            school_id = self.request.query_params.get("school_id")
            if school_id:
                return int(school_id)
            return None
        profile = UserProfile.objects.filter(user=self.request.user).only("school_id").first()
        if profile and profile.school_id:
            return profile.school_id
        return None

    def get_queryset(self):
        base_qs = super().get_queryset()
        school_id = self.get_user_school()
        if school_id is None:
            if self.request.user.is_superuser:
                return base_qs
            return base_qs.none()
        return base_qs.filter(**{self.school_field + "_id": school_id})

    def perform_create(self, serializer):
        school_id = self.get_user_school()
        if school_id is None and self.request.user.is_superuser:
            school_id = self.request.data.get("school")
        if school_id is None:
            raise PermissionDenied("School context is required for this user.")
        serializer.save(school_id=school_id)
