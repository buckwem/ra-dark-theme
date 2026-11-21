/* Copyright (C) 2026 Mark Buckwell. SPDX-License-Identifier: GPL-2.0-or-later */
(() => {
  'use strict';
  const valid = value => ['system', 'light', 'dark'].includes(value);
  const configured = document.currentScript?.getAttribute('data-ra-default');
  let preference = valid(configured) ? configured : 'system';
  try { const saved = localStorage.getItem('ra-dark-theme:preference'); if (valid(saved)) preference = saved; } catch (_) {}
  const dark = preference === 'dark' || (preference === 'system'
    && window.matchMedia('(prefers-color-scheme: dark)').matches);
  document.documentElement.dataset.raTheme = dark ? 'dark' : 'light';
})();
