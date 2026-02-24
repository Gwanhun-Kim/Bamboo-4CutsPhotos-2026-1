import os
import time
import threading
import shutil
import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
import sys
import cv2
import tkinter as tk

# [기존 모듈 경로 설정]
sys.path.append(os.path.join(os.path.dirname(__file__), 'addPhotos2Frame'))
try:
    import addPhotos2Frame
except ImportError:
    print("⚠️ addPhotos2Frame 모듈을 찾을 수 없습니다.")

# [1. 경로 및 설정]
BASE_PATH = "/Users/kimgwanhun/Desktop/Pictures/밤부/26-1/가두모집/인생네컷"
WATCH_DIR = os.path.join(BASE_PATH, "Bamboo_Studio")
RESULT_ROOT = os.path.join(BASE_PATH, "Bamboo_Results")
RAW_STORAGE_DIR = os.path.join(RESULT_ROOT, "Raw_Storage")
CLOUD_ZIP_DIR = os.path.join(RESULT_ROOT, "Cloud_Upload")

for d in [WATCH_DIR, RAW_STORAGE_DIR, CLOUD_ZIP_DIR]:
    if not os.path.exists(d): os.makedirs(d)

FRAME_PATH = os.path.join(BASE_PATH, "assets/밤부_인생네컷_최종mk4.png")
LOGO_PATH = os.path.join(BASE_PATH, "assets/bamboo_logo.jpeg")
CLOUD_LINK = "https://drive.google.com/drive/folders/1P7M1o9lTkkPwL754xjDONYqGOLlX04Fd?hl=ko"
TOTAL_SHOTS = 4
PRINTER_NAME = "Canon_CP1500"

class BambooApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BAMBOO STUDIO v4.2")
        
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        ctk.set_appearance_mode("dark")
        
        self.is_monitoring = False
        self.user_name = ""
        self.user_pw = ""
        self.cap = cv2.VideoCapture(0)
        self.current_frame = None
        self.is_previewing = True 
        self.freeze_frame = False # 3. 사진 확인을 위한 정지 상태 변수
        
        self.setup_ui()
        self.start_preview()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- 왼쪽 영역 (라이브 뷰) ---
        self.left_frame = ctk.CTkFrame(self, fg_color="black")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.preview_label = tk.Label(self.left_frame, bg="black")
        self.preview_label.pack(expand=True, fill="both")

        # 1. 효과 라벨 위치 변경 (중앙 -> 오른쪽 위)
        self.effect_label = ctk.CTkLabel(self.left_frame, text="", font=("Helvetica", 120, "bold"), text_color="#f1c40f")
        self.effect_label.place(relx=0.95, rely=0.05, anchor="ne")

        # --- 오른쪽 영역 (제어 패널) ---
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        try:
            raw_img = Image.open(LOGO_PATH)
            logo_img = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(120, 120))
            ctk.CTkLabel(self.right_frame, image=logo_img, text="").pack(pady=20)
        except:
            ctk.CTkLabel(self.right_frame, text="🐼 BAMBOO", font=("Apple SD Gothic Neo", 30, "bold")).pack(pady=20)

        self.progress_label = ctk.CTkLabel(self.right_frame, text="0 / 4", font=("Helvetica", 70, "bold"), text_color="#f1c40f")
        self.progress_label.pack(pady=20)

        self.status_box = ctk.CTkTextbox(self.right_frame, width=250, height=400, font=("Apple SD Gothic Neo", 12))
        self.status_box.pack(pady=10, padx=20, fill="both", expand=True)

        self.start_btn = ctk.CTkButton(self.right_frame, text="촬영 시작 (Enter)", height=80, 
                                       fg_color="#27ae60", font=("Apple SD Gothic Neo", 24, "bold"),
                                       command=self.toggle)
        self.start_btn.pack(side="bottom", pady=40, padx=20, fill="x")

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M")
        self.status_box.insert("end", f"[{ts}] {msg}\n")
        self.status_box.see("end")

    def start_preview(self):
        def update_frame():
            # 3. 사진 확인 중(freeze_frame)이 아닐 때만 라이브 화면 업데이트
            if self.is_previewing and not self.freeze_frame and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    self.current_frame = frame
                    cv2_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(cv2_img)
                    
                    w = self.preview_label.winfo_width()
                    h = self.preview_label.winfo_height()
                    if w > 1 and h > 1:
                        img = img.resize((w, h), Image.Resampling.LANCZOS)
                    
                    tk_img = ImageTk.PhotoImage(image=img)
                    self.preview_label.configure(image=tk_img)
                    self.preview_label.image = tk_img 
            self.after(20, update_frame)
        update_frame()

    def play_sound(self):
        os.system("afplay /System/Library/Sounds/Hero.aiff &")

    def flash_effect(self):
        self.preview_label.config(bg="white")
        self.after(100, lambda: self.preview_label.config(bg="black"))

    # 2. 엔터 키 입력을 지원하는 입력창 함수
    def get_input_with_enter(self, text, title):
        dialog = ctk.CTkInputDialog(text=text, title=title)
        # 다이얼로그가 뜨자마자 엔터 키 바인딩
        dialog.bind("<Return>", lambda e: dialog._ok_event())
        return dialog.get_input()

    def toggle(self):
        if not self.is_monitoring:
            # 2. 엔터만 누르면 넘어가는 입력창
            name = self.get_input_with_enter("성함을 입력하세요:", "사용자 확인")
            if not name: return
            
            pw = self.get_input_with_enter("비밀번호를 설정하세요:", "보안 설정")
            if not pw: return

            self.user_name = name.strip()
            self.user_pw = pw.strip()
            self.is_monitoring = True
            self.start_btn.configure(text="중단 (Stop)", fg_color="#e74c3c")
            
            for f in os.listdir(WATCH_DIR):
                if f.lower().endswith(('.jpg', '.jpeg')): os.remove(os.path.join(WATCH_DIR, f))

            self.after(0, lambda: self.progress_label.configure(text="0 / 4"))
            self.log(f"🟢 {self.user_name}님 세션 시작")

            threading.Thread(target=self.main_process_thread, daemon=True).start()
        else:
            self.is_monitoring = False
            self.start_btn.configure(text="촬영 시작", fg_color="#27ae60")

    def main_process_thread(self):
        current_session_files = []
        
        for i in range(TOTAL_SHOTS):
            if not self.is_monitoring: return
            
            # 4. 촬영 간 시간 8초 (카운트다운 포함)
            for count in range(8, 0, -1):
                if not self.is_monitoring: return
                self.after(0, lambda c=count: self.effect_label.configure(text=str(c)))
                time.sleep(1)
            
            self.after(0, lambda: self.effect_label.configure(text="📸"))
            self.play_sound()
            self.flash_effect()
            
            if self.current_frame is not None:
                filename = f"Shot_{datetime.now().strftime('%H%M%S')}_{i+1}.jpg"
                filepath = os.path.join(WATCH_DIR, filename)
                save_frame = cv2.flip(self.current_frame, 1)
                cv2.imwrite(filepath, save_frame)
                
                while not os.path.exists(filepath):
                    time.sleep(0.1)
                
                current_session_files.append(filepath)
                self.log(f"✅ {i+1}/4 촬영 완료")
                self.after(0, lambda c=i+1: self.progress_label.configure(text=f"{c} / 4"))

                # 3. 촬영 직후 1.5초간 프리뷰 정지
                self.freeze_frame = True
                time.sleep(1.5)
                self.freeze_frame = False
            
            self.after(0, lambda: self.effect_label.configure(text=""))

        if len(current_session_files) == TOTAL_SHOTS:
            try:
                self.log("🚀 프로세싱 시작...")
                self.is_previewing = False
                
                now_str = datetime.now().strftime('%H%M%S')
                team_raw_folder = os.path.join(RAW_STORAGE_DIR, f"{self.user_name}_{now_str}")
                os.makedirs(team_raw_folder, exist_ok=True)
                
                for idx, src in enumerate(current_session_files):
                    shutil.copy(src, os.path.join(team_raw_folder, f"Original_{idx+1}.jpg"))
                
                out_path = os.path.join(team_raw_folder, f"Result_{self.user_name}_{now_str}.jpg")
                addPhotos2Frame.create_bamboo_life4cut(current_session_files, FRAME_PATH, out_path, CLOUD_LINK)
                
                if os.path.exists(out_path):
                    os.system(f"lpr -P {PRINTER_NAME} -o media=Postcard -o fit-to-page '{out_path}'")
                    self.log("✅ 인쇄 전송 완료!")
                
                zip_name = f"{self.user_name}_{now_str}.zip"
                zip_path = os.path.join(CLOUD_ZIP_DIR, zip_name)
                os.system(f'cd "{team_raw_folder}" && zip -P "{self.user_pw}" -j "{zip_path}" ./*')
                
                self.log(f"🔒 세션 종료")
                self.is_monitoring = False
                self.is_previewing = True
                self.after(0, self.reset_ui_after_session)
                
            except Exception as e:
                self.log(f"❌ 에러: {str(e)}")
                self.is_previewing = True
        else:
            self.log("⚠️ 촬영 실패")

    def reset_ui_after_session(self):
        self.start_btn.configure(text="촬영 시작", fg_color="#27ae60")
        self.progress_label.configure(text="0 / 4")

    def on_closing(self):
        if self.cap: self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = BambooApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()