import os
import time
import addPhotos2Frame
from datetime import datetime

# ==========================================
# [환경 설정]
# ==========================================
BASE_PATH = "/Users/kimgwanhun/Desktop/Pictures/밤부/26-1/가두모집/인생네컷"
WATCH_DIR = os.path.join(BASE_PATH, "Bamboo_Studio")   # 테더링 앱 저장 경로
RESULT_DIR = os.path.join(BASE_PATH, "Bamboo_Results") # 결과물 저장 경로
FRAME_PATH = os.path.join(BASE_PATH, "assets/frame.png")

TOTAL_SHOTS = 4    # 촬영 컷수
SHOT_INTERVAL = 3  # 촬영 간격 (초)

# def trigger_shutter():
#     """AppleScript를 통해 FUJIFILM TETHER APP의 셔터를 누릅니다."""
#     script = """
#     tell application "System Events"
#         tell process "FUJIFILM TETHER APP"
#             set frontmost to true
#             try
#                 click menu item "Shutter button" of menu "Camera" of menu bar 1
#             on error
#                 key code 111 -- F12 키 코드
#             end try
#         end tell
#     end tell
#     """
#     os.system(f"osascript -e '{script}'")

def get_current_files():
    if not os.path.exists(WATCH_DIR): return []
    files = [os.path.join(WATCH_DIR, f) for f in os.listdir(WATCH_DIR) 
             if f.lower().endswith(('.jpg', '.jpeg'))]
    files.sort(key=os.path.getmtime)
    return files

def main():
    for d in [WATCH_DIR, RESULT_DIR]:
        if not os.path.exists(d): os.makedirs(d, exist_ok=True)

    print("\n" + "="*45)
    print("   Bamboo Studio v5.0")
    print("="*45)
    print("👉 엔터를 누르면 시작합니다.")
    
    initial_files = get_current_files()

    try:
        while True:
            cmd = input("\n[Enter]: 촬영 시작 / [q]: 종료 -> ")
            if cmd.lower() == 'q': break

            # # 1. 촬영 시퀀스
            # 자동 촬영 기능을 넣으려 했으나, 후지필름 카메라와 gphoto2의 연결 오류로 인해 수동 촬영으로 전환
            print("👉 4장을 촬영해주세요!\n")

            # 2. 파일 수집 및 합성 대기
            print("\n⏳ 사진이 전송되기를 기다리는 중...")
            photo_paths = []
            timeout = 60 # 최대 60초 대기
            start_time = time.time()

            while len(photo_paths) < TOTAL_SHOTS:
                if time.time() - start_time > timeout:
                    print("❌ 타임아웃: 사진 전송이 지연되고 있습니다.")
                    break
                
                current_all = get_current_files()
                # 초기 파일 리스트 이후에 생긴 파일들만 추출
                photo_paths = [f for f in current_all if f not in initial_files]
                time.sleep(0.5)

            if len(photo_paths) >= TOTAL_SHOTS:
                print("🎨 4장 수집 완료! 합성을 시작합니다...")
                time.sleep(2.0) # 파일 쓰기 완료 대기
                
                timestamp = datetime.now().strftime('%H%M%S')
                out_path = os.path.join(RESULT_DIR, f"Bamboo_{timestamp}.jpg")
                
                final = addPhotos2Frame.create_life4cut(photo_paths[:4], FRAME_PATH, out_path)
                
                if final:
                    print(f"✅ 완성! {final}")
                    # os.system(f"open {final}") 
                    # 즉시 보기
                
                # 다음 세션을 위해 현재 상태를 다시 기준으로 잡음
                initial_files = get_current_files()

    except KeyboardInterrupt:
        print("\n👋 종료합니다.")

if __name__ == "__main__":
    main()