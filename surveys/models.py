import qrcode
from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.text import slugify

from django.urls import reverse
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.text import slugify



class Survey(models.Model):
    title = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def generate_qr_code(self):
        """Generate QR code for the survey with dynamic URL."""
        # URL including the survey's ID after it's been saved
        base_url = settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://127.0.0.1:8000'
        survey_url = base_url + reverse('survey_detail', args=[self.id])

        # Generate QR code
        qr = qrcode.make(survey_url)
        
        # Save it as a PNG image in memory
        image_io = BytesIO()
        qr.save(image_io, 'PNG')  # Make sure to specify the format as PNG
        image_io.seek(0)  # Reset pointer to the beginning

        # Create the image file name using the survey title
        qr_code_name = f"{slugify(self.title)}.png"

        # Save the file as an image in the ImageField
        self.qr_code.save(qr_code_name, ContentFile(image_io.read()), save=False)

    def save(self, *args, **kwargs):
        """Override the save method to generate QR code on save."""
        super().save(*args, **kwargs)  # First save the instance to generate an ID
        if not self.qr_code:  # Only generate QR code if it doesn't exist
            self.generate_qr_code()
            super().save(*args, **kwargs)  # Save again after generating the QR code

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text

class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    first_answer = models.CharField(max_length=255, blank=True, null=True)  # Stores "username"
    text_color = models.CharField(max_length=7, blank=True, null=True)  # stores color hex, e.g., "#ff6f61"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.survey.title} by {self.first_answer or 'Anonymous'}"

class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()

    def save(self, *args, **kwargs):
        # Store the first answer as the "username"
        if not self.response.first_answer:
            self.response.first_answer = self.text
            self.response.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.question.text}: {self.text}"
