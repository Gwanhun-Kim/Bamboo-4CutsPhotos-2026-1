import os
import time
import threading
import customtkinter as ctk
from datetime import datetime
import addPhotos2Frame

# [필수 설정] 부장님 경로에 맞게 수정
BASE_PATH = "/Users/kimgwanhun/Desktop/Pictures/밤부/26-1/가두모집/인생네컷"
WATCH_DIR = os.path.join(BASE_PATH, "Bamboo_Studio")
RESULT_DIR = os.path.join(BASE_PATH, "Bamboo_Results")
FRAME_PATH = os.path.join(BASE_PATH, "assets/frame.png")
TOTAL_SHOTS = 4

class BambooApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bamboo 4-Cuts Manager")
        self.geometry("500x550")
        ctk.set_appearance_mode("dark")
        
        self.is_monitoring = False
        self.initial_count = 0
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self, text="📸 밤부 사진관 제어 패널", font=("Apple SD Gothic Neo", 22, "bold")).pack(pady=20)
        
        # 상태창
        self.status_box = ctk.CTkTextbox(self, width=400, height=200)
        self.status_box.pack(pady=10)
        
        # 촬영 카운트
        self.progress_label = ctk.CTkLabel(self, text="대기 중: 0 / 4", font=("Apple SD Gothic Neo", 18))
        self.progress_label.pack(pady=10)
        
        # 버튼
        self.start_btn = ctk.CTkButton(self, text="감시 시작", command=self.toggle, fg_color="#2ecc71", hover_color="#27ae60")
        self.start_btn.pack(pady=10)
        
        ctk.CTkButton(self, text="결과 폴더 열기", fg_color="gray", command=lambda: os.system(f"open {RESULT_DIR}")).pack(pady=5)

    def log(self, msg):
        self.status_box.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.status_box.see("end")

    def toggle(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.start_btn.configure(text="감시 중지", fg_color="#e74c3c")
            self.initial_count = len([f for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))])
            self.log("🟢 시스템 가동 시작")
            threading.Thread(target=self.monitor, daemon=True).start()
        else:
            self.is_monitoring = False
            self.start_btn.configure(text="감시 시작", fg_color="#2ecc71")
            self.log("🔴 시스템 중지")

    def monitor(self):
        while self.is_monitoring:
            files = [os.path.join(WATCH_DIR, f) for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]
            files.sort(key=os.path.getmtime)
            new_files = files[self.initial_count:]
            
            self.progress_label.configure(text=f"현재 세션: {len(new_files)} / {TOTAL_SHOTS}")
            
            if len(new_files) >= TOTAL_SHOTS:
                self.log("🎨 4장 수집 완료! 합성 중...")
                time.sleep(1)
                out_path = os.path.join(RESULT_DIR, f"Bamboo_{datetime.now().strftime('%H%M%S')}.jpg")
                final = addPhotos2Frame.create_life4cut(new_files[:4], FRAME_PATH, out_path)
                
                if final:
                    self.log(f"✅ 완성: {os.path.basename(final)}")
                    os.system(f"open {final}")
                self.initial_count = len(files)
            time.sleep(1)

if __name__ == "__main__":
    app = BambooApp()
    app.mainloop()