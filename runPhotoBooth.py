import os
import time
import subprocess
from datetime import datetime
from PIL import Image

TEST_MODE = False  # 테스트 모드 설정
BASE_SAVE_DIR = "Bamboo_Studio" 

def kill_mac_camera_process():
    """macOS 카메라 점유 프로세스를 반복해서 확실히 종료"""
    print("🔄 카메라 권한 확인 중...")
    processes = ["PTPCamera", "Photos", "Image Capture"]
    for proc in processes:
        try:
            # -9 옵션으로 강제 종료하고, 모든 사용자 프로세스(-a) 대상
            subprocess.run(["pkill", "-9", "-a", proc], stderr=subprocess.DEVNULL)
        except Exception:
            pass
    time.sleep(1) # 프로세스가 완전히 죽고 포트가 풀릴 때까지 대기

def capture_photo(filename):
    if TEST_MODE:
        time.sleep(0.5)
        # 테스트 모드 시 구분하기 쉽게 촬영 번호를 텍스트로 넣어도 좋지만, 일단 기본 로직 유지
        dummy = Image.new('RGB', (3000, 2000), color=(100, 150, 255))
        dummy.save(filename)
        return True
    else:
        cmd = ["gphoto2", "--capture-image-and-download", "--force-overwrite", "--filename", filename]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
            return os.path.exists(filename)
        except Exception as e:
            print(f"촬영 에러: {e}")
            return False

def run_booth():
    """촬영을 수행하고 저장된 파일 경로 리스트를 반환합니다."""
    session_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_path = os.path.join(BASE_SAVE_DIR, session_name)

    if not os.path.exists(session_path):
        os.makedirs(session_path)

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