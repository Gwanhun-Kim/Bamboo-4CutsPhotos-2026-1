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


from PIL import Image
import os

def create_life4cut(photo_paths, frame_path, output_path="result_final.jpg"):
    """
    4장의 사진 경로 리스트를 받아 인생네컷을 생성하는 함수
    
    Args:
        photo_paths (list): 사진 파일 경로 4개가 담긴 리스트
        frame_path (str): 프레임(배경 투명 PNG) 파일 경로
        output_path (str): 결과물을 저장할 경로 (기본값: result_final.jpg)
        
    Returns:
        str: 성공 시 생성된 파일 경로, 실패 시 None
    """
    
    # 1. 기초 유효성 검사
    if len(photo_paths) != 4:
        print(f"[Error] 사진은 정확히 4장이 필요합니다. (입력됨: {len(photo_paths)}장)")
        return None
        
    if not os.path.exists(frame_path):
        print(f"[Error] 프레임 파일을 찾을 수 없습니다: {frame_path}")
        return None

    # 2. 캔버스 및 상수 설정
    canvas = Image.new("RGB", (1200, 1800), "white")
    photos_positions = [(87, 61), (88, 432), (88, 803), (88, 1173)]
    
    IMG_WIDTH = 438
    IMG_HEIGHT = 331
    OFFSET_X = -5
    OFFSET_Y = -5
    RIGHT_STRIP_GAP = 603

    # 3. 사진 합성 루프
    for i, photo_path in enumerate(photo_paths):
        if i >= 4: break # 안전장치
        
        x, y = photos_positions[i]
        
        try:
            target_img = Image.open(photo_path)
            target_img = target_img.resize((IMG_WIDTH, IMG_HEIGHT))

            final_x = x + OFFSET_X
            final_y = y + OFFSET_Y

            # 왼쪽 & 오른쪽 배치
            canvas.paste(target_img, (final_x, final_y))
            canvas.paste(target_img, (final_x + RIGHT_STRIP_GAP, final_y))

        except FileNotFoundError:
            print(f"[Warning] 사진 파일을 찾을 수 없습니다: {photo_path}. 해당 칸은 비워둡니다.")
            continue
        except Exception as e:
            print(f"[Error] 이미지 처리 중 오류 발생 ({photo_path}): {e}")
            continue

    # 4. 프레임 덮어쓰기
    try:
        frame_img = Image.open(frame_path).convert("RGBA")
        if frame_img.size != canvas.size:
            frame_img = frame_img.resize(canvas.size)

        canvas.paste(frame_img, (0, 0), frame_img)

    except Exception as e:
        print(f"[Error] 프레임 합성 실패: {e}")
        return None

    # 5. 저장
    try:
        canvas.save(output_path)
        print(f"✅ 인생네컷 생성 완료: {output_path}")
        return output_path
    except Exception as e:
        print(f"[Error] 파일 저장 실패: {e}")
        return None

# 테스트용 코드 (이 파일만 직접 실행했을 때만 작동)
if __name__ == "__main__":
    # 테스트 데이터 예시
    sample_photos = [
        "img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg"
    ]
    sample_frame = "frame.png"
    
    # 함수 호출 테스트
    create_life4cut(sample_photos, sample_frame, "test_result.jpg")