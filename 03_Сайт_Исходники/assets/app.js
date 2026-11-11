/* ============================================================
   Эстетический Справочник — общий скрипт
   - мобильное меню (дровер)
   - прогресс чтения
   - поиск на главной
   - движок схем: анимация по одному параметру p (0..1),
     поэтому работает и автоплей, и ручная прокрутка ползунком
   ============================================================ */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------
     1. Мобильное меню
     --------------------------------------------------------- */
  function initNav() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.getElementById('site-nav');
    if (!toggle || !nav) return;

    function setOpen(open) {
      toggle.setAttribute('aria-expanded', String(open));
      nav.setAttribute('data-open', String(open));
      document.body.classList.toggle('is-locked', open);
    }

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 1040) setOpen(false);
    });
  }

  /* ---------------------------------------------------------
     2. Прогресс чтения
     --------------------------------------------------------- */
  function initProgress() {
    var bar = document.getElementById('progress');
    if (!bar) return;

    var ticking = false;
    function update() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      var p = max > 0 ? (h.scrollTop / max) * 100 : 0;
      bar.style.width = p.toFixed(2) + '%';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* ---------------------------------------------------------
     3. Поиск
     --------------------------------------------------------- */
  function initSearch() {
    var root = document.querySelector('[data-search]');
    if (!root) return;

    var input = root.querySelector('.search__input');
    var results = root.querySelector('.search__results');
    var hints = root.querySelectorAll('.search-hint');
    var data = window.SITE_SEARCH || [];

    function norm(s) { return (s || '').toLowerCase().replace(/ё/g, 'е').trim(); }

    // keywords допускаются и строкой, и массивом: так индекс проще
    // пополнять вручную, не вспоминая про форму записи
    function keyString(k) {
      if (!k) return '';
      return Array.isArray(k) ? k.join(' ') : String(k);
    }

    function score(item, q) {
      var title = norm(item.title);
      var desc = norm(item.desc);
      var keys = norm(keyString(item.keywords));
      var s = 0;
      if (title.indexOf(q) === 0) s += 100;
      if (title.indexOf(q) > -1) s += 50;
      if (keys.indexOf(q) > -1) s += 30;
      if (desc.indexOf(q) > -1) s += 15;
      return s;
    }

    function runs() {
      var q = norm(input.value);
      if (q.length < 2) { results.hidden = true; results.innerHTML = ''; return; }

      var found = data
        .map(function (it) { return { it: it, s: score(it, q) }; })
        .filter(function (x) { return x.s > 0; })
        .sort(function (a, b) { return b.s - a.s; })
        .slice(0, 6);

      if (!found.length) {
        results.innerHTML = '<p class="search__empty">По запросу «' + escapeHtml(input.value) +
          '» пока ничего нет. База пополняется: напишите в Telegram, и я подготовлю разбор.</p>';
        results.hidden = false;
        return;
      }

      results.innerHTML = found.map(function (x) {
        return '<a class="search-result" href="' + x.it.href + '">' +
          '<span class="search-result__type">' + escapeHtml(x.it.type) + '</span>' +
          '<span class="search-result__title">' + escapeHtml(x.it.title) + '</span>' +
          '<span class="search-result__desc">' + escapeHtml(x.it.desc) + '</span>' +
          '</a>';
      }).join('');
      results.hidden = false;
    }

    function escapeHtml(s) {
      return String(s).replace(/[&<>"']/g, function (c) {
        return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
      });
    }

    input.addEventListener('input', runs);
    input.addEventListener('focus', runs);

    root.addEventListener('submit', function (e) {
      e.preventDefault();
      var first = results.querySelector('.search-result');
      if (first) window.location.href = first.getAttribute('href');
    });

    hints.forEach(function (h) {
      h.addEventListener('click', function () {
        input.value = h.getAttribute('data-q') || h.textContent.trim();
        runs();
        input.focus();
      });
    });

    document.addEventListener('click', function (e) {
      if (!root.contains(e.target)) { results.hidden = true; }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') results.hidden = true;
    });
  }

  /* ---------------------------------------------------------
     4. Движок схем
     ---------------------------------------------------------
     Каждый рисунок — функция от одного числа p (0..1).
     Ни CSS-анимаций, ни таймеров внутри SVG: поэтому состояние
     можно выставить в любой момент, а значит ползунок работает
     честно и рисунок можно рассмотреть по кадрам.

     Атрибуты на элементах SVG:
       data-at="0.2"              появление (fade in) с 0.2
       data-out="0.6,0.85"        исчезновение между 0.6 и 0.85
       data-tx="0,120"            перенос по x от 0 до 120
       data-ty="450,200"          перенос по y
       data-scale="1,1,1.4,.4"    sx0,sy0,sx1,sy1 (вокруг локального 0,0)
       data-draw                   прорисовка обводки (штрих «рисуется»)
       data-flow="3"              бегущий пунктир, 3 цикла за проход
     --------------------------------------------------------- */
  function smoothstep(a, b, x) {
    var t = (x - a) / (b - a || 1);
    t = Math.max(0, Math.min(1, t));
    return t * t * (3 - 2 * t);
  }

  function FigureRoot(root) {
    var self = this;
    this.root = root;
    this.dur = (parseFloat(root.getAttribute('data-dur')) || 6) * 1000;
    this.p = 0;
    this.playing = false;
    this.raf = null;
    this.lastTime = 0;
    this.touched = false;

    this.playBtn = root.querySelector('.fig__play');
    this.range = root.querySelector('.fig__range');
    this.phaseEl = root.querySelector('.fig__phase');

    this.phases = [];
    try { this.phases = JSON.parse(root.getAttribute('data-phases') || '[]'); } catch (e) { }

    this.els = Array.prototype.slice.call(
      root.querySelectorAll('[data-at],[data-out],[data-tx],[data-ty],[data-scale],[data-draw],[data-flow]')
    );

    this.els.forEach(function (el) {
      el._baseOpacity = el.getAttribute('opacity') !== null
        ? parseFloat(el.getAttribute('opacity')) : 1;
      // Прорисовка штриха. Приоритет — атрибуту pathLength: он нормализует
      // длину в самом SVG, поэтому анимация работает одинаково везде и не
      // зависит от того, успел ли браузер измерить геометрию.
      if (el.hasAttribute('data-draw')) {
        var declared = parseFloat(el.getAttribute('pathLength'));
        var len = declared > 0 ? declared : 0;
        if (!len && el.getTotalLength) {
          try { len = el.getTotalLength() || 0; } catch (e) { len = 0; }
        }
        if (!len) len = 100;
        el._len = len;
        el.style.strokeDasharray = len + ' ' + len;
        el.style.strokeDashoffset = len;
      }
      if (el.hasAttribute('data-flow')) {
        el._flowLen = 0;
        try { el._flowLen = el.getTotalLength(); } catch (e) { }
      }
    });

    this.render(0);

    if (this.playBtn) {
      this.playBtn.addEventListener('click', function () { self.toggle(); });
    }
    if (this.range) {
      this.range.addEventListener('input', function () {
        self.pause();
        self.touched = true;
        self.setProgress(parseInt(self.range.value, 10) / 1000);
      });
    }

    if (reduceMotion) {
      root.classList.add('no-anim');
      this.setProgress(1);
      return;
    }

    this.observe();
  }

  FigureRoot.prototype.observe = function () {
    var self = this;
    if (!('IntersectionObserver' in window)) { this.play(); return; }

    this.io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && en.intersectionRatio > 0.35) {
          if (!self.touched && self.p < 1) self.play();
        } else if (!en.isIntersecting) {
          self.pause();
        }
      });
    }, { threshold: [0, 0.35, 0.75] });

    this.io.observe(this.root);
  };

  FigureRoot.prototype.play = function () {
    if (this.playing) return;
    if (this.p >= 1) this.setProgress(0);
    this.playing = true;
    this.lastTime = performance.now();
    this.updateButton();
    var self = this;
    var step = function (now) {
      if (!self.playing) return;
      var dt = now - self.lastTime;
      self.lastTime = now;
      self.setProgress(self.p + dt / self.dur);
      if (self.p >= 1) { self.pause(); return; }
      self.raf = requestAnimationFrame(step);
    };
    this.raf = requestAnimationFrame(step);
  };

  FigureRoot.prototype.pause = function () {
    this.playing = false;
    if (this.raf) { cancelAnimationFrame(this.raf); this.raf = null; }
    this.updateButton();
  };

  FigureRoot.prototype.toggle = function () {
    this.touched = true;
    if (this.playing) this.pause(); else this.play();
  };

  FigureRoot.prototype.updateButton = function () {
    if (!this.playBtn) return;
    this.playBtn.setAttribute('aria-label', this.playing ? 'Пауза' : 'Проиграть анимацию');
    this.playBtn.innerHTML = this.playing
      ? '<svg viewBox="0 0 12 12" aria-hidden="true"><rect x="1" y="1" width="3.5" height="10" rx="1" fill="currentColor"/><rect x="7.5" y="1" width="3.5" height="10" rx="1" fill="currentColor"/></svg>'
      : '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 1.4v9.2a.6.6 0 0 0 .92.5l7.2-4.6a.6.6 0 0 0 0-1L3.42.9a.6.6 0 0 0-.92.5Z" fill="currentColor"/></svg>';
  };

  FigureRoot.prototype.setProgress = function (p) {
    this.p = Math.max(0, Math.min(1, p));
    this.render(this.p);
    if (this.range) {
      this.range.value = Math.round(this.p * 1000);
      this.range.style.setProperty('--fill', (this.p * 100) + '%');
    }
    if (this.phaseEl && this.phases.length) {
      var idx = Math.min(this.phases.length - 1, Math.floor(this.p * this.phases.length));
      if (this.phaseEl.textContent !== this.phases[idx]) {
        this.phaseEl.textContent = this.phases[idx];
      }
    }
  };

  FigureRoot.prototype.render = function (p) {
    this.els.forEach(function (el) {
      var op = el._baseOpacity;
      var hasOpacityRule = false;

      if (el.hasAttribute('data-at')) {
        op *= smoothstep(parseFloat(el.dataset.at), parseFloat(el.dataset.at) + 0.12, p);
        hasOpacityRule = true;
      }
      if (el.hasAttribute('data-out')) {
        var parts = el.dataset.out.split(',');
        var a = parseFloat(parts[0]);
        var b = parseFloat(parts[1]);
        op *= 1 - smoothstep(a, b, p);
        hasOpacityRule = true;
      }
      if (hasOpacityRule) {
        el.style.opacity = Math.max(0, Math.min(1, op));
      }

      var tx = 0, ty = 0, sx = 1, sy = 1, hasTransform = false;

      if (el.hasAttribute('data-tx')) {
        var v = el.dataset.tx.split(',');
        tx = parseFloat(v[0]) + (parseFloat(v[1]) - parseFloat(v[0])) * p;
        hasTransform = true;
      }
      if (el.hasAttribute('data-ty')) {
        var vy = el.dataset.ty.split(',');
        ty = parseFloat(vy[0]) + (parseFloat(vy[1]) - parseFloat(vy[0])) * p;
        hasTransform = true;
      }
      if (el.hasAttribute('data-scale')) {
        var s = el.dataset.scale.split(',');
        sx = parseFloat(s[0]) + (parseFloat(s[2]) - parseFloat(s[0])) * p;
        sy = parseFloat(s[1]) + (parseFloat(s[3]) - parseFloat(s[1])) * p;
        hasTransform = true;
      }
      if (hasTransform) {
        el.setAttribute('transform',
          'translate(' + tx.toFixed(2) + ' ' + ty.toFixed(2) + ') scale(' +
          sx.toFixed(3) + ' ' + sy.toFixed(3) + ')');
      }

      if (el._len) {
        el.style.strokeDashoffset = (el._len * (1 - p)).toFixed(2);
      }

      if (el.hasAttribute('data-flow') && el._flowLen) {
        var cycles = parseFloat(el.dataset.flow) || 2;
        el.style.strokeDashoffset = (-el._flowLen * cycles * p).toFixed(2);
      }
    });
  };

  function initFigures() {
    var roots = document.querySelectorAll('[data-fig]');
    Array.prototype.forEach.call(roots, function (r) {
      try {
        new FigureRoot(r);
        r.classList.add('is-ready');
      } catch (e) {
        // схема осталась статичной — не оставляем читателя с пустой областью
        r.classList.add('no-anim');
        console.warn('figure init failed', r, e);
      }
    });
  }

  /* ---------------------------------------------------------
     5. Ленивая подгрузка видео (без cookie до клика)
     --------------------------------------------------------- */
  function initVideo() {
    var slots = document.querySelectorAll('[data-video]');
    Array.prototype.forEach.call(slots, function (slot) {
      slot.addEventListener('click', function () {
        var id = slot.getAttribute('data-video');
        var src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
        var ifr = document.createElement('iframe');
        ifr.src = src;
        ifr.title = slot.getAttribute('data-title') || 'Видео';
        ifr.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture';
        ifr.allowFullscreen = true;
        slot.innerHTML = '';
        slot.appendChild(ifr);
        slot.style.cursor = 'default';
      }, { once: true });
    });
  }

  /* --------------------------------------------------------- */
  function boot() {
    initNav();
    initProgress();
    initSearch();
    initFigures();
    initVideo();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
