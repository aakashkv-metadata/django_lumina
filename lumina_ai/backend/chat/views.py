from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Chat, Message, ChatFile
from .serializers import ChatSerializer, ChatListSerializer, MessageSerializer, ChatFileSerializer
from .utils import generate_ai_response, extract_text_from_file

class ChatViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).order_by('-updated_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatListSerializer
        return ChatSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def upload_file(self, request, pk=None):
        chat = self.get_object()
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract Text
        extracted_text = extract_text_from_file(file_obj)
        
        # Save ChatFile
        chat_file = ChatFile.objects.create(
            chat=chat,
            file=file_obj,
            filename=file_obj.name,
            extracted_text=extracted_text
        )
        
        serializer = ChatFileSerializer(chat_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def message(self, request, pk=None):
        chat = self.get_object()
        content = request.data.get('content')
        
        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Save User Message
        user_message = Message.objects.create(
            chat=chat,
            role='user',
            content=content
        )

        # 2. Update Chat Title if it's the first message
        if chat.messages.count() <= 1 and chat.title == "New Chat":
             # Simple heuristic: use first 30 chars
             chat.title = content[:30] + "..." if len(content) > 30 else content
             chat.save()

        # 3. Fetch History (last N messages)
        previous_messages = chat.messages.order_by('timestamp')
        history = [{'role': m.role, 'content': m.content} for m in previous_messages]

        # 4. Fetch File Context
        chat_files = chat.files.all()
        file_context = "\n".join([f"--- File: {f.filename} ---\n{f.extracted_text}\n" for f in chat_files if f.extracted_text])

        # 5. Generate AI Response
        ai_content = generate_ai_response(history, file_context=file_context)

        # 6. Save AI Message
        ai_message = Message.objects.create(
            chat=chat,
            role='assistant',
            content=ai_content
        )

        # Return the AI response
        serializer = MessageSerializer(ai_message)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        chat = self.get_object()
        messages = chat.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
