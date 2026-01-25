# import subprocess
# import os
# import time
#
# # 사진이 저장될 폴더 이름
# SAVE_DIR = "Bamboo_Test_Shot"
#
#
# def kill_mac_camera_process():
#     """
#     [매우 중요] 맥북이 카메라를 자동으로 잡고 놓아주지 않는 'PTPCamera' 프로세스를 강제로 끕니다.
#     이게 켜져 있으면 gphoto2가 "장치를 사용할 수 없습니다"라며 에러를 냅니다.
#     """
#     print("🔄 맥 기본 카메라 연결 프로세스 정리 중...")
#     subprocess.run(["pkill", "-9", "PTPCamera"])
#     time.sleep(1)  # 프로세스가 죽을 때까지 잠깐 대기
#
#
# def test_capture():
#     # 폴더가 없으면 생성
#     if not os.path.exists(SAVE_DIR):
#         os.makedirs(SAVE_DIR)
#
#     print(f"📸 {SAVE_DIR} 폴더로 촬영 테스트를 시작합니다...")
#
#     # gphoto2 명령어: 촬영하고(--capture-image) 바로 다운로드(--and-download)
#     # --filename: 저장될 경로와 파일명 지정 (%H%M%S는 시분초)
#     filename = f"{SAVE_DIR}/test_shot_%H%M%S.jpg"
#
#     cmd = [
#         "gphoto2",
#         "--capture-image-and-download",
#         "--filename", filename,
#         "--force-overwrite"
#     ]
#
#     try:
#         # 명령어 실행
#         result = subprocess.run(cmd, capture_output=True, text=True)
#
#         # 성공 여부 확인
#         if result.returncode == 0:
#             print("\n✅ 성공! 셔터가 눌렸고 사진이 전송되었습니다.")
#             print(f"저장 위치를 확인하세요: {os.path.abspath(SAVE_DIR)}")
#         else:
#             print("\n❌ 실패했습니다.")
#             print("에러 내용:", result.stderr)
#
#             if "Could not claim the USB device" in result.stderr:
#                 print("👉 팁: USB 케이블을 뺐다 다시 꽂고 재시도해보세요.")
#
#     except Exception as e:
#         print(f"실행 중 오류 발생: {e}")
#
#
# if __name__ == "__main__":
#     kill_mac_camera_process()
#     test_capture()



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
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# [설정 구역] 여기만 수정하면 됩니다!
# ==========================================

# 1. 기능 켜기/끄기 (테스트할 때 편하게)
ENABLE_PRINT = True  # 프린터 연결됐으면 True, 아니면 False
ENABLE_CLOUD = False  # Firebase 키 파일 있으면 True (QR코드 생성용)

# 2. 프린터 이름 (터미널에서 'lpstat -p' 로 확인한 이름 정확히 입력)
PRINTER_NAME = "Canon_CP1500"  # 예: "Canon_SELPHY_CP1500"

# 3. 파일 저장 경로
SAVE_DIR = "Bamboo_Photos"
TEMPLATE_PATH = "frame_template.png"  # 배경 프레임 파일명

# 4. Firebase 설정 (ENABLE_CLOUD = True 일 때만 필요)
FIREBASE_KEY_PATH = "serviceAccountKey.json"
FIREBASE_BUCKET = "your-project-id.appspot.com"

# ==========================================

# Firebase 라이브러리 (옵션)
if ENABLE_CLOUD:
    import firebase_admin
    from firebase_admin import credentials, storage
    import qrcode

    # 앱이 이미 초기화되었는지 확인 후 초기화
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred, {'storageBucket': FIREBASE_BUCKET})


# def speak(text):
#     """맥북 자체 음성 합성(TTS) 사용"""
#     os.system(f'say "{text}"')


def kill_mac_camera_process():
    """방해되는 PTPCamera 프로세스 종료"""
    subprocess.run(["pkill", "-9", "PTPCamera"])
    time.sleep(0.5)


def capture_photo(filename):
    """gphoto2로 촬영 및 다운로드"""
    print(f"📸 촬영 중: {filename}")
    cmd = [
        "gphoto2", "--capture-image-and-download",
        "--filename", filename, "--force-overwrite"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def create_photostrip(photo_files, output_path):
    """
    4장의 사진을 받아 4x6인치(1800x1200px) 이미지로 합성
    구조: 인생네컷 2줄(1+1)이 들어가는 형태
    """
    print("🎨 사진 합성 중...")

    # 1. 캔버스 준비 (4x6인치, 300dpi 기준 약 1800x1200)
    # 템플릿 파일이 있으면 쓰고, 없으면 흰 배경 생성
    if os.path.exists(TEMPLATE_PATH):
        bg = Image.open(TEMPLATE_PATH).convert("RGB")
        bg = bg.resize((1800, 1200))
    else:
        bg = Image.new("RGB", (1800, 1200), "white")

    # 2. 사진 배치 좌표 설정 (예시: 왼쪽 줄 기준)
    # (x, y, 가로크기, 세로크기) - 프레임 디자인에 맞춰 수정 필요
    # 여기서는 대략적인 4컷 좌표를 잡습니다.
    # 사진 크기: 가로 700, 세로 500 정도라고 가정
    photo_positions = [
        (100, 50),  # 1번 사진
        (100, 330),  # 2번 사진
        (100, 610),  # 3번 사진
        (100, 890)  # 4번 사진
    ]

    photo_width = 700
    photo_height = 260  # 와이드하게 자르거나 비율 조절 필요

    # 3. 사진 4장을 순서대로 붙이기
    for i, path in enumerate(photo_files):
        img = Image.open(path)

        # 이미지 리사이징 (프레임 구멍 크기에 맞게)
        # 비율 유지하며 자르기(Crop) 로직이 들어가면 더 좋음, 여기선 단순 리사이즈
        img = img.resize((photo_width, photo_height))

        # 왼쪽 줄에 붙이기
        x, y = photo_positions[i]
        bg.paste(img, (x, y))

        # 오른쪽 줄에 복사해서 붙이기 (1+1 행사용)
        # 오른쪽 시작점이 x=950 이라고 가정
        bg.paste(img, (x + 850, y))

    # 4. QR 코드 공간이 있다면 여기에 QR 붙이기 로직 추가 가능

    bg.save(output_path, quality=100)
    return output_path


def upload_and_get_qr(file_path):
    """Firebase에 올리고 QR 이미지 반환"""
    if not ENABLE_CLOUD:
        return None

    print("☁️ 클라우드 업로드 중...")
    unique_name = f"bamboo_{uuid.uuid4()}.jpg"
    bucket = storage.bucket()
    blob = bucket.blob(unique_name)

    # 업로드용으로 이미지 리사이즈 (속도 향상)
    # (원본이 아닌 리사이즈본을 올리는 게 빠름 - 여기선 원본 업로드 예시)
    blob.upload_from_filename(file_path)
    blob.make_public()

    url = blob.public_url
    print(f"🔗 URL 생성됨: {url}")

    # QR 생성
    qr = qrcode.QRCode(box_size=5, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


def print_photo(file_path):
    """Mac CUPS 시스템으로 출력"""
    print(f"🖨️ 출력 명령 전송: {PRINTER_NAME}")
    # lp 명령어 옵션: -o media=Postcard (4x6인치 지정, 프린터마다 다를 수 있음)
    subprocess.run(["lp", "-d", PRINTER_NAME, "-o", "media=Postcard", "-o", "fit-to-page", file_path])


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

    # 1. 4컷 촬영 루프
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

    # 2. 사진 합성
    speak("사진을 예쁘게 만들고 있습니다.")
    final_output = f"{SAVE_DIR}/final_{int(time.time())}.jpg"
    create_photostrip(current_photos, final_output)

    # 3. QR 코드 (옵션)
    if ENABLE_CLOUD:
        qr_img = upload_and_get_qr(final_output)
        if qr_img:
            # 합성된 사진 위에 QR 덧붙이기 (오른쪽 하단 구석 등)
            bg = Image.open(final_output)
            qr_img = qr_img.resize((150, 150))  # QR 크기 조절
            bg.paste(qr_img, (800, 1000))  # 위치 조절 필요
            bg.save(final_output)

    # 4. 출력
    if ENABLE_PRINT:
        speak("사진을 출력합니다. 잠시만 기다려주세요.")
        print_photo(final_output)
    else:
        speak("완료되었습니다.")
        # 사진 자동 열기 (확인용)
        subprocess.run(["open", final_output])


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