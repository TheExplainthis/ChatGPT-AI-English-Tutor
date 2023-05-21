# ChatGPT-AI-English-Tutor

[![license](https://img.shields.io/pypi/l/ansicolortags.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/TheExplainthis/ChatGPT-AI-English-Tutor)](https://github.com/TheExplainthis/ChatGPT-AI-English-Tutor/releases/)


## 介紹
本專案會利用 Whisper + GPT-3.5 + Google Text-To-Speech 打造一個 AI 英文家教老師，而老師也會去記錄學生的學習狀況，並定期的反思學生學習狀態，並給予較是適當的回饋與回覆給學生。

## Demo
![Demo](https://explainthis.s3-ap-northeast-1.amazonaws.com/3e77cc21083a4506990bb7bf4b46ff34.png)

## 安裝步驟
### Token 取得
1. 取得 OpenAI 給的 API Key
    1. [OpenAI](https://beta.openai.com/) 平台中註冊/登入帳號
    2. 右上方有一個頭像，點入後選擇 `View API keys`
    3. 點選中間的 `Create new secret key` -> 生成後即為 `OPENAI_API_KEY` （稍晚會用到）
    - 注意：每隻 API 有免費額度，也有其限制，詳情請看 [OpenAI Pricing](https://openai.com/api/pricing/)
2. 取得 LINE Token：
    1. 登入 [LINE Developer](https://developers.line.biz/zh-hant/)
    2. 創建機器人：
        1. 創建 `Provider` -> 按下 `Create`
        2. 創建 `Channel` -> 選擇 `Create a Messaging API channel`
        3. 輸入完必填的基本資料
        4. 輸入完成後，在 `Basic Settings` 下方，有一個 `Channel Secret` -> 按下 `Issue`，生成後即為 `LINE_CHANNEL_SECRET` （稍晚會用到）
        5. 在 `Messaging API` 下方，有一個 `Channel access token` -> 按下 `Issue`，生成後即為 `LINE_CHANNEL_ACCESS_TOKEN` （稍晚會用到）
3. 取得 Google Text-To-Speech API
    1. 註冊/登入 [Google Cloud Platform](https://console.cloud.google.com/)
    2. 登入後點擊左上方 `下拉式選項`，並點擊 `新增專案`。
    3. 輸入完 `專案名稱`、選擇完 `機構` 後，就可以按下 `建立`
    4. 上方搜尋列表輸入 `Cloud Text-To-Speech API` ，選擇下方 `MARKETPLACE` 的 `Cloud Text-To-Speech API` -> 點擊 `啟用`
    5. 上方搜尋列表輸入 `IAM` ，選擇 `IAM 與管理`
    6. 左邊選擇 `服務帳戶`，右邊選擇 `建立服務帳戶` 
    7. 任意輸入完帳號後，點擊 `完成`
    8. 建立完成後，在該帳號後面的 ... 點擊後，選擇 `管理金鑰`
    9. 進入後，上方 `金鑰` 的地方，下方選擇 `建立新的金鑰`
    10. 選擇 `JSON` 格式，並點擊 `建立` -> 此時會下載一份 `credential.json` 請保存好，稍待會會用到。

### 專案設置
1. Fork Github 專案：
    1. 註冊/登入 [GitHub](https://github.com/)
    2. 進入 [ChatGPT-AI-English-Tutor](https://github.com/TheExplainthis/ChatGPT-AI-English-Tutor)
    3. 點選 `Star` 支持開發者
    4. 點選 `Fork` 複製全部的程式碼到自己的倉庫
2. 部署（免費空間）：
    1. 進入 [replit](https://replit.com/)
    2. 註冊登入一個帳號
    3. 將 [專案](https://replit.com/@TheExplainthis/ChatGPT-AI-English-Tutor) Fork 回去 

### 專案執行
1. 環境變數設定
    1. 接續上一步 `Fork` 完成後在 `Replit` 的專案管理頁面左下方 `Tools` 點擊 `Secrets`。
    2. 右方按下 `Open raw editor` ，此時可以直接新增 json 格式進去，請直接複製剛剛的 `crenditial.json` 例如:
        ```
        {
       "type": "service_account",
        "project_id": "ai-english-tutor",
        "private_key_id": "2f79XXXXXXXXXXXXXbd2",
        "private_key": "-----BEGIN PRIVATE KEY---- XXXXXXX",
        "client_email": "teacher@XXXXX.gserviceaccount.com",
        "client_id": "115XXXXXXXXXXX20",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.gooXXXXX",
        "client_x509_cert_url": "https://www.gooXXXXXXX"
        }
        ```
    3. 再新增另外三個環境變數，需新增：
        1. 欲選擇的模型：
            - key: `OPENAI_API_KEY`
            - value: `[由步驟一取得]`  
        2. Line Channel Secret:
            - key: `LINE_CHANNEL_SECRET`
            - value: `[由步驟一取得]`
        3. Line Channel Access Token:
            - key: `LINE_CHANNEL_ACCESS_TOKEN`
            - value: `[由步驟一取得]`
    
2. 開始執行
    1. 點擊上方的 `Run`
    2. 成功後右邊畫面會顯示 `Hello World`，並將畫面中上方的**網址複製**下來
    3. 回到 Line Developer，在 `Messaging API` 下方的 `Webhook URL` 江上方網址貼過來，並加上 `/callback` 例如：`https://ChatGPT-AI-English-Tutor.explainthis.repl.co/callback`
    4. 打開下方的 `Use webhook`
    5. 將下方 `Auto-reply messages` 關閉
    - 注意：若一小時內沒有任何請求，則程式會中斷，因此需要下步驟
3. CronJob 定時發送請求
    1. 註冊/登入 [cron-job.org](https://cron-job.org/en/)
    2. 進入後面板右上方選擇 `CREATE CRONJOB`
    3. `Title` 輸入 `ChatGPT-AI-English-Tutor`，網址輸入上一步驟的網址，例如：`https://ChatGPT-AI-English-Tutor.explainthis.repl.co/`
    4. 下方則每 `5 分鐘` 打一次
    5. 按下 `CREATE`

## 如何客製化修改？
1. `main.py` 中第 86 - 96 行的提示詞，用途是針對學生的問題，要怎麼去回應，可以依據不同的情境去做設定，像是某部分的學生很常用中文問問題，有部分的學生可能很需要老師修改他的英文文法等，大家可以自行嘗試不同的提示詞，可能會有不同效果。
2. `main.py` 中第 59 - 73 行的提示詞，用途在於老師會每 10 次回覆後做一次反思，反思這個學生是否有進步，以及反思自己是否有給出好的引導與回應，並適時地做調整，大家可以自行嘗試不同的提示詞，可能會有不同的效果。

## 支持我們
如果你喜歡這個專案，願意[支持我們](https://www.buymeacoffee.com/explainthis)，可以請我們喝一杯咖啡，這會成為我們繼續前進的動力！

[<a href="https://www.buymeacoffee.com/explainthis" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="45px" width="162px" alt="Buy Me A Coffee"></a>](https://www.buymeacoffee.com/explainthis)


## 授權
[MIT](LICENSE)