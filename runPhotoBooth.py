import os
import time
import subprocess
from datetime import datetime  # 시간 정보 획득을 위해 추가
from PIL import Image

TEST_MODE = True
BASE_SAVE_DIR = "Bamboo_Studio" # 메인 저장 폴더

def kill_mac_camera_process():
    """macOS 카메라 점유 프로세스 종료"""
    try:
        subprocess.run(["pkill", "-9", "PTPCamera"], stderr=subprocess.DEVNULL)
        time.sleep(0.5)
    except Exception:
        pass

def capture_photo(filename):
    """사진 촬영 함수"""
    if TEST_MODE:
        time.sleep(0.5)
        dummy = Image.new('RGB', (3000, 2000), color=(100, 150, 255)) # 테스트용 푸른색
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
    # 1. 현재 시간을 기준으로 고유한 세션 폴더명 생성 (예: 20260127_180530)
    session_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_path = os.path.join(BASE_SAVE_DIR, session_name)

    # 2. 폴더가 없으면 생성
    if not os.path.exists(session_path):
        os.makedirs(session_path)
        print(f"📁 새 폴더 생성됨: {session_path}")

    kill_mac_camera_process()

    print(f"\n📸 밤부 사진관 [{session_name}] 세션을 시작합니다.")
    input("👉 엔터키를 누르면 4컷 촬영이 시작됩니다...")

    current_photos = []

    for i in range(1, 5):
        print(f"\n[{i}/4] 준비하세요!")
        for countdown in range(8, 0, -1):
            print(f"{countdown}...")
            time.sleep(1)

        # 3. 해당 세션 폴더 안에 파일 저장
        filename = os.path.join(session_path, f"shot_{i}.jpg")
        
        if capture_photo(filename):
            print(f"✨ 찰칵! {filename} 저장 완료")
            current_photos.append(filename)
        else:
            print("⚠️ 촬영 실패. 다음 컷으로 넘어갑니다.")
        
        time.sleep(1)

    print(f"\n✅ 촬영 종료. 총 {len(current_photos)}장의 사진이 {session_path}에 저장되었습니다.")
    return current_photos

if __name__ == "__main__":
    run_booth()
