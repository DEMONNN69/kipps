from celery import shared_task
from .models import Conversation, Message, ConversationAnalysis
from .analysis import analyze_messages


@shared_task
def analyze_new_conversations():
    conversations = Conversation.objects.prefetch_related('message_set').all()
    analyzed_count = 0
    
    for conversation in conversations:
        if not conversation.has_analysis():
            messages = conversation.message_set.all()
            if messages.exists():
                messages_list = [{'sender': msg.sender, 'text': msg.text} for msg in messages]
                analysis_data = analyze_messages(messages_list)
                ConversationAnalysis.objects.create(
                    conversation=conversation,
                    **analysis_data
                )
                analyzed_count += 1
    
    return analyzed_count

