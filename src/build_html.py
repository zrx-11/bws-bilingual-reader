#!/usr/bin/env python3
"""Build mobile-first offline bilingual study HTML with full e-book reader."""
import json, os

CH_DIR = "/home/user/Doubao/chats/38446786379870466/bws_chapters"
OUT = "/home/user/Doubao/chats/38446786379870466/BWS数学双语学习网页.html"

# Key points data (for skeleton, guide, glossary, rules, quiz tabs)
kp_chapters = []
for i in range(1, 10):
    fs = [f for f in os.listdir(CH_DIR) if f.startswith(f"ch{i:02d}") and f.endswith(".json")]
    kp_chapters.append(json.load(open(os.path.join(CH_DIR, fs[0]))))

# Full e-book data (for e-book tab)
ebook = json.load(open(os.path.join(CH_DIR, "ebook_merged.json")))

DATA_JS = json.dumps({"kp": kp_chapters, "ebook": ebook}, ensure_ascii=False)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>BWS 数学证明写作 · 双语学习</title>
<style>
:root{
  --bg:#fafaf8; --card:#fff; --ink:#1f2328; --muted:#6b7280;
  --line:#e5e7eb; --accent:#2563eb; --accent-light:#dbeafe;
  --def:#7c3aed; --thm:#059669; --ex:#d97706; --strat:#2563eb;
  --warn:#dc2626; --note:#6b7280; --reader-bg:#fdfcf8;
}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
html{font-size:16px;overflow-x:hidden}
body{font-family:-apple-system,"PingFang SC","Microsoft YaHei","Segoe UI",sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.75;font-size:15px;
  padding-bottom:env(safe-area-inset-bottom);overflow-x:hidden;max-width:100vw;word-wrap:break-word;word-break:break-word}
header{background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff;
  padding:14px 16px calc(14px + env(safe-area-inset-top));
  position:sticky;top:0;z-index:100;box-shadow:0 2px 8px rgba(0,0,0,.15)}
header h1{font-size:16px;font-weight:600;line-height:1.4}
header .sub{font-size:11px;opacity:.85;margin-top:2px}
nav{display:flex;gap:0;background:#fff;border-bottom:1px solid var(--line);
  overflow-x:auto;position:sticky;top:0;z-index:99;scrollbar-width:none}
nav::-webkit-scrollbar{display:none}
nav button{background:none;border:none;padding:12px 14px;font-size:13px;cursor:pointer;
  color:var(--muted);border-bottom:2px solid transparent;white-space:nowrap;min-height:44px}
nav button.active{color:var(--accent);border-bottom-color:var(--accent);font-weight:600}
main{max-width:1000px;margin:0 auto;padding:16px}
@media(min-width:768px){main{padding:24px;max-width:900px}}
.tab{display:none}.tab.active{display:block}

/* ebook reader */
#tab-ebook{padding:0;max-width:100%}
.ebook-toolbar{position:sticky;top:0;background:var(--reader-bg);border-bottom:1px solid var(--line);
  padding:10px 16px;display:flex;justify-content:space-between;align-items:center;z-index:50}
.ebook-toolbar button{background:none;border:1px solid var(--line);border-radius:6px;
  padding:8px 14px;font-size:13px;cursor:pointer;min-height:36px}
.ebook-toolbar .title{font-size:13px;font-weight:600;color:var(--muted)}
.ebook-progress{height:2px;background:var(--line);position:fixed;top:0;left:0;z-index:200}
.ebook-progress-bar{height:100%;background:var(--accent);width:0%}
.ebook-content{max-width:700px;margin:0 auto;padding:20px 18px 80px}
.ebook-ch{margin-bottom:40px;scroll-margin-top:80px}
.ebook-ch-title{font-size:22px;font-weight:700;margin:30px 0 6px;line-height:1.3}
.ebook-ch-title .en{display:block;font-size:14px;color:var(--muted);font-weight:400;font-style:italic;margin-top:4px}
.ebook-ch-meta{font-size:11px;color:var(--muted);margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.ebook-sec{margin-bottom:28px;scroll-margin-top:80px}
.ebook-sec-title{font-size:17px;font-weight:600;margin:24px 0 12px;color:#111827}
.ebook-sec-title .en{display:block;font-size:12px;color:var(--muted);font-weight:400;font-style:italic;margin-top:2px}
.ebook-sec-title .pg{font-size:10px;color:var(--muted);font-weight:400;margin-left:6px}
.ep{margin-bottom:14px;padding-bottom:12px;border-bottom:1px dotted var(--line);overflow-wrap:break-word;word-break:break-word}
.ep:last-child{border-bottom:none}
.ep .en{font-size:13px;color:#6b7280;font-style:italic;line-height:1.7;margin-bottom:4px;overflow-wrap:break-word;word-break:break-word}
.ep .zh{font-size:15px;line-height:1.85;color:#1a1a1a;overflow-wrap:break-word;word-break:break-word}
.ep .zh.empty{color:#aaa;font-size:13px;font-style:italic}
.ep .pg{float:right;font-size:10px;color:var(--muted);font-weight:400}
.ebook-drawer{position:fixed;top:0;left:-280px;width:280px;height:100vh;background:#fff;
  z-index:300;transition:left .3s ease;box-shadow:2px 0 12px rgba(0,0,0,.1);overflow-y:auto;padding:20px 0}
.ebook-drawer.open{left:0}
.ebook-drawer h3{padding:0 16px 10px;font-size:14px;border-bottom:1px solid var(--line);margin-bottom:8px}
.ebook-drawer .dch{font-weight:600;padding:8px 16px;font-size:13px;color:#111827}
.ebook-drawer .dsec{padding:6px 16px 6px 28px;font-size:12px;color:var(--muted);cursor:pointer}
.ebook-drawer .dsec:active{background:var(--accent-light)}
.ebook-mask{position:fixed;inset:0;background:rgba(0,0,0,.3);z-index:250;display:none}
.ebook-mask.open{display:block}
.ebook-fab{position:fixed;bottom:20px;right:16px;width:48px;height:48px;border-radius:50%;
  background:var(--accent);color:#fff;border:none;font-size:20px;cursor:pointer;z-index:150;
  box-shadow:0 2px 8px rgba(0,0,0,.2);display:none}
#tab-ebook.active ~ .ebook-fab, .ebook-fab.show{display:block}
.ebook-top-btn{position:fixed;bottom:76px;right:16px;width:48px;height:48px;border-radius:50%;
  background:var(--accent);color:#fff;border:none;font-size:20px;cursor:pointer;z-index:150;
  box-shadow:0 2px 8px rgba(0,0,0,.2);display:none;align-items:center;justify-content:center}
.ebook-top-btn.show{display:flex}

/* other tabs */
.skeleton-chapter{background:var(--card);border:1px solid var(--line);border-radius:8px;margin-bottom:10px;overflow:hidden}
.sk-head{padding:14px 16px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:14px}
.sk-head:hover{background:#f9fafb}
.sk-head .pages{font-size:11px;color:var(--muted);font-weight:400;text-align:right}
.sk-body{padding:0 16px 12px;border-top:1px solid var(--line);display:none}
.skeleton-chapter.open .sk-body{display:block}
.sk-section{padding:8px 0;border-bottom:1px dashed var(--line);font-size:13px}
.sk-section:last-child{border:none}
.sk-section .sid{color:var(--accent);font-weight:600;margin-right:6px}
.sk-section .en{color:var(--muted);font-style:italic;font-size:12px;margin-left:4px}
.guide-layout{display:flex;flex-direction:column}
.guide-toc{display:flex;gap:6px;overflow-x:auto;padding-bottom:10px;scrollbar-width:none}
.guide-toc::-webkit-scrollbar{display:none}
.guide-toc button{flex-shrink:0;padding:8px 12px;background:var(--card);border:1px solid var(--line);
  border-radius:16px;cursor:pointer;font-size:12px;color:var(--muted);min-height:36px}
.guide-toc button.active{border-color:var(--accent);color:var(--accent);background:var(--accent-light);font-weight:600}
@media(min-width:768px){
  .guide-layout{display:grid;grid-template-columns:200px 1fr;gap:20px}
  .guide-toc{position:sticky;top:130px;flex-direction:column;overflow-y:auto;max-height:calc(100vh-150px)}
  .guide-toc button{width:100%;text-align:left;border-radius:6px;min-height:auto}
}
.chapter-block{margin-bottom:30px;scroll-margin-top:120px}
.chapter-title{font-size:18px;font-weight:700;margin-bottom:4px;padding-bottom:8px;border-bottom:2px solid var(--accent)}
.chapter-title .en{font-size:13px;color:var(--muted);font-weight:400;font-style:italic;margin-left:6px}
.chapter-meta{font-size:11px;color:var(--muted);margin-bottom:16px}
.section-title{font-size:15px;font-weight:600;margin:20px 0 10px;color:#111827;scroll-margin-top:120px}
.section-title .sid{color:var(--accent);margin-right:4px}
.section-title .en{font-size:12px;color:var(--muted);font-weight:400;font-style:italic;margin-left:4px}
.kp{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px;margin-bottom:10px}
.kp-type{display:inline-block;font-size:10px;padding:2px 8px;border-radius:10px;color:#fff;margin-bottom:6px;font-weight:600}
.t-def{background:var(--def)} .t-thm{background:var(--thm)} .t-ex{background:var(--ex)}
.t-strategy{background:var(--strat)} .t-warning{background:var(--warn)} .t-note{background:var(--note)}
.kp-page{float:right;font-size:10px;color:var(--muted)}
.kp-en{font-size:13px;color:#4b5563;font-style:italic;margin-bottom:6px;line-height:1.6}
.kp-zh{font-size:14px;line-height:1.7}
.search-box{width:100%;padding:12px 14px;border:1px solid var(--line);border-radius:8px;font-size:15px;margin-bottom:14px;background:var(--card)}
.gloss-item{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:10px 14px;margin-bottom:8px}
.gloss-item .term-en{font-weight:600;color:var(--def);font-size:14px}
.gloss-item .term-zh{font-weight:600;margin-left:6px;font-size:14px}
.gloss-item .note{font-size:12px;color:var(--muted);margin-top:2px}
.gloss-item .page{float:right;font-size:10px;color:var(--muted)}
.rule-item{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--strat);
  border-radius:6px;padding:12px 14px;margin-bottom:10px}
.rule-item .zh{font-weight:500;font-size:14px}
.rule-item .en{font-size:11px;color:var(--muted);font-style:italic;margin-top:4px}
.quiz-card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px;margin-bottom:14px}
.quiz-q{font-weight:600;margin-bottom:10px;font-size:14px}
.quiz-q .en{font-size:11px;color:var(--muted);font-weight:400;font-style:italic;margin-top:2px;display:block}
.quiz-opt{display:block;padding:10px 12px;border:1px solid var(--line);border-radius:6px;margin-bottom:6px;cursor:pointer;font-size:13px}
.quiz-opt:hover{background:#f9fafb}
.quiz-opt.selected{border-color:var(--accent);background:var(--accent-light)}
.quiz-opt.correct{border-color:var(--thm);background:#d1fae5}
.quiz-opt.wrong{border-color:var(--warn);background:#fee2e2}
.quiz-explain{margin-top:10px;padding:10px;background:#f9fafb;border-radius:6px;font-size:12px;display:none}
.quiz-explain.show{display:block}
.quiz-explain .en{color:var(--muted);font-style:italic;font-size:11px;margin-top:4px}
.quiz-jump{display:inline-block;margin-top:8px;font-size:12px;color:var(--accent);cursor:pointer}
.wrong-badge{display:inline-block;background:var(--warn);color:#fff;font-size:10px;padding:1px 6px;border-radius:8px;margin-left:6px}
.note-adder{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px;margin-bottom:16px}
.note-adder textarea{width:100%;min-height:80px;padding:10px;border:1px solid var(--line);border-radius:6px;font-size:14px;font-family:inherit}
.note-adder button{margin-top:8px;padding:10px 20px;background:var(--accent);color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:14px;min-height:44px}
.note-item{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:10px 14px;margin-bottom:8px}
.note-item .meta{font-size:10px;color:var(--muted);margin-bottom:4px}
.note-item .del{float:right;color:var(--warn);cursor:pointer;font-size:12px}
.empty{text-align:center;color:var(--muted);padding:40px 20px;font-size:13px}
.stats{font-size:11px;color:var(--muted);margin-bottom:12px}
</style>
</head>
<body>
<header>
  <h1>数学证明写作双语学习</h1>
  <div class="sub">Sullivan (CMU 2013) · 离线使用 · 笔记/错题仅存本地</div>
</header>
<nav>
  <button data-tab="ebook" class="active">电子书</button>
  <button data-tab="skeleton">骨架</button>
  <button data-tab="guide">导学</button>
  <button data-tab="glossary">术语</button>
  <button data-tab="rules">规则</button>
  <button data-tab="quiz">自检</button>
  <button data-tab="notes">笔记 <span id="noteCount" style="font-size:10px"></span></button>
</nav>
<main>

<div class="tab active" id="tab-ebook">
  <div class="ebook-progress"><div class="ebook-progress-bar" id="ebookBar"></div></div>
  <div class="ebook-toolbar">
    <button onclick="toggleDrawer(true)">☰ 目录</button>
    <div class="title" id="ebookNow">双语对照读本</div>
    <span style="width:60px;display:inline-block"></span>
  </div>
  <div class="ebook-content" id="ebookContent"></div>
</div>
<div class="ebook-mask" id="ebookMask" onclick="toggleDrawer(false)"></div>
<div class="ebook-drawer" id="ebookDrawer">
  <h3>目录</h3>
  <div id="drawerList"></div>
</div>
<button class="ebook-fab" id="ebookFab" onclick="toggleDrawer(true)">☰</button>
<button class="ebook-top-btn" id="ebookTopBtn" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>

<div class="tab" id="tab-skeleton">
  <div class="stats">共 9 章 · <span id="skStats"></span>。点击章节展开。</div>
  <div id="skeletonTree"></div>
</div>
<div class="tab" id="tab-guide">
  <div class="guide-layout">
    <div class="guide-toc" id="guideToc"></div>
    <div class="guide-content" id="guideContent"></div>
  </div>
</div>
<div class="tab" id="tab-glossary">
  <input class="search-box" id="glossSearch" placeholder="搜索术语（中英文均可）…">
  <div id="glossList"></div>
</div>
<div class="tab" id="tab-rules">
  <div class="stats">证明写作行动规则，按章排列。</div>
  <div id="rulesList"></div>
</div>
<div class="tab" id="tab-quiz">
  <div class="stats">共 <span id="quizTotal"></span> 题 · 答错自动记入错题本 · 可跳回原书页码重读。</div>
  <div id="quizList"></div>
</div>
<div class="tab" id="tab-notes">
  <div class="note-adder">
    <div style="font-weight:600;margin-bottom:6px;font-size:14px">添加笔记</div>
    <textarea id="noteText" placeholder="记录你的理解、疑问、证明思路……自动保存在本地。"></textarea>
    <button onclick="addNote()">保存笔记</button>
  </div>
  <div id="notesList"></div>
</div>
</main>

<script>
const DATA = __DATA__;
const KP = DATA.kp;
const EBOOK = DATA.ebook;
const LS_NOTES='bws_notes_v2', LS_WRONG='bws_wrong_v2', LS_EBOOK_POS='bws_ebook_pos_v2';
let notes=JSON.parse(localStorage.getItem(LS_NOTES)||'[]');
let wrongMap=JSON.parse(localStorage.getItem(LS_WRONG)||'{}');

document.querySelectorAll('nav button').forEach(b=>{
  b.onclick=()=>{
    document.querySelectorAll('nav button').forEach(x=>x.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    document.getElementById('tab-'+b.dataset.tab).classList.add('active');
    document.getElementById('ebookFab').classList.toggle('show', b.dataset.tab==='ebook');
    window.scrollTo(0,0);
  };
});

// EBOOK
function renderEbook(){
  let html='';
  EBOOK.forEach(c=>{
    html+=`<div class="ebook-ch" id="eb-ch${c.chapter}">
      <div class="ebook-ch-title">第 ${c.chapter} 章 · ${c.title_zh}<span class="en">${c.title_en}</span></div>
      <div class="ebook-ch-meta">原书 p${c.start_page}–${c.end_page}</div>`;
    c.sections.forEach(s=>{
      html+=`<div class="ebook-sec" id="eb-s${c.chapter}-${s.section_id}">
        <div class="ebook-sec-title">${s.section_id} ${s.title_zh||s.title_en}<span class="en">${s.title_en}</span><span class="pg">p${s.page}</span></div>`;
      s.paragraphs.forEach(kp=>{
        const zh = kp.zh ? `<div class="zh">${esc(kp.zh)}</div>` : `<div class="zh empty">（本段英文原文，中文翻译待补充）</div>`;
        html+=`<div class="ep">
          <span class="pg">p${kp.page}</span>
          <div class="en">${esc(kp.en)}</div>
          ${zh}
        </div>`;
      });
      html+=`</div>`;
    });
    html+=`</div>`;
  });
  document.getElementById('ebookContent').innerHTML=html;
  let dh='<div class="dch">目录</div>';
  EBOOK.forEach(c=>{
    dh+=`<div class="dch">第${c.chapter}章 ${c.title_zh}</div>`;
    c.sections.forEach(s=>{
      dh+=`<div class="dsec" onclick="jumpTo('eb-s${c.chapter}-${s.section_id}')">${s.section_id} ${s.title_zh||s.title_en}</div>`;
    });
  });
  document.getElementById('drawerList').innerHTML=dh;
  setTimeout(()=>{
    const pos=parseInt(localStorage.getItem(LS_EBOOK_POS)||'0');
    if(pos>0) window.scrollTo(0,pos);
  },100);
}
function toggleDrawer(open){
  document.getElementById('ebookDrawer').classList.toggle('open',open);
  document.getElementById('ebookMask').classList.toggle('open',open);
}
function jumpTo(id){
  toggleDrawer(false);
  setTimeout(()=>{document.getElementById(id).scrollIntoView({behavior:'smooth',block:'start'});},300);
}
window.addEventListener('scroll',()=>{
  if(!document.getElementById('tab-ebook').classList.contains('active'))return;
  const h=document.documentElement;
  const pct=(h.scrollTop/(h.scrollHeight-h.clientHeight))*100;
  document.getElementById('ebookBar').style.width=pct+'%';
  localStorage.setItem(LS_EBOOK_POS,h.scrollTop);
  const secs=document.querySelectorAll('.ebook-sec');
  let cur='双语对照读本';
  secs.forEach(s=>{if(s.getBoundingClientRect().top<120)cur=s.querySelector('.ebook-sec-title').textContent.trim().slice(0,20);});
  document.getElementById('ebookNow').textContent=cur;
  const topBtn=document.getElementById('ebookTopBtn');
  if(h.scrollTop>400){topBtn.classList.add('show');}else{topBtn.classList.remove('show');}
},{passive:true});

// SKELETON
function renderSkeleton(){
  let html='',total=0;
  KP.forEach(c=>{
    total+=c.sections.length;
    html+=`<div class="skeleton-chapter" id="sk-ch${c.chapter}">
      <div class="sk-head" onclick="this.parentElement.classList.toggle('open')">
        <span>第${c.chapter}章 · ${c.title_zh}</span>
        <span class="pages">${c.title_en}<br>p${c.start_page}–${c.end_page}</span>
      </div><div class="sk-body">`;
    c.sections.forEach(s=>{
      html+=`<div class="sk-section"><span class="sid">${s.section_id}</span>${s.title_zh}<span class="en">${s.title_en}·p${s.page}</span></div>`;
    });
    html+=`</div></div>`;
  });
  document.getElementById('skStats').textContent=total+'节';
  document.getElementById('skeletonTree').innerHTML=html;
}

// GUIDE
function renderGuide(){
  let tocH='',contentH='';
  KP.forEach(c=>{
    tocH+=`<button onclick="scrollToCh(${c.chapter})">第${c.chapter}章 ${c.title_zh}</button>`;
    contentH+=`<div class="chapter-block" id="ch${c.chapter}">
      <div class="chapter-title">第${c.chapter}章 · ${c.title_zh}<span class="en">${c.title_en}</span></div>
      <div class="chapter-meta">原书 p${c.start_page}–${c.end_page} · ${c.sections.length}节</div>`;
    c.sections.forEach(s=>{
      contentH+=`<div class="section-title"><span class="sid">${s.section_id}</span>${s.title_zh}<span class="en">${s.title_en}·p${s.page}</span></div>`;
      s.key_points.forEach(kp=>{
        const tag={definition:'定义',theorem:'定理',example:'例题',strategy:'策略',warning:'注意',note:'要点'}[kp.type]||kp.type;
        contentH+=`<div class="kp"><span class="kp-type t-${kp.type}">${tag}</span><span class="kp-page">p${kp.page}</span>
          <div class="kp-en">${esc(kp.en)}</div><div class="kp-zh">${esc(kp.zh)}</div></div>`;
      });
    });
    contentH+=`</div>`;
  });
  document.getElementById('guideToc').innerHTML=tocH;
  document.getElementById('guideContent').innerHTML=contentH;
}
function scrollToCh(n){document.getElementById('ch'+n).scrollIntoView({behavior:'smooth'});}

// GLOSSARY
function renderGlossary(f=''){
  let html='';const q=f.trim().toLowerCase();
  KP.forEach(c=>c.glossary.forEach(g=>{
    if(q&&!g.term_en.toLowerCase().includes(q)&&!g.term_zh.includes(q)&&!(g.note_zh||'').includes(q))return;
    html+=`<div class="gloss-item"><span class="page">p${g.page}</span>
      <span class="term-en">${esc(g.term_en)}</span><span class="term-zh">${esc(g.term_zh)}</span>
      <div class="note">${esc(g.note_zh||'')} · 第${c.chapter}章</div></div>`;
  }));
  document.getElementById('glossList').innerHTML=html||'<div class="empty">无匹配术语</div>';
}
document.getElementById('glossSearch').addEventListener('input',e=>renderGlossary(e.target.value));

// RULES
function renderRules(){
  let html='';
  KP.forEach(c=>{
    html+=`<h3 style="margin:16px 0 8px;font-size:14px;color:#374151">第${c.chapter}章 · ${c.title_zh}</h3>`;
    c.action_rules.forEach(r=>{html+=`<div class="rule-item"><div class="zh">${esc(r.zh)}</div><div class="en">${esc(r.en)}</div></div>`;});
  });
  document.getElementById('rulesList').innerHTML=html;
}

// QUIZ
function renderQuiz(){
  let html='',total=0;
  KP.forEach(c=>c.quiz.forEach((q,qi)=>{
    total++;const qid=c.chapter+'-'+qi;const w=wrongMap[qid];
    html+=`<div class="quiz-card"><div class="quiz-q">
      <span class="zh">${esc(q.question_zh)} ${w?`<span class="wrong-badge">错${w.count}次</span>`:''}</span>
      <span class="en">${esc(q.question_en)}</span></div>`;
    q.options.forEach((op,oi)=>{
      html+=`<label class="quiz-opt" id="opt-${qid}-${oi}" onclick="answerQuiz('${qid}',${oi},${q.answer})">
        ${String.fromCharCode(65+oi)}. ${esc(op.zh)} <span style="font-size:11px;color:var(--muted);font-style:italic">${esc(op.en)}</span></label>`;
    });
    html+=`<div class="quiz-explain" id="expl-${qid}">
        <div class="zh"><b>解析：</b>${esc(q.explanation_zh)}</div>
        <div class="en">${esc(q.explanation_en)}</div>
        <span class="quiz-jump" onclick="alert('请回到原书第 ${q.page} 页重读相关内容。')">→ 见原书第 ${q.page} 页</span>
      </div></div>`;
  }));
  document.getElementById('quizTotal').textContent=total;
  document.getElementById('quizList').innerHTML=html;
}
function answerQuiz(qid,chosen,correct){
  for(let i=0;i<6;i++){const el=document.getElementById('opt-'+qid+'-'+i);if(!el)break;el.classList.remove('selected','correct','wrong');}
  document.getElementById('opt-'+qid+'-'+chosen).classList.add('selected');
  document.getElementById('opt-'+qid+'-'+correct).classList.add('correct');
  if(chosen!==correct){
    document.getElementById('opt-'+qid+'-'+chosen).classList.add('wrong');
    if(!wrongMap[qid])wrongMap[qid]={count:0};
    wrongMap[qid].count++;
  }else{
    if(wrongMap[qid]&&wrongMap[qid].count>0){wrongMap[qid].count--;if(wrongMap[qid].count===0)delete wrongMap[qid];}
  }
  localStorage.setItem(LS_WRONG,JSON.stringify(wrongMap));
  document.getElementById('expl-'+qid).classList.add('show');
}

// NOTES
function renderNotes(){
  document.getElementById('noteCount').textContent=notes.length?`(${notes.length})`:'';
  const list=document.getElementById('notesList');
  if(!notes.length){list.innerHTML='<div class="empty">还没有笔记。</div>';return;}
  let html='';
  notes.slice().reverse().forEach(n=>{
    html+=`<div class="note-item"><span class="del" onclick="delNote(${n.id})">删除</span>
      <div class="meta">${new Date(n.ts).toLocaleString('zh-CN')}</div><div>${esc(n.text)}</div></div>`;
  });
  list.innerHTML=html;
}
function addNote(){
  const ta=document.getElementById('noteText');const text=ta.value.trim();
  if(!text)return;
  notes.push({id:Date.now(),text,ts:Date.now()});
  localStorage.setItem(LS_NOTES,JSON.stringify(notes));
  ta.value='';renderNotes();
}
function delNote(id){
  notes=notes.filter(n=>n.id!==id);
  localStorage.setItem(LS_NOTES,JSON.stringify(notes));renderNotes();
}

function esc(s){const d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML;}

renderEbook();
renderSkeleton();
renderGuide();
renderGlossary();
renderRules();
renderQuiz();
renderNotes();
</script>
</body>
</html>
"""

out = TEMPLATE.replace("__DATA__", DATA_JS)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(out)
print("Wrote", OUT, os.path.getsize(OUT), "bytes")
