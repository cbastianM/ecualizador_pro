import streamlit as st
import json as _json

st.set_page_config(
    page_title="Ecualizador Pro",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0f1119 30%, #0d1525 60%, #0a0a0f 100%);
        font-family: 'Inter', sans-serif;
    }
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse at 30% 20%, rgba(59,130,246,0.06) 0%, transparent 60%),
                    radial-gradient(ellipse at 70% 60%, rgba(168,85,247,0.04) 0%, transparent 60%),
                    radial-gradient(ellipse at 50% 80%, rgba(34,197,94,0.04) 0%, transparent 50%);
        pointer-events: none; z-index: 0;
    }
    section.main > div { position: relative; z-index: 1; }
    h1, h2, h3, h4, h5, h6, p, span, div, label, caption, .stMarkdown { color: #e2e8f0 !important; }
    hr { border-color: rgba(255,255,255,0.06) !important; }
    .stSelectbox > div > div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; color: #e2e8f0 !important; }
    .stSelectbox label { color: #94a3b8 !important; font-weight: 500 !important; font-size: 13px !important; }
    .stSubheader { color: #f1f5f9 !important; font-weight: 700 !important; }
    .stCaption { color: #64748b !important; }
    section[data-testid="stSidebar"] { display: none; }
    /* Ocultar scrollbar del iframe del componente */
    .stHtml iframe { border: none !important; }
    /* Ocultar scrollbar horizontal y dejar solo la vertical de la página */
    .stHtml { overflow-x: hidden !important; }
    @media (max-width: 768px) { .stColumns { flex-direction: column !important; } .stColumns > div { width: 100% !important; } }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom: 8px;">
    <h1 style="font-size:clamp(1.5rem, 5vw, 2.8rem); font-weight:800; margin:0; background: linear-gradient(135deg, #60a5fa, #a78bfa, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        🎛️ Ecualizador Pro
    </h1>
    <p style="color:#94a3b8; font-size:clamp(0.8rem, 2.5vw, 1rem); margin-top:4px;">
        Afiná tu sonido en tiempo real · Activá el micrófono y recibí instrucciones precisas
    </p>
</div>
""", unsafe_allow_html=True)
st.divider()

st.markdown("""
<div style="text-align:center; margin-bottom:12px;">
    <span style="background:rgba(59,130,246,0.15); color:#60a5fa; padding:4px 16px; border-radius:20px; font-size:13px; font-weight:600;">
        ⚙️ Configurá tu entorno para un análisis más preciso
    </span>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""<div class="config-card">""", unsafe_allow_html=True)
    st.subheader("📍 El lugar")
    lugar = st.selectbox("¿Dónde estás?", ["Adentro (salón, club)", "Carpa / toldo", "Al aire libre"])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="config-card">""", unsafe_allow_html=True)
    st.subheader("🔊 El equipo")
    marca = st.selectbox("Marca del equipo", ["JBL", "Yamaha", "RCF"])
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("""<div class="config-card">""", unsafe_allow_html=True)
    st.subheader("🎵 La música")
    genero = st.selectbox("¿Qué música va a sonar?", ["Salsa", "Rock", "Clásica"])
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.subheader("🎤 Escuchá en tiempo real")
st.caption("Activá el micrófono, poné la música a volumen de evento y el afinador te dirá qué ajustar.")

ctx = _json.dumps({
    "lugar": lugar, "marca": marca, "genero": genero,
})

COMPONENT_HTML = f"""
<div id="ecualizador-pro" style="font-family:'Inter',system-ui,sans-serif; overflow:hidden;">

  <div id="btnContainer" style="text-align:center; margin-bottom:20px;">
    <button id="btnStart" onclick="startListening()" class="btn-start">🎙️ Activar micrófono</button>
    <button id="btnStop" onclick="stopListening()" class="btn-stop">⏹ Detener</button>
  </div>

  <div id="spectrumWrap" style="display:none; margin-bottom:20px; background:rgba(0,0,0,0.3); border-radius:14px; padding:14px; border:1px solid rgba(255,255,255,0.06);">
    <div style="font-size:11px; font-weight:600; color:#64748b; margin-bottom:6px; letter-spacing:1px; text-transform:uppercase;">📊 Espectro de frecuencias</div>
    <canvas id="spectrumCanvas" style="width:100%; height:140px; border-radius:8px; display:block;"></canvas>
  </div>

  <div id="meters" style="display:none; margin-bottom:24px;">
    <div class="meters-grid">
      <div id="m_sub" class="meter-card">
        <div class="m-label"><span class="m-dot" style="background:#ef4444;"></span>SUB-GRAVES</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_sub"></div><div class="m-bar-glow" id="g_sub"></div></div>
        <div class="m-val" id="v_sub">-- dB</div>
        <div class="m-peak" id="p_sub">Pico: -- Hz</div>
        <div class="m-hz">20 – 120 Hz</div>
      </div>
      <div id="m_low" class="meter-card">
        <div class="m-label"><span class="m-dot" style="background:#f59e0b;"></span>MEDIOS-BAJOS</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_low"></div><div class="m-bar-glow" id="g_low"></div></div>
        <div class="m-val" id="v_low">-- dB</div>
        <div class="m-peak" id="p_low">Pico: -- Hz</div>
        <div class="m-hz">120 – 500 Hz</div>
      </div>
      <div id="m_mid" class="meter-card">
        <div class="m-label"><span class="m-dot" style="background:#22c55e;"></span>MEDIOS</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_mid"></div><div class="m-bar-glow" id="g_mid"></div></div>
        <div class="m-val" id="v_mid">-- dB</div>
        <div class="m-peak" id="p_mid">Pico: -- Hz</div>
        <div class="m-hz">500 Hz – 4K Hz</div>
      </div>
      <div id="m_high" class="meter-card">
        <div class="m-label"><span class="m-dot" style="background:#a78bfa;"></span>AGUDOS</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_high"></div><div class="m-bar-glow" id="g_high"></div></div>
        <div class="m-val" id="v_high">-- dB</div>
        <div class="m-peak" id="p_high">Pico: -- Hz</div>
        <div class="m-hz">4K – 16K Hz</div>
      </div>
    </div>
  </div>

  <div id="instructions" style="display:none;">
    <div style="font-size:12px; font-weight:700; color:#94a3b8; margin-bottom:12px; letter-spacing:1px; text-transform:uppercase;">🎛️ Instrucciones de ecualización</div>
    <div id="inst_sub"  class="inst-row"><div class="inst-band" style="color:#ef4444;">SUB-GRAVES</div><div class="inst-text" id="inst_sub_text">—</div></div>
    <div id="inst_low"  class="inst-row"><div class="inst-band" style="color:#f59e0b;">MEDIOS-BAJOS</div><div class="inst-text" id="inst_low_text">—</div></div>
    <div id="inst_mid"  class="inst-row"><div class="inst-band" style="color:#22c55e;">MEDIOS</div><div class="inst-text" id="inst_mid_text">—</div></div>
    <div id="inst_high" class="inst-row"><div class="inst-band" style="color:#a78bfa;">AGUDOS</div><div class="inst-text" id="inst_high_text">—</div></div>
  </div>

  <div id="status" style="text-align:center; font-size:13px; color:#64748b; margin-top:16px;">⏳ Listo para escuchar...</div>
</div>

<style>
  .btn-start {{
    padding: 14px 36px; font-size: 16px; font-weight: 700; border-radius: 12px;
    border: none; background: linear-gradient(135deg, #2563eb, #7c3aed); color: white;
    cursor: pointer; box-shadow: 0 4px 20px rgba(37,99,235,0.4); transition: all .3s;
  }}
  .btn-stop {{
    display: none; padding: 14px 36px; font-size: 16px; font-weight: 700; border-radius: 12px;
    border: none; background: linear-gradient(135deg, #dc2626, #e11d48); color: white;
    cursor: pointer; box-shadow: 0 4px 20px rgba(220,38,38,0.4); margin-left: 12px; transition: all .3s;
  }}
  .meters-grid {{
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
  }}
  @media (max-width: 600px) {{
    .meters-grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
  }}
  .meter-card {{
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 14px 10px 12px; text-align: center;
    backdrop-filter: blur(10px); transition: border-color .4s, box-shadow .4s;
  }}
  .meter-card:hover {{ border-color: rgba(255,255,255,0.15); box-shadow: 0 0 30px rgba(59,130,246,0.08); }}
  .m-label {{ font-size: 10px; font-weight: 700; color: #94a3b8; margin-bottom: 8px; letter-spacing: 1.2px; display: flex; align-items: center; justify-content: center; gap: 6px; }}
  .m-dot {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; flex-shrink: 0; }}
  .m-bar-wrap {{ background: rgba(0,0,0,0.4); border-radius: 8px; height: 100px; position: relative; overflow: hidden; }}
  .m-bar {{ position: absolute; bottom: 0; width: 100%; height: 0%; border-radius: 8px; transition: height .12s ease-out, background .4s; z-index: 2; }}
  .m-bar-glow {{ position: absolute; bottom: 0; width: 100%; height: 0%; border-radius: 8px; transition: height .12s ease-out; filter: blur(12px); opacity: 0.5; z-index: 1; }}
  .m-val {{ font-size: 15px; font-weight: 700; margin-top: 6px; color: #e2e8f0; font-variant-numeric: tabular-nums; }}
  .m-peak {{ font-size: 12px; font-weight: 600; color: #60a5fa; margin-top: 2px; }}
  .m-hz {{ font-size: 9px; color: #475569; margin-top: 2px; letter-spacing: .5px; }}
  .inst-row {{
    padding: 14px 16px; border-radius: 10px; margin-bottom: 10px;
    border-left: 4px solid #475569; background: rgba(0,0,0,0.25);
    transition: all .35s; overflow-wrap: break-word; word-break: break-word;
  }}
  .inst-band {{ font-size: 10px; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 4px; }}
  .inst-text {{ font-size: 15px; font-weight: 600; line-height: 1.5; overflow-wrap: break-word; word-break: break-word; }}
  @media (max-width: 480px) {{
    .btn-start, .btn-stop {{ width: 100%; margin-left: 0 !important; }}
    .btn-stop {{ margin-top: 10px; }}
    #btnContainer {{ display: flex; flex-direction: column; align-items: center; gap: 10px; }}
  }}
  @keyframes pulse {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(220,38,38,0.6); }}
    50% {{ box-shadow: 0 0 0 12px rgba(220,38,38,0); }}
  }}
  .listening-active {{ animation: pulse 1.8s infinite; }}
</style>

<script>
const CTX = {ctx};

let audioCtx, analyser, source, stream, raf;
const FFT = 4096;

const BANDS = [
  {{ id:"sub",  label:"SUB-GRAVES",   lo:20,   hi:120,  color:"#ef4444" }},
  {{ id:"low",  label:"MEDIOS-BAJOS", lo:120,  hi:500,  color:"#f59e0b" }},
  {{ id:"mid",  label:"MEDIOS",       lo:500,  hi:4000, color:"#22c55e" }},
  {{ id:"high", label:"AGUDOS",       lo:4000, hi:16000,color:"#a78bfa" }}
];

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

// ── Find peak frequency in a band ──
function peakFrequency(data, lo, hi, sr) {{
  const iLo = freqToIndex(lo, sr);
  const iHi = freqToIndex(hi, sr);
  let maxVal = -Infinity, maxIdx = iLo;
  for (let i = iLo; i <= iHi && i < data.length; i++) {{
    if (data[i] > maxVal) {{ maxVal = data[i]; maxIdx = i; }}
  }}
  const hzPerBin = sr / FFT;
  return maxIdx * hzPerBin;
}}

// ── Format Hz nicely ──
function formatHz(hz) {{
  if (hz >= 1000) return (hz / 1000).toFixed(1) + " kHz";
  return Math.round(hz) + " Hz";
}}

const smooth = {{sub:[], low:[], mid:[], high:[]}};
const smoothPeak = {{sub:[], low:[], mid:[], high:[]}};
const SMOOTH_N = 8;

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

// ── Brand profiles ──
const BRAND_PROFILES = {{
  "JBL": {{
    sub: {{ hiTh: 7, loTh: -5 }}, low: {{ hiTh: 5, loTh: -4 }}, mid: {{ hiTh: 4, loTh: -4 }}, high: {{ hiTh: 5, loTh: -4 }},
    subNote:  "JBL tiene bass reflex potente — si suena retumbante puede ser exceso real",
    lowNote:  "Los medios-bajos JBL pueden embarrar si el cuarto es chico",
    midNote:  "La curva JBL+ tiene presencia media alta — cuidado con lo nasal",
    highNote: "JBL puede subir +10 dB en 10 kHz — suena muy brillante en interiores",
  }},
  "Yamaha": {{
    sub: {{ hiTh: 6, loTh: -6 }}, low: {{ hiTh: 6, loTh: -5 }}, mid: {{ hiTh: 4, loTh: -4 }}, high: {{ hiTh: 5, loTh: -5 }},
    subNote:  "Yamaha DXR tiene buen sub pero no es tan profundo — puede faltar pegada",
    lowNote:  "Los DSR/DXR tienden a hinchar medios-bajos a alto volumen",
    midNote:  "Yamaha es fiel en medios — si suena nasal probablemente es la sala",
    highNote: "Yamaha tiene tweeter de titanio — los agudos picados se sienten rápido",
  }},
  "RCF": {{
    sub: {{ hiTh: 6, loTh: -6 }}, low: {{ hiTh: 5, loTh: -5 }}, mid: {{ hiTh: 4, loTh: -4 }}, high: {{ hiTh: 5, loTh: -5 }},
    subNote:  "RCF tiene buen punch en sub pero puede quedarse corto en exteriores",
    lowNote:  "Los medios-bajos RCF son limpios — si suena enlodenado, baja",
    midNote:  "RCF es claro en medios — ideal para voces",
    highNote: "RCF tiene buena extension en agudos — si falta brillo revisa posicion",
  }},
}};

// ── Target EQ center frequencies per band (for practical EQ advice) ──
const EQ_FREQ = {{
  sub:  [50, 80],
  low:  [200, 315],
  mid:  [1000, 2500],
  high: [6000, 10000, 16000]
}};

function getBrandProfile(marca) {{
  return BRAND_PROFILES[marca] || BRAND_PROFILES["JBL"];
}}

function getInstruction(bandId, dbRelative, peakHz, context) {{
  const lugar = context.lugar || "";
  const genero = context.genero || "";
  const marca = context.marca || "JBL";
  const exterior = lugar.includes("aire libre") || lugar.includes("Carpa");

  const profile = getBrandProfile(marca);
  const thresh = profile[bandId] || profile.sub;
  const bandTip = profile[bandId + "Note"] || "";

  // Pick best EQ frequency suggestion based on peak and available EQ points
  const freqs = EQ_FREQ[bandId] || [1000];
  let eqFreq = freqs[0];
  let minDist = Infinity;
  for (const f of freqs) {{
    const dist = Math.abs(f - peakHz);
    if (dist < minDist) {{ minDist = dist; eqFreq = f; }}
  }}
  const freqLabel = eqFreq >= 1000 ? (eqFreq/1000) + " kHz" : eqFreq + " Hz";

  let genreTip = "";
  if (genero === "Salsa") genreTip = "En salsa los graves y medios-bajos son clave para la percusion.";
  else if (genero === "Rock") genreTip = "En rock los medios y graves dan peso a las guitarras.";
  else if (genero === "Clásica") genreTip = "En clásica los medios y agudos deben ser claros y naturales.";

  let status = "ok", action = "", detail = "";
  let color = "#e2e8f0", bg = "rgba(255,255,255,0.04)", border = "#475569";

  // Detail messages per band referencing the peak frequency
  const peakLabel = formatHz(peakHz);
  const details = {{
    sub:  {{ down: "El pico en " + peakLabel + " está muy fuerte — baja ese rango para limpiar el sub", up: "Falta cuerpo en " + peakLabel + " — sube el sub para darle pegada", ok: "Sub equilibrado con pico en " + peakLabel }},
    low:  {{ down: "El pico en " + peakLabel + " está tapando las voces — baja medios-bajos", up: "Falta calidez en " + peakLabel + " — sube medios-bajos para llenar el sonido", ok: "Medios-bajos equilibrados con pico en " + peakLabel }},
    mid:  {{ down: "El pico en " + peakLabel + " hace las voces nasales o metálicas — baja medios", up: "Voces poco claras, falta presencia en " + peakLabel + " — sube medios", ok: "Medios equilibrados con pico en " + peakLabel }},
    high: {{ down: "El pico en " + peakLabel + " suena muy brillante o chillón — baja agudos", up: "Falta brillo y presencia en " + peakLabel + " — sube agudos para definir", ok: "Agudos equilibrados con pico en " + peakLabel }},
  }};

  if (bandId === "sub" && exterior) {{
    status = "warn"; action = "IGNORAR lectura";
    detail = "En exteriores el viento distorsiona los graves — no ajustes basándote en esto";
    color="#f59e0b"; bg="rgba(245,158,11,0.12)"; border="#f59e0b";
  }} else if (dbRelative > thresh.hiTh) {{
    status = "down";
    const dbCut = Math.min(6, Math.max(1, Math.round((dbRelative - thresh.hiTh) / 2)));
    action = "📉 EQ: BAJAR " + dbCut + " dB en " + freqLabel;
    detail = details[bandId].down + (bandTip ? " · " + bandTip : "");
    color="#f87171"; bg="rgba(239,68,68,0.12)"; border="#ef4444";
  }} else if (dbRelative < thresh.loTh) {{
    status = "up";
    const dbBoost = Math.min(6, Math.max(1, Math.round((thresh.loTh - dbRelative) / 2)));
    action = "📈 EQ: SUBIR " + dbBoost + " dB en " + freqLabel;
    detail = details[bandId].up + (bandTip ? " · " + bandTip : "");
    color="#4ade80"; bg="rgba(34,197,94,0.12)"; border="#22c55e";
  }} else {{
    status = "ok"; action = "✅ " + freqLabel + " OK";
    detail = details[bandId].ok + (bandTip ? " · " + bandTip : "");
    color="#e2e8f0"; bg="rgba(255,255,255,0.04)"; border="#475569";
  }}

  let note = "";
  if (genreTip && status !== "warn") note = " 💡 " + genreTip;

  return {{ action, detail, note, color, bg, border, status }};
}}

// ── Canvas spectrum with Hz labels ──
function drawSpectrum(data, sr) {{
  const canvas = document.getElementById("spectrumCanvas");
  if (!canvas) return;
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const w = rect.width;
  const h = 140;
  canvas.width = w * dpr;
  canvas.height = h * dpr;
  canvas.style.height = h + "px";
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);

  ctx.fillStyle = "rgba(0,0,0,0.5)";
  ctx.fillRect(0, 0, w, h);

  const maxFreq = 8000;
  const maxIdx = freqToIndex(maxFreq, sr);
  const usable = Math.min(maxIdx, data.length);
  const barW = Math.max(1, (w / usable) * 1.5);

  // Draw bars
  for (let i = 1; i < usable; i++) {{
    const val = data[i];
    const norm = Math.max(0, Math.min(1, (val + 100) / 100));
    const barH = norm * (h - 20) * 0.95;
    const x = (i / usable) * w;
    const freq = (i / usable) * maxFreq;
    let r, g, b;
    if (freq < 120)        {{ r=239; g=68;  b=68;  }}
    else if (freq < 500)   {{ r=245; g=158; b=11;  }}
    else if (freq < 4000)  {{ r=34;  g=197; b=94;  }}
    else                   {{ r=167; g=139; b=250; }}
    const alpha = 0.4 + norm * 0.6;
    ctx.fillStyle = `rgba(${{r}},${{g}},${{b}},${{alpha}})`;
    ctx.fillRect(x, (h - 20) - barH, barW, barH);
  }}

  // Hz labels
  const hzLabels = [50, 120, 250, 500, 1000, 2000, 4000, 8000];
  ctx.fillStyle = "rgba(255,255,255,0.35)";
  ctx.font = "10px Inter, system-ui, sans-serif";
  ctx.textAlign = "center";
  for (const hz of hzLabels) {{
    const x = (hz / maxFreq) * w;
    const label = hz >= 1000 ? (hz/1000) + "k" : hz + "";
    ctx.fillText(label, x, h - 4);
    ctx.strokeStyle = "rgba(255,255,255,0.06)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h - 18);
    ctx.stroke();
  }}

  // Reference line
  ctx.strokeStyle = "rgba(255,255,255,0.08)";
  ctx.setLineDash([4, 8]);
  ctx.beginPath();
  ctx.moveTo(0, (h-20) * 0.1);
  ctx.lineTo(w, (h-20) * 0.1);
  ctx.stroke();
  ctx.setLineDash([]);

  // "Hz" label
  ctx.fillStyle = "rgba(255,255,255,0.2)";
  ctx.font = "9px Inter, system-ui, sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("Hz", w - 18, h - 4);
}}

// ── Main loop ──
function loop() {{
  const sr = audioCtx.sampleRate;
  const data = new Float32Array(analyser.frequencyBinCount);
  analyser.getFloatFrequencyData(data);

  drawSpectrum(data, sr);
  const eRef = bandEnergy(data, 500, 4000, sr);

  BANDS.forEach(band => {{
    const raw = bandEnergy(data, band.lo, band.hi, sr);
    const rel = smoothVal(band.id, raw - eRef);
    const peakHz = smoothPeakVal(band.id, peakFrequency(data, band.lo, band.hi, sr));
    const pct  = Math.min(100, Math.max(0, (rel + 30) / 50 * 100));

    let barColor = band.color;
    const absR = Math.abs(rel);
    if (absR > 6)      barColor = "#ef4444";
    else if (absR > 3) barColor = "#f59e0b";

    document.getElementById("b_" + band.id).style.height = pct + "%";
    document.getElementById("b_" + band.id).style.background = barColor;
    document.getElementById("g_" + band.id).style.height = pct + "%";
    document.getElementById("g_" + band.id).style.background = barColor;
    document.getElementById("v_" + band.id).textContent = (rel >= 0 ? "+" : "") + rel.toFixed(1) + " dB";
    document.getElementById("p_" + band.id).textContent = "⚡ Pico: " + formatHz(peakHz);

    const inst = getInstruction(band.id, rel, peakHz, CTX);
    const row = document.getElementById("inst_" + band.id);
    row.style.background = inst.bg;
    row.style.borderLeftColor = inst.border;
    row.style.borderLeftWidth = "4px";
    row.style.borderLeftStyle = "solid";

    const textEl = document.getElementById("inst_" + band.id + "_text");
    textEl.innerHTML = '<span style="font-size:14px;font-weight:700;color:' + inst.color + ';">' + inst.action + '</span>' +
      '<br><span style="color:#94a3b8;font-size:13px;">' + inst.detail + inst.note + '</span>';
  }});

  raf = requestAnimationFrame(loop);
}}

async function startListening() {{
  try {{
    stream = await navigator.mediaDevices.getUserMedia({{ audio: true, video: false }});
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = FFT;
    analyser.smoothingTimeConstant = 0.7;
    source  = audioCtx.createMediaStreamSource(stream);
    source.connect(analyser);

    document.getElementById("btnStart").style.display = "none";
    const btnStop = document.getElementById("btnStop");
    btnStop.style.display = "inline-block";
    btnStop.classList.add("listening-active");
    document.getElementById("meters").style.display = "block";
    document.getElementById("spectrumWrap").style.display = "block";
    document.getElementById("instructions").style.display = "block";
    document.getElementById("status").innerHTML = '<span style="color:#4ade80;font-weight:600;">🔴 Escuchando en tiempo real...</span>';

    window.parent.postMessage({{ type: "streamlit:setSize", height: document.body.scrollHeight }}, "*");
    loop();
  }} catch(e) {{
    document.getElementById("status").innerHTML = '<span style="color:#f87171;">❌ No se pudo acceder al micrófono: ' + e.message + '</span>';
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
  document.getElementById("status").innerHTML = '⏸️ Detenido. Volvé a activar para seguir afinando.';

  const canvas = document.getElementById("spectrumCanvas");
  if (canvas) {{
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "rgba(0,0,0,0.5)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
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
components.html(COMPONENT_HTML, height=1100, scrolling=False)
