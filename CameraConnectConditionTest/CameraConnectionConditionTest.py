import cv2

# 보통 내장 카메라는 0번, 캡처보드는 1번입니다.
# 1번으로 시도해보고 안 나오면 2번, 3번순으로 바꿔보세요.
cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()
    if not ret:
        print("화면을 불러올 수 없습니다. 인덱스를 확인하세요.")
        break
    
    cv2.imshow('BAMBOO X-T3 TEST', frame)
    
    # 'q' 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
