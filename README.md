# AI agent 開發分組實作

> 課程：AI agent 開發 — Tool 與 Skill
> 主題： 旅遊前哨站 

---

## Agent 功能總覽

> 說明這個 Agent 能做什麼，使用者可以輸入哪些指令

| 使用者輸入   | Agent 行為                             | 負責組員 |
| ------------ | -------------------------------------- | -------- |
| （例：天氣） | 呼叫 weather_tool，查詢即時天氣        | 吳宸宇         |
| （例：景點） | 呼叫 search_tool，搜尋熱門景點         |   林富閎       |
| （例：建議） | 呼叫 advice_tool，取得隨機建議         | 張承新         |
| （例：出發） | 執行 trip_briefing Skill，產出行前簡報 |  張承新           |

---

## 組員與分工


| 姓名 | 負責功能     | 檔案        | 使用的 API |
| ---- | ------------ | ----------- | ---------- |
| 吳宸宇 | 查詢即時天氣     | `tools/get_weather`  |https://wttr.in/{city}?format=j1            |
|林富閎 | 搜尋熱門景點  | `search_attractions_tools/`  | pip install duckduckgo-search      |
| 張承新     | 給建議             | `tools/get_advice`  |   https://api.adviceslip.com/advice         |
|張承新       | Skill 整合   | `skills/` | —         |
| 吳宸宇     | Agent 主程式 | `main.py` | —         |

---

## 專案架構


```
├── tools/
│   ├── get_advice.py       # 呼叫 API 取得每日隨機格言 / 生活建議
│   ├── get_weather.py      # 查詢目的地的即時天氣與溫度
│   └── search_places.py    # 使用 DuckDuckGo 搜尋當地的熱門景點
├── skills/
│   └── travel_outpost/
│       └── SKILL.md        # 定義 Agent 行為、呼叫邏輯與報告輸出格式的技能指令
├── agent.py                # 專案主程式 (AI Agent 核心思考邏輯)
├── requirements.txt        # 專案相依套件清單
├── .env                    # 本機環境變數 (存放您的 API Key，不被 commit)
├── .gitignore              # Git 忽略清單 (確保安全與乾淨)
└── README.md               # 您現在正在看的說明文件
```
---

## 使用方式

範例：

```bash
# 1. 建立虛擬環境
python3 -m venv .venv
# 2. 啟動虛擬環境
source .venv/bin/activate  # Windows 系統請改用 .\.venv\Scripts\activate
# 3. 安裝所需套件
pip install -r requirements.txt
# 4. 設定您的環境變數 (請在資料夾中建立 .env 檔案)
# 並且在檔案內加入您的 API Key：
# GEMINI_API_KEY=您的_Google_GenAI_金鑰
# 5. 執行主程式
python agent.py
```

---

## 執行結果

> 貼上程式執行的實際範例輸出


<img width="523" height="62" alt="image" src="https://github.com/user-attachments/assets/c6e706e9-a667-4e6b-ab24-a945e7b9d44f" />
<img width="1107" height="198" alt="image" src="https://github.com/user-attachments/assets/83d96398-030e-4d84-bbe5-9c6b2415fd2c" />




---

## 各功能說明

### [功能名稱]（負責：姓名）

- **Tool 名稱**： advice_tool
- **使用 API**： Advice Slip JSON API (或是內建的隨機語錄庫)
- **輸入**： query (可選的主題或關鍵字)
- **輸出範例：**

```python
ADVICE_TOOL = {
    "name": "advice_tool",
    "description": "取得一句隨機的生活建議、名言或心靈雞湯。當使用者感到迷惘、遇到困難需要他人建議，或是單純想要聽一些有智慧的中肯語錄時，請呼叫此工具。",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "(選填) 希望獲得建議的特定主題或關鍵字 (例如：'love', 'life', 'work')。若使用者未特別指定，可以留空，系統將會回傳完全隨機的建議。"
            }
        },
        "required": []
    }
}

```

### [搜尋熱門景點]（負責：林富閎）

- **Tool 名稱**： search_attractions_tool
- **使用 API**： DuckDuckGo Search API (或 Google Places API / Google Search API)
- **輸入**：
location (字串, string): 欲查詢景點的地點或城市名稱（例如："台北"、"京都"、"冰島"）。
category (字串, string, 選填): 景點的分類或性質，預設為 "熱門景點"（其他例如："親子景點"、"室內景點"、"私房秘境" 等）。
- **輸出範例**：
```python
SEARCH_ATTRACTIONS_TOOL = {
    "name": "search_attractions_tool",
    "description": "搜尋指定地點或城市的熱門旅遊景點、秘境或地標。當使用者詢問任何與景點推薦、必去地方或旅遊行程規劃相關的問題時，請呼叫此工具。",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "欲查詢景點的地點或城市名稱，例如：'台北'、'京都'、'冰島'"
            },
            "query_type": {
                "type": "string",
                "description": "景點的分類、性質或關鍵字，例如：'熱門景點'、'親子景點'、'私房秘境'、'室內景點'。若使用者未特別指定，預設請帶入 '熱門景點'。",
                "default": "熱門景點"
            }
        },
        "required": ["location"]
    }
}
```

### [查詢即時天氣]（負責：吳宸宇）

- **Tool 名稱**：`get_weather`
- **使用 API**：`https://wttr.in/{city}?format=j1`
- **輸入**：`city` (字串格式，目標城市名稱)
- **輸出範例**：`18°C，Clear` 或 `22°C，Partly cloudy`

```python
TOOL = {
    "name": "get_weather",
    "description": "查詢目的地的即時溫度與天氣狀態",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "要查詢即時天氣的城市名稱，例如：'Tokyo'"
            }
        },
        "required": ["city"]
    }
}
```

### Skill：[Skill Travel Outpost]（負責：張承新）

- **組合了哪些 Tool**：`get_weather` (實時天氣)、`search_places` (景點搜尋)、`get_advice` (每日格言)
- **執行順序**：

```text
Step 1: 呼叫 get_weather → 取得 目標城市的實時溫度與天氣狀態
Step 2: 呼叫 search_places → 取得 該城市的前三名熱門旅遊景點
Step 3: 呼叫 get_advice → 取得 一則隨機的英文每日格言
Step 4: 組合輸出 → 產生 格式嚴格統一且翻譯成中文的「行前簡報」
```

## 心得

### 遇到最難的問題

**最困難的事：第三方工具庫 (LangChain) 的版本相容性問題**
在實作 Agent 的核心邏輯時，原先使用了 LangChain 的 `create_tool_calling_agent` 來將那幾個 Python 腳本封裝成 Agent 的 Tools。但因為使用者的環境中可能存在較舊版本的 LangChain，結果執行時直接丟出 `ImportError: cannot import name 'create_tool_calling_agent'`，導致 Agent 無法啟動。

**如何解決的：**
我立刻轉換思路，決定**捨棄過度複雜且版本更迭頻繁的 LangChain**，改為使用 Google 官方提供的原生命名空間套件 **`google-generativeai`** 來重構 `agent.py`。
透過它內建的 `enable_automatic_function_calling=True` 參數，我只需建立一個普通的 Python List 將 Function 傳給模型，模型就能完美且自動地完成所有 Tool 的呼叫循環，這不僅避開了相容性地雷，程式碼結構也變得更加輕量且容易維護！

### Tool 和 Skill 的差別

 Tool（工具）像「四肢」或「特化零件」： 它就是一段能夠連接外部世界或是進行單純資料運算的程式碼（例如：打 API 查天氣的腳本、用 DuckDuckGo 搜尋的函式）。給它特定輸入，它就生出對應結果，但本身自己並「不會思考」要在什麼時候使用自己。
 
 Skill（技能）像「大腦的神經網路」或「SOP 流程」： 它是一整包具有邏輯性與執行策略的知識與規範（例如 SKILL.md 或系統裡的 Prompt）。它讓 Agent 知道在收到類似「幫我規劃旅遊」這種模糊指令時，要如何思考、先呼叫什麼 Tool（先調天氣、再調景點），最後再把 Tool 的生硬產出「漂亮地包裹重組」成充滿情感的總結（行前簡報）！


### 如果再加一個功能

**我會增加一個「即時匯率換算 (Currency Exchange Rate)」Tool。**

**為什麼？**
因為對於要出國旅遊的人來說，除了確認天氣和景點之外，「當地的消費水準與匯率」絕對是最核心、最務實的需求之一。
如果有了匯率 Tool，Agent 可以自動偵測目的地的國家（例如輸入 Tokyo，Agent 就知道要查台幣對日幣的匯率），並在「行前簡報」中貼心加上這段提醒：
>`[匯率] 目前 1 TWD 約等於 4.7 JPY，近期日幣匯率划算，建議可多換一些現金備用！`

這個功能實作簡單（網路上有豐富的免費匯率 API），卻能極大地提升整份「行前簡報」的商業價值與旅行者的好感度！

