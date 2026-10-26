// Daftar judul halaman (<title>) dinamis untuk setiap slide (01 - 06)
const slideTitles = [
  "LYQU VISUAL — Studio Fotografi & Visual Kreatif Yogyakarta",
  "Koleksi Karya & Portofolio — LYQU VISUAL Yogyakarta",
  "Filosofi Kreatif, Tim & Gear Kamera — LYQU VISUAL Yogyakarta",
  "Paket Harga, Kalender Jadwal & Booking DP — LYQU VISUAL Yogyakarta",
  "Portal Klien: Proofing RAW & Google Drive — LYQU VISUAL Yogyakarta",
  "FAQ Operasional, Kebijakan Studio & Kontak — LYQU VISUAL Yogyakarta"
];

    // 1. CAMERA SHUTTER FLASH EFFECT
    function fireCameraFlash() {
      gsap.fromTo("#shutterFlash",
        { opacity: 0.85 },
        { opacity: 0, duration: 0.45, ease: "power2.out" }
      );
    }

    // 2. CUSTOM VIEWFINDER CURSOR & MAGNETIC BUTTONS
    const cursorEl = document.getElementById('viewfinderCursor');
    window.addEventListener('mousemove', (e) => {
      if (!cursorEl) return;
      gsap.to(cursorEl, { x: e.clientX, y: e.clientY, duration: 0.12, ease: "power2.out" });
    });

    document.querySelectorAll('a, button, select, .frosted-glass').forEach(el => {
      el.addEventListener('mouseenter', () => cursorEl && cursorEl.classList.add('cursor-hover'));
      el.addEventListener('mouseleave', () => cursorEl && cursorEl.classList.remove('cursor-hover'));
    });

    document.querySelectorAll('.magnetic-el').forEach(btn => {
      btn.addEventListener('mousemove', (e) => {
        if (window.innerWidth < 1024) return;
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        gsap.to(btn, { x: x * 0.28, y: y * 0.28, duration: 0.25, ease: "power2.out" });
      });
      btn.addEventListener('mouseleave', () => {
        gsap.to(btn, { x: 0, y: 0, duration: 0.4, ease: "elastic.out(1, 0.4)" });
      });
    });


    function renderBentoGallery(genre) {
      const container = document.getElementById('galleryGrid');
      const items = genre === 'all' ? bentoPortfolioData : bentoPortfolioData.filter(x => Array.isArray(x.genre) ? x.genre.includes(genre) : x.genre === genre);

      container.innerHTML = items.map(item => `
        <div class="gallery-card w-[85vw] max-w-[340px] md:w-auto md:max-w-none shrink-0 snap-center ${item.cardStyle} ${item.imageOverlap ? 'gallery-card--image-overlap' : ''} rounded-[24px] p-4 sm:p-5 relative flex flex-col justify-between shadow-lg mt-2 hover:-translate-y-1 transition">
          <span class="${item.tabStyle} font-hero font-bold text-[9px] sm:text-[10px] px-3 sm:px-3.5 py-1 rounded-full absolute -top-3 right-4 sm:right-5 rotate-2 sm:rotate-3 shadow z-20">
            ${item.pillTab}
          </span>

          <div class="flex flex-col sm:grid sm:grid-cols-12 gap-3 sm:gap-4 items-stretch sm:items-center">
            <div class="order-1 sm:order-2 sm:col-span-5 rounded-xl ${item.imageOverlap ? 'portfolio-image-stage--overlap' : 'overflow-hidden'}">
              <img src="${item.img}" alt="${item.title}" style="object-position: ${item.imgPosition || 'center'};" class="w-full h-36 sm:h-28 object-cover hover:scale-110 transition duration-500" />
            </div>
            <div class="order-2 sm:order-1 sm:col-span-7 space-y-1 sm:space-y-1.5 relative z-10">
              <span class="font-mono text-[10px] uppercase opacity-75">GENRE: ${Array.isArray(item.genre) ? item.genre.join(' & ') : item.genre}</span>
              <h3 class="font-hero font-extrabold text-sm sm:text-base leading-snug">${item.title}</h3>
              <p class="text-[11px] opacity-85 leading-relaxed">${item.desc}</p>
            </div>
          </div>

          <div class="mt-3 pt-2.5 border-t border-current/10 flex items-center justify-between">
            <a href="#slide-4" class="${item.btnStyle} px-3.5 py-1.5 rounded-full font-hero font-bold text-[10px] uppercase inline-flex items-center gap-1.5 shadow-sm">
              <span>Booking Genre Ini</span>
              <span>→</span>
            </a>
            <span class="font-mono text-[10px] opacity-70">WebP &lt; 240KB</span>
          </div>
        </div>
      `).join('');

      gsap.fromTo(".gallery-card",
        { y: 30, opacity: 0, scale: 0.95 },
        { y: 0, opacity: 1, scale: 1, duration: 0.5, stagger: 0.08, ease: "back.out(1.4)" }
      );
    }

    function filterGallery(genre, btnEl) {
      document.querySelectorAll('#portfolioFilters button').forEach(b => {
        b.className = 'shrink-0 px-4 py-1.5 rounded-full text-[11px] font-hero font-bold bg-white/10 text-white hover:bg-cobalt transition';
      });
      btnEl.className = 'shrink-0 px-4 py-1.5 rounded-full text-[11px] font-hero font-bold bg-acid text-obsidian transition';
      renderBentoGallery(genre);
    }

    // 4. TOGGLE LUT KARTU HERO DENGAN EFEK BLITZ KAMERA
    const heroRawState = [false, false];
    function triggerShutterLut(index) {
      fireCameraFlash();
      heroRawState[index] = !heroRawState[index];
      const img = document.getElementById(`heroCardImg${index}`);
      img.style.filter = heroRawState[index] ? 'grayscale(100%) contrast(135%)' : 'none';
    }


let selectedDay = 28;

    function renderMiniCalendar() {
      const grid = document.getElementById('calendarDaysGrid');
      let html = '';
      for (let d = 1; d <= 28; d++) {
        if (bookedDates.includes(d)) {
          html += `<button disabled class="min-w-[34px] min-h-[34px] sm:min-w-[40px] sm:min-h-[40px] flex items-center justify-center rounded bg-neutral-200 text-neutral-400 line-through cursor-not-allowed">${d}</button>`;
        } else if (d === selectedDay) {
          html += `<button onclick="selectCalendarDate(${d})" class="min-w-[34px] min-h-[34px] sm:min-w-[40px] sm:min-h-[40px] flex items-center justify-center rounded bg-cobalt text-white font-bold shadow">${d}</button>`;
        } else {
          html += `<button onclick="selectCalendarDate(${d})" class="min-w-[34px] min-h-[34px] sm:min-w-[40px] sm:min-h-[40px] flex items-center justify-center rounded bg-surface hover:bg-acid transition">${d}</button>`;
        }
      }
      grid.innerHTML = html;
    }

    function selectCalendarDate(day) {
      selectedDay = day;
      document.getElementById('pickedDateText').value = `${day} Okt 2026`;
      renderMiniCalendar();
    }

    // 6. KALKULATOR PAKET & ANIMASI ANGKA DP 30%
    function formatRp(n) {
      return 'Rp ' + n.toLocaleString('id-ID');
    }

    function choosePackage(priceVal, title) {
      document.getElementById('calcPackage').value = priceVal;
      recalculateDp();
      if (window.innerWidth < 1024) {
        const ticket = document.getElementById('booking-ticket');
        if (ticket) ticket.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }

    function recalculateDp() {
      const pkg = parseInt(document.getElementById('calcPackage').value, 10);
      const loc = parseInt(document.getElementById('calcLocation').value, 10);
      const total = pkg + loc;
      const dp = Math.round(total * 0.3);

      document.getElementById('totalEstDisplay').innerText = formatRp(total);
      const dpEl = document.getElementById('bigDpDisplay');
      gsap.fromTo(dpEl, { scale: 1.18 }, { scale: 1, duration: 0.35, ease: "back.out(2)" });
      dpEl.innerText = formatRp(dp);
    }


let filterSelectedActive = false;

    function renderProofingCards() {
      const grid = document.getElementById('proofingCardsGrid');
      const list = filterSelectedActive ? rawPhotos.filter(p => p.selected) : rawPhotos;

      grid.innerHTML = list.map(p => `
        <button type="button" onclick="toggleProofSelection('${p.id}')" aria-pressed="${p.selected}" aria-label="${p.selected ? 'Batalkan pilihan' : 'Pilih'} foto ${p.id}" class="proofing-photo-card shrink-0 cursor-pointer text-left rounded-xl overflow-hidden bg-white shadow-sm border-2 transition hover:-translate-y-0.5 snap-start ${p.selected ? 'border-cobalt' : 'border-transparent'}">
          <div class="relative">
            <img src="${p.img}" alt="${p.id}" loading="lazy" class="w-full h-32 sm:h-36 object-cover transition duration-300 ${p.selected ? '' : 'grayscale contrast-125'}" />
            <span class="absolute top-1.5 right-1.5 px-2 py-0.5 rounded-full font-mono text-[9px] font-bold ${p.selected ? 'bg-acid text-obsidian' : 'bg-obsidian/75 text-white'}">
              ${p.selected ? 'TERPILIH' : 'PILIH'}
            </span>
          </div>
          <div class="px-2.5 py-1.5 flex items-center justify-between font-mono text-[10px]">
            <span class="font-bold truncate max-w-[115px]">${p.id}</span>
            <span class="${p.selected ? 'text-cobalt font-bold' : 'text-neutral-400'}">${p.selected ? 'ANTREAN EDIT' : 'RAW'}</span>
          </div>
        </button>
      `).join('');

      document.getElementById('selectedCounter').innerText = rawPhotos.filter(x => x.selected).length;
    }

    function scrollProofingGallery(direction) {
      const gallery = document.getElementById('proofingCardsGrid');
      const card = gallery.querySelector('.proofing-photo-card');
      if (!card) return;

      const gap = parseFloat(getComputedStyle(gallery).columnGap) || 0;
      gallery.scrollLeft += direction * (card.getBoundingClientRect().width + gap);
    }

    function toggleProofSelection(id) {
      fireCameraFlash();
      const item = rawPhotos.find(x => x.id === id);
      if (item) {
        item.selected = !item.selected;
        renderProofingCards();
      }
    }

    function toggleFilterSelected() {
      filterSelectedActive = !filterSelectedActive;
      document.getElementById('btnOnlySelected').innerText = filterSelectedActive ? 'Semua RAW' : 'Pilihan Saja';
      renderProofingCards();
    }

    function lockProofingChoices() {
      fireCameraFlash();
      const total = rawPhotos.filter(x => x.selected).length;
      document.getElementById('clientProjectStatus').innerText = `Proyek: #LYQ-JGJ-2026 • ${total} Foto Masuk Antrean Grading`;
    }

    // 8. MODAL SSO & QRIS
    let loggedUser = null;

    function openSsoModal() {
      document.getElementById('ssoModal').classList.remove('hidden');
      document.getElementById('ssoModal').classList.add('flex');
    }
    function closeSsoModal() {
      document.getElementById('ssoModal').classList.add('hidden');
      document.getElementById('ssoModal').classList.remove('flex');
    }

    function handleSsoLogin() {
      const name = document.getElementById('ssoName').value || 'Klien Lyqu';
      const email = document.getElementById('ssoEmail').value || 'klien@gmail.com';
      loggedUser = { name, email };

      const shortName = name.split(' ')[0] + ' ✓';
      document.getElementById('navAuthText').innerText = shortName;
      const mobileAuthText = document.getElementById('navAuthTextMobile');
      if (mobileAuthText) mobileAuthText.innerText = shortName;

      document.getElementById('ssoStatusPill').innerText = `SSO: ${email}`;
      document.getElementById('clientNameBadge').innerText = `${name} (${email})`;
      document.getElementById('clientAvatarBadge').innerText = name.charAt(0).toUpperCase();
      closeSsoModal();
    }

    function openInvoiceModal() {
      if (!loggedUser) {
        openSsoModal();
        return;
      }
      const sel = document.getElementById('calcPackage');
      const title = sel.options[sel.selectedIndex].getAttribute('data-title');
      document.getElementById('modalPkgName').innerText = title;
      document.getElementById('modalDateInfo').innerText = `Jadwal Terkunci: ${document.getElementById('pickedDateText').value}`;
      document.getElementById('modalDpAmount').innerText = document.getElementById('bigDpDisplay').innerText;

      document.getElementById('invoiceModal').classList.remove('hidden');
      document.getElementById('invoiceModal').classList.add('flex');
    }

    function closeInvoiceModal() {
      document.getElementById('invoiceModal').classList.add('hidden');
      document.getElementById('invoiceModal').classList.remove('flex');
    }

    function completePayment() {
      closeInvoiceModal();
      fireCameraFlash();
      document.getElementById('clientProjectStatus').innerText = 'Proyek: #LYQ-JGJ-2026 • DP 30% Lunas ✓ (Jadwal Terkunci)';
      document.getElementById('slide-5').scrollIntoView({ behavior: 'smooth' });
    }

    // 9. TAMBAH ULASAN BARU
    function addNewReview() {
      const text = document.getElementById('inputReviewText').value.trim();
      const ratingScore = parseInt(document.getElementById('inputReviewRating').value, 10);
      if (!text) return;

      const author = loggedUser ? loggedUser.name.split(' ')[0] : 'Klien Jogja';
      const html = `
        <div class="w-[82vw] max-w-[310px] md:w-auto md:max-w-none shrink-0 snap-center bg-acid/40 px-4 py-2.5 rounded-xl border-l-4 border-obsidian flex items-center justify-between">
          <p class="text-[11px] text-obsidian truncate">"${text}" — <strong>${author}</strong></p>
          <span class="text-cobalt text-xs font-bold ml-2">${ratingScore}/5</span>
        </div>
      `;
      const container = document.getElementById('testimonialList');
      container.insertAdjacentHTML('afterbegin', html);
      if (container.children.length > 3) container.lastElementChild.remove();
      document.getElementById('inputReviewText').value = '';
    }

    // 10. INTERSECTION OBSERVER: SLIDE ENTRANCE MOTION + ACTIVE NAV LINKS (SIDEBAR & MOBILE BOTTOM BAR)
    window.addEventListener('DOMContentLoaded', () => {
      renderBentoGallery('all');
      renderMiniCalendar();
      renderProofingCards();
      recalculateDp();

      // Matikan VanillaTilt pada perangkat layar sentuh murni agar tap kartu lebih responsif
      if (window.matchMedia && window.matchMedia('(hover: none)').matches) {
        document.querySelectorAll('[data-tilt]').forEach(el => {
          if (el.vanillaTilt) el.vanillaTilt.destroy();
        });
      }

      // Jika dibuka melalui route spesifik (misal /portofolio), scroll ke slide tersebut
      if (typeof window.INITIAL_SLIDE_INDEX === 'number' && window.INITIAL_SLIDE_INDEX > 0) {
        const targetSlide = document.getElementById(`slide-${window.INITIAL_SLIDE_INDEX + 1}`);
        if (targetSlide) {
          targetSlide.scrollIntoView({ behavior: 'instant' });
        }
      }

      // Animasi Pembuka Hero Text 3D
      gsap.fromTo(".hero-line",
        { y: 90, rotateX: -65, opacity: 0 },
        { y: 0, rotateX: 0, opacity: 1, duration: 1, stagger: 0.14, ease: "power4.out" }
      );

      const slides = document.querySelectorAll('.deck-slide');
      const slideLinks = document.querySelectorAll('.slide-link');
      const mobileBottomLinks = document.querySelectorAll('.mobile-bottom-link');
      const sidebarToggle = document.getElementById('sidebarToggleBtn');
      const sidebarBackdrop = document.getElementById('sidebarBackdrop');
      const sidebarClose = document.getElementById('sidebarCloseBtn');

      const closeSidebar = () => {
        document.body.classList.remove('sidebar-open');
        sidebarToggle.setAttribute('aria-expanded', 'false');
        sidebarToggle.setAttribute('aria-label', 'Buka navigasi slide');
      };

      sidebarToggle.addEventListener('click', () => {
        const isOpen = document.body.classList.toggle('sidebar-open');
        sidebarToggle.setAttribute('aria-expanded', String(isOpen));
        sidebarToggle.setAttribute('aria-label', isOpen ? 'Tutup navigasi slide' : 'Buka navigasi slide');
      });

      sidebarBackdrop.addEventListener('click', closeSidebar);
      sidebarClose.addEventListener('click', closeSidebar);

      slideLinks.forEach(link => {
        link.addEventListener('click', closeSidebar);
      });

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const idx = Array.from(slides).indexOf(entry.target);

            // Update tag <title> sesuai slide yang sedang aktif
            if (slideTitles[idx]) {
              document.title = slideTitles[idx];
            }

            // Update active state pada navigasi sidebar
            slideLinks.forEach((link, i) => {
              const isActive = i === idx;
              link.classList.toggle('is-active', isActive);
              if (isActive) {
                link.setAttribute('aria-current', 'page');
              } else {
                link.removeAttribute('aria-current');
              }
            });

            // Update active state pada Mobile Bottom Navigation Bar
            mobileBottomLinks.forEach((link, i) => {
              const isActive = i === idx;
              link.classList.toggle('is-active', isActive);
              if (isActive) {
                link.setAttribute('aria-current', 'page');
              } else {
                link.removeAttribute('aria-current');
              }
            });

            // Trigger Staggered Entrance pada Elemen di Slide Aktif
            const animEls = entry.target.querySelectorAll('.anim-el');
            gsap.fromTo(animEls,
              { y: 40, opacity: 0, scale: 0.96 },
              { y: 0, opacity: 1, scale: 1, duration: 0.65, stagger: 0.09, ease: "back.out(1.3)", overwrite: true }
            );

            // Trigger Self-Drawing SVG Paths di Slide Aktif
            entry.target.querySelectorAll('.svg-draw').forEach(path => {
              const len = path.getTotalLength ? path.getTotalLength() : 900;
              gsap.fromTo(path,
                { strokeDasharray: len, strokeDashoffset: len },
                { strokeDashoffset: 0, duration: 1.6, ease: "power2.out", overwrite: true }
              );
            });

            // Trigger Animated Number Counters
            entry.target.querySelectorAll('.counter-num').forEach(counter => {
              const targetVal = parseInt(counter.getAttribute('data-target'), 10);
              gsap.fromTo(counter,
                { innerText: 0 },
                {
                  innerText: targetVal,
                  duration: 1.4,
                  snap: { innerText: 1 },
                  ease: "power2.out"
                }
              );
            });
          }
        });
      }, { threshold: window.innerWidth < 1024 ? 0.25 : 0.45 });

      slides.forEach(s => observer.observe(s));
    });
