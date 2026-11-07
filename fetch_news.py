<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ファンダニュース</title>
<style>
body{font-family:-apple-system,sans-serif;margin:0;background:#f5f6f8;color:#111}
h1{font-size:18px;margin:0;padding:14px 16px;background:#0b2545;color:#fff}
nav{display:flex;gap:6px;overflow-x:auto;padding:10px 12px;background:#fff;position:sticky;top:0}
nav button{flex:none;border:1px solid #ccd;background:#fff;border-radius:16px;padding:6px 12px;font-size:14px}
nav button.on{background:#0b2545;color:#fff}
ul{list-style:none;margin:0;padding:8px 12px}
li{background:#fff;border-radius:8px;padding:10px 12px;margin-bottom:8px}
li a{color:#111;text-decoration:none;font-size:15px;line-height:1.4}
li small{display:block;color:#778;margin-top:4px}
#msg,#upd{padding:8px 16px;color:#778;font-size:13px}
</style>
</head>
<body>
<h1>ファンダニュース</h1>
<nav id="tabs"></nav>
<div id="upd"></div>
<div id="msg">読み込み中…</div>
<ul id="list"></ul>
<script>
const tabs=document.getElementById("tabs"),list=document.getElementById("list"),msg=document.getElementById("msg"),upd=document.getElementById("upd");let D={};
const esc=s=>s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const jp=t=>new Date(t).toLocaleString("ja-JP",{timeZone:"Asia/Tokyo",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",hour12:false});
const fmt=t=>t?new Date(t).toISOString().slice(0,16).replace("T"," ")+" UTC（日本時間 "+jp(t)+"）":"";
function show(n,btn){[...tabs.children].forEach(b=>b.classList.remove("on"));btn.classList.add("on");const it=D[n]||[];msg.textContent=it.length?"":"記事がありません";list.innerHTML=it.map(i=>`<li><a href="${esc(i.link)}" target="_blank" rel="noopener">${esc(i.title)}</a><small>${esc(fmt(i.t))}</small></li>`).join("")}
fetch("news.json?"+Date.now()).then(r=>r.json()).then(d=>{D=d;upd.textContent="最終更新（日本時間）: "+jp(d._updated);Object.keys(d).filter(k=>k[0]!=="_").forEach((n,i)=>{const b=document.createElement("button");b.textContent=n;b.onclick=()=>show(n,b);tabs.appendChild(b);if(i===0)show(n,b)})}).catch(()=>{msg.textContent="データを読み込めませんでした"});
</script>
</body>
</html>
