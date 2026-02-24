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
import subprocess

# [1. 경로 및 설정] 
# 폴더명을 '가두모집'에서 'Recruitment'로 바꿨다고 가정합니다. 실제 이름에 맞춰 수정하세요.
BASE_PATH = "/Users/kimgwanhun/Desktop/Pictures/Bamboo/Recruitment/Life4Cut"
RESULT_ROOT = os.path.join(BASE_PATH, "Bamboo_Results")
RAW_STORAGE_DIR = os.path.join(RESULT_ROOT, "Raw_Storage")
CLOUD_ZIP_DIR = os.path.join(RESULT_ROOT, "Cloud_Upload")

for d in [RAW_STORAGE_DIR, CLOUD_ZIP_DIR]:
    if not os.path.exists(d): os.makedirs(d, exist_ok=True)

FRAME_PATH = os.path.join(BASE_PATH, "assets/밤부_인생네컷_최종mk4.png")
LOGO_PATH = os.path.join(BASE_PATH, "assets/bamboo_logo.jpeg")
CLOUD_LINK = "https://drive.google.com/drive/folders/1P7M1o9lTkkPwL754xjDONYqGOLlX04Fd?usp=sharing"
TOTAL_SHOTS = 4
PRINTER_NAME = "Canon_CP1500"

class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, parent, image_path, callback):
        super().__init__(parent)
        self.title("인쇄 확인")
        self.attributes("-topmost", True)
        self.callback = callback
        
        # 맥북 화면 해상도를 고려하여 창 크기 재조정
        self.geometry("700x820") 
        self.resizable(False, False)

        try:
            raw_img = Image.open(image_path)
            img_w, img_h = raw_img.size
            # 버튼이 밀려나지 않도록 이미지 높이를 500px로 제한
            display_h = 500 
            display_w = int(display_h * (img_w / img_h))
            self.preview_img = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(display_w, display_h))
            
            ctk.CTkLabel(self, text="📸 촬영 결과 확인", font=("Apple SD Gothic Neo", 24, "bold")).pack(pady=10)
            ctk.CTkLabel(self, image=self.preview_img, text="").pack(pady=5)
            ctk.CTkLabel(self, text="이대로 출력하시겠습니까?", font=("Apple SD Gothic Neo", 18)).pack(pady=10)
        except Exception as e:
            ctk.CTkLabel(self, text=f"이미지 로드 실패: {e}").pack(pady=20)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15, fill="x", padx=80)
        
        ctk.CTkButton(btn_frame, text="예 (Print)", fg_color="#27ae60", height=60, font=("Apple SD Gothic Neo", 20, "bold"),
                       command=self.confirm).pack(side="left", expand=True, padx=15)
        ctk.CTkButton(btn_frame, text="아니오 (Cancel)", fg_color="#e74c3c", height=60, font=("Apple SD Gothic Neo", 20, "bold"),
                       command=self.cancel).pack(side="right", expand=True, padx=15)

    def confirm(self):
        self.callback(True)
        self.destroy()

    def cancel(self):
        self.callback(False)
        self.destroy()

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
        self.freeze_frame = False
        
        self.setup_ui()
        self.start_preview()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = ctk.CTkFrame(self, fg_color="black")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.preview_label = tk.Label(self.left_frame, bg="black")
        self.preview_label.pack(expand=True, fill="both")
        self.effect_label = ctk.CTkLabel(self.left_frame, text="", font=("Helvetica", 130, "bold"), text_color="#f1c40f")
        self.effect_label.place(relx=0.95, rely=0.05, anchor="ne")

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.progress_label = ctk.CTkLabel(self.right_frame, text="0 / 4", font=("Helvetica", 70, "bold"), text_color="#f1c40f")
        self.progress_label.pack(pady=20)
        self.status_box = ctk.CTkTextbox(self.right_frame, width=250, height=400, font=("Apple SD Gothic Neo", 13))
        self.status_box.pack(pady=10, padx=20, fill="both", expand=True)
        self.start_btn = ctk.CTkButton(self.right_frame, text="촬영 시작 (Enter)", height=80, 
                                       fg_color="#27ae60", font=("Apple SD Gothic Neo", 24, "bold"),
                                       command=self.toggle)
        self.start_btn.pack(side="bottom", pady=40, padx=20, fill="x")

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M")
        self.status_box.insert("end", f"[{ts}] {msg}\n")
        self.status_box.see("end")

    def play_sound(self):
        os.system("afplay /System/Library/Sounds/Hero.aiff &")

    def start_preview(self):
        def update_frame():
            if self.is_previewing and not self.freeze_frame and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    self.current_frame = frame.copy()
                    if self.is_monitoring:
                        win_width = self.winfo_width()
                        left_frame_width = self.left_frame.winfo_width()
                        w_orig = frame.shape[1]
                        target_x_in_img = int(((win_width // 2) / left_frame_width) * w_orig)
                        cv2.arrowedLine(frame, (target_x_in_img, 85), (target_x_in_img, 15), (0, 255, 255), 8, tipLength=0.4)
                        text = "LOOK HERE!"
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        scale = 1.1
                        thick = 3
                        t_size = cv2.getTextSize(text, font, scale, thick)[0]
                        cv2.putText(frame, text, (target_x_in_img - t_size[0]//2, 130), font, scale, (0, 255, 255), thick)
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

    def toggle(self):
        if not self.is_monitoring:
            name = self.get_input_with_enter("성함을 입력하세요:", "사용자 확인")
            if not name: return
            pw = self.get_input_with_enter("비밀번호를 설정하세요:", "보안 설정")
            if not pw: return
            self.user_name = name.strip()
            self.user_pw = pw.strip()
            self.is_monitoring = True
            self.start_btn.configure(text="중단 (Stop)", fg_color="#e74c3c")
            self.log(f"🟢 {self.user_name}님 세션 시작")
            threading.Thread(target=self.main_process_thread, daemon=True).start()
        else:
            self.is_monitoring = False
            self.reset_ui_after_session()

    def main_process_thread(self):
        current_session_files = []
        now_ts = datetime.now().strftime('%H%M%S')
        session_folder = os.path.abspath(os.path.join(RAW_STORAGE_DIR, f"{self.user_name}_{now_ts}"))
        os.makedirs(session_folder, exist_ok=True)
        try:
            for i in range(TOTAL_SHOTS):
                if not self.is_monitoring: break
                for count in range(8, 0, -1):
                    if not self.is_monitoring: break
                    self.after(0, lambda c=count: self.effect_label.configure(text=str(c)))
                    time.sleep(1)
                if not self.is_monitoring: break
                self.after(0, lambda: self.effect_label.configure(text="📸"))
                self.play_sound()
                if self.current_frame is not None:
                    shot_frame = self.current_frame.copy()
                    filename = f"Shot_{i+1}.jpg"
                    filepath = os.path.join(session_folder, filename)
                    cv2.imwrite(filepath, shot_frame)
                    current_session_files.append(filepath)
                    self.log(f"✅ {i+1}/4 촬영 완료")
                    self.after(0, lambda c=i+1: self.progress_label.configure(text=f"{c} / 4"))
                    self.freeze_frame = True
                    time.sleep(1.5)
                    self.freeze_frame = False
                self.after(0, lambda: self.effect_label.configure(text=""))
            if len(current_session_files) == TOTAL_SHOTS and self.is_monitoring:
                self.after(0, self.prepare_result_for_confirm, current_session_files, session_folder, now_ts)
        except Exception as e:
            self.log(f"❌ 촬영 오류: {e}")

    def prepare_result_for_confirm(self, session_files, session_folder, now_ts):
        self.log("🎨 결과물 생성 중...")
        out_path = os.path.join(session_folder, f"Result_{self.user_name}_{now_ts}.jpg")
        import addPhotos2Frame
        addPhotos2Frame.create_bamboo_life4cut(session_files, FRAME_PATH, out_path, CLOUD_LINK)
        # 팝업 호출
        self.after(500, lambda: ConfirmDialog(self, out_path, lambda choice: self.handle_confirm_choice(choice, out_path, session_folder, now_ts)))

    def handle_confirm_choice(self, choice, out_path, session_folder, now_ts):
        if choice:
            try:
                # [끝판왕 방식] 데이터 스트리밍 인쇄 - 경로 문제를 완전히 무시함
                self.log(f"🖨 인쇄 데이터 전송 시작...")
                with open(out_path, 'rb') as f:
                    img_data = f.read()
                
                process = subprocess.Popen(
                    ["lpr", "-P", PRINTER_NAME, "-o", "media=Postcard", "-o", "fit-to-page"],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                stdout, stderr = process.communicate(input=img_data)
                
                if process.returncode == 0:
                    self.log("✅ 인쇄 명령 전송 완료")
                else:
                    self.log(f"❌ 인쇄 실패: {stderr.decode('utf-8', errors='ignore')}")
            except Exception as e:
                self.log(f"❌ 인쇄 시스템 에러: {e}")
        else:
            self.log("🚫 인쇄 취소")
        
        self.archive_session(session_folder, now_ts)
        self.reset_ui_after_session()

    def archive_session(self, session_folder, now_ts):
        try:
            self.log("🔒 보안 압축 중...")
            zip_name = f"{self.user_name}_{now_ts}.zip"
            zip_out_path = os.path.abspath(os.path.join(CLOUD_ZIP_DIR, zip_name))
            result = subprocess.run(
                ["zip", "-P", self.user_pw, "-r", zip_out_path, "."],
                cwd=os.path.abspath(session_folder),
                capture_output=True, text=True
            )
            if result.returncode == 0: self.log(f"📦 Cloud_Upload 완료")
            else: self.log(f"⚠️ 압축 실패")
        except Exception as e: self.log(f"❌ 압축 오류: {e}")

    def reset_ui_after_session(self):
        self.is_monitoring = False
        self.start_btn.configure(text="촬영 시작 (Enter)", fg_color="#27ae60")
        self.progress_label.configure(text="0 / 4")
        self.effect_label.configure(text="")

    def get_input_with_enter(self, text, title):
        dialog = ctk.CTkInputDialog(text=text, title=title)
        dialog.bind("<Return>", lambda e: dialog._ok_event())
        return dialog.get_input()

    def on_closing(self):
        if self.cap: self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = BambooApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()