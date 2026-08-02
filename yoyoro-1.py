import os
import io
from PIL import Image
import streamlit as st
import google.generativeai as genai


# ==========================================
# 1. ページ設定とタイトル
# ==========================================

pip install streamlit google-generativeai pillow
st.set_page_config(
    page_title="怪獣画像ジェネレーター (Streamlit + Gemini API)",
    page_icon="🦖",
    layout="centered"
)
streamlit run app.py


st.title("🦖 オリジナル怪獣 画像ジェネレーター")
st.write("Gemini / Imagen APIを使用して、あなただけのオリジナル怪獣を生成・表示します。")

# ==========================================
# 2. サイドバーでAPIキーを設定
# ==========================================
st.sidebar.header("🔑 API設定")
api_key_input = st.sidebar.text_input(
    "Google Gemini APIキーを入力してください",
    type="password",
    help="Google AI Studioで取得したAPIキーを入力します。"
)

# 環境変数または入力されたAPIキーを適用
api_key = api_key_input or os.environ.get("GEMINI_API_KEY", "")

if not api_key:
    st.info("👈 左側のサイドバーに Google Gemini APIキー を入力すると生成が可能になります。")

# ==========================================
# 3. Session State（状態保存用キャッシュ）の初期化
# ==========================================
# 画面を操作しても画像やプロンプトが消えないように session_state に保存します
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

# ==========================================
# 4. 怪獣の設定・プロンプト入力エリア
# ==========================================
st.subheader("⚙️ 怪獣の特徴を指定")

col1, col2 = st.columns(2)
with col1:
    element = st.selectbox(
        "属性・テーマ",
        ["炎・マグマ", "氷・氷河", "雷・プラズマ", "深海・水流", "サイボーグ・鋼鉄", "古代・恐竜"]
    )
with col2:
    style = st.selectbox(
        "画風・スタイル",
        ["特撮ジオラマ風", "映画ポスター風", "リアルな3D CG", "アニメ・イラスト風"]
    )

custom_detail = st.text_area(
    "自由入力（怪獣の見た目や背景のこだわりなど）",
    value="超高層ビルを見下ろす巨大な姿、背中から発光するエネルギーの結晶、迫力ある構図",
    height=80
)

# 生成用プロンプトの構築
full_prompt = (
    f"A powerful giant Kaiju monster, theme of {element}, "
    f"style of {style}, detailed illustration. "
    f"Details: {custom_detail}. High cinematic quality, dramatic lighting."
)

# ==========================================
# 5. 画像生成ボタン処理
# ==========================================
generate_button = st.button("🔥 怪獣画像を生成する", type="primary", use_container_width=True)

if generate_button:
    if not api_key:
        st.error("APIキーが設定されていません。左サイドバーから設定してください。")
    else:
        try:
            with st.spinner("AIがオリジナル怪獣を生成中です... (約5〜15秒ほどかかります)"):
                # APIキーの登録
                genai.configure(api_key=api_key)

                # Google AI Studio / Gemini Imagen 3 モデルの呼び出し
                # ※ 画像生成対応モデルとして imagen-3.0-generate-002 を指定
                model = genai.ImageGenerationModel("imagen-3.0-generate-002")

                result = model.generate_images(
                    prompt=full_prompt,
                    number_of_images=1,
                    aspect_ratio="1:1",
                    person_generation="DONT_ALLOW"
                )

                # 生成された画像をPILイメージとしてセッションに保存
                if result.images:
                    generated_pil_image = result.images[0]._pil_image
                    st.session_state.generated_image = generated_pil_image
                    st.session_state.last_prompt = full_prompt
                    st.success("🎉 怪獣の生成に成功しました！")
                else:
                    st.error("画像の生成に失敗しました。プロンプトを見直してください。")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# ==========================================
# 6. 生成された画像の表示とダウンロード機能
# ==========================================
# session_state に画像が残っている限り、他のボタンを押しても画像は消えません
if st.session_state.generated_image is not None:
    st.divider()
    st.subheader("🖼️ 生成された怪獣")
    
    # 画像を表示
    st.image(
        st.session_state.generated_image,
        caption=f"プロンプト: {st.session_state.last_prompt}",
        use_container_width=True
    )

    # 画像をバイト配列に変換してダウンロードボタンを用意
    buffer = io.BytesIO()
    st.session_state.generated_image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()

    st.download_button(
        label="📥 画像をPNGとしてダウンロード",
        data=img_bytes,
        file_name="my_original_kaiju.png",
        mime="image/png",
        use_container_width=True
    )

# ==========================================
# 7. 画像リセットボタン
# ==========================================
if st.session_state.generated_image is not None:
    if st.button("🗑️ 画像をクリアして最初から作り直す"):
        st.session_state.generated_image = None
        st.session_state.last_prompt = ""
        st.rerun()
