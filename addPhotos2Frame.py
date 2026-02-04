import os
import qrcode
from PIL import Image

def create_bamboo_life4cut(photo_paths, frame_path, out_path, qr_data, logo_path=None):
    """
    frame_path: 이미 사진 구멍이 뚫려 있는 '밤부_인생네컷_최종mk4.png'
    """
    # 사진을 배치할 바닥 좌표
    boxes = [
        (87, 61, 519, 385), (88, 432, 519, 755),
        (88, 803, 519, 1126), (88, 1173, 519, 1497),
        (691.1, 61, 1121, 383), (691.1, 432, 1121, 754),
        (691.1, 803, 1121, 1125), (691.1, 1173, 1122, 1496)
    ]
    
    try:
        # 1. 이미 구멍 뚫린 프레임 로드 (RGBA 모드 필수)
        overlay_frame = Image.open(frame_path).convert("RGBA")
        
        # 2. 결과물이 그려질 흰색 바탕 캔버스 생성
        canvas = Image.new("RGBA", overlay_frame.size, (255, 255, 255, 255))
        
        # 3. [바닥 레이어] 사진들 먼저 배치
        for i, box in enumerate(boxes):
            photo_idx = i % len(photo_paths)
            img = Image.open(photo_paths[photo_idx]).convert("RGBA")
            
            box_w, box_h = int(box[2] - box[0]), int(box[3] - box[1])
            
            # 중앙 크롭 리사이즈
            img_ratio = img.width / img.height
            box_ratio = box_w / box_h
            if img_ratio > box_ratio:
                new_h = box_h
                new_w = int(box_h * img_ratio)
            else:
                new_w = box_w
                new_h = int(box_w / img_ratio)
                
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            img = img.crop(((new_w - box_w)/2, (new_h - box_h)/2, (new_w + box_w)/2, (new_h + box_h)/2))
            
            # 사진을 캔버스(바닥)에 붙임
            canvas.paste(img, (int(box[0]), int(box[1])))

        # 4. [중간 레이어] 사진 위에 투명 프레임 덮기
        # 세 번째 인자에 overlay_frame을 넣어줘야 투명 구멍으로 사진이 보입니다!
        canvas.paste(overlay_frame, (0, 0), overlay_frame)

        # 5. [최상단 레이어] QR 코드 2개 삽입
        qr_raw = qrcode.make(qr_data).convert("RGBA")
        qr_img = qr_raw.resize((100, 100))
        canvas.paste(qr_img, (88, 1675), qr_img)
        canvas.paste(qr_img, (691, 1675), qr_img)

        # 6. 저장 (JPEG는 투명도를 지원 안 하므로 RGB로 최종 변환)
        canvas.convert("RGB").save(out_path, "JPEG", quality=95)
        print(f"✅ 합성 성공: {os.path.basename(out_path)}")
        return out_path

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return None