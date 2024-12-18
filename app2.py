import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 글꼴 설정
font_path = "NanumGothic.ttf"
font_manager.fontManager.addfont(font_path)
rc('font', family='NanumGothic')

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
    ],
    "🔢수학": [
        {"question": "사탕을 보미는 4개의 3배, 희주는 3개의 5배만큼 가지고 있습니다. 두 사람이 가지고 있는 사탕은 모두 몇 개인가요?", "options": ["27개", "30개", "33개"], "answer": "27개"},
        {"question": "아버지의 나이는 38세이고 나의 나이는 9살입니다. 나는 아버지보다 몇 살 더 적을까요?", "options": ["29살", "27살", "30살"], "answer": "29살"},
    ],
    "📝국어": [
        {"question": "장갑산에 놀러간 장갑친구들이 낭떠러지에 떨어졌을 때 모두를 구한 장갑은?", "options": ["비닐장갑", "면장갑", "가죽장갑"], "answer": "비닐장갑"},
        {"question": "그림책, 만화, 뉴스, 광고, 웹툰, 에니메이션, 영화를 (       )라고 합니다.", "options": ["책", "매체", "생각"], "answer": "매체"},
    ]
}

# 페이지별 함수
def start_page():
    st.subheader("선배가 알려주는 초 2 생활 꿀팁🍯‧₊˚")
    st.title("3️⃣2학년 공부를 돌아봐")
    st.markdown(
        """
        2학년 때 배운 내용을 돌아보고 후배들에게 도움을 줄 방법을 생각해 봅시다.  
        - 오른쪽 메뉴에서 각 교과 문제를 모두 풀고 제출하세요.  
        - 점수 확인 페이지에서 결과를 확인하세요.
        """,
        unsafe_allow_html=True
    )

def quiz_page(subject):
    st.title(f"{subject} 퀴즈")
    questions = quiz_data[subject]
    score = 0
    user_answers = []

    with st.form(f"{subject}_quiz_form"):
        for idx, question in enumerate(questions):
            # 문제 폰트 크기와 줄간격 조정
            st.markdown(
                f"<h3 style='font-size:24px; line-height:2;'>{idx+1}. {question['question']}</h3>", 
                unsafe_allow_html=True
            )
            # 선택지 폰트 크기와 줄간격 조정
            answer = st.radio(
                "정답을 선택하세요.",
                question["options"],
                key=f"{subject}_{idx}"
            )
            st.markdown("<style>div.row-widget label { font-size:18px; line-height:1.8; }</style>", unsafe_allow_html=True)
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
    if not st.session_state["results"]:
        st.warning("점수가 없습니다.")
    else:
        df = pd.DataFrame(list(st.session_state["results"].items()), columns=["과목", "점수"])
        st.table(df)
    if st.button("점수 초기화"):
        reset_results()
        st.success("점수가 초기화되었습니다.")

# 사이드바 버튼 구현
menu_items = ["2학년 공부를 돌아봐", "📝국어", "🔢수학", "✨통합교과", "📊점수 확인"]
if "selected_menu" not in st.session_state:
    st.session_state["selected_menu"] = menu_items[0]

st.sidebar.title("메뉴")
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
        background-color: #ffd700; /* 버튼 배경색 (진한 노란색) */
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
