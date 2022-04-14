# 프로그램 설계
# 1. x, y, dx, dy 랜덤 설정
# 2. color.jpg와 putText의 bitwise_and연산을 통하여 글자 삽입, 마스킹
# 3. Text의 좌표값을 재지정하면서 움직이는 것처럼 구현
# 4. 2,3과정을 무한루프
# 5. imwrite를 통해 마스킹한 것을 이미지파일로 생성
# 6. 생성된 이미지 파일을 대상으로 비디오 캡쳐 및 저장
import numpy as np, cv2
import random

move_x_or_y = [-1, 1]   #dx와 dy가 랜덤으로 뽑을 수
img = cv2.imread('color.jpg')   #이미지 불러오기
w, h = 480, 360 #이미지 크기(원본 크기)
x, y = random.randrange(0, w), random.randrange(0, h)   #x는 0~480의 랜덤 수, y는 0~360의 랜덤수를 얻는다
dx, dy = int(random.choice(move_x_or_y)), int(random.choice(move_x_or_y))   #dx, dy에 -1 or 1을 랜덤으로 뽑는다. 이동할 좌표 ex)dx가 1이면 x축을 1로 이동

# 과제에서 정해진 조건을 입력
fps = 29.97 #초당 프레임 수
delay = round(1000/fps) #프레임 간 지연 시간
size = (w, h)   #동영상 파일 해상도
fourcc = cv2.VideoWriter_fourcc(*'DX50')    #프레임 압축에 사용되는 코덱

writer = cv2.VideoWriter('ScreenProtect_20182152.avi', fourcc, fps, size)   #동영상 출력을 위해 사용

while(True):
    # img와 마스킹할 mask를 만듦
    mask = np.zeros_like(img)  # np.zeros_like : 어떤 변수만큼의 사이즈인 0 으로 가득 찬 Array를 배출한다. 즉 img만큼의 사이즈 0(검정색)의 Array
    cv2.putText(mask, 'ChoiHaneol', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3) #랜덤 좌표를 시작으로 흰색, 굵기 3, 크기 1, 폰트 cv2.FONT_HERSHEY_SIMPLEX 의 Text를 mask배열에 삽입
    masked = cv2.bitwise_and(img, mask) #bitwise_and를 통해 이미지 연산, 비트 연산으로 겹치는 부분 출력, mask는 text부분이 255 나머지 0. img의 rgb값과 text부분이 겹치는 영역을 출력 ex) img(233,124,234) & mask(255,255,255) => masked(233,124,234)
    cv2.imwrite("ScreenProtect.jpg", masked)    #마스킹한 이미지를 해당 파일로 저장

    if cv2.waitKey(delay) == ord('q'): break    #키보드로 q가 입력되면 break

    writer.write(cv2.imread("ScreenProtect.jpg")) #jpg파일을 읽어서 write

    cv2.imshow('ScreenProtect_20182152', masked)    #masked를 창으로 띄워서 보여줌

    #벽에 부딪힐 때의 좌표 이동 값. 90도이기 때문에 x, y중 하나의 좌표만 정 반대로(1 => -1, -1 => 1) 설정, 만약 x, y 둘 다 바꾸면 180도로 바뀜
    if x < 0:   #text의 x좌표가 0(왼쪽벽)에 부딪힐 때
        dx = 1  #dx를 1로 , 아래의 조건도 같은 원리로 구현
    elif x > w:
        dx = -1
    if y < 0:
        dy = 1
    elif y > h:
        dy = -1
    x += dx
    y += dy

writer.release() #동영상 장치 해제 알아서 호출되서 굳이 안적어도 됨
cv2.waitKey()
cv2.destroyAllWindows()