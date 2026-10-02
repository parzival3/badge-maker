/* Badge Maker — builds A4 sheets of name badges entirely in the browser. */

(function () {
  'use strict';

  // A4 is 210 x 297 mm. Each preset tiles the sheet edge to edge and the grid
  // is centred, so the sheet margins fall out of the arithmetic: three 70 mm
  // columns span the full 210 mm with no side margin at all, and eight 37 mm
  // rows leave 0.5 mm top and bottom.
  var SIZES = {
    '85x54': { w: 85, h: 54, cols: 2, rows: 5 },
    '90x54': { w: 90, h: 54, cols: 2, rows: 5 },
    '70x37': { w: 70, h: 37, cols: 3, rows: 8 }
  };
  var STORE_KEY = 'badge-maker/v1';

  var el = {
    names: document.getElementById('names'),
    file: document.getElementById('file'),
    fileHint: document.getElementById('fileHint'),
    showSub: document.getElementById('showSub'),
    showMarks: document.getElementById('showMarks'),
    showRuler: document.getElementById('showRuler'),
    uniform: document.getElementById('uniform'),
    topMargin: document.getElementById('topMargin'),
    safe: document.getElementById('safe'),
    marginHint: document.getElementById('marginHint'),
    size: document.getElementById('size'),
    customSize: document.getElementById('customSize'),
    cw: document.getElementById('cw'),
    ch: document.getElementById('ch'),
    ccols: document.getElementById('ccols'),
    crows: document.getElementById('crows'),
    fitHint: document.getElementById('fitHint'),
    count: document.getElementById('count'),
    print: document.getElementById('print'),
    preview: document.getElementById('preview')
  };

  // The chosen size, either a preset or whatever is typed into the custom boxes.
  function topMargin() {
    var v = el.topMargin.value.trim();
    return v === '' ? null : Math.max(0, parseFloat(v) || 0);
  }

  function currentSize() {
    var id = el.size.value;
    if (id !== 'custom') return SIZES[id];
    return {
      w: parseFloat(el.cw.value) || 70,
      h: parseFloat(el.ch.value) || 37,
      cols: parseInt(el.ccols.value, 10) || 1,
      rows: parseInt(el.crows.value, 10) || 1
    };
  }

  /* ---------- input parsing ---------- */

  // One person per line. Everything after the FIRST comma is the role,
  // so "Doe, Jane" becomes name "Doe" + role "Jane" — use the spreadsheet
  // upload when names contain commas.
  function parsePeople(text) {
    return text.split('\n').map(function (line) {
      var raw = line.trim();
      if (!raw) return null;
      var at = raw.indexOf(',');
      if (at === -1) return { name: raw, sub: '' };
      return { name: raw.slice(0, at).trim(), sub: raw.slice(at + 1).trim() };
    }).filter(Boolean);
  }

  var NAME_HEADER = /^(name|full ?name|nome|nom|naam)$/i;
  var SUB_HEADER = /^(role|title|job ?title|position|department|dept|team|ruolo|organisation|organization)$/i;

  // Rows come from SheetJS as arrays of cell values. Returns "Name, Role" lines.
  function rowsToLines(rows) {
    if (!rows.length) return '';

    var nameCol = 0;
    var subCol = 1;
    var body = rows;

    var head = (rows[0] || []).map(function (c) { return String(c == null ? '' : c).trim(); });
    var headNameAt = head.findIndex(function (c) { return NAME_HEADER.test(c); });
    if (headNameAt !== -1) {
      nameCol = headNameAt;
      var headSubAt = head.findIndex(function (c) { return SUB_HEADER.test(c); });
      subCol = headSubAt === -1 ? -1 : headSubAt;
      body = rows.slice(1);
    }

    return body.map(function (row) {
      var name = String(row[nameCol] == null ? '' : row[nameCol]).trim();
      if (!name) return null;
      var sub = subCol === -1 ? '' : String(row[subCol] == null ? '' : row[subCol]).trim();
      // strip commas from the name so the round-trip through the textarea
      // doesn't re-split it in the wrong place
      name = name.replace(/,/g, ' ').replace(/\s+/g, ' ');
      return sub ? name + ', ' + sub : name;
    }).filter(Boolean).join('\n');
  }

  function loadFile(file) {
    var reader = new FileReader();
    reader.onload = function (e) {
      var lines;
      try {
        var wb = XLSX.read(new Uint8Array(e.target.result), { type: 'array' });
        var sheet = wb.Sheets[wb.SheetNames[0]];
        var rows = XLSX.utils.sheet_to_json(sheet, { header: 1, blankrows: false, raw: false });
        lines = rowsToLines(rows);
      } catch (err) {
        el.fileHint.textContent = 'Could not read that file: ' + err.message;
        return;
      }
      if (!lines) {
        el.fileHint.textContent = 'No names found in the first sheet of ' + file.name + '.';
        return;
      }
      el.names.value = lines;
      el.fileHint.textContent = 'Loaded ' + lines.split('\n').length + ' names from ' + file.name +
        '. Edit them in the box above if needed.';
      render();
    };
    reader.readAsArrayBuffer(file);
  }

  /* ---------- rendering ---------- */

  function makeBadge(person, showSub) {
    var badge = document.createElement('div');
    badge.className = 'badge' + (person ? '' : ' empty');

    var logo = document.createElement('img');
    logo.className = 'badge-logo';
    logo.src = 'assets/logo.svg';
    logo.alt = '';
    badge.appendChild(logo);

    var main = document.createElement('div');
    main.className = 'badge-main';

    var box = document.createElement('div');
    box.className = 'badge-name-box';
    var name = document.createElement('div');
    name.className = 'badge-name';
    name.textContent = person ? person.name : 'placeholder';
    box.appendChild(name);
    main.appendChild(box);

    // When anyone on the sheet has a role, every badge reserves the line, so
    // names sit at the same height from badge to badge.
    if (showSub) {
      var sub = document.createElement('div');
      sub.className = 'badge-sub';
      sub.textContent = (person && person.sub) || ' ';
      main.appendChild(sub);
    }

    badge.appendChild(main);
    return badge;
  }

  // Pick the largest font size at which the name still fits the space the logo
  // and role line leave behind. The name may wrap, so a long "First Surname"
  // lands on two lines at a readable size rather than being squeezed onto one
  // tiny line. Measuring the rendered text beats guessing from the character
  // count: "WILHELMINA" and "iiiiiiiiii" are the same length but not the same
  // width.
  // Measured once per sheet, from the first badge. Grid cells can differ by a
  // sub-pixel, and measuring each badge separately let that rounding flip
  // identical names between one line and two.
  function nameBox(main) {
    var sub = main.querySelector('.badge-sub');
    var gap = parseFloat(getComputedStyle(main).rowGap) || 0;
    return {
      w: Math.floor(main.clientWidth),
      h: Math.floor(main.clientHeight - (sub ? sub.offsetHeight + gap : 0))
    };
  }

  function fitName(node, box, startPt, minPt) {
    // collapse the text first so it cannot inflate the box we are measuring
    node.style.fontSize = minPt + 'pt';
    var maxW = box.w, maxH = box.h;

    for (var pt = startPt; pt > minPt; pt -= 0.5) {
      node.style.fontSize = pt + 'pt';
      if (node.scrollWidth <= maxW + 0.5 && node.scrollHeight <= maxH + 0.5) return pt;
    }
    node.style.fontSize = minPt + 'pt';
    return minPt;
  }

  // The role line stays on one line; shrink it against its own width.
  function shrinkToFit(node, startPt, minPt) {
    var pt = startPt;
    node.style.fontSize = pt + 'pt';
    while (node.scrollWidth > node.clientWidth && pt > minPt) {
      pt -= 0.5;
      node.style.fontSize = pt + 'pt';
    }
  }

  function bottomMargin(size, top) {
    var used = size.rows * size.h;
    return top === null ? (297 - used) / 2 : 297 - used - top;
  }

  // Printers cannot print to the paper edge; most lose 3-5 mm. Say what the
  // margins actually are so a clipped top row is predictable, not a surprise.
  function reportMargins(size, top, safe) {
    var bottom = bottomMargin(size, top);
    var actualTop = top === null ? (297 - size.rows * size.h) / 2 : top;
    var txt = 'Sheet margins: ' + actualTop.toFixed(1) + ' mm top, ' +
              bottom.toFixed(1) + ' mm bottom, ' +
              ((210 - size.cols * size.w) / 2).toFixed(1) + ' mm sides.';
    if (bottom < -0.01) {
      txt += ' The last row runs ' + (-bottom).toFixed(1) + ' mm off the page.';
    } else {
      // most printers lose the outer 3-5 mm of the paper
      var side = (210 - size.cols * size.w) / 2;
      var tight = [];
      if (actualTop + safe < 5) tight.push('top');
      if (bottom + safe < 5) tight.push('bottom');
      if (side + safe < 5) tight.push('left and right');
      if (tight.length) {
        txt += ' Printers cannot reach the outer 3-5 mm of the paper, so the ' +
               tight.join(' and ') + ' edge' + (tight.length > 1 ? 's' : '') +
               ' may be clipped. Raise the safe area to hold the printing' +
               ' further inside each badge.';
      }
    }
    el.marginHint.textContent = txt;
  }

  // A4 is 210 x 297 mm; say so plainly when a custom grid will not fit.
  function reportFit(size) {
    if (el.size.value !== 'custom') { el.fitHint.textContent = ''; return; }
    var w = size.cols * size.w, h = size.rows * size.h;
    var over = [];
    if (w > 210.01) over.push(w.toFixed(1) + ' mm wide');
    if (h > 297.01) over.push(h.toFixed(1) + ' mm tall');
    el.fitHint.textContent = over.length
      ? 'Does not fit A4: the grid is ' + over.join(' and ') + '. Badges will be cut off.'
      : size.cols * size.rows + ' per sheet. Margins: ' +
        ((210 - w) / 2).toFixed(1) + ' mm left/right, ' +
        ((297 - h) / 2).toFixed(1) + ' mm top/bottom.';
  }

  function render() {
    var people = parsePeople(el.names.value);
    // no point reserving the role line if nobody has a role
    var showSub = el.showSub.checked && people.some(function (p) { return !!p.sub; });

    var size = currentSize();
    var top = topMargin();
    var safe = Math.max(0, parseFloat(el.safe.value) || 0);
    var perSheet = size.cols * size.rows;
    reportMargins(size, top, safe);
    document.body.className = (el.showMarks.checked ? 'marks' : '') +
                              (el.uniform.checked ? ' oneline' : '');
    el.customSize.hidden = el.size.value !== 'custom';
    reportFit(size);

    // the bar lives in the bottom margin; edge-to-edge grids have none
    var rulerFits = bottomMargin(size, top) >= 9;
    el.showRuler.parentNode.title = rulerFits ? '' :
      'No room at this badge size - the grid reaches the edge of the sheet.';
    el.showRuler.disabled = !rulerFits;

    var sheets = Math.ceil(people.length / perSheet);
    el.count.textContent = people.length + (people.length === 1 ? ' name' : ' names') +
      (sheets ? ' → ' + sheets + (sheets === 1 ? ' sheet' : ' sheets') : '');

    el.preview.textContent = '';
    if (!people.length) {
      var hint = document.createElement('p');
      hint.className = 'empty-state';
      hint.textContent = 'Add some names to see the A4 preview.';
      el.preview.appendChild(hint);
      save();
      return;
    }

    for (var s = 0; s < sheets; s++) {
      var sheet = document.createElement('div');
      sheet.className = 'sheet';
      sheet.style.setProperty('--bw', size.w + 'mm');
      sheet.style.setProperty('--bh', size.h + 'mm');
      sheet.style.setProperty('--cols', size.cols);
      sheet.style.setProperty('--safe', safe + 'mm');
      if (top !== null) {
        sheet.style.setProperty('--valign', 'start');
        sheet.style.setProperty('--padtop', top + 'mm');
      }
      for (var i = 0; i < perSheet; i++) {
        // empty trailing slots keep the cut lines on the last sheet aligned
        sheet.appendChild(makeBadge(people[s * perSheet + i] || null, showSub));
      }
      if (el.showRuler.checked && rulerFits) {
        var ruler = document.createElement('div');
        ruler.className = 'sheet-ruler';
        var tag = document.createElement('span');
        tag.textContent = 'this bar should measure 100 mm; if it does not, your print scale is not 100 %';
        ruler.appendChild(tag);
        sheet.appendChild(ruler);
      }
      el.preview.appendChild(sheet);
    }

    // Size the role line first: it is flex: none, so its final height decides
    // how much room is left for the name box.
    var k = size.h / 54;                       // 54 mm is the size the type was tuned at
    el.preview.querySelectorAll('.badge-sub').forEach(function (n) {
      shrinkToFit(n, 10.5 * k, 5 * k);
    });
    var first = el.preview.querySelector('.badge-main');
    if (first) {
      var box = nameBox(first);
      var names = el.preview.querySelectorAll('.badge-name');
      var smallest = Infinity;
      names.forEach(function (n) {
        smallest = Math.min(smallest, fitName(n, box, 28 * k, 5));
      });
      // level every badge to the size the longest name needed, so near-identical
      // names cannot sit at different sizes on the same sheet
      if (el.uniform.checked && isFinite(smallest)) {
        names.forEach(function (n) { n.style.fontSize = smallest + 'pt'; });
      }
    }

    save();
  }

  /* ---------- persistence ---------- */

  function save() {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({
        names: el.names.value,
        size: el.size.value,
        custom: { w: el.cw.value, h: el.ch.value, cols: el.ccols.value, rows: el.crows.value },
        showSub: el.showSub.checked,
        showMarks: el.showMarks.checked,
        showRuler: el.showRuler.checked,
        uniform: el.uniform.checked,
        topMargin: el.topMargin.value,
        safe: el.safe.value
      }));
    } catch (e) { /* private mode — not worth bothering the user about */ }
  }

  function restore() {
    var saved;
    try { saved = JSON.parse(localStorage.getItem(STORE_KEY) || 'null'); } catch (e) { return; }
    if (!saved) return;
    el.names.value = saved.names || '';
    el.showSub.checked = saved.showSub !== false;
    el.showMarks.checked = saved.showMarks !== false;
    el.showRuler.checked = saved.showRuler !== false;
    el.uniform.checked = !!saved.uniform;
    if (saved.topMargin !== undefined) el.topMargin.value = saved.topMargin;
    if (saved.safe !== undefined) el.safe.value = saved.safe;
    if (saved.size) el.size.value = saved.size;
    if (saved.custom) {
      el.cw.value = saved.custom.w; el.ch.value = saved.custom.h;
      el.ccols.value = saved.custom.cols; el.crows.value = saved.custom.rows;
    }
  }

  /* ---------- wiring ---------- */

  el.names.addEventListener('input', render);
  el.showSub.addEventListener('change', render);
  el.showMarks.addEventListener('change', render);
  el.showRuler.addEventListener('change', render);
  el.uniform.addEventListener('change', render);
  el.topMargin.addEventListener('input', render);
  el.safe.addEventListener('input', render);
  el.size.addEventListener('change', render);
  ['cw','ch','ccols','crows'].forEach(function (id) {
    el[id].addEventListener('input', render);
  });
  el.file.addEventListener('change', function () {
    if (this.files[0]) loadFile(this.files[0]);
  });
  el.print.addEventListener('click', function () { window.print(); });

  // exposed for the test harness in test/parse-test.html
  window.BadgeMaker = { parsePeople: parsePeople, rowsToLines: rowsToLines };

  restore();
  render();
  // the logo is an external SVG; re-fit once it has laid out
  window.addEventListener('load', render);
})();
