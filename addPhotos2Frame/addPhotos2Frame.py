import os
import time
import addPhotos2Frame
from datetime import datetime

# [환경 설정]
WATCH_DIR = "/Users/kimgwanhun/Desktop/Pictures/밤부/26-1/가두모집/인생네컷/Bamboo_Studio"  # 사진이 들어오는 곳
RESULT_DIR = "/Users/kimgwanhun/Desktop/Pictures/밤부/26-1/가두모집/인생네컷/Bamboo_Results" # 결과물이 저장될 곳
FRAME_PATH = "assets/frame.png"
TOTAL_SHOTS = 4

def get_current_jpg_files():
    return [os.path.join(WATCH_DIR, f) for f in os.listdir(WATCH_DIR) 
            if f.lower().endswith(('.jpg', '.jpeg'))]

def main():
    # 저장 폴더들이 없으면 자동으로 생성합니다.
    for directory in [WATCH_DIR, RESULT_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📂 폴더 생성 완료: {directory}")

    print("====================================")
    print("   Bamboo Photo Watcher v4.1")
    print("====================================")
    print(f"📍 사진 감시: {WATCH_DIR}")
    print(f"📍 결과 저장: {RESULT_DIR}")
    print(f"👉 리모컨으로 {TOTAL_SHOTS}장을 촬영하세요.")

    initial_files = get_current_jpg_files()
    last_count = len(initial_files)

    try:
        while True:
            current_files = get_current_jpg_files()
            current_count = len(current_files)
            
            if current_count > last_count:
                new_files_count = current_count - len(initial_files)
                print(f"📸 새 사진 감지! ({new_files_count}/{TOTAL_SHOTS})")
                
                if new_files_count >= TOTAL_SHOTS:
                    print("\n🎨 4장 수집 완료! 합성을 시작합니다...")
                    
                    current_files.sort(key=os.path.getmtime)
                    photo_paths = current_files[-TOTAL_SHOTS:]
                    
                    time.sleep(1.5)
                    
                    # 🌟 결과물 파일명을 경로와 함께 생성
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    result_filename = f"Bamboo_Cut_{timestamp}.jpg"
                    output_path = os.path.join(RESULT_DIR, result_filename)
                    
                    # 합성 함수 호출 (output_path 전달)
                    final_path = addPhotos2Frame.create_life4cut(photo_paths, FRAME_PATH, output_path)
                    
                    if final_path:
                        print(f"✅ 완성! 저장 위치: {final_path}")
                        # os.system(f"open {final_path}")
                    
                    initial_files = get_current_jpg_files()
                    print("\n" + "-"*30)
                    print("👉 다음 세션 준비 완료. 다시 촬영하세요.")
                
                last_count = current_count
            
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")

if __name__ == "__main__":
    main()