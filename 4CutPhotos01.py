from PIL import Image      # 이미지를 열고, 자르고, 저장하는 기본 모듈
from PIL import ImageDraw  # 이미지 위에 선, 도형, 글자를 그리는 모듈
from PIL import ImageFont  # 텍스트 폰트를 설정하는 모듈

backGroundImg = Image.open("밤부 인생네컷 프레임 mk3.jpg")
targetImg_1 = Image.open("000001790025.JPG")
targetImg_2 = Image.open("000001790026.JPG")
targetImg_3 = Image.open("000001790027.JPG")
targetImg_4 = Image.open("000001790032.JPG")


canvas = Image.new("RGB", (1200, 1800), "white")
transparentCanvas = Image.new("RGB", (1200, 1800),(0, 0, 0, 0))

targetImg_1.thumbnail((428, 321))
targetImg_2.thumbnail((428, 321))
targetImg_3.thumbnail((428, 321))
targetImg_4.thumbnail((428, 321))





