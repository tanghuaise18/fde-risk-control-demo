import streamlit as st
import pandas as pd

# 1. 页面配置
st.set_page_config(page_title="SaaS卡台 AI 风控诊断平台", layout="wide", page_icon="🛡️")

st.title("🛡️ SaaS 卡台 AI 智能风控与拦截诊断 Demo")
st.caption("基于 Streamlit + Dify RAG 工作流的自动化风控排查系统")

# 2. 侧边栏
st.sidebar.header("⚙️ 系统状态")
st.sidebar.success("✅ FastAPI 路由就绪")
st.sidebar.success("✅ Dify RAG 引擎在线")

customer_tier = st.sidebar.selectbox("客户分级", ["Tier 1 (白名单大客户)", "Tier 2 (标准客户/观察期)"])

# 3. 核心功能
tab1, tab2 = st.tabs(["🔍 单条异常实时诊断", "📊 批量日志解析与报表"])

with tab1:
    st.subheader("单笔扣款失败诊断")
    col1, col2 = st.columns(2)
    
    with col1:
        account_id = st.text_input("广告账户 ID", value="act_8899321")
        error_code = st.selectbox("Meta 扣款错误代码", [100, 200, 300, "TX1004 (网关超时)"])
        error_msg = st.text_area("原始错误日志/报文", value="Unknown gateway timeout / Risk control flag")
        submit_btn = st.button("🚀 提交 AI 诊断", type="primary")

    with col2:
        st.subheader("💡 AI 诊断与处置建议")
        if submit_btn:
            with st.spinner("AI 智能引擎诊断中..."):
                if error_code == 100:
                    st.error("诊断结论：卡片余额不足")
                    st.info("处置建议：请检查扣款卡片额度或更换绑卡。")
                elif "TX1004" in str(error_code):
                    st.warning("诊断结论：【Dify RAG 智能归因】网关超时与风控紧逼碰撞")
                    st.markdown("""
                    **建议处置策略：**
                    1. 触发 Tier 1 动态溢价策略，将卡片额度提升至 Meta 阈值 +$5（如 $10）。
                    2. 自动化解封通道，阻断下游 Meta 审核机制。
                    """)
                else:
                    st.success("诊断结论：正常交易，建议保持当前动态限额。")

with tab2:
    st.subheader("批量 Meta 扣款 CSV 日志解析")
    uploaded_file = st.file_uploader("上传 Meta 扣款日志 CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())