from django.db import models


class Conversation(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_message_count(self):
        return self.message_set.count()

    def has_analysis(self):
        return hasattr(self, 'analysis')


class Message(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50, choices=SENDER_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.text[:50]}"


class ConversationAnalysis(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, related_name='analysis')
    clarity_score = models.FloatField()
    relevance_score = models.FloatField()
    accuracy_score = models.FloatField()
    completeness_score = models.FloatField()
    sentiment = models.CharField(max_length=50, choices=SENTIMENT_CHOICES)
    empathy_score = models.FloatField()
    avg_response_time = models.FloatField()
    resolved = models.BooleanField(default=False)
    escalation_needed = models.BooleanField(default=False)
    fallback_count = models.IntegerField(default=0)
    overall_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Conversation Analyses'

    def __str__(self):
        return f"Analysis for {self.conversation.title} - Score: {self.overall_score}"
