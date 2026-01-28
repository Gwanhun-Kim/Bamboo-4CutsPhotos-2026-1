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



# import os
# import time
# import subprocess
# import uuid
# from PIL import Image, ImageDraw, ImageFont
# import addPhotos2Frame
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler


# # 파일 저장 경로
# SAVE_DIR = "Bamboo_Photos"
# TEMPLATE_PATH = "frame_template.png"  # 배경 프레임 파일명

# # def speak(text):
# #     """맥북 자체 음성 합성(TTS) 사용"""
# #     os.system(f'say "{text}"')




# def getSavedFiles(SAVE_DIR):
#     files = os.listdir(SAVE_DIR)
#     #계속해서 더 만들어줘.

# if __name__ == "__main__":
#     while True:
#         try:
#             run_booth()
#             # 연속 촬영을 위해 루프
#             q = input("\n🔄 다시 찍으려면 엔터, 종료하려면 'q' 입력: ")
#             if q.lower() == 'q':
#                 break

#             addPhotos2Frame.create_life4cut()
#             '''
#             Args:
#                 photo_paths (list): 사진 파일 경로 4개가 담긴 리스트
#                 frame_path (str): 프레임(배경 투명 PNG) 파일 경로
#                 output_path (str): 결과물을 저장할 경로 (기본값: result_final.jpg)
                
#             Returns:
#                 str: 성공 시 생성된 파일 경로, 실패 시 None
#             '''
#         except Exception as e:
#             print(f"오류 발생: {e}")
#             break






# import checkNewFiles
# import addPhotos2Frame
# import runPhotoBooth
# from PIL import Image, ImageDraw, ImageFont
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler


import runPhotoBooth
import addPhotos2Frame



def main():
    print(dir(addPhotos2Frame)) # addPhotos2Frame 모듈 안에 무엇이 있는지 출력
    print("====================================")
    print("   Bamboo 4-Cuts System v1.0")
    print("====================================")

    while True:
        # 1. 촬영 수행 (파일 경로 리스트를 받아옴)
        photo_paths = runPhotoBooth.run_booth()

        # 2. 사진이 정상적으로 4장 찍혔는지 확인
        if len(photo_paths) == 4:
            print("\n🎨 모든 사진이 준비되었습니다. 합성을 시작합니다...")
            
            # 3. addPhotos2Frame 모듈로 경로 전달
            # 프레임 경로는 assets 폴더 내의 파일을 지정하세요.
            frame_image = "assets/frame.png"
            result_path = addPhotos2Frame.create_life4cut(photo_paths, frame_image, "result_final.jpg")
            
            print(f"✅ 완성! 결과물 경로: {result_path}")
        else:
            print(f"\n❌ 촬영이 정상적으로 완료되지 않았습니다. (확보된 사진: {len(photo_paths)}장)")

        # 4. 반복 여부 확인
        retry = input("\n다시 촬영하시겠습니까? (y/n): ")
        if retry.lower() != 'y':
            print("프로그램을 종료합니다.")
            break

if __name__ == "__main__":
    main()