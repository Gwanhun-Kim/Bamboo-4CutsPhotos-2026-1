from PIL import Image      

def create4CutPhotoImages():
    canvas = Image.new("RGB", (1200, 1800), "white")
    photosPositions = [(87, 61), (88, 432), (88, 803), (88, 1173)]
    IMG_WIDTH = 438
    IMG_HEIGHT = 331

    OFFSET_X = -5
    OFFSET_Y = -5

    for i, (x, y) in enumerate(photosPositions):
        try:
            # 위에 미리 지정해둔 위치로 사진들 넣기
        
            fileName = f"0000017900{25 + i}.JPG"
            targetImg = Image.open(fileName)

            #targetImg.thumbnail((428, 321))
            targetImg = targetImg.resize((IMG_WIDTH, IMG_HEIGHT))

            final_x = x + OFFSET_X
            final_y = y + OFFSET_Y

            '''
                (87.3, 61.3, 516.3, 382.3),
                (88.3, 432, 516.3, 753),
                (88.3, 803, 516.3, 1124),
                (88.3, 1173, 516.3, 1495),
                (691.1, 61.3, 1119.1, 382.3),
                (691.1, 432, 1119.1, 753),
                (691.1, 803, 1119.1, 1124),
                (691.1, 1173, 1119.1, 1495)
            '''
            # 왼쪽에 사진 넣기
            canvas.paste(targetImg, (final_x, final_y))

            # 오른쪽에 같은 사진 넣기
            canvas.paste(targetImg, (final_x + 603, final_y))

        except FileNotFoundError:
            print(f"{fileName} not found. Skipping.")
            continue

        try:
            frameFileName = "밤부 인생네컷 프레임 mk23.png"
            frameImg = Image.open(frameFileName).convert("RGBA")

            if frameImg.size != canvas.size:
                frameImg = frameImg.resize(canvas.size, Image.ANTIALIAS)

            canvas.paste(frameImg, (0, 0), frameImg)

        except FileNotFoundError:
            print(f"{frameFileName} not found. Skipping frame overlay.")


    outputFileName = "result_addPhotos2Frame.jpg"
    canvas.save(outputFileName)

if __name__ == "__main__":
    create4CutPhotoImages()