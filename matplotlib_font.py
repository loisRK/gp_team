import matplotlib.font_manager
import matplotlib.pyplot as plt
import platform

def font_setting() :
    if platform.system() == 'Darwin': #맥
            plt.rc('font', family='AppleGothic')
    elif platform.system() == 'Windows': #윈도우
            plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
            #!wget "https://www.wfonts.com/download/data/2016/06/13/malgun-gothic/malgun.ttf"
            #!mv malgun.ttf /usr/share/fonts/truetype/
            #import matplotlib.font_manager as fm
            #fm._rebuild()
            plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결
    #matplotlib 패키지 한글 깨짐 처리 끝



##### 한글깨짐 확인용 코드
# ratio = [18, 6, 4, 4, 6]
# labels = ['순살양념（보통맛）', '순살양념（순한맛）', '공기밥 추가', '뼈 양념치킨（보통맛）', '기타']
# plt.pie(ratio, labels=labels, autopct='%.1f%%')
# print(plt.show())