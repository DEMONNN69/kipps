from rest_framework import serializers
from .models import Message, Conversation, ConversationAnalysis


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'created_at']
        read_only_fields = ['created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'messages', 'message_count']
        read_only_fields = ['created_at']

    def get_message_count(self, obj):
        return obj.get_message_count()


class ConversationAnalysisSerializer(serializers.ModelSerializer):
    conversation_title = serializers.CharField(source='conversation.title', read_only=True)

    class Meta:
        model = ConversationAnalysis
        fields = '__all__'
        read_only_fields = ['created_at']

