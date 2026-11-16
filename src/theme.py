import streamlit as st


CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap');
:root{--paper:#f2f0e8;--paper-deep:#e8e5da;--ink:#1d2824;--muted:#707a70;--line:#d3d0c4;--map:#203b35;--land:#d9dfc5;--accent:#c3d65b;--rust:#b96748}
.stApp{color:var(--ink);background:radial-gradient(ellipse at 84% 13%,rgba(195,214,91,.12),transparent 23rem),var(--paper)}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.block-container{max-width:940px;padding:2rem 2rem 4rem}
header[data-testid="stHeader"]{background:transparent}
.atlas-masthead{border-top:1px solid var(--ink);border-bottom:1px solid var(--line);padding:.78rem 0;display:flex;justify-content:space-between;align-items:center;gap:1rem;color:var(--ink);font:500 .7rem 'DM Mono',monospace;letter-spacing:.1em;text-transform:uppercase}
.atlas-wordmark{display:inline-flex;align-items:center;gap:.65rem}.atlas-mark{width:1.55rem;height:1.55rem;color:var(--map)}.atlas-edition{color:var(--muted);text-align:right}
.atlas-hero{display:grid;grid-template-columns:minmax(0,1fr) 9rem;align-items:end;gap:1.5rem;padding:clamp(2.4rem,7vw,5.3rem) 0 2rem;border-bottom:1px solid var(--ink)}
.atlas-kicker{margin-bottom:.8rem;color:var(--rust);font:500 .7rem 'DM Mono',monospace;letter-spacing:.16em;text-transform:uppercase}
.atlas-title{max-width:12ch;margin:0;color:var(--ink);font:500 clamp(3rem,8vw,5.9rem)/.92 'Fraunces',Georgia,serif;letter-spacing:-.055em}.atlas-title em{color:var(--map);font-weight:500}
.atlas-deck{max-width:31rem;margin:1.2rem 0 0;color:#515d55;font-size:1rem;line-height:1.65}
.atlas-globe{width:8.3rem;aspect-ratio:1;position:relative;justify-self:end;overflow:hidden;border:1px solid rgba(29,40,36,.28);border-radius:50%;background:linear-gradient(90deg,transparent 49.5%,rgba(29,40,36,.22) 50%,transparent 50.5%),linear-gradient(0deg,transparent 49.5%,rgba(29,40,36,.22) 50%,transparent 50.5%),repeating-radial-gradient(ellipse at center,transparent 0 13px,rgba(29,40,36,.2) 14px 15px,transparent 16px 27px),var(--paper-deep);box-shadow:inset -13px 0 0 rgba(29,40,36,.055)}
.atlas-globe:before{content:'';position:absolute;inset:20% 27% 25% 21%;background:var(--map);clip-path:polygon(14% 5%,43% 0,54% 12%,73% 11%,84% 29%,70% 39%,76% 53%,59% 57%,56% 74%,43% 86%,34% 72%,23% 65%,27% 49%,12% 40%,18% 26%,0 18%);opacity:.92}
.atlas-section-label{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;margin:1.8rem 0 .8rem;color:var(--muted);font:500 .68rem 'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase}.atlas-section-label strong{color:var(--ink);font-weight:500}
div[data-testid="stSelectbox"]>label,div[data-testid="stTextInput"]>label{color:var(--ink);font-weight:600}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{min-height:3.15rem;border:1px solid #aaa99d;border-radius:2px;background:rgba(255,255,255,.42);box-shadow:none}
div[data-baseweb="select"]>div:focus-within,div[data-baseweb="input"]>div:focus-within{border-color:var(--map);box-shadow:0 0 0 2px rgba(32,59,53,.14)}
.stButton>button,button[kind="primary"],.stFormSubmitButton>button,div[data-testid="stFormSubmitButton"] button,button[kind="primaryFormSubmit"]{min-height:3rem;border:1px solid var(--map);border-radius:2px;background:var(--map)!important;color:#fff!important;font:500 .78rem 'DM Mono',monospace;letter-spacing:.08em;text-transform:uppercase;transition:background .16s ease,color .16s ease,transform .16s ease}
.stButton>button:hover,button[kind="primary"]:hover,.stFormSubmitButton>button:hover,div[data-testid="stFormSubmitButton"] button:hover,button[kind="primaryFormSubmit"]:hover{border-color:var(--ink)!important;background:var(--accent)!important;color:var(--ink)!important;transform:translateY(-1px)}
.stButton>button:focus-visible,button[kind="primary"]:focus-visible{outline:3px solid var(--rust);outline-offset:3px}
div[data-testid="stMetric"]{padding:.9rem 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);border-radius:0;background:transparent}div[data-testid="stMetricLabel"]{color:var(--muted);font:500 .65rem 'DM Mono',monospace;letter-spacing:.11em;text-transform:uppercase}div[data-testid="stMetricValue"]{color:var(--ink);font-family:'Fraunces',Georgia,serif}
div[data-testid="stAlert"]{border:1px solid var(--line);border-left:3px solid var(--rust);border-radius:0;background:rgba(255,255,255,.38);color:var(--ink)}hr{border-color:var(--line)}
@media(max-width:640px){.block-container{padding:1.15rem 1rem 2.5rem}.atlas-masthead{font-size:.59rem}.atlas-hero{grid-template-columns:minmax(0,1fr) 5.5rem;gap:.7rem;padding:3rem 0 1.5rem}.atlas-globe{width:5.2rem}.atlas-title{font-size:clamp(2.8rem,13vw,4.3rem)}.atlas-deck{font-size:.92rem}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;transition-duration:.01ms!important}}
"""


def apply_theme() -> None:
    """Apply page-level colors, typography, layout, and control styling."""
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def render_masthead() -> None:
    """Render the Cartogram-inspired masthead and introductory hero."""
    st.markdown(
        """
        <div class="atlas-masthead">
          <span class="atlas-wordmark">
            <svg class="atlas-mark" viewBox="0 0 32 32" fill="none" aria-hidden="true">
              <circle cx="16" cy="16" r="13.5" stroke="currentColor"/>
              <ellipse cx="16" cy="16" rx="6" ry="13" stroke="currentColor"/>
              <path d="M3 16h26M5.5 9.5h21M5.5 22.5h21" stroke="currentColor"/>
              <path d="m19 7-2 5 4 2-3 4 1 6-5-2-2-5 3-3-1-4z" fill="#c3d65b" stroke="currentColor" stroke-linejoin="round"/>
            </svg>
            <span>KRAINALE</span>
          </span>
          <span class="atlas-edition">A game of scale &amp; place</span>
        </div>
        <section class="atlas-hero">
          <div>
            <div class="atlas-kicker">The world, in clues</div>
            <h1 class="atlas-title">Find your place <em>on the map.</em></h1>
            <p class="atlas-deck">One hidden country. Every guess reveals how its land and population compare.</p>
          </div>
          <div class="atlas-globe" role="img" aria-label="Stylized globe with graticule lines"></div>
        </section>
        """,
        unsafe_allow_html=True,
    )
