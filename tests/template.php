<?php
namespace Joomla\CMS {
    class Factory { public static $app; public static function getApplication() { return self::$app; } }
}
namespace Joomla\CMS\Uri {
    class Uri { public static $root; public static function root($only) { return self::$root; } }
}
namespace {
    define('_JEXEC', 1);
    class Params { public $values = []; public function get($key, $default) { return $this->values[$key] ?? $default; } }
    class Assets {
        public $styles = [], $scripts = [];
        public function registerAndUseStyle(...$args) { $this->styles[] = $args; }
        public function registerAndUseScript(...$args) { $this->scripts[] = $args; }
    }
    class Document {
        public $options; public $assets;
        public function __construct() { $this->assets = new Assets(); }
        public function addScriptOptions($key, $options) { $this->options = $options; }
        public function getWebAssetManager() { return $this->assets; }
    }
    class App {
        public $params; public $doc;
        public function __construct() { $this->params = new Params(); $this->doc = new Document(); }
        public function getDocument() { return $this->doc; }
        public function getTemplate($withParams) { return (object) ['params' => $this->params]; }
    }
    function expect($value, $message) { if (!$value) throw new \RuntimeException($message); }
    foreach (['', '/', '/subdirectory', '/subdirectory/'] as $root) {
        foreach (['system', 'light', 'dark', 'invalid'] as $default) {
            $app = new App();
            $app->params->values = ['ra_default_theme' => $default, 'ra_show_toggle' => 0, 'ra_weather' => 0];
            \Joomla\CMS\Factory::$app = $app;
            \Joomla\CMS\Uri\Uri::$root = $root;
            require __DIR__ . '/../theme-source/includes/ra-theme.php';
            expect($app->doc->options['defaultTheme'] === ($default === 'invalid' ? 'system' : $default), 'Incorrect default');
            expect(!$app->doc->options['showToggle'] && !$app->doc->options['weather'], 'Settings lost');
            foreach (array_merge($app->doc->assets->styles, $app->doc->assets->scripts) as $asset) {
                expect(str_starts_with($asset[1], rtrim($root, '/') . '/templates/ra_darktheme/ra-assets/'), 'Wrong asset URL');
                expect(!str_starts_with($asset[1], '//'), 'Protocol-relative URL');
            }
            expect($app->doc->assets->styles[0][3]['media'] === 'screen', 'Print colours changed');
            expect($app->doc->assets->scripts[1][4] === ['core', 'tpl_ra_darktheme.bootstrap'], 'Missing dependencies');
        }
    }
    echo "Passed template settings and asset tests across four root paths.\n";
}
