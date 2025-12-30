
import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumina.settings')
django.setup()

from chat.models import Chat, ChatFile

def test_chat_file_model():
    print("Testing ChatFile model...")
    # Create a dummy chat
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Ensure a user exists
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    if created:
        user.set_password('password')
        user.save()
        
    chat = Chat.objects.create(user=user, title="File Test Chat")
    
    # Create a dummy file
    file_content = b"Hello world, this is a test file content."
    uploaded_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")
    
    # Create ChatFile
    chat_file = ChatFile.objects.create(
        chat=chat,
        file=uploaded_file,
        filename="test.txt",
        extracted_text="Hello world, this is a test file content."
    )
    
    print(f"ChatFile created: {chat_file}")
    print(f"Extracted Text: {chat_file.extracted_text}")
    print("ChatFile model test passed!")

if __name__ == "__main__":
    test_chat_file_model()
