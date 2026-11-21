<?php
/** Built-in palette for the RA Dark Theme Gantry template. GPL-2.0-or-later. */
defined('_JEXEC') or die;

use Joomla\CMS\Factory;
use Joomla\CMS\Uri\Uri;

$app = Factory::getApplication();
$document = $app->getDocument();
$params = $app->getTemplate(true)->params;
$default = (string) $params->get('ra_default_theme', 'system');
$default = in_array($default, ['system', 'light', 'dark'], true) ? $default : 'system';
$base = rtrim(Uri::root(true), '/') . '/templates/ra_darktheme/ra-assets/';
$document->addScriptOptions('plg_system_ra_darktheme', [
    'enabled' => true,
    'defaultTheme' => $default,
    'showToggle' => (bool) $params->get('ra_show_toggle', 1),
    'position' => 'header',
    'weather' => (bool) $params->get('ra_weather', 1),
    'labels' => ['light' => 'Switch to light mode', 'dark' => 'Switch to dark mode'],
]);
$assets = $document->getWebAssetManager();
$assets->registerAndUseStyle('tpl_ra_darktheme.theme', $base . 'css/theme.css',
    ['version' => 'auto', 'weight' => 1000], ['media' => 'screen']);
$assets->registerAndUseStyle('tpl_ra_darktheme.toggle', $base . 'css/toggle.css',
    ['version' => 'auto', 'weight' => 1001]);
$assets->registerAndUseScript('tpl_ra_darktheme.bootstrap', $base . 'js/bootstrap.js',
    ['version' => 'auto', 'weight' => -1000], ['data-ra-default' => $default]);
$assets->registerAndUseScript('tpl_ra_darktheme.theme', $base . 'js/theme.js',
    ['version' => 'auto'], ['defer' => true], ['core', 'tpl_ra_darktheme.bootstrap']);
