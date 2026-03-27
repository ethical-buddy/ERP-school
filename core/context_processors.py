def current_school(request):
    user = request.user
    is_auth = getattr(user, "is_authenticated", False)
    is_admin = bool(is_auth and (user.is_superuser or user.groups.filter(name="admin_portal").exists()))
    is_teacher = bool(is_auth and user.groups.filter(name="teacher_portal").exists())
    is_student = bool(is_auth and user.groups.filter(name="student_portal").exists())
    primary_label = ""
    primary_url = ""
    if is_admin:
        primary_label = "Admin Portal"
        primary_url = "/portal/admin/"
    elif is_teacher:
        primary_label = "Teacher Portal"
        primary_url = "/portal/teacher/"
    elif is_student:
        primary_label = "Student Portal"
        primary_url = "/portal/student/"
    return {
        "current_school": getattr(request, "current_school", None),
        "is_admin_portal": is_admin,
        "is_teacher_portal": is_teacher,
        "is_student_portal": is_student,
        "primary_portal_label": primary_label,
        "primary_portal_url": primary_url,
    }
