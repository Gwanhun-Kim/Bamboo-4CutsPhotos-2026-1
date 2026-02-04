import os
import time
import threading
import shutil
import qrcode
import customtkinter as ctk
from PIL import Image
from datetime import datetime
import sys

# addPhotos2Frame 모듈이 있는 폴더를 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'addPhotos2Frame'))
import addPhotos2Frame

# [1. 경로 및 설정]
BASE_PATH = "/Users/kimgwanhun/Desktop/Pictures/밤부/26-1/가두모집/인생네컷"
WATCH_DIR = os.path.join(BASE_PATH, "Bamboo_Studio")
RESULT_ROOT = os.path.join(BASE_PATH, "Bamboo_Results")
FRAME_PATH = os.path.join(BASE_PATH, "assets/밤부_인생네컷_최종mk4.png")
LOGO_PATH = os.path.join(BASE_PATH, "assets/bamboo_logo.jpeg")

# [중요] 구글 드라이브 공유 폴더 링크 (최상위 공유 폴더 주소)
CLOUD_LINK = "https://drive.google.com/drive/folders/10_VLzMxQIQ_JpVkuOvbP4hlMMNC4VUpA?hl=ko"
TOTAL_SHOTS = 4

class BambooApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("BAMBOO STUDIO v1.4")
        self.geometry("250x750+0+0")
        ctk.set_appearance_mode("dark")
        
        self.is_monitoring = False
        self.initial_count = 0
        self.current_user = "Unknown" # 현재 촬영자 이름 저장용
        self.setup_ui()

    def setup_ui(self):
        # --- [최상단] 밤부 로고 ---
        try:
            raw_img = Image.open(LOGO_PATH)
            logo_img = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(120, 120))
            self.logo_label = ctk.CTkLabel(self, image=logo_img, text="")
            self.logo_label.pack(pady=(40, 20))
        except:
            ctk.CTkLabel(self, text="🐼 BAMBOO", font=("Apple SD Gothic Neo", 22, "bold")).pack(pady=(40, 20))

        # --- [중단 1] 촬영 카운트 ---
        self.count_frame = ctk.CTkFrame(self, fg_color="#2c3e50", corner_radius=15)
        self.count_frame.pack(pady=10, padx=20, fill="x")
        self.progress_label = ctk.CTkLabel(self.count_frame, text="0 / 4", 
                                           font=("Helvetica", 55, "bold"), text_color="#f1c40f")
        self.progress_label.pack(pady=10)

        # --- [중단 2] 상태 로그창 ---
        self.status_box = ctk.CTkTextbox(self, width=210, height=300, font=("Apple SD Gothic Neo", 11))
        self.status_box.pack(pady=10, padx=20)

        # --- [하단] 제어 버튼 영역 ---
        self.start_btn = ctk.CTkButton(self, text="촬영 시작", width=210, height=55, 
                                       fg_color="#27ae60", font=("Apple SD Gothic Neo", 18, "bold"),
                                       command=self.toggle)
        self.start_btn.pack(side="bottom", pady=(5, 30))
        
        self.reset_btn = ctk.CTkButton(self, text="🔄 촬영 초기화 (Reset)", width=210, height=35,
                                       fg_color="#e67e22", command=self.reset_session)
        self.reset_btn.pack(side="bottom", pady=5)

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M")
        self.status_box.insert("end", f"[{ts}] {msg}\n")
        self.status_box.see("end")

    def toggle(self):
        if not self.is_monitoring:
            # 1. 촬영 시작 전 이름 입력 받기
            dialog = ctk.CTkInputDialog(text="촬영하시는 분의 성함을 입력하세요:", title="사용자 확인")
            input_name = dialog.get_input()

            if input_name is None: # 취소 버튼 눌렀을 때
                return
            
            self.current_user = input_name.strip() if input_name.strip() != "" else "NoName"
            
            # 2. 모니터링 시작
            self.is_monitoring = True
            self.start_btn.configure(text="촬영 중단 (Stop)", fg_color="#e74c3c")
            # 감시 시작 시점의 파일 개수 파악
            self.initial_count = len([f for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))])
            
            self.log(f"🟢 {self.current_user}님 세션 시작")
            threading.Thread(target=self.monitor_loop, daemon=True).start()
        else:
            self.is_monitoring = False
            self.start_btn.configure(text="촬영 시작", fg_color="#27ae60")
            self.log("🔴 모니터링 중지")

    def reset_session(self):
        if self.is_monitoring:
            self.initial_count = len([f for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))])
            self.progress_label.configure(text="0 / 4")
            self.log("⚠️ 세션 리셋됨")

    def monitor_loop(self):
        while self.is_monitoring:
            try:
                files = [os.path.join(WATCH_DIR, f) for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]
                files.sort(key=os.path.getmtime)
                new_files = files[self.initial_count:]
                
                self.progress_label.configure(text=f"{len(new_files)} / {TOTAL_SHOTS}")
                
                if len(new_files) >= TOTAL_SHOTS:
                    self.log(f"🚀 {self.current_user}님 4장 감지!")
                    time.sleep(1.5)
                    
                    now = datetime.now()
                    # 폴더명을 [이름_시간] 형태로 설정
                    folder_name = f"{self.current_user}_{now.strftime('%H%M%S')}"
                    team_path = os.path.join(RESULT_ROOT, folder_name)
                    os.makedirs(team_path, exist_ok=True)
                    
                    source_photos = new_files[:4]
                    for idx, src in enumerate(source_photos):
                        shutil.copy(src, os.path.join(team_path, f"Original_{idx+1}.jpg"))
                    
                    out_path = os.path.join(team_path, f"Result_{now.strftime('%H%M%S')}.jpg")
                    
                    # 합성 함수 호출
                    final = addPhotos2Frame.create_bamboo_life4cut(
                        photo_paths=source_photos,
                        frame_path=FRAME_PATH,
                        out_path=out_path,
                        qr_data=CLOUD_LINK,
                        logo_path=LOGO_PATH
                    )
                    
                    if final:
                        self.log(f"✅ {folder_name} 저장 완료")
                        os.system(f"open {team_path}")
                        # 한 팀 촬영 완료 후 자동 중단 (새 이름을 받기 위해)
                        self.is_monitoring = False
                        self.start_btn.configure(text="촬영 시작", fg_color="#27ae60")
                        break # 루프 탈출
                    
                    self.initial_count = len(files)
            except Exception as e:
                self.log(f"❌ 에러: {str(e)}")
            
            time.sleep(1)

if __name__ == "__main__":
    app = BambooApp()
    app.mainloop()