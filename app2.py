import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 글꼴 설정
font_path = "NanumGothic.ttf"
font_manager.fontManager.addfont(font_path)
rc('font', family='NanumGothic')

st.set_page_config(layout="wide")

# 점수 관리
if "results" not in st.session_state:
    st.session_state["results"] = {}

# 점수 저장 함수
def save_results(subject, score):
    st.session_state["results"][subject] = score

# 점수 초기화 함수
def reset_results():
    st.session_state["results"] = {}

# 교과 문제 데이터
quiz_data = {
    "✨통합교과": [
         {"question": "훈민정음을 만든 사람은?", "options": ["세종대왕", "이순신", "강감찬"], "answer": "세종대왕"},
        {"question": "인도의 수도는?", "options": ["뉴델리", "도쿄", "베이징"], "answer": "뉴델리"},
        {"question": "다음 중 발명품이 아닌 것은?", "options": ["컴퓨터", "단풍나무", "연필", "칫솔"], "answer": "단풍나무"},
        {"question": "날씨의 변화를 예측하여 미리 알려주는 것을 무엇이라고 부를까요?", "options": ["일기예보", "기상청", "뉴스"], "answer": "일기예보"},
        {"question": "낮이 가장 긴 절기는?", "options": ["하지", "동지", "춘분"], "answer": "하지"},
        {"question": "나는 꿈이 있어요 우리 가족을 지키는 (  )", "options": ["슈퍼맨", "아빠", "경찰"], "answer": "슈퍼맨"},
        {"question": "가을이 제철인 과일을 모두 고르세요.", "options": ["수박", "귤", "딸기", "감"], "answer": "감"},
        {"question": "빵, 케이크 등을 만들고 판매하는 직업은 무엇입니까?", "options": ["제과제빵사", "경찰관", "미용사"], "answer": "제과제빵사"},
        {"question": "중국 전통의상의 이름은?", "options": ["치파오", "기모노", "한복"], "answer": "치파오"},
        {"question": "우리 학교가 있는 구의 이름은?","options":["강서구", "양천구", "광진구"],"answer":"양천구"}
    ],
    "🔢수학": [
        {"question": "사탕을 보미는 4개의 3배, 희주는 3개의 5배만큼 가지고 있습니다. 두 사람이 가지고 있는 사탕은 모두 몇 개인가요?", "options": ["27개", "30개", "33개"], "answer": "27개"},
        {"question": "아버지의 나이는 38세이고 나의 나이는 9살입니다. 나는 아버지보다 몇 살 더 적을까요?", "options": ["29살", "27살", "30살"], "answer": "29살"},
        {"question": "100이 7개, 10이 5개, 1이 8개인 수는 무엇인가요?", "options": ["758", "785", "857"], "answer": "758"},
        {"question": "덧셈식을 계산하세요. 78+17=", "options": ["95", "85", "97"], "answer": "95"},
        {"question": "변과 꼭짓점이 4개인 도형은 무엇입니까?", "options": ["사각형", "삼각형", "원"], "answer": "사각형"},
        {"question": "1m는 몇 cm입니까?", "options": ["100cm", "10cm", "1000cm"], "answer": "100cm"},
        {"question": "6572부터 100씩 5번 뛰어 센 수는 얼마일까요?", "options": ["7072", "7272", "7172"], "answer": "7072"},
        {"question": "곱셈식을 계산하세요. 8x0=?", "options": ["0", "8", "1"], "answer": "0"},
        {"question": "2일은 몇 시간인가요?","options":["24시간","48시간","50시간"],"answer":"48시간"},
        {"question": "곱셈식을 계산하세요.6x7=", "options":["35","28","42"],"answer":"42"}
    ],
    "📝국어": [
        {"question": "장갑산에 놀러간 장갑친구들이 낭떠러지에 떨어졌을 때 모두를 구한 장갑은?", "options": ["비닐장갑", "면장갑", "가죽장갑"], "answer": "비닐장갑"},
        {"question": "그림책, 만화, 뉴스, 광고, 웹툰, 에니메이션, 영화를 (            )라고 합니다.", "options": ["책","매체","생각"], "answer": "매체"},
        {"question": "여러 사람의 이익을 목적으로 하는 광고를 (            )라고 합니다.", "options": ["가게광고", "상품광고", "공익광고"],"answer": "공익광고"},
        {"question": "남자아이가 달을 (가리키다/가르치다)", "options": ["가리키다", "가르치다"], "answer": "가리키다"},
        {"question": "나와 내 짝꿍은 서로 (다른/틀린) 과일을 좋아합니다.", "options": ["다른", "틀린"], "answer": "다른"},
        {"question": "약속시간을 (잊어버려서/잃어버려서) 미안해.", "options": ["잊어버려서", "잃어버려서"], "answer": "잊어버려서"},
        {"question": "1학년 때 입었던 옷이 이제는 (작아요/적어요).", "options": ["작아요", "적어요"], "answer": "작아요"},
        {"question": "느낌이나 마음이 어수선할 때 (            )고 합니다.", "options": ["뒤숭숭하다", "벅차다"], "answer": "뒤숭숭하다"},
        {"question": "다음 중 조언을 하는 방법으로 알맞지 않은 것을 고르세요", "options": ["듣는 사람의 마음에 공감하며 말한다.", "걱정하는 마음을 담아서 말한한다.","명령하듯이 말한다."], "answer": "명령하듯이 말한다."},
        {"question": "종류에 따라서 나누는 것을 (            )라고 합니다.","options": ["부표","분류","더미"],"answer": "분류"}
    ]
}

# 페이지별 함수
def start_page():
    st.subheader("선배가 알려주는 초 2 생활 꿀팁🍯‧₊˚")
    st.title("2학년 공부를 돌아봐")
    st.markdown(
        """
        <div style="font-size:18px; line-height:1.8; text-align:left;">
            2학년 때 배운 내용을 돌아보고 후배들에게 도움을 줄 방법을 생각해 봅시다.<br><br>
            1️⃣오른쪽 메뉴에서 <b>국어</b>, <b>수학</b>, <b>통합교과</b> 문제를 모두 풀고 제출해주세요.<br><br>
            2️⃣모든 문제를 푼 뒤 <b>점수 확인 페이지</b>에서 점수를 확인하세요.
        </div>
        """,
        unsafe_allow_html=True
    )

def quiz_page(subject):
    st.title(f"{subject} 문제를 풀어봅시다.")
    questions = quiz_data[subject]
    score = 0
    user_answers = []

    with st.form(f"{subject}_quiz_form"):
        for idx, question in enumerate(questions):
            # 문제 폰트 크기와 줄간격 조정
            st.markdown(
                f"<h3 style='font-size:20px; line-height:2;'>{idx+1}. {question['question']}</h3>", 
                unsafe_allow_html=True
            )
            # 선택지 폰트 크기와 줄간격 조정
            answer = st.radio(
                "알맞은 답을 선택하세요.",
                question["options"],
                index=None,
                key=f"{subject}_{idx}"
            )
            st.markdown("<style>div.row-widget label { font-size:20px; line-height:1.8; }</style>", unsafe_allow_html=True)
            user_answers.append((answer, question["answer"]))

        submitted = st.form_submit_button("제출")
        if submitted:
            for idx, (user_answer, correct_answer) in enumerate(user_answers):
                if user_answer == correct_answer:
                    st.success(f"문제 {idx+1}: 정답입니다! ✅")
                    score += 1
                else:
                    st.error(f"문제 {idx+1}: 오답입니다. ❌ 정답: {correct_answer}")
            st.subheader(f"총 점수: {score} / {len(questions)}")
            save_results(subject, score)

def score_page():
    st.title("📊 점수 확인")

    # 점수가 없을 때 경고 메시지 표시
    if not st.session_state["results"]:
        st.warning("점수가 없습니다.")
        return  # 점수가 없으면 함수 종료

    # 점수 데이터 생성
    results = st.session_state["results"]
    df = pd.DataFrame(list(results.items()), columns=["과목", "점수"])

    # 점수표 출력
    st.subheader("과목별 점수표")
    table_style = """
    <style>
    .table {
        width: 80%;  /* 표 너비 */
        margin: auto; /* 가운데 정렬 */
        font-size: 20px; /* 글씨 크기 */
        text-align: center; /* 텍스트 가운데 정렬 */
        border-collapse: collapse; /* 테이블 경계 병합 */
    }
    .table th, .table td {
        border: 1px solid black; /* 테이블 경계선 */
        padding: 8px; /* 여백 */
    }
    </style>
    """
    st.markdown(table_style, unsafe_allow_html=True)
    st.markdown(df.to_html(index=False, justify='center', classes='table', border=0), unsafe_allow_html=True)

    # 점수 그래프 출력
    st.subheader("과목별 점수 기호 그래프")
    fig, ax = plt.subplots(figsize=(10, 6))

    subjects = df["과목"]
    scores = df["점수"]

    # 수직 막대 그래프
    ax.bar(subjects, scores, color="white", edgecolor="white", width=0.6)

    # 각 점수 위치에 기호 추가
    for i, score in enumerate(scores):
        for j in range(score):
            ax.text(i, j + 0.5, "○", ha="center", va="center", fontsize=40, color="blue")

    # 그래프 스타일 설정
    ax.set_ylim(0, max(scores) + 1)
    ax.set_yticks(range(0, max(scores) + 2))
    ax.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)
    ax.set_xticks(range(len(subjects)))
    ax.set_xticklabels(subjects, fontsize=14, rotation=0)
    ax.set_xlabel("과목", fontsize=14, color='gray')
    ax.set_ylabel("점수", fontsize=14, color='gray')
    ax.set_title("과목별 점수 기호 그래프", fontsize=16)

    st.pyplot(fig)

    # 점수 초기화 버튼
    if st.button("점수 초기화"):
        reset_results()
        st.success("점수가 초기화되었습니다.")

        
  # 서술식 질문 및 답변 입력
 
    st.markdown(
    """
    <style>
    /* 질문 텍스트 스타일 */
    .question-text {
        font-size: 18px; /* 질문 글씨 크기 */
        font-weight: bold; /* 글씨 굵게 */
        margin-bottom: 10px; /* 입력창과 간격 */
    }

    /* 입력창 텍스트 스타일 */
    textarea {
        font-size: 16px !important; /* 입력창 텍스트 크기 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

    st.subheader("🤓후배들을 위해 한 걸음 더")
    st.markdown('<div class="question-text">1. 어떤 과목이 가장 어려웠나요?</div>', unsafe_allow_html=True)
    question1 = st.text_area("", key="question1")
    st.markdown('<div class="question-text">2. 후배들이 그 과목을 잘 공부하려면 어떤 도움이 필요할까요?</div>', unsafe_allow_html=True)
    question2 = st.text_area("", key="question2")
        # 답변 제출 버튼
    if st.button("답변 제출"):
       st.success("답변이 제출되었습니다.")
       st.write("### 제출된 답변:")
       st.write(f"1. {question1}")
       st.write(f"2. {question2}")




# 사이드바 버튼 구현
menu_items = ["2학년 공부를 돌아봐", "📝국어", "🔢수학", "✨통합교과", "📊점수 확인"]
if "selected_menu" not in st.session_state:
    st.session_state["selected_menu"] = menu_items[0]

st.sidebar.title("초 2 생활 꿀팁🍯")
for item in menu_items:
    button_clicked = st.sidebar.button(item, key=item)
    if button_clicked:
        st.session_state["selected_menu"] = item

# 선택된 메뉴에 따라 페이지 렌더링
selected_menu = st.session_state["selected_menu"]
if selected_menu == "2학년 공부를 돌아봐":
    start_page()
elif selected_menu == "📝국어":
    quiz_page("📝국어")
elif selected_menu == "🔢수학":
    quiz_page("🔢수학")
elif selected_menu == "✨통합교과":
    quiz_page("✨통합교과")
elif selected_menu == "📊점수 확인":
    score_page()

# 스타일 추가
st.markdown(
    """
    <style>
    /* 사이드바 배경색 */
    [data-testid="stSidebar"] {
        background-color: #fffacd; /* 연한 노란색 */
    }

    /* 사이드바 버튼 스타일 */
    div.stButton > button {
        background-color: #FFF173; /* 버튼 배경색 (진한 노란색) */
        color: black; /* 버튼 글씨 색 */
        font-size: 18px; /* 버튼 글씨 크기 */
        height: 50px; /* 버튼 높이 */
        width: 100%; /* 버튼 너비 */
        margin-bottom: 10px; /* 버튼 간 간격 */
        border-radius: 5px; /* 모서리 둥글게 */
    }
    div.stButton > button:hover {
        background-color: #ffc107; /* 마우스 오버 색상 */
    }
    </style>
    """,
    unsafe_allow_html=True
)
