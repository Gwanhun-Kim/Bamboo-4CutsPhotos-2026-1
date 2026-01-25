from PIL import Image, ImageDraw

def createTransparentFrame(inputPath, outputPath, targetCoords):
    '''
    inputPath: a path of your original frame image
    outputPath: a path to save your file
    targetCoords: lists that you want to make transparent
    '''

    # 1. open Images and convert to RGBA
    targetImg = Image.open(inputPath).convert("RGBA")

    # 2. make Draw Object
    mask = Image.new("L", targetImg.size, 255)
    draw = ImageDraw.Draw(mask)

    # 3. fill sections with 0 (transparent)
    for box in targetCoords:
        int_box = tuple(map(int, box))
        draw.rectangle(int_box, fill=0)

    targetImg.putalpha(mask)
    

    targetImg.save(outputPath, "PNG")
    print(f"변환 완료: {outputPath}")


boxes = [
    (87.3, 61.3, 516.3, 382.3),
    (88.3, 432, 516.3, 753),
    (88.3, 803, 516.3, 1124),
    (88.3, 1173, 516.3, 1495),
    (691.1, 61.3, 1119.1, 382.3),
    (691.1, 432, 1119.1, 753),
    (691.1, 803, 1119.1, 1124),
    (691.1, 1173, 1119.1, 1495)
]

createTransparentFrame("밤부 인생네컷 프레임 mk21.png", "밤부 인생네컷 프레임 mk22.png", boxes)
