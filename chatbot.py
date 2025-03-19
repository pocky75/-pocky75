import requests

# Hugging Face API 토큰
API_TOKEN = ''  # 여기에 발급받은 Hugging Face API 토큰을 넣으세요
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Hugging Face에서 사용할 모델
MODEL = "facebook/blenderbot-1B-distill"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

def get_response_from_huggingface(user_input):
    data = {"inputs": user_input}
   
    try:
        # API 요청을 보냄
        response = requests.post(API_URL, headers=HEADERS, json=data)
        
        # API 응답 코드와 데이터를 출력하여 디버깅
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.json()}")  # 응답을 JSON 형식으로 출력
        
        if response.status_code == 200:
            try:
                return response.json()[0]["generated_text"]
            except (IndexError, KeyError):
                return "응답을 처리하는데 오류가 발생했습니다. 다시 시도해주세요."
        elif response.status_code == 403:
            return "Error 403: 권한이 없습니다. API 토큰을 확인하세요."
        else:
            return f"Error: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return f"요청 중 오류가 발생했습니다: {e}"

def chat():
    print("챗봇과 대화를 시작합니다. 종료하려면 'exit'을 입력하세요.")
   
    while True:
        user_input = input("나: ")
       
        if user_input.lower() == "exit":
            print("대화를 종료합니다.")
            break
       
        # Hugging Face 모델을 통해 챗봇의 응답을 얻음
        bot_response = get_response_from_huggingface(user_input)
       
        print("챗봇: " + bot_response)

if __name__ == "__main__":
    chat()