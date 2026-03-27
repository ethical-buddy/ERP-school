def current_school(request):
    return {"current_school": getattr(request, "current_school", None)}
