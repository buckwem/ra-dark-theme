// Behaviour checks for the shipped scripts. No browser automation or dependencies.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const bootstrap = fs.readFileSync('template/ra-assets/js/bootstrap.js', 'utf8');
const source = fs.readFileSync('template/ra-assets/js/theme.js', 'utf8');

function runtime({config={enabled:true, defaultTheme:'system'}, saved=null, dark=false,
  storageBlocked=false, heading=true, ready='complete', weather=false}={}) {
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName=tag; this.children=[]; this.dataset={}; this.attributes={}; }
    setAttribute(name,value) { this.attributes[name]=String(value); }
    getAttribute(name) { return this.attributes[name] ?? null; }
    removeAttribute(name) { delete this.attributes[name]; }
    append(...nodes) { for(const node of nodes){node.remove(); this.children.push(node); node.parentNode=this;} }
    before(node) { node.remove(); const p=this.parentNode; p.children.splice(p.children.indexOf(this),0,node);node.parentNode=p; }
    remove(){if(this.parentNode){const p=this.parentNode;p.children=p.children.filter(n=>n!==this);this.parentNode=null;}}
    click(){this.dispatchEvent(new Event('click'));}
    querySelector(){return this.children.find(n=>n.tagName==='iframe') || null;}
  }
  const document=new EventTarget(), window=new EventTarget(), device=new EventTarget();
  document.body=new Element('body'); document.documentElement=new Element('html');
  document.readyState=ready; document.createElement=tag=>new Element(tag);
  document.currentScript={getAttribute:()=>config?.defaultTheme || 'system'};
  const elements=()=>{const found=[];const walk=n=>{found.push(n);n.children.forEach(walk);};walk(document.body);return found;};
  document.getElementById=id=>elements().find(n=>n.id===id) || null;
  let title;
  if(heading){title=new Element('h1');title.id='ramblerstitle';document.body.append(title);}
  let link;
  if(weather){link=new Element('a');link.href='https://forecast7.com/alton/';link.setAttribute('data-textcolor','#123456');document.body.append(link);}
  document.querySelectorAll=()=>link?[link]:[];
  device.matches=dark; window.matchMedia=()=>device;
  window.Joomla={getOptions:()=>config};
  const storage=new Map(saved===null?[]:[['ra-dark-theme:preference',saved]]);
  const observers=[];
  const localStorage={getItem:key=>{if(storageBlocked)throw Error('blocked');return storage.get(key)??null;},
    setItem:(key,value)=>{if(storageBlocked)throw Error('blocked');storage.set(key,value);},
    removeItem:key=>{if(storageBlocked)throw Error('blocked');storage.delete(key);}};
  const context=vm.createContext({document,window,localStorage,
    MutationObserver:class{constructor(callback){observers.push(callback);}observe(){}}});
  if(config?.enabled)vm.runInContext(bootstrap,context);
  const earlyTheme=document.documentElement.dataset.raTheme;
  const load=()=>vm.runInContext(source,context);load();
  return {window,document,device,storage,title,link,observers,load,earlyTheme,elements,
    theme:()=>document.documentElement.dataset.raTheme,
    button:()=>document.getElementById('ra-theme-toggle'),
    ready(){document.readyState='complete';document.dispatchEvent(new Event('DOMContentLoaded'));},
    deviceChange(value){device.matches=value;device.dispatchEvent(new Event('change'));},
    storageChange(value,key='ra-dark-theme:preference'){
      const event=new Event('storage');Object.assign(event,{key,newValue:value});window.dispatchEvent(event);
    },
    addWeatherFrame(){const frame=new Element('iframe'),messages=[];frame.id='weather1';frame.contentWindow={postMessage:(...args)=>messages.push(args)};
      link.append(frame);observers.forEach(callback=>callback());return {frame,messages};}
  };
}

test('no Joomla options means no theme controls or page mutation',()=>{
  for(const config of [null,{}, {enabled:false}]){const r=runtime({config});assert.equal(r.button(),null);assert.equal(r.theme(),undefined);}
});
test('configured and saved preferences agree before and after the DOM loads',()=>{
  for(const [configured,saved,device,expected] of [['dark',null,false,'dark'],['light',null,true,'light'],
    ['system',null,true,'dark'],['dark','light',true,'light'],['light','dark',false,'dark'],
    ['dark','corrupt',false,'dark'],['dark','system',false,'light']]){
    const r=runtime({config:{enabled:true,defaultTheme:configured},saved,dark:device,ready:'loading'});
    assert.equal(r.earlyTheme,expected);assert.equal(r.theme(),expected);assert.equal(r.button(),null);
    r.ready();assert.ok(r.button());assert.equal(r.theme(),expected);
  }
});
test('toggle saves the choice and reset restores the configured device default',()=>{
  const r=runtime();r.button().click();assert.equal(r.theme(),'dark');assert.equal(r.storage.get('ra-dark-theme:preference'),'dark');
  r.deviceChange(true);r.deviceChange(false);assert.equal(r.theme(),'dark');
  r.window.RADarkTheme.resetPreference();assert.equal(r.theme(),'light');assert.equal(r.storage.size,0);
  r.deviceChange(true);assert.equal(r.theme(),'dark');
});
test('unavailable storage does not break theme switching',()=>{
  const r=runtime({storageBlocked:true,dark:true});assert.equal(r.theme(),'dark');r.button().click();assert.equal(r.theme(),'light');
  r.window.RADarkTheme.resetPreference();assert.equal(r.theme(),'dark');
});
test('tab storage updates and clear events follow the configured fallback',()=>{
  const r=runtime({config:{enabled:true,defaultTheme:'dark'}});
  r.storageChange('light');assert.equal(r.theme(),'light');
  r.storageChange('dark','unrelated');assert.equal(r.theme(),'light');
  r.storageChange(null,null);assert.equal(r.theme(),'dark');
});
test('header placement retains the title and duplicate scripts create only one switch',()=>{
  const r=runtime();assert.equal(r.title.parentNode.className,'ra-title-tools');assert.equal(r.button().parentNode,r.title.parentNode);
  r.load();assert.equal(r.elements().filter(n=>n.id==='ra-theme-toggle').length,1);
});
test('missing headers fall back to a corner and fixed positions honour configuration',()=>{
  const r=runtime({heading:false});assert.equal(r.button().dataset.position,'bottom-right');assert.equal(r.button().parentNode,r.document.body);
  const left=runtime({config:{enabled:true,position:'bottom-left'}});assert.equal(left.button().dataset.position,'bottom-left');
});
test('hiding the switch still applies the theme and translated labels describe the action',()=>{
  const hidden=runtime({config:{enabled:true,defaultTheme:'dark',showToggle:false}});assert.equal(hidden.button(),null);assert.equal(hidden.theme(),'dark');
  const r=runtime({config:{enabled:true,labels:{dark:'Choose dark',light:'Choose light'}}});
  assert.equal(r.button().getAttribute('aria-label'),'Choose dark');r.button().click();assert.equal(r.button().getAttribute('aria-label'),'Choose light');
  assert.ok(r.button().innerHTML.includes('aria-hidden="true"'));
});
test('weather iframe inserted later receives dark colours and light restores original attributes',()=>{
  const r=runtime({weather:true,dark:true});assert.equal(r.link.getAttribute('data-textcolor'),'#e7ede8');
  const {messages}=r.addWeatherFrame();assert.equal(messages.at(-1)[1],'https://weatherwidget.io');assert.equal(messages.at(-1)[0].textcolor,'#e7ede8');
  r.button().click();assert.equal(r.link.getAttribute('data-textcolor'),'#123456');assert.equal(r.link.getAttribute('data-basecolor'),null);
  assert.equal(messages.at(-1)[0].textcolor,'#123456');
});
test('weather integration can be disabled without changing the existing widget',()=>{
  const r=runtime({weather:true,config:{enabled:true,defaultTheme:'dark',weather:false}});
  assert.equal(r.link.getAttribute('data-textcolor'),'#123456');assert.equal(r.observers.length,0);
});
