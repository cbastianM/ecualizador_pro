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
    lugar = st.selectbox("¿Dónde estás?", ["Adentro (salón, club)", "Carpa / toldo", "Alaire libre"])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="config-card">""", unsafe_allow_html=True)
    st.subheader("🎵 La música")
    genero = st.selectbox("¿Qué música va a sonar?", ["Salsa", "Rock", "Clásica"])
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.subheader("🎤 Escuchá en tiempo real")
st.caption("Activá el micrófono, poné la música a volumen de evento y el afinador te dirá qué ajustar.")

ctx = _json.dumps({"lugar": lugar, "genero": genero})

COMPONENT_HTML = f"""
<div id="ecualizador-pro" style="font-family:'Inter',system-ui,sans-serif; overflow:hidden;">

  <div id="btnContainer" style="text-align:center; margin-bottom:20px;">
    <button id="btnStart" onclick="startListening()" class="btn-start">🎙️ Activar micrófono</button>
    <button id="btnStop" onclick="stopListening()" class="btn-stop">⏹ Detener</button>
  </div>

  <div id="spectrumWrap" style="display:none; margin-bottom:20px; background:rgba(0,0,0,0.3); border-radius:14px; padding:14px; border:1px solid rgba(255,255,255,0.06);">
    <div style="font-size:11px; font-weight:600; color:#64748b; margin-bottom:6px; letter-spacing:1px; text-transform:uppercase;">📊 Espectro de frecuencias</div>
    <canvas id="spectrumCanvas" style="width:100%; height:120px; border-radius:8px; display:block;"></canvas>
  </div>

  <div id="meters" style="display:none; margin-bottom:20px;">
    <div class="meters-grid">
      <div id="m_bass" class="meter-card">
        <div class="m-label"><span class="m-dot" style="background:#ef4444;"></span>BAJOS</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_bass"></div><div class="m-bar-glow" id="g_bass"></div></div>
        <div class="m-val" id="v_bass">-- dB</div>
        <div class="m-peak" id="p_bass">⚡ --</div>
        <div class="m-hz">20 – 500 Hz</div>
      </div>
      <div id="m_mid" class="meter-card">
        <div class="m-label"><span class="m-dot" style="background:#22c55e;"></span>MEDIOS</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_mid"></div><div class="m-bar-glow" id="g_mid"></div></div>
        <div class="m-val" id="v_mid">-- dB</div>
        <div class="m-peak" id="p_mid">⚡ --</div>
        <div class="m-hz">500 Hz – 4K Hz</div>
      </div>
      <div id="m_high" class="meter-card">
        <div class="m-label"><span class="m-dot" style="background:#a78bfa;"></span>BRILLO</div>
        <div class="m-bar-wrap"><div class="m-bar" id="b_high"></div><div class="m-bar-glow" id="g_high"></div></div>
        <div class="m-val" id="v_high">-- dB</div>
        <div class="m-peak" id="p_high">⚡ --</div>
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
  .inst-header-row {{ display: grid; grid-template-columns: 80px 1fr 1fr; gap: 8px; margin-bottom: 6px; }}
  .inst-col-band {{ font-size: 10px; font-weight: 700; color: #64748b; letter-spacing: 1px; text-transform: uppercase; }}
  .inst-col-eq, .inst-col-xo {{ font-size: 10px; font-weight: 700; color: #64748b; letter-spacing: 1px; text-transform: uppercase; }}
  .inst-row {{
    display: grid; grid-template-columns: 80px 1fr 1fr; gap: 8px; align-items: start;
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

function formatHz(hz) {{
  if (hz >= 1000) return (hz / 1000).toFixed(1) + " kHz";
  return Math.round(hz) + " Hz";
}}

const smooth = {{bass:[], mid:[], high:[]}};
const smoothPeak = {{bass:[], mid:[], high:[]}};
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

// ── Recommendations ──
function getRecommendations(bandId, level, peakHz, context) {{
  const lugar = context.lugar || "";
  const genero = context.genero || "";
  const exterior = lugar.includes("aire libre") || lugar.includes("Carpa");

  // Independent absolute thresholds (mid is more sensitive)
  let hiTh, loTh;
  if (bandId === "bass") {{ hiTh = -45; loTh = -65; }}
  else if (bandId === "mid") {{ hiTh = -50; loTh = -70; }}
  else {{ hiTh = -48; loTh = -68; }}

  // Crossover cut frequencies (Hz) — shifted based on room and genre
  let xoLowCut, xoMidLow, xoMidHigh, xoHighCut;

  // Base crossover: Low < 80-120 | Mid 80-4000 | High > 4000-8000
  if (genero === "Salsa") {{
    xoLowCut = 40; xoMidLow = 80; xoMidHigh = 5000; xoHighCut = 16000;
  }} else if (genero === "Rock") {{
    xoLowCut = 30; xoMidLow = 100; xoMidHigh = 4000; xoHighCut = 16000;
  }} else {{ // Clasica
    xoLowCut = 50; xoMidLow = 120; xoMidHigh = 6000; xoHighCut = 16000;
  }}

  // Adjust crossover based on room
  if (lugar.includes("aire libre")) {{
    xoLowCut = Math.min(xoLowCut + 10, 60); // cut sub-bass more outdoors
    xoHighCut = 14000; // reduce high extension outdoors
  }} else if (lugar.includes("Carpa")) {{
    xoLowCut = Math.min(xoLowCut + 5, 50);
  }}

  // EQ recommendation
  let eqAction = "", eqColor = "#e2e8f0", eqDetail = "";
  let xoAction = "", xoDetail = "";
  let rowBg = "rgba(0,0,0,0.15)", rowBorder = "#475569";

  // Crossover for each band
  if (bandId === "bass") {{
    xoAction = "Corte bajo: " + xoLowCut + " Hz | Subir hasta " + xoMidLow + " Hz";
    xoDetail = "HPF en " + xoLowCut + " Hz, crossover a medios en " + xoMidLow + " Hz";
  }} else if (bandId === "mid") {{
    xoAction = "Rango: " + xoMidLow + " Hz – " + formatHz(xoMidHigh);
    xoDetail = "Pasar bajos a medios en " + xoMidLow + " Hz, cortar agudos en " + formatHz(xoMidHigh);
  }} else {{
    xoAction = "Corte alto: " + formatHz(xoHighCut) + " | Desde " + formatHz(xoMidHigh);
    xoDetail = "Crossover desde medios en " + formatHz(xoMidHigh) + ", LPF en " + formatHz(xoHighCut);
  }}

  if (bandId === "bass" && exterior) {{
    eqAction = "⚠️ IGNORAR";
    eqDetail = "Viento distorsiona graves en exteriores";
    eqColor = "#f59e0b"; rowBg = "rgba(245,158,11,0.08)"; rowBorder = "#f59e0b";
  }} else if (level > hiTh) {{
    const dbCut = Math.min(6, Math.max(1, Math.round((level - hiTh) / 3)));
    const freqs = bandId === "bass" ? [50, 80, 200] : bandId === "mid" ? [1000, 2500] : [6000, 10000];
    let eqFreq = freqs[0];
    for (const f of freqs) {{ if (Math.abs(f - peakHz) < Math.abs(eqFreq - peakHz)) eqFreq = f; }}
    const freqLabel = eqFreq >= 1000 ? (eqFreq/1000) + " kHz" : eqFreq + " Hz";
    eqAction = "📉 BAJAR " + dbCut + " dB en " + freqLabel;
    eqDetail = "Pico en " + formatHz(peakHz) + " está fuerte";
    eqColor = "#f87171"; rowBg = "rgba(239,68,68,0.08)"; rowBorder = "#ef4444";
  }} else if (level < loTh) {{
    const dbBoost = Math.min(6, Math.max(1, Math.round((loTh - level) / 3)));
    const freqs = bandId === "bass" ? [50, 80, 200] : bandId === "mid" ? [1000, 2500] : [6000, 10000];
    let eqFreq = freqs[0];
    for (const f of freqs) {{ if (Math.abs(f - peakHz) < Math.abs(eqFreq - peakHz)) eqFreq = f; }}
    const freqLabel = eqFreq >= 1000 ? (eqFreq/1000) + " kHz" : eqFreq + " Hz";
    eqAction = "📈 SUBIR " + dbBoost + " dB en " + freqLabel;
    eqDetail = "Nivel bajo en " + formatHz(peakHz);
    eqColor = "#4ade80"; rowBg = "rgba(34,197,94,0.08)"; rowBorder = "#22c55e";
  }} else {{
    eqAction = "✅ OK";
    eqDetail = "Equilibrado en " + formatHz(peakHz);
    eqColor = "#94a3b8"; rowBg = "rgba(255,255,255,0.02)"; rowBorder = "#475569";
  }}

  // Brand tip (RCF internally)
  const tips = {{
    bass: "RCF: buen punch en graves, puede faltar en exteriores",
    mid: "RCF: claro en medios, ideal para voces",
    high: "RCF: buena extension en agudos"
  }};

  return {{ eqAction, eqColor, eqDetail, xoAction, xoDetail, rowBg, rowBorder, tip: tips[bandId] || "" }};
}}

// ── Spectrum ──
function drawSpectrum(data, sr) {{
  const canvas = document.getElementById("spectrumCanvas");
  if (!canvas) return;
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const w = rect.width;
  const h = 120;
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

  const hzLabels = [50, 120, 250, 500, 1000, 2000, 4000, 8000];
  ctx.fillStyle = "rgba(255,255,255,0.35)";
  ctx.font = "10px Inter, system-ui, sans-serif";
  ctx.textAlign = "center";
  for (const hz of hzLabels) {{
    const x = (hz / maxFreq) * w;
    const label = hz >= 1000 ? (hz/1000) + "k" : hz + "";
    ctx.fillText(label, x, h - 3);
    ctx.strokeStyle = "rgba(255,255,255,0.06)"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, drawH - 5); ctx.stroke();
  }}
}}

function loop() {{
  const sr = audioCtx.sampleRate;
  const data = new Float32Array(analyser.frequencyBinCount);
  analyser.getFloatFrequencyData(data);

  drawSpectrum(data, sr);

  BANDS.forEach(band => {{
    const raw = bandEnergy(data, band.lo, band.hi, sr);
    const level = smoothVal(band.id, raw);
    const peakHz = smoothPeakVal(band.id, peakFrequency(data, band.lo, band.hi, sr));
    const pct = Math.min(100, Math.max(0, (level + 100) / 100 * 100));

    // Bar color: use band color normally, yellow/red only when adjusting is needed
    let barColor = band.color;
    const rec = getRecommendations(band.id, level, peakHz, CTX);
    if (rec.eqColor === "#f87171") barColor = "#ef4444";
    else if (rec.eqColor === "#4ade80") barColor = "#22c55e";

    document.getElementById("b_" + band.id).style.height = pct + "%";
    document.getElementById("b_" + band.id).style.background = barColor;
    document.getElementById("g_" + band.id).style.height = pct + "%";
    document.getElementById("g_" + band.id).style.background = barColor;
    document.getElementById("v_" + band.id).textContent = level.toFixed(1) + " dB";
    document.getElementById("p_" + band.id).textContent = "⚡ " + formatHz(peakHz);

    const row = document.getElementById("inst_" + band.id);
    row.style.background = rec.rowBg;
    row.style.borderLeftColor = rec.rowBorder;
    row.style.borderLeftWidth = "4px";
    row.style.borderLeftStyle = "solid";

    // Build row: [BAND] [EQ] [XO]
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
    document.getElementById("status").innerHTML = '<span style="color:#4ade80;font-weight:600;">🔴 Escuchando...</span>';
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
components.html(COMPONENT_HTML, height=1100, scrolling=False)
