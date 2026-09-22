(function () {
  const data = window.SUPPLIER_DATA;
  const colors = { DEVELOP:'#1e6f6a', DIVERSIFY:'#d85b2a', RENEGOTIATE:'#c9952d', PROTECT:'#80909e' };
  const usd = v => '$' + (v / 1e6).toFixed(1) + 'M';
  const pct = v => (v * 100).toFixed(1) + '%';
  const actionText = { DIVERSIFY:'DIVERSIFY / MITIGATE', DEVELOP:'PERFORMANCE DEVELOPMENT', RENEGOTIATE:'COMMERCIAL REVIEW', PROTECT:'PROTECT / MONITOR' };
  const questions = { DIVERSIFY:'Can dependency be reduced without compromising continuity?', DEVELOP:'Which delivery or planning issues are controllable with supplier and logistics owners?', RENEGOTIATE:'Does the commercial context validate a negotiation or specification review?', PROTECT:'What monitoring keeps this relationship appropriately protected?' };
  document.querySelector('#eligible-value').textContent = usd(data.reduce((a,d)=>a+d.line_value_usd,0));
  document.querySelector('#eligible-count').textContent = data.length;
  document.querySelector('#priority-count').textContent = data.filter(d=>d.action!=='PROTECT').length;
  const select = document.querySelector('#supplier');
  data.forEach(d=>select.add(new Option(d.supplier_alias,d.supplier_alias)));
  select.value = 'Supplier 02';
  function panel() {
    const d = data.find(x=>x.supplier_alias===select.value);
    document.querySelector('#hypothesis').textContent = 'REVIEW HYPOTHESIS - ' + actionText[d.action];
    document.querySelector('#why').textContent = d.action==='DIVERSIFY' ? 'High observable risk is paired with material observed value and dependency.' : d.action==='DEVELOP' ? 'A schedule-adherence signal merits performance review.' : d.action==='RENEGOTIATE' ? 'Comparable cohorts identify a commercial screening signal.' : 'Available signals support ongoing monitoring.';
    document.querySelector('#question').textContent = questions[d.action];
    document.querySelector('#observed-value').textContent = usd(d.line_value_usd);
    document.querySelector('#risk-score').textContent = d.observable_risk_score.toFixed(1);
    document.querySelector('#dependency').textContent = pct(d.max_product_dependency);
    document.querySelector('#comparable-lines').textContent = d.comparable_lines;
    [['delivery',d.delivery_risk],['commercial',d.commercial_risk],['dependency-risk',d.dependency_risk]].forEach(([id,v])=>{document.querySelector('#'+id).style.width=v+'%';document.querySelector('#'+id+'-v').textContent=v.toFixed(0);});
  }
  select.addEventListener('change',panel); panel();
  const svg=document.querySelector('#matrix'), W=1000,H=450,L=72,R=28,T=24,B=56;
  const x=v=>L+(W-L-R)*v/100, y=v=>H-B-(H-T-B)*v/160;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  let html=`<line x1="${L}" y1="${H-B}" x2="${W-R}" y2="${H-B}" stroke="#a8b1b7"/><line x1="${L}" y1="${T}" x2="${L}" y2="${H-B}" stroke="#a8b1b7"/>`;
  [0,25,50,75,100].forEach(v=>html+=`<text x="${x(v)}" y="${H-30}" text-anchor="middle" fill="#66737e" font-size="12">${v}</text>`);
  [0,40,80,120,160].forEach(v=>html+=`<text x="${L-10}" y="${y(v)+4}" text-anchor="end" fill="#66737e" font-size="12">${v}</text>`);
  html+=`<text x="${W/2}" y="${H-8}" text-anchor="middle" fill="#66737e" font-size="12">Observable risk score</text><text x="18" y="${H/2}" transform="rotate(-90 18 ${H/2})" text-anchor="middle" fill="#66737e" font-size="12">Observed line-item value (USD m)</text>`;
  const offsets = {'Supplier 07':[8,-9], 'Supplier 09':[8,16], 'Supplier 14':[8,-10], 'Supplier 22':[8,-9], 'Supplier 24':[8,18]};
  data.forEach(d=>{const r=13, off=offsets[d.supplier_alias] || [r+4,4];html+=`<circle cx="${x(d.observable_risk_score)}" cy="${y(d.line_value_usd/1e6)}" r="${r}" fill="${colors[d.action]}" stroke="#fff" stroke-width="2"><title>${d.supplier_alias}: ${usd(d.line_value_usd)} | ${d.action}</title></circle><text x="${x(d.observable_risk_score)+off[0]}" y="${y(d.line_value_usd/1e6)+off[1]}" fill="#17212b" font-size="12">${d.supplier_alias}</text>`});
  svg.innerHTML=html;
})();

