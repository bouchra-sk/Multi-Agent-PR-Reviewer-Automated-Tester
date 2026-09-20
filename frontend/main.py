import streamlit as st
from streamlit_option_menu import option_menu
import time

# ─────────────────────────────────────────────────────────────
# 1. PAGE CONFIGURATION & STYLING
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Code Review Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Glassmorphism, Theme Colors (#4A90E2, #50E3C2, #0F172A), and Clean UI
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header and Title Styling */
    h1, h2, h3 {
        color: #F8FAFC !important;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #4A90E2 0%, #50E3C2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Cards & Glassmorphism */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    
    /* Buttons Styling */
    .stButton>button {
        background: linear-gradient(135deg, #4A90E2 0%, #3B82F6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #50E3C2 0%, #10B981 100%);
        color: #0F172A;
        box-shadow: 0 6px 20px rgba(80, 227, 194, 0.4);
    }

    /* Google Login Custom Button */
    .google-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 12px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        text-align: center;
        text-decoration: none;
        margin-top: 10px;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 2. SESSION STATE & NAVIGATION
# ─────────────────────────────────────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest User"

# Top Navbar
col_logo, col_nav, col_auth = st.columns([2, 5, 2])

with col_logo:
    st.markdown('<h3 style="margin:0;"><span class="gradient-text">⚡ Code Review Assistant</span></h3>', unsafe_allow_html=True)

with col_nav:
    selected_page = option_menu(
        menu_title=None,
        options=["Home", "Upload", "Review Report", "Dashboard", "Settings"],
        icons=["house", "cloud-upload", "file-code", "grid", "gear"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#50E3C2", "font-size": "14px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "center",
                "margin": "0px 4px",
                "color": "#94A3B8",
                "border-radius": "8px",
            },
            "nav-link-selected": {"background-color": "#1E293B", "color": "#50E3C2", "border": "1px solid #4A90E2"},
        }
    )

with col_auth:
    if not st.session_state.logged_in:
        if st.button("🔑 Sign in with Google", key="login_trigger"):
            st.session_state.show_modal = True
    else:
        st.success(f"👤 {st.session_state.user_name}")

# Google Sign-in Modal (Dialog)
if getattr(st.session_state, 'show_modal', False) and not st.session_state.logged_in:
    @st.dialog("Sign in to Code Review Assistant")
    def login_modal():
        st.write("Save your past reviews, manage custom LLM keys, and access automated testing.")
        st.markdown("""
        <div style="text-align: center; margin-bottom: 15px;">
            <svg width="48" height="48" viewBox="0 0 24 24">
                <path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z"/>
                <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/>
                <path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.3s.2-1.6.4-2.3L1.9 7.3C.7 9.7 0 10.8 0 12s.7 2.3 1.9 4.7l3.7-2.9z"/>
                <path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.3-6.4-5.2L1.9 16C3.7 19.7 7.5 23 12 23z"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Continue with Google", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.user_name = "Bouchra Dev"
            st.session_state.show_modal = False
            st.rerun()
            
    login_modal()

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# 3. PAGE CONTENT ROUTING
# ─────────────────────────────────────────────────────────────

# --- PAGE 1: LANDING PAGE ---
if selected_page == "Home":
    col_hero, col_mockup = st.columns([1, 1], gap="large")
    
    with col_hero:
        st.markdown("""
        <div style="padding-top: 40px;">
            <h1 style="font-size: 3.2rem; line-height: 1.2;">
                AI Code Review <br><span class="gradient-text">Assistant</span>
            </h1>
            <p style="font-size: 1.2rem; color: #94A3B8; margin-top: 20px;">
                Upload. Analyze. Improve your code instantly with multi-agent intelligence and automated testing suggestions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("🚀 Get Started", use_container_width=True):
                st.session_state['selected_page'] = "Upload"
                st.rerun()
        with c2:
            st.link_button("📖 Documentation", "https://github.com", use_container_width=True)

    with col_mockup:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #50E3C2; margin-bottom: 10px;">⚡ Live Review Mockup</h4>
            <pre style="background-color: #090D16; padding: 15px; border-radius: 8px; color: #E2E8F0;">
<span style="color: #F43F5E;">- def login(user):</span>
<span style="color: #10B981;">+ async def login(user: UserLogin):</span>
    <span style="color: #50E3C2;"># 🤖 Agent Suggestion: Added Type Validation</span>
    token = await create_token(user.id)
    return token
            </pre>
            <p style="color: #94A3B8; font-size: 0.85rem;">✨ 3 Suggestions Generated in 1.2s</p>
        </div>
        """, unsafe_allow_html=True)

# --- PAGE 2: UPLOAD PAGE ---
elif selected_page == "Upload":
    st.subheader("📤 Upload Source Code for AI Review")
    
    col_upload, col_history = st.columns([2, 1], gap="medium")
    
    with col_upload:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Drag & drop code files (.py, .js, .java, .cpp, .ts)",
            accept_multiple_files=True,
            type=["py", "js", "java", "cpp", "ts"]
        )
        
        if uploaded_files:
            st.success(f"Selected {len(uploaded_files)} file(s).")
            for f in uploaded_files:
                st.text(f"📄 {f.name} ({f.size} bytes)")
            
            if st.button("⚡ Analyze Code Now", use_container_width=True):
                progress = st.progress(0)
                for percent in range(100):
                    time.sleep(0.01)
                    progress.progress(percent + 1)
                st.success("Analysis Complete! Go to 'Review Report' to view results.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_history:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🕒 Upload History")
        st.caption("Recent uploads from your workspace")
        st.text("• auth_service.py (2 mins ago)")
        st.text("• pytest_runner.py (1 hour ago)")
        st.text("• database_models.py (Yesterday)")
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 3: REVIEW REPORT PAGE ---
elif selected_page == "Review Report":
    st.subheader("📋 AI Code Review Report")
    
    col_code, col_report = st.columns([1, 1], gap="medium")
    
    with col_code:
        st.markdown("### 📄 Code Preview (`app/core/auth.py`)")
        st.code("""
def verify_jwt_token(token: str):
    # Potential Bug: Missing try-except block around decode
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
        """, language="python")

    with col_report:
        st.markdown("### 🤖 AI Suggestions & Insights")
        
        with st.expander("🐛 Potential Bugs (1 Warning)", expanded=True):
            st.error("Unhandled JWT Expired Exception in line 3. Token decoding might crash the server if invalid.")
            st.code("try:\n    payload = jwt.decode(...)\nexcept jwt.ExpiredSignatureError:\n    raise HTTPException(status_code=401)", language="python")
            
        with st.expander("🧩 Modularity & Structure", expanded=False):
            st.info("Extract `SECRET_KEY` loading into a central `config.py` setting module.")
            
        with st.expander("✨ Readability & Type Hints", expanded=False):
            st.success("Function signature uses explicit type annotations. Good job!")

        st.download_button("📥 Download PDF Report", data="Report Details...", file_name="code_review_report.txt")

# --- PAGE 4: DASHBOARD PAGE ---
elif selected_page == "Dashboard":
    st.subheader("📊 Past Reviews & Activity")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        search = st.text_input("🔍 Search reviews by file or language...", "")
    with c2:
        filter_lang = st.selectbox("Filter by Language", ["All", "Python", "JavaScript", "Java"])
    
    # Sample Data Table
    reviews_data = [
        {"File Name": "auth_controller.py", "Language": "Python", "Date": "2026-09-20", "Score": "85/100"},
        {"File Name": "api_routes.js", "Language": "JavaScript", "Date": "2026-09-19", "Score": "92/100"},
        {"File Name": "PaymentGateway.java", "Language": "Java", "Date": "2026-09-15", "Score": "78/100"},
    ]
    
    for item in reviews_data:
        col_f, col_l, col_d, col_s, col_act = st.columns([2, 1, 1, 1, 2])
        col_f.write(f"📄 **{item['File Name']}**")
        col_l.write(item['Language'])
        col_d.write(item['Date'])
        col_s.write(f"🟢 {item['Score']}")
        if col_act.button("View Report", key=item['File Name']):
            st.info(f"Opening report for {item['File Name']}")
        st.markdown("<hr style='margin: 5px 0; border-color: #334155;'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 5: SETTINGS PAGE ---
elif selected_page == "Settings":
    st.subheader("⚙️ Account & Application Settings")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🔑 API Key Management")
    api_key = st.text_input("IBM Bob 2.0 / OpenAI API Key", value="sk-xxxxxxxxxxxxxxxxxxxxxxxx", type="password")
    if st.button("Save Keys"):
        st.success("API Key saved successfully!")
    
    st.markdown("---")
    st.markdown("### 👤 Profile Info")
    st.text(f"Logged in as: {st.session_state.user_name}")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = "Guest User"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)