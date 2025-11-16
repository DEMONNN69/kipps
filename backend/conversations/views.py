from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message, ConversationAnalysis
from .serializers import ConversationAnalysisSerializer
from .analysis import analyze_messages


@api_view(['POST'])
def create_conversation(request):
    messages_data = request.data.get('messages', [])
    
    if not messages_data:
        return Response({'error': 'messages required'}, status=status.HTTP_400_BAD_REQUEST)

    title = f"Conversation {Conversation.objects.count() + 1}"
    conversation = Conversation.objects.create(title=title)

    for msg_data in messages_data:
        Message.objects.create(
            conversation=conversation,
            sender=msg_data.get('sender', ''),
            text=msg_data.get('message', '')
        )

    return Response({'conversation_id': conversation.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def analyze_conversation(request):
    conversation_id = request.data.get('conversation_id')
    
    if not conversation_id:
        return Response({'error': 'conversation_id required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response({'error': 'conversation not found'}, status=status.HTTP_404_NOT_FOUND)

    messages = Message.objects.filter(conversation=conversation)
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
    analyses = ConversationAnalysis.objects.all()
    serializer = ConversationAnalysisSerializer(analyses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
