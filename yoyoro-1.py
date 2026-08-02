import os
import streamlit as st
import google.generativeai as genai

# ==========================================
# 0. ページ設定とAPIキーの設定
# ==========================================
st.set_page_config(
    page_title="Gemini 怪獣ジェネレーター",
    page_icon="🐉",
    layout="centered"
)

st.title("🐉 Gemini 怪獣ジェネレーター")
st.write("ボタンを押した時だけAPIを呼び出し、結果を `session_state` に保存して再描画時も消えないようにします。")

# ※ 環境変数または Streamlit Secrets から APIキーを取得
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# ==========================================
# 1. session_state（保存用の箱）の初期化
# ==========================================
if "generated_result" not in st.session_state:
    st.session_state.generated_result = None

if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

# ==========================================
# 2. 入力フォームと生成実行ボタン
# ==========================================
prompt = st.text_area(
    "どんな怪獣を作りたいですか？",
    value="炎をまとった巨大なドラゴンのような怪獣、サイバーパンクな都市を背景に。",
    height=100
)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("⚡ 怪獣を生成する", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("プロンプトを入力してください。")
        else:
            with st.spinner("怪獣の設定・ビジュアル説明を生成中..."):
                try:
                    # モデルの初期化と生成呼び出し
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)

                    # 結果を session_state に保存（画面を動かしても消えません）
                    st.session_state.generated_result = response.text
                    st.session_state.prompt_history.append(prompt)

                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

with col2:
    if st.button("🗑️ リセット", use_container_width=True):
        st.session_state.generated_result = None
        st.rerun()

# ==========================================
# 3. 保存された生成結果の表示
# ==========================================
if st.session_state.generated_result is not None:
    st.divider()
    st.subheader("✨ 生成結果")
    st.markdown(st.session_state.generated_result)

    # コピーしやすいようにテキストエリアとしても出力
    with st.expander("テキストとしてコピー"):
        st.code(st.session_state.generated_result, language="markdown")
