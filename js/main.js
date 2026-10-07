/* Pixopoly: marketing site. No dependencies. */
(() => {
  "use strict";

  // ─── Edit these when the pages exist ───────────────────────────────────────
  const CONFIG = {
    steam: "",                                   // e.g. "https://store.steampowered.com/app/1234567/Pixopoly/"
    itch: "https://intebat.itch.io/pixopoly",
  };

  const $ = (q, el = document) => el.querySelector(q);
  const $$ = (q, el = document) => [...el.querySelectorAll(q)];
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const PAWNS = ["Pawn", "Top Hat", "Car", "Cat", "Boat", "Castle", "Crown", "Rocket", "Duck", "Dog", "Robot", "Ghost", "Dino",
    "Penguin", "Frog", "Teapot", "Skateboard", "UFO", "Boot", "Cactus", "Mushroom", "Alien", "Crab", "Pumpkin", "Slime"];
  const CHAOS = ["Earthquake", "Property Boom", "Market Crash", "Tax Holiday", "Double Payday", "Robin Hood", "Jailbreak", "Building Sale"];

  // ─── Links ─────────────────────────────────────────────────────────────────
  // Until there's a Steam page, the Steam buttons say so and don't pretend to go anywhere.
  $$("[data-link]").forEach((a) => {
    const url = CONFIG[a.dataset.link];
    if (url) {
      a.href = url;
      a.target = "_blank";
      a.rel = "noopener";
    } else if (a.dataset.link === "steam") {
      a.classList.add("is-soon");
      a.textContent = a.classList.contains("sm") ? "Soon" : "Steam page soon";
      a.setAttribute("aria-disabled", "true");
      a.addEventListener("click", (e) => e.preventDefault());
    }
  });
  $("#year").textContent = new Date().getFullYear();

  // A press bursts a gold frame out of the button, like in the game.
  $$(".btn").forEach((b) => b.addEventListener("click", () => {
    if (calm || b.classList.contains("is-soon")) return;
    b.classList.remove("pop");
    void b.offsetWidth;
    b.classList.add("pop");
    setTimeout(() => b.classList.remove("pop"), 300);
  }));

  // ─── The logo's die hops and lands on a new face ───────────────────────────
  const die = $("#die");
  const dieBox = die && die.parentElement;
  function roll() {
    if (!die || calm || document.hidden) return;
    dieBox.classList.remove("hop");
    void dieBox.offsetWidth;
    dieBox.classList.add("hop");
    setTimeout(() => { die.src = `/assets/img/die_${1 + Math.floor(Math.random() * 6)}.png`; }, 200);
  }
  if (die) {
    for (let n = 1; n <= 6; n++) new Image().src = `/assets/img/die_${n}.png`;
    setInterval(roll, 2600);
    dieBox.addEventListener("click", roll);
    dieBox.style.cursor = "pointer";
  }

  // ─── Pawns walking across the bottom of the hero ───────────────────────────
  const parade = $("#parade");
  if (parade && !calm) {
    const picks = [0, 3, 10, 14, 7, 15, 12, 20, 16, 23];
    picks.forEach((n, i) => {
      const p = document.createElement("i");
      p.className = "spr pawn";
      p.style.setProperty("--n", n);
      p.style.setProperty("--t", `${24 + (i % 3) * 5}s`);
      p.style.setProperty("--d", `${-i * 3.1}s`);
      parade.appendChild(p);
    });
  }

  // ─── Parallax on the hero's backdrop ───────────────────────────────────────
  if (!calm) {
    addEventListener("scroll", () => document.documentElement.style.setProperty("--scroll", scrollY), { passive: true });
  }

  // ─── Chaos events cycle; the stamp slams down with each one ────────────────
  const chaos = $("#chaos"), stamp = $("#stamp");
  if (chaos && stamp) {
    let i = 0;
    setInterval(() => {
      if (document.hidden) return;
      i = (i + 1) % CHAOS.length;
      const an = /^[AEIOU]/.test(CHAOS[i]) ? "an" : "a";
      chaos.textContent = CHAOS[i];
      chaos.previousSibling.textContent = chaos.previousSibling.textContent.replace(/\ban? $/, `${an} `);
      stamp.textContent = CHAOS[i].toUpperCase();
      if (!calm) {
        stamp.classList.remove("slam");
        void stamp.offsetWidth;
        stamp.classList.add("slam");
      }
    }, 2400);
  }

  // ─── Pick a pawn ───────────────────────────────────────────────────────────
  const picker = $("#picker"), big = $("#bigpawn"), nameEl = $("#pawnname");
  if (picker && big) {
    const shown = [14, 15, 16, 0, 3, 10, 11, 12, 13, 17, 20, 22, 23, 24, 8, 9];
    const choose = (n, btn) => {
      big.style.setProperty("--n", n);
      nameEl.textContent = PAWNS[n];
      $$("button", picker).forEach((b) => b.setAttribute("aria-pressed", b === btn));
      $("#bigdie").style.setProperty("--n", (n * 7 + 5) % 27);
      $("#bigdie2").style.setProperty("--n", (n * 11 + 9) % 27);
      if (!calm) {
        big.classList.remove("swap");
        void big.offsetWidth;
        big.classList.add("swap");
      }
    };
    shown.forEach((n, i) => {
      const b = document.createElement("button");
      b.type = "button";
      b.title = PAWNS[n];
      b.setAttribute("aria-label", PAWNS[n]);
      b.setAttribute("aria-pressed", i === 0);
      b.innerHTML = `<i class="spr pawn" style="--n:${n}"></i>`;
      b.addEventListener("click", () => choose(n, b));
      picker.appendChild(b);
    });
  }

  // ─── Tables ────────────────────────────────────────────────────────────────
  const tableShot = $("#tableshot");
  $$(".tabs [role=tab]").forEach((tab) => tab.addEventListener("click", () => {
    $$(".tabs [role=tab]").forEach((t) => t.setAttribute("aria-selected", t === tab));
    const id = tab.dataset.table;
    tableShot.dataset.shot = id;
    $("img", tableShot).src = `/assets/shots/${id}_s.webp`;
    tableShot.classList.remove("swap");
    void tableShot.offsetWidth;
    tableShot.classList.add("swap");
  }));

  // ─── Screenshots open full size ────────────────────────────────────────────
  const box = $("#lightbox"), boxImg = $("#lightimg");
  const closeBox = () => { box.hidden = true; boxImg.removeAttribute("src"); };
  $$(".shot").forEach((s) => s.addEventListener("click", () => {
    boxImg.src = `/assets/shots/${s.dataset.shot}.webp`;
    boxImg.alt = $("img", s).alt;
    box.hidden = false;
  }));
  if (box) {
    box.addEventListener("click", closeBox);
    addEventListener("keydown", (e) => { if (e.key === "Escape" && !box.hidden) closeBox(); });
  }

  // ─── Things rise into place as you reach them ──────────────────────────────
  const items = $$(".reveal");
  if (calm || !("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("in"));
  } else {
    const io = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("in");
        io.unobserve(e.target);
      }
    }), { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    items.forEach((el, i) => {
      el.style.transitionDelay = `${(i % 3) * 70}ms`;
      io.observe(el);
    });
  }
})();
