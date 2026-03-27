from django.contrib import admin

from .models import CertificateTemplate, IDCardTemplate, ProspectusLead, Student, StudentCertificate, StudentDocument, StudentDocumentType

admin.site.register(Student)
admin.site.register(ProspectusLead)
admin.site.register(StudentDocumentType)
admin.site.register(StudentDocument)
admin.site.register(IDCardTemplate)
admin.site.register(CertificateTemplate)
admin.site.register(StudentCertificate)
