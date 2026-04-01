import sys
import requests


def get_travel_tips(country_name: str) -> str:
    """
    根據國家名稱查詢旅遊注意事項，包含安全等級、當地貨幣、語言、時區等資訊。
    使用 REST Countries API 與 Travel Advisory API。
    """
    try:
        # --- Step 1: 透過 REST Countries API 取得國家基本資料 ---
        countries_url = f"https://restcountries.com/v3.1/name/{country_name}"
        countries_resp = requests.get(countries_url, timeout=10)
        countries_resp.raise_for_status()
        countries_data = countries_resp.json()

        if not countries_data:
            return f"查無 {country_name} 的國家資料，請改用英文國家名稱（如 Japan、France）"

        info = countries_data[0]
        country_code = info.get("cca2", "").upper()

        # 貨幣
        currencies = info.get("currencies", {})
        currency_str = "、".join(
            f"{v.get('name', k)} ({k})" for k, v in currencies.items()
        ) if currencies else "未知"

        # 語言
        languages = info.get("languages", {})
        lang_str = "、".join(languages.values()) if languages else "未知"

        # 時區
        timezones = info.get("timezones", ["未知"])
        timezone_str = timezones[0] if timezones else "未知"

        # 電話國碼
        idd = info.get("idd", {})
        phone_code = idd.get("root", "") + (idd.get("suffixes", [""])[0] if idd.get("suffixes") else "")

        # --- Step 2: 透過 Travel Advisory API 取得安全公告 ---
        advisory_url = f"https://www.travel-advisory.info/api?countrycode={country_code}"
        advisory_resp = requests.get(advisory_url, timeout=10)
        advisory_resp.raise_for_status()
        advisory_data = advisory_resp.json()

        advisory_info = advisory_data.get("data", {}).get(country_code, {})
        advisory = advisory_info.get("advisory", {})
        score = advisory.get("score", None)
        message = advisory.get("message", "")

        # 將分數轉換為風險等級文字
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

        result = (
            f"[安全等級] {risk_level}\n"
            f"[當地貨幣] {currency_str}\n"
            f"[通用語言] {lang_str}\n"
            f"[主要時區] {timezone_str}\n"
            f"[國際電話] {phone_code if phone_code else '未知'}\n"
            f"[安全公告] {advisory_text}"
        )
        return result

    except requests.exceptions.HTTPError as e:
        return f"找不到國家資料，請使用英文國家名稱（如 Japan、France）：{e}"
    except Exception as e:
        return f"旅遊注意事項查詢錯誤：{e}"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(get_travel_tips(sys.argv[1]))
    else:
        print("Usage: python get_travel_tips.py <country_name>")
        print("Example: python get_travel_tips.py Japan")
