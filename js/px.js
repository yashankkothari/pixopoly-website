/* Pixonomy home page: the store links, the dice you can roll on the hero board, the scroll
   track in the bar, the teaser and pieces dropping onto the table as you scroll. No libraries. */
(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Same links as js/main.js: fill in steam when the Steam page exists.
  const CONFIG = {
    steam: "",                                   // e.g. "https://store.steampowered.com/app/1234567/Pixonomy/"
  };

  // ── Links: until there's a Steam page, the Steam buttons say so and go nowhere ──
  document.querySelectorAll("[data-link]").forEach((a) => {
    const url = CONFIG[a.dataset.link];
    if (url) {
      a.href = url; a.target = "_blank"; a.rel = "noopener";
    } else if (a.dataset.link === "steam") {
      a.classList.add("is-soon");
      a.textContent = a.classList.contains("sm") ? "Steam (soon)" : "Steam page soon";
      a.setAttribute("aria-disabled", "true");
      a.addEventListener("click", (e) => e.preventDefault());
    }
  });
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // ── The teaser plays muted; a button turns the sound on ──
  const reel = document.getElementById("reel"), sound = document.getElementById("sound");
  if (reel && sound) {
    if (reduce) { reel.removeAttribute("autoplay"); reel.pause(); reel.controls = true; }
    sound.addEventListener("click", () => {
      reel.muted = !reel.muted;
      if (!reel.muted) { reel.currentTime = 0; reel.play(); }
      sound.setAttribute("aria-pressed", String(!reel.muted));
      sound.textContent = reel.muted ? "Sound on" : "Sound off";
    });
  }

  // The World Tour board in play order, from Payday clockwise (RULES.md section 4).
  const SETS = { brown: "#a8704a", lblue: "#7ab6dc", pink: "#d4548f", orange: "#e87a2c", red: "#c8323a", yellow: "#f0c62e", green: "#3c9a4a", dblue: "#3a66c8", rail: "#3d3d50", util: "#2a8f8a", card: "#7c42c0", tax: "#c8323a", corner: "#4a9458" };
  const SET_NAME = { brown: "Brown set", lblue: "Light blue set", pink: "Pink set", orange: "Orange set", red: "Red set", yellow: "Yellow set", green: "Green set", dblue: "Dark blue set" };
  const T = [
    ["Payday", "corner", "Collect $200 every time you pass"], ["Trans-Siberian Railway", "rail", "Railroad · $180"],
    ["Cairo", "brown", 70], ["Istanbul", "brown", 90], ["Mailbox", "card", "Draw a Mailbox card"],
    ["Mumbai", "lblue", 110], ["Bangkok", "lblue", 110], ["Income Tax", "tax", "Pay $180 to the bank"], ["Rio de Janeiro", "lblue", 130],
    ["Lockup", "corner", "Just passing by"], ["Mexico City", "pink", 150], ["Athens", "pink", 150], ["Power Grid Co.", "util", "Utility · $140"],
    ["Silk Road Line", "rail", "Railroad · $180"], ["Toronto", "orange", 190], ["Wildcard", "card", "Draw a Wildcard"], ["Tel Aviv", "orange", 190], ["Seoul", "orange", 210],
    ["Bank Loan", "corner", "Borrow $200, pay $250 at Payday"], ["Channel Express", "rail", "Railroad · $180"], ["Los Angeles", "red", 230], ["Paris", "red", 230],
    ["Mailbox", "card", "Draw a Mailbox card"], ["Rome", "yellow", 270], ["Berlin", "yellow", 270], ["Global Water Co.", "util", "Utility · $140"], ["Dubai", "yellow", 290],
    ["Lucky Spin", "corner", "Spin the case for a prize"], ["Tokyo", "green", 310], ["Sydney", "green", 310], ["Wildcard", "card", "Draw a Wildcard"],
    ["Bullet Train", "rail", "Railroad · $180"], ["Hong Kong", "green", 330], ["London", "dblue", 370], ["Luxury Tax", "tax", "Pay $120 to the bank"], ["New York City", "dblue", 420],
  ];

  // Tile centres on the 464 px board picture: 56 px corners, 44 px edge tiles.
  const C = 56, E = 44, W = 464;
  function centre(i) {
    if (i === 0) return [W - C / 2, W - C / 2];
    if (i < 9) return [W - C - E * (i - 1) - E / 2, W - C / 2];
    if (i === 9) return [C / 2, W - C / 2];
    if (i < 18) return [C / 2, W - C - E * (i - 10) - E / 2];
    if (i === 18) return [C / 2, C / 2];
    if (i < 27) return [C + E * (i - 19) + E / 2, C / 2];
    if (i === 27) return [W - C / 2, C / 2];
    return [W - C / 2, C + E * (i - 28) + E / 2];
  }
  function rect(i) {
    const [x, y] = centre(i), corner = i % 9 === 0;
    const side = (i > 9 && i < 18) || (i > 27);
    const w = corner ? C : side ? C : E, h = corner ? C : side ? E : C;
    return [x - w / 2, y - h / 2, w, h];
  }
  const pct = (v) => (v / W * 100) + "%";

  // ── Hero roll ──
  const board = document.querySelector("[data-board]");
  if (board) {
    const pawn = board.querySelector(".pawn"), hl = board.querySelector(".board__hl");
    const dice = [...board.querySelectorAll(".die")], btn = board.querySelector("[data-roll]");
    const art = board.querySelector(".landed__art"), title = board.querySelector(".landed b"), sub = board.querySelector(".landed div span"), hint = board.querySelector(".roll-hint");
    let pos = 0, doubles = 0, busy = false;
    const place = (i) => { const [x, y] = centre(i); pawn.style.left = pct(x); pawn.style.top = pct(y); };
    const mark = (i) => {
      const [x, y, w, h] = rect(i);
      Object.assign(hl.style, { left: pct(x), top: pct(y), width: pct(w), height: pct(h) });
      hl.classList.remove("on"); void hl.offsetWidth; hl.classList.add("on");
    };
    const show = (i, note) => {
      const [name, kind, x] = T[i];
      art.style.setProperty("--t", i);
      title.textContent = name;
      const tag = `<i class="tag" style="--c:${SETS[kind]}"></i>`;
      sub.innerHTML = (typeof x === "number" ? `${tag}${SET_NAME[kind]} · $${x}. Buy it or auction it.` : tag + x) + (note ? `<br>${note}` : "");
    };
    const wait = (ms) => new Promise((r) => setTimeout(r, ms));
    place(0);

    btn.addEventListener("click", async () => {
      if (busy) return;
      busy = true; btn.setAttribute("aria-busy", "true");
      const a = 1 + Math.floor(Math.random() * 6), b = 1 + Math.floor(Math.random() * 6);
      if (!reduce) {
        for (let k = 0; k < 10; k++) {
          dice[0].style.setProperty("--d", (k * 5) % 12); dice[1].style.setProperty("--d", (k * 7 + 3) % 12);
          await wait(55);
        }
      }
      dice[0].style.setProperty("--d", 11 + a); dice[1].style.setProperty("--d", 11 + b);
      btn.setAttribute("aria-label", `Roll the dice. Last roll: ${a} and ${b}`);
      const dbl = a === b;
      doubles = dbl ? doubles + 1 : 0;
      let note = "", passed = false;
      if (doubles === 3) {
        doubles = 0; await wait(200);
        pos = 9; place(pos); mark(pos); show(pos, "Third double in a row: straight to the Lockup!");
      } else {
        for (let s = 1; s <= a + b; s++) {
          pos = (pos + 1) % 36;
          if (pos === 0 && s < a + b) passed = true;
          place(pos);
          if (!reduce) { pawn.classList.remove("hop"); void pawn.offsetWidth; pawn.classList.add("hop"); await wait(150); }
        }
        if (passed) note = "Passed Payday: +$200.";
        if (dbl) note += (note ? " " : "") + "Doubles! Roll again.";
        mark(pos); show(pos, note);
      }
      if (hint) hint.textContent = dbl ? "Doubles! Roll again" : `You rolled ${a + b}`;
      busy = false; btn.removeAttribute("aria-busy");
    });
  }

  // ── Scroll track: the board's 36 tiles along the bottom of the bar ──
  const track = document.querySelector("[data-track]");
  if (track) {
    track.innerHTML = T.map(([, k]) => `<i style="--c:${SETS[k]}"></i>`).join("") + '<span class="pawn" style="--r:0" aria-hidden="true"></span>';
    const cells = [...track.querySelectorAll("i")], tp = track.querySelector(".pawn");
    let last = -1;
    const upd = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      const n = Math.max(0, Math.min(35, Math.round((scrollY / Math.max(1, max)) * 35)));
      if (n === last) return;
      last = n;
      cells.forEach((c, i) => c.classList.toggle("on", i <= n));
      const r = cells[n].getBoundingClientRect(), tr = track.getBoundingClientRect();
      tp.style.left = (r.left - tr.left + r.width / 2 - 10) + "px";
    };
    addEventListener("scroll", upd, { passive: true }); addEventListener("resize", () => { last = -1; upd(); }); upd();
  }

  // ── Pieces drop onto the table ──
  const rv = document.querySelectorAll(".rv");
  if ("IntersectionObserver" in window && !reduce) {
    document.documentElement.classList.add("js");
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
    rv.forEach((el) => io.observe(el));
    // never leave anything hidden if the observer is slow
    setTimeout(() => rv.forEach((el) => el.classList.add("in")), 6000);
  }
})();
