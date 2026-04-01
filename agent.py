import os
import sys
import requests
from dotenv import load_dotenv
from duckduckgo_search import DDGS
import google.generativeai as genai

# 讀取 .env 檔案
load_dotenv()

# 確保已經設定 GEMINI_API_KEY
if not os.environ.get("GEMINI_API_KEY"):
    print("錯誤: 請在 .env 檔案中設定 GEMINI_API_KEY")
    sys.exit(1)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_weather(city: str) -> str:
    """查詢目的地的即時溫度與天氣狀態"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data['current_condition'][0]
        temp_c = current['temp_C']
        desc = current['weatherDesc'][0]['value']
        return f"{temp_c}°C，{desc}"
    except Exception as e:
        return f"天氣查詢錯誤: {e}"

def search_places(city: str) -> str:
    """利用 duckduckgo 搜尋當地熱門景點，例如輸入城市名"""
    query = f"{city} 景點"
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            if results:
                places = [res.get('title', '').split('|')[0].strip() or res.get('body', '')[:20] for res in results]
                return "、".join(places)
            return "查無相關景點"
    except Exception as e:
        return f"搜尋錯誤: {e}"

def get_advice() -> str:
    """取得一則出發前的人生建議（旅行格言），回傳為英文建議字串"""
    try:
        response = requests.get("https://api.adviceslip.com/advice", timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['slip']['advice']
    except Exception as e:
        return f"隨機建議取得錯誤: {e}"

def generate_travel_brief(city: str):
    print(f"正在透過 Agent 產生 {city} 的行前簡報...\n")
    
    # 初始化 Gemini Model 並將函數當作工具傳入
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        tools=[get_weather, search_places, get_advice],
        system_instruction="""你是一個「旅遊前哨站」AI Agent。
請利用提供的 Tools，依序查詢使用者的目的地：
1. 即時天氣
2. 熱門景點
3. 取得一則隨機的人生建議（需翻譯為繁體中文）

最後，請【嚴格】遵守以下格式輸出「行前簡報」（不要加上 Markdown 的程式碼區塊符號，直接輸出純文字即可）：

=== {city} 行前簡報 ===

[天氣]  (帶入天氣與溫度，簡短補充是否適合戶外活動)

[景點]  (帶入景點清單)

[提醒]  (帶入提醒與翻譯後的格言)"""
    )

    # 啟用自動調用函數的聊天模式
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    prompt = f"請幫我產出一份 {city} 的行前簡報"
    
    try:
        response = chat.send_message(prompt)
        print("\n\n" + "-"*40 + "\n")
        print(response.text.strip())
        print("\n" + "-"*40 + "\n")
    except Exception as e:
        print(f"產生簡報時發生錯誤: {e}")

if __name__ == "__main__":
    target_city = input("請輸入您想去的城市 (例如 Tokyo, Taipei)：").strip()
    if not target_city:
        target_city = "Tokyo"
    generate_travel_brief(target_city)
