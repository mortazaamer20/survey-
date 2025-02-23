from django.contrib import admin
from .models import Survey, Question, Response, Answer
from django.utils.html import mark_safe


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'qr_code_display')

    def qr_code_display(self, obj):
        if obj.qr_code:
            return f'<img src="{obj.qr_code.url}" width="100" height="100" />'
        return "No QR code"
    qr_code_display.allow_tags = True  # Allow HTML for displaying image
    qr_code_display.short_description = 'QR Code'

admin.site.register(Survey, SurveyAdmin)


admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Answer)
