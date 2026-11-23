/* Interactive figures for the CTS Insight on world models and architecture (Conor Black). */
(function () {
  /* RIBA chart */
  var data = [
    ['Early-stage design visualisation', 56, 0], ['Standards and compliance checking', 40, 0], ['Practice management', 32, 0],
    ['Project briefing', 26, 0], ['Project management', 26, 0], ['Specification and technical design', 24, 0], ['Other', 23, 0],
    ['Product and material selection', 18, 0], ['Interdisciplinary collaboration', 12, 0], ['BIM creation and maintenance', 10, 0],
    ['Building performance simulation', 7, 1], ['Environmental impact modelling', 6, 1]
  ];
  var bars = document.getElementById('riba-bars'), tip = document.getElementById('riba-tip'), max = 60, sorted = false;
  function draw(animate) {
    var rows = data.slice();
    if (sorted) rows.sort(function (a, b) { return a[0].localeCompare(b[0]); });
    bars.innerHTML = '';
    rows.forEach(function (d) {
      var li = document.createElement('li');
      li.className = 'bar-row' + (d[2] ? ' is-predict' : '');
      li.tabIndex = 0;
      li.setAttribute('aria-label', d[0] + ': ' + d[1] + '% of AI-using practices');
      li.innerHTML = '<span class="bar-label">' + d[0] + '</span><span class="bar-track"><span class="bar-fill"></span><span class="bar-value">' + d[1] + '%</span></span>';
      li._d = d;
      bars.appendChild(li);
      var f = li.querySelector('.bar-fill');
      if (animate) { requestAnimationFrame(function () { requestAnimationFrame(function () { f.style.width = (d[1] / max * 85) + '%'; }); }); }
      else { f.style.transition = 'none'; f.style.width = (d[1] / max * 85) + '%'; }
      ['mouseenter', 'focus'].forEach(function (ev) { li.addEventListener(ev, function () { showTip(li); }); });
      ['mouseleave', 'blur'].forEach(function (ev) { li.addEventListener(ev, hideTip); });
      li.addEventListener('click', function () { showTip(li); });
    });
  }
  function showTip(li) {
    var d = li._d, wrapBox = bars.parentNode.getBoundingClientRect(), r = li.querySelector('.bar-fill').getBoundingClientRect();
    tip.innerHTML = '<b>' + d[1] + '%</b>' + d[0] + (d[2] ? '<br><span style="color:#9fc4ba">Predicts how a building will perform</span>' : '') + '<br><span style="color:#b9cade">of practices using AI</span>';
    var left = Math.min(r.right - wrapBox.left + 10, wrapBox.width - 210);
    tip.style.left = Math.max(0, left) + 'px';
    tip.style.top = (r.top - wrapBox.top - 6) + 'px';
    tip.classList.add('show');
  }
  function hideTip() { tip.classList.remove('show'); }
  var drawn = false;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es, ob) { es.forEach(function (e) { if (e.isIntersecting && !drawn) { drawn = true; draw(true); ob.disconnect(); } }); }, { threshold: 0.25 }).observe(bars);
    draw(false); bars.querySelectorAll('.bar-fill').forEach(function (f) { f.style.width = '0'; f.style.transition = ''; });
  } else { draw(false); }
  var hlBtn = document.getElementById('riba-hl');
  hlBtn.addEventListener('click', function () { var on = bars.classList.toggle('hl'); hlBtn.setAttribute('aria-pressed', on); });
  var sortBtn = document.getElementById('riba-sort');
  sortBtn.addEventListener('click', function () { sorted = !sorted; sortBtn.setAttribute('aria-pressed', sorted); sortBtn.textContent = sorted ? 'Sort by share' : 'Sort A–Z'; drawn = true; draw(false); });

  /* V-JEPA 2 frame animation */
  (function () {
    var box = document.getElementById('flip'); if (!box) return;
    var frame = document.getElementById('flip-frame'), ticks = document.getElementById('flip-ticks'), count = document.getElementById('flip-count'), btn = document.getElementById('flip-play');
    var cols = +box.dataset.cols, rows = +box.dataset.rows, n = cols * rows, i = 0, timer = null, reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    for (var r = 0; r < rows; r++) {
      var g = document.createElement('div'); g.className = 'flip__group'; ticks.appendChild(g);
      for (var c = 0; c < cols; c++) { (function (j, grp) { var t = document.createElement('button'); t.type = 'button'; t.className = 'flip__tick'; t.setAttribute('aria-label', 'Trial ' + (Math.floor(j / cols) + 1) + ', frame ' + (j % cols + 1)); t.addEventListener('click', function () { stop(); show(j); }); grp.appendChild(t); })(r * cols + c, g); }
    }
    function show(j) { i = j; var c = j % cols, r = Math.floor(j / cols); frame.style.backgroundPosition = (100 * c / (cols - 1)) + '% ' + (rows > 1 ? 100 * r / (rows - 1) : 0) + '%'; count.textContent = 'Trial ' + (r + 1) + ' · ' + (c + 1) + ' / ' + cols; ticks.querySelectorAll('.flip__tick').forEach(function (t, m) { t.setAttribute('aria-current', m === j); }); }
    function tick() { show((i + 1) % n); timer = setTimeout(tick, i % cols === cols - 1 ? 1600 : 700); }
    function play() { if (timer) return; btn.setAttribute('aria-pressed', 'true'); btn.textContent = 'Pause'; timer = setTimeout(tick, 700); }
    function stop() { clearTimeout(timer); timer = null; btn.setAttribute('aria-pressed', 'false'); btn.textContent = 'Play'; }
    btn.addEventListener('click', function () { if (timer) stop(); else play(); });
    show(0);
    var img = new Image();
    img.onload = function () { frame.style.backgroundImage = 'url("' + box.dataset.src + '")'; box.classList.add('is-loaded'); if (reduce) stop(); else play(); };
    img.onerror = function () { stop(); };
    img.src = box.dataset.src;
  })();

  /* BIM */
  var bimData = {
    door: ['Door, ground-floor entrance', [['IFC class', 'IfcDoor'], ['Type', 'Single-leaf timber door'], ['Fire rating', 'FD30'], ['Acoustic rating', 'Rw 30 dB'], ['Leaf size', '926 × 2040 mm'], ['Ironmongery', 'Hardware set 03'], ['Manufacturer', 'Supplier, product code'], ['Cost', 'Unit rate, cost code'], ['Programme', 'Install date, phase'], ['Maintenance', 'Inspection schedule']]],
    window: ['Curtain wall panel, first floor', [['IFC class', 'IfcWindow'], ['Type', 'Unitised curtain wall panel'], ['Glazing', 'Triple glazed, argon filled'], ['Thermal transmittance', 'U-value 0.8 W/m²K'], ['Solar factor', 'g-value 0.35'], ['Panel size', '1500 × 3000 mm'], ['Manufacturer', 'Supplier, product code'], ['Cost', 'Unit rate, cost code'], ['Maintenance', 'Cleaning and inspection cycle']]],
    wall: ['External wall, east elevation', [['IFC class', 'IfcWall'], ['Type', 'Rainscreen cladding on framing'], ['Fire classification', 'Euroclass A2-s1, d0'], ['Thermal transmittance', 'U-value 0.18 W/m²K'], ['Build-up thickness', '350 mm'], ['Acoustic rating', 'Rw 45 dB'], ['Embodied carbon', 'kgCO₂e per m²'], ['Programme', 'Install date, phase']]],
    slab: ['Floor slab, level 2', [['IFC class', 'IfcSlab'], ['Type', 'Reinforced concrete flat slab'], ['Thickness', '250 mm'], ['Fire resistance', 'REI 90'], ['Imposed load', '2.5 kN/m²'], ['Concrete grade', 'C32/40'], ['Embodied carbon', 'kgCO₂e per m³'], ['Programme', 'Pour sequence, phase']]],
    roof: ['Roof', [['IFC class', 'IfcRoof'], ['Type', 'Flat roof, green roof finish'], ['Thermal transmittance', 'U-value 0.13 W/m²K'], ['Drainage', 'Outlets and falls'], ['Plant zones', 'Area, load allowance'], ['Access', 'Edge protection, access route'], ['Maintenance', 'Inspection schedule']]]
  };
  var order = [['door', 'Door'], ['window', 'Window'], ['wall', 'Wall'], ['slab', 'Floor slab'], ['roof', 'Roof']];
  var chipsBox = document.getElementById('bim-chips'), els = document.querySelectorAll('.bim-el');
  order.forEach(function (o) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'chip'; b.textContent = o[1]; b.dataset.el = o[0];
    b.addEventListener('click', function () { selectEl(o[0]); }); chipsBox.appendChild(b);
  });
  function selectEl(k) {
    var d = bimData[k];
    els.forEach(function (e) { e.classList.toggle('is-sel', e.dataset.el === k); });
    chipsBox.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.el === k); });
    document.getElementById('bim-name').textContent = d[0];
    document.getElementById('bim-rows').innerHTML = d[1].map(function (r) { return '<tr><th scope="row">' + r[0] + '</th><td>' + r[1] + '</td></tr>'; }).join('');
  }
  els.forEach(function (e) {
    e.setAttribute('tabindex', '0'); e.setAttribute('role', 'button'); e.setAttribute('aria-label', 'Select ' + e.dataset.el);
    e.addEventListener('click', function () { selectEl(e.dataset.el); });
    e.addEventListener('keydown', function (ev) { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); selectEl(e.dataset.el); } });
  });
  selectEl('door');
})();

/* Lead slideshow: autoplays, pauses on hover/focus or when the reader takes control */
(function () {
  var root = document.getElementById('lead-ss'); if (!root) return;
  var slides = root.querySelectorAll('.ss-slide'), n = slides.length, idx = 0, timer = null, paused = false, held = false;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var caps = [
    "The Sagrada Família, Barcelona, in April 2026. A century after Gaudí’s death, it is still being built.",
    "A reconstruction of Gaudí’s hanging model for the church at the Colònia Güell. Strings and small weighted bags let gravity find the shape of every arch; turned upside down, the model becomes the building.",
    "The nave’s columns lean and branch like trees to carry the vaults, a structural idea Gaudí first tested at the Colònia Güell.",
    "Inside the Sagrada Família. Less than a tenth of the building existed when Gaudí died in 1926, and most of his models were destroyed in the Spanish Civil War. Architects including Mark Burry have since used aerospace software to recover his geometry from the surviving fragments."
  ];
  var BYSA = '<a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>';
  function credit(file, who) { return '<a href="https://commons.wikimedia.org/wiki/File:' + file + '">' + who + '</a>, ' + BYSA + ', via Wikimedia Commons'; }
  var credits = [
    credit('Sagrada_Fam%C3%ADlia_exterior_Barcelona_2026.jpg', 'Wikipsico43'),
    credit('Maqueta_funicular.jpg', 'Canaan'),
    '<a href="https://www.pexels.com/photo/the-ceiling-of-sagrada-familia-in-barcelona-spain-27348442/">AXP Photography</a>, <a href="https://www.pexels.com/license/">Pexels License</a>, via Pexels',
    credit('Sagrada_Familia_March_2015-10a.jpg', 'Alvesgaspar')
  ];
  var cap = root.querySelector('.ss-caption'), photo = root.querySelector('.ss-photo'), count = root.querySelector('.ss-count'),
      dotsBox = root.querySelector('.ss-dots'), toggle = root.querySelector('.ss-toggle');
  for (var i = 0; i < n; i++) {
    (function (j) {
      var d = document.createElement('button'); d.type = 'button'; d.className = 'ss-dot'; d.setAttribute('aria-label', 'Image ' + (j + 1));
      d.addEventListener('click', function () { go(j); setPaused(true); }); dotsBox.appendChild(d);
    })(i);
  }
  function go(k) {
    idx = (k + n) % n;
    for (var j = 0; j < n; j++) { slides[j].classList.toggle('is-active', j === idx); slides[j].setAttribute('aria-hidden', j === idx ? 'false' : 'true'); }
    cap.textContent = caps[idx]; photo.innerHTML = credits[idx]; count.textContent = (idx + 1) + ' / ' + n;
    dotsBox.querySelectorAll('.ss-dot').forEach(function (d, j) { d.setAttribute('aria-current', j === idx); });
  }
  function schedule() { clearTimeout(timer); timer = null; if (!paused && !held) timer = setTimeout(function () { go(idx + 1); schedule(); }, 5500); }
  function setPaused(p) { paused = p; toggle.textContent = p ? 'Play' : 'Pause'; toggle.setAttribute('aria-pressed', p ? 'true' : 'false'); cap.setAttribute('aria-live', p ? 'polite' : 'off'); schedule(); }
  root.querySelector('.ss-prev').addEventListener('click', function () { go(idx - 1); setPaused(true); });
  root.querySelector('.ss-next').addEventListener('click', function () { go(idx + 1); setPaused(true); });
  toggle.addEventListener('click', function () { setPaused(!paused); });
  root.addEventListener('mouseenter', function () { held = true; schedule(); });
  root.addEventListener('mouseleave', function () { held = false; schedule(); });
  root.addEventListener('focusin', function () { held = true; schedule(); });
  root.addEventListener('focusout', function (e) { if (!root.contains(e.relatedTarget)) { held = false; schedule(); } });
  root.tabIndex = -1;
  root.addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') { go(idx - 1); setPaused(true); } if (e.key === 'ArrowRight') { go(idx + 1); setPaused(true); } });
  var x0 = null;
  root.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  root.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) { go(idx + (dx < 0 ? 1 : -1)); setPaused(true); } x0 = null; });
  go(0);
  setPaused(reduce);
})();
