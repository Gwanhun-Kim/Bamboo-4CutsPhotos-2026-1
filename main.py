# from PIL import Image
#
# image = Image.open("/Users/kimgwanhun/Desktop/Pictures/밤부/25-2/가두모집/인생네컷/GWAN2843.JPG")
#
# # 이미지 가져오고 다른 이름으로 저장하기
# image.show()
# #image.save("/Users/kimgwanhun/Desktop/Pictures/밤부/25-2/가두모집/인생네컷/GWAN2843_1.JPG")
#
# # 이미지 크기 조절하기
# resized = image.resize((300, 200))
# resized.show()
#
# # 이미지 크롭하기
# cropped = image.crop((200, 200, 600, 600)) # left, upper, right, lower
# cropped.show()
#
# # 이미지 회전
# rotated = image.rotate(90)
# rotated.show()
#
# # 이미지 대칭
# flipped = image.transpose(Image.FLIP_LEFT_RIGHT)   # 좌우 대칭
# flipped = image.transpose(Image.FLIP_TOP_BOTTOM)   # 상하 대칭
# flipped.show()
#
# # 이미지 정보 가져오기
# print(image.filename)
# print(image.size)
# print(image.format)
# print(image.width)
# print(image.height)
# print(image.mode)
# # => 출력
# # (6240, 4160)
# # JPEG
# # 6240
# # 4160
# # RGB
#
#
# # 이미지 효과
# image_gray = image.convert('L') # 흑백으로 변환
# image_gray.show()
#
# # 1 (1비트 픽셀, 흑백, 바이트당 1픽셀로 저장)
# # L (8비트 픽셀, 흑백)
# # P (8비트 픽셀, 색상 팔레트를 사용하여 다른 모드에 매핑됨)
# # RGB (3x8비트 픽셀, 트루 컬러)
# # RGBA (4x8비트 픽셀, 투명 마스크가 있는 트루 컬러)
# # CMYK (4x8비트 픽셀, 색상 분리)
# # YCbCr (3x8비트 픽셀, 컬러 비디오 형식)
# # LAB (3x8비트 픽셀, Lab 색 공간)
# # HSV (3x8비트 픽셀, 색조, 채도, 값 색 공간)
# # I (32비트 부호 있는 정수 픽셀)
# # F (32비트 부동 소수점 픽셀)
#
#
#
# # 이미지 필터
# from PIL import ImageFilter
# image_blurred = image.filter(ImageFilter.GaussianBlur(10))
# image_blurred.show()
#
# # BLUR : BLUR, BoxBlur( ), GaussianBlur( )
# # MedianFilter( ), MinFilter( ), MaxFilter( ) 등
# # CONTOUR
# # DETAIL
# # EDGE_ENHANCE, EDGE_ENHANCE_MORE
# # EMBOSS
# # FIND_EDGES
# # SHARPEN
# # SMOOTH, SMOOTH_MORE



import os
import time
import subprocess
import uuid
import addPhotos2Frame as photoMaker
from PIL import Image, ImageDraw, ImageFont


# 파일 저장 경로
SAVE_DIR = "Bamboo_Photos"
TEMPLATE_PATH = "frame_template.png"  # 배경 프레임 파일명

# def speak(text):
#     """맥북 자체 음성 합성(TTS) 사용"""
#     os.system(f'say "{text}"')


def kill_mac_camera_process():
    """방해되는 PTPCamera 프로세스 종료"""
    subprocess.run(["pkill", "-9", "PTPCamera"])
    time.sleep(0.5)

# ==========================================
# 메인 실행 함수
# ==========================================
def run_booth():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    kill_mac_camera_process()

    print("\n👋 안녕하세요! 밤부 사진관입니다.")
    speak("안녕하세요. 밤부 사진관입니다. 촬영을 시작하시려면 엔터키를 눌러주세요.")
    input("👉 엔터키를 누르면 촬영이 시작됩니다...")

    current_photos = []

    # 4컷 촬영 루프
    for i in range(1, 5):
        print(f"\n[{i}/4] 촬영 준비...")
        speak(f"{i}번째 사진을 찍습니다.")
        time.sleep(1)

        # 카운트다운
        speak("쓰리")
        time.sleep(1)
        speak("투")
        time.sleep(1)
        speak("원")

        # 촬영
        filename = f"{SAVE_DIR}/shot_{i}_{int(time.time())}.jpg"
        if capture_photo(filename):
            current_photos.append(filename)
            speak("찰칵")
        else:
            speak("촬영 실패. 다시 시도합니다.")
            return  # 에러 처리

        time.sleep(1)  # 다음 컷 대기



if __name__ == "__main__":
    while True:
        try:
            run_booth()
            # 연속 촬영을 위해 루프
            q = input("\n🔄 다시 찍으려면 엔터, 종료하려면 'q' 입력: ")
            if q.lower() == 'q':
                break
        except Exception as e:
            print(f"오류 발생: {e}")
            break


