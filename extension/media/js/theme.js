/* Copyright (C) 2026 Mark Buckwell. SPDX-License-Identifier: GPL-2.0-or-later */
(() => {
  'use strict';
  if (window.RADarkTheme) return;
  const config = window.Joomla?.getOptions('plg_system_ra_darktheme', null);
  if (!config?.enabled) return;
  const root = document.documentElement;
  const key = 'ra-dark-theme:preference';
  const device = window.matchMedia('(prefers-color-scheme: dark)');
  const valid = value => ['system', 'light', 'dark'].includes(value);
  const fallback = valid(config.defaultTheme) ? config.defaultTheme : 'system';
  let preference = fallback;
  try { const saved = localStorage.getItem(key); if (valid(saved)) preference = saved; } catch (_) {}
  let button;
  const weather = new Map();
  const darkColours = {basecolor:'#161d1a', textcolor:'#e7ede8', highcolor:'#f6b09d',
    lowcolor:'#9bc8ab', suncolor:'#f9b104', cloudcolor:'#bdc9c0'};
  const lightColours = {basecolor:'#ffffff', textcolor:'#222222', highcolor:'#222222',
    lowcolor:'#777777', suncolor:'#222222', cloudcolor:'#222222'};

  function refreshWeather(link, state) {
    const dark = root.dataset.raTheme === 'dark';
    const colours = dark ? darkColours : state.colours;
    for (const name of Object.keys(darkColours)) {
      if (!dark && state.original[name] === null) link.removeAttribute('data-' + name);
      else link.setAttribute('data-' + name, colours[name]);
    }
    const frame = link.querySelector('iframe.weatherwidget-io-frame');
    if (frame) {
      if (state.frame !== frame) {
        state.frame = frame;
        frame.addEventListener('load', () => refreshWeather(link, state));
      }
      frame.contentWindow?.postMessage({id:frame.id, href:link.href,
        label_1:link.getAttribute('data-label_1'), label_2:link.getAttribute('data-label_2'),
        theme:link.getAttribute('data-theme') || 'pure', ...colours}, 'https://weatherwidget.io');
    }
  }

  function apply() {
    const dark = preference === 'dark' || (preference === 'system' && device.matches);
    root.dataset.raTheme = dark ? 'dark' : 'light';
    if (button) {
      const label = dark ? (config.labels?.light || 'Switch to light mode') : (config.labels?.dark || 'Switch to dark mode');
      button.title = label;
      button.setAttribute('aria-label', label);
      // Lucide sun and moon paths used on prodockit.org. See THIRD_PARTY_NOTICES.txt.
      button.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        (dark ? '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>' : '<path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"/>') + '</svg>';
    }
    weather.forEach((state, link) => refreshWeather(link, state));
  }

  function choose(value) {
    if (!valid(value)) return;
    preference = value;
    try { localStorage.setItem(key, value); } catch (_) {}
    apply();
  }

  function mount() {
    if (config.showToggle !== false) {
      button = document.createElement('button');
      button.id = 'ra-theme-toggle';
      button.type = 'button';
      button.addEventListener('click', () => choose(root.dataset.raTheme === 'dark' ? 'light' : 'dark'));
      const heading = document.getElementById('ramblerstitle');
      if ((!config.position || config.position === 'header') && heading) {
        const tools = document.createElement('div');
        tools.className = 'ra-title-tools';
        heading.before(tools);
        tools.append(heading, button);
      } else {
        button.dataset.position = config.position === 'bottom-left' ? 'bottom-left' : 'bottom-right';
        document.body.append(button);
      }
    }
    if (config.weather !== false) {
      for (const link of document.querySelectorAll('.weatherwidget-io')) {
        const original = {}, colours = {};
        for (const name of Object.keys(darkColours)) {
          original[name] = link.getAttribute('data-' + name);
          colours[name] = original[name] ?? lightColours[name];
        }
        const state = {original, colours};
        weather.set(link, state);
        // The existing weather script may insert its iframe after this plugin loads.
        const observer = new MutationObserver(() => refreshWeather(link, state));
        observer.observe(link, {childList:true, subtree:true});
        state.observer = observer;
      }
    }
    apply();
  }

  device.addEventListener('change', () => { if (preference === 'system') apply(); });
  window.addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    preference = valid(event.newValue) ? event.newValue : fallback;
    apply();
  });
  window.RADarkTheme = Object.freeze({
    setPreference: choose,
    resetPreference() {
      try { localStorage.removeItem(key); } catch (_) {}
      preference = fallback;
      apply();
    }
  });
  apply();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, {once:true});
  else mount();
})();
