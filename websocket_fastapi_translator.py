from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel, Field
import requests, uuid, yaml, os


# FastAPI 서버를 만들고 Swagger 문서용 제목 설정
app = FastAPI(
    title="Azure Translator WebSocket API",
    description="실시간 번역을 WebSocket으로 처리하는 FastAPI 서버",
    version="1.0.0"
)

# config.yaml 로드
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')
with open(config_path, "r", encoding="utf-8") as file:
    configs = yaml.safe_load(file)

key = configs["azure_config"]["key"]
endpoint = configs["azure_config"]["endpoint"]
location = configs["azure_config"]["location"]

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
}

@app.get("/")
def read_root():
    return {"message": "WebSocket 기반 Azure Translator 서버입니다."}

@app.websocket("/ws/translate")
async def websocket_translate(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            text = data.get("text")
            to_langs = data.get("to", ["en"])

            if not text:
                await websocket.send_json({"error": "'text' 값이 필요합니다."})
                continue

            url = endpoint + "/translate"
            params = {
                'api-version': '3.0',
                'to': to_langs
            }
            body = [{"text": text}]

            try:
                response = requests.post(url, params=params, headers={**headers, 'X-ClientTraceId': str(uuid.uuid4())}, json=body)
                result = response.json()

                if isinstance(result, dict) and "error" in result:
                    await websocket.send_json({"error": result["error"]["message"]})
                else:
                    await websocket.send_json({
                        "original": text,
                        "detectedLanguage": result[0].get("detectedLanguage", {}).get("language", "unknown"),
                        "translations": result[0].get("translations", [])
                    })
            except Exception as e:
                await websocket.send_json({"error": str(e)})

    except WebSocketDisconnect:
        print("WebSocket 클라이언트 연결 종료됨.")
    except Exception as e:
        await websocket.send_json({"error": str(e)})
