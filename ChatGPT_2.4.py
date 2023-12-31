import tkinter as tk
import openai
import datetime
import os
import threading
import pyttsx3
import speech_recognition as sr
import pyaudio

# 設定 OpenAI API 金鑰
openai.api_key = "請在這裡輸入您的 API KEY"

# 定義 ChatGPT 設定
chatgpt_engine = "text-davinci-003"
chatgpt_temperature = 0.7
chatgpt_max_tokens = 1024

#變數的指定
chat_history = []  #歷史紀錄的 list
folder_name = "chatlog"  # 要創建的資料夾名稱
chatgpt_output = ""
is_voiceout_enabled = False  # voiceout初始值為關閉

# 創建 tk 視窗
window = tk.Tk()
window.title("Chat with ChatGPT")
window.iconbitmap('image/chatgptico.ico')

# 創建 tk 視窗
title_frame = tk.Frame(window, background='#282828')
title_frame.grid(row=0, column=0, columnspan=2, sticky='we', padx=10, pady=10)

# 創建文字輸出框視窗
output_frame = tk.Frame(window, background='#282828')
output_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

# 創建卷軸
scrollbar = tk.Scrollbar(output_frame, highlightcolor='#282828')
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 創建文字框標題
output_label = tk.Label(title_frame, text="ChatGPT Response : ", foreground='white', background='#282828', font=("微軟黑正體", 14))
output_label.pack(side=tk.LEFT)

# 創建文字輸出框
output_text = tk.Text(output_frame, width=60, height=40, yscrollcommand=scrollbar.set, foreground='white', background='#282828', font=("微軟黑正體", 12))
output_text.configure(insertbackground='white')
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#綁定卷軸
scrollbar.config(command=output_text.yview)

# 創建輸入框視窗
input_frame = tk.Frame(window, background='#282828')
input_frame.grid(row=2, column=0, padx=10, pady=15, sticky='we')
# 創建輸入框標題
input_label = tk.Label(input_frame, text="Chat : ", foreground='white', background='#282828', font=("微軟黑正體", 14))
input_label.pack(side=tk.LEFT)
# 創建輸入框
input_text = tk.Entry(input_frame, font=("微軟黑正體", 14))
input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 創建按鈕
# 送訊息用
imgforsend = tk.PhotoImage(file="image/imgforsend.png").subsample(20,20)
button = tk.Button(input_frame, image=imgforsend)
button.pack(side=tk.LEFT, padx=(10, 0))
# 錄製音訊用
imgforrecd = tk.PhotoImage(file="image/imgforrecd.png").subsample(20,20)
button3 = tk.Button(input_frame, image=imgforrecd)
button3.pack(side=tk.LEFT, padx=(10, 0))
# 清除畫面用
imgforclean = tk.PhotoImage(file="image/imgforclean.png").subsample(20,20)
button4 = tk.Button(title_frame,image=imgforclean)
button4.pack(side=tk.RIGHT, padx=(10,0))
# 存檔聊天紀錄用
imgforsendsave = tk.PhotoImage(file="image/imgforsave.png").subsample(20,20)
button2 = tk.Button(title_frame,image=imgforsendsave)
button2.pack(side=tk.RIGHT, padx=(10, 0))

imgforvoice = tk.PhotoImage(file="image/imgforvoice.png").subsample(20,20)
button_voiceout = tk.Button(title_frame, image=imgforvoice)
button_voiceout.pack(side=tk.RIGHT, padx=(10, 0))

# 設置視窗的行列權重，讓元件可以隨著視窗大小調整
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)

# 設置元件的行列權重，讓元件可以隨著視窗大小調整
title_frame.columnconfigure(0, weight=1)
output_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=1)

window.configure(background='#282828')  #視窗背景顏色設定

# 使用 mkdir() 函數創建資料夾
try:
    os.mkdir(folder_name)
    print(f"資料夾 '{folder_name}' 創建成功。")
except FileExistsError:
    print(f"資料夾 '{folder_name}' 已經存在。")

# 定義 ChatGPT 函數
def chatgpt(input_text, output_text):
    global chat_history, chatgpt_output
    # 將對話歷史加入 prompt 中
    chat_history.append(input_text)
    chat_history_prompt = " ".join(chat_history[-3:])
    chatgpt_input = f"{chat_history_prompt}"

    # 請求 ChatGPT 回應
    response = openai.Completion.create(
        engine=chatgpt_engine,
        prompt=chatgpt_input,
        temperature=chatgpt_temperature,
        max_tokens=chatgpt_max_tokens
    )

    # 解析 ChatGPT 回應
    chatgpt_output = response.choices[0].text.strip()

    # 更新 GUI 輸出框
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, "\n-")
    output_text.insert(tk.END, f"\nChatGPT: {chatgpt_output}")
    output_text.see(tk.END)
    output_label.config(text="ChatGPT Response: ")

    # 將用戶輸入和 ChatGPT 的回應一起加入聊天歷史中
    chat_history.append(f"{chatgpt_output}")

    voiceout()

# 定義聲音輸出的函數
def voiceout():
    global is_voiceout_enabled  # 宣告使用全域變數

    if not is_voiceout_enabled:  # 如果關閉狀態就直接返回
        return

    # 設定聲音的輸出 #TW:HANHAN、HUIHUI #EN:DAVID、ZIRA
    message = chatgpt_output
    voiceengine = pyttsx3.init()
    voices = voiceengine.getProperty('voices')
    for voice in voices:
        if 'HANHAN' in voice.id:
            voiceengine.setProperty('voice', voice.id)
            voiceengine.setProperty('rate', 150)
    voiceengine.say(message)
    voiceengine.runAndWait()

# 定義開關 voiceout()
def toggle_voiceout():
    global is_voiceout_enabled  # 宣告使用全域變數
    is_voiceout_enabled = not is_voiceout_enabled  # 切換開關狀態
    if is_voiceout_enabled == True:
        output_text.insert(tk.END, "\n-")
        output_text.insert(tk.END, "\n回應語音已開啟")
    else:
        output_text.insert(tk.END, "\n-")
        output_text.insert(tk.END, "\n回應語音已關閉")

# 下方函數的防當機函數
def start_recording():
    t = threading.Thread(target=record)
    t.start()

# 定義聲音輸入函數
def record():
    r = sr.Recognizer()
    r.energy_threshold = 3000
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1
    r.operation_timeout = None
    r.non_speaking_duration = 0.5
    vtext=None
    print("請說點甚麼...")
    output_text.insert(tk.END, "\n請說點甚麼...")
    with sr.Microphone() as source:
        audio = r.listen(source, phrase_time_limit=5)
    try:
        vtext = r.recognize_google(audio, language='zh-TW')  #zh-TW、en-US
        input_text.insert(tk.END, vtext)
    except sr.UnknownValueError:
        output_text.insert(tk.END, "\n\nGoogle Speech Recognition 無法識別")
    except sr.RequestError as e:
        output_text.insert(tk.END, "\n\n無法從 Google Speech Recognition 取得資料: {0}".format(e))
    finally:
        if vtext is None:
            output_text.insert(tk.END, "，請確認音訊輸入裝置")
        elif vtext == "存檔":
            on_save()
        elif vtext == "清空":
            on_clean()
        else:
            button_click()

# 下方函數的防當機函數
def start_voice():
    t2 = threading.Thread(target=voiveopen)
    t2.start()

# 長時間開啟麥克風 先不開了
def voiveopen():
    # 設定麥克風
    p = pyaudio.PyAudio()
    mic = sr.Microphone(device_index=0, sample_rate=16000, chunk_size=1024)

    # 設定語音辨識器
    r = sr.Recognizer()

    # 不斷聆聽使用者的語音
    while True:
        try:
            # 聆聽使用者的語音
            print("Please say something...")
            with mic as source:
                audio = r.listen(source, phrase_time_limit=5)

            # 辨識使用者的語音
            text = r.recognize_google(audio, language="zh-TW")
            print("You said: " + text)

            # 根據使用者說的話來執行相應的函數
            if text == "哈囉，涵涵":
                output_text.insert(tk.END, "請問需要甚麼幫助 ?")
                record()
                pass
            elif text == "存檔":
                on_save()
            elif text == "停止監聽":
                break
            else:
                output_text.insert(tk.END, "抱歉，請再說一次")
                print("Sorry, I don't understand.")
        except sr.UnknownValueError:
            print("Sorry, could not understand your voice.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    p.terminate() #關閉麥克風

# 定義送出按鈕函數
def button_click():
    # 等待回應故修改 ChatGPT Response: 
    output_label.config(text="ChatGPT Response: 對方輸入中...")
    
    # 讀取輸入文本
    input_text_str = input_text.get() + "(請用中文回答)"

    # 清空輸入框
    input_text.delete(0, tk.END)

    # 更新 GUI 輸出框
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, "\n-")
    output_text.insert(tk.END, f"\nYou: {input_text_str}")
    output_text.see(tk.END)
    output_text.config(state=tk.DISABLED)

    # 啟動 ChatGPT 函數
    threading.Thread(target=chatgpt, args=(input_text_str, output_text)).start()

# 定義存檔以及清空按鈕函數
def on_save():
    global chat_history
    # 獲取當前日期與時間
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    # 將聊天紀錄寫入以日期與時間為名的檔案中
    file_name = f"chatlog/chat_history_{date_time}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(chat_history))

    output_text.delete('1.0', tk.END)
    chat_history.clear()
    output_text.insert(tk.END, "已儲存")

# 清空不存檔畫面函數
def on_clean():
    output_text.delete('1.0', tk.END)
    chat_history.clear()
    output_text.insert(tk.END, "已清空")

#定義關閉時存檔函數
def on_closing():
    # 獲取當前日期與時間
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    # 將聊天紀錄寫入以日期與時間為名的檔案中
    file_name = f"chatlog/chat_history_{date_time}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(chat_history))

    window.destroy()

# 指定按鈕動作
button.config(command=button_click)
button2.config(command=on_save)
button3.config(command=start_recording)
button4.config(command=on_clean)
button_voiceout.config(command=toggle_voiceout)

# 綁定硬體快捷鍵
window.bind('<Return>', lambda event=None: button.invoke())
window.bind('<F1>', lambda event=None: start_recording())
window.bind('<F2>', lambda event=None: toggle_voiceout())
window.bind('<F3>', lambda event=None: button2.invoke())
window.bind('<F4>', lambda event=None: on_clean())

#執行將聊天紀錄寫入檔案中的動作
window.protocol("WM_DELETE_WINDOW", on_closing)

#啟動 tk 視窗循環
window.mainloop()
