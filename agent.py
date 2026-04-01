import os
import sys
import time
import requests
from dotenv import load_dotenv
from ddgs import DDGS
from google import genai
from google.genai import types

# 讀取 .env 檔案
load_dotenv()

# 確保已經設定 GEMINI_API_KEY
if not os.environ.get("GEMINI_API_KEY"):
    print("錯誤: 請在 .env 檔案中設定 GEMINI_API_KEY")
    sys.exit(1)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

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

def get_travel_tips(country_name: str) -> str:
    """根據英文國家名稱查詢旅遊注意事項，包含安全等級、當地貨幣、語言、時區與官方安全公告"""
    try:
        # Step 1: 透過 REST Countries API 取得國家基本資料
        countries_url = f"https://restcountries.com/v3.1/name/{country_name}"
        countries_resp = requests.get(countries_url, timeout=10)
        countries_resp.raise_for_status()
        countries_data = countries_resp.json()

        if not countries_data:
            return f"查無 {country_name} 的國家資料"

        info = countries_data[0]
        country_code = info.get("cca2", "").upper()

        currencies = info.get("currencies", {})
        currency_str = "、".join(
            f"{v.get('name', k)} ({k})" for k, v in currencies.items()
        ) if currencies else "未知"

        languages = info.get("languages", {})
        lang_str = "、".join(languages.values()) if languages else "未知"

        timezones = info.get("timezones", ["未知"])
        timezone_str = timezones[0] if timezones else "未知"

        idd = info.get("idd", {})
        phone_code = idd.get("root", "") + (idd.get("suffixes", [""])[0] if idd.get("suffixes") else "")

        # Step 2: 透過 Travel Advisory API 取得安全公告
        advisory_url = f"https://www.travel-advisory.info/api?countrycode={country_code}"
        advisory_resp = requests.get(advisory_url, timeout=10)
        advisory_resp.raise_for_status()
        advisory_data = advisory_resp.json()

        advisory_info = advisory_data.get("data", {}).get(country_code, {})
        advisory = advisory_info.get("advisory", {})
        score = advisory.get("score", None)
        message = advisory.get("message", "")

        if score is not None:
            try:
                score_float = float(score)
                if score_float < 2.0:
                    risk_level = f"✅ 低風險（{score}/5），適合旅遊"
                elif score_float < 3.0:
                    risk_level = f"⚠️ 中低風險（{score}/5），一般注意即可"
                elif score_float < 4.0:
                    risk_level = f"⚠️ 中高風險（{score}/5），請隨時保持警覺"
                else:
                    risk_level = f"🚫 高風險（{score}/5），非必要請勿前往"
            except (ValueError, TypeError):
                risk_level = "風險等級未知"
        else:
            risk_level = "風險等級資料不足"

        advisory_text = message.strip() if message.strip() else "目前無特別安全公告"

        return (
            f"[安全等級] {risk_level}\n"
            f"[當地貨幣] {currency_str}\n"
            f"[通用語言] {lang_str}\n"
            f"[主要時區] {timezone_str}\n"
            f"[國際電話] {phone_code if phone_code else '未知'}\n"
            f"[安全公告] {advisory_text}"
        )
    except requests.exceptions.HTTPError:
        return f"查無 {country_name} 的資料，請使用英文國家名稱（如 Japan、France）"
    except Exception as e:
        return f"旅遊注意事項查詢錯誤：{e}"

def generate_travel_brief(city: str):
    print(f"正在透過 Agent 產生 {city} 的行前簡報...\n")
    print("為避免觸發免費 API 頻率限制，程式暫停 5 秒等待配額恢復...")
    time.sleep(5)

    system_prompt = """你是一個「旅遊前哨站」AI Agent。
請利用提供的 Tools，依序查詢使用者的目的地：
1. 即時天氣（呼叫 get_weather，傳入城市名稱）
2. 熱門景點（呼叫 search_places，傳入城市名稱）
3. 取得一則隨機的人生建議（呼叫 get_advice，需翻譯為繁體中文）
4. 旅遊注意事項（呼叫 get_travel_tips，傳入該城市所屬的英文國家名稱，例如東京→Japan、台北→Taiwan）

最後，請【嚴格】遵守以下格式輸出「行前簡報」（不要加上 Markdown 的程式碼區塊符號，直接輸出純文字即可）：

=== {city} 行前簡報 ===

[天氣]  (帶入天氣與溫度，簡短補充是否適合戶外活動)

[景點]  (帶入景點清單)

[提醒]  (帶入提醒與翻譯後的格言)

[注意事項]
(依序帶入 get_travel_tips 回傳的安全等級、當地貨幣、語言、時區、電話國碼與安全公告，每項各佔一行)"""

    chat = client.chats.create(
        model="gemini-3.1-flash-lite-preview",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[get_weather, search_places, get_advice, get_travel_tips],
        ),
    )

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
