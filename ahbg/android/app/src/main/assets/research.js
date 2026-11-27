"use strict";
function el(tag,text){const n=document.createElement(tag);n.textContent=text;return n;}
async function loadNotebook(){
  const response=await fetch("research.json");if(!response.ok)throw Error("Notebook unavailable");
  const data=await response.json();let index=0;
  function puzzle(){
    const target=data.epac.cases[index];
    document.getElementById("clue").textContent="EPAC recovered "+target.seats.map(s=>s.kind).join(" → ")+". Which named seats preserve that order?";
    const options=document.getElementById("options");options.replaceChildren();
    document.getElementById("answer").textContent="";
    for(const candidate of data.epac.cases){
      const b=el("button",candidate.seats.map(s=>s.name).join(" → "));
      b.onclick=()=>{document.getElementById("answer").textContent=candidate.digest===target.digest?
        "Construction recovered. Origin lineage: "+target.lineage.join(" → "):"Same counts, different seating. Try the other construction.";};
      options.append(b);
    }
  }
  puzzle();document.getElementById("another").onclick=()=>{index=1-index;puzzle();};
  document.getElementById("weave").textContent="Weave recovered "+data.weave.bytes_restored+" bytes. Replaying the restored plans reproduced "+data.weave.replayed.turns+" turns and built "+data.weave.replayed.built.join(", ")+".";
  for(const [key,metric] of Object.entries(data.edcm.measurements)){
    const item=el("details","");item.append(el("summary",key+" · "+metric.name),el("p",metric.meaning));
    for(const arm of metric.arms)item.append(el("strong",String(arm.value)+" · "+arm.board.outcome),el("pre",arm.exact_window));
    item.append(el("p",metric.interpretation_limit));document.getElementById("metrics").append(item);
  }
  const readers=document.getElementById("readers");
  readers.append(el("p",data.uchc.method));
  for(const [name,values] of Object.entries(data.uchc.totals))
    readers.append(el("p",name+" · matched "+values.False+"/"+data.uchc.test_examples_per_reader+" correct; swapped "+values.True+"/"+data.uchc.test_examples_per_reader));
  document.getElementById("a0").textContent="In the separate A0 dispatcher fixture the "+data.a0.roles.join(", ")+" received individual views. The Builder chose "+data.a0.choice+" and was "+data.a0.outcome+".";
}
loadNotebook().catch(e=>{document.getElementById("failure").textContent=e.message;});
