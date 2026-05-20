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
    },
    initCTAVisibility: function() {
      const whatsappCTAs = document.querySelectorAll('[data-cta="whatsapp"]');
      const directOrderCTAs = document.querySelectorAll('[data-cta="direct"]');

      if (this.isMobile()) {
        whatsappCTAs.forEach(function(el) { el.style.display = ''; });
        directOrderCTAs.forEach(function(el) { el.style.display = 'none'; });
      } else {
        whatsappCTAs.forEach(function(el) { el.style.display = 'none'; });
        directOrderCTAs.forEach(function(el) { el.style.display = ''; });
      }
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
      Memory.set('last_branch_selected', branchData.name);
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
      call:    { title: 'Call Your Branch',             sub: 'Tap a branch to call directly. Each branch has its own line.' }
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
          e.preventDefault();
          self.open(btn.getAttribute('data-modal-trigger') || 'order');
        });
      });

      // Legacy class hooks from Phase 1A (preserve behaviour)
      document.querySelectorAll('.order-trigger').forEach(function(btn) {
        if (btn.hasAttribute('data-modal-trigger')) return;
        btn.addEventListener('click', function(e) { e.preventDefault(); self.open('order'); });
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

      // Track branch selection clicks (lets Tracking module log + remember)
      options.forEach(function(opt) {
        opt.addEventListener('click', function() {
          const slug = opt.getAttribute('data-branch-slug') || opt.getAttribute('data-branch');
          if (slug) Memory.set('last_order_branch', slug);
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
      if (this.titleEl) this.titleEl.textContent = text.title;
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
        opt.setAttribute('href', target);
        // Open external links in a new tab (tel: links stay same-window)
        if (m === 'call') {
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

      // Pre-fill the edit-details form (if present) every time we open
      EditDetails.populate();

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

  // ──────────────────────────────────────────────────────────
  // EditDetails: in-modal name/phone/address override.
  // Surfaces a hidden form that pre-fills with localStorage values
  // and saves overrides back to Memory. GTM event on save.
  // ──────────────────────────────────────────────────────────
  const EditDetails = {
    init: function() {
      const trigger = document.getElementById('edit-details-trigger');
      const form = document.getElementById('edit-details-form');
      if (!trigger || !form) return;

      const saveBtn = document.getElementById('save-details-btn');
      const cancelBtn = document.getElementById('cancel-details-btn');
      const self = this;

      trigger.addEventListener('click', function(e) {
        e.preventDefault();
        const showing = form.style.display && form.style.display !== 'none';
        form.style.display = showing ? 'none' : 'flex';
        if (!showing) self.populate();
      });

      if (saveBtn) {
        saveBtn.addEventListener('click', function(e) {
          e.preventDefault();
          self.save();
          form.style.display = 'none';
        });
      }
      if (cancelBtn) {
        cancelBtn.addEventListener('click', function(e) {
          e.preventDefault();
          form.style.display = 'none';
        });
      }
    },

    populate: function() {
      const nameEl = document.getElementById('user-name-input');
      const phoneEl = document.getElementById('user-phone-input');
      const addressEl = document.getElementById('user-address-input');
      if (nameEl) nameEl.value = Memory.get('user_name') || '';
      if (phoneEl) phoneEl.value = Memory.get('user_phone') || '';
      if (addressEl) addressEl.value = Memory.get('user_address') || '';
    },

    save: function() {
      const nameEl = document.getElementById('user-name-input');
      const phoneEl = document.getElementById('user-phone-input');
      const addressEl = document.getElementById('user-address-input');
      const name = nameEl ? nameEl.value.trim() : '';
      const phone = phoneEl ? phoneEl.value.trim() : '';
      const address = addressEl ? addressEl.value.trim() : '';

      if (name) Memory.set('user_name', name);
      if (phone) Memory.set('user_phone', phone);
      if (address) Memory.set('user_address', address);

      Tracking.push({
        event: 'user_details_updated',
        has_name: !!name,
        has_phone: !!phone,
        has_address: !!address,
        page_type: Tracking.getPageType(),
        branch: Tracking.getCurrentBranch(),
        timestamp: new Date().toISOString()
      });
    }
  };

  const OrderCTA = {
    updateCTAText: function() {
      const orderButtons = document.querySelectorAll('[data-order-btn]:not(.modal-opt)');

      if (Memory.hasOrderedRecently()) {
        orderButtons.forEach(function(btn) {
          if (btn.closest('[data-hero-cta]') || btn.closest('.dish-card') || btn.closest('.takeaway-banner')) return;
          btn.textContent = 'Re-order Your Favorites?';
          btn.setAttribute('data-repeat', 'true');
        });
      } else {
        orderButtons.forEach(function(btn) {
          if (btn.closest('[data-hero-cta]') || btn.closest('.dish-card') || btn.closest('.takeaway-banner')) return;
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
        if (Tracking.getPageType() === 'homepage') {
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

      if (Tracking.getPageType() === 'homepage') {
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

  function personalizeHeroCTA() {
    var btn = document.querySelector('[data-hero-cta]');
    var span = btn && btn.querySelector('.hero-cta-text');
    if (!btn || !span) return;
    if (Tracking.getPageType() !== 'homepage') return;

    var branchKey = Memory.get('last_order_branch');
    if (!branchKey || !BRANCHES[branchKey]) return;

    var branchName = BRANCHES[branchKey].name;
    var lastOrderTime = Memory.get('last_order_time');
    var within24 = lastOrderTime && (Date.now() - parseInt(lastOrderTime, 10)) < CONFIG.orderRecentThreshold;
    span.textContent = within24
      ? ('Order from ' + branchName + ' Again →')
      : ('Order from ' + branchName + ' →');
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

  function init() {
    window.pageLoadTime = Date.now();

    Platform.initCTAVisibility();
    OrderCTA.updateCTAText();
    AbandonCart.init();
    Modal.init();
    EditDetails.init();
    QuickLook.init();
    bindTrackingHandlers();
    personalizeHeroCTA();

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
    EditDetails: EditDetails,
    QuickLook: QuickLook,
    init: init
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
