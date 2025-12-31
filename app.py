from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

# LLMからの回答を取得する関数を定義
def get_llm_response(input_text, specialist_type):
    """
    入力テキストとラジオボタンの選択値を受け取り、LLMからの回答を返す関数
    """
    # LangChainのChatOpenAIインスタンスを作成
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

    # 選択された専門家に応じてシステムメッセージを切り替える
    if specialist_type == "料理研究家":
        system_template = "あなたはプロの料理研究家です。美味しいレシピや調理のコツ、食材の知識について、親切かつ具体的にアドバイスしてください。"
    else:
        system_template = "あなたは経験豊富なITエンジニアです。プログラミングやシステム設計、最新技術に関する質問に対して、専門的な知見から論理的に回答してください。"

    # メッセージリストを作成
    messages = [
        SystemMessage(content=system_template),
        HumanMessage(content=input_text)
    ]

    # LLMにプロンプトを渡し、回答を得る
    response = llm(messages)
    return response.content

# --- Streamlit UIの構築---

# アプリのタイトル
st.title("専門家相談AIチャット")

# アプリの概要と操作方法の明示
st.write("### アプリの概要")
st.write("このアプリは、LangChainを活用して選択した専門家からアドバイスをもらえるWebアプリケーションです。")

st.write("### 操作方法")
st.write("1. 相談したい**専門家の種類**をラジオボタンから選択してください。")
st.write("2. 下の入力フォームに**相談内容や質問**を記入してください。")
st.write("3. 「送信」ボタンを押すと、専門家AIからの回答が表示されます。")

st.divider()

# 専門家を選択するラジオボタン
selected_specialist = st.radio(
    "相談する専門家を選んでください：",
    ["料理研究家", "ITエンジニア"]
)

# 質問を入力するフォーム
user_input = st.text_input(label="相談内容を入力してください：")

# 送信ボタンが押された時の処理
if st.button("送信"):
    if user_input:
        # ローディング表示をしながら回答を取得
        with st.spinner("専門家が考えています..."):
            answer = get_llm_response(user_input, selected_specialist)

        st.write("### 専門家からの回答")
        st.write(answer)
    else:
        st.error("相談内容を入力してから送信してください。")