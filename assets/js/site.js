(() => {
  const EMAIL = "reubenabraham.official@gmail.com";
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  /* toast ---------------------------------------------------------- */
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.setAttribute("role", "status");
  document.body.append(toast);
  let toastTimer;
  const say = (msg) => {
    toast.textContent = msg;
    toast.classList.add("on");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("on"), 2400);
  };

  /* Singapore clock + what I'm probably doing ---------------------- */
  const sgParts = () => {
    const parts = new Intl.DateTimeFormat("en-GB", {
      timeZone: "Asia/Singapore",
      hour: "2-digit",
      minute: "2-digit",
      weekday: "short",
      hour12: false,
    }).formatToParts(new Date());
    return Object.fromEntries(parts.map((p) => [p.type, p.value]));
  };

  const statusFor = (h, day) => {
    const weekend = day === "Sat" || day === "Sun";
    if (h < 6) return "probably asleep. I'll reply in the morning.";
    if (h < 9) return "probably still waking up.";
    if (h < 12) return weekend ? "probably offline. It's the weekend." : "probably heads-down in Figma.";
    if (h < 14) return "probably at lunch.";
    if (h < 18) return weekend ? "possibly baking a cheesecake." : "probably in a design review, or prototyping one.";
    if (h < 21) return "probably wrapping up for the day.";
    return "probably winding down. I'll reply in the morning.";
  };

  const tick = () => {
    const p = sgParts();
    $$("[data-clock]").forEach((el) => {
      el.innerHTML = `SGT ${p.hour}<span class="colon">:</span>${p.minute}`;
    });
    $$("[data-status]").forEach((el) => {
      el.textContent = `It's ${p.hour}:${p.minute} in Singapore — I'm ${statusFor(+p.hour, p.weekday)}`;
    });
  };
  tick();
  setInterval(tick, 15000);

  /* copy email ------------------------------------------------------ */
  const copyEmail = async () => {
    try {
      await navigator.clipboard.writeText(EMAIL);
      say("Email copied. Talk soon.");
    } catch {
      window.location.href = `mailto:${EMAIL}`;
    }
  };
  $$("[data-copy-email]").forEach((b) => b.addEventListener("click", copyEmail));

  /* keyboard shortcuts --------------------------------------------- */
  const card = document.createElement("div");
  card.className = "keys-card";
  card.innerHTML = `
    <div class="card" role="dialog" aria-modal="true" aria-label="Keyboard shortcuts">
      <h2>A few shortcuts</h2>
      <dl>
        <dt><kbd>J</kbd> <kbd>K</kbd></dt><dd>Next / previous section</dd>
        <dt><kbd>N</kbd></dt><dd>Next case study</dd>
        <dt><kbd>H</kbd></dt><dd>Home</dd>
        <dt><kbd>E</kbd></dt><dd>Copy my email</dd>
        <dt><kbd>?</kbd></dt><dd>Toggle this card</dd>
      </dl>
      <span class="label">Esc to close</span>
    </div>`;
  document.body.append(card);
  const toggleCard = (on = !card.classList.contains("on")) => card.classList.toggle("on", on);
  card.addEventListener("click", (e) => e.target === card && toggleCard(false));

  const sections = () => $$(".chapter[id], .cs-hero");
  const jump = (dir) => {
    const list = sections();
    if (!list.length) return;
    const y = window.scrollY + 40;
    let idx = list.findIndex((s) => s.offsetTop > y);
    if (idx === -1) idx = list.length;
    const target = dir > 0 ? list[idx] : list[Math.max(0, idx - 2)];
    if (target) target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
  };

  const jokes = [
    "I'd tell you a UX joke, but you'd need onboarding first.",
    "How many designers does it take to change a lightbulb? Does it have to be a lightbulb?",
    "My grid and I broke up. It kept boxing me in.",
    "I asked for feedback. Got 14 comments and a new font.",
  ];
  let typed = "";
  let lastKey = 0;
  let jokeIdx = 0;
  document.addEventListener("keydown", (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (/input|textarea|select/i.test(e.target.tagName)) return;
    const k = e.key;
    const now = performance.now();
    const midWord = /^[a-z]$/i.test(k) && now - lastKey < 600;
    lastKey = /^[a-z]$/i.test(k) ? now : 0;
    typed = (typed + k.toLowerCase()).slice(-10);
    if (typed.endsWith("cheesecake")) return say("Noted. I'll bring one to the interview.");
    if (typed.endsWith("lame")) return say(jokes[jokeIdx++ % jokes.length]);
    if (midWord) return;
    if (k === "?") return toggleCard();
    if (k === "Escape") return toggleCard(false);
    if (k === "j") return jump(1);
    if (k === "k") return jump(-1);
    if (k === "h") return (window.location.href = document.documentElement.dataset.root || "/");
    if (k === "e") return copyEmail();
    if (k === "n") {
      const next = $("[data-next]");
      if (next) window.location.href = next.getAttribute("href");
    }
  });

  /* tab title when away -------------------------------------------- */
  const title = document.title;
  document.addEventListener("visibilitychange", () => {
    document.title = document.hidden ? "Still here when you're back — Reuben" : title;
  });

  /* hello, curious engineer ---------------------------------------- */
  console.log(
    "%cHi, I'm Reuben.%c\nThis site is hand-written HTML, CSS and a little JS. No framework.\nPress ? on any page for shortcuts. Or just say hi: " + EMAIL,
    "font: italic 20px Newsreader, Georgia, serif; color: #cf472c",
    "font: 12px ui-monospace, monospace; color: #5e5b55"
  );

  /* hover preview for the ledger ----------------------------------- */
  const peekTargets = $$("[data-peek]");
  if (peekTargets.length && window.matchMedia("(hover: hover)").matches) {
    const peek = document.createElement("div");
    peek.className = "peek";
    const img = document.createElement("img");
    img.alt = "";
    peek.append(img);
    document.body.append(peek);
    let x = 0, y = 0, raf;
    const move = () => {
      peek.style.transform = `translate3d(${x + 22}px, ${y - 90}px, 0) rotate(-1.5deg)`;
      raf = null;
    };
    peekTargets.forEach((t) => {
      t.addEventListener("mouseenter", () => {
        img.src = t.dataset.peek;
        peek.classList.add("on");
      });
      t.addEventListener("mouseleave", () => peek.classList.remove("on"));
      t.addEventListener("mousemove", (e) => {
        x = e.clientX;
        y = e.clientY;
        if (!raf) raf = requestAnimationFrame(move);
      });
    });
  }

  /* reveal-on-view (bars, funnels) --------------------------------- */
  const io = new IntersectionObserver(
    (entries) =>
      entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.classList.add("in");
          io.unobserve(en.target);
        }
      }),
    { threshold: 0.35 }
  );
  $$(".bars, .funnel, [data-reveal]").forEach((el) => io.observe(el));

  /* prototype loops ------------------------------------------------- */
  $$(".loop video").forEach((v) => {
    const wrap = v.closest(".loop");
    const state = document.createElement("span");
    state.className = "state";
    state.textContent = "Pause";
    wrap.append(state);
    v.muted = true;
    v.playsInline = true;
    v.loop = true;
    let userPaused = reduceMotion;
    const sync = () => {
      wrap.classList.toggle("paused", v.paused);
      state.textContent = v.paused ? "Play prototype" : "Pause";
    };
    v.addEventListener("play", sync);
    v.addEventListener("pause", sync);
    v.addEventListener("click", () => {
      if (v.paused) {
        userPaused = false;
        v.play();
      } else {
        userPaused = true;
        v.pause();
      }
    });
    new IntersectionObserver(
      ([en]) => {
        if (en.isIntersecting && !userPaused) v.play().catch(() => {});
        else v.pause();
      },
      { threshold: 0.4 }
    ).observe(v);
    sync();
  });

  /* before / after -------------------------------------------------- */
  $$(".compare").forEach((c) => {
    const btns = $$(".seg button", c);
    btns.forEach((b) =>
      b.addEventListener("click", () => {
        btns.forEach((o) => o.setAttribute("aria-pressed", String(o === b)));
        c.classList.toggle("show-after", b.dataset.side === "after");
      })
    );
  });

  /* sidenote highlight --------------------------------------------- */
  $$("sup.ref[data-n]").forEach((r) => {
    const note = $(`.note[data-n="${r.dataset.n}"]`);
    if (!note) return;
    const on = () => note.classList.add("lit");
    const off = () => note.classList.remove("lit");
    r.addEventListener("mouseenter", on);
    r.addEventListener("mouseleave", off);
    note.addEventListener("mouseenter", on);
    note.addEventListener("mouseleave", off);
  });

  /* case study: progress, toc, minutes left ------------------------ */
  const article = $(".cs-body");
  const toc = $(".toc");
  const bar = $(".progress");
  if (article) {
    const words = article.innerText.split(/\s+/).length;
    const totalMin = Math.max(1, Math.round(words / 230));
    const left = toc && $(".left", toc);
    const links = toc ? $$("a", toc) : [];
    const chapters = links.map((a) => $(a.getAttribute("href"))).filter(Boolean);
    const hero = $(".cs-hero");
    const onScroll = () => {
      const start = article.offsetTop;
      const end = start + article.offsetHeight - window.innerHeight;
      const p = Math.min(1, Math.max(0, (window.scrollY - start) / Math.max(1, end - start)));
      if (bar) bar.style.transform = `scaleX(${p})`;
      if (toc) {
        toc.classList.toggle("on", window.scrollY > (hero ? hero.offsetTop + hero.offsetHeight - 200 : 400) && p < 0.995);
        let active = 0;
        chapters.forEach((c, i) => {
          if (c.getBoundingClientRect().top < window.innerHeight * 0.35) active = i;
        });
        links.forEach((a, i) => a.classList.toggle("active", i === active));
        if (left) {
          const m = Math.ceil(totalMin * (1 - p));
          left.textContent = m <= 0 ? "That's the story." : `${m} min left of ${totalMin}`;
        }
      }
    };
    document.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    onScroll();
  }

  /* shared basket demo (Scan to Order) ----------------------------- */
  const demo = $("[data-basket-demo]");
  if (demo) {
    const list = $("ul", demo);
    const total = $(".tot span", demo);
    const ping = $(".ping", demo);
    const people = [
      { n: "Reuben", c: "#1d2230" },
      { n: "Zihui", c: "#cf472c" },
      { n: "Arun", c: "#00875a" },
      { n: "Mei", c: "#7a5af8" },
    ];
    const dishes = [
      ["Chicken fried rice", 8.9],
      ["Kung pao prawns", 16.5],
      ["Xiao long bao ×6", 9.8],
      ["Sambal kangkong", 7.2],
      ["Iced lemon tea", 3.5],
      ["Mapo tofu", 11.0],
      ["Har gow ×4", 7.8],
    ];
    let sum = 0, i = 0;
    const add = (who, quiet) => {
      const [dish, price] = dishes[i++ % dishes.length];
      sum += price;
      const li = document.createElement("li");
      li.innerHTML = `<span class="who" style="background:${who.c}">${who.n[0]}</span><span>1 × ${dish}<small>added by ${who.n}</small></span><span>$${price.toFixed(2)}</span>`;
      list.prepend(li);
      while (list.children.length > 5) list.lastElementChild.remove();
      total.textContent = `$${sum.toFixed(2)}`;
      if (quiet) return;
      ping.textContent = `1 × ${dish} added by ${who.n}`;
      ping.classList.add("on");
      clearTimeout(ping._t);
      ping._t = setTimeout(() => ping.classList.remove("on"), 1800);
    };
    add(people[2], true);
    add(people[1], true);
    $("[data-add-mine]", demo).addEventListener("click", () => add(people[0]));
    $("[data-add-theirs]", demo).addEventListener("click", () =>
      add(people[1 + Math.floor(Math.random() * (people.length - 1))])
    );
  }
})();
