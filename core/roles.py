def in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or in_group(user, "admin_portal"))


def is_teacher(user):
    return user.is_authenticated and in_group(user, "teacher_portal")


def is_student(user):
    return user.is_authenticated and in_group(user, "student_portal")


def can_manage_finance(user):
    return is_admin(user) or is_teacher(user)


def can_manage_attendance(user):
    return is_admin(user) or is_teacher(user)


def can_manage_students(user):
    return is_admin(user) or is_teacher(user)


def can_manage_staff(user):
    return is_admin(user)
