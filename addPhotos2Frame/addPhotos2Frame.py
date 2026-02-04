import os
import qrcode
from PIL import Image, ImageDraw

def create_bamboo_life4cut(photo_paths, frame_path, out_path, qr_data, logo_path=None):
    """
    photo_paths: 촬영된 사진 4장의 경로 리스트
    frame_path: 원본 프레임 이미지 경로 (mk21)
    out_path: 최종 결과물 저장 경로
    qr_data: 구글 드라이브 링크 (QR용)
    logo_path: 밤부 로고 이미지 경로
    """
    
    # 1. 프레임 구멍 좌표 (부장님의 mk21 기준)
    boxes = [
        (87.3, 61.3, 516.3, 382.3), (88.3, 432, 516.3, 753),
        (88.3, 803, 516.3, 1124), (88.3, 1173, 516.3, 1495),
        (691.1, 61.3, 1119.1, 382.3), (691.1, 432, 1119.1, 753),
        (691.1, 803, 1119.1, 1124), (691.1, 1173, 1119.1, 1495)
    ]
    
    try:
        # 프레임 로드 및 투명 구멍 뚫기
        base_frame = Image.open(frame_path).convert("RGBA")
        mask = Image.new("L", base_frame.size, 255)
        draw = ImageDraw.Draw(mask)
        for box in boxes:
            draw.rectangle(tuple(map(int, box)), fill=0)
        base_frame.putalpha(mask)
        
        # 2. 배경 캔버스 생성 (흰색 배경)
        canvas = Image.new("RGBA", base_frame.size, (255, 255, 255, 255))
        
        # 3. 사진 배치 (4장의 사진을 8개 구멍에 순차 배치)
        for i, box in enumerate(boxes):
            photo_idx = i % len(photo_paths)
            img = Image.open(photo_paths[photo_idx]).convert("RGBA")
            
            box_w = int(box[2] - box[0])
            box_h = int(box[3] - box[1])
            
            # 사진 비율 유지하며 리사이즈 (중앙 크롭 방식)
            img_ratio = img.width / img.height
            box_ratio = box_w / box_h
            
            if img_ratio > box_ratio:
                new_h = box_h
                new_w = int(box_h * img_ratio)
            else:
                new_w = box_w
                new_h = int(box_w / img_ratio)
                
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            left = (new_w - box_w) / 2
            top = (new_h - box_h) / 2
            img = img.crop((left, top, left + box_w, top + box_h))
            
            canvas.paste(img, (int(box[0]), int(box[1])))

        # 4. 프레임 덮기
        canvas.paste(base_frame, (0, 0), base_frame)

        # 5. QR 코드 생성 및 합성 (하단 중앙부)
        qr = qrcode.QRCode(box_size=4, border=1)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
        qr_img = qr_img.resize((160, 160))
        
        # 중앙 하단 여백 위치 계산 (프레임 디자인에 따라 조정 필요)
        qr_x = (canvas.width // 2) - (qr_img.width // 2)
        qr_y = canvas.height - 200 
        canvas.paste(qr_img, (qr_x, qr_y), qr_img)

        # 6. 밤부 로고 합성 (상단 중앙)
        if logo_path and os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo = logo.resize((150, 150))
            canvas.paste(logo, (canvas.width // 2 - 75, 20), logo)

        # 7. 최종 저장
        canvas.convert("RGB").save(out_path, "JPEG", quality=95)
        return out_path

    except Exception as e:
        print(f"합성 에러: {e}")
        return None