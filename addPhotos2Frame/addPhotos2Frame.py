# from PIL import Image      


# def create4CutPhotoImages(path2Photos):

#     base_dir = os.path.dirname(os.path.abspath(__file__))

#     # 사진이 4장이 아니라면 종료
#     if len(path2Photos) != 4:
#         print("4장의 사진이 필요합니다.")
#         return

#     canvas = Image.new("RGB", (1200, 1800), "white")
#     photosPositions = [(87, 61), (88, 432), (88, 803), (88, 1173)]
#     IMG_WIDTH = 438
#     IMG_HEIGHT = 331
#     OFFSET_X = -5
#     OFFSET_Y = -5

#     for i, (x, y) in enumerate(photosPositions):
#         if i >= len(path2Photos):
#             break

#         x, y = photosPositions[i]

#         try:
#             # 위에 미리 지정해둔 위치로 사진들 넣기
#             targetImg = Image.open(path2Photos[i]).convert("RGB")

#             #targetImg.thumbnail((428, 321))
#             targetImg = targetImg.resize((IMG_WIDTH, IMG_HEIGHT))

#             final_x = x + OFFSET_X
#             final_y = y + OFFSET_Y

#             '''
#                 (87.3, 61.3, 516.3, 382.3),
#                 (88.3, 432, 516.3, 753),
#                 (88.3, 803, 516.3, 1124),
#                 (88.3, 1173, 516.3, 1495),
#                 (691.1, 61.3, 1119.1, 382.3),
#                 (691.1, 432, 1119.1, 753),
#                 (691.1, 803, 1119.1, 1124),
#                 (691.1, 1173, 1119.1, 1495)
#             '''
#             # 왼쪽에 사진 넣기
#             canvas.paste(targetImg, (final_x, final_y))

#             # 오른쪽에 같은 사진 넣기
#             canvas.paste(targetImg, (final_x + 603, final_y))

#         except FileNotFoundError:
#             print(f"{path2Photos} not found. Skipping.")
#             continue

#     try:
#         frameFileName = "addPhotos2Frame/밤부_인생네컷_최종mk2.png"
#         frameImg = Image.open(frameFileName).convert("RGBA")

#         if frameImg.size != canvas.size:
#             frameImg = frameImg.resize(canvas.size)

#         canvas.paste(frameImg, (0, 0), frameImg)

#     except FileNotFoundError:
#         print(f"{frameFileName} not found. Skipping frame overlay.")


#     outputFileName = "addPhotos2Frame/result_addPhotos2Frame.jpg"
#     canvas.save(outputFileName)


# if __name__ == "__main__":
#     path2Photo = ["000001790025.jpg", "000001790026.jpg", "000001790027.jpg", "000001790028.jpg"]
#     create4CutPhotoImages(path2Photo)


import os
from PIL import Image

def create4CutPhotoImages(path2Photos):
    # 1. 현재 스크립트 파일이 있는 폴더 경로 확보
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 사진이 4장이 아니라면 종료
    if len(path2Photos) != 4:
        print(f"에러: 4장의 사진이 필요합니다. (현재 {len(path2Photos)}장)")
        return

    # 배경 캔버스 생성 (1200x1800)
    canvas = Image.new("RGB", (1200, 1800), "white")
    
    # 좌표 및 설정
    photosPositions = [(87, 61), (88, 432), (88, 803), (88, 1173)]
    IMG_WIDTH = 438
    IMG_HEIGHT = 331
    OFFSET_X = -5
    OFFSET_Y = -5

    for i, (x, y) in enumerate(photosPositions):
        # 개별 사진의 절대 경로 생성
        photo_path = os.path.join(base_dir, path2Photos[i])
        
        try:
            targetImg = Image.open(photo_path).convert("RGB")
            targetImg = targetImg.resize((IMG_WIDTH, IMG_HEIGHT))

            final_x = x + OFFSET_X
            final_y = y + OFFSET_Y

            # 왼쪽에 사진 넣기
            canvas.paste(targetImg, (final_x, final_y))
            # 오른쪽에 사진 넣기
            canvas.paste(targetImg, (final_x + 603, final_y))
            print(f"✅ 사진 합성 완료: {path2Photos[i]}")

        except FileNotFoundError:
            print(f"❌ 파일을 찾을 수 없음: {photo_path}")
            continue

    # 2. 프레임 합성
    # 스크립트와 같은 폴더에 있다고 가정
    frameFileName = "밤부_인생네컷_최종mk3.png" 
    frame_path = os.path.join(base_dir, frameFileName)

    try:
        frameImg = Image.open(frame_path).convert("RGBA")
        if frameImg.size != canvas.size:
            frameImg = frameImg.resize(canvas.size)
        
        # 프레임을 캔버스 위에 덮어쓰기
        canvas.paste(frameImg, (0, 0), frameImg)
        print(f"✅ 프레임 합성 완료: {frameFileName}")

    except FileNotFoundError:
        print(f"⚠️ 프레임 파일을 찾을 수 없습니다: {frame_path}")

    # 3. 결과 저장
    outputFileName = "result_addPhotos2Frame.jpg"
    output_path = os.path.join(base_dir, outputFileName)
    canvas.save(output_path, quality=95)
    print(f"\n🎉 최종 결과물이 저장되었습니다: {output_path}")


if __name__ == "__main__":
    # 파일 이름들 (이 파일들이 스크립트와 같은 폴더에 있어야 합니다)
    photos = ["예시사진1.jpg", "예시사진2.jpg", "예시사진3.jpg", "예시사진4.jpg"]
    create4CutPhotoImages(photos)