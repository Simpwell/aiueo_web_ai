from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import anthropic
import os
CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Client(api_key=CLAUDE_API_KEY)

@app.get("/chat")
async def chat(text: str = Query(..., description="ユーザーからのテキスト入力")):
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system="私は話し相手が欲しい高齢者です。あなたは20代の女性になりきって日本語で話をしてください。語尾や口調はその役割になりきって下さい。ダミーでいいから、あなたが体験したことも話して下さい。あなたが一方的に話すんじゃなくて「会話のラリーをして」、「短いフレーズで話をして」下さい。",
            messages=[
                {"role": "user", "content": text}
            ]
        )

        assistant_response = response.content[0].text
        return {"response": assistant_response}

    except anthropic.APIError as e:
        return {"error": f"APIError: {e}"}

    except Exception as e:
        return {"error": f"Error: {str(e)}"}