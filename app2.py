import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams, font_manager
import os

# 한글 폰트 설정 (배포환경 포함)
def set_korean_font():
    font_path = "./NanumGothic.ttf"  # 프로젝트 폴더에 저장된 나눔고딕 폰트 파일
    if os.path.exists(font_path):
        font_prop = font_manager.FontProperties(fname=font_path)
        rcParams['font.family'] = font_prop.get_name()

# 점수 관리: 세션 상태를 활용해 안정적으로 점수를 저장/로드
if "results" not in st.session_state:
    st.session_state["results"] = {}

# 점수 저장 함수
def save_results(subject, score):
    st.session_state["results"][subject] = score

# 점수 초기화 함수
def reset_results():
    st.session_state["results"] = {}
    
# 과목별 퀴즈
quiz_data = {
    "통합교과": [
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
    "수학": [
        {"question": "사탕을 보미는 4개의 3배, 희주는 3개의 5배만큼 가지고 있습니다. 두 사람이 가지고 있는 사탕은 모두 몇 개인가요?", "options": ["27개", "30개", "33개"], "answer": "27개"},
        {"question": "아버지의 나이는 38세이고 나의 나이는 9살입니다. 나는 아버지보다 몇 살 더 적을까요?", "options": ["29살", "27살", "30살"], "answer": "29살"},
        {"question": "100이 7개, 10이 5개, 1이 8개인 수는 무엇인가요?", "options": ["758", "785", "857"], "answer": "758"},
        {"question": "덧셈식을 계산하세요. 78+17=", "options": ["95", "85", "97"], "answer": "95"},
        {"question": "변과 꼭짓점이 4개인 도형은 무엇입니까?", "options": ["사각형", "삼각형", "원"], "answer": "사각형"},
        {"question": "1m는 몇 cm입니까?", "options": ["100cm", "10cm", "1000cm"], "answer": "100cm"},
        {"question": "6572부터 100씩 5번 뛰어 센 수는 얼마일까요?", "options": ["7072", "7272", "7172"], "answer": "7072"},
        {"question": "곱셈식을 계산하세요. 8x0=?", "options": ["0", "8", "1"], "answer": "0"},
        {"question": "2일은 몇 시간인가요?","options":["24시간","48시간","50시간"],"answer":"48시간간"},
        {"question": "곱셈식을 계산하세요.6x7=", "options":["35","28","42"],"answer":"42"}
    ],
        "국어": [
        {"question": "장갑산에 놀러간 장갑친구들이 낭떠러지에 떨어졌을 때 모두를 구한 장갑은?", "options": ["비닐장갑", "면장갑", "가죽장갑"], "answer": "비닐장갑"},
        {"question": "그림책, 만화, 뉴스, 광고, 웹툰, 에니메이션, 영화를 (       )라고 합니다.", "options": ["책","매체","생각"], "answer": "매체"},
        {"question": "여러 사람의 이익을 목적으로 하는 광고를 (    )라고 합니다.", "options": ["가게광고", "상품광고", "공익광고"],"answer": "공익광고"},
        {"question": "남자아이가 달을 (가리키다/가르치다)", "options": ["가리키다", "가르치다"], "answer": "가리키다"},
        {"question": "나와 내 짝꿍은 서로 (다른/틀린) 과일을 좋아합니다.", "options": ["다른", "틀린"], "answer": "다른"},
        {"question": "약속시간을 (잊어버려서/잃어버려서) 미안해.", "options": ["잊어버려서", "잃어버려서"], "answer": "잊어버려서"},
        {"question": "1학년 때 입었던 옷이 이제는 (작아요/적어요).", "options": ["작아요", "적어요"], "answer": "작아요"},
        {"question": "느낌이나 마음이 어수선할 때 (   )고 합니다.", "options": ["뒤숭숭하다", "벅차다"], "answer": "뒤숭숭하다"}
    ]
}

# 과목별 퀴즈 페이지
def quiz_page(subject):
    st.title(f"{subject} 퀴즈")
    questions = quiz_data[subject]
    score = 0
    user_answers = []

    with st.form(f"{subject}_quiz_form"):
        for idx, question in enumerate(questions):
            st.write(f"**문제 {idx+1}: {question['question']}**")
            answer = st.radio("알맞은 답을 고르세요.", question["options"], index=None, key=f"{subject}_{idx}")
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

            # 점수 저장
            save_results(subject, score)
            st.success("점수가 저장되었습니다!")

# 점수 확인 페이지
# 점수 확인 페이지
def score_page():
    st.title("저장된 점수 확인")
    
    # 점수 초기화 확인
    if "reset" not in st.session_state:
        st.session_state["reset"] = False

    # 점수 초기화 버튼
    if st.button("점수 초기화"):
        reset_results()
        st.session_state["reset"] = True  # 초기화 신호 설정
        st.success("점수가 초기화되었습니다.")

    # 초기화된 상태 처리
    if st.session_state["reset"]:
        st.info("점수가 초기화되었습니다. 새 점수를 추가해주세요.")
        return  # 초기화 후 페이지 중단

    # 저장된 점수 표시
    if not st.session_state["results"]:
        st.warning("저장된 점수가 없습니다.")
    else:
        results = st.session_state["results"]
        df = pd.DataFrame(list(results.items()), columns=["과목", "점수"])

        # 점수표 출력 (HTML 스타일 그대로 유지)
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
        st.write(df.to_html(index=False, justify='center', classes='table', border=0), unsafe_allow_html=True)

        # 점수 그래프 출력 (기존 그래프 스타일 유지)
        st.subheader("과목별 점수 기호 그래프")
        fig, ax = plt.subplots(figsize=(10, 6))

        subjects = df["과목"]
        scores = df["점수"]

        # 수직 막대 그래프 (색상, 스타일 유지)
        bar_width = 0.6
        ax.bar(subjects, scores, color="white", edgecolor="white", width=bar_width)

        # 세로선 추가 (과목 간 경계선)
        for i in range(len(subjects) + 1):
            ax.axvline(x=i - 0.5, color="gray", linestyle="--", linewidth=0.5)

        # 각 칸에 점수 기호 ○ 표시
        for i, score in enumerate(scores):
            for j in range(score):
                ax.text(i, j + 0.5, "○", ha="center", va="center", fontsize=50, color="blue")

        # Y축 눈금 설정 및 격자선 추가
        max_score = max(scores)
        ax.set_ylim(0, max_score + 1)
        ax.set_yticks(range(0, max_score + 2))
        ax.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)

        # 그래프 라벨 및 제목 스타일
        ax.set_xticklabels(subjects, fontsize=14, rotation=0)
        ax.tick_params(axis="x", labelsize=14)
        ax.set_xlabel("과목", color='gray', fontsize=14)
        ax.set_ylabel("점수", color='gray', fontsize=14)
        ax.set_title("과목별 점수 기호 그래프", fontsize=16)

        st.pyplot(fig)
        
            # 서술식 질문 및 답변 입력
        st.subheader("질문 및 답변")
        question1 = st.text_area("1. 어떤 과목의 문제가 가장 어려웠나요?")
        question2 = st.text_area("2. 후배들이 그 과목을 잘 공부하려면 어떤 도움이 필요할까요?")

        # 답변 제출 버튼
        if st.button("답변 제출"):
            st.success("답변이 제출되었습니다.")
            st.write("### 제출된 답변:")
            st.write(f"1. {question1}")
            st.write(f"2. {question2}")

# 페이지 라우팅
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["국어", "수학", "통합교과", "점수 확인"])

if page == "국어":
    quiz_page("국어")
elif page == "수학":
    quiz_page("수학")
elif page == "통합교과":
    quiz_page("통합교과")
elif page == "점수 확인":
    score_page()
    
    
