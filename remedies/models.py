from django.db import models

class Remedy(models.Model):
    symptom_english = models.CharField(max_length=255)
    symptom_telugu = models.CharField(max_length=255)
    symptom_hindi = models.CharField(max_length=255)
    remedy_name = models.CharField(max_length=255)
    ingredients = models.TextField()
    preparation_steps = models.TextField()
    relief_time = models.CharField(max_length=100)
    remedy_type = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)

    remedy_name_te = models.TextField(blank=True, null=True)
    ingredients_te = models.TextField(blank=True, null=True)
    preparation_steps_te = models.TextField(blank=True, null=True)

    remedy_name_hi = models.TextField(blank=True, null=True)
    ingredients_hi = models.TextField(blank=True, null=True)
    preparation_steps_hi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.remedy_name

class SuggestedRemedy(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    symptom = models.CharField(max_length=255)
    remedy_name = models.CharField(max_length=255)
    ingredients = models.TextField()
    preparation_steps = models.TextField()
    language = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.remedy_name} ({self.status})"

class Feedback(models.Model):
    remedy = models.ForeignKey(Remedy, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField()
    feedback_text = models.TextField()
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.remedy.remedy_name} - {self.rating} Stars"

class UnknownSymptom(models.Model):
    symptom_text = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symptom_text
