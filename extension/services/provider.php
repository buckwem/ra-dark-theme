<?php

/**
 * @copyright Copyright (C) 2026 Mark Buckwell
 * @license GPL-2.0-or-later
 */

defined('_JEXEC') or die;

use RADarkTheme\Plugin\System\RaDarktheme\Extension\DarkTheme;
use Joomla\CMS\Extension\PluginInterface;
use Joomla\CMS\Factory;
use Joomla\CMS\Plugin\PluginHelper;
use Joomla\DI\Container;
use Joomla\DI\ServiceProviderInterface;
use Joomla\Event\DispatcherInterface;

return new class implements ServiceProviderInterface {
    public function register(Container $container): void
    {
        $container->set(
            PluginInterface::class,
            static function (Container $container): PluginInterface {
                // The dispatcher argument supports the Joomla 5.4 constructor.
                $plugin = new DarkTheme(
                    $container->get(DispatcherInterface::class),
                    (array) PluginHelper::getPlugin('system', 'ra_darktheme')
                );
                $plugin->setApplication(Factory::getApplication());

                return $plugin;
            }
        );
    }
};
