import streamlit as st
import streamlit.components.v1 as components
import requests
from supabase import create_client
import os
import time
import extra_streamlit_components as stx
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.set_page_config(
    page_title="Job Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Cormorant+Garamond:wght@700&display=swap');

    :root {
        --bg: #0f0f13;
        --card: #1a1a24;
        --accent: #7c6aff;
        --accent2: #ff6a9e;
        --accent3: #6affce;
        --text: #ffffff;
        --muted: #a0a0b8;
        --border: #2a2a38;
    }

    html, body, [class*="css"], p, span, div, label, input, textarea, button {
        font-family: 'Outfit', sans-serif !important;
        color: var(--text);
    }

    .stApp { background: var(--bg); direction: rtl; }

    .hero {
        text-align: center;
        padding: 2rem 2rem 1.5rem 2rem;
        background: var(--card);
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }
    .hero-sub { color: var(--muted); font-size: 1rem; margin: 0; }

    .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: linear-gradient(180deg, var(--accent), var(--accent2));
    }
    .card-title {
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 0.9rem;
        font-weight: 600;
    }

    .auth-wrap { max-width: 420px; margin: 4rem auto; }
    .auth-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2.5rem;
    }
    .auth-sub {
        text-align: center;
        color: var(--muted);
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }

    .score-num {
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--accent3), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    .progress-wrap {
        background: var(--border);
        border-radius: 100px;
        height: 6px;
        margin-top: 0.7rem;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: 100px;
        background: linear-gradient(90deg, var(--accent), var(--accent3));
    }

    .tag {
        display: inline-block;
        border-radius: 20px;
        padding: 0.25rem 0.8rem;
        font-size: 0.82rem;
        margin: 0.2rem;
        font-weight: 500;
    }
    .tag-missing { background: rgba(255,106,158,0.15); border: 1px solid rgba(255,106,158,0.4); color: #ffaac8 !important; }
    .tag-have    { background: rgba(106,255,206,0.15); border: 1px solid rgba(106,255,206,0.4); color: #6affce !important; }
    .tag-skill   { background: rgba(124,106,255,0.15); border: 1px solid rgba(124,106,255,0.4); color: #b0a4ff !important; }

    .app-company { color: #ffffff !important; font-weight: 700; font-size: 1rem; }
    .app-score   { color: #6affce !important; font-weight: 600; font-size: 0.9rem; }
    .status-badge { display: inline-block; padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.78rem; font-weight: 600; }
    .s-applied   { background:rgba(106,255,206,0.15); color:#6affce !important; border:1px solid rgba(106,255,206,0.4); }
    .s-pending   { background:rgba(255,200,50,0.15);  color:#ffc832 !important; border:1px solid rgba(255,200,50,0.4); }
    .s-rejected  { background:rgba(255,80,80,0.15);   color:#ff7070 !important; border:1px solid rgba(255,80,80,0.4); }
    .s-interview { background:rgba(124,106,255,0.15); color:#b0a4ff !important; border:1px solid rgba(124,106,255,0.4); }
    .s-accepted { background:rgba(106,255,206,0.25); color:#00ff9d !important; border:1px solid rgba(106,255,206,0.6); }
    .stSelectbox [data-baseweb="select"] {
        background: #12121a !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
    .stSelectbox [data-baseweb="select"] * {
        background: #12121a !important;
        color: #ffffff !important;
    }
    [data-baseweb="popover"], [data-baseweb="popover"] * {
        background: #12121a !important;
        color: #ffffff !important;
    }
    [data-baseweb="menu"] {
        background: #12121a !important;
    }
    [data-baseweb="menu"] li {
        background: #12121a !important;
        color: #ffffff !important;
    }
    [data-baseweb="menu"] li:hover {
        background: #2a2a38 !important;
    }

    .stTextArea textarea, .stTextInput input {
        background: #12121a !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.92rem !important;
        text-align: right;
        direction: rtl;
    }
    .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    label { color: var(--muted) !important; font-size: 0.84rem !important; font-weight: 500 !important; }
    p, li, span { color: #ffffff !important; }

    .stTabs [data-baseweb="tab-list"] { background: var(--card); border-radius: 8px; padding: 4px; gap: 4px; }
    .stTabs [data-baseweb="tab"] { color: var(--muted) !important; border-radius: 6px; }
    .stTabs [aria-selected="true"] { background: var(--accent) !important; color: white !important; }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 1rem; }

    section[data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 2rem 1rem 2rem !important; max-width: 100% !important; }
    [data-testid="stFileUploader"] {
        background: #12121a !important;
        border: 1px dashed var(--border) !important;
        border-radius: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(
    """
    <script>
    if (!sessionStorage.getItem('tab_alive')) {
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    }
    sessionStorage.setItem('tab_alive', 'true');
    </script>
    """,
    height=0,
)

API_URL = "https://job-analyzer-oi1o.onrender.com"
TIMEOUT_SECONDS = 30 * 60
cookie_manager = stx.CookieManager()


def get_auth_header():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}


def logout():
    for key in [
        "token",
        "user_email",
        "login_time",
        "skills",
        "last_result",
        "cv_hash",
    ]:
        st.session_state.pop(key, None)
    cookie_manager.delete("token")


def update_activity():
    st.session_state["login_time"] = time.time()


def check_timeout():
    if "login_time" in st.session_state:
        if time.time() - st.session_state["login_time"] > TIMEOUT_SECONDS:
            logout()
            st.warning("⏰ פג תוקף החיבור — התחבר מחדש")
            st.rerun()


def add_skill_callback():
    val = st.session_state.get("skill_to_add", "").strip()
    if val and val not in st.session_state.get("skills", []):
        st.session_state["skills"] = st.session_state.get("skills", []) + [val]
        st.session_state.pop("last_result", None)


if "token" not in st.session_state:
    token_from_cookie = cookie_manager.get("token")
    if token_from_cookie:
        st.session_state["token"] = token_from_cookie
        st.session_state["login_time"] = time.time()
        st.rerun()

if "token" not in st.session_state:
    st.markdown(
        """
        <div class="auth-wrap">
            <div class="auth-card">
                <p style="font-family:'Cormorant Garamond',serif;font-size:3rem;font-weight:700;background:linear-gradient(135deg,#7c6aff,#ff6a9e);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;margin:0 0 0.3rem 0">Job Analyzer</p>
                <p class="auth-sub">התחבר כדי להתחיל לנתח משרות</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_tab1, auth_tab2 = st.tabs(["🔐  התחברות", "📝  הרשמה"])

        with auth_tab1:
            email = st.text_input("מייל", key="login_email")
            password = st.text_input("סיסמה", type="password", key="login_pass")
            if st.button("התחבר", use_container_width=True, key="login_btn"):
                try:
                    res = supabase.auth.sign_in_with_password(
                        {"email": email, "password": password}
                    )
                    st.session_state["token"] = res.session.access_token
                    st.session_state["user_email"] = email
                    st.session_state["login_time"] = time.time()
                    cookie_manager.set("token", res.session.access_token)
                    st.rerun()
                except Exception:
                    st.error("מייל או סיסמה שגויים")

        with auth_tab2:
            email_r = st.text_input("מייל", key="reg_email")
            password_r = st.text_input("סיסמה", type="password", key="reg_pass")
            if st.button("הירשם", use_container_width=True, key="reg_btn"):
                try:
                    supabase.auth.sign_up({"email": email_r, "password": password_r})
                    st.success("✅ נרשמת! כעת התחבר עם הפרטים שלך")
                except Exception as e:
                    st.error(f"שגיאה: {e}")
    st.stop()

check_timeout()

st.markdown(
    """
    <div class="hero">
        <p style="font-family:'Cormorant Garamond',serif;font-size:4rem;font-weight:700;background:linear-gradient(135deg,#7c6aff,#ff6a9e,#6affce);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;margin:0 0 0.4rem 0">Job Analyzer</p>
        <p class="hero-sub">העלה קורות חיים, הדבק תיאור משרה — וגלה כמה אתה מתאים</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_logout = st.columns([6, 1])[1]
with col_logout:
    if st.button("🚪 יציאה"):
        logout()
        st.rerun()

tab1, tab2 = st.tabs(["✨  נתח משרה", "📋  המשרות שלי"])

with tab1:
    col_right, col_left = st.columns([1, 1], gap="large")

    with col_right:
        st.markdown(
            '<div class="card"><p class="card-title">📄 פרטי המשרה</p>',
            unsafe_allow_html=True,
        )
        description = st.text_area(
            "תיאור המשרה", height=150, placeholder="הדבק כאן את תיאור המשרה..."
        )
        company_name = st.text_input("שם החברה", placeholder="Google")
        cv_file = st.file_uploader("קורות חיים (PDF)", type=["pdf"])

        if cv_file:
            file_hash = hash(cv_file.getvalue())
            if st.session_state.get("cv_hash") != file_hash:
                with st.spinner("מחלץ כישורים..."):
                    try:
                        res = requests.post(
                            f"{API_URL}/extract-skills",
                            files={
                                "file": (
                                    cv_file.name,
                                    cv_file.getvalue(),
                                    "application/pdf",
                                )
                            },
                            timeout=30,
                        )
                        extracted = res.json().get("skills", [])
                        existing_manual = [
                            s
                            for s in st.session_state.get("skills", [])
                            if s not in extracted
                        ]
                        st.session_state["skills"] = extracted + existing_manual
                        st.session_state["cv_hash"] = file_hash
                        update_activity()
                        st.success(
                            f"✅ זוהו {len(st.session_state['skills'])} כישורים!"
                        )
                    except Exception as e:
                        st.error(f"שגיאה: {e}")

        if "skills" in st.session_state and st.session_state["skills"]:
            skills_html = "".join(
                f'<span class="tag tag-skill">{s}</span>'
                for s in st.session_state["skills"]
            )
            st.markdown(
                f'<div style="margin-top:0.6rem"><p class="card-title">כישורים שזוהו ({len(st.session_state["skills"])})</p>{skills_html}</div>',
                unsafe_allow_html=True,
            )

            st.text_input(
                "הוסף כישור", placeholder="לדוגמה: Python", key="skill_to_add"
            )
            st.button("➕ הוסף כישור", key="add_skill_btn", on_click=add_skill_callback)

        analyze_btn = st.button("🔍  נתח עכשיו", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_left:
        if analyze_btn and description:
            update_activity()
            user_skills = st.session_state.get("skills", [])
            if not user_skills:
                st.warning("⚠️ העלה קורות חיים קודם!")
            else:
                with st.spinner("מנתח..."):
                    try:
                        res = requests.post(
                            f"{API_URL}/analyze",
                            json={
                                "description": description,
                                "user_skills": user_skills,
                            },
                            timeout=30,
                        )
                        r = res.json()
                        st.session_state["last_result"] = {
                            "score": r.get("match_score", 0),
                            "missing": r.get("missing_skills", []),
                            "ttl": r.get("time_to_learn", {}),
                            "company": company_name,
                            "user_skills": user_skills,
                        }
                    except Exception as e:
                        st.error(f"שגיאה: {e}")

        if "last_result" in st.session_state:
            result = st.session_state["last_result"]
            score = result["score"]
            missing = result["missing"]
            ttl = result["ttl"]
            user_skills = result["user_skills"]

            st.markdown(
                f"""<div class="card">
                <p class="card-title">🎯 ציון התאמה</p>
                <span class="score-num">{score}%</span>
                <div class="progress-wrap">
                    <div class="progress-fill" style="width:{score}%"></div>
                </div>
                </div>""",
                unsafe_allow_html=True,
            )

            have = [s for s in user_skills if s not in missing]
            have_html = "".join(
                f'<span class="tag tag-have">✓ {s}</span>' for s in have
            )
            miss_html = "".join(
                f'<span class="tag tag-missing">✗ {s}</span>' for s in missing
            )
            st.markdown(
                f"""<div class="card">
                <p class="card-title">⚡ כישורים</p>
                {have_html}{miss_html}
                </div>""",
                unsafe_allow_html=True,
            )

            if ttl:
                rows = "".join(
                    f"<tr><td style='padding:0.4rem 0.6rem;color:#ffffff;font-size:0.9rem'>{k}</td>"
                    f"<td style='padding:0.4rem 0.6rem;color:#6affce;font-size:0.85rem;font-weight:600'>{v}</td></tr>"
                    for k, v in ttl.items()
                )
                st.markdown(
                    f"""<div class="card">
                    <p class="card-title">📚 זמן לימוד</p>
                    <table style="width:100%;border-collapse:collapse">{rows}</table>
                    </div>""",
                    unsafe_allow_html=True,
                )

            if st.button("💾  שמור במעקב", use_container_width=True):
                save = requests.post(
                    f"{API_URL}/applications",
                    json={
                        "company": result["company"] or "לא צוין",
                        "status": "applied",
                        "match_score": score,
                    },
                    headers=get_auth_header(),
                )
                if save.status_code == 200:
                    st.success("✅ נשמר!")
                    update_activity()
                    del st.session_state["last_result"]
                    st.rerun()
                else:
                    st.error(f"שגיאה: {save.status_code}")
        else:
            if not analyze_btn:
                st.markdown(
                    """<div class="card" style="text-align:center;padding:3.5rem 1rem">
                    <div style="font-size:2.8rem;margin-bottom:1rem">🎯</div>
                    <div style="color:#a0a0b8;font-size:0.95rem;line-height:1.6">
                    העלה קורות חיים<br>והדבק תיאור משרה<br>כדי לראות ניתוח התאמה
                    </div></div>""",
                    unsafe_allow_html=True,
                )

with tab2:
    st.markdown(
        '<div class="card"><p class="card-title">📋 רשימת המשרות שלי</p>',
        unsafe_allow_html=True,
    )
    try:
        apps = requests.get(
            f"{API_URL}/applications",
            headers=get_auth_header(),
            timeout=10,
        ).json()

        if apps:
            for app in apps:
                status = app.get("status", "applied")
                score = app.get("match_score", 0)
                company = app.get("company", "—")
                app_id = app.get("id")
                statuses = ["applied", "pending", "interview", "accepted", "rejected"]

                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                with col1:
                    st.markdown(
                        f"<span class='app-company'>{company}</span>",
                        unsafe_allow_html=True,
                    )
                with col2:
                    new_status = st.selectbox(
                        "",
                        options=statuses,
                        index=statuses.index(status) if status in statuses else 0,
                        key=f"status_{app_id}",
                        label_visibility="collapsed",
                    )
                    if new_status != status:
                        requests.put(
                            f"{API_URL}/applications/{app_id}?status={new_status}"
                        )
                        update_activity()
                        st.rerun()
                with col3:
                    st.markdown(
                        f"<span class='app-score'>{score}%</span>",
                        unsafe_allow_html=True,
                    )
                with col4:
                    if st.button("🗑", key=f"del_{app_id}"):
                        requests.delete(f"{API_URL}/applications/{app_id}")
                        update_activity()
                        st.rerun()
                st.markdown(
                    "<hr style='border:none;border-top:1px solid #2a2a38;margin:0.4rem 0'>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                """<div style="text-align:center;padding:2.5rem;color:#a0a0b8">
                <div style="font-size:2.2rem;margin-bottom:0.8rem">📭</div>
                עדיין אין משרות שמורות
                </div>""",
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.error(f"שגיאה: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
