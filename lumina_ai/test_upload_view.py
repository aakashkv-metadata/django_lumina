
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumina.settings')
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from chat.models import Chat
from django.contrib.auth import get_user_model

def test_upload_view():
    print("Testing Upload View...")
    User = get_user_model()
    user, _ = User.objects.get_or_create(username='testuser_view', defaults={'email': 'test_view@example.com'})
    user.set_password('password')
    user.save()
    
    # Authenticate
    client = APIClient()
    client.force_authenticate(user=user)
    
    # Create Chat
    chat = Chat.objects.create(user=user, title="Upload View Test")
    
    # Create Dummy File
    file_content = b"Content for upload test"
    uploaded_file = SimpleUploadedFile("test_api.txt", file_content, content_type="text/plain")
    
    # Upload
    url = f'/api/chats/{chat.id}/upload_file/'
    response = client.post(url, {'file': uploaded_file}, format='multipart')
    
    print(f"Response Status: {response.status_code}")
    print(f"Response Data: {response.data}")
    
    if response.status_code == 201:
        print("Upload Successful!")
    else:
        print("Upload Failed!")

if __name__ == "__main__":
    test_upload_view()
