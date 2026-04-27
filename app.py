import streamlit as st
import json as _json

st.set_page_config(
    page_title="Ecualizador Pro",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Tema ─────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.header("🎨 Apariencia")
    is_light = st.toggle("☀️ Modo claro", value=(st.session_state.theme == "light"), key="light_toggle")
    theme = "light" if is_light else "dark"
    st.session_state.theme = theme
    st.divider()

    st.header("🎤 Fuente de audio")
    st.caption("Activá el micrófono y poné la música a volumen de evento.")

    st.divider()

    st.header("🎚️ Referencia")
    st.caption("Elegí un perfil contra el cual comparar cortes y ecualización.")

    referencia = st.selectbox(
        "Tipo de sonido",
        [
            "Referencia 1 - Agresiva (graves profundos)",
            "Referencia 2 - Equilibrada (vocales claras)",
            "Referencia 3 - Detallada (mucha definicion)",
            "Referencia 4 - Ruido Rosa (calibracion)"
        ],
        index=0,
        key="ref_selector",
        help="Cada referencia cambia los cortes de frecuencia y las sugerencias de ecualización."
    )

    ref_num = int(referencia.split(" ")[1])

    ref_cuts = {
        1: {"name": "Agresiva", "bajo": 250, "medio": 35, "brillo": 35},
        2: {"name": "Equilibrada", "bajo": 200, "medio": 80, "brillo": 80},
        3: {"name": "Detallada", "bajo": 150, "medio": 120, "brillo": 120},
        4: {"name": "Ruido Rosa", "bajo": 180, "medio": 100, "brillo": 100}
    }
    ref = ref_cuts.get(ref_num, ref_cuts[1])

    # ── Estilos según tema ──
    if theme == "light":
        sw, sb = "rgba(0,0,0,0.03)", "rgba(0,0,0,0.10)"
        ba_bg, ba_bor = "rgba(239,68,68,0.06)", "rgba(239,68,68,0.18)"
        md_bg, md_bor = "rgba(34,197,94,0.06)", "rgba(34,197,94,0.18)"
        br_bg, br_bor = "rgba(168,85,247,0.06)", "rgba(168,85,247,0.18)"
        rng_c, dsc_c = "#64748b", "#94a3b8"
    else:
        sw, sb = "rgba(15,17,25,0.6)", "rgba(255,255,255,0.08)"
        ba_bg, ba_bor = "rgba(239,68,68,0.10)", "rgba(239,68,68,0.25)"
        md_bg, md_bor = "rgba(34,197,94,0.10)", "rgba(34,197,94,0.25)"
        br_bg, br_bor = "rgba(168,85,247,0.10)", "rgba(168,85,247,0.25)"
        rng_c, dsc_c = "#94a3b8", "#64748b"

    st.markdown(f"""
    <div style="background:{sw}; border:1px solid {sb}; border-radius:12px; padding:14px 12px; margin:8px 0 12px 0;">
        <div style="font-size:10px; font-weight:600; color:{dsc_c}; margin-bottom:8px; letter-spacing:0.8px; text-transform:uppercase;">Cortes de referencia</div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:7px;">
            <div style="background:{ba_bg}; border:1px solid {ba_bor}; border-radius:10px; padding:10px 6px; text-align:center;">
                <div style="font-size:10px; font-weight:700; color:#ef4444; margin-bottom:2px;">BAJOS</div>
                <div style="font-size:8px; color:{rng_c};">45 – 250 Hz</div>
                <div style="font-size:24px; font-weight:800; color:#ef4444; margin:3px 0;">{ref["bajo"]}</div>
                <div style="font-size:8px; color:{dsc_c};">Corte alto</div>
            </div>
            <div style="background:{md_bg}; border:1px solid {md_bor}; border-radius:10px; padding:10px 6px; text-align:center;">
                <div style="font-size:10px; font-weight:700; color:#22c55e; margin-bottom:2px;">MEDIOS</div>
                <div style="font-size:8px; color:{rng_c};">35 – 400 Hz</div>
                <div style="font-size:24px; font-weight:800; color:#22c55e; margin:3px 0;">{ref["medio"]}</div>
                <div style="font-size:8px; color:{dsc_c};">Corte bajo</div>
            </div>
            <div style="background:{br_bg}; border:1px solid {br_bor}; border-radius:10px; padding:10px 6px; text-align:center;">
                <div style="font-size:10px; font-weight:700; color:#a78bfa; margin-bottom:2px;">BRILLO</div>
                <div style="font-size:8px; color:{rng_c};">35 – 400 Hz</div>
                <div style="font-size:24px; font-weight:800; color:#a78bfa; margin:3px 0;">{ref["brillo"]}</div>
                <div style="font-size:8px; color:{dsc_c};">Corte bajo</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("Los cortes y ajustes cambian según la referencia. Compará en tiempo real.")

# ── CSS Global ── (según tema) ───────────────────────────
if theme == "dark":
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        .stApp {
            background: linear-gradient(165deg, #08090d 0%, #0d1018 30%, #12192a 55%, #0d1018 75%, #08090d 100%);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }
        .stApp::before {
            content: "";
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(ellipse 70% 50% at 25% 15%, rgba(59,130,246,0.08) 0%, transparent 70%),
                radial-gradient(ellipse 70% 50% at 75% 55%, rgba(168,85,247,0.05) 0%, transparent 65%),
                radial-gradient(ellipse 60% 40% at 45% 85%, rgba(34,197,94,0.04) 0%, transparent 55%);
            pointer-events: none; z-index: 0;
        }
        section.main > div { position: relative; z-index: 1; }
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown { color: #e2e8f0 !important; }
        .stSubheader { color: #f1f5f9 !important; font-weight: 700 !important; font-size: 1.05rem !important; }
        .stCaption { color: #64748b !important; font-size: 0.8rem !important; }
        hr { border-color: rgba(255,255,255,0.05) !important; margin: 12px 0 !important; }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(8,9,13,0.97) 0%, rgba(13,16,24,0.94) 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.05) !important;
        }
        [data-testid="stSidebar"] h2 { font-size: 1rem !important; letter-spacing: 0.3px !important; }
        .stSelectbox > div > div {
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid rgba(255,255,255,0.10) !important;
            border-radius: 10px !important; color: #e2e8f0 !important;
            transition: border-color 0.25s !important;
        }
        .stSelectbox > div > div:hover { border-color: rgba(59,130,246,0.35) !important; }
        .stSelectbox label { color: #94a3b8 !important; font-weight: 500 !important; font-size: 12px !important; }
        .stHtml iframe { border: none !important; border-radius: 14px !important; overflow: hidden !important; }
        .stHtml { overflow-x: hidden !important; }
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.06); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.12); }
        @media (max-width: 768px) {
            .stColumns { flex-direction: column !important; }
            .stColumns > div { width: 100% !important; }
        }
    </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        .stApp {
            background: linear-gradient(165deg, #f1f5f9 0%, #f8fafc 30%, #eef2f6 55%, #f8fafc 75%, #f1f5f9 100%);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }
        .stApp::before {
            content: "";
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(ellipse 70% 50% at 25% 15%, rgba(59,130,246,0.05) 0%, transparent 70%),
                radial-gradient(ellipse 70% 50% at 75% 55%, rgba(168,85,247,0.03) 0%, transparent 65%),
                radial-gradient(ellipse 60% 40% at 45% 85%, rgba(34,197,94,0.03) 0%, transparent 55%);
            pointer-events: none; z-index: 0;
        }
        section.main > div { position: relative; z-index: 1; }
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown { color: #1e293b !important; }
        .stSubheader { color: #0f172a !important; font-weight: 700 !important; font-size: 1.05rem !important; }
        .stCaption { color: #64748b !important; font-size: 0.8rem !important; }
        hr { border-color: rgba(0,0,0,0.08) !important; margin: 12px 0 !important; }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
            border-right: 1px solid rgba(0,0,0,0.06) !important;
        }
        [data-testid="stSidebar"] h2 { font-size: 1rem !important; letter-spacing: 0.3px !important; }
        .stSelectbox > div > div {
            background: #ffffff !important;
            border: 1px solid rgba(0,0,0,0.12) !important;
            border-radius: 10px !important; color: #1e293b !important;
            transition: border-color 0.25s !important;
        }
        .stSelectbox > div > div:hover { border-color: rgba(59,130,246,0.40) !important; }
        .stSelectbox label { color: #475569 !important; font-weight: 500 !important; font-size: 12px !important; }
        .stHtml iframe { border: none !important; border-radius: 14px !important; overflow: hidden !important; }
        .stHtml { overflow-x: hidden !important; }
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.12); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.22); }
        @media (max-width: 768px) {
            .stColumns { flex-direction: column !important; }
            .stColumns > div { width: 100% !important; }
        }
    </style>
    """, unsafe_allow_html=True)

# ── Cabecera principal ──────────────────────────────────
badge_bg = "rgba(59,130,246,0.08)" if theme == "light" else "rgba(59,130,246,0.12)"
badge_cl = "#2563eb" if theme == "light" else "#93c5fd"

st.markdown(f"""
<div style="text-align:center; margin-bottom: 16px;">
    <h1 style="font-size:clamp(1.3rem, 4vw, 2.3rem); font-weight:800; margin:0 0 6px 0; background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #34d399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing:-0.5px;">
        &#x1F39B;&#xFE0F; Ecualizador Pro
    </h1>
    <span style="display:inline-block; background:{badge_bg}; color:{badge_cl}; padding:4px 16px; border-radius:18px; font-size:12px; font-weight:500;">
        &#x2699;&#xFE0F; EQ + Crossover en tiempo real
    </span>
</div>
""", unsafe_allow_html=True)

st.divider()
st.caption("Activá el micrófono y escuchá el entorno. La app analiza, sugiere cortes y compara contra la referencia.")

# ── Preparar datos para el componente ───────────────────
ctx_dict = {"referencia": ref_num, "theme": theme}
ctx = _json.dumps(ctx_dict, ensure_ascii=False)
btn_text = "MIC Activar"

COMPONENT_HTML = f"""
<div id="ecualizador-pro" class="theme-{theme}" style="font-family:'Inter',system-ui,-apple-system,sans-serif; overflow:hidden;">

  <!-- ── CSS variables del tema ── -->
  <style>
    .theme-light {{
      --sp-bg: rgba(0,0,0,0.03);          --sp-border: rgba(0,0,0,0.08);
      --cnv-bg: rgba(0,0,0,0.04);
      --mc-bg: rgba(0,0,0,0.015);          --mc-border: rgba(0,0,0,0.08);
      --mc-hov-border: rgba(0,0,0,0.16);   --mc-hov-shadow: rgba(0,0,0,0.04);
      --bw-bg: rgba(0,0,0,0.06);
      --mv-c: #0f172a;                     --mp-c: #2563eb;
      --mhz-c: #94a3b8;                    --ml-c: #475569;
      --sec-c: #475569;
      --xo-b-bg: rgba(239,68,68,0.06);     --xo-b-bd: rgba(239,68,68,0.18);
      --xo-m-bg: rgba(34,197,94,0.06);     --xo-m-bd: rgba(34,197,94,0.18);
      --xo-h-bg: rgba(168,85,247,0.06);    --xo-h-bd: rgba(168,85,247,0.18);
      --xol-c: #64748b;                    --xod-c: #94a3b8;
      --st-c: #94a3b8;
    }}
    .theme-dark {{
      --sp-bg: rgba(0,0,0,0.25);           --sp-border: rgba(255,255,255,0.05);
      --cnv-bg: rgba(0,0,0,0.30);
      --mc-bg: rgba(255,255,255,0.025);    --mc-border: rgba(255,255,255,0.06);
      --mc-hov-border: rgba(255,255,255,0.14); --mc-hov-shadow: rgba(59,130,246,0.06);
      --bw-bg: rgba(0,0,0,0.45);
      --mv-c: #f1f5f9;                     --mp-c: #60a5fa;
      --mhz-c: #475569;                    --ml-c: #94a3b8;
      --sec-c: #94a3b8;
      --xo-b-bg: rgba(239,68,68,0.08);     --xo-b-bd: rgba(239,68,68,0.20);
      --xo-m-bg: rgba(34,197,94,0.08);     --xo-m-bd: rgba(34,197,94,0.20);
      --xo-h-bg: rgba(168,85,247,0.08);    --xo-h-bd: rgba(168,85,247,0.20);
      --xol-c: #94a3b8;                    --xod-c: #64748b;
      --st-c: #475569;
    }}
  </style>

  <!-- ── Botones de control ── -->
  <div id="btnContainer" style="text-align:center; margin-bottom:18px; display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
    <button id="btnStart" onclick="startListening()" class="btn-start">{btn_text}</button>
    <button id="btnStop" onclick="stopListening()" class="btn-stop" style="display:none;">STOP Detener</button>
  </div>

  <!-- ── Espectro ── -->
  <div id="spectrumWrap" style="display:none; margin-bottom:16px; background:var(--sp-bg); border-radius:14px; padding:14px; border:1px solid var(--sp-border);">
    <div style="font-size:10px; font-weight:600; color:var(--sec-c); margin-bottom:6px; letter-spacing:1.2px; text-transform:uppercase;">Espectro en vivo</div>
    <canvas id="spectrumCanvas" style="width:100%; height:140px; border-radius:8px; display:block; background:var(--cnv-bg);"></canvas>
  </div>

  <!-- ── Medidores de banda ── -->
  <div id="meters" style="display:none; margin-bottom:16px;">
    <div class="meters-grid">
      <div id="m_bass" class="meter-card meter-bass">
        <div class="m-label"><span class="m-dot bass"></span>BAJOS</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_bass"></div><div class="m-bar-glow" id="g_bass"></div></div>
        <div class="m-val" id="v_bass">-- dB</div>
        <div class="m-peak" id="p_bass">Pico: --</div>
        <div class="m-hz">20 – 500 Hz</div>
      </div>
      <div id="m_mid" class="meter-card meter-mid">
        <div class="m-label"><span class="m-dot mid"></span>MEDIOS</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_mid"></div><div class="m-bar-glow" id="g_mid"></div></div>
        <div class="m-val" id="v_mid">-- dB</div>
        <div class="m-peak" id="p_mid">Pico: --</div>
        <div class="m-hz">500 Hz – 4K Hz</div>
      </div>
      <div id="m_high" class="meter-card meter-high">
        <div class="m-label"><span class="m-dot high"></span>BRILLO</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_high"></div><div class="m-bar-glow" id="g_high"></div></div>
        <div class="m-val" id="v_high">-- dB</div>
        <div class="m-peak" id="p_high">Pico: --</div>
        <div class="m-hz">4K – 16K Hz</div>
      </div>
    </div>
  </div>

  <!-- ── Tabla EQ y cortes ── -->
  <div id="instructions" style="display:none;">
    <div style="font-size:11px;font-weight:700;color:var(--sec-c);margin-bottom:8px;letter-spacing:1px;text-transform:uppercase;">Tabla de 15 bandas</div>

    <div style="font-size:11px;font-weight:600;color:#f87171;margin-bottom:4px;">GRAVES</div>
    <div id="gravesRow" style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px;"></div>

    <div style="font-size:11px;font-weight:600;color:#4ade80;margin-bottom:4px;">MEDIOS</div>
    <div id="mediosRow" style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px;"></div>

    <div style="font-size:11px;font-weight:600;color:#c4b5fd;margin-bottom:4px;">AGUDOS</div>
    <div id="agudosRow" style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px;"></div>

    <div id="xoCortes" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;margin-top:8px;">
      <div style="background:var(--xo-b-bg);border:1px solid var(--xo-b-bd);border-radius:10px;padding:8px 6px;text-align:center;">
        <div style="font-size:8px;color:var(--xol-c);text-transform:uppercase;">BAJOS</div>
        <div id="xoBajo" style="font-size:22px;font-weight:800;color:#ef4444;">250 Hz</div>
        <div style="font-size:7px;color:var(--xod-c);">Corte alto</div>
      </div>
      <div style="background:var(--xo-m-bg);border:1px solid var(--xo-m-bd);border-radius:10px;padding:8px 6px;text-align:center;">
        <div style="font-size:8px;color:var(--xol-c);text-transform:uppercase;">MEDIOS</div>
        <div id="xoMedio" style="font-size:22px;font-weight:800;color:#22c55e;">400 Hz</div>
        <div style="font-size:7px;color:var(--xod-c);">Corte bajo</div>
      </div>
      <div style="background:var(--xo-h-bg);border:1px solid var(--xo-h-bd);border-radius:10px;padding:8px 6px;text-align:center;">
        <div style="font-size:8px;color:var(--xol-c);text-transform:uppercase;">BRILLO</div>
        <div id="xoBrillo" style="font-size:22px;font-weight:800;color:#a78bfa;">35 Hz</div>
        <div style="font-size:7px;color:var(--xod-c);">Corte bajo</div>
      </div>
    </div>
  </div>

  <!-- ── Estado ── -->
  <div id="status" style="text-align:center; font-size:13px; font-weight:500; color:var(--st-c); margin-top:14px;">⏳ Listo para escuchar...</div>
</div>

<style>
  /* ── Botones ── */
  .btn-start {{
    padding: 14px 40px; font-size: 15px; font-weight: 700; border-radius: 12px;
    border: none; background: linear-gradient(135deg, #2563eb, #7c3aed); color: #fff;
    cursor: pointer; box-shadow: 0 4px 24px rgba(37,99,235,0.35); transition: all .25s;
    letter-spacing: 0.3px;
  }}
  .btn-start:hover {{ box-shadow: 0 6px 30px rgba(37,99,235,0.5); transform: translateY(-1px); }}
  .btn-stop {{
    padding: 14px 40px; font-size: 15px; font-weight: 700; border-radius: 12px;
    border: none; background: linear-gradient(135deg, #dc2626, #e11d48); color: #fff;
    cursor: pointer; box-shadow: 0 4px 24px rgba(220,38,38,0.35); transition: all .25s;
    letter-spacing: 0.3px;
  }}
  .btn-stop:hover {{ box-shadow: 0 6px 30px rgba(220,38,38,0.5); transform: translateY(-1px); }}

  /* ── Grilla de medidores ── */
  .meters-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}

  .meter-card {{
    background: var(--mc-bg); border: 1px solid var(--mc-border);
    border-radius: 14px; padding: 16px 12px 14px; text-align: center;
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    transition: border-color .4s, box-shadow .4s, transform .4s;
  }}
  .meter-card:hover {{
    border-color: var(--mc-hov-border); box-shadow: 0 0 40px var(--mc-hov-shadow);
    transform: translateY(-2px);
  }}

  .m-label {{
    font-size: 11px; font-weight: 700; color: var(--ml-c); margin-bottom: 10px;
    letter-spacing: 1.5px; display: flex; align-items: center; justify-content: center; gap: 7px;
  }}
  .m-dot {{ width: 9px; height: 9px; border-radius: 50%; display: inline-block; flex-shrink: 0; }}
  .m-dot.bass {{ background: #ef4444; box-shadow: 0 0 8px rgba(239,68,68,0.5); }}
  .m-dot.mid  {{ background: #22c55e; box-shadow: 0 0 8px rgba(34,197,94,0.5); }}
  .m-dot.high {{ background: #a78bfa; box-shadow: 0 0 8px rgba(168,85,247,0.5); }}

  .m-bar-wrap {{ background: var(--bw-bg); border-radius: 8px; height: 130px; position: relative; overflow: hidden; }}
  .m-bar {{
    position: absolute; bottom: 0; width: 100%; height: 0%; border-radius: 8px;
    transition: height .12s ease-out, background .4s; z-index: 2;
  }}
  .m-bar-glow {{
    position: absolute; bottom: 0; width: 100%; height: 0%; border-radius: 8px;
    transition: height .12s ease-out; filter: blur(14px); opacity: 0.45; z-index: 1;
  }}
  .m-val {{ font-size: 17px; font-weight: 800; margin-top: 8px; color: var(--mv-c); font-variant-numeric: tabular-nums; }}
  .m-peak {{ font-size: 13px; font-weight: 600; color: var(--mp-c); margin-top: 3px; }}
  .m-hz {{ font-size: 10px; color: var(--mhz-c); margin-top: 3px; letter-spacing: .5px; }}

  /* ── Animación pulso (escuchando) ── */
  @keyframes pulse {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(220,38,38,0.5); }}
    50%      {{ box-shadow: 0 0 0 14px rgba(220,38,38,0); }}
  }}
  .listening-active {{ animation: pulse 1.8s infinite; }}

  /* ── Responsive ── */
  @media (max-width: 768px) {{
    .meters-grid {{ grid-template-columns: 1fr; gap: 10px; }}
    .btn-start, .btn-stop {{ width: 100%; font-size: 15px; padding: 14px 24px; }}
    #btnContainer {{ flex-direction: column; align-items: center; gap: 10px; }}
    #xoCortes {{ grid-template-columns: 1fr !important; gap: 8px !important; }}
    .m-bar-wrap {{ height: 110px; }}
  }}
  @media (max-width: 480px) {{
    .m-bar-wrap {{ height: 90px; }}
    .m-val {{ font-size: 15px; }}
    .m-peak {{ font-size: 12px; }}
    .m-hz {{ font-size: 9px; }}
    #spectrumWrap {{ padding: 10px !important; }}
    #spectrumCanvas {{ height: 110px !important; }}
  }}
</style>

<script>
const CTX = {ctx};

let audioCtx, analyser, source, stream, raf;
const FFT = 4096;

const BANDS = [
  {{ id:"bass", label:"BAJOS",   lo:20,   hi:500,  color:"#ef4444" }},
  {{ id:"mid",  label:"MEDIOS",  lo:500,  hi:4000, color:"#22c55e" }},
  {{ id:"high", label:"BRILLO",  lo:4000, hi:16000,color:"#a78bfa" }},
];

const EQ_FREQS = [
  {{ hz: 25,   group: "graves" }},
  {{ hz: 40,   group: "graves" }},
  {{ hz: 63,   group: "graves" }},
  {{ hz: 100,  group: "graves" }},
  {{ hz: 160,  group: "graves" }},
  {{ hz: 250,  group: "graves" }},
  {{ hz: 400,  group: "graves" }},
  {{ hz: 630,  group: "medios" }},
  {{ hz: 1000, group: "medios" }},
  {{ hz: 1600, group: "medios" }},
  {{ hz: 2500, group: "medios" }},
  {{ hz: 4000, group: "medios" }},
  {{ hz: 6300, group: "agudos" }},
  {{ hz: 10000,group: "agudos" }},
  {{ hz: 16000,group: "agudos" }},
];

const REFERENCES = {{
  1: {{
    name: "Agresiva",
    bajo: 250, medio: 35, brillo: 35,
    xoLow: 250, xoHigh: 6300,
    eq: {{
      25: 4, 40: 3, 63: 2, 100: 0, 160: 0, 250: 3, 400: 1,
      630: 0, 1000: 1, 1600: 0, 2500: -2, 4000: -3,
      6300: -1, 10000: 0, 16000: -2
    }}
  }},
  2: {{
    name: "Equilibrada",
    bajo: 200, medio: 80, brillo: 80,
    xoLow: 200, xoHigh: 4000,
    eq: {{
      25: -1, 40: 0, 63: 1, 100: 2, 160: 1, 250: 0, 400: 0,
      630: 1, 1000: 2, 1600: 2, 2500: 1, 4000: 0,
      6300: 1, 10000: 1, 16000: 0
    }}
  }},
  3: {{
    name: "Detallada",
    bajo: 150, medio: 120, brillo: 120,
    xoLow: 150, xoHigh: 8000,
    eq: {{
      25: -3, 40: -2, 63: -1, 100: 0, 160: 1, 250: 2, 400: 2,
      630: 1, 1000: 2, 1600: 3, 2500: 3, 4000: 2,
      6300: 2, 10000: 3, 16000: 3
    }}
  }},
  4: {{
    name: "Ruido Rosa",
    bajo: 180, medio: 100, brillo: 100,
    xoLow: 180, xoHigh: 5000,
    eq: {{
      25: 7, 40: 5, 63: 4, 100: 3, 160: 2, 250: 1, 400: 0,
      630: -1, 1000: -2, 1600: -3, 2500: -4, 4000: -5,
      6300: -6, 10000: -7, 16000: -8
    }}
  }}
}};

function formatHz(hz) {{
  if (hz >= 1000) return (hz / 1000) + "K";
  return hz + "";
}}

// ── Render 15-band EQ table ──
function renderEqTable(data, sr) {{
  const gravesEl = document.getElementById("gravesRow");
  const mediosEl = document.getElementById("mediosRow");
  const agudosEl = document.getElementById("agudosRow");
  const xoBajoEl = document.getElementById("xoBajo");
  const xoMedioEl = document.getElementById("xoMedio");
  const xoBrilloEl = document.getElementById("xoBrillo");

  if (!gravesEl) return;

  gravesEl.innerHTML = "";
  mediosEl.innerHTML = "";
  agudosEl.innerHTML = "";

  const refNum = CTX.referencia || 1;
  const ref = REFERENCES[refNum] || REFERENCES[1];

  xoBajoEl.textContent = formatHz(ref.bajo) + " Hz";
  xoMedioEl.textContent = formatHz(ref.medio) + " Hz";
  xoBrilloEl.textContent = formatHz(ref.brillo) + " Hz";

  const hzPerBin = sr / FFT;

  for (const freq of EQ_FREQS) {{
    const centerIdx = Math.round(freq.hz / hzPerBin);
    let energy = -100;
    let sum = 0, count = 0;

    for (let i = centerIdx - 3; i <= centerIdx + 3; i++) {{
      if (i >= 0 && i < data.length) {{ sum += data[i]; count++; }}
    }}
    energy = count > 0 ? sum / count : -100;

    const refEq = ref.eq[freq.hz] || 0;

    let hiTh, loTh;
    if (freq.group === "graves")  {{ hiTh = -45; loTh = -65; }}
    else if (freq.group === "medios") {{ hiTh = -50; loTh = -70; }}
    else {{ hiTh = -48; loTh = -68; }}

    let color = "#22c55e";
    let bgColor = "rgba(34,197,94,0.12)";
    let borderColor = "rgba(34,197,94,0.4)";

    const nearLowXO  = (ref.xoLow  && freq.hz <= ref.xoLow  + 20 && freq.hz >= ref.xoLow  - 40);
    const nearHighXO = (ref.xoHigh && freq.hz >= ref.xoHigh - 500 && freq.hz <= ref.xoHigh + 500);

    if (energy > hiTh || (nearLowXO && freq.hz < ref.xoLow) || (nearHighXO && freq.hz > ref.xoHigh)) {{
      color = "#ef4444";
      bgColor = "rgba(239,68,68,0.12)";
      borderColor = "rgba(239,68,68,0.4)";
    }} else if (energy < loTh) {{
      color = "#3b82f6";
      bgColor = "rgba(59,130,246,0.12)";
      borderColor = "rgba(59,130,246,0.4)";
    }}

    const groupLabel = freq.group === "graves" ? "BAJO" : freq.group === "medios" ? "MEDIO" : "BRILLO";

    const hzLabel = freq.hz >= 1000 ? (freq.hz/1000) + "K" : freq.hz;
    const refDb = ref.eq[freq.hz] || 0;
    const dbLabel = refDb > 0 ? "+" + refDb : "" + refDb;
    const div = document.createElement("div");
    div.style.cssText = "background:" + bgColor + ";border:1px solid " + borderColor + ";border-radius:7px;padding:5px 7px;text-align:center;min-width:48px;transition:all 0.3s;";
    div.innerHTML =
      '<div style="font-size:7px;font-weight:600;color:#64748b;text-transform:uppercase;margin-bottom:1px;">' + groupLabel + '</div>' +
      '<div style="font-size:12px;font-weight:700;color:' + color + ';">' + hzLabel + '</div>' +
      '<div style="font-size:14px;font-weight:800;color:' + color + ';">' + dbLabel + '</div>';

    if (freq.group === "graves")  gravesEl.appendChild(div);
    else if (freq.group === "medios") mediosEl.appendChild(div);
    else agudosEl.appendChild(div);
  }}
}}

// ── Utilidades de audio ──
function freqToIndex(f, sampleRate) {{
  return Math.round(f / (sampleRate / FFT));
}}

function bandEnergy(data, lo, hi, sr) {{
  const iLo = freqToIndex(lo, sr);
  const iHi = freqToIndex(hi, sr);
  let sum = 0, count = 0;
  for (let i = iLo; i <= iHi && i < data.length; i++) {{ sum += data[i]; count++; }}
  return count > 0 ? sum / count : -100;
}}

function peakFrequency(data, lo, hi, sr) {{
  const iLo = freqToIndex(lo, sr);
  const iHi = freqToIndex(hi, sr);
  let maxVal = -Infinity, maxIdx = iLo;
  for (let i = iLo; i <= iHi && i < data.length; i++) {{
    if (data[i] > maxVal) {{ maxVal = data[i]; maxIdx = i; }}
  }}
  return maxIdx * (sr / FFT);
}}

function findCrossover(data, fromHz, toHz, sr) {{
  const iLo = freqToIndex(fromHz, sr);
  const iHi = freqToIndex(toHz, sr);
  const hzPerBin = sr / FFT;

  let sum = 0, count = 0;
  for (let i = iLo; i <= iHi && i < data.length; i++) {{ sum += data[i]; count++; }}
  const avg = sum / count;

  let weightedSum = 0, weightTotal = 0;
  for (let i = iLo; i <= iHi && i < data.length; i++) {{
    if (data[i] < avg) {{
      const weight = avg - data[i];
      weightedSum += i * weight;
      weightTotal += weight;
    }}
  }}

  if (weightTotal > 0) return (weightedSum / weightTotal) * hzPerBin;

  let minVal = Infinity, minIdx = iLo;
  for (let i = iLo; i <= iHi && i < data.length; i++) {{
    if (data[i] < minVal) {{ minVal = data[i]; minIdx = i; }}
  }}
  return minIdx * hzPerBin;
}}

// ── Suavizado ──
const smooth = {{bass:[], mid:[], high:[]}};
const smoothPeak = {{bass:[], mid:[], high:[]}};
const smoothXoData = {{xoLow:[], xoHigh:[]}};
const prevXo = {{xoLow: 500, xoHigh: 4000}};
const SMOOTH_N = 8;
const MAX_CHANGE_PER_FRAME = 30;

function smoothVal(key, val) {{
  smooth[key].push(val);
  if (smooth[key].length > SMOOTH_N) smooth[key].shift();
  return smooth[key].reduce((a,b) => a+b, 0) / smooth[key].length;
}}

function smoothPeakVal(key, val) {{
  smoothPeak[key].push(val);
  if (smoothPeak[key].length > 6) smoothPeak[key].shift();
  return smoothPeak[key].reduce((a,b) => a+b, 0) / smoothPeak[key].length;
}}

function smoothXo(key, val) {{
  smoothXoData[key].push(val);
  if (smoothXoData[key].length > 30) smoothXoData[key].shift();
  const sorted = [...smoothXoData[key]].sort((a,b) => a-b);
  const median = sorted[Math.floor(sorted.length / 2)];
  const change = median - prevXo[key];
  const limitedChange = Math.max(-MAX_CHANGE_PER_FRAME, Math.min(MAX_CHANGE_PER_FRAME, change));
  prevXo[key] = prevXo[key] + limitedChange * 0.3;
  return Math.round(prevXo[key]);
}}

// ── Dibujo del espectro ──
function drawSpectrum(data, sr) {{
  const canvas = document.getElementById("spectrumCanvas");
  if (!canvas) return;
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const w = rect.width; const h = 140;
  canvas.width = w * dpr; canvas.height = h * dpr; canvas.style.height = h + "px";
  const ctx2 = canvas.getContext("2d"); ctx2.scale(dpr, dpr);
  // Fondo según tema
  const isLight = document.getElementById("ecualizador-pro").classList.contains("theme-light");
  ctx2.fillStyle = isLight ? "rgba(0,0,0,0.03)" : "rgba(0,0,0,0.45)";
  ctx2.fillRect(0, 0, w, h);

  const maxFreq = 8000;
  const maxIdx = freqToIndex(maxFreq, sr);
  const usable = Math.min(maxIdx, data.length);
  const barW = Math.max(1, (w / usable) * 1.5);
  const drawH = h - 20;

  for (let i = 1; i < usable; i++) {{
    const val = data[i];
    const norm = Math.max(0, Math.min(1, (val + 100) / 100));
    const barH = norm * drawH * 0.95;
    const x = (i / usable) * w;
    const freqBar = (i / usable) * maxFreq;
    let r, g, b;
    if (freqBar < 500)       {{ r=239; g=68;  b=68;  }}
    else if (freqBar < 4000) {{ r=34;  g=197; b=94;  }}
    else                     {{ r=167; g=139; b=250; }}
    const alpha = isLight ? (0.50 + norm * 0.50) : (0.35 + norm * 0.65);
    ctx2.fillStyle = `rgba(${{r}},${{g}},${{b}},${{alpha}})`;
    ctx2.fillRect(x, drawH - barH, barW, barH);
  }}

  // Líneas de crossover
  const xoLowX  = (smoothXoData.xoLow.length  ? smoothXoData.xoLow[smoothXoData.xoLow.length-1]   : 250) / maxFreq * w;
  const xoHighX = (smoothXoData.xoHigh.length ? smoothXoData.xoHigh[smoothXoData.xoHigh.length-1] : 4000) / maxFreq * w;
  ctx2.setLineDash([6, 4]);
  ctx2.lineWidth = 2;
  ctx2.strokeStyle = "rgba(245,158,11,0.8)";
  ctx2.beginPath(); ctx2.moveTo(xoLowX, 0); ctx2.lineTo(xoLowX, drawH - 5); ctx2.stroke();
  ctx2.strokeStyle = "rgba(168,85,247,0.8)";
  ctx2.beginPath(); ctx2.moveTo(xoHighX, 0); ctx2.lineTo(xoHighX, drawH - 5); ctx2.stroke();
  ctx2.setLineDash([]);

  // Etiquetas Hz
  const hzLabels = [50, 120, 250, 500, 1000, 2000, 4000, 8000];
  ctx2.fillStyle = isLight ? "rgba(0,0,0,0.40)" : "rgba(255,255,255,0.35)";
  ctx2.font = "10px Inter, system-ui, sans-serif"; ctx2.textAlign = "center";
  for (const hz of hzLabels) {{
    const x = (hz / maxFreq) * w;
    const label = hz >= 1000 ? (hz/1000) + "k" : hz + "";
    ctx2.fillText(label, x, h - 3);
  }}
}}

// ── Loop principal ──
function loop() {{
  const sr = audioCtx.sampleRate;
  const data = new Float32Array(analyser.frequencyBinCount);
  analyser.getFloatFrequencyData(data);

  const rawXoLow  = findCrossover(data, 200, 800, sr);
  const rawXoHigh = findCrossover(data, 3000, 6000, sr);
  const xoLow  = smoothXo("xoLow", rawXoLow);
  const xoHigh = smoothXo("xoHigh", rawXoHigh);

  drawSpectrum(data, sr);
  renderEqTable(data, sr);

  BANDS.forEach(band => {{
    const raw    = bandEnergy(data, band.lo, band.hi, sr);
    const level  = smoothVal(band.id, raw);
    const peakHz = smoothPeakVal(band.id, peakFrequency(data, band.lo, band.hi, sr));
    const pct    = Math.min(100, Math.max(0, (level + 100) / 100 * 100));

    document.getElementById("b_" + band.id).style.height = pct + "%";
    document.getElementById("b_" + band.id).style.background = band.color;
    document.getElementById("g_" + band.id).style.height = pct + "%";
    document.getElementById("g_" + band.id).style.background = band.color;
    document.getElementById("v_" + band.id).textContent = level.toFixed(1) + " dB";
    document.getElementById("p_" + band.id).textContent = "Pico: " + formatHz(peakHz);
  }});

  raf = requestAnimationFrame(loop);
}}

// ── Control de micrófono ──
async function startListening() {{
  try {{
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = FFT;
    analyser.smoothingTimeConstant = 0.7;

    stream = await navigator.mediaDevices.getUserMedia({{ audio: true, video: false }});
    source = audioCtx.createMediaStreamSource(stream);
    source.connect(analyser);

    document.getElementById("status").innerHTML = '<span style="color:#4ade80;font-weight:600;">&#x25CF; Escuchando...</span>';
    document.getElementById("btnStart").style.display = "none";
    const btnStop = document.getElementById("btnStop");
    btnStop.style.display = "inline-block";
    btnStop.classList.add("listening-active");
    document.getElementById("meters").style.display = "block";
    document.getElementById("spectrumWrap").style.display = "block";
    document.getElementById("instructions").style.display = "block";
    window.parent.postMessage({{ type: "streamlit:setSize", height: document.body.scrollHeight }}, "*");
    loop();
  }} catch(e) {{
    document.getElementById("status").innerHTML = '<span style="color:#f87171;">&#x2716; Error: ' + e.message + '</span>';
  }}
}}

function stopListening() {{
  if (raf) cancelAnimationFrame(raf);
  if (stream) stream.getTracks().forEach(t => t.stop());
  if (audioCtx) audioCtx.close();
  document.getElementById("btnStart").style.display = "inline-block";
  const btnStop = document.getElementById("btnStop");
  btnStop.style.display = "none";
  btnStop.classList.remove("listening-active");
  document.getElementById("status").innerHTML = '<span style="color:#475569;">&#x25A0; Detenido</span>';
  const canvas = document.getElementById("spectrumCanvas");
  if (canvas) {{
    const ctx2 = canvas.getContext("2d");
    const isLight = document.getElementById("ecualizador-pro").classList.contains("theme-light");
    ctx2.fillStyle = isLight ? "rgba(0,0,0,0.03)" : "rgba(0,0,0,0.45)";
    ctx2.fillRect(0, 0, canvas.width, canvas.height);
  }}
}}

function notifySize() {{
  const el = document.getElementById("ecualizador-pro");
  if (el) {{ window.parent.postMessage({{ type: "streamlit:setSize", height: el.scrollHeight + 20 }}, "*"); }}
}}
new MutationObserver(notifySize).observe(document.getElementById("ecualizador-pro"), {{ childList: true, subtree: true, attributes: true }});
</script>
"""

import streamlit.components.v1 as components
components.html(COMPONENT_HTML, height=900, scrolling=True)
