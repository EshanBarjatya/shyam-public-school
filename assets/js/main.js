/* ==========================================================================
   Shyam Public School — behaviour
   Vanilla JS, no dependencies. Progressive enhancement only: every page
   remains readable and every contact route works with JS disabled.
   ========================================================================== */
(function () {
  "use strict";

  var SCHOOL = {
    phone: "+918952021550",
    phoneDisplay: "+91 89520 21550",
    email: "sharma.rakesh3488@gmail.com",
    contactPerson: "Rakesh Sharma"
  };

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Mobile navigation ---------- */
  function initNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var nav = document.getElementById("primary-nav");
    var scrim = document.querySelector("[data-nav-scrim]");
    if (!toggle || !nav) return;

    function setOpen(open) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      nav.classList.toggle("is-open", open);
      if (scrim) scrim.classList.toggle("is-visible", open);
      document.body.style.overflow = open ? "hidden" : "";
      if (open) {
        var first = nav.querySelector("a, button");
        if (first) first.focus({ preventScroll: true });
      }
    }

    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    if (scrim) scrim.addEventListener("click", function () { setOpen(false); });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        toggle.focus();
      }
    });

    nav.addEventListener("click", function (e) {
      if (e.target.closest("a") && window.innerWidth < 1024) setOpen(false);
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1024) setOpen(false);
    });
  }

  /* ---------- Sticky header, mobile action bar, floating enquire button ---------- */
  function initScrollChrome() {
    var header = document.querySelector(".site-header");
    var bar = document.querySelector("[data-action-bar]");
    var floatCta = document.querySelector("[data-float-cta]");
    if (bar) document.body.classList.add("has-action-bar");

    // Suppress the floating button while the enquiry form is on screen —
    // offering a shortcut to something already in front of the reader is noise.
    var formInView = false;
    var enquiry = document.getElementById("enquiry");
    if (floatCta && enquiry && "IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        formInView = entries[0].isIntersecting;
        update();
      }, { threshold: 0.12 }).observe(enquiry);
    }

    function update() {
      var y = window.scrollY;
      if (header) header.classList.toggle("is-stuck", y > 8);
      if (bar) bar.classList.toggle("is-visible", y > 280);
      if (floatCta) floatCta.classList.toggle("is-visible", y > 520 && !formInView);
    }

    update();
    window.addEventListener("scroll", update, { passive: true });
  }

  /* ---------- Scroll reveal ---------- */
  function initReveal() {
    var items = document.querySelectorAll("[data-reveal]");
    if (!items.length) return;

    if (reduceMotion || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("is-revealed"); });
      return;
    }

    // Stagger siblings that share a parent group
    document.querySelectorAll("[data-reveal-group]").forEach(function (group) {
      Array.prototype.forEach.call(group.children, function (child, i) {
        if (child.hasAttribute("data-reveal")) {
          child.style.setProperty("--reveal-delay", Math.min(i * 90, 450) + "ms");
        }
      });
    });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-revealed");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- FAQ accordion ---------- */
  function initFaq() {
    document.querySelectorAll(".faq__q").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var item = btn.closest(".faq__item");
        var open = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", open ? "false" : "true");
        item.classList.toggle("is-open", !open);
      });
    });
  }

  /* ---------- Gallery lightbox ---------- */
  function initLightbox() {
    var items = document.querySelectorAll("[data-lightbox]");
    if (!items.length) return;

    var box = document.createElement("div");
    box.className = "lightbox";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Enlarged photograph");
    box.innerHTML =
      '<button class="lightbox__close" type="button" aria-label="Close">&times;</button>' +
      '<div><img alt=""><p class="lightbox__cap"></p></div>';
    document.body.appendChild(box);

    var img = box.querySelector("img");
    var cap = box.querySelector(".lightbox__cap");
    var closeBtn = box.querySelector(".lightbox__close");
    var lastFocus = null;

    function open(src, alt, caption) {
      lastFocus = document.activeElement;
      img.src = src;
      img.alt = alt || "";
      cap.textContent = caption || "";
      box.classList.add("is-open");
      document.body.style.overflow = "hidden";
      closeBtn.focus();
    }
    function close() {
      box.classList.remove("is-open");
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    }

    items.forEach(function (item) {
      item.addEventListener("click", function () {
        var picture = item.querySelector("img");
        if (!picture) return;
        open(picture.currentSrc || picture.src, picture.alt, item.getAttribute("data-caption"));
      });
    });

    closeBtn.addEventListener("click", close);
    box.addEventListener("click", function (e) { if (e.target === box) close(); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && box.classList.contains("is-open")) close();
    });
  }

  /* ---------- Enquiry form ----------
     No server is wired up yet. Until a backend or form service is connected
     (see docs/launch-checklist.md), a validated submission is handed to
     WhatsApp — the fastest route to a reply for a school this size — with a
     pre-filled email as the fallback. Nothing is silently dropped.
  ------------------------------------- */
  function initForms() {
    document.querySelectorAll("[data-enquiry-form]").forEach(function (form) {
      var status = form.querySelector("[data-form-status]");

      function fail(field, message) {
        // The consent checkbox sits in its own label, not a .field wrapper —
        // without this it was possible to be told to "complete the highlighted
        // fields" with nothing highlighted.
        var wrap = field.closest(".field") || field.closest(".consent");
        if (!wrap) return;
        wrap.classList.add("has-error");
        var err = wrap.querySelector(".field__error");
        if (err && message) err.textContent = message;
      }

      form.addEventListener("input", function (e) {
        var wrap = e.target.closest(".field") || e.target.closest(".consent");
        if (wrap) wrap.classList.remove("has-error");
      });

      form.addEventListener("submit", function (e) {
        e.preventDefault();
        form.querySelectorAll(".field, .consent").forEach(function (f) { f.classList.remove("has-error"); });

        var required = form.querySelectorAll("[required]");
        var firstBad = null;

        for (var i = 0; i < required.length; i++) {
          var f = required[i];
          var value = (f.type === "checkbox") ? f.checked : f.value.trim();
          if (!value) {
            fail(f, "This field is needed so we can respond.");
            if (!firstBad) firstBad = f;
            continue;
          }
          if (f.type === "tel") {
            var digits = f.value.replace(/\D/g, "");
            if (digits.length < 10) {
              fail(f, "Please enter a 10-digit mobile number.");
              if (!firstBad) firstBad = f;
            }
          }
          if (f.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.value.trim())) {
            fail(f, "Please check the email address.");
            if (!firstBad) firstBad = f;
          }
        }

        if (firstBad) {
          firstBad.focus();
          if (status) {
            status.className = "form-status form-status--warn is-visible";
            status.textContent = "Please complete the highlighted fields.";
          }
          return;
        }

        var data = new FormData(form);
        var lines = ["Admission enquiry — Shyam Public School", ""];
        form.querySelectorAll("input, select, textarea").forEach(function (f) {
          if (!f.name || f.type === "checkbox") return;
          var label = form.querySelector('label[for="' + f.id + '"]');
          var name = label ? label.textContent.replace("*", "").trim() : f.name;
          var val = (data.get(f.name) || "").toString().trim();
          if (val) lines.push(name + ": " + val);
        });
        var body = lines.join("\n");

        var waHref = "https://wa.me/" + SCHOOL.phone.replace("+", "") +
          "?text=" + encodeURIComponent(body);
        var mailHref = "mailto:" + SCHOOL.email +
          "?subject=" + encodeURIComponent("Admission enquiry — " + (data.get("student-name") || "New enquiry")) +
          "&body=" + encodeURIComponent(body);

        if (status) {
          status.className = "form-status form-status--ok is-visible";
          status.innerHTML =
            "Thank you. Your enquiry is ready to send — WhatsApp is opening in a new tab. " +
            'If it does not, <a href="' + waHref + '" target="_blank" rel="noopener">tap here for WhatsApp</a> ' +
            'or <a href="' + mailHref + '">send it by email instead</a>.';
          status.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
        }

        window.open(waHref, "_blank", "noopener");
      });
    });
  }

  /* ---------- Landing on a #fragment ----------
     With smooth scrolling enabled, Chrome starts the fragment jump before web
     fonts and images have settled, so a deep link such as admissions.html#faq
     stops well short of its target. Re-seat the page on the real position once
     everything has loaded — instantly, so it is not seen as a second scroll.
  --------------------------------------------- */
  function initHashLanding() {
    if (!window.location.hash) return;
    var target;
    try { target = document.querySelector(window.location.hash); } catch (e) { return; }
    if (!target) return;

    function settle() {
      var root = document.documentElement;
      var previous = root.style.scrollBehavior;
      root.style.scrollBehavior = "auto";
      target.scrollIntoView();          // scroll-padding-top clears the header
      root.style.scrollBehavior = previous;
    }

    window.addEventListener("load", settle);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(settle);
  }

  /* ---------- Pointer depth and card spotlights ----------
     These effects are deliberately small: they clarify which image or card is
     active without competing with the school's content. Touch devices and
     reduced-motion visitors get the same content with no pointer physics.
  --------------------------------------------- */
  function initImageDepth() {
    if (reduceMotion || !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;

    document.querySelectorAll("[data-tilt]").forEach(function (tile) {
      var frame = 0;

      function update(e) {
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(function () {
          var rect = tile.getBoundingClientRect();
          var x = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
          var y = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));
          tile.style.setProperty("--tilt-x", ((0.5 - y) * 4).toFixed(2) + "deg");
          tile.style.setProperty("--tilt-y", ((x - 0.5) * 4).toFixed(2) + "deg");
          tile.style.setProperty("--shine-x", (x * 100).toFixed(1) + "%");
          tile.style.setProperty("--shine-y", (y * 100).toFixed(1) + "%");
        });
      }

      tile.addEventListener("pointermove", update);
      tile.addEventListener("pointerleave", function () {
        cancelAnimationFrame(frame);
        tile.style.setProperty("--tilt-x", "0deg");
        tile.style.setProperty("--tilt-y", "0deg");
        tile.style.setProperty("--shine-x", "50%");
        tile.style.setProperty("--shine-y", "50%");
      });
    });

    document.querySelectorAll(".card").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        var rect = card.getBoundingClientRect();
        card.style.setProperty("--spot-x", (e.clientX - rect.left).toFixed(0) + "px");
        card.style.setProperty("--spot-y", (e.clientY - rect.top).toFixed(0) + "px");
      });
    });
  }

  /* ---------- Current year ---------- */
  function initYear() {
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    initNav();
    initScrollChrome();
    initReveal();
    initFaq();
    initLightbox();
    initForms();
    initHashLanding();
    initImageDepth();
    initYear();
  });
})();
