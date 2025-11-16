from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, ConversationAnalysis
from .serializers import ConversationAnalysisSerializer, ConversationSerializer
from .analysis import analyze_messages


@api_view(['POST'])
def create_conversation(request):
    messages_data = request.data.get('messages', [])
    
    if not messages_data:
        return Response(
            {'error': 'messages field is required and cannot be empty'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    if not isinstance(messages_data, list):
        return Response(
            {'error': 'messages must be a list'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    title = f"Conversation {Conversation.objects.count() + 1}"
    conversation = Conversation.objects.create(title=title)

    created_messages = []
    for msg_data in messages_data:
        sender = msg_data.get('sender', '').lower()
        message_text = msg_data.get('message', '')
        
        if sender not in ['user', 'ai']:
            conversation.delete()
            return Response(
                {'error': f'invalid sender: {sender}. Must be "user" or "ai"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not message_text.strip():
            continue
            
        msg = Message.objects.create(
            conversation=conversation,
            sender=sender,
            text=message_text
        )
        created_messages.append(msg)

    if not created_messages:
        conversation.delete()
        return Response(
            {'error': 'at least one valid message is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = ConversationSerializer(conversation)
    return Response({
        'conversation_id': conversation.id,
        'conversation': serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def analyze_conversation(request):
    conversation_id = request.data.get('conversation_id')
    
    if not conversation_id:
        return Response(
            {'error': 'conversation_id is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        conversation_id = int(conversation_id)
    except (ValueError, TypeError):
        return Response(
            {'error': 'conversation_id must be a valid integer'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    messages = Message.objects.filter(conversation=conversation)
    if not messages.exists():
        return Response(
            {'error': 'conversation has no messages to analyze'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    messages_list = [{'sender': msg.sender, 'text': msg.text} for msg in messages]
    analysis_data = analyze_messages(messages_list)

    analysis, created = ConversationAnalysis.objects.update_or_create(
        conversation=conversation,
        defaults=analysis_data
    )

    serializer = ConversationAnalysisSerializer(analysis)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_reports(request):
    analyses = ConversationAnalysis.objects.select_related('conversation').all()
    
    sentiment_filter = request.query_params.get('sentiment')
    if sentiment_filter:
        analyses = analyses.filter(sentiment=sentiment_filter)
    
    resolved_filter = request.query_params.get('resolved')
    if resolved_filter is not None:
        resolved_bool = resolved_filter.lower() == 'true'
        analyses = analyses.filter(resolved=resolved_bool)
    
    serializer = ConversationAnalysisSerializer(analyses, many=True)
    return Response({
        'count': len(serializer.data),
        'results': serializer.data
    }, status=status.HTTP_200_OK)
