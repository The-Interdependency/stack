"use strict";
const byId = id => document.getElementById(id);
const names = {environment:"Seeded environment", smol:"SmolLM2 local agent", granite:"Granite local agent", duel:"Private multiplayer"};
const faunaNames = {environment:"Seeded", smol:"SmolLM2", granite:"Granite"};
for (const id of ["fauna", "fork-fauna"]) {
  for (const [value, label] of Object.entries(faunaNames)) byId(id).add(new Option(label, value));
}
let room = null, state = null, unit = null, busy = false;
let orders = {}, messages = {}, camera = null, base = null;
const nameOf = id => ({builder:"Builder",explorer:"Explorer",rival:"Rival builder",fauna:"Fauna"})[id] || id;
const tileName = id => id === "CENTER" ? "Center" : id.replace("RING_", "Ring ");
const actionName = a => (a.action === "construct" ? "Build " : "Move to ") + tileName(a.to_tile_id);
const say = text => { byId("status").textContent = text; };
const draftKey = () => "ahbg/draft/" + room + "/" + state.observation.turn;
const saveDraft = () => localStorage.setItem(draftKey(), JSON.stringify({orders, messages}));
function button(text, click) {
  const b = document.createElement("button");
  b.type = "button"; b.textContent = text; b.addEventListener("click",click); return b;
}
async function api(path, data) {
  const init = {credentials:"same-origin",cache:"no-store"};
  if (data !== undefined) Object.assign(init,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
  const response = await fetch("/api/"+path,init);
  const payload = await response.json();
  if (!response.ok) throw Error(payload.error || "Connection failed");
  return payload;
}
async function run(fn) {
  if (busy) return;
  busy = true; byId("commit").disabled = true;
  try { await fn(); } catch (error) { say(error.message + ". You can retry."); }
  finally { busy=false; if (state) drawOrders(); }
}
async function listPlanes() {
  const rows = (await api("rooms")).rooms;
  const saved = byId("saved"); saved.replaceChildren();
  if (rows.length) {
    const title = document.createElement("h3"); title.textContent="Resume a plane"; saved.append(title);
    rows.forEach(r=>saved.append(button(names[r.mode]+" · "+r.id.slice(-6),()=>run(()=>openPlane(r.id)))));
  }
}
async function openPlane(id) {
  const next = await api("rooms/"+id+"/state");
  const change = !state || room!==id || state.observation.turn!==next.observation.turn;
  room=id; state=next; localStorage.setItem("ahbg/current",room);
  byId("lobby").hidden=true; byId("game").hidden=false;
  if (change) {
    const draft=JSON.parse(localStorage.getItem(draftKey()) || "{}");
    orders=draft.orders||{}; messages=draft.messages||{};
    if (!state.observation.owned.includes(unit)) unit=state.observation.owned[0];
    camera=null;
    byId("fork-fauna").value="";
  }
  if (state.own_commit) {
    orders=Object.fromEntries(state.own_commit.intents.map(a=>[a.unit_id,a]));
    messages=state.own_commit.messages||{};
  }
  draw();
}
function draw() {
  const o=state.observation, p=o.presentation;
  const previous=state.history.at(-1)||[];
  p.motions=previous.filter(e=>e.kind==="move" && p.units.some(u=>u.id===e.unit_id && u.tile===e.to_tile_id))
    .map(e=>({unit:e.unit_id,from:e.from_tile_id,to:e.to_tile_id}));
  render(validateSnapshot(p));
  const svg=byId("board");
  base=svg.getAttribute("viewBox").split(" ").map(Number);
  if (!camera) camera=[...base];
  setCamera();
  svg.querySelectorAll(".unit").forEach((n,i)=>n.classList.toggle("mine",o.owned.includes(p.units[i].id)));
  svg.querySelectorAll(".unit-label").forEach((n,i)=>{ n.textContent=nameOf(p.units[i].id)[0]; });
  svg.querySelectorAll(".tile-point").forEach(n=>{
    n.classList.toggle("built",o.built.includes(n.dataset.tile));
    n.classList.toggle("fog",!o.visible.includes(n.dataset.tile));
  });
  byId("heading").textContent="Turn "+Math.min(o.turn+1,state.turn_limit)+" / "+state.turn_limit;
  byId("opponent").textContent=names[state.mode]+" · "+faunaNames[state.fauna_mode]+" fauna · "+state.seat+" seat · "+room.slice(-6);
  byId("phase").textContent=state.done?"Complete":state.committed?"Orders committed":"Planning";
  byId("share").hidden=!state.waiting_join || state.seat!=="amber";
  byId("fork-panel").hidden=state.mode==="duel";
  const turns=byId("fork-turn"); turns.replaceChildren();
  for (let i=0;i<=o.turn && i<state.turn_limit;i++) turns.add(new Option("Turn "+(i+1),i));
  if(turns.length) turns.selectedIndex=turns.length-1;
  const history=byId("history"); history.replaceChildren();
  state.history.forEach((events,idx)=>{
    const row=document.createElement("li");
    const descriptions=events.map(e=>nameOf(e.unit_id)+" "+({move:"moved to",construct:"built on",war:"contested",build_refused:"could not build on"})[e.kind]+" "+tileName(e.to_tile_id)+(e.kind==="war"?" · "+e.resolution.replaceAll("_"," "):""));
    row.textContent="Turn "+(idx+1)+" · "+(descriptions.join(" / ")||"No visible changes"); history.prepend(row);
  });
  drawOrders();
}
function drawOrders() {
  const o=state.observation, locked=busy||state.committed||state.done;
  const units=byId("units"); units.replaceChildren();
  for(const id of o.owned) {
    const b=button(nameOf(id),()=>{unit=id; drawOrders();});
    b.setAttribute("aria-pressed",String(unit===id)); units.append(b);
  }
  byId("budget").textContent=Object.keys(orders).length+" / "+o.owned.length+" slots";
  byId("utext").textContent=nameOf(unit)+" · one order this turn";
  const target=byId("actions"); target.replaceChildren();
  for(const a of o.legal.filter(a=>a.unit_id===unit)) {
    const b=button(actionName(a),()=>{orders[unit]=a;saveDraft();drawOrders();});
    b.disabled=locked;
    b.setAttribute("aria-pressed",String(orders[unit]?.to_tile_id===a.to_tile_id && orders[unit]?.action===a.action));
    target.append(b);
  }
  byId("message").value=messages[unit]||""; byId("message").disabled=locked;
  const pending=byId("draft"); pending.replaceChildren();
  for(const id of o.owned) {
    const row=document.createElement("p");
    row.append(nameOf(id)+" · "+(orders[id]?actionName(orders[id]):"Hold"));
    if (orders[id]) {
      const undo=button("Cancel",()=>{delete orders[id];saveDraft();drawOrders();});
      undo.disabled=locked; row.append(undo);
    }
    pending.append(row);
  }
  const commit=byId("commit"); commit.disabled=locked;
  commit.textContent=state.done?"Campaign complete":state.committed?"Waiting for the other seat":busy?"Resolving…":"Commit plan";
}
byId("message").oninput=()=>{
  const text=Array.from(byId("message").value).slice(0,256).join("");
  messages[unit]=text; byId("message").value=text; saveDraft();
};
byId("create").onclick=()=>run(async()=>{
  const newRoom=await api("rooms",{mode:byId("mode").value,fauna_mode:byId("fauna").value || undefined,request_id:crypto.randomUUID()});
  byId("invite-code").textContent=newRoom.invite||"";
  await openPlane(newRoom.room); say("");
});
byId("join").onclick=()=>run(async()=>{const r=await api("join",{invite:byId("code").value.trim()});await openPlane(r.room);say("");});
byId("planes").onclick=()=>run(async()=>{await listPlanes();state=null;room=null;localStorage.removeItem("ahbg/current");byId("game").hidden=true;byId("lobby").hidden=false;say("");});
byId("invite").onclick=()=>run(async()=>{const r=await api("rooms/"+room+"/invite",{});byId("invite-code").textContent=r.invite;});
byId("commit").onclick=()=>run(async()=>{
  const key=draftKey();
  const payload={session_id:room,turn:state.observation.turn,intents:Object.values(orders),messages};
  say("Submitting orders…");
  await api("rooms/"+room+"/plan",payload);
  localStorage.removeItem(key); await openPlane(room);
  say(state.committed?"Plan received. Waiting for the other seat.":"Turn resolved and saved.");
});
byId("refresh").onclick=()=>run(()=>openPlane(room));
byId("fork").onclick=()=>run(async()=>{
  const result=await api("rooms/"+room+"/fork",{turn:Number(byId("fork-turn").value),
    fauna_mode:byId("fork-fauna").value || undefined,request_id:crypto.randomUUID()});
  await openPlane(result.room);say("Fork opened. The next agent decision runs fresh.");
});
byId("board").addEventListener("tile-selected",e=>{
  const here=state.observation.field.units.find(u=>u.tile_id===e.detail && state.observation.owned.includes(u.unit_id));
  if(here){unit=here.unit_id;drawOrders();}
});
function setCamera(){if(camera) byId("board").setAttribute("viewBox",camera.join(" "));}
function zoom(factor){
  if(!camera)return;
  const width=Math.min(base[2]*2,Math.max(base[2]/4,camera[2]*factor));
  const height=width*base[3]/base[2];
  camera=[camera[0]+(camera[2]-width)/2,camera[1]+(camera[3]-height)/2,width,height];setCamera();
}
byId("plus").onclick=()=>zoom(.8);byId("minus").onclick=()=>zoom(1.25);
byId("fit").onclick=()=>{camera=[...base];setCamera();};
const pointers=new Map(); let span=0;
const map=byId("board");
map.addEventListener("pointerdown",e=>{pointers.set(e.pointerId,[e.clientX,e.clientY]);});
map.addEventListener("pointermove",e=>{
  if (!pointers.has(e.pointerId)||!camera)return;
  const last=pointers.get(e.pointerId); pointers.set(e.pointerId,[e.clientX,e.clientY]);
  if(pointers.size===2){
    const [a,b]=[...pointers.values()];const distance=Math.hypot(a[0]-b[0],a[1]-b[1]);
    if(span>0&&distance>0)zoom(span/distance);span=distance;
  }else{
    const scale=camera[2]/map.clientWidth;
    camera[0]-=(e.clientX-last[0])*scale;camera[1]-=(e.clientY-last[1])*scale;setCamera();
  }
});
for(const name of ["pointerup","pointercancel","pointerleave"])map.addEventListener(name,e=>{pointers.delete(e.pointerId);span=0;});
window.addEventListener("online",()=>{if(!busy)run(async()=>{
  await api("identity",{}); const saved=room||localStorage.getItem("ahbg/current");
  if(saved)await openPlane(saved);else await listPlanes();
});});
setInterval(()=>{if(!document.hidden&&state?.committed&&!busy)run(()=>openPlane(room));},4000);
run(async()=>{
  await api("identity",{}); const last=localStorage.getItem("ahbg/current");
  if(last){try{await openPlane(last);return;}catch(e){say(e.message);}}
  await listPlanes();
});
