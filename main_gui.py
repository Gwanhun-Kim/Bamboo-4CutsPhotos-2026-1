import os
import time
import threading
import shutil
import customtkinter as ctk
from PIL import Image
from datetime import datetime
import sys
import cv2

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
CLOUD_LINK = "https://drive.google.com/drive/folders/10_VLzMxQIQ_JpVkuOvbP4hlMMNC4VUpA?hl=ko"
TOTAL_SHOTS = 4

class BambooApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BAMBOO STUDIO v2.7 (Final Stable)")
        self.geometry("280x750+0+0")
        ctk.set_appearance_mode("dark")
        
        self.is_monitoring = False
        self.initial_count = 0
        self.user_name = ""
        self.user_pw = ""
        self.setup_ui()

    def setup_ui(self):
        try:
            raw_img = Image.open(LOGO_PATH)
            logo_img = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(120, 120))
            ctk.CTkLabel(self, image=logo_img, text="").pack(pady=(40, 10))
        except:
            ctk.CTkLabel(self, text="🐼 BAMBOO", font=("Apple SD Gothic Neo", 22, "bold")).pack(pady=(40, 10))

        self.cam_var = ctk.StringVar(value="DSLR")
        self.cam_switch = ctk.CTkSegmentedButton(self, values=["DSLR", "FaceTime"], variable=self.cam_var)
        self.cam_switch.pack(pady=10, padx=20, fill="x")

        self.count_frame = ctk.CTkFrame(self, fg_color="#2c3e50", corner_radius=15)
        self.count_frame.pack(pady=10, padx=20, fill="x")
        self.progress_label = ctk.CTkLabel(self.count_frame, text="0 / 4", 
                                           font=("Helvetica", 55, "bold"), text_color="#f1c40f")
        self.progress_label.pack(pady=10)

        self.status_box = ctk.CTkTextbox(self, width=240, height=300, font=("Apple SD Gothic Neo", 11))
        self.status_box.pack(pady=10, padx=20)

        self.start_btn = ctk.CTkButton(self, text="촬영 시작", width=240, height=55, 
                                       fg_color="#27ae60", font=("Apple SD Gothic Neo", 18, "bold"),
                                       command=self.toggle)
        self.start_btn.pack(side="bottom", pady=(20, 30))

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M")
        self.status_box.insert("end", f"[{ts}] {msg}\n")
        self.status_box.see("end")

    def toggle(self):
        if not self.is_monitoring:
            name_dialog = ctk.CTkInputDialog(text="성함을 입력하세요:", title="사용자 확인")
            name = name_dialog.get_input()
            if not name: return
            pw_dialog = ctk.CTkInputDialog(text="압축 비밀번호를 설정하세요:", title="보안 설정")
            pw = pw_dialog.get_input()
            if not pw: return

            self.user_name = name.strip()
            self.user_pw = pw.strip()
            self.is_monitoring = True
            self.start_btn.configure(text="중단 (Stop)", fg_color="#e74c3c")
            
            self.initial_count = len([f for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))])
            self.log(f"🟢 {self.user_name}님 촬영 시작 ({self.cam_var.get()})")

            threading.Thread(target=self.monitor_loop, daemon=True).start()
            if self.cam_var.get() == "FaceTime":
                threading.Thread(target=self.auto_capture_webcam, daemon=True).start()
        else:
            self.is_monitoring = False
            self.start_btn.configure(text="촬영 시작", fg_color="#27ae60")
            self.log("🔴 촬영 중단")

    def auto_capture_webcam(self):
        """카메라 노출 조절 및 검은 화면 방지를 위한 예열 로직 강화"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            self.log("❌ 카메라 장치(0) 실패. 장치(1) 시도...")
            cap = cv2.VideoCapture(1)
            if not cap.isOpened():
                self.log("❌ 에러: 모든 카메라 연결 실패!")
                self.is_monitoring = False
                return

        # [1] 카메라 센서 예열 (빛을 받아들여 노출을 맞출 시간 필요)
        self.log("📸 카메라 센서 예열 중 (3초)...")
        for _ in range(60): # 약 2초간 프레임을 버리며 노출 조정
            cap.read()
            time.sleep(0.05)

        for i in range(TOTAL_SHOTS):
            if not self.is_monitoring: break
            
            # [2] 카운트다운
            for count in range(3, 0, -1):
                self.log(f"📸 {i+1}번 촬영 {count}초 전!")
                time.sleep(1)
            
            # [3] 촬영 직전 버퍼 비우기 (가장 최신의 밝은 프레임을 가져오기 위함)
            for _ in range(15):
                cap.read()
            
            ret, frame = cap.read()
            if ret and frame is not None:
                # [4] 파일 저장
                filename = f"FaceTime_{datetime.now().strftime('%H%M%S')}.jpg"
                filepath = os.path.join(WATCH_DIR, filename)
                cv2.imwrite(filepath, frame)
                
                # 밝기 체크 (디버깅용)
                avg_brightness = frame.mean()
                if avg_brightness < 15:
                    self.log(f"⚠️ {i+1}번 사진이 너무 어둡습니다 (밝기: {avg_brightness:.1f})")
                else:
                    self.log(f"✅ {i+1}/4 촬영 완료!")
            else:
                self.log(f"❌ {i+1}번 촬영 실패")
            
        cap.release()

    def monitor_loop(self):
        while self.is_monitoring:
            try:
                files = [os.path.join(WATCH_DIR, f) for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]
                files.sort(key=os.path.getmtime)
                new_files = files[self.initial_count:]
                self.progress_label.configure(text=f"{len(new_files)} / {TOTAL_SHOTS}")
                
                if len(new_files) >= TOTAL_SHOTS:
                    self.log("🚀 프로세싱 시작...")
                    time.sleep(2.0)
                    now_str = datetime.now().strftime('%H%M%S')
                    team_raw_folder = os.path.join(RAW_STORAGE_DIR, f"{self.user_name}_{now_str}")
                    os.makedirs(team_raw_folder, exist_ok=True)
                    
                    source_photos = new_files[:4]
                    for idx, src in enumerate(source_photos):
                        shutil.copy(src, os.path.join(team_raw_folder, f"Original_{idx+1}.jpg"))
                    
                    out_path = os.path.join(team_raw_folder, f"Result_{self.user_name}_{now_str}.jpg")
                    addPhotos2Frame.create_bamboo_life4cut(source_photos, FRAME_PATH, out_path, CLOUD_LINK)
                    
                    zip_name = f"{self.user_name}_{now_str}.zip"
                    zip_path = os.path.join(CLOUD_ZIP_DIR, zip_name)
                    # Mac 시스템 명령어로 고호환성 압축
                    os.system(f'zip -P "{self.user_pw}" -j "{zip_path}" "{team_raw_folder}"/*')

                    self.log(f"🔒 보안 압축 완료: {zip_name}")
                    os.system(f"open {CLOUD_ZIP_DIR}")
                    self.is_monitoring = False
                    self.start_btn.configure(text="촬영 시작", fg_color="#27ae60")
                    break
            except Exception as e:
                self.log(f"❌ 에러: {str(e)}")
            time.sleep(1)

if __name__ == "__main__":
    app = BambooApp()
    app.mainloop()