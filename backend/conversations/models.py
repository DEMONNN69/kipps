from django.db import models


class Conversation(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    text = models.TextField()


class ConversationAnalysis(models.Model):
    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE)
    clarity_score = models.FloatField()
    relevance_score = models.FloatField()
    accuracy_score = models.FloatField()
    completeness_score = models.FloatField()
    sentiment = models.CharField(max_length=50)
    empathy_score = models.FloatField()
    avg_response_time = models.FloatField()
    resolved = models.BooleanField()
    escalation_needed = models.BooleanField()
    fallback_count = models.IntegerField()
    overall_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
