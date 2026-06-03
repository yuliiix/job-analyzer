import streamlit as st
import requests

st.set_page_config(
    page_title="Job Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Playfair+Display:wght@700&display=swap');

    :root {
        --bg: #0f0f13;
        --card: #1a1a24;
        --accent: #7c6aff;
        --accent2: #ff6a9e;
        --accent3: #6affce;
        --text: #e8e8f0;
        --muted: #6b6b80;
        --border: #2a2a38;
    }

    html, body, [class*="css"], p, span, div, label, input, textarea, button {
        font-family: 'Outfit', sans-serif !important;
    }

    .stApp { background: var(--bg); }

    .hero {
        text-align: center;
        padding: 1.8rem 2rem 1.4rem 2rem;
        background: var(--card);
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--accent), var(--accent2), var(--accent3));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
    }
    .hero-sub {
        color: var(--muted);
        font-size: 0.9rem;
        margin: 0;
        font-family: 'Outfit', sans-serif !important;
    }

    .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
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
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 0.8rem;
    }

    .score-num {
        font-family: 'Outfit', sans-serif !important;
        font-size: 3rem;
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
        margin-top: 0.6rem;
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
        padding: 0.2rem 0.7rem;
        font-size: 0.8rem;
        margin: 0.2rem;
        font-family: 'Outfit', sans-serif !important;
    }
    .tag-missing { background: rgba(255,106,158,0.1); border: 1px solid rgba(255,106,158,0.3); color: var(--accent2); }
    .tag-have    { background: rgba(106,255,206,0.1); border: 1px solid rgba(106,255,206,0.3); color: var(--accent3); }
    .tag-skill   { background: rgba(124,106,255,0.1); border: 1px solid rgba(124,106,255,0.3); color: var(--accent); }

    .app-company { color: var(--text); font-weight: 600; }
    .app-score   { font-family: 'Outfit', sans-serif !important; color: var(--accent3); font-size: 0.85rem; }
    .status-badge { display: inline-block; padding: 0.15rem 0.6rem; border-radius: 20px; font-size: 0.75rem; }
    .s-applied   { background:rgba(106,255,206,0.1); color:#6affce; border:1px solid rgba(106,255,206,0.3); }
    .s-pending   { background:rgba(255,200,50,0.1);  color:#ffc832; border:1px solid rgba(255,200,50,0.3); }
    .s-rejected  { background:rgba(255,80,80,0.1);   color:#ff5050; border:1px solid rgba(255,80,80,0.3); }
    .s-interview { background:rgba(124,106,255,0.1); color:#7c6aff; border:1px solid rgba(124,106,255,0.3); }

    .stTextArea textarea, .stTextInput input {
        background: #12121a !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.9rem !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    label { color: var(--muted) !important; font-size: 0.82rem !important; }
    .stTabs [data-baseweb="tab-list"] { background: var(--card); border-radius: 8px; padding: 4px; gap: 4px; }
    .stTabs [data-baseweb="tab"] { color: var(--muted) !important; border-radius: 6px; font-family: 'Outfit', sans-serif !important; }
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

API_URL = "http://localhost:8000"

# ---- Hero ----
st.markdown(
    """
    <div class="hero">
        <p class="hero-title">Job Analyzer 🎯</p>
        <p class="hero-sub">העלה קורות חיים, הדבק תיאור משרה — וגלה כמה אתה מתאים</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["✨  נתח משרה", "📋  המשרות שלי"])

# ================================================
# TAB 1
# ================================================
with tab1:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="card"><p class="card-title">📄 פרטי המשרה</p>', unsafe_allow_html=True)

        description = st.text_area("תיאור המשרה", height=140, placeholder="הדבק כאן את תיאור המשרה...")
        company_name = st.text_input("שם החברה", placeholder="Google")

        cv_file = st.file_uploader("קורות חיים (PDF)", type=["pdf"])

        if cv_file:
            with st.spinner("מחלץ כישורים..."):
                try:
                    res = requests.post(
                        f"{API_URL}/extract-skills",
                        files={"file": (cv_file.name, cv_file.getvalue(), "application/pdf")},
                        timeout=30,
                    )
                    extracted = res.json().get("skills", [])
                    st.session_state["skills"] = extracted
                    st.success(f"✅ זוהו {len(extracted)} כישורים!")
                except Exception as e:
                    st.error(f"שגיאה בחילוץ: {e}")

        if "skills" in st.session_state and st.session_state["skills"]:
            skills_html = "".join(
                f'<span class="tag tag-skill">{s}</span>'
                for s in st.session_state["skills"]
            )
            st.markdown(
                f'<div style="margin-top:0.5rem"><p class="card-title">כישורים שזוהו</p>{skills_html}</div>',
                unsafe_allow_html=True,
            )

        analyze_btn = st.button("🔍  נתח עכשיו", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        if analyze_btn and description:
            user_skills = st.session_state.get("skills", [])

            if not user_skills:
                st.warning("⚠️ העלה קורות חיים קודם כדי לחלץ כישורים!")
            else:
                with st.spinner("מנתח..."):
                    try:
                        res = requests.post(
                            f"{API_URL}/analyze",
                            json={"description": description, "user_skills": user_skills},
                            timeout=30,
                        )
                        r = res.json()
                        score = r.get("match_score", 0)
                        missing = r.get("missing_skills", [])
                        ttl = r.get("time_to_learn", {})

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
                        have_html = "".join(f'<span class="tag tag-have">✓ {s}</span>' for s in have)
                        miss_html = "".join(f'<span class="tag tag-missing">✗ {s}</span>' for s in missing)
                        st.markdown(
                            f"""<div class="card">
                            <p class="card-title">⚡ כישורים</p>
                            {have_html}{miss_html}
                            </div>""",
                            unsafe_allow_html=True,
                        )

                        if ttl:
                            rows = "".join(
                                f"<tr><td style='padding:0.3rem 0.6rem;color:var(--text)'>{k}</td>"
                                f"<td style='padding:0.3rem 0.6rem;color:#6affce;font-size:0.8rem'>{v}</td></tr>"
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
                                    "company": company_name or "לא צוין",
                                    "status": "applied",
                                    "match_score": score,
                                },
                            )
                            if save.status_code == 200:
                                st.success("✅ נשמר!")

                    except Exception as e:
                        st.error(f"שגיאה: {e}")
        else:
            st.markdown(
                """<div class="card" style="text-align:center;padding:3rem 1rem">
                <div style="font-size:2.5rem;margin-bottom:0.8rem">🎯</div>
                <div style="color:var(--muted);font-size:0.9rem">
                העלה קורות חיים והדבק תיאור משרה<br>כדי לראות ניתוח התאמה
                </div></div>""",
                unsafe_allow_html=True,
            )

# ================================================
# TAB 2
# ================================================
with tab2:
    st.markdown('<div class="card"><p class="card-title">📋 רשימת המשרות שלי</p>', unsafe_allow_html=True)
    try:
        apps = requests.get(f"{API_URL}/applications", timeout=10).json()
        if apps:
            for app in apps:
                status = app.get("status", "applied")
                score = app.get("match_score", 0)
                company = app.get("company", "—")
                app_id = app.get("id")
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                with col1:
                    st.markdown(f"<span class='app-company'>{company}</span>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<span class="status-badge s-{status}">{status}</span>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<span class='app-score'>{score}%</span>", unsafe_allow_html=True)
                with col4:
                    if st.button("🗑", key=f"del_{app_id}"):
                        requests.delete(f"{API_URL}/applications/{app_id}")
                        st.rerun()
                st.markdown(
                    "<hr style='border:none;border-top:1px solid #2a2a38;margin:0.3rem 0'>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                """<div style="text-align:center;padding:2rem;color:var(--muted)">
                <div style="font-size:2rem;margin-bottom:0.5rem">📭</div>
                עדיין אין משרות שמורות
                </div>""",
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.error(f"שגיאה: {e}")
    st.markdown("</div>", unsafe_allow_html=True)