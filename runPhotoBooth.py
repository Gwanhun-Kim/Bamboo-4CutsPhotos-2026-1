import os
import time
import subprocess
from datetime import datetime
from PIL import Image

TEST_MODE = False  # 테스트 모드 설정
BASE_SAVE_DIR = "Bamboo_Studio" 

def kill_mac_camera_process():
    """프로세스를 죽이는 대신, 포트 소유권을 가져오기 위해 리셋 시도"""
    # pkill은 프로세스가 없어도 에러를 내지 않으므로 sudo 없이 실행
    subprocess.run(["pkill", "-9", "PTPCamera"], stderr=subprocess.DEVNULL)
    time.sleep(0.5)
    
    # 🌟 gphoto2 자체 기능을 이용해 USB 포트를 강제 리셋
    # 이 명령어가 하드웨어 수준에서 연결을 초기화해줍니다.
    subprocess.run(["gphoto2", "--reset"], stderr=subprocess.DEVNULL)
    time.sleep(1.0) 

def capture_photo(filename):
    # 이제 매 컷마다 초기화하지 않고, 그냥 촬영만 수행합니다.
    cmd = ["gphoto2", "--capture-image-and-download", "--force-overwrite", "--filename", filename]
    try:
        # 촬영 전 카메라가 살아있는지 확인하는 용도로만 사용
        subprocess.run(cmd, check=True, timeout=15) # 15초 타임아웃 추가
        return os.path.exists(filename)
    except Exception as e:
        print(f"❌ 촬영 에러 (연결 상태 확인 필요): {e}")
        return False

def run_booth():
    session_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_path = os.path.join(BASE_SAVE_DIR, session_name)
    if not os.path.exists(session_path):
        os.makedirs(session_path)

    # ⭐ 중요: 촬영 세션 시작 전 '딱 한 번'만 프로세스를 정리합니다.
    kill_mac_camera_process() 

    print(f"\n📸 밤부 사진관 세션 시작: {session_name}")
    input("👉 엔터키를 누르면 4컷 촬영이 시작됩니다...")

    current_photos = []
    for i in range(1, 5):
        print(f"\n[{i}/4] {i}번째 컷 준비!")
        for countdown in range(3, 0, -1): # 테스트를 위해 3초로 단축 (실제 환경에선 8초 권장)
            print(f"{countdown}...")
            time.sleep(1)

        filename = os.path.join(session_path, f"shot_{i}.jpg")
        
        if capture_photo(filename):
            print(f"✨ 찰칵! 저장 완료")
            current_photos.append(filename)
        else:
            print(f"⚠️ {i}번째 촬영 실패.")
        
        time.sleep(0.5)

    return current_photos # 중요: 촬영된 4장의 경로 리스트를 반환