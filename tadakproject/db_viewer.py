import streamlit as st
import pandas as pd
from config.database import DatabaseConfig  # 기존 프로젝트의 DB 설정을 가져옴

# Streamlit 페이지 설정
st.set_page_config(page_title="DB Viewer", page_icon="📋", layout="wide")

st.title("📋 데이터베이스 보기")

conn = DatabaseConfig.get_connection()
cursor = conn.cursor()

try:
    # 데이터베이스에서 테이블 선택
    table_options = ["main_ai_results", "meeting_logs", "coworkers", "checklist", "users"]
    selected_table = st.selectbox("조회할 테이블을 선택하세요", table_options)

    # 선택한 테이블 내용 가져오기
    query = f"SELECT * FROM {selected_table}"
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    # 데이터 출력
    if rows:
        df = pd.DataFrame(rows, columns=column_names)
        st.subheader(f"📋 {selected_table} 테이블 내용")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"{selected_table} 테이블에 데이터가 없습니다.")
except Exception as e:
    st.error(f"데이터 조회 중 오류가 발생했습니다: {e}")
finally:
    conn.close()