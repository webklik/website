/**
 * Mister Wok Engine
 * Handles:
 * - Relationship Memory (localStorage for user details)
 * - Platform Awareness (desktop vs mobile CTA behavior)
 * - Event Tracking (DataLayer push)
 * - Abandon-Cart Detection
 *
 * Container: GTM-WGQ2FPZR
 */

(function() {
  'use strict';

  const CONFIG = {
    storagePrefix: 'mw_',
    abandonCartThreshold: 3000,
    orderRecentThreshold: 86400000,
  };

  const BRANCHES = {
    'parklands': {
      name: 'Parklands',
      location: 'Kolobot Road, Parklands',
      phone: '+254724100100',
      rating: '4.3',
      hours: '11am-11pm'
    },
    'capital-centre': {
      name: 'Capital Centre',
      location: 'Capital Centre Mall, Mombasa Road',
      phone: '+254722248248',
      rating: '4.2',
      hours: '11am-9:30pm'
    },
    'two-rivers': {
      name: 'Two Rivers',
      location: 'Two Rivers Mall, Limuru Road',
      phone: '+254753222222',
      rating: '4.1',
      hours: '11am-9pm'
    }
  };

  const Memory = {
    get: function(key) {
      try {
        return localStorage.getItem(CONFIG.storagePrefix + key);
      } catch (_) {
        return null;
      }
    },
    set: function(key, value) {
      try {
        localStorage.setItem(CONFIG.storagePrefix + key, value);
        return true;
      } catch (e) {
        console.warn('localStorage full or unavailable:', e);
        return false;
      }
    },
    getAll: function() {
      return {
        user_name: this.get('user_name'),
        user_phone: this.get('user_phone'),
        user_address: this.get('user_address'),
        last_order_time: this.get('last_order_time'),
        last_order_branch: this.get('last_order_branch')
      };
    },
    hasOrderedRecently: function() {
      const lastOrderTime = this.get('last_order_time');
      if (!lastOrderTime) return false;
      const lastOrder = parseInt(lastOrderTime, 10);
      if (Number.isNaN(lastOrder)) return false;
      return (Date.now() - lastOrder) < CONFIG.orderRecentThreshold;
    },
    clear: function() {
      ['user_name', 'user_phone', 'user_address', 'last_order_time', 'last_order_branch', 'last_branch_selected'].forEach(function(key) {
        try {
          localStorage.removeItem(CONFIG.storagePrefix + key);
        } catch (_) {}
      });
    }
  };

  const Platform = {
    isMobile: function() {
      return /iPhone|iPad|Android|webOS|BlackBerry|Windows Phone|mobile/i.test(navigator.userAgent);
    },
    isDesktop: function() {
      return !this.isMobile();
    }
  };

  const Tracking = {
    push: function(eventObject) {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(eventObject);
      if (window.console && typeof console.log === 'function') {
        console.log('[GTM Event]', eventObject.event, eventObject);
      }
    },
    trackMenuView: function(branch) {
      this.push({
        event: 'view_menu',
        branch: branch,
        menu_url: window.location.href,
        referrer: document.referrer,
        user_device: Platform.isMobile() ? 'mobile' : 'desktop',
        timestamp: new Date().toISOString()
      });
    },
    trackBranchSelected: function(branchSource) {
      const fromElement = branchSource && typeof branchSource.getAttribute === 'function';
      const branchData = fromElement ? {
        name: branchSource.getAttribute('data-branch'),
        location: branchSource.getAttribute('data-branch-location'),
        phone: branchSource.getAttribute('data-branch-phone'),
        rating: branchSource.getAttribute('data-branch-rating'),
        hours: branchSource.getAttribute('data-branch-hours')
      } : (branchSource || {});

      if (!branchData.name) return;
      this.push({
        event: 'branch_selected',
        branch_name: branchData.name,
        branch_location: branchData.location,
        branch_phone: branchData.phone,
        branch_rating: branchData.rating,
        branch_hours: branchData.hours,
        user_first_time: !Memory.get('last_branch_selected'),
        timestamp: new Date().toISOString()
      });
      if (isBranchPage()) {
        Memory.set('last_branch_selected', branchData.name);
      }
    },
    trackWhatsAppOrder: function(branch) {
      this.push({
        event: 'initiate_whatsapp_order',
        branch: branch,
        user_name: Memory.get('user_name') || 'Unknown',
        user_phone: Memory.get('user_phone') || 'Unknown',
        user_address: Memory.get('user_address') || 'Unknown',
        device_type: Platform.isMobile() ? 'mobile' : 'desktop',
        conversion_type: 'relationship',
        user_has_ordered_before: Memory.hasOrderedRecently(),
        timestamp: new Date().toISOString()
      });
    },
    trackDirectOrder: function(orderData) {
      this.push({
        event: 'gloria_order_complete',
        order_id: orderData.id || ('DIRECT_' + Date.now()),
        branch: orderData.branch || this.getCurrentBranch(),
        order_value: orderData.value || '0',
        currency: 'KES',
        delivery_method: orderData.delivery_method || 'delivery',
        user_is_repeat: Memory.hasOrderedRecently(),
        conversion_type: 'system',
        timestamp: new Date().toISOString()
      });

      Memory.set('last_order_time', Date.now().toString());
      Memory.set('last_order_branch', orderData.branch || this.getCurrentBranch());
    },
    trackAbandonCart: function() {
      const timeOnPage = Math.round((Date.now() - window.pageLoadTime) / 1000);
      this.push({
        event: 'abandon_cart',
        time_on_page: timeOnPage,
        branch_viewed: this.getCurrentBranch(),
        page_type: this.getPageType(),
        device: 'desktop',
        scroll_depth: window.scrollY || 0,
        timestamp: new Date().toISOString()
      });
    },
    trackContactBranch: function(method, phone, branch) {
      this.push({
        event: 'contact_branch',
        branch: branch || this.getCurrentBranch(),
        phone: phone || 'Unknown',
        contact_method: method,
        timestamp: new Date().toISOString()
      });
    },
    getCurrentBranch: function() {
      const url = window.location.pathname;
      if (url.includes('parklands')) return 'Parklands';
      if (url.includes('capital-centre')) return 'Capital Centre';
      if (url.includes('two-rivers')) return 'Two Rivers';
      return 'Unknown';
    },
    getPageType: function() {
      const url = window.location.pathname;
      // Branch landing pages live at /parklands/, /capital-centre/, /two-rivers/
      // (index.html implicit). Match before the homepage rule so they don't
      // collide with the root index.
      if (/^\/(parklands|capital-centre|two-rivers)\/?(index\.html)?$/.test(url)) return 'branch_landing';
      if (url === '/' || url === '/index.html') return 'homepage';
      if (url.includes('menu')) return 'menu';
      if (url.includes('journal') || /halal-wok|long-grain-aromatic-rice|falcon-rice|wok-hei|spring-rolls|ntv-am-live|birthday-catering/.test(url)) return 'article';
      if (url.includes('catering')) return 'catering';
      if (url.includes('videos')) return 'videos';
      return 'page';
    }
  };

  const AbandonCart = {
    init: function() {
      if (!Platform.isDesktop()) return;
      let mouseOutTimer = null;

      document.addEventListener('mouseleave', function() {
        clearTimeout(mouseOutTimer);
        mouseOutTimer = setTimeout(function() {
          Tracking.trackAbandonCart();
        }, CONFIG.abandonCartThreshold);
      });

      document.addEventListener('mouseenter', function() {
        clearTimeout(mouseOutTimer);
      });
    }
  };

  // ──────────────────────────────────────────────────────────
  // Modal: Phase 1B branch selector with mode-aware href swap.
  // Modes: 'order' | 'reserve' | 'call'
  //   order   -> opt.href = opt.dataset.orderUrl       (GloriaFood order)
  //   reserve -> opt.href = opt.dataset.reserveUrl     (GloriaFood reserve)
  //   call    -> opt.href = 'tel:' + opt.dataset.branchPhone
  // History API: pushState on open, popstate listener so Android back
  // button closes the modal instead of leaving the page.
  // ──────────────────────────────────────────────────────────
  const Modal = {
    el: null,
    isOpen: false,
    historyPushed: false,
    copy: {
      order:   { title: 'Choose Your Branch',          sub: 'Delivery radius varies by branch. Pick the one nearest you.' },
      reserve: { title: 'Reserve Table — Choose Branch', sub: 'Reserve via FoodBooking at your preferred branch.' },
      call:    { title: 'Call Your Branch',             sub: 'Tap a branch to call directly. Each branch has its own line.' },
      menu:    { title: 'View the Menu Online',         sub: 'Full menu with prices for your nearest branch.' },
      find:    { title: 'Get Directions',               sub: 'Opens Google Maps with directions to your branch.' }
    },

    titleIcons: {
      call:  'ico-phone',
      order: 'ico-cart',
      menu:  'ico-fork-knife',
      find:  'ico-car'
    },

    setTitle: function(mode, titleText) {
      if (!this.titleEl) return;
      var iconId = this.titleIcons[mode] || this.titleIcons.order;
      var iconSize = mode === 'find' ? 28 : 24;
      this.titleEl.innerHTML =
        '<span class="modal-title-icon modal-title-icon--' + mode + '" aria-hidden="true">' + svgUse(iconId, iconSize) + '</span>' +
        '<span class="modal-title-text">' + titleText + '</span>';
    },

    focusBranchPicker: function() {
      if (!this.el) return;
      var inner = this.el.querySelector('.modal-inner');
      var first = this.el.querySelector('.modal-options .modal-opt');
      if (inner) inner.scrollTop = 0;
      if (!first) return;
      requestAnimationFrame(function() {
        try { first.focus({ preventScroll: true }); } catch (_) { first.focus(); }
      });
    },

    setChinActive: function(mode) {
      document.querySelectorAll('#bottom-nav .bn-tab').forEach(function(t) {
        t.classList.remove('bn-tab--active');
      });
      document.querySelectorAll('.hero-action-btn').forEach(function(t) {
        t.classList.remove('hero-action-btn--active');
      });
      if (!mode) return;
      var activeTab = document.getElementById('bn-' + mode);
      if (activeTab) activeTab.classList.add('bn-tab--active');
      var heroTab = document.getElementById('hero-' + mode + '-cta');
      if (heroTab) heroTab.classList.add('hero-action-btn--active');
    },

    init: function() {
      this.el = document.getElementById('modal');
      if (!this.el) return; // page has no modal (branch pages skip it)

      const titleEl = this.el.querySelector('.modal-title');
      const subEl = this.el.querySelector('.modal-sub');
      const options = this.el.querySelectorAll('.modal-opt');
      const closeBtn = this.el.querySelector('.modal-close, #modal-close');
      const self = this;

      this.titleEl = titleEl;
      this.subEl = subEl;
      this.options = options;

      // Trigger bindings (any element marked with the relevant data attribute)
      document.querySelectorAll('[data-modal-trigger]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
          var mode = btn.getAttribute('data-modal-trigger') || 'order';
          if (isBranchPage()) {
            e.preventDefault();
            e.stopPropagation();
            if (mode === 'order') {
              var url = getBranchGloriaUrl();
              if (url) window.open(url, '_blank', 'noopener');
            } else if (mode === 'call') {
              var phone = getBranchPhone();
              if (phone) window.location.href = 'tel:' + phone.replace(/\s+/g, '');
            } else if (mode === 'menu') {
              var menuUrl = isMenuPage() ? getBranchHomeUrl() : getBranchMenuUrl();
              if (menuUrl) window.location.href = menuUrl;
            } else if (mode === 'find') {
              var findUrl = getBranchFindUrl();
              if (findUrl) window.open(findUrl, '_blank', 'noopener');
            }
            return;
          }
          e.preventDefault();
          e.stopPropagation();
          if (self.isOpen && self.currentMode === mode) {
            self.close();
          } else {
            self.open(mode);
          }
        });
      });

      // Legacy class hooks from Phase 1A (preserve behaviour)
      document.querySelectorAll('.order-trigger').forEach(function(btn) {
        if (btn.hasAttribute('data-modal-trigger')) return;
        btn.addEventListener('click', function(e) {
          if (isBranchPage()) return;
          e.preventDefault();
          self.open('order');
        });
      });
      document.querySelectorAll('.reserve-trigger').forEach(function(btn) {
        if (btn.hasAttribute('data-modal-trigger')) return;
        btn.addEventListener('click', function(e) { e.preventDefault(); self.open('reserve'); });
      });
      document.querySelectorAll('.call-trigger').forEach(function(btn) {
        if (btn.hasAttribute('data-modal-trigger')) return;
        btn.addEventListener('click', function(e) { e.preventDefault(); self.open('call'); });
      });

      // Close handlers
      if (closeBtn) closeBtn.addEventListener('click', function() { self.close(); });
      this.el.addEventListener('click', function(e) {
        if (e.target === self.el) self.close();
      });
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && self.isOpen) self.close();
      });

      // Track branch selection; persist branch memory only on branch-level pages
      options.forEach(function(opt) {
        opt.addEventListener('click', function() {
          const slug = opt.getAttribute('data-branch-slug') || opt.getAttribute('data-branch');
          if (slug && isBranchPage()) {
            Memory.set('last_order_branch', slug);
          }
          Tracking.trackBranchSelected(opt);
        });
      });

      // History API: back button closes modal rather than navigating away
      window.addEventListener('popstate', function(e) {
        if (self.isOpen) {
          self.historyPushed = false; // popstate already consumed our entry
          self.close(true);
        }
      });
    },

    open: function(mode) {
      if (!this.el) return;
      const m = this.copy[mode] ? mode : 'order';
      const text = this.copy[m];
      this.setTitle(m, text.title);
      if (this.subEl) this.subEl.textContent = text.sub;

      // Rewrite href on each option to match the requested action
      this.options.forEach(function(opt) {
        let target = '#';
        if (m === 'order')   target = opt.getAttribute('data-order-url')   || target;
        if (m === 'reserve') target = opt.getAttribute('data-reserve-url') || target;
        if (m === 'call') {
          const phone = opt.getAttribute('data-branch-phone');
          if (phone) target = 'tel:' + phone.replace(/\s+/g, '');
        }
        if (m === 'menu') target = opt.getAttribute('data-menu-url') || target;
        if (m === 'find') target = opt.getAttribute('data-find-url') || target;
        opt.setAttribute('href', target);
        // menu stays same-window; find and order open new tab; tel stays same-window
        if (m === 'call' || m === 'menu') {
          opt.removeAttribute('target');
          opt.removeAttribute('rel');
        } else {
          opt.setAttribute('target', '_blank');
          opt.setAttribute('rel', 'noopener');
        }
      });

      this.el.classList.add('open');
      this.el.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      this.isOpen = true;
      this.currentMode = m;

      this.setChinActive(m);
      this.focusBranchPicker();

      // Push a history state so Android hardware-back closes the modal
      if (window.history && typeof window.history.pushState === 'function') {
        try {
          window.history.pushState({ mwModal: true, mode: m }, '');
          this.historyPushed = true;
        } catch (_) {}
      }

      Tracking.push({
        event: 'modal_opened',
        modal_mode: m,
        page_type: Tracking.getPageType(),
        timestamp: new Date().toISOString()
      });
    },

    close: function(fromPopstate) {
      if (!this.el || !this.isOpen) return;
      this.el.classList.remove('open');
      this.el.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      this.isOpen = false;

      // Clear chin + hero active state
      this.setChinActive(null);

      // Hide the edit-details form if it was left open
      const form = document.getElementById('edit-details-form');
      if (form) form.style.display = 'none';

      // If we pushed a history entry and this close isn't itself triggered by
      // popstate, walk back so the URL bar is clean.
      if (this.historyPushed && !fromPopstate && window.history && typeof window.history.back === 'function') {
        this.historyPushed = false;
        try { window.history.back(); } catch (_) {}
      }
    }
  };

  const OrderCTA = {
    updateCTAText: function() {
      if (!isBranchPage()) return;

      const orderButtons = document.querySelectorAll('[data-order-btn]:not(.modal-opt)');

      if (Memory.hasOrderedRecently()) {
        orderButtons.forEach(function(btn) {
          if (btn.closest('[data-hero-cta]') || btn.closest('.dish-card') || btn.closest('.takeaway-banner') || btn.closest('#bottom-nav')) return;
          if (btn.querySelector('.cta-flame, .flame')) return;
          btn.textContent = 'Re-order Your Favorites?';
          btn.setAttribute('data-repeat', 'true');
        });
      } else {
        orderButtons.forEach(function(btn) {
          if (btn.closest('[data-hero-cta]') || btn.closest('.dish-card') || btn.closest('.takeaway-banner') || btn.closest('#bottom-nav')) return;
          if (btn.querySelector('.cta-flame, .flame')) return;
          btn.textContent = 'Order Now';
          btn.removeAttribute('data-repeat');
        });
      }
    },
    captureUserDetails: function(form) {
      if (!form) return;
      form.addEventListener('submit', function() {
        const nameInput = form.querySelector('input[name="name"]');
        const phoneInput = form.querySelector('input[name="phone"]');
        const addressInput = form.querySelector('input[name="address"]');

        if (nameInput) Memory.set('user_name', nameInput.value || '');
        if (phoneInput) Memory.set('user_phone', phoneInput.value || '');
        if (addressInput) Memory.set('user_address', addressInput.value || '');
      });
    }
  };

  const BRANCH_GLORIA_ORDER_URL = {
    'Parklands': 'https://www.foodbooking.com/api/fb/67_y_m',
    'Capital Centre': 'https://www.foodbooking.com/api/fb/d_yq_g',
    'Two Rivers': 'https://www.foodbooking.com/api/fb/k8_d_z'
  };

  const MW_LAST_BRANCH_KEY = 'mw_last_branch';

  function openBranchSelector() {
    Modal.open('order');
  }

  function isBranchPage() {
    const path = window.location.pathname;
    return /\/(parklands|capital-centre|two-rivers)\//i.test(path);
  }

  function isMenuPage() {
    const path = window.location.pathname;
    return /\/(parklands|capital-centre|two-rivers)\/menu\.html$/i.test(path);
  }

  function getBranchHomeUrl() {
    const path = window.location.pathname;
    if (/parklands/i.test(path))      return '/parklands/';
    if (/capital-centre/i.test(path)) return '/capital-centre/';
    if (/two-rivers/i.test(path))     return '/two-rivers/';
    return '/';
  }

  function getBranchGloriaUrl() {
    const path = window.location.pathname;
    if (/parklands/i.test(path)) return BRANCH_GLORIA_ORDER_URL['Parklands'];
    if (/capital-centre/i.test(path)) return BRANCH_GLORIA_ORDER_URL['Capital Centre'];
    if (/two-rivers/i.test(path)) return BRANCH_GLORIA_ORDER_URL['Two Rivers'];
    return null;
  }

  function getBranchPhone() {
    const path = window.location.pathname;
    if (/parklands/i.test(path))      return '+254724100100';
    if (/capital-centre/i.test(path)) return '+254722248248';
    if (/two-rivers/i.test(path))     return '+254753222222';
    return null;
  }

  function getBranchMenuUrl() {
    const path = window.location.pathname;
    if (/parklands/i.test(path))      return '/parklands/menu.html';
    if (/capital-centre/i.test(path)) return '/capital-centre/menu.html';
    if (/two-rivers/i.test(path))     return '/two-rivers/menu.html';
    return null;
  }

  function getBranchFindUrl() {
    const path = window.location.pathname;
    if (/parklands/i.test(path))      return 'https://www.google.com/maps/place/Mister+Wok+Parklands/@-1.2689288,36.8010833,14.67z/data=!4m6!3m5!1s0x182f17250fd1b1b7:0xbd19122fb0b6b0cc!8m2!3d-1.2701858!4d36.8163282!16s%2Fg%2F1pwfbvqq8?entry=tts';
    if (/capital-centre/i.test(path)) return 'https://www.google.com/maps/place/Mister+Wok+Capital+Centre/@-1.3158532,36.8322619,17z/data=!3m2!4b1!5s0x182f11af9fd6ebef:0x23e467a66242813c!4m6!3m5!1s0x182f11af745976ff:0x535fec0e200c01e9!8m2!3d-1.3158586!4d36.8348368!16s%2Fg%2F1tf9dfy_?entry=tts';
    if (/two-rivers/i.test(path))     return 'https://www.google.com/maps/place/Mister+Wok+Two+Rivers/@-1.2108474,36.7935251,17z/data=!3m1!4b1!4m6!3m5!1s0x182f172507130c6f:0xfa26da9db0b374d1!8m2!3d-1.2108528!4d36.7961!16s%2Fg%2F1hf0cy20z?entry=tts';
    return null;
  }

  const NavDrawer = {
    drawer: null,
    toggle: null,
    backdrop: null,
    bound: false,

    init: function() {
      this.drawer = document.getElementById('drawer') || document.getElementById('site-nav-drawer');
      this.toggle = document.getElementById('ham') || document.getElementById('nav-toggle');
      if (!this.drawer || !this.toggle || this.bound) return;

      this.ensureBackdrop();
      var self = this;

      this.toggle.addEventListener('click', function(e) {
        e.stopPropagation();
        self.setOpen(!self.drawer.classList.contains('open'));
      });

      if (this.backdrop) {
        this.backdrop.addEventListener('click', function() { self.setOpen(false); });
      }

      document.addEventListener('click', function(e) {
        if (!self.drawer.classList.contains('open')) return;
        if (self.drawer.contains(e.target) || self.toggle.contains(e.target)) return;
        self.setOpen(false);
      });

      this.drawer.querySelectorAll('a, button.drawer-order-btn').forEach(function(el) {
        el.addEventListener('click', function() { self.setOpen(false); });
      });

      this.drawer.querySelectorAll('details.drawer-accordion').forEach(function(details) {
        details.addEventListener('toggle', function() {
          if (!details.open) return;
          self.drawer.querySelectorAll('details.drawer-accordion').forEach(function(other) {
            if (other !== details) other.open = false;
          });
        });
      });

      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && self.drawer.classList.contains('open')) self.setOpen(false);
      });

      this.bound = true;
    },

    ensureBackdrop: function() {
      this.backdrop = document.getElementById('nav-backdrop');
      if (!this.backdrop) {
        this.backdrop = document.createElement('div');
        this.backdrop.id = 'nav-backdrop';
        this.backdrop.setAttribute('aria-hidden', 'true');
        this.backdrop.style.cssText = 'display:none;position:fixed;inset:0;z-index:8999;background:rgba(0,0,0,0.55)';
        document.body.appendChild(this.backdrop);
      }
    },

    setOpen: function(open) {
      this.drawer.classList.toggle('open', open);
      this.toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      this.drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
      document.body.classList.toggle('nav-open', open);
      if (this.backdrop) this.backdrop.style.display = open ? 'block' : 'none';
    }
  };

  function injectAuditStyles() {
    if (document.getElementById('mw-audit-fixes')) return;
    var style = document.createElement('style');
    style.id = 'mw-audit-fixes';
    style.textContent = [
      '#drawer,.drawer{position:fixed!important;top:0!important;right:0!important;height:100%!important;',
      'max-width:min(320px,88vw)!important;width:min(320px,88vw)!important;z-index:9000!important;',
      'transform:translateX(100%);transition:transform .25s ease;}',
      '#drawer.open,.drawer.open{transform:translateX(0);}',
      '#modal{z-index:8500!important;}',
      '#bottom-nav{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;',
      'position:fixed;bottom:0;left:0;right:0;background:#0a0a0a;',
      'border-top:1px solid rgba(212,175,55,0.2);padding-bottom:env(safe-area-inset-bottom,0px);',
      'z-index:8000;height:64px;gap:0!important;align-items:stretch!important;}',
      '#bottom-nav .bn-tab,#bottom-nav .bn-btn,#bottom-nav>a,#bottom-nav>button{',
      'display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:flex-end!important;',
      'gap:0!important;padding:6px 2px 8px!important;min-width:0!important;width:100%!important;max-width:none!important;',
      'font-size:10px;letter-spacing:.08em;color:rgba(255,255,255,0.55);text-decoration:none;',
      'transition:color .2s,background .2s;border:none;background:transparent;min-height:0;flex:none;box-sizing:border-box!important;}',
      '#bottom-nav .bn-icon,#bottom-nav .bn-tab>span.bn-icon,#bottom-nav .bn-tab>span:first-child,#bottom-nav .bn-btn>span:first-child{',
      'flex:1 1 auto!important;display:flex!important;align-items:center!important;justify-content:center!important;',
      'min-height:22px!important;width:100%!important;margin:0!important;padding:0!important;line-height:0!important;}',
      '#bottom-nav .bn-icon svg,#bottom-nav .bn-tab>span:first-child svg{width:20px!important;height:20px!important;display:block!important;}',
      '#bottom-nav .bn-label{flex:0 0 11px!important;height:11px!important;line-height:11px!important;',
      'white-space:nowrap!important;font-size:8px!important;font-weight:600!important;letter-spacing:.1em!important;',
      'text-transform:uppercase!important;display:block!important;text-align:center!important;margin:0!important;}',
      '#bottom-nav .bn-cta .bn-label,#bottom-nav .bn-order .bn-label{font-size:8px!important;letter-spacing:.1em!important;}',
      '#bottom-nav .bn-tab:active,#bottom-nav .bn-btn:active{color:#d4af37;}',
      '#bottom-nav .bn-tab--active{color:#d4af37!important;background:rgba(212,175,55,0.12)!important;}',
      '#bottom-nav .bn-cta:not(.bn-tab--active),#bottom-nav .bn-order:not(.bn-tab--active){background:transparent!important;color:rgba(255,255,255,0.55)!important;}',
      '#bottom-nav .bn-cta:not(.bn-tab--active) .bn-label{color:rgba(255,255,255,0.55)!important;}',
      '#bottom-nav .bn-cta.bn-tab--active,#bottom-nav .bn-order.bn-tab--active{background:#d4af37!important;color:#0a0a0a!important;}',
      '#bottom-nav .bn-cta.bn-tab--active .bn-label{color:#0a0a0a!important;}',
      '.modal-title{display:flex;align-items:center;gap:4px;line-height:1.2;}',
      '.modal-title-icon{display:inline-flex;align-items:center;justify-content:center;line-height:0;flex-shrink:0;width:28px;height:28px;}',
      '.modal-title-icon svg{display:block;width:100%;height:100%;}',
      '.modal-title-text{flex:0 1 auto;}',
      '.modal-opt:focus,.modal-opt:focus-visible{outline:2px solid #d4af37;outline-offset:2px;}',
      '#bottom-nav .bn-cta,#bottom-nav .bn-order{background:#d4af37!important;color:#0a0a0a!important;border-radius:6px!important;',
      'flex-direction:column!important;align-items:center!important;justify-content:flex-end!important;padding:6px 2px 8px!important;}',
      '#bottom-nav .bn-cta:active,#bottom-nav .bn-order:active{background:#c49b2e!important;}',
      '@media(max-width:1023px){body{padding-bottom:calc(64px + env(safe-area-inset-bottom,0px))!important;}}',
      '@keyframes mw-fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}',
      'main,.page-body,.page{animation:mw-fade .35s ease forwards}',
      '@media(max-width:1023px){section{padding:48px 24px}section+section,.card+.card{margin-bottom:40px}}',
      '@media(min-width:1024px){#bottom-nav{display:none!important;}}',
      '@keyframes mw-flicker{',
      '0%{transform:scaleY(1) rotate(-1deg);filter:brightness(1.05);opacity:1;}',
      '30%{transform:scaleY(0.97) rotate(1deg);filter:brightness(1.15);opacity:0.95;}',
      '60%{transform:scaleY(1.04) rotate(-0.5deg);filter:brightness(1);opacity:0.88;}',
      '100%{transform:scaleY(1) rotate(0deg);filter:brightness(1.05);opacity:1;}}',
      '.mw-flame{display:inline-block;animation:mw-flicker 1.8s ease-in-out infinite;',
      'transform-origin:bottom center;will-change:transform,filter;vertical-align:middle;}',
      '#bottom-nav .mw-flame{vertical-align:top!important;display:flex!important;align-items:center!important;justify-content:center!important;}',
      '.hero-cta .flame,.hero-cta .cta-flame,.hero-action-btn--cta .cta-flame{margin-right:8px;}',
      '.hero-cta .flame svg,.hero-cta .cta-flame svg,.hero-action-btn--cta .cta-flame svg{width:26px!important;height:26px!important;display:block;}',
      '.nav-order .cta-flame svg,.mob-order .cta-flame svg{width:20px!important;height:20px!important;display:block;}',
      '.drawer-order-btn .cta-flame svg{width:20px!important;height:20px!important;display:block;}',
      '#bottom-nav .bn-cta .bn-icon svg,#bottom-nav .bn-order .bn-icon svg{width:20px!important;height:20px!important;display:block!important;}'
    ].join('');
    document.head.appendChild(style);
  }

  const QuickLook = {
    lastTrigger: null,
    lastDishId: null,

    init: function() {
      var modal = document.getElementById('ql-modal');
      var orderBtn = document.getElementById('ql-order-btn');
      if (!modal || !orderBtn) return;

      var self = this;
      var closeBtn = document.getElementById('ql-close');
      var backdrop = document.getElementById('ql-backdrop');
      var imgEl = document.getElementById('ql-img');

      orderBtn.addEventListener('click', function(e) {
        if (!isBranchPage()) {
          e.preventDefault();
          self.close();
          Modal.open('order');
        }
      });

      document.querySelectorAll('[data-ql-trigger]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
          e.preventDefault();
          e.stopPropagation();
          var article = btn.closest('article.dish-card');
          if (!article) return;
          self.openFromCard(article, btn);
        });
      });

      if (closeBtn) closeBtn.addEventListener('click', function() { self.close(); });
      if (backdrop) backdrop.addEventListener('click', function() { self.close(); });

      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('open')) self.close();
      });
    },

    openFromCard: function(article, triggerBtn) {
      var modal = document.getElementById('ql-modal');
      var orderBtn = document.getElementById('ql-order-btn');
      var imgEl = document.getElementById('ql-img');
      if (!modal || !orderBtn || !imgEl) return;

      this.lastTrigger = triggerBtn;
      this.lastDishId = article.getAttribute('data-dish-id') || '';

      var name = article.getAttribute('data-ql-name') || '';
      var desc = article.getAttribute('data-ql-desc') || '';
      var price = article.getAttribute('data-ql-price') || '';
      var tag = article.getAttribute('data-ql-tag') || '';
      var src = article.getAttribute('data-ql-src') || '';

      imgEl.src = src;
      imgEl.alt = name;
      var elTag = document.getElementById('ql-tag');
      var elName = document.getElementById('ql-name');
      var elDesc = document.getElementById('ql-desc');
      var elPrice = document.getElementById('ql-price');
      if (elTag) elTag.textContent = tag;
      if (elName) elName.textContent = name;
      if (elDesc) elDesc.textContent = desc;
      if (elPrice) elPrice.textContent = price;

      if (!isBranchPage()) {
        orderBtn.setAttribute('href', '#');
        orderBtn.removeAttribute('target');
        orderBtn.removeAttribute('rel');
      } else {
        var branch = Tracking.getCurrentBranch();
        var url = BRANCH_GLORIA_ORDER_URL[branch];
        if (url) {
          orderBtn.setAttribute('href', url);
          orderBtn.setAttribute('target', '_blank');
          orderBtn.setAttribute('rel', 'noopener');
        }
      }

      modal.classList.add('open');
      modal.setAttribute('aria-hidden', 'false');

      var mainEl = document.getElementById('mw-main');
      if (mainEl) mainEl.setAttribute('inert', '');

      Tracking.push({
        event: 'quick_look_open',
        dish_id: this.lastDishId,
        dish_name: name,
        branch: Tracking.getCurrentBranch(),
        timestamp: new Date().toISOString()
      });
    },

    close: function() {
      var modal = document.getElementById('ql-modal');
      var imgEl = document.getElementById('ql-img');
      if (!modal || !modal.classList.contains('open')) return;

      var dishId = this.lastDishId;
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
      if (imgEl) imgEl.src = '';

      var mainEl = document.getElementById('mw-main');
      if (mainEl) mainEl.removeAttribute('inert');

      if (this.lastTrigger && typeof this.lastTrigger.focus === 'function') {
        try { this.lastTrigger.focus(); } catch (_) {}
      }

      Tracking.push({
        event: 'quick_look_close',
        dish_id: dishId,
        branch: Tracking.getCurrentBranch(),
        timestamp: new Date().toISOString()
      });

      this.lastTrigger = null;
      this.lastDishId = null;
    }
  };

  function clearSavedBranchOnGlobalPage() {
    if (isBranchPage()) return;
    try { localStorage.removeItem(MW_LAST_BRANCH_KEY); } catch (_) {}
  }

  function svgUse(symbolId, size) {
    size = size || 18;
    return '<svg width="' + size + '" height="' + size + '" aria-hidden="true"><use href="#' + symbolId + '"/></svg>';
  }

  function setChinIcon(tab, symbolId, extraClasses) {
    if (!tab) return;
    var icon = tab.querySelector('.bn-icon') || tab.querySelector('span:first-child');
    if (!icon) return;
    icon.innerHTML = svgUse(symbolId, 20);
    icon.className = 'bn-icon' + (extraClasses ? ' ' + extraClasses : '');
    icon.setAttribute('aria-hidden', 'true');
  }

  function syncChinIcons() {
    var nav = document.getElementById('bottom-nav');
    if (!nav) return;

    nav.querySelectorAll('[data-modal-trigger="call"]').forEach(function(tab) {
      setChinIcon(tab, 'ico-phone');
    });
    nav.querySelectorAll('[data-modal-trigger="menu"]').forEach(function(tab) {
      setChinIcon(tab, isMenuPage() ? 'ico-home' : 'ico-fork-knife');
    });
    nav.querySelectorAll('[data-modal-trigger="find"]').forEach(function(tab) {
      setChinIcon(tab, 'ico-compass');
    });
    nav.querySelectorAll('[data-modal-trigger="order"], #bn-order, .bn-cta').forEach(function(tab) {
      if (!tab.closest('#bottom-nav')) return;
      setChinIcon(tab, 'ico-flame', 'cta-flame mw-flame');
    });

    // Branch pages: direct links without data-modal-trigger
    nav.querySelectorAll('a[href^="tel:"]').forEach(function(tab) {
      setChinIcon(tab, 'ico-phone');
    });
    nav.querySelectorAll('a[href*="/menu.html"]').forEach(function(tab) {
      if (!tab.closest('#bottom-nav')) return;
      setChinIcon(tab, 'ico-bowl');
    });
    nav.querySelectorAll('a[href="/locations/"]').forEach(function(tab) {
      if (!tab.closest('#bottom-nav')) return;
      setChinIcon(tab, 'ico-compass');
    });
  }

  function syncHeroActionIcons() {
    var map = [
      ['hero-call-cta', 'ico-phone', ''],
      ['hero-order-cta', 'ico-flame', 'cta-flame mw-flame'],
      ['hero-menu-cta', 'ico-fork-knife', ''],
      ['hero-find-cta', 'ico-compass', '']
    ];
    map.forEach(function(entry) {
      var btn = document.getElementById(entry[0]);
      if (!btn) return;
      var icon = btn.querySelector('.hero-action-icon');
      if (!icon) return;
      var size = entry[0] === 'hero-order-cta' ? 26 : 22;
      icon.innerHTML = svgUse(entry[1], size);
      icon.className = 'hero-action-icon' + (entry[2] ? ' ' + entry[2] : '');
      icon.setAttribute('aria-hidden', 'true');
    });
  }

  function ensureFlame(btn) {
    if (!btn) return;
    var isHero = btn.classList.contains('hero-cta') || btn.classList.contains('hero-action-btn--cta');
    var size = isHero ? 26 : (btn.classList.contains('mob-order') || btn.classList.contains('nav-order') || btn.classList.contains('drawer-order-btn') ? 20 : 18);
    var flame = btn.querySelector('.cta-flame, .flame');
    if (!flame) {
      flame = document.createElement('span');
      flame.className = isHero ? 'flame' : 'cta-flame';
      flame.setAttribute('aria-hidden', 'true');
      btn.insertBefore(flame, btn.firstChild);
    }
    flame.innerHTML = svgUse('ico-flame', size);
    flame.classList.add('mw-flame');
  }

  function promoteFlameIcons() {
    document.querySelectorAll('.hero-cta, .hero-action-btn--cta, .nav-order, .mob-order, .drawer-order-btn, #ql-order-btn, .article-cta-primary').forEach(ensureFlame);
  }

  // Fix legacy 0x9D / replacement-char mojibake from cp1252-encoded HTML sources
  function sanitizePageText() {
    var bad = String.fromCharCode(0x9D);
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function(n) {
        var tag = n.parentElement && n.parentElement.tagName;
        if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var node;
    while (node = walker.nextNode()) {
      var t = node.textContent;
      if (t.indexOf(bad) === -1 && t.indexOf('\uFFFD') === -1) continue;
      var fixed = t
        .replace(/300[\u009D\uFFFD]C/g, '300\u00B0C')
        .replace(/[\u009D\uFFFD]/g, ' \u00B7 ')
        .replace(/\s+\u00B7\s+/g, ' \u00B7 ')
        .replace(/(\u00B7\s+){2,}/g, '\u00B7 ');
      if (fixed !== t) node.textContent = fixed;
    }
  }

  function syncHeroOrderCTA() {
    var heroBtn = document.getElementById('hero-order-cta');
    var heroText = heroBtn ? heroBtn.querySelector('.hero-action-label, .hero-cta-text') : null;
    var changeLink = document.getElementById('hero-change-branch');
    if (heroText) heroText.textContent = 'Order Now';
    if (changeLink) changeLink.style.display = 'none';
    if (heroBtn) ensureFlame(heroBtn);
  }

  function normalizeGlobalOrderButtons() {
    if (isBranchPage()) return;

    clearSavedBranchOnGlobalPage();
    syncHeroOrderCTA();

    var bnOrder = document.getElementById('bn-order');
    if (bnOrder && !bnOrder.hasAttribute('data-modal-trigger')) {
      bnOrder.setAttribute('data-modal-trigger', 'order');
      if (bnOrder.tagName === 'A') {
        bnOrder.removeAttribute('href');
        bnOrder.setAttribute('type', 'button');
      }
    }

    document.querySelectorAll(
      '.nav-order, .mob-order, .drawer-order-btn, .hero-cta, .article-cta-primary, #ql-order-btn'
    ).forEach(ensureFlame);

    document.querySelectorAll('#bottom-nav .bn-cta, #bottom-nav .bn-order, .bottom-nav .bn-order').forEach(function(btn) {
      setChinIcon(btn, 'ico-flame', 'cta-flame mw-flame');
      var label = btn.querySelector('.bn-label') || btn.querySelector('span:last-child');
      if (label) label.textContent = 'ORDER NOW';
      if (!btn.hasAttribute('data-modal-trigger')) btn.setAttribute('data-modal-trigger', 'order');
    });

    syncChinIcons();
  }

  function inferBranchFromText(text) {
    if (!text) return null;
    const lower = text.toLowerCase();
    if (lower.includes('parklands')) return BRANCHES['parklands'];
    if (lower.includes('capital')) return BRANCHES['capital-centre'];
    if (lower.includes('two rivers') || lower.includes('tworivers')) return BRANCHES['two-rivers'];
    return null;
  }

  function bindTrackingHandlers() {
    document.addEventListener('click', function(event) {
      const target = event.target.closest('a,button');
      if (!target) return;

      const branchLink = event.target.closest('[data-branch]');
      if (branchLink) {
        Tracking.trackBranchSelected(branchLink);
      }

      const href = (target.getAttribute('href') || '').trim();
      const text = (target.textContent || '').trim();
      const branchData = inferBranchFromText(text + ' ' + href);

      if (/wa\.me|whatsapp\.com|api\.whatsapp/i.test(href) || target.matches('[data-cta="whatsapp"]')) {
        const branchName = (branchData && branchData.name) || Tracking.getCurrentBranch();
        Tracking.trackWhatsAppOrder(branchName);
      }

      if (/foodbooking\.com|gloriafood/i.test(href) || target.matches('[data-cta="direct"]')) {
        Tracking.push({
          event: 'add_to_cart',
          dish_name: 'Unknown',
          dish_category: 'Unknown',
          dish_price: '0',
          currency: 'KES',
          branch: Tracking.getCurrentBranch(),
          quantity: 1,
          user_has_ordered_before: Memory.hasOrderedRecently(),
          timestamp: new Date().toISOString()
        });
      }

      if (href.startsWith('tel:')) {
        Tracking.trackContactBranch('phone_click', href.replace('tel:', ''), (branchData && branchData.name) || Tracking.getCurrentBranch());
      }
      if (/maps\.google|google\.com\/maps/i.test(href)) {
        Tracking.trackContactBranch('map', branchData ? branchData.phone : null, branchData ? branchData.name : Tracking.getCurrentBranch());
      }
    }, true);

    if (Tracking.getPageType() === 'menu') {
      Tracking.trackMenuView(Tracking.getCurrentBranch());
    }

    document.querySelectorAll('a.nav-order, a.mob-order, a[data-order-btn], button[data-order-btn]').forEach(function(el) {
      el.setAttribute('data-order-btn', 'true');
      if (!el.hasAttribute('data-cta')) {
        const href = el.getAttribute('href') || '';
        if (/wa\.me|whatsapp\.com/i.test(href)) el.setAttribute('data-cta', 'whatsapp');
        if (/foodbooking\.com|gloriafood/i.test(href)) el.setAttribute('data-cta', 'direct');
      }
    });
  }

  function initNavDropdownTriggers() {
    document.querySelectorAll('a.nav-dropdown-trigger').forEach(function(trigger) {
      trigger.addEventListener('click', function(e) {
        var href = trigger.getAttribute('href') || '';
        if (href === '#' || href === '') e.preventDefault();
      });
    });
  }

  function injectSVGSprites() {
    var sprite = document.getElementById('mw-svg-sprites');
    if (sprite) return;
    var div = document.createElement('div');
    div.id = 'mw-svg-sprites';
    div.style.cssText = 'position:absolute;width:0;height:0;overflow:hidden;';
    div.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg"><defs>' +
      '<symbol id="ico-flame" viewBox="0 0 24 24">' +
      '<path d="M12 2C12 2 8.5 7.5 8.5 11a3.5 3.5 0 0 0 7 0C15.5 7.5 12 2 12 2z" fill="#ff8c00"/>' +
      '<path d="M12 7C12 7 9.5 10.5 9.5 13a2.5 2.5 0 0 0 5 0C14.5 10.5 12 7 12 7z" fill="#ffd54f"/>' +
      '<path d="M12 10.5c0 0-1 1.5-1 2.8a1.2 1.2 0 0 0 2.4 0c0-1.3-1.4-2.8-1.4-2.8z" fill="#fff3e0"/>' +
      '</symbol>' +
      '<symbol id="ico-cart" viewBox="0 0 24 24">' +
      '<path d="M6 6h15l-1.5 9H7.5L6 6z" fill="none" stroke="rgba(255,255,255,0.75)" stroke-width="1.5" stroke-linejoin="round"/>' +
      '<circle cx="9" cy="20" r="1.5" fill="#d4af37"/>' +
      '<circle cx="18" cy="20" r="1.5" fill="#d4af37"/>' +
      '<path d="M6 6L5 3H2" fill="none" stroke="rgba(255,255,255,0.75)" stroke-width="1.5" stroke-linecap="round"/>' +
      '</symbol>' +
      '<symbol id="ico-phone" viewBox="0 0 24 24">' +
      '<path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z" fill="rgba(180,210,255,0.9)"/>' +
      '</symbol>' +
      '<symbol id="ico-bowl" viewBox="0 0 24 24">' +
      '<ellipse cx="12" cy="13" rx="9" ry="5" fill="none" stroke="rgba(255,255,255,0.75)" stroke-width="1.5"/>' +
      '<path d="M3 13c0 4 4 7 9 7s9-3 9-7" fill="rgba(255,255,255,0.12)" stroke="none"/>' +
      '<path d="M8 10 Q10 6 12 10" fill="none" stroke="#d4af37" stroke-width="1.5" stroke-linecap="round"/>' +
      '<path d="M11 9 Q13 5 15 9" fill="none" stroke="#d4af37" stroke-width="1.5" stroke-linecap="round"/>' +
      '</symbol>' +
      '<symbol id="ico-fork-knife" viewBox="0 0 24 24">' +
      '<path d="M5 3v7c0 1.4 1 2.4 2 2.4V21" fill="none" stroke="#d4af37" stroke-width="1.5" stroke-linecap="round"/>' +
      '<path d="M5 3v4M7 3v4" stroke="#d4af37" stroke-width="1.2" stroke-linecap="round"/>' +
      '<path d="M17 3v18" stroke="rgba(255,255,255,0.85)" stroke-width="1.5" stroke-linecap="round"/>' +
      '<path d="M17 3c2.2 2 2.2 4.8 0 6.8" fill="none" stroke="rgba(255,255,255,0.85)" stroke-width="1.5" stroke-linecap="round"/>' +
      '</symbol>' +
      '<symbol id="ico-car" viewBox="0 0 24 24">' +
      '<path d="M5 11l1.5-4.5h11L19 11" stroke="currentColor" stroke-width="1.5" fill="none"/>' +
      '<rect x="2" y="11" width="20" height="6" rx="2" fill="currentColor"/>' +
      '<circle cx="6.5" cy="17.5" r="1.5" fill="#8b1a1a"/>' +
      '<circle cx="17.5" cy="17.5" r="1.5" fill="#8b1a1a"/>' +
      '<rect x="4" y="12.5" width="4" height="2.5" rx="0.5" fill="rgba(255,255,255,0.3)"/>' +
      '<rect x="10" y="12.5" width="4" height="2.5" rx="0.5" fill="rgba(255,255,255,0.3)"/>' +
      '</symbol>' +
      '<symbol id="ico-home" viewBox="0 0 24 24">' +
      '<path d="M3 12L12 3l9 9" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>' +
      '<path d="M5 10v9a1 1 0 001 1h4v-4h4v4h4a1 1 0 001-1v-9" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>' +
      '</symbol>' +
      '<symbol id="ico-compass" viewBox="0 0 24 24">' +
      '<circle cx="12" cy="12" r="9" fill="none" stroke="rgba(80,210,180,0.8)" stroke-width="1.8"/>' +
      '<circle cx="12" cy="12" r="1.5" fill="rgba(80,210,180,0.9)"/>' +
      '<polygon points="12,4 14.5,12 12,20 9.5,12" fill="#d4af37"/>' +
      '<polygon points="4,12 12,9.5 20,12 12,14.5" fill="rgba(255,255,255,0.4)"/>' +
      '</symbol>' +
      '<symbol id="ico-arrow-right" viewBox="0 0 24 24">' +
      '<path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>' +
      '</symbol>' +
      '<symbol id="ico-check" viewBox="0 0 24 24">' +
      '<path d="M4 12l5 5L20 7" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>' +
      '</symbol>' +
      '<symbol id="ico-close" viewBox="0 0 24 24">' +
      '<path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>' +
      '</symbol>' +
      '</defs></svg>';
    document.body.insertBefore(div, document.body.firstChild);
  }

  function initFlames() {
    document.querySelectorAll('.cta-flame, [data-flame]').forEach(function(el) {
      el.classList.add('mw-flame');
    });
  }

  function init() {
    window.pageLoadTime = Date.now();

    injectAuditStyles();
    injectSVGSprites();
    sanitizePageText();
    initNavDropdownTriggers();
    NavDrawer.init();
    OrderCTA.updateCTAText();
    AbandonCart.init();
    Modal.init();
    QuickLook.init();
    bindTrackingHandlers();
    normalizeGlobalOrderButtons();
    syncChinIcons();
    syncHeroActionIcons();
    promoteFlameIcons();
    initFlames();

    Tracking.push({
      event: 'page_view',
      page_title: document.title,
      page_url: window.location.href,
      page_type: Tracking.getPageType(),
      branch: Tracking.getCurrentBranch(),
      timestamp: new Date().toISOString()
    });

    console.log('[Mister Wok Engine] Initialized');
    console.log('[User Data]', Memory.getAll());
  }

  window.MisterWokEngine = {
    Memory: Memory,
    Platform: Platform,
    Tracking: Tracking,
    OrderCTA: OrderCTA,
    Modal: Modal,
    QuickLook: QuickLook,
    NavDrawer: NavDrawer,
    isBranchPage: isBranchPage,
    openBranchSelector: openBranchSelector,
    init: init
  };

  window.openBranchSelector = openBranchSelector;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
