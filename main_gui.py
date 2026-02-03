import os
import time
import threading
import customtkinter as ctk
from datetime import datetime
import addPhotos2Frame

# [필수 설정]
BASE_PATH = "/Users/kimgwanhun/Desktop/Pictures/밤부/26-1/가두모집/인생네컷"
WATCH_DIR = os.path.join(BASE_PATH, "Bamboo_Studio")
RESULT_DIR = os.path.join(BASE_PATH, "Bamboo_Results")
FRAME_PATH = os.path.join(BASE_PATH, "assets/frame.png")
TOTAL_SHOTS = 4

class BambooApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 좌측 1/4용 슬림 설정
        self.title("BAMBOO")
        self.geometry("250x850+0+0")
        ctk.set_appearance_mode("dark")
        
        self.is_monitoring = False
        self.initial_count = 0
        self.setup_ui()

    def setup_ui(self):
        # 1. 미니 로고
        ctk.CTkLabel(self, text="📸 BAMBOO", font=("Apple SD Gothic Neo", 20, "bold")).pack(pady=(30, 10))

        # 2. 대형 카운트
        self.count_frame = ctk.CTkFrame(self, fg_color="#2c3e50", corner_radius=15)
        self.count_frame.pack(pady=10, padx=20, fill="x")
        
        self.progress_label = ctk.CTkLabel(self.count_frame, text="0 / 4", 
                                           font=("Helvetica", 55, "bold"),
                                           text_color="#f1c40f")
        self.progress_label.pack(pady=20)

        # 3. 상태창
        self.status_box = ctk.CTkTextbox(self, width=210, height=400, 
                                         font=("Apple SD Gothic Neo", 11),
                                         fg_color="#1a1a1a")
        self.status_box.pack(pady=10, padx=20)
        self.log("준비 완료. '촬영 시작'을 누르세요.")

        # 4. 하단 제어 버튼 영역
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(side="bottom", pady=30)

        # 촬영 시작/중지 버튼
        self.start_btn = ctk.CTkButton(self.btn_frame, text="촬영 시작", 
                                       width=210, height=50,
                                       font=("Apple SD Gothic Neo", 16, "bold"),
                                       command=self.toggle, 
                                       fg_color="#27ae60")
        self.start_btn.pack(pady=5)

        # [신규] 초기화 버튼 (오류 발생 시 세션 리셋)
        self.reset_btn = ctk.CTkButton(self.btn_frame, text="🔄 촬영 초기화", 
                                       width=210, height=40,
                                       font=("Apple SD Gothic Neo", 14),
                                       fg_color="#e67e22", hover_color="#d35400",
                                       command=self.reset_session)
        self.reset_btn.pack(pady=5)
        
        # 결과 폴더 버튼
        ctk.CTkButton(self.btn_frame, text="📁 결과 폴더 열기", 
                      width=210, height=40,
                      fg_color="#34495e",
                      command=lambda: os.system(f"open {RESULT_DIR}")).pack(pady=5)

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M")
        self.status_box.insert("end", f"[{ts}] {msg}\n")
        self.status_box.see("end")

    def toggle(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.start_btn.configure(text="촬영 중 (Running)", fg_color="#e74c3c")
            # 현재 폴더의 파일 개수를 기준점으로 잡음
            self.initial_count = len([f for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))])
            self.log("🟢 촬영 감시를 시작합니다.")
            threading.Thread(target=self.monitor_loop, daemon=True).start()
        else:
            self.is_monitoring = False
            self.start_btn.configure(text="촬영 시작", fg_color="#27ae60")
            self.log("🔴 촬영을 중단했습니다.")

    def reset_session(self):
        """오류 시 현재까지 찍힌 카운트를 무시하고 현재 시점부터 다시 시작"""
        if self.is_monitoring:
            # 현재 폴더에 있는 모든 파일을 '이미 찍힌 것'으로 간주하여 카운트를 새로 고침
            self.initial_count = len([f for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))])
            self.progress_label.configure(text="0 / 4")
            self.log("⚠️ 촬영 세션을 초기화했습니다. 다시 4장을 찍으세요.")
        else:
            self.log("❌ 촬영 중이 아닐 때는 초기화할 수 없습니다.")

    def monitor_loop(self):
        while self.is_monitoring:
            files = [os.path.join(WATCH_DIR, f) for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]
            files.sort(key=os.path.getmtime)
            
            new_files = files[self.initial_count:]
            count = len(new_files)
            
            # 실시간 카운트 표시
            self.progress_label.configure(text=f"{count} / {TOTAL_SHOTS}")
            
            if count >= TOTAL_SHOTS:
                self.log("🎨 4장 감지! 합성 진행 중...")
                time.sleep(1.5) # 전송 완료 대기
                
                timestamp = datetime.now().strftime("%H%M%S")
                out_path = os.path.join(RESULT_DIR, f"B_{timestamp}.jpg")
                
                final = addPhotos2Frame.create_life4cut(new_files[:4], FRAME_PATH, out_path)
                
                if final:
                    self.log(f"✅ 완성: {os.path.basename(final)}")
                    os.system(f"open {final}")
                
                # 다음 팀을 위해 기준점 업데이트
                self.initial_count = len(files)
                self.log("✨ 다음 촬영 대기 중...")
            
            time.sleep(1)

if __name__ == "__main__":
    app = BambooApp()
    app.mainloop()