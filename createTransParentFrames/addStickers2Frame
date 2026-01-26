# from PIL import Image, ImageDraw

# def addStickers2Frame(path2photos, locations):
#     frame = Image.open("밤부 인생네컷 프레임 mk22.png").convert("RGBA")
#     for i, path, (x, y) in enumerate(path2photos, locations):
#         # 1. open Images and convert to RGBA
#         sticker = Image.open(path).convert("RGBA")

#         # 2. paste sticker onto frame
#         frame.paste(sticker, (x, y), sticker)

#     frame.save("밤부 인생네컷 프레임 mk23.png")

# locations = [
#     (90, 170),
#     (300, 600),
#     (90, 1000),
#     (300, 1380),
#     (690, 170),
#     (900, 600),
#     (690, 1000),
#     (900, 1380)
# ]

# photos = [
#     "cameraImage.png",
#     "bambooImage.png",
#     "pandaImage.png",
#     "filmImage.png",
# ]

# addStickers2Frame(photos, locations)

import os
from PIL import Image

def addStickers2Frame(path2photos, locations):
    # 스크립트 위치 기준 절대 경로 확보
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. 프레임 파일명 확인 (png와 jpg 둘 다 체크하도록 수정)
    frame_name = "밤부 인생네컷 프레임 mk22.png" # 깃허브 파일명 기준
    frame_path = os.path.join(current_dir, frame_name)
    
    if not os.path.exists(frame_path):
        # 만약 png가 없다면 jpg로 한 번 더 시도
        frame_name = "밤부 인생네컷 프레임 mk22.jpg"
        frame_path = os.path.join(current_dir, frame_name)

    try:
        frame = Image.open(frame_path).convert("RGBA")
        print(f"✅ 프레임 로드 성공: {frame_name}")
    except FileNotFoundError:
        print(f"❌ 에러: 프레임 파일을 찾을 수 없습니다.")
        print(f"확인된 경로에 파일이 있는지 봐주세요: {current_dir}")
        return

    # 2. 스티커 로드 및 리사이징 (크기를 250으로 키웠습니다)
    sticker_size = (250, 250) 
    loaded_stickers = []

    for filename in path2photos:
        full_path = os.path.join(current_dir, filename)
        if os.path.exists(full_path):
            s = Image.open(full_path).convert("RGBA")
            s = s.resize(sticker_size)
            loaded_stickers.append(s)
            print(f"✅ 스티커 로드 성공: {filename}")
        else:
            print(f"⚠️ 경고: {filename} 없음 (경로: {full_path})")
            # 위치를 맞추기 위해 투명 이미지 삽입
            loaded_stickers.append(Image.new("RGBA", sticker_size, (0,0,0,0)))

    # 3. 스티커 배치
    for i, (x, y) in enumerate(locations):
        sticker = loaded_stickers[i % len(loaded_stickers)]
        frame.paste(sticker, (x, y), sticker)

    # 4. 결과 저장
    output_path = os.path.join(current_dir, "밤부_인생네컷_최종mk3.png")
    frame.save(output_path)
    print(f"\n🎉 작업 완료! 결과물: {output_path}")

# 설정값
locations = [
    (25, 170), (335, 535), (30, 950), (365, 1300),
    (625, 170), (935, 535), (630, 950), (965, 1300)
]
photos = ["cameraImage.png", "bambooImage.png", "pandaImage.png", "filmImage.png"]

if __name__ == "__main__":
    addStickers2Frame(photos, locations)