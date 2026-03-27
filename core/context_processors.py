def current_school(request):
    user = request.user
    is_auth = getattr(user, "is_authenticated", False)
    return {
        "current_school": getattr(request, "current_school", None),
        "is_admin_portal": bool(is_auth and (user.is_superuser or user.groups.filter(name="admin_portal").exists())),
        "is_teacher_portal": bool(is_auth and user.groups.filter(name="teacher_portal").exists()),
        "is_student_portal": bool(is_auth and user.groups.filter(name="student_portal").exists()),
    }
