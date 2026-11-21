<?php

/**
 * @copyright Copyright (C) 2026 Mark Buckwell
 * @license GPL-2.0-or-later
 */

namespace RADarkTheme\Plugin\System\RaDarktheme\Extension;

use Joomla\CMS\Document\HtmlDocument;
use Joomla\CMS\Event\Application\BeforeCompileHeadEvent;
use Joomla\CMS\Language\Text;
use Joomla\CMS\Plugin\CMSPlugin;
use Joomla\CMS\Uri\Uri;
use Joomla\Event\SubscriberInterface;

defined('_JEXEC') or die;

final class DarkTheme extends CMSPlugin implements SubscriberInterface
{
    protected $autoloadLanguage = true;

    public static function getSubscribedEvents(): array
    {
        return ['onBeforeCompileHead' => 'onBeforeCompileHead'];
    }

    public function onBeforeCompileHead(BeforeCompileHeadEvent $event): void
    {
        $app = $event->getApplication();
        $document = $event->getDocument();
        if (!$app->isClient('site') || !$document instanceof HtmlDocument
            || $app->getInput()->getCmd('tmpl') === 'component') {
            return;
        }

        $template = trim((string) $this->params->get('template', 'g5_hydrogen'));
        if ($template !== '' && $app->getTemplate() !== $template) {
            return;
        }

        $default = (string) $this->params->get('default_theme', 'system');
        $default = in_array($default, ['system', 'light', 'dark'], true) ? $default : 'system';
        $position = (string) $this->params->get('position', 'header');
        $position = in_array($position, ['header', 'bottom-right', 'bottom-left'], true) ? $position : 'header';
        $document->addScriptOptions('plg_system_ra_darktheme', [
            'enabled' => true,
            'defaultTheme' => $default,
            'showToggle' => (bool) $this->params->get('show_toggle', 1),
            'position' => $position,
            'weather' => (bool) $this->params->get('weather', 1),
            'labels' => [
                'light' => Text::_('PLG_SYSTEM_RA_DARKTHEME_SWITCH_LIGHT'),
                'dark' => Text::_('PLG_SYSTEM_RA_DARKTHEME_SWITCH_DARK'),
            ],
        ]);

        $base = Uri::root(true) . '/media/plg_system_ra_darktheme/';
        $assets = $document->getWebAssetManager();
        // Register late and give colour overrides a higher weight than template CSS.
        $assets->registerAndUseStyle('plg_system_ra_darktheme.theme', $base . 'css/theme.css',
            ['version' => 'auto', 'weight' => 1000], ['media' => 'screen']);
        $assets->registerAndUseStyle('plg_system_ra_darktheme.toggle', $base . 'css/toggle.css',
            ['version' => 'auto', 'weight' => 1001]);
        // This small external script applies the saved palette before the body renders.
        $assets->registerAndUseScript('plg_system_ra_darktheme.bootstrap', $base . 'js/bootstrap.js',
            ['version' => 'auto', 'weight' => -1000], ['data-ra-default' => $default]);
        $assets->registerAndUseScript('plg_system_ra_darktheme.theme', $base . 'js/theme.js',
            ['version' => 'auto'], ['defer' => true], ['core', 'plg_system_ra_darktheme.bootstrap']);
    }
}
