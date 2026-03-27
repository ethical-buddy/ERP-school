from django import forms

from .models import Exam


class ExamBulkUploadForm(forms.Form):
    exam = forms.ModelChoiceField(queryset=Exam.objects.none())
    marks_file = forms.FileField(help_text="CSV with columns: admission_no,theory,internal,practical,remarks")

    def __init__(self, *args, **kwargs):
        school = kwargs.pop("school", None)
        super().__init__(*args, **kwargs)
        qs = Exam.objects.select_related("course", "section", "subject").order_by("-id")
        if school is not None:
            qs = qs.filter(school=school)
        self.fields["exam"].queryset = qs
