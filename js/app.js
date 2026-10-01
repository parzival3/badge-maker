/* Badge Maker — builds A4 sheets of name badges entirely in the browser. */

(function () {
  'use strict';

  var PER_ROW = 2;
  var PER_SHEET = 10;
  var STORE_KEY = 'badge-maker/v1';

  var el = {
    names: document.getElementById('names'),
    file: document.getElementById('file'),
    fileHint: document.getElementById('fileHint'),
    showSub: document.getElementById('showSub'),
    showMarks: document.getElementById('showMarks'),
    count: document.getElementById('count'),
    print: document.getElementById('print'),
    preview: document.getElementById('preview')
  };

  function sizeInput() {
    return document.querySelector('input[name=size]:checked');
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
  function fitName(node, main, startPt, minPt) {
    // collapse the text first so it cannot inflate the box we are measuring
    node.style.fontSize = minPt + 'pt';

    var sub = main.querySelector('.badge-sub');
    var gap = parseFloat(getComputedStyle(main).rowGap) || 0;
    var maxW = main.clientWidth;
    var maxH = main.clientHeight - (sub ? sub.offsetHeight + gap : 0);

    for (var pt = startPt; pt > minPt; pt -= 0.5) {
      node.style.fontSize = pt + 'pt';
      if (node.scrollWidth <= maxW + 0.5 && node.scrollHeight <= maxH + 0.5) return;
    }
    node.style.fontSize = minPt + 'pt';
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

  function render() {
    var people = parsePeople(el.names.value);
    // no point reserving the role line if nobody has a role
    var showSub = el.showSub.checked && people.some(function (p) { return !!p.sub; });

    document.body.className = 'size-' + sizeInput().value + (el.showMarks.checked ? ' marks' : '');

    var sheets = Math.ceil(people.length / PER_SHEET);
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
      for (var i = 0; i < PER_SHEET; i++) {
        // empty trailing slots keep the cut lines on the last sheet aligned
        sheet.appendChild(makeBadge(people[s * PER_SHEET + i] || null, showSub));
      }
      el.preview.appendChild(sheet);
    }

    // Size the role line first: it is flex: none, so its final height decides
    // how much room is left for the name box.
    el.preview.querySelectorAll('.badge-sub').forEach(function (n) {
      shrinkToFit(n, 10.5, 6);
    });
    el.preview.querySelectorAll('.badge-main').forEach(function (main) {
      fitName(main.querySelector('.badge-name'), main, 36, 8);
    });

    save();
  }

  /* ---------- persistence ---------- */

  function save() {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({
        names: el.names.value,
        size: sizeInput().value,
        showSub: el.showSub.checked,
        showMarks: el.showMarks.checked
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
    var radio = document.querySelector('input[name=size][value="' + saved.size + '"]');
    if (radio) radio.checked = true;
  }

  /* ---------- wiring ---------- */

  el.names.addEventListener('input', render);
  el.showSub.addEventListener('change', render);
  el.showMarks.addEventListener('change', render);
  document.querySelectorAll('input[name=size]').forEach(function (r) {
    r.addEventListener('change', render);
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
