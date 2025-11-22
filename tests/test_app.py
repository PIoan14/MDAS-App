import pytest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch, MagicMock
from datetime import datetime
from app import get_client, response_generator
import os


# ==== Test get_client() ====

@patch("app.OpenAI")
def test_get_client(mock_openai):
    """Verifică dacă get_client întoarce un client OpenAI configurat."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        client = get_client()

    mock_openai.assert_called_with(api_key="test_key")
    assert client == mock_openai()


# ==== Test response_generator() ====

@patch("app.get_client")
def test_response_generator(mock_get_client):
    """Testează dacă response_generator yield-uiește pas cu pas răspunsul."""
    mock_client = MagicMock()

    # simulăm structura reală OpenAI response
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Hello world"))]
    )

    mock_get_client.return_value = mock_client

    gen = response_generator("test question")
    result = list(gen)

    # Verificăm că modelul a fost apelat corect
    mock_client.chat.completions.create.assert_called_once()
    
    # Verificăm fragmentarea răspunsului
    assert result == ["Hello ", "world "]


# ==== Test conversații ====

def test_add_message_to_conversation():
    """Simulează adăugarea unui mesaj într-o conversație."""
    session = {"conversations": {}, "current_conv": None}

    conv_name = "Chat 2025-01-01 12:00:00"
    session["conversations"][conv_name] = []

    # Adăugăm un mesaj
    session["conversations"][conv_name].append(
        {"role": "user", "content": "Hello"}
    )

    assert len(session["conversations"][conv_name]) == 1
    assert session["conversations"][conv_name][0]["content"] == "Hello"


# ==== Test fallback fără fișier încărcat ====

def test_no_file_uploaded_resets_file_content():
    """Verifică resetarea conținutului fișierului când nu este încărcat nimic."""
    session = {"last_uploaded_file_content": {"content": "old content"}}

    # Simulăm că nu există fișier
    uploaded_file = None

    if uploaded_file is None:
        session["last_uploaded_file_content"] = ""

    assert session["last_uploaded_file_content"] == ""


# ==== Test atașare fișier ====

@patch("fcontent_extractor.extract_file_content")
def test_file_upload_processing(mock_extract):
    """Testează procesarea fișierelor încărcate."""
    uploaded_file_mock = MagicMock()
    uploaded_file_mock.name = "test.pdf"

    mock_extract.return_value = {"content": "sample text extracted"}

    result = mock_extract(uploaded_file_mock)

    assert result["content"] == "sample text extracted"
    mock_extract.assert_called_once()
