# Azure AI Translator 서비스를 활용한 웹 채팅 어플리케이션 번역 서버 개발 프로젝트

1. 번역 기능 : Azure AI Translator의 Text 번역 기능
2. 웹 서버 프레임워크 : FAST API
3. 테스트 클라이언트 : HTML
4. 웹 통신 : WebSocket

# 실행 방법

1. PYTHON 가상환경 설치

2. Config Azure key, region, endpoint 설정
- azure_config:
  key: your_azure_key_here
  endpoint: your_azure_endpoint_here
  location: your_azure_location_here

3. LOCAL 서버에서 uvicorn 명령어 실행

uvicorn websocket_fastapi_translator:app --reload


# HTML UI

![image](https://github.com/user-attachments/assets/7777a1da-22c1-4fd9-a539-a2e86142e1b7)
