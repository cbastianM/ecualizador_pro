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
    .stHtml iframe { border: none !important; }
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
        Afiná tu sonido en tiempo real · EQ y Crossover
    </p>
</div>
""", unsafe_allow_html=True)
st.divider()

st.markdown("""
<div style="text-align:center; margin-bottom:12px;">
    <span style="background:rgba(59,130,246,0.15); color:#60a5fa; padding:4px 16px; border-radius:20px; font-size:13px; font-weight:600;">
        ⚙️ Configurá tu entorno
    </span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""<div class="config-card">""", unsafe_allow_html=True)
    st.subheader("📍 El lugar")
    lugar = st.selectbox("¿Dónde estás?", ["Adentro (salón, club)", "Carpa / toldo", "Al aire libre"])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="config-card">""", unsafe_allow_html=True)
    st.subheader("🎵 La música")
    genero = st.selectbox("¿Qué música va a sonar?", ["Salsa", "Rock", "Clásica"])
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.subheader("🎤 Escuchá en tiempo real")
st.caption("Activá el micrófono, poné la música a volumen de evento y el afinador te dirá qué ajustar.")

ctx = _json.dumps({"lugar": lugar, "genero": genero}, ensure_ascii=False)

COMPONENT_HTML = f"""
<div id="ecualizador-pro" style="font-family:'Inter',system-ui,sans-serif; overflow:hidden;">

  <div id="btnContainer" style="text-align:center; margin-bottom:20px;">
    <button id="btnStart" onclick="startListening()" class="btn-start">MIC Activar</button>
    <button id="btnStop" onclick="stopListening()" class="btn-stop">STOP Detener</button>
  </div>

  <div id="spectrumWrap" style="display:none; margin-bottom:20px; background:rgba(0,0,0,0.3); border-radius:14px; padding:14px; border:1px solid rgba(255,255,255,0.06);">
    <div style="font-size:11px; font-weight:600; color:#64748b; margin-bottom:6px; letter-spacing:1px; text-transform:uppercase;">ESPECTRO DE FRECUENCIAS</div>
    <canvas id="spectrumCanvas" style="width:100%; height:120px; border-radius:8px; display:block;"></canvas>
  </div>

  <div id="meters" style="display:none; margin-bottom:20px;">
    <div class="meters-grid">
      <div id="m_bass" class="meter-card">
        <div class="m-label"><span class="m-dot" style="background:#ef4444;"></span>BAJOS</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_bass"></div><div class="m-bar-glow" id="g_bass"></div></div>
        <div class="m-val" id="v_bass">-- dB</div>
        <div class="m-peak" id="p_bass">Pico: --</div>
        <div class="m-hz">20 – 500 Hz</div>
      </div>
      <div id="m_mid" class="meter-card">
        <div class="m-label"><span class="m-dot" style="background:#22c55e;"></span>MEDIOS</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_mid"></div><div class="m-bar-glow" id="g_mid"></div></div>
        <div class="m-val" id="v_mid">-- dB</div>
        <div class="m-peak" id="p_mid">Pico: --</div>
        <div class="m-hz">500 Hz – 4K Hz</div>
      </div>
      <div id="m_high" class="meter-card">
        <div class="m-label"><span class="m-dot" style="background:#a78bfa;"></span>BRILLO</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_high"></div><div class="m-bar-glow" id="g_high"></div></div>
        <div class="m-val" id="v_high">-- dB</div>
        <div class="m-peak" id="p_high">Pico: --</div>
        <div class="m-hz">4K – 16K Hz</div>
      </div>
    </div>
  </div>

  <div id="instructions" style="display:none;">
    <div class="inst-header">🎛️ Ajustes recomendados</div>
    <div class="inst-table">
      <div class="inst-header-row">
        <div class="inst-col-band">Banda</div>
        <div class="inst-col-eq">🎚️ Ecualizador</div>
        <div class="inst-col-xo">✂️ Crossover</div>
      </div>
      <div id="inst_bass" class="inst-row"></div>
      <div id="inst_mid"  class="inst-row"></div>
      <div id="inst_high" class="inst-row"></div>
    </div>
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
  .meters-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
  @media (max-width: 480px) {{ .meters-grid {{ grid-template-columns: 1fr; gap: 10px; }} }}
  .meter-card {{
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 14px 10px 12px; text-align: center;
    backdrop-filter: blur(10px); transition: border-color .4s, box-shadow .4s;
  }}
  .meter-card:hover {{ border-color: rgba(255,255,255,0.15); box-shadow: 0 0 30px rgba(59,130,246,0.08); }}
  .m-label {{ font-size: 11px; font-weight: 700; color: #94a3b8; margin-bottom: 8px; letter-spacing: 1.2px; display: flex; align-items: center; justify-content: center; gap: 6px; }}
  .m-dot {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; flex-shrink: 0; }}
  .m-bar-wrap {{ background: rgba(0,0,0,0.4); border-radius: 8px; height: 100px; position: relative; overflow: hidden; }}
  .m-bar {{ position: absolute; bottom: 0; width: 100%; height: 0%; border-radius: 8px; transition: height .12s ease-out, background .4s; z-index: 2; }}
  .m-bar-glow {{ position: absolute; bottom: 0; width: 100%; height: 0%; border-radius: 8px; transition: height .12s ease-out; filter: blur(12px); opacity: 0.5; z-index: 1; }}
  .m-val {{ font-size: 15px; font-weight: 700; margin-top: 6px; color: #e2e8f0; font-variant-numeric: tabular-nums; }}
  .m-peak {{ font-size: 12px; font-weight: 600; color: #60a5fa; margin-top: 2px; }}
  .m-hz {{ font-size: 9px; color: #475569; margin-top: 2px; letter-spacing: .5px; }}
  .inst-header {{ font-size: 12px; font-weight: 700; color: #94a3b8; margin-bottom: 10px; letter-spacing: 1px; text-transform: uppercase; }}
  .inst-table {{ width: 100%; }}
  .inst-header-row {{ display: grid; grid-template-columns: 70px 1fr 1fr; gap: 8px; margin-bottom: 6px; }}
  .inst-col-band {{ font-size: 10px; font-weight: 700; color: #64748b; letter-spacing: 1px; text-transform: uppercase; }}
  .inst-col-eq, .inst-col-xo {{ font-size: 10px; font-weight: 700; color: #64748b; letter-spacing: 1px; text-transform: uppercase; }}
  .inst-row {{
    display: grid; grid-template-columns: 70px 1fr 1fr; gap: 8px; align-items: start;
    padding: 10px 12px; border-radius: 10px; margin-bottom: 8px;
    background: rgba(0,0,0,0.25); border-left: 4px solid #475569;
    transition: all .35s; overflow-wrap: break-word; word-break: break-word;
  }}
  @media (max-width: 480px) {{
    .inst-header-row, .inst-row {{ grid-template-columns: 1fr; gap: 4px; }}
    .inst-col-band, .inst-col-eq, .inst-col-xo {{ display: none; }}
    .inst-row {{ padding: 10px; }}
    .btn-start, .btn-stop {{ width: 100%; margin-left: 0 !important; font-size: 15px; }}
    .btn-stop {{ margin-top: 10px; }}
    #btnContainer {{ display: flex; flex-direction: column; align-items: center; gap: 10px; }}
  }}
  @keyframes pulse {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(220,38,38,0.6); }}
    50%      {{ box-shadow: 0 0 0 12px rgba(220,38,38,0); }}
  }}
  .listening-active {{ animation: pulse 1.8s infinite; }}
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

// ── Audio analysis functions ──
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
  const hzPerBin = sr / FFT;
  return maxIdx * hzPerBin;
}}

// ── Find -3dB rolloff point within a range (from peak going down) ──
function findRolloffPoint(data, loHz, hiHz, sr, direction) {{
  // direction: "low" = find where level drops -3dB below peak going LOW freq
  //            "high" = find where level drops -3dB below peak going HIGH freq
  const peakHz = peakFrequency(data, loHz, hiHz, sr);
  const peakVal = data[freqToIndex(peakHz, sr)] || -100;
  const threshold = peakVal - 3;
  const hzPerBin = sr / FFT;

  if (direction === "low") {{
    const startIdx = freqToIndex(loHz, sr);
    const peakIdx = freqToIndex(peakHz, sr);
    for (let i = peakIdx; i >= startIdx; i--) {{
      if (data[i] <= threshold) return (i + 1) * hzPerBin;
    }}
    return loHz;
  }} else {{
    const endIdx = freqToIndex(hiHz, sr);
    const peakIdx = freqToIndex(peakHz, sr);
    for (let i = peakIdx; i <= endIdx; i++) {{
      if (data[i] <= threshold) return (i - 1) * hzPerBin;
    }}
    return hiHz;
  }}
}}

// ── Find energy minimum between two frequency ranges (= crossover point) ──
function findCrossover(data, fromHz, toHz, sr) {{
  const iLo = freqToIndex(fromHz, sr);
  const iHi = freqToIndex(toHz, sr);
  let minVal = Infinity, minIdx = iLo;
  for (let i = iLo; i <= iHi && i < data.length; i++) {{
    if (data[i] < minVal) {{ minVal = data[i]; minIdx = i; }}
  }}
  const hzPerBin = sr / FFT;
  return minIdx * hzPerBin;
}}

function formatHz(hz) {{
  if (hz >= 1000) return (hz / 1000).toFixed(1) + " kHz";
  return Math.round(hz) + " Hz";
}}

const smooth = {{bass:[], mid:[], high:[]}};
const smoothPeak = {{bass:[], mid:[], high:[]}};
const smoothXo = {{xoLow:[], xoHigh:[]}};
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

function smoothXo(key, val) {{
  smoothXo[key].push(val);
  if (smoothXo[key].length > 12) smoothXo[key].shift();
  return smoothXo[key].reduce((a,b) => a+b, 0) / smoothXo[key].length;
}}

// ── Recommendations with detected crossover ──
function getRecommendations(bandId, level, peakHz, detectedXoLow, detectedXoHigh, context) {{
  const lugar = context.lugar || "";
  const genero = context.genero || "";
  const exterior = lugar.includes("aire libre") || lugar.includes("Carpa");

  // Absolute thresholds (mid more sensitive)
  let hiTh, loTh;
  if (bandId === "bass") {{ hiTh = -45; loTh = -65; }}
  else if (bandId === "mid") {{ hiTh = -50; loTh = -70; }}
  else {{ hiTh = -48; loTh = -68; }}

  // Ideal crossover targets per genre
  let idealXoLow, idealXoHigh;
  if (genero === "Salsa") {{ idealXoLow = 80; idealXoHigh = 5000; }}
  else if (genero === "Rock") {{ idealXoLow = 100; idealXoHigh = 4000; }}
  else {{ idealXoHigh = 6000; idealXoLow = 120; }} // Clasica

  // Adjust for outdoors
  if (exterior) {{ idealXoLow = Math.min(idealXoLow + 10, 60); idealXoHigh = Math.max(idealXoHigh - 500, 3000); }}

  // EQ recommendation
  const freqs = bandId === "bass" ? [50, 80, 200] : bandId === "mid" ? [1000, 2500] : [6000, 10000];
  let eqFreq = freqs[0];
  for (const f of freqs) {{ if (Math.abs(f - peakHz) < Math.abs(eqFreq - peakHz)) eqFreq = f; }}
  const freqLabel = eqFreq >= 1000 ? (eqFreq/1000) + " kHz" : eqFreq + " Hz";

  let eqAction = "", eqColor = "#94a3b8", eqDetail = "", rowBg = "rgba(0,0,0,0.15)", rowBorder = "#475569";

  if (bandId === "bass" && exterior) {{
    eqAction = "! IGNORAR"; eqDetail = "Viento distorsiona graves"; eqColor = "#f59e0b";
    rowBg = "rgba(245,158,11,0.08)"; rowBorder = "#f59e0b";
  }} else if (level > hiTh) {{
    const dbCut = Math.min(6, Math.max(1, Math.round((level - hiTh) / 3)));
    eqAction = "v BAJAR " + dbCut + " dB en " + freqLabel;
    eqDetail = "Pico en " + formatHz(peakHz) + " esta fuerte";
    eqColor = "#f87171"; rowBg = "rgba(239,68,68,0.08)"; rowBorder = "#ef4444";
  }} else if (level < loTh) {{
    const dbBoost = Math.min(6, Math.max(1, Math.round((loTh - level) / 3)));
    eqAction = "^ SUBIR " + dbBoost + " dB en " + freqLabel;
    eqDetail = "Nivel bajo en " + formatHz(peakHz);
    eqColor = "#4ade80"; rowBg = "rgba(34,197,94,0.08)"; rowBorder = "#22c55e";
  }} else {{
    eqAction = "OK"; eqDetail = "Equilibrado en " + formatHz(peakHz);
    eqColor = "#94a3b8";
  }}

  // Crossover recommendation with detected frequencies
  let xoAction = "", xoDetail = "";
  const detectedLow = Math.round(detectedXoLow);
  const detectedHigh = Math.round(detectedXoHigh);
  const idealLow = Math.round(idealXoLow);
  const idealHigh = Math.round(idealXoHigh);

  if (bandId === "bass") {{
    const diff = detectedLow - idealLow;
    if (diff > 30) {{
      xoAction = "v Bajar corte a " + idealLow + " Hz";
      xoDetail = "Detectado: " + detectedLow + " Hz → Ideal: " + idealLow + " Hz. El corte esta alto, los graves se pierden.";
    }} else if (diff < -30) {{
      xoAction = "^ Subir corte a " + idealLow + " Hz";
      xoDetail = "Detectado: " + detectedLow + " Hz → Ideal: " + idealLow + " Hz. Los graves invaden medios.";
    }} else {{
      xoAction = "OK Corte en " + detectedLow + " Hz";
      xoDetail = "HPF " + detectedLow + " Hz (ideal: " + idealLow + " Hz)";
    }}
  }} else if (bandId === "mid") {{
    const diff = detectedLow - idealLow;
    let lowAdvice = "";
    if (diff > 30) {{
      lowAdvice = "Bajar entrada a " + idealLow + " Hz";
    }} else if (diff < -30) {{
      lowAdvice = "Subir entrada a " + idealLow + " Hz";
    }} else {{
      lowAdvice = "Entrada OK en " + detectedLow + " Hz";
    }}
    const diffH = detectedHigh - idealXoHigh;
    let highAdvice = "";
    if (diffH > 500) {{
      highAdvice = "Bajar corte alto a " + formatHz(idealXoHigh);
    }} else if (diffH < -500) {{
      highAdvice = "Subir corte alto a " + formatHz(idealXoHigh);
    }} else {{
      highAdvice = "Corte alto OK en " + formatHz(detectedHigh);
    }}
    xoAction = lowAdvice;
    xoDetail = "Entrada: " + detectedLow + " Hz | Salida: " + formatHz(detectedHigh) + " (ideal: " + idealLow + " Hz – " + formatHz(idealXoHigh) + ")";
  }} else {{
    const diff = detectedHigh - idealXoHigh;
    if (diff > 500) {{
      xoAction = "v Bajar entrada a " + formatHz(idealXoHigh);
      xoDetail = "Detectado: " + formatHz(detectedHigh) + " → Ideal: " + formatHz(idealXoHigh) + ". Agudos entran muy tarde.";
    }} else if (diff < -500) {{
      xoAction = "^ Subir entrada a " + formatHz(idealXoHigh);
      xoDetail = "Detectado: " + formatHz(detectedHigh) + " → Ideal: " + formatHz(idealXoHigh) + ". Agudos invaden medios.";
    }} else {{
      xoAction = "OK Entrada en " + formatHz(detectedHigh);
      xoDetail = "Crossover desde " + formatHz(detectedHigh) + " (ideal: " + formatHz(idealXoHigh) + ")";
    }}
  }}

  return {{ eqAction, eqColor, eqDetail, xoAction, xoDetail, rowBg, rowBorder }};
}}

// ── Spectrum ──
function drawSpectrum(data, sr) {{
  const canvas = document.getElementById("spectrumCanvas");
  if (!canvas) return;
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const w = rect.width; const h = 120;
  canvas.width = w * dpr; canvas.height = h * dpr; canvas.style.height = h + "px";
  const ctx = canvas.getContext("2d"); ctx.scale(dpr, dpr);
  ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(0, 0, w, h);

  const maxFreq = 8000;
  const maxIdx = freqToIndex(maxFreq, sr);
  const usable = Math.min(maxIdx, data.length);
  const barW = Math.max(1, (w / usable) * 1.5);
  const drawH = h - 18;

  for (let i = 1; i < usable; i++) {{
    const val = data[i];
    const norm = Math.max(0, Math.min(1, (val + 100) / 100));
    const barH = norm * drawH * 0.95;
    const x = (i / usable) * w;
    const freq = (i / usable) * maxFreq;
    let r, g, b;
    if (freq < 500)       {{ r=239; g=68;  b=68;  }}
    else if (freq < 4000) {{ r=34;  g=197; b=94;  }}
    else                  {{ r=167; g=139; b=250; }}
    const alpha = 0.4 + norm * 0.6;
    ctx.fillStyle = `rgba(${{r}},${{g}},${{b}},${{alpha}})`;
    ctx.fillRect(x, drawH - barH, barW, barH);
  }}

  // Draw crossover lines
  const xoLowX = (smoothXo.xoLow.length > 0 ? smoothXo.xoLow[smoothXo.xoLow.length-1] : 80) / maxFreq * w;
  const xoHighX = (smoothXo.xoHigh.length > 0 ? smoothXo.xoHigh[smoothXo.xoHigh.length-1] : 4000) / maxFreq * w;
  ctx.setLineDash([6, 4]);
  ctx.lineWidth = 2;
  ctx.strokeStyle = "#f59e0b";
  ctx.beginPath(); ctx.moveTo(xoLowX, 0); ctx.lineTo(xoLowX, drawH - 5); ctx.stroke();
  ctx.strokeStyle = "#a78bfa";
  ctx.beginPath(); ctx.moveTo(xoHighX, 0); ctx.lineTo(xoHighX, drawH - 5); ctx.stroke();
  ctx.setLineDash([]);

  // Hz labels
  const hzLabels = [50, 120, 250, 500, 1000, 2000, 4000, 8000];
  ctx.fillStyle = "rgba(255,255,255,0.35)"; ctx.font = "10px Inter, system-ui, sans-serif"; ctx.textAlign = "center";
  for (const hz of hzLabels) {{
    const x = (hz / maxFreq) * w;
    const label = hz >= 1000 ? (hz/1000) + "k" : hz + "";
    ctx.fillText(label, x, h - 3);
  }}
}}

function loop() {{
  const sr = audioCtx.sampleRate;
  const data = new Float32Array(analyser.frequencyBinCount);
  analyser.getFloatFrequencyData(data);

  // Detect crossover points (energy minimums between bands)
  const rawXoLow = findCrossover(data, 200, 800, sr);   // Bass↔Mid crossover
  const rawXoHigh = findCrossover(data, 3000, 6000, sr);  // Mid↔High crossover
  const xoLow = smoothXo("xoLow", rawXoLow);
  const xoHigh = smoothXo("xoHigh", rawXoHigh);

  drawSpectrum(data, sr);

  BANDS.forEach(band => {{
    const raw = bandEnergy(data, band.lo, band.hi, sr);
    const level = smoothVal(band.id, raw);
    const peakHz = smoothPeakVal(band.id, peakFrequency(data, band.lo, band.hi, sr));
    const pct = Math.min(100, Math.max(0, (level + 100) / 100 * 100));

    const rec = getRecommendations(band.id, level, peakHz, xoLow, xoHigh, CTX);

    let barColor = band.color;
    if (rec.eqColor === "#f87171") barColor = "#ef4444";
    else if (rec.eqColor === "#4ade80") barColor = "#22c55e";

    document.getElementById("b_" + band.id).style.height = pct + "%";
    document.getElementById("b_" + band.id).style.background = barColor;
    document.getElementById("g_" + band.id).style.height = pct + "%";
    document.getElementById("g_" + band.id).style.background = barColor;
    document.getElementById("v_" + band.id).textContent = level.toFixed(1) + " dB";
    document.getElementById("p_" + band.id).textContent = "Pico: " + formatHz(peakHz);

    const row = document.getElementById("inst_" + band.id);
    row.style.background = rec.rowBg;
    row.style.borderLeftColor = rec.rowBorder;
    row.style.borderLeftWidth = "4px";
    row.style.borderLeftStyle = "solid";

    const bandNames = {{ bass: "BAJOS", mid: "MEDIOS", high: "BRILLO" }};
    const bandColors = {{ bass: "#ef4444", mid: "#22c55e", high: "#a78bfa" }};

    row.innerHTML = '<div style="font-size:11px;font-weight:700;color:' + bandColors[band.id] + ';letter-spacing:1px;padding-top:2px;">' + bandNames[band.id] + '</div>'
      + '<div><span style="font-size:13px;font-weight:700;color:' + rec.eqColor + ';">' + rec.eqAction + '</span><br><span style="font-size:12px;color:#94a3b8;">' + rec.eqDetail + '</span></div>'
      + '<div><span style="font-size:13px;font-weight:700;color:#60a5fa;">' + rec.xoAction + '</span><br><span style="font-size:12px;color:#94a3b8;">' + rec.xoDetail + '</span></div>';
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
    source = audioCtx.createMediaStreamSource(stream);
    source.connect(analyser);

    document.getElementById("btnStart").style.display = "none";
    const btnStop = document.getElementById("btnStop");
    btnStop.style.display = "inline-block";
    btnStop.classList.add("listening-active");
    document.getElementById("meters").style.display = "block";
    document.getElementById("spectrumWrap").style.display = "block";
    document.getElementById("instructions").style.display = "block";
    document.getElementById("status").innerHTML = '<span style="color:#4ade80;font-weight:600;">O Escuchando...</span>';
    window.parent.postMessage({{ type: "streamlit:setSize", height: document.body.scrollHeight }}, "*");
    loop();
  }} catch(e) {{
    document.getElementById("status").innerHTML = '<span style="color:#f87171;">❌ Micrófono: ' + e.message + '</span>';
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
  document.getElementById("status").innerHTML = '⏸️ Detenido.';
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
components.html(COMPONENT_HTML, height=1150, scrolling=False)
