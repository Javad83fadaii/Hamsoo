/* ==========================================================================
   اسکریپت اصلی سایت رسانه همسو
   - ناوبری بین بخش‌ها (بدون بارگذاری مجدد صفحه)
   - فیلتر آثار تولیدی (پادکست / ویدئو / نشریه)
   - پخش‌کننده صوتی پادکست‌ها
   ========================================================================== */

(function () {
  'use strict';

  var PERSIAN_DIGITS = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

  /* ------------------------------------------------------------------
     ابزارهای کمکی
     ------------------------------------------------------------------ */
  function toPersianDigits(value) {
    return String(value).replace(/\d/g, function (digit) {
      return PERSIAN_DIGITS[Number(digit)];
    });
  }

  function formatTime(seconds) {
    if (!isFinite(seconds) || seconds < 0) {
      return '۰۰:۰۰';
    }
    var total = Math.floor(seconds);
    var minutes = String(Math.floor(total / 60)).padStart(2, '0');
    var rest = String(total % 60).padStart(2, '0');
    return toPersianDigits(minutes + ':' + rest);
  }

  /* ------------------------------------------------------------------
     ناوبری بین بخش‌های سایت
     ------------------------------------------------------------------ */
  function navigateTo(pageId, options) {
    var target = document.getElementById(pageId);
    if (!target) {
      return;
    }

    document.querySelectorAll('.page-section').forEach(function (section) {
      section.classList.remove('active');
    });
    target.classList.add('active');

    document.querySelectorAll('.nav-link').forEach(function (link) {
      link.classList.toggle('nav-active', link.dataset.nav === pageId);
    });

    if (!options || options.scroll !== false) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, '', '#' + pageId);
    }
  }

  /* ------------------------------------------------------------------
     فیلتر آثار تولیدی
     ------------------------------------------------------------------ */
  function filterWorks(type, activeTab) {
    document.querySelectorAll('.work-tab').forEach(function (tab) {
      tab.classList.toggle('active', tab === activeTab);
    });

    document.querySelectorAll('.work-item').forEach(function (item) {
      var shouldShow = type === 'all' || item.classList.contains(type);
      item.style.display = shouldShow ? '' : 'none';
    });
  }

  /* ------------------------------------------------------------------
     پخش‌کننده صوتی پادکست‌ها
     ------------------------------------------------------------------ */
  var audio = new Audio();
  var activeButton = null;
  var activeCard = null;

  function setPlayingIcon(button, isPlaying) {
    var icon = button.querySelector('i');
    if (!icon) {
      return;
    }
    icon.classList.toggle('fa-play', !isPlaying);
    icon.classList.toggle('fa-pause', isPlaying);
  }

  function resetPlayer() {
    if (activeButton) {
      setPlayingIcon(activeButton, false);
    }
    if (activeCard) {
      var bar = activeCard.querySelector('.js-audio-progress');
      if (bar) {
        bar.style.width = '0%';
      }
      var current = activeCard.querySelector('.js-audio-current');
      if (current) {
        current.textContent = '۰۰:۰۰';
      }
    }
    activeButton = null;
    activeCard = null;
  }

  function toggleAudio(button) {
    var source = button.dataset.audioSrc;
    if (!source) {
      return;
    }

    if (activeButton === button) {
      if (audio.paused) {
        audio.play().then(function () {
          setPlayingIcon(button, true);
        }).catch(function () {
          setPlayingIcon(button, false);
        });
      } else {
        audio.pause();
        setPlayingIcon(button, false);
      }
      return;
    }

    resetPlayer();
    activeButton = button;
    activeCard = button.closest('[data-audio-card]');
    audio.src = source;
    audio.play().then(function () {
      setPlayingIcon(button, true);
    }).catch(function () {
      setPlayingIcon(button, false);
    });
  }

  audio.addEventListener('timeupdate', function () {
    if (!activeCard || !isFinite(audio.duration) || audio.duration === 0) {
      return;
    }
    var percent = (audio.currentTime / audio.duration) * 100;
    var bar = activeCard.querySelector('.js-audio-progress');
    if (bar) {
      bar.style.width = percent + '%';
    }
    var current = activeCard.querySelector('.js-audio-current');
    if (current) {
      current.textContent = formatTime(audio.currentTime);
    }
  });

  audio.addEventListener('ended', resetPlayer);
  audio.addEventListener('error', resetPlayer);

  /* ------------------------------------------------------------------
     اتصال رویدادها
     ------------------------------------------------------------------ */
  document.addEventListener('click', function (event) {
    var navTrigger = event.target.closest('[data-nav]');
    if (navTrigger) {
      event.preventDefault();
      navigateTo(navTrigger.dataset.nav);
      return;
    }

    var filterTrigger = event.target.closest('[data-filter]');
    if (filterTrigger) {
      filterWorks(filterTrigger.dataset.filter, filterTrigger);
      return;
    }

    var audioTrigger = event.target.closest('[data-audio-src]');
    if (audioTrigger) {
      toggleAudio(audioTrigger);
    }
  });

  /* اگر آدرسی با # باز شد، همان بخش نمایش داده شود. */
  function showInitialSection() {
    var pageId = window.location.hash.replace('#', '');
    if (pageId && document.getElementById(pageId)) {
      navigateTo(pageId, { scroll: false });
    } else {
      navigateTo('home', { scroll: false });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', showInitialSection);
  } else {
    showInitialSection();
  }
})();
