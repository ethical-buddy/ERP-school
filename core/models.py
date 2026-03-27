from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class School(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=30, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SchoolBranch(TimeStampedModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=30)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("school", "code")

    def __str__(self):
        return f"{self.school.code} - {self.name}"


class AcademicSession(TimeStampedModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="academic_sessions")
    title = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ("school", "title")

    def __str__(self):
        return self.title


class FinancialYear(TimeStampedModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="financial_years")
    title = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ("school", "title")

    def __str__(self):
        return self.title


class FeatureFlag(TimeStampedModel):
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SchoolFeature(TimeStampedModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="enabled_features")
    feature = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE, related_name="enabled_schools")
    is_enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ("school", "feature")


class AuditLog(TimeStampedModel):
    school = models.ForeignKey(School, null=True, blank=True, on_delete=models.SET_NULL)
    actor = models.CharField(max_length=150)
    action = models.CharField(max_length=255)
    entity = models.CharField(max_length=150)
    entity_id = models.CharField(max_length=100, blank=True)
    metadata = models.JSONField(default=dict, blank=True)


class SchoolScopedModel(TimeStampedModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        abstract = True
