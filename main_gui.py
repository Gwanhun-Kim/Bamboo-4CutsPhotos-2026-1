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

# addPhotos2Frame 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'addPhotos2Frame'))
import addPhotos2Frame

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
# 요청하신 드라이브 링크로 업데이트 완료
CLOUD_LINK = "https://drive.google.com/drive/folders/1P7M1o9lTkkPwL754xjDONYqGOLlX04Fd?hl=ko"
TOTAL_SHOTS = 4

class BambooApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BAMBOO STUDIO v3.2")
        self.geometry("350x850+0+0")
        ctk.set_appearance_mode("dark")
        
        self.is_monitoring = False
        self.user_name = ""
        self.user_pw = ""
        
        self.cap = None
        self.current_frame = None
        self.is_previewing = True 
        
        self.setup_ui()
        self.start_preview()

    def setup_ui(self):
        try:
            raw_img = Image.open(LOGO_PATH)
            logo_img = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(100, 100))
            ctk.CTkLabel(self, image=logo_img, text="").pack(pady=(20, 10))
        except:
            ctk.CTkLabel(self, text="🐼 BAMBOO", font=("Apple SD Gothic Neo", 22, "bold")).pack(pady=(20, 10))

        self.preview_label = tk.Label(self, text="카메라 연결 중...", width=320, height=240, bg="black", fg="white")
        self.preview_label.pack(pady=10, padx=20)

        self.cam_var = ctk.StringVar(value="DSLR")
        self.cam_switch = ctk.CTkSegmentedButton(self, values=["DSLR", "FaceTime"], variable=self.cam_var)
        self.cam_switch.pack(pady=5, padx=20, fill="x")

        self.progress_label = ctk.CTkLabel(self, text="0 / 4", font=("Helvetica", 45, "bold"), text_color="#f1c40f")
        self.progress_label.pack(pady=10)

        self.status_box = ctk.CTkTextbox(self, width=300, height=200, font=("Apple SD Gothic Neo", 11))
        self.status_box.pack(pady=10, padx=20)

        self.start_btn = ctk.CTkButton(self, text="촬영 시작", width=300, height=55, 
                                       fg_color="#27ae60", font=("Apple SD Gothic Neo", 18, "bold"),
                                       command=self.toggle)
        self.start_btn.pack(side="bottom", pady=(10, 30))

    def log(self, msg):
        def _log():
            ts = datetime.now().strftime("%H:%M")
            self.status_box.insert("end", f"[{ts}] {msg}\n")
            self.status_box.see("end")
        self.after(0, _log)

    def start_preview(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(1)

        def update_frame():
            if self.is_previewing and self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    self.current_frame = frame
                    cv2_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(cv2_img)
                    img = img.resize((320, 240), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(image=img)
                    self.preview_label.configure(image=tk_img)
                    self.preview_label.image = tk_img 
            self.after(30, update_frame)
        update_frame()

    def toggle(self):
        if not self.is_monitoring:
            # 1. 성함 입력 팝업 및 엔터 바인딩
            name_dialog = ctk.CTkInputDialog(text="성함을 입력하세요:", title="사용자 확인")
            name_dialog.after(100, name_dialog.focus_force)
            name_dialog.bind("<Return>", lambda e: name_dialog._ok_event())
            name = name_dialog.get_input()
            if not name: return
            
            # 2. 비밀번호 입력 팝업 및 엔터 바인딩
            pw_dialog = ctk.CTkInputDialog(text="비밀번호를 설정하세요:", title="보안 설정")
            pw_dialog.after(100, pw_dialog.focus_force)
            pw_dialog.bind("<Return>", lambda e: pw_dialog._ok_event())
            pw = pw_dialog.get_input()
            if not pw: return

            self.user_name = name.strip()
            self.user_pw = pw.strip()
            self.is_monitoring = True
            self.start_btn.configure(text="중단 (Stop)", fg_color="#e74c3c")
            
            self.initial_count = len([f for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))])
            self.after(0, lambda: self.progress_label.configure(text="0 / 4"))
            self.log(f"🟢 {self.user_name}님 세션 시작")

            threading.Thread(target=self.main_process_thread, daemon=True).start()
        else:
            self.is_monitoring = False
            self.start_btn.configure(text="촬영 시작", fg_color="#27ae60")
            self.log("🔴 중단됨")

    def main_process_thread(self):
        # FaceTime 촬영 시퀀스
        if self.cam_var.get() == "FaceTime":
            for i in range(TOTAL_SHOTS):
                if not self.is_monitoring: return
                for count in range(3, 0, -1):
                    self.log(f"📸 {i+1}번 촬영 {count}초 전!")
                    time.sleep(1)
                
                if self.current_frame is not None:
                    filename = f"FaceTime_{datetime.now().strftime('%H%M%S')}.jpg"
                    filepath = os.path.join(WATCH_DIR, filename)
                    cv2.imwrite(filepath, cv2.flip(self.current_frame, 1)) 
                    self.log(f"✅ {i+1}/4 촬영 완료!")
                    current_count = i + 1
                    self.after(0, lambda c=current_count: self.progress_label.configure(text=f"{c} / {TOTAL_SHOTS}"))
            
        while self.is_monitoring:
            try:
                files = [os.path.join(WATCH_DIR, f) for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]
                files.sort(key=os.path.getmtime)
                new_files = files[self.initial_count:]
                
                if len(new_files) >= TOTAL_SHOTS:
                    self.log("🚀 프로세싱 시작...")
                    self.is_previewing = False
                    time.sleep(2.0)
                    
                    now_str = datetime.now().strftime('%H%M%S')
                    team_raw_folder = os.path.join(RAW_STORAGE_DIR, f"{self.user_name}_{now_str}")
                    os.makedirs(team_raw_folder, exist_ok=True)
                    
                    source_photos = new_files[:4]
                    for idx, src in enumerate(source_photos):
                        shutil.copy(src, os.path.join(team_raw_folder, f"Original_{idx+1}.jpg"))
                    
                    out_path = os.path.join(team_raw_folder, f"Result_{self.user_name}_{now_str}.jpg")
                    addPhotos2Frame.create_bamboo_life4cut(source_photos, FRAME_PATH, out_path, CLOUD_LINK)
                    
                    # --- [추가] CP1500 자동 인쇄 명령 ---
                    self.log(f"🖨️ {self.user_name}님 사진 출력 중...")
                    os.system(f"lpr -P Canon_CP1500 -o media=Postcard -o fit-to-page '{out_path}'")
                    # ---------------------------------

                    zip_name = f"{self.user_name}_{now_str}.zip"
                    zip_path = os.path.join(CLOUD_ZIP_DIR, zip_name)
                    os.system(f'cd "{team_raw_folder}" && zip -P "{self.user_pw}" -j "{zip_path}" ./*')

                    self.log(f"🔒 압축 완료 및 세션 종료")
                    self.is_monitoring = False
                    self.is_previewing = True
                    self.after(0, self.reset_ui_after_session)
                    break
            except Exception as e:
                self.log(f"❌ 에러: {str(e)}")
                self.is_previewing = True
                break
            time.sleep(1)

    def reset_ui_after_session(self):
        self.start_btn.configure(text="촬영 시작", fg_color="#27ae60")

    def on_closing(self):
        self.is_previewing = False
        if self.cap: self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = BambooApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()