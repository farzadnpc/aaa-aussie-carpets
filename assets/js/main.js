/* AAA Aussie Carpets — site script (menu, dropdown, gallery, quote form) */
(function () {
  "use strict";

  var body = document.body;
  var burger = document.querySelector(".burger");
  var dropdownItem = document.querySelector(".has-dropdown");
  var dropdownBtn = document.querySelector(".nav-toggle-sub");
  var desktop = window.matchMedia("(min-width: 1181px)");

  /* ---------- Mobile menu ---------- */
  function setNav(open) {
    body.classList.toggle("nav-open", open);
    if (burger) {
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
  }
  if (burger) {
    burger.addEventListener("click", function () {
      setNav(!body.classList.contains("nav-open"));
    });
  }

  /* ---------- Services dropdown ---------- */
  function setDropdown(open) {
    if (!dropdownItem) return;
    dropdownItem.classList.toggle("open", open);
    dropdownBtn.setAttribute("aria-expanded", String(open));
  }
  var hoverOpenedAt = 0;
  if (dropdownItem && dropdownBtn) {
    dropdownBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      // If the mouse just opened it by hovering, a click shouldn't immediately close it
      if (desktop.matches && Date.now() - hoverOpenedAt < 600) { setDropdown(true); return; }
      setDropdown(!dropdownItem.classList.contains("open"));
    });
    dropdownItem.addEventListener("mouseenter", function () {
      if (desktop.matches && !dropdownItem.classList.contains("open")) { hoverOpenedAt = Date.now(); setDropdown(true); }
    });
    dropdownItem.addEventListener("mouseleave", function () { if (desktop.matches) setDropdown(false); });
    document.addEventListener("click", function (e) {
      if (desktop.matches && !dropdownItem.contains(e.target)) setDropdown(false);
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      if (dropdownItem && dropdownItem.classList.contains("open")) { setDropdown(false); dropdownBtn.focus(); }
      if (body.classList.contains("nav-open")) { setNav(false); burger.focus(); }
      closeLightbox();
    }
  });

  // Close the mobile menu after tapping a link (e.g. jumping to a section)
  document.querySelectorAll(".main-nav a").forEach(function (a) {
    a.addEventListener("click", function () { setNav(false); setDropdown(false); });
  });
  desktop.addEventListener && desktop.addEventListener("change", function () { setNav(false); setDropdown(false); });

  /* ---------- Gallery lightbox ---------- */
  var lightbox = document.querySelector(".lightbox");
  var lightboxImg = lightbox ? lightbox.querySelector("img") : null;
  var lastFocus = null;
  function closeLightbox() {
    if (!lightbox || !lightbox.classList.contains("open")) return;
    lightbox.classList.remove("open");
    body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  if (lightbox) {
    document.querySelectorAll("[data-full]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        lastFocus = btn;
        lightboxImg.src = btn.getAttribute("data-full");
        lightboxImg.alt = btn.querySelector("img").alt;
        lightbox.classList.add("open");
        body.style.overflow = "hidden";
        lightbox.querySelector(".lightbox-close").focus();
      });
    });
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox || e.target.classList.contains("lightbox-close")) closeLightbox();
    });
  }

  /* ---------- Quote form (sent to your email by EmailJS) ----------
     Paste your three EmailJS values below (from emailjs.com):
       publicKey  -> Account > General > Public Key
       serviceId  -> Email Services > your service > Service ID
       templateId -> Email Templates > your template > Template ID
     Until they're filled in, the form asks people to call instead. */
  var EMAILJS = {
    publicKey: "7j1oLuM2A3mmmb_O6",
    serviceId: "service_pv3newe",
    templateId: "template_sh4ox3p"
  };

  var form = document.querySelector(".quote-form");
  if (form) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector(".hp input").value) return; // spam bot
      var configured = [EMAILJS.publicKey, EMAILJS.serviceId, EMAILJS.templateId]
        .every(function (v) { return v && v.indexOf("YOUR_") !== 0; });
      if (!configured) {
        status.className = "form-status err";
        status.textContent = "Online quotes are coming soon — please call us on 0415 850 095 for a free quote.";
        return;
      }
      var data = new FormData(form);
      var params = {
        name: data.get("name") || "",
        phone: data.get("phone") || "",
        email: data.get("email") || "",
        suburb: data.get("suburb") || "",
        service: data.get("service") || "",
        message: data.get("message") || "",
        page: document.title
      };
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      status.className = "form-status";
      status.textContent = "Sending…";
      fetch("https://api.emailjs.com/api/v1.0/email/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          service_id: EMAILJS.serviceId,
          template_id: EMAILJS.templateId,
          user_id: EMAILJS.publicKey,
          template_params: params
        })
      })
        .then(function (res) {
          if (!res.ok) throw new Error("Request failed");
          form.reset();
          status.className = "form-status ok";
          status.textContent = "Thanks! We've got your request and will be in touch shortly.";
        })
        .catch(function () {
          status.className = "form-status err";
          status.textContent = "Sorry, something went wrong. Please call us on 0415 850 095.";
        })
        .finally(function () { btn.disabled = false; });
    });
  }

  /* ---------- Footer year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
