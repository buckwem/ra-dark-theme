<?php
/** Behaviour checks with Joomla API test doubles; run with PHP 8.3+. */
namespace Joomla\CMS\Plugin {
    class CMSPlugin {
        protected $params;
        public function __construct($dispatcher, array $config) { $this->params = new \TestParams($config['params']); }
    }
}
namespace Joomla\Event {
    interface SubscriberInterface { public static function getSubscribedEvents(): array; }
}
namespace Joomla\CMS\Document {
    class HtmlDocument {
        public array $options = [];
        public \TestAssets $assets;
        public function __construct() { $this->assets = new \TestAssets(); }
        public function addScriptOptions($name, $options) { $this->options[$name] = $options; }
        public function getWebAssetManager() { return $this->assets; }
    }
}
namespace Joomla\CMS\Event\Application {
    class BeforeCompileHeadEvent {
        public function __construct(private $app, private $document) {}
        public function getApplication() { return $this->app; }
        public function getDocument() { return $this->document; }
    }
}
namespace Joomla\CMS\Uri {
    class Uri { public static string $path = '/subdirectory'; public static function root($pathOnly) { return self::$path; } }
}
namespace Joomla\CMS\Language {
    class Text { public static function _($key) { return $key; } }
}
namespace {
    define('_JEXEC', 1);
    class TestParams {
        public function __construct(private array $values) {}
        public function get($key, $default = null) { return $this->values[$key] ?? $default; }
    }
    class TestAssets {
        public array $styles = [], $scripts = [];
        public function registerAndUseStyle(...$args) { $this->styles[] = $args; }
        public function registerAndUseScript(...$args) { $this->scripts[] = $args; }
    }
    class TestInput {
        public function __construct(private string $tmpl) {}
        public function getCmd($key) { return $this->tmpl; }
    }
    class TestApplication {
        public function __construct(private string $client, private string $template, private string $tmpl) {}
        public function isClient($value) { return $this->client === $value; }
        public function getTemplate() { return $this->template; }
        public function getInput() { return new TestInput($this->tmpl); }
    }
    function expect($condition, $message) { if (!$condition) throw new \RuntimeException($message); }
    require __DIR__ . '/../extension/src/Extension/DarkTheme.php';
    function runPlugin(array $params = [], string $client = 'site', string $template = 'g5_hydrogen', string $tmpl = '', bool $html = true) {
        $doc = $html ? new \Joomla\CMS\Document\HtmlDocument() : new \stdClass();
        $plugin = new \RADarkTheme\Plugin\System\RaDarktheme\Extension\DarkTheme(null, ['params' => $params]);
        $app = new TestApplication($client, $template, $tmpl);
        $plugin->onBeforeCompileHead(new \Joomla\CMS\Event\Application\BeforeCompileHeadEvent($app, $doc));
        return $doc;
    }
    foreach ([['client'=>'administrator'], ['client'=>'api'], ['tmpl'=>'component'], ['template'=>'cassiopeia']] as $case) {
        $doc = runPlugin(...$case);
        expect(!$doc->options && !$doc->assets->styles && !$doc->assets->scripts, 'Excluded page received theme assets');
    }
    expect(runPlugin(html:false) instanceof \stdClass, 'Non-HTML response was changed');
    $doc = runPlugin();
    expect(count($doc->assets->styles) === 2 && count($doc->assets->scripts) === 2, 'Missing assets');
    expect($doc->assets->styles[0][3]['media'] === 'screen', 'Dark styles must not change print colours');
    expect($doc->assets->scripts[0][1] === '/subdirectory/media/plg_system_ra_darktheme/js/bootstrap.js', 'Incorrect subdirectory URL');
    expect(!isset($doc->assets->scripts[0][3]['defer']), 'Early palette script must run before the body renders');
    expect($doc->assets->scripts[1][4] === ['core','plg_system_ra_darktheme.bootstrap'], 'Missing runtime dependencies');
    expect($doc->options['plg_system_ra_darktheme']['defaultTheme'] === 'system', 'Incorrect default');
    $doc = runPlugin(['default_theme'=>'invalid', 'position'=>'<script>', 'show_toggle'=>'0', 'weather'=>'0']);
    $options = $doc->options['plg_system_ra_darktheme'];
    expect($options['defaultTheme'] === 'system' && $options['position'] === 'header', 'Invalid settings were not rejected');
    expect($options['showToggle'] === false && $options['weather'] === false, 'Incorrect option booleans');
    expect(count(runPlugin(['template'=>''], template:'cassiopeia')->assets->styles) === 2, 'Explicit template opt-in failed');
    $doc = runPlugin(['default_theme'=>'dark','position'=>'bottom-left']);
    expect($doc->assets->scripts[0][3]['data-ra-default'] === 'dark', 'Early palette lost the configured default');
    expect($doc->options['plg_system_ra_darktheme']['position'] === 'bottom-left', 'Position setting was lost');
    foreach (['', '/', '/subdirectory/'] as $root) {
        \Joomla\CMS\Uri\Uri::$path = $root;
        $doc = runPlugin();
        $base = rtrim($root, '/') . '/media/plg_system_ra_darktheme/';
        foreach (array_merge($doc->assets->styles, $doc->assets->scripts) as $asset) {
            expect(str_starts_with($asset[1], $base), 'Incorrect root installation asset URL');
            expect(!str_starts_with($asset[1], '//'), 'Asset URL became a hostname');
        }
    }
    echo "Passed public/document/template guards, settings, print isolation, dependencies and subdirectory URLs.\n";
}
