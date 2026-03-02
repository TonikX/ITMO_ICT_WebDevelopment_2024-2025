/*!
* Vuetify v3.11.8
* Forged by John Leider
* Released under the MIT License.
*/
!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?t(exports,require("vue")):"function"==typeof define&&define.amd?define(["exports","vue"],t):t((e="undefined"!=typeof globalThis?globalThis:e||self).Vuetify={},e.Vue)}(this,function(e,t){"use strict"
function a(e){t.warn(`Vuetify: ${e}`)}function l(e){t.warn(`Vuetify error: ${e}`)}function n(e,a){a=Array.isArray(a)?a.slice(0,-1).map(e=>`'${e}'`).join(", ")+` or '${a.at(-1)}'`:`'${a}'`,t.warn(`[Vuetify UPGRADE] '${e}' is deprecated, use ${a} instead.`)}const o="undefined"!=typeof window,r=o&&"IntersectionObserver"in window,i=o&&("ontouchstart"in window||window.navigator.maxTouchPoints>0),s=o&&"EyeDropper"in window,u=o&&"matchMedia"in window&&"function"==typeof window.matchMedia,c=()=>u&&window.matchMedia("(prefers-reduced-motion: reduce)").matches
function d(e,t,a){(function(e,t){if(t.has(e))throw new TypeError("Cannot initialize the same private elements twice on an object")})(e,t),t.set(e,a)}function v(e,t,a){return e.set(m(e,t),a),a}function p(e,t){return e.get(m(e,t))}function m(e,t,a){if("function"==typeof e?e===t:e.has(t))return arguments.length<3?t:a
throw new TypeError("Private element is not present on this object")}function f(e,t,a){const l=t.length-1
if(l<0)return void 0===e?a:e
for(let n=0;n<l;n++){if(null==e)return a
e=e[t[n]]}return null==e||void 0===e[t[l]]?a:e[t[l]]}function g(e,t,a){return null!=e&&t&&"string"==typeof t?void 0!==e[t]?e[t]:f(e,(t=(t=t.replace(/\[(\w+)\]/g,".$1")).replace(/^\./,"")).split("."),a):a}function h(e,t,a){if(!0===t)return void 0===e?a:e
if(null==t||"boolean"==typeof t)return a
if(e!==Object(e)){if("function"!=typeof t)return a
const l=t(e,a)
return void 0===l?a:l}if("string"==typeof t)return g(e,t,a)
if(Array.isArray(t))return f(e,t,a)
if("function"!=typeof t)return a
const l=t(e,a)
return void 0===l?a:l}function y(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0
return Array.from({length:e},(e,a)=>t+a)}function b(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"px"
if(null==e||""===e)return
const a=Number(e)
return isNaN(a)?String(e):isFinite(a)?`${a}${t}`:void 0}function V(e){return null!==e&&"object"==typeof e&&!Array.isArray(e)}function w(e){let t
return null!==e&&"object"==typeof e&&((t=Object.getPrototypeOf(e))===Object.prototype||null===t)}function k(e){if(e&&"$el"in e){const t=e.$el
return t?.nodeType===Node.TEXT_NODE?t.nextElementSibling:t}return e}const S=Object.freeze({enter:"Enter",tab:"Tab",delete:"Delete",esc:"Escape",space:"Space",up:"ArrowUp",down:"ArrowDown",left:"ArrowLeft",right:"ArrowRight",end:"End",home:"Home",del:"Delete",backspace:"Backspace",insert:"Insert",pageup:"PageUp",pagedown:"PageDown",shift:"Shift"})
function x(e){return Object.keys(e)}function N(e,t){return t.every(t=>e.hasOwnProperty(t))}function C(e,t){const a={}
for(const l of t)Object.prototype.hasOwnProperty.call(e,l)&&(a[l]=e[l])
return a}function E(e,t,a){const l=Object.create(null),n=Object.create(null)
for(const a in e)t.some(e=>e instanceof RegExp?e.test(a):e===a)?l[a]=e[a]:n[a]=e[a]
return[l,n]}function I(e,t){const a={...e}
return t.forEach(e=>delete a[e]),a}const _=/^on[^a-z]/,P=e=>_.test(e),A=["onAfterscriptexecute","onAnimationcancel","onAnimationend","onAnimationiteration","onAnimationstart","onAuxclick","onBeforeinput","onBeforescriptexecute","onChange","onClick","onCompositionend","onCompositionstart","onCompositionupdate","onContextmenu","onCopy","onCut","onDblclick","onFocusin","onFocusout","onFullscreenchange","onFullscreenerror","onGesturechange","onGestureend","onGesturestart","onGotpointercapture","onInput","onKeydown","onKeypress","onKeyup","onLostpointercapture","onMousedown","onMousemove","onMouseout","onMouseover","onMouseup","onMousewheel","onPaste","onPointercancel","onPointerdown","onPointerenter","onPointerleave","onPointermove","onPointerout","onPointerover","onPointerup","onReset","onSelect","onSubmit","onTouchcancel","onTouchend","onTouchmove","onTouchstart","onTransitioncancel","onTransitionend","onTransitionrun","onTransitionstart","onWheel"],R=["ArrowUp","ArrowDown","ArrowRight","ArrowLeft","Enter","Escape","Tab"," "]
function T(e){const[t,a]=E(e,[_]),l=I(t,A),[n,o]=E(a,["class","style","id","inert",/^data-/])
return Object.assign(n,t),Object.assign(o,l),[n,o]}function B(e){return null==e?[]:Array.isArray(e)?e:[e]}function D(e,a){let l=0
const n=function(){for(var n=arguments.length,o=new Array(n),r=0;r<n;r++)o[r]=arguments[r]
clearTimeout(l),l=setTimeout(()=>e(...o),t.unref(a))}
return n.clear=()=>{clearTimeout(l)},n.immediate=e,n}function F(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0,a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:1
return Math.max(t,Math.min(a,e))}function $(e){const t=e.toString().trim()
return t.includes(".")?t.length-t.indexOf(".")-1:0}function M(e,t){return e+(arguments.length>2&&void 0!==arguments[2]?arguments[2]:"0").repeat(Math.max(0,t-e.length))}function z(e,t){return(arguments.length>2&&void 0!==arguments[2]?arguments[2]:"0").repeat(Math.max(0,t-e.length))+e}function L(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:1e3
if(e<t)return`${e} B`
const a=1024===t?["Ki","Mi","Gi"]:["k","M","G"]
let l=-1
for(;Math.abs(e)>=t&&l<a.length-1;)e/=t,++l
return`${e.toFixed(1)} ${a[l]}B`}function O(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},a=arguments.length>2?arguments[2]:void 0
const l={}
for(const t in e)l[t]=e[t]
for(const n in t){const o=e[n],r=t[n]
w(o)&&w(r)?l[n]=O(o,r,a):a&&Array.isArray(o)&&Array.isArray(r)?l[n]=a(o,r):l[n]=r}return l}function j(e){return e.map(e=>e.type===t.Fragment?j(e.children):e).flat()}function H(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:""
if(H.cache.has(e))return H.cache.get(e)
const t=e.replace(/[^a-z]/gi,"-").replace(/\B([A-Z])/g,"-$1").toLowerCase()
return H.cache.set(e,t),t}function W(e,t){if(!t||"object"!=typeof t)return[]
if(Array.isArray(t))return t.map(t=>W(e,t)).flat(1)
if(t.suspense)return W(e,t.ssContent)
if(Array.isArray(t.children))return t.children.map(t=>W(e,t)).flat(1)
if(t.component){if(Object.getOwnPropertyDescriptor(t.component.provides,e))return[t.component]
if(t.component.subTree)return W(e,t.component.subTree).flat(1)}return[]}H.cache=new Map
var Y=new WeakMap,U=new WeakMap
class G{constructor(e){d(this,Y,[]),d(this,U,0),this.size=e}get isFull(){return p(Y,this).length===this.size}push(e){p(Y,this)[p(U,this)]=e,v(U,this,(p(U,this)+1)%this.size)}values(){return p(Y,this).slice(p(U,this)).concat(p(Y,this).slice(0,p(U,this)))}clear(){p(Y,this).length=0,v(U,this,0)}}function K(e){const a=t.reactive({})
t.watchEffect(()=>{const t=e()
for(const e in t)a[e]=t[e]},{flush:"sync"})
const l={}
for(const e in a)l[e]=t.toRef(()=>a[e])
return l}function q(e,t){return e.includes(t)}function X(e){return e[2].toLowerCase()+e.slice(3)}const Z=()=>[Function,Array]
function Q(e,a){return!!(e[a="on"+t.capitalize(a)]||e[`${a}Once`]||e[`${a}Capture`]||e[`${a}OnceCapture`]||e[`${a}CaptureOnce`])}function J(e){for(var t=arguments.length,a=new Array(t>1?t-1:0),l=1;l<t;l++)a[l-1]=arguments[l]
if(Array.isArray(e))for(const t of e)t(...a)
else"function"==typeof e&&e(...a)}function ee(e){let t=!(arguments.length>1&&void 0!==arguments[1])||arguments[1]
const a=["button","[href]",'input:not([type="hidden"])',"select","textarea","details:not(:has(> summary))","details > summary","[tabindex]",'[contenteditable]:not([contenteditable="false"])',"audio[controls]","video[controls]"].map(e=>`${e}${t?':not([tabindex="-1"])':""}:not([disabled], [inert])`).join(", ")
let n
try{n=[...e.querySelectorAll(a)]}catch(e){return l(String(e)),[]}return n.filter(e=>!e.closest("[inert]")).filter(e=>!!e.offsetParent||e.getClientRects().length>0).filter(e=>!e.parentElement?.closest("details:not([open])")||"SUMMARY"===e.tagName&&"DETAILS"===e.parentElement?.tagName)}function te(e,t,a){let l,n=e.indexOf(document.activeElement)
const o="next"===t?1:-1
do{n+=o,l=e[n]}while((!l||null==l.offsetParent||!(a?.(l)??1))&&n<e.length&&n>=0)
return l}function ae(e,t){const a=ee(e)
if(null==t)e!==document.activeElement&&e.contains(document.activeElement)||a[0]?.focus()
else if("first"===t)a[0]?.focus()
else if("last"===t)a.at(-1)?.focus()
else if("number"==typeof t)a[t]?.focus()
else{const l=te(a,t)
l?l.focus():ae(e,"next"===t?"first":"last")}}function le(e){return null==e||"string"==typeof e&&""===e.trim()}function ne(){}function oe(e,t){if(!(o&&"undefined"!=typeof CSS&&void 0!==CSS.supports&&CSS.supports(`selector(${t})`)))return null
try{return!!e&&e.matches(t)}catch(e){return null}}function re(e){return e.some(e=>!t.isVNode(e)||e.type!==t.Comment&&(e.type!==t.Fragment||re(e.children)))?e:null}function ie(e,t,a){return e?.(t)??a?.(t)}function se(){const e=t.shallowRef(),a=t=>{e.value=t}
return Object.defineProperty(a,"value",{enumerable:!0,get:()=>e.value,set:t=>e.value=t}),Object.defineProperty(a,"el",{enumerable:!0,get:()=>k(e.value)}),a}function ue(e){const t=1===e.key.length,a=!e.ctrlKey&&!e.metaKey&&!e.altKey
return t&&a}function ce(e){return"string"==typeof e||"number"==typeof e||"boolean"==typeof e||"bigint"==typeof e}function de(e){return"\\^$*+?.()|{}[]".includes(e)?`\\${e}`:e}function ve(e){const a=e=>Array.isArray(e)?e.map(e=>a(e)):t.isRef(e)||t.isReactive(e)||t.isProxy(e)?a(t.toRaw(e)):w(e)?Object.keys(e).reduce((t,l)=>(t[l]=a(e[l]),t),{}):e
return a(e)}const pe=["top","bottom"],me=["start","end","left","right"]
function fe(e,t){let[a,l]=e.split(" ")
return l||(l=q(pe,a)?"start":q(me,a)?"top":"center"),{side:ge(a,t),align:ge(l,t)}}function ge(e,t){return"start"===e?t?"right":"left":"end"===e?t?"left":"right":e}function he(e){return{side:{center:"center",top:"bottom",bottom:"top",left:"right",right:"left"}[e.side],align:e.align}}function ye(e){return{side:e.side,align:{center:"center",top:"bottom",bottom:"top",left:"right",right:"left"}[e.align]}}function be(e){return{side:e.align,align:e.side}}function Ve(e){return q(pe,e.side)?"y":"x"}class we{constructor(e){const t=document.body.currentCSSZoom??1,a=e instanceof Element,l=a?1+(1-t)/t:1,{x:n,y:o,width:r,height:i}=a?e.getBoundingClientRect():e
this.x=n*l,this.y=o*l,this.width=r*l,this.height=i*l}get top(){return this.y}get bottom(){return this.y+this.height}get left(){return this.x}get right(){return this.x+this.width}}function ke(e,t){return{x:{before:Math.max(0,t.left-e.left),after:Math.max(0,e.right-t.right)},y:{before:Math.max(0,t.top-e.top),after:Math.max(0,e.bottom-t.bottom)}}}function Se(e){if(Array.isArray(e)){const t=document.body.currentCSSZoom??1,a=1+(1-t)/t
return new we({x:e[0]*a,y:e[1]*a,width:0*a,height:0*a})}return new we(e)}function xe(e){const t=new we(e),a=getComputedStyle(e),l=a.transform
if(l){let n,o,r,i,s
if(l.startsWith("matrix3d("))n=l.slice(9,-1).split(/, /),o=Number(n[0]),r=Number(n[5]),i=Number(n[12]),s=Number(n[13])
else{if(!l.startsWith("matrix("))return new we(t)
n=l.slice(7,-1).split(/, /),o=Number(n[0]),r=Number(n[3]),i=Number(n[4]),s=Number(n[5])}const u=a.transformOrigin,c=t.x-i-(1-o)*parseFloat(u),d=t.y-s-(1-r)*parseFloat(u.slice(u.indexOf(" ")+1)),v=o?t.width/o:e.offsetWidth+1,p=r?t.height/r:e.offsetHeight+1
return new we({x:c,y:d,width:v,height:p})}return new we(t)}function Ne(e,t,a){if(void 0===e.animate)return{finished:Promise.resolve()}
let l
try{l=e.animate(t,a)}catch(e){return{finished:Promise.resolve()}}return void 0===l.finished&&(l.finished=new Promise(e=>{l.onfinish=()=>{e(l)}})),l}const Ce=new WeakMap
const Ee=2.4,Ie=.2126729,_e=.7151522,Pe=.072175,Ae=.03,Re=12.82051282051282,Te=.06
function Be(e,t){const a=(e.r/255)**Ee,l=(e.g/255)**Ee,n=(e.b/255)**Ee,o=(t.r/255)**Ee,r=(t.g/255)**Ee,i=(t.b/255)**Ee
let s,u=a*Ie+l*_e+n*Pe,c=o*Ie+r*_e+i*Pe
if(u<=Ae&&(u+=(Ae-u)**1.45),c<=Ae&&(c+=(Ae-c)**1.45),Math.abs(c-u)<5e-4)return 0
if(c>u){const e=1.25*(c**.55-u**.58)
s=e<.001?0:e<.078?e-e*Re*Te:e-Te}else{const e=1.25*(c**.62-u**.57)
s=e>-.001?0:e>-.078?e-e*Re*Te:e+Te}return 100*s}const De=.20689655172413793,Fe=e=>e>De**3?Math.cbrt(e):e/(3*De**2)+4/29,$e=e=>e>De?e**3:3*De**2*(e-4/29)
function Me(e){const t=Fe,a=t(e[1])
return[116*a-16,500*(t(e[0]/.95047)-a),200*(a-t(e[2]/1.08883))]}function ze(e){const t=$e,a=(e[0]+16)/116
return[.95047*t(a+e[1]/500),t(a),1.08883*t(a-e[2]/200)]}const Le=[[3.2406,-1.5372,-.4986],[-.9689,1.8758,.0415],[.0557,-.204,1.057]],Oe=e=>e<=.0031308?12.92*e:1.055*e**(1/2.4)-.055,je=[[.4124,.3576,.1805],[.2126,.7152,.0722],[.0193,.1192,.9505]],He=e=>e<=.04045?e/12.92:((e+.055)/1.055)**2.4
function We(e){const t=Array(3),a=Oe,l=Le
for(let n=0;n<3;++n)t[n]=Math.round(255*F(a(l[n][0]*e[0]+l[n][1]*e[1]+l[n][2]*e[2])))
return{r:t[0],g:t[1],b:t[2]}}function Ye(e){let{r:t,g:a,b:l}=e
const n=[0,0,0],o=He,r=je
t=o(t/255),a=o(a/255),l=o(l/255)
for(let e=0;e<3;++e)n[e]=r[e][0]*t+r[e][1]*a+r[e][2]*l
return n}function Ue(e){return!!e&&/^(#|var\(--|(rgb|hsl)a?\()/.test(e)}const Ge=/^(?<fn>(?:rgb|hsl)a?)\((?<values>.+)\)/,Ke={rgb:(e,t,a,l)=>({r:e,g:t,b:a,a:l}),rgba:(e,t,a,l)=>({r:e,g:t,b:a,a:l}),hsl:(e,t,a,l)=>Ze({h:e,s:t,l:a,a:l}),hsla:(e,t,a,l)=>Ze({h:e,s:t,l:a,a:l}),hsv:(e,t,a,l)=>Xe({h:e,s:t,v:a,a:l}),hsva:(e,t,a,l)=>Xe({h:e,s:t,v:a,a:l})}
function qe(e){if("number"==typeof e)return(isNaN(e)||e<0||e>16777215)&&a(`'${e}' is not a valid hex color`),{r:(16711680&e)>>16,g:(65280&e)>>8,b:255&e}
if("string"==typeof e&&Ge.test(e)){const{groups:t}=e.match(Ge),{fn:a,values:l}=t,n=l.split(/,\s*|\s*\/\s*|\s+/).map((e,t)=>e.endsWith("%")||t>0&&t<3&&["hsl","hsla","hsv","hsva"].includes(a)?parseFloat(e)/100:parseFloat(e))
return Ke[a](...n)}if("string"==typeof e){let t=e.startsWith("#")?e.slice(1):e;[3,4].includes(t.length)?t=t.split("").map(e=>e+e).join(""):[6,8].includes(t.length)||a(`'${e}' is not a valid hex(a) color`)
const l=parseInt(t,16)
return(isNaN(l)||l<0||l>4294967295)&&a(`'${e}' is not a valid hex(a) color`),ot(t)}if("object"==typeof e){if(N(e,["r","g","b"]))return e
if(N(e,["h","s","l"]))return Xe(et(e))
if(N(e,["h","s","v"]))return Xe(e)}throw new TypeError(`Invalid color: ${null==e?e:String(e)||e.constructor.name}\nExpected #hex, #hexa, rgb(), rgba(), hsl(), hsla(), object or number`)}function Xe(e){const{h:t,s:a,v:l,a:n}=e,o=e=>{const n=(e+t/60)%6
return l-l*a*Math.max(Math.min(n,4-n,1),0)},r=[o(5),o(3),o(1)].map(e=>Math.round(255*e))
return{r:r[0],g:r[1],b:r[2],a:n}}function Ze(e){return Xe(et(e))}function Qe(e){if(!e)return{h:0,s:1,v:1,a:1}
const t=e.r/255,a=e.g/255,l=e.b/255,n=Math.max(t,a,l),o=Math.min(t,a,l)
let r=0
n!==o&&(n===t?r=60*(0+(a-l)/(n-o)):n===a?r=60*(2+(l-t)/(n-o)):n===l&&(r=60*(4+(t-a)/(n-o)))),r<0&&(r+=360)
const i=[r,0===n?0:(n-o)/n,n]
return{h:i[0],s:i[1],v:i[2],a:e.a}}function Je(e){const{h:t,s:a,v:l,a:n}=e,o=l-l*a/2
return{h:t,s:1===o||0===o?0:(l-o)/Math.min(o,1-o),l:o,a:n}}function et(e){const{h:t,s:a,l,a:n}=e,o=l+a*Math.min(l,1-l)
return{h:t,s:0===o?0:2-2*l/o,v:o,a:n}}function tt(e){let{r:t,g:a,b:l,a:n}=e
return void 0===n?`rgb(${t}, ${a}, ${l})`:`rgba(${t}, ${a}, ${l}, ${n})`}function at(e){return tt(Xe(e))}function lt(e){const t=Math.round(e).toString(16)
return("00".substr(0,2-t.length)+t).toUpperCase()}function nt(e){let{r:t,g:a,b:l,a:n}=e
return`#${[lt(t),lt(a),lt(l),void 0!==n?lt(Math.round(255*n)):""].join("")}`}function ot(e){e=function(e){e.startsWith("#")&&(e=e.slice(1))
e=e.replace(/([^0-9a-f])/gi,"F"),(3===e.length||4===e.length)&&(e=e.split("").map(e=>e+e).join(""))
6!==e.length&&(e=M(M(e,6),8,"F"))
return e}(e)
let[t,a,l,n]=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:1
const a=[]
let l=0
for(;l<e.length;)a.push(e.substr(l,t)),l+=t
return a}(e,2).map(e=>parseInt(e,16))
return n=void 0===n?n:n/255,{r:t,g:a,b:l,a:n}}function rt(e){return nt(Xe(e))}function it(e,t){const a=Me(Ye(e))
return a[0]=a[0]+10*t,We(ze(a))}function st(e,t){const a=Me(Ye(e))
return a[0]=a[0]-10*t,We(ze(a))}function ut(e){return Ye(qe(e))[1]}function ct(e,t){const a=ut(e),l=ut(t)
return(Math.max(a,l)+.05)/(Math.min(a,l)+.05)}function dt(e){const t=Math.abs(Be(qe(0),qe(e)))
return Math.abs(Be(qe(16777215),qe(e)))>Math.min(t,50)?"#fff":"#000"}function vt(e,t){return a=>Object.keys(e).reduce((l,n)=>{const o="object"==typeof e[n]&&null!=e[n]&&!Array.isArray(e[n])?e[n]:{type:e[n]}
return l[n]=a&&n in a?{...o,default:a[n]}:o,t&&!l[n].source&&(l[n].source=t),l},{})}const pt=vt({class:[String,Array,Object],style:{type:[String,Array,Object],default:null}},"component")
function mt(e,a){const l=t.getCurrentInstance()
if(!l)throw new Error(`[Vuetify] ${e} must be called from inside a setup function`)
return l}function ft(){const e=mt(arguments.length>0&&void 0!==arguments[0]?arguments[0]:"composables").type
return H(e?.aliasName||e?.name)}const gt=Symbol.for("vuetify:defaults")
function ht(){const e=t.inject(gt)
if(!e)throw new Error("[Vuetify] Could not find defaults instance")
return e}function yt(e,a){const l=ht(),n=t.ref(e),o=t.computed(()=>{if(t.unref(a?.disabled))return l.value
const e=t.unref(a?.scoped),o=t.unref(a?.reset),r=t.unref(a?.root)
if(null==n.value&&!(e||o||r))return l.value
let i=O(n.value,{prev:l.value})
if(e)return i
if(o||r){const e=Number(o||1/0)
for(let t=0;t<=e&&(i&&"prev"in i);t++)i=i.prev
return i&&"string"==typeof r&&r in i&&(i=O(O(i,{prev:i}),i[r])),i}return i.prev?O(i.prev,i):i})
return t.provide(gt,o),o}function bt(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},a=arguments.length>1?arguments[1]:void 0,l=arguments.length>2&&void 0!==arguments[2]?arguments[2]:ht()
const n=mt("useDefaults")
if(a=a??n.type.name??n.type.__name,!a)throw new Error("[Vuetify] Could not determine component name")
const o=t.computed(()=>l.value?.[e._as??a]),r=new Proxy(e,{get(e,t){const a=Reflect.get(e,t)
if("class"===t||"style"===t)return[o.value?.[t],a].filter(e=>null!=e)
if(function(e,t){return e.props&&(void 0!==e.props[t]||void 0!==e.props[H(t)])}(n.vnode,t))return a
const r=o.value?.[t]
if(void 0!==r)return r
const i=l.value?.global?.[t]
return void 0!==i?i:a}}),i=t.shallowRef()
return t.watchEffect(()=>{if(o.value){const e=Object.entries(o.value).filter(e=>{let[t]=e
return t.startsWith(t[0].toUpperCase())})
i.value=e.length?Object.fromEntries(e):void 0}else i.value=void 0}),{props:r,provideSubDefaults:function(){const e=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:mt("injectSelf")
const{provides:a}=t
if(a&&e in a)return a[e]}(gt,n)
t.provide(gt,t.computed(()=>i.value?O(e?.value??{},i.value):e?.value))}}}function Vt(e){if(e._setup=e._setup??e.setup,!e.name)return a("The component is missing an explicit name, unable to generate default prop value"),e
if(e._setup){e.props=vt(e.props??{},e.name)()
const t=Object.keys(e.props).filter(e=>"class"!==e&&"style"!==e)
e.filterProps=function(e){return C(e,t)},e.props._as=String,e.setup=function(t,a){const l=ht()
if(!l.value)return e._setup(t,a)
const{props:n,provideSubDefaults:o}=bt(t,t._as??e.name,l),r=e._setup(n,a)
return o(),r}}return e}function wt(){let e=!(arguments.length>0&&void 0!==arguments[0])||arguments[0]
return a=>(e?Vt:t.defineComponent)(a)}function kt(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"div",l=arguments.length>2?arguments[2]:void 0
return wt()({name:l??t.capitalize(t.camelize(e.replace(/__/g,"-"))),props:{tag:{type:String,default:a},...pt()},setup(a,l){let{slots:n}=l
return()=>t.h(a.tag,{class:[e,a.class],style:a.style},n.default?.())}})}function St(e,t){let a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:new WeakMap
if(e===t)return!0
if(e instanceof Date&&t instanceof Date&&e.getTime()!==t.getTime())return!1
if(e!==Object(e)||t!==Object(t))return!1
const l=Object.keys(e)
if(l.length!==Object.keys(t).length)return!1
const n=function(e,t,a){if(!a||ce(e)||ce(t))return null
const l=a.get(e)?.get(t)
if("boolean"==typeof l)return l
const n=a.get(t)?.get(e)
return"boolean"==typeof n?n:null}(e,t,a)
return n||(function(e,t,a,l){if(!a||ce(e)||ce(t))return
const n=a.get(e)
if(n)n.set(t,l)
else{const n=new WeakMap
n.set(t,l),a.set(e,n)}}(e,t,a,!0),l.every(l=>St(e[l],t[l],a)))}function xt(e){if("function"!=typeof e.getRootNode){for(;e.parentNode;)e=e.parentNode
return e!==document?null:document}const t=e.getRootNode()
return t!==document&&t.getRootNode({composed:!0})!==document?null:t}const Nt="cubic-bezier(0.4, 0, 0.2, 1)",Ct="cubic-bezier(0.0, 0, 0.2, 1)",Et="cubic-bezier(0.4, 0, 1, 1)",It={linear:e=>e,easeInQuad:e=>e**2,easeOutQuad:e=>e*(2-e),easeInOutQuad:e=>e<.5?2*e**2:(4-2*e)*e-1,easeInCubic:e=>e**3,easeOutCubic:e=>--e**3+1,easeInOutCubic:e=>e<.5?4*e**3:(e-1)*(2*e-2)*(2*e-2)+1,easeInQuart:e=>e**4,easeOutQuart:e=>1- --e**4,easeInOutQuart:e=>e<.5?8*e**4:1-8*--e**4,easeInQuint:e=>e**5,easeOutQuint:e=>1+--e**5,easeInOutQuint:e=>e<.5?16*e**5:1+16*--e**5,instant:e=>1}
function _t(e,t,a){return Object.keys(e).filter(e=>P(e)&&e.endsWith(t)).reduce((l,n)=>(l[n.slice(0,-t.length)]=t=>J(e[n],t,a(t)),l),{})}function Pt(e){let t=arguments.length>1&&void 0!==arguments[1]&&arguments[1]
for(;e;){if(t?Tt(e):Rt(e))return e
e=e.parentElement}return document.scrollingElement}function At(e,t){const a=[]
if(t&&e&&!t.contains(e))return a
for(;e&&(Rt(e)&&a.push(e),e!==t);)e=e.parentElement
return a}function Rt(e){if(!e||e.nodeType!==Node.ELEMENT_NODE)return!1
const t=window.getComputedStyle(e),a="scroll"===t.overflowY||"auto"===t.overflowY&&e.scrollHeight>e.clientHeight,l="scroll"===t.overflowX||"auto"===t.overflowX&&e.scrollWidth>e.clientWidth
return a||l}function Tt(e){if(!e||e.nodeType!==Node.ELEMENT_NODE)return!1
const t=window.getComputedStyle(e)
return["scroll","auto"].includes(t.overflowY)}function Bt(e){mt("useRender").render=e}const Dt=[String,Function,Object,Array],Ft=Symbol.for("vuetify:icons"),$t=vt({icon:{type:Dt},tag:{type:[String,Object,Function],required:!0}},"icon"),Mt=wt()({name:"VComponentIcon",props:$t(),setup(e,a){let{slots:l}=a
return()=>{const a=e.icon
return t.createVNode(e.tag,null,{default:()=>[e.icon?t.createVNode(a,null,null):l.default?.()]})}}}),zt=Vt({name:"VSvgIcon",inheritAttrs:!1,props:$t(),setup(e,a){let{attrs:l}=a
return()=>t.createVNode(e.tag,t.mergeProps(l,{style:null}),{default:()=>[t.createElementVNode("svg",{class:"v-icon__svg",xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",role:"img","aria-hidden":"true"},[Array.isArray(e.icon)?e.icon.map(e=>Array.isArray(e)?t.createElementVNode("path",{d:e[0],"fill-opacity":e[1]},null):t.createElementVNode("path",{d:e},null)):t.createElementVNode("path",{d:e.icon},null)])]})}}),Lt=Vt({name:"VLigatureIcon",props:$t(),setup:e=>()=>t.createVNode(e.tag,null,{default:()=>[e.icon]})}),Ot=Vt({name:"VClassIcon",props:$t(),setup:e=>()=>t.createVNode(e.tag,{class:t.normalizeClass(e.icon)},null)}),jt={collapse:"mdi-chevron-up",complete:"mdi-check",cancel:"mdi-close-circle",close:"mdi-close",delete:"mdi-close-circle",clear:"mdi-close-circle",success:"mdi-check-circle",info:"mdi-information",warning:"mdi-alert-circle",error:"mdi-close-circle",prev:"mdi-chevron-left",next:"mdi-chevron-right",checkboxOn:"mdi-checkbox-marked",checkboxOff:"mdi-checkbox-blank-outline",checkboxIndeterminate:"mdi-minus-box",delimiter:"mdi-circle",sortAsc:"mdi-arrow-up",sortDesc:"mdi-arrow-down",expand:"mdi-chevron-down",menu:"mdi-menu",subgroup:"mdi-menu-down",dropdown:"mdi-menu-down",radioOn:"mdi-radiobox-marked",radioOff:"mdi-radiobox-blank",edit:"mdi-pencil",ratingEmpty:"mdi-star-outline",ratingFull:"mdi-star",ratingHalf:"mdi-star-half-full",loading:"mdi-cached",first:"mdi-page-first",last:"mdi-page-last",unfold:"mdi-unfold-more-horizontal",file:"mdi-paperclip",plus:"mdi-plus",minus:"mdi-minus",calendar:"mdi-calendar",treeviewCollapse:"mdi-menu-down",treeviewExpand:"mdi-menu-right",tableGroupCollapse:"mdi-chevron-down",tableGroupExpand:"mdi-chevron-right",eyeDropper:"mdi-eyedropper",upload:"mdi-cloud-upload",color:"mdi-palette",command:"mdi-apple-keyboard-command",ctrl:"mdi-apple-keyboard-control",space:"mdi-keyboard-space",shift:"mdi-apple-keyboard-shift",alt:"mdi-apple-keyboard-option",enter:"mdi-keyboard-return",arrowup:"mdi-arrow-up",arrowdown:"mdi-arrow-down",arrowleft:"mdi-arrow-left",arrowright:"mdi-arrow-right",backspace:"mdi-backspace",play:"mdi-play",pause:"mdi-pause",fullscreen:"mdi-fullscreen",fullscreenExit:"mdi-fullscreen-exit",volumeHigh:"mdi-volume-high",volumeMedium:"mdi-volume-medium",volumeLow:"mdi-volume-low",volumeOff:"mdi-volume-variant-off"},Ht={component:e=>t.h(Ot,{...e,class:"mdi"})},Wt={defaults:{global:{rounded:"sm"},VAvatar:{rounded:"circle"},VAutocomplete:{variant:"underlined"},VBanner:{color:"primary"},VBtn:{color:"primary",rounded:0},VCheckbox:{color:"secondary"},VCombobox:{variant:"underlined"},VDatePicker:{color:"primary",controlHeight:44,elevation:1,rounded:0,controlVariant:"modal",VBtn:{color:"high-emphasis",rounded:"circle"}},VSelect:{variant:"underlined"},VSlider:{color:"primary"},VTabs:{color:"primary"},VTextarea:{variant:"underlined"},VTextField:{variant:"underlined"},VToolbar:{VBtn:{color:null}}},icons:{defaultSet:"mdi",sets:{mdi:Ht}},theme:{themes:{light:{colors:{primary:"#3F51B5","primary-darken-1":"#303F9F","primary-lighten-1":"#C5CAE9",secondary:"#FF4081","secondary-darken-1":"#F50057","secondary-lighten-1":"#FF80AB",accent:"#009688"}}}}},Yt={defaults:{global:{rounded:"md"},VAvatar:{rounded:"circle"},VAutocomplete:{variant:"filled"},VBanner:{color:"primary"},VBtn:{color:"primary"},VCheckbox:{color:"secondary"},VCombobox:{variant:"filled"},VDatePicker:{color:"primary",controlHeight:56,elevation:2,rounded:"md",controlVariant:"modal",VBtn:{color:"high-emphasis",rounded:"circle"}},VSelect:{variant:"filled"},VSlider:{color:"primary"},VTabs:{color:"primary"},VTextarea:{variant:"filled"},VTextField:{variant:"filled"},VToolbar:{VBtn:{color:null}}},icons:{defaultSet:"mdi",sets:{mdi:Ht}},theme:{themes:{light:{colors:{primary:"#6200EE","primary-darken-1":"#3700B3",secondary:"#03DAC6","secondary-darken-1":"#018786",error:"#B00020"}}}}},Ut={defaults:{VAppBar:{flat:!0},VAutocomplete:{variant:"outlined"},VBanner:{color:"primary"},VBottomSheet:{contentClass:"rounded-t-xl overflow-hidden"},VBtn:{color:"primary",rounded:"xl"},VBtnGroup:{rounded:"xl",VBtn:{rounded:null}},VCard:{rounded:"lg"},VCheckbox:{color:"secondary",inset:!0},VChip:{rounded:"sm"},VCombobox:{variant:"outlined"},VDateInput:{variant:"outlined"},VDatePicker:{controlHeight:48,color:"primary",divided:!0,headerColor:"",elevation:3,rounded:"xl",VBtn:{color:"high-emphasis",rounded:"circle"}},VFileInput:{variant:"outlined"},VList:{prependGap:16},VNavigationDrawer:{},VNumberInput:{variant:"outlined",VBtn:{color:void 0,rounded:void 0}},VSelect:{variant:"outlined"},VSlider:{color:"primary"},VTabs:{color:"primary"},VTextarea:{variant:"outlined"},VTextField:{variant:"outlined"},VToolbar:{VBtn:{color:null}}},icons:{defaultSet:"mdi",sets:{mdi:Ht}},theme:{themes:{light:{colors:{primary:"#6750a4",secondary:"#b4b0bb",tertiary:"#7d5260",error:"#b3261e",surface:"#fffbfe"}}}}}
var Gt=Object.freeze({__proto__:null,md1:Wt,md2:Yt,md3:Ut})
function Kt(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"content"
const l=se(),n=t.ref()
if(o){const o=new ResizeObserver(t=>{e?.(t,o),t.length&&(n.value="content"===a?t[0].contentRect:t[0].target.getBoundingClientRect())})
t.onBeforeUnmount(()=>{o.disconnect()}),t.watch(()=>l.el,(e,t)=>{t&&(o.unobserve(t),n.value=void 0),e&&o.observe(e)},{flush:"post"})}return{resizeRef:l,contentRect:t.readonly(n)}}const qt=Symbol.for("vuetify:layout"),Xt=Symbol.for("vuetify:layout-item"),Zt=vt({overlaps:{type:Array,default:()=>[]},fullHeight:Boolean},"layout"),Qt=vt({name:{type:String},order:{type:[Number,String],default:0},absolute:Boolean},"layout-item")
function Jt(){const e=t.inject(qt)
if(!e)throw new Error("[Vuetify] Could not find injected layout")
return{getLayoutItem:e.getLayoutItem,mainRect:e.mainRect,mainStyles:e.mainStyles}}function ea(e){const a=t.inject(qt)
if(!a)throw new Error("[Vuetify] Could not find injected layout")
const l=e.id??`layout-item-${t.useId()}`,n=mt("useLayoutItem")
t.provide(Xt,{id:l})
const o=t.shallowRef(!1)
t.onDeactivated(()=>o.value=!0),t.onActivated(()=>o.value=!1)
const{layoutItemStyles:r,layoutItemScrimStyles:i}=a.register(n,{...e,active:t.computed(()=>!o.value&&e.active.value),id:l})
return t.onBeforeUnmount(()=>a.unregister(l)),{layoutItemStyles:r,layoutRect:a.layoutRect,layoutItemScrimStyles:i}}function ta(e){const l=t.inject(qt,null),n=t.computed(()=>l?l.rootZIndex.value-100:1e3),o=t.ref([]),r=t.reactive(new Map),i=t.reactive(new Map),s=t.reactive(new Map),u=t.reactive(new Map),c=t.reactive(new Map),{resizeRef:d,contentRect:v}=Kt(),p=t.computed(()=>{const t=new Map,a=e.overlaps??[]
for(const e of a.filter(e=>e.includes(":"))){const[a,l]=e.split(":")
if(!o.value.includes(a)||!o.value.includes(l))continue
const n=r.get(a),s=r.get(l),u=i.get(a),c=i.get(l)
n&&s&&u&&c&&(t.set(l,{position:n.value,amount:parseInt(u.value,10)}),t.set(a,{position:s.value,amount:-parseInt(c.value,10)}))}return t}),m=t.computed(()=>{const e=[...new Set([...s.values()].map(e=>e.value))].sort((e,t)=>e-t),t=[]
for(const a of e){const e=o.value.filter(e=>s.get(e)?.value===a)
t.push(...e)}return((e,t,a,l)=>{let n={top:0,left:0,right:0,bottom:0}
const o=[{id:"",layer:{...n}}]
for(const r of e){const e=t.get(r),i=a.get(r),s=l.get(r)
if(!e||!i||!s)continue
const u={...n,[e.value]:parseInt(n[e.value],10)+(s.value?parseInt(i.value,10):0)}
o.push({id:r,layer:u}),n=u}return o})(t,r,i,u)}),f=t.computed(()=>!Array.from(c.values()).some(e=>e.value)),g=t.computed(()=>m.value[m.value.length-1].layer),h=t.toRef(()=>({"--v-layout-left":b(g.value.left),"--v-layout-right":b(g.value.right),"--v-layout-top":b(g.value.top),"--v-layout-bottom":b(g.value.bottom),...f.value?void 0:{transition:"none"}})),y=t.computed(()=>m.value.slice(1).map((e,t)=>{let{id:a}=e
const{layer:l}=m.value[t],n=i.get(a),o=r.get(a)
return{id:a,...l,size:Number(n.value),position:o.value}})),V=e=>y.value.find(t=>t.id===e),w=mt("createLayout"),k=t.shallowRef(!1)
t.onMounted(()=>{k.value=!0}),t.provide(qt,{register:(e,l)=>{let{id:d,order:v,position:g,layoutSize:h,elementSize:b,active:V,disableTransitions:S,absolute:x}=l
s.set(d,v),r.set(d,g),i.set(d,h),u.set(d,V),S&&c.set(d,S)
const N=W(Xt,w?.vnode).indexOf(e)
N>-1?o.value.splice(N,0,d):o.value.push(d)
const C=t.computed(()=>y.value.findIndex(e=>e.id===d)),E=t.computed(()=>n.value+2*m.value.length-2*C.value)
return{layoutItemStyles:t.computed(()=>{const e="left"===g.value||"right"===g.value,t="right"===g.value,l="bottom"===g.value,o=b.value??h.value,r=0===o?"%":"px",i={[g.value]:0,zIndex:E.value,transform:`translate${e?"X":"Y"}(${(V.value?0:-(0===o?100:o))*(t||l?-1:1)}${r})`,position:x.value||1e3!==n.value?"absolute":"fixed",...f.value?void 0:{transition:"none"}}
if(!k.value)return i
const s=y.value[C.value]
s||a(`[Vuetify] Could not find layout item "${d}"`)
const u=p.value.get(d)
return u&&(s[u.position]+=u.amount),{...i,height:e?`calc(100% - ${s.top}px - ${s.bottom}px)`:b.value?`${b.value}px`:void 0,left:t?void 0:`${s.left}px`,right:t?`${s.right}px`:void 0,top:"bottom"!==g.value?`${s.top}px`:void 0,bottom:"top"!==g.value?`${s.bottom}px`:void 0,width:e?b.value?`${b.value}px`:void 0:`calc(100% - ${s.left}px - ${s.right}px)`}}),layoutItemScrimStyles:t.computed(()=>({zIndex:E.value-1})),zIndex:E}},unregister:e=>{s.delete(e),r.delete(e),i.delete(e),u.delete(e),c.delete(e),o.value=o.value.filter(t=>t!==e)},mainRect:g,mainStyles:h,getLayoutItem:V,items:y,layoutRect:v,rootZIndex:n})
return{layoutClasses:t.toRef(()=>["v-layout",{"v-layout--full-height":e.fullHeight}]),layoutStyles:t.toRef(()=>({zIndex:l?n.value:void 0,position:l?"relative":void 0,overflow:l?"hidden":void 0})),getLayoutItem:V,items:y,layoutRect:v,layoutRef:d}}function aa(e,a){let l
function n(){l=t.effectScope(),l.run(()=>a.length?a(()=>{l?.stop(),n()}):a())}t.watch(e,e=>{e&&!l?n():e||(l?.stop(),l=void 0)},{immediate:!0}),t.onScopeDispose(()=>{l?.stop()})}function la(e,a,l){let n=arguments.length>3&&void 0!==arguments[3]?arguments[3]:e=>e,o=arguments.length>4&&void 0!==arguments[4]?arguments[4]:e=>e
const r=mt("useProxiedModel"),i=t.ref(void 0!==e[a]?e[a]:l),s=H(a),u=s!==a?t.computed(()=>(e[a],!(!r.vnode.props?.hasOwnProperty(a)&&!r.vnode.props?.hasOwnProperty(s)||!r.vnode.props?.hasOwnProperty(`onUpdate:${a}`)&&!r.vnode.props?.hasOwnProperty(`onUpdate:${s}`)))):t.computed(()=>(e[a],!(!r.vnode.props?.hasOwnProperty(a)||!r.vnode.props?.hasOwnProperty(`onUpdate:${a}`))))
aa(()=>!u.value,()=>{t.watch(()=>e[a],e=>{i.value=e})})
const c=t.computed({get(){const t=e[a]
return n(u.value?t:i.value)},set(l){const s=o(l),c=t.toRaw(u.value?e[a]:i.value)
c!==s&&n(c)!==l&&(i.value=s,r?.emit(`update:${a}`,s))}})
return Object.defineProperty(c,"externalValue",{get:()=>u.value?e[a]:i.value}),c}var na={badge:"Badge",open:"Open",close:"Close",dismiss:"Dismiss",confirmEdit:{ok:"OK",cancel:"Cancel"},dataIterator:{noResultsText:"No matching records found",loadingText:"Loading items..."},dataTable:{itemsPerPageText:"Rows per page:",ariaLabel:{sortDescending:"Sorted descending.",sortAscending:"Sorted ascending.",sortNone:"Not sorted.",activateNone:"Activate to remove sorting.",activateDescending:"Activate to sort descending.",activateAscending:"Activate to sort ascending."},sortBy:"Sort by"},dataFooter:{itemsPerPageText:"Items per page:",itemsPerPageAll:"All",nextPage:"Next page",prevPage:"Previous page",firstPage:"First page",lastPage:"Last page",pageText:"{0}-{1} of {2}"},dateRangeInput:{divider:"to"},datePicker:{itemsSelected:"{0} selected",range:{title:"Select dates",header:"Enter dates"},title:"Select date",header:"Enter date",input:{placeholder:"Enter date"},ariaLabel:{previousMonth:"Previous month",nextMonth:"Next month",selectYear:"Select year",previousYear:"Previous year",nextYear:"Next year",selectMonth:"Select month",selectDate:"{0}",currentDate:"Today, {0}"}},noDataText:"No data available",carousel:{prev:"Previous visual",next:"Next visual",ariaLabel:{delimiter:"Carousel slide {0} of {1}"}},calendar:{moreEvents:"{0} more",today:"Today"},input:{clear:"Clear {0}",prependAction:"{0} prepended action",appendAction:"{0} appended action",otp:"Please enter OTP character {0}"},fileInput:{counter:"{0} files",counterSize:"{0} files ({1} in total)"},fileUpload:{title:"Drag and drop files here",divider:"or",browse:"Browse Files"},timePicker:{am:"AM",pm:"PM",title:"Select Time",hour:"Hour",minute:"Minute",second:"Second"},pagination:{ariaLabel:{root:"Pagination Navigation",next:"Next page",previous:"Previous page",page:"Go to page {0}",currentPage:"Page {0}, Current page",first:"First page",last:"Last page"}},stepper:{next:"Next",prev:"Previous"},rating:{ariaLabel:{item:"Rating {0} of {1}"}},loading:"Loading...",infiniteScroll:{loadMore:"Load more",empty:"No more"},rules:{required:"This field is required",email:"Please enter a valid email",number:"This field can only contain numbers",integer:"This field can only contain integer values",capital:"This field can only contain uppercase letters",maxLength:"You must enter a maximum of {0} characters",minLength:"You must enter a minimum of {0} characters",strictLength:"The length of the entered field is invalid",exclude:"The {0} character is not allowed",notEmpty:"Please choose at least one value",pattern:"Invalid format"},hotkey:{then:"then",ctrl:"Ctrl",command:"Command",space:"Space",shift:"Shift",alt:"Alt",enter:"Enter",escape:"Escape",upArrow:"Up Arrow",downArrow:"Down Arrow",leftArrow:"Left Arrow",rightArrow:"Right Arrow",backspace:"Backspace",option:"Option",plus:"plus",shortcut:"Keyboard shortcut: {0}",or:"or"},video:{play:"Play",pause:"Pause",seek:"Seek",volume:"Volume",showVolume:"Show volume control",mute:"Mute",unmute:"Unmute",enterFullscreen:"Full screen",exitFullscreen:"Exit full screen"},colorPicker:{ariaLabel:{eyedropper:"Select color with eyedropper",hueSlider:"Hue",alphaSlider:"Alpha",redInput:"Red value",greenInput:"Green value",blueInput:"Blue value",alphaInput:"Alpha value",hueInput:"Hue value",saturationInput:"Saturation value",lightnessInput:"Lightness value",hexInput:"HEX value",hexaInput:"HEX with alpha value",changeFormat:"Change color format"}}}
const oa="$vuetify.",ra=(e,t)=>e.replace(/\{(\d+)\}/g,(e,a)=>String(t[Number(a)])),ia=(e,t,n)=>function(o){for(var r=arguments.length,i=new Array(r>1?r-1:0),s=1;s<r;s++)i[s-1]=arguments[s]
if(!o.startsWith(oa))return ra(o,i)
const u=o.replace(oa,""),c=e.value&&n.value[e.value],d=t.value&&n.value[t.value]
let v=g(c,u,null)
return v||(a(`Translation key "${o}" not found in "${e.value}", trying fallback locale`),v=g(d,u,null)),v||(l(`Translation key "${o}" not found in fallback`),v=o),"string"!=typeof v&&(l(`Translation key "${o}" has a non-string value`),v=o),ra(v,i)}
function sa(e,t){return(a,l)=>new Intl.NumberFormat([e.value,t.value],l).format(a)}function ua(e,t){return sa(e,t)(.1).includes(",")?",":"."}function ca(e,a,l){const n=la(e,a,e[a]??l.value)
return n.value=e[a]??l.value,t.watch(l,t=>{null==e[a]&&(n.value=l.value)}),n}function da(e){return a=>{const l=ca(a,"locale",e.current),n=ca(a,"fallback",e.fallback),o=ca(a,"messages",e.messages)
return{name:"vuetify",current:l,fallback:n,messages:o,decimalSeparator:t.toRef(()=>ua(l,n)),t:ia(l,n,o),n:sa(l,n),provide:da({current:l,fallback:n,messages:o})}}}const va=Symbol.for("vuetify:locale")
function pa(e){const a=e?.adapter&&(l=e?.adapter,null!=l.name)?e?.adapter:function(e){const a=t.shallowRef(e?.locale??"en"),l=t.shallowRef(e?.fallback??"en"),n=t.ref({en:na,...e?.messages})
return{name:"vuetify",current:a,fallback:l,messages:n,decimalSeparator:t.toRef(()=>e?.decimalSeparator??ua(a,l)),t:ia(a,l,n),n:sa(a,l),provide:da({current:a,fallback:l,messages:n})}}(e)
var l
const n=function(e,a){const l=t.ref(a?.rtl??{af:!1,ar:!0,bg:!1,ca:!1,ckb:!1,cs:!1,de:!1,el:!1,en:!1,es:!1,et:!1,fa:!0,fi:!1,fr:!1,hr:!1,hu:!1,he:!0,id:!1,it:!1,ja:!1,km:!1,ko:!1,lv:!1,lt:!1,nl:!1,no:!1,pl:!1,pt:!1,ro:!1,ru:!1,sk:!1,sl:!1,srCyrl:!1,srLatn:!1,sv:!1,th:!1,tr:!1,az:!1,uk:!1,vi:!1,zhHans:!1,zhHant:!1}),n=t.computed(()=>l.value[e.current.value]??!1)
return{isRtl:n,rtl:l,rtlClasses:t.toRef(()=>"v-locale--is-"+(n.value?"rtl":"ltr"))}}(a,e)
return{...a,...n}}function ma(){const e=t.inject(va)
if(!e)throw new Error("[Vuetify] Could not find injected locale instance")
return e}function fa(e){const a=t.inject(va)
if(!a)throw new Error("[Vuetify] Could not find injected locale instance")
const l=a.provide(e),n=function(e,a,l){const n=t.computed(()=>l.rtl??a.value[e.current.value]??!1)
return{isRtl:n,rtl:a,rtlClasses:t.toRef(()=>"v-locale--is-"+(n.value?"rtl":"ltr"))}}(l,a.rtl,e),o={...l,...n}
return t.provide(va,o),o}function ga(){const e=t.inject(va)
if(!e)throw new Error("[Vuetify] Could not find injected rtl instance")
return{isRtl:e.isRtl,rtlClasses:e.rtlClasses}}const ha=Symbol.for("vuetify:theme"),ya=vt({theme:String},"theme")
function ba(e,t,a,l){e.push(`${function(e,t){if(!t)return e
const a=`:where(${t})`
return":root"===e?a:`${a} ${e}`}(t,l)} {\n`,...a.map(e=>`  ${e};\n`),"}\n")}function Va(e,t){const a=e.dark?2:1,l=e.dark?1:2,n=[]
for(const[o,r]of Object.entries(e.colors)){const e=qe(r)
n.push(`--${t}theme-${o}: ${e.r},${e.g},${e.b}`),o.startsWith("on-")||n.push(`--${t}theme-${o}-overlay-multiplier: ${ut(r)>.18?a:l}`)}for(const[a,l]of Object.entries(e.variables)){const e="string"==typeof l&&l.startsWith("#")?qe(l):void 0,o=e?`${e.r}, ${e.g}, ${e.b}`:void 0
n.push(`--${t}${a}: ${o??l}`)}return n}function wa(e,t,a){const l={}
if(a)for(const n of["lighten","darken"]){const o="lighten"===n?it:st
for(const r of y(a[n],1))l[`${e}-${n}-${r}`]=nt(o(qe(t),r))}return l}function ka(e,t){if(!t)return{}
let a={}
for(const l of t.colors){const n=e[l]
n&&(a={...a,...wa(l,n,t)})}return a}function Sa(e){const t={}
for(const a of Object.keys(e)){if(a.startsWith("on-")||e[`on-${a}`])continue
const l=`on-${a}`,n=qe(e[a])
t[l]=dt(n)}return t}function xa(e,t,a){const l=function(e,t){if(!o)return null
let a=document.getElementById(e)
a||(a=document.createElement("style"),a.id=e,a.type="text/css",t&&a.setAttribute("nonce",t),document.head.appendChild(a))
return a}(e,t)
l&&(l.innerHTML=a)}function Na(e){const l=function(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{defaultTheme:"light",prefix:"v-",variations:{colors:[],lighten:0,darken:0},themes:{light:{dark:!1,colors:{background:"#FFFFFF",surface:"#FFFFFF","surface-bright":"#FFFFFF","surface-light":"#EEEEEE","surface-variant":"#424242","on-surface-variant":"#EEEEEE",primary:"#1867C0","primary-darken-1":"#1F5592",secondary:"#48A9A6","secondary-darken-1":"#018786",error:"#B00020",info:"#2196F3",success:"#4CAF50",warning:"#FB8C00"},variables:{"border-color":"#000000","border-opacity":.12,"high-emphasis-opacity":.87,"medium-emphasis-opacity":.6,"disabled-opacity":.38,"idle-opacity":.04,"hover-opacity":.04,"focus-opacity":.12,"selected-opacity":.08,"activated-opacity":.12,"pressed-opacity":.12,"dragged-opacity":.08,"theme-kbd":"#EEEEEE","theme-on-kbd":"#000000","theme-code":"#F5F5F5","theme-on-code":"#000000"}},dark:{dark:!0,colors:{background:"#121212",surface:"#212121","surface-bright":"#ccbfd6","surface-light":"#424242","surface-variant":"#c8c8c8","on-surface-variant":"#000000",primary:"#2196F3","primary-darken-1":"#277CC1",secondary:"#54B6B2","secondary-darken-1":"#48A9A6",error:"#CF6679",info:"#2196F3",success:"#4CAF50",warning:"#FB8C00"},variables:{"border-color":"#FFFFFF","border-opacity":.12,"high-emphasis-opacity":1,"medium-emphasis-opacity":.7,"disabled-opacity":.5,"idle-opacity":.1,"hover-opacity":.04,"focus-opacity":.12,"selected-opacity":.08,"activated-opacity":.12,"pressed-opacity":.16,"dragged-opacity":.08,"theme-kbd":"#424242","theme-on-kbd":"#FFFFFF","theme-code":"#343434","theme-on-code":"#CCCCCC"}}},stylesheetId:"vuetify-theme-stylesheet",scoped:!1,unimportant:!1,utilities:!0}
const t={defaultTheme:"light",prefix:"v-",variations:{colors:[],lighten:0,darken:0},themes:{light:{dark:!1,colors:{background:"#FFFFFF",surface:"#FFFFFF","surface-bright":"#FFFFFF","surface-light":"#EEEEEE","surface-variant":"#424242","on-surface-variant":"#EEEEEE",primary:"#1867C0","primary-darken-1":"#1F5592",secondary:"#48A9A6","secondary-darken-1":"#018786",error:"#B00020",info:"#2196F3",success:"#4CAF50",warning:"#FB8C00"},variables:{"border-color":"#000000","border-opacity":.12,"high-emphasis-opacity":.87,"medium-emphasis-opacity":.6,"disabled-opacity":.38,"idle-opacity":.04,"hover-opacity":.04,"focus-opacity":.12,"selected-opacity":.08,"activated-opacity":.12,"pressed-opacity":.12,"dragged-opacity":.08,"theme-kbd":"#EEEEEE","theme-on-kbd":"#000000","theme-code":"#F5F5F5","theme-on-code":"#000000"}},dark:{dark:!0,colors:{background:"#121212",surface:"#212121","surface-bright":"#ccbfd6","surface-light":"#424242","surface-variant":"#c8c8c8","on-surface-variant":"#000000",primary:"#2196F3","primary-darken-1":"#277CC1",secondary:"#54B6B2","secondary-darken-1":"#48A9A6",error:"#CF6679",info:"#2196F3",success:"#4CAF50",warning:"#FB8C00"},variables:{"border-color":"#FFFFFF","border-opacity":.12,"high-emphasis-opacity":1,"medium-emphasis-opacity":.7,"disabled-opacity":.5,"idle-opacity":.1,"hover-opacity":.04,"focus-opacity":.12,"selected-opacity":.08,"activated-opacity":.12,"pressed-opacity":.16,"dragged-opacity":.08,"theme-kbd":"#424242","theme-on-kbd":"#FFFFFF","theme-code":"#343434","theme-on-code":"#CCCCCC"}}},stylesheetId:"vuetify-theme-stylesheet",scoped:!1,unimportant:!1,utilities:!0}
if(!e)return{...t,isDisabled:!0}
const a={}
for(const[l,n]of Object.entries(e.themes??{})){const e=n.dark||"dark"===l?t.themes?.dark:t.themes?.light
a[l]=O(e,n)}return O(t,{...e,themes:a})}(e),r=t.shallowRef(l.defaultTheme),i=t.ref(l.themes),s=t.shallowRef("light"),c=t.computed({get:()=>"system"===r.value?s.value:r.value,set(e){r.value=e}}),d=t.computed(()=>{const e={}
for(const[t,a]of Object.entries(i.value)){const n={...a.colors,...ka(a.colors,l.variations)}
e[t]={...a,colors:{...n,...Sa(n)}}}return e}),v=t.toRef(()=>d.value[c.value]),p=t.toRef(()=>"system"===r.value),m=t.computed(()=>{const e=[],t=l.unimportant?"":" !important",a=l.scoped?l.prefix:""
v.value?.dark&&ba(e,":root",["color-scheme: dark"],l.scope),ba(e,":root",Va(v.value,l.prefix),l.scope)
for(const[t,a]of Object.entries(d.value))ba(e,`.${l.prefix}theme--${t}`,["color-scheme: "+(a.dark?"dark":"normal"),...Va(a,l.prefix)],l.scope)
if(l.utilities){const n=[],o=[],r=new Set(Object.values(d.value).flatMap(e=>Object.keys(e.colors)))
for(const e of r)e.startsWith("on-")?ba(o,`.${e}`,[`color: rgb(var(--${l.prefix}theme-${e}))${t}`],l.scope):(ba(n,`.${a}bg-${e}`,[`--${l.prefix}theme-overlay-multiplier: var(--${l.prefix}theme-${e}-overlay-multiplier)`,`background-color: rgb(var(--${l.prefix}theme-${e}))${t}`,`color: rgb(var(--${l.prefix}theme-on-${e}))${t}`],l.scope),ba(o,`.${a}text-${e}`,[`color: rgb(var(--${l.prefix}theme-${e}))${t}`],l.scope),ba(o,`.${a}border-${e}`,[`--${l.prefix}border-color: var(--${l.prefix}theme-${e})`],l.scope))
l.layers?e.push("@layer background {\n",...n.map(e=>`  ${e}`),"}\n","@layer foreground {\n",...o.map(e=>`  ${e}`),"}\n"):e.push(...n,...o)}let n=e.map((e,t)=>0===t?e:`    ${e}`).join("")
return l.layers&&(n="@layer vuetify.theme {\n"+e.map(e=>`  ${e}`).join("")+"\n}"),n}),f=t.toRef(()=>l.isDisabled?void 0:`${l.prefix}theme--${c.value}`),g=t.toRef(()=>Object.keys(d.value))
if(u){const V=window.matchMedia("(prefers-color-scheme: dark)")
function w(){s.value=V.matches?"dark":"light"}w(),V.addEventListener("change",w,{passive:!0}),t.getCurrentScope()&&t.onScopeDispose(()=>{V.removeEventListener("change",w)})}function h(e){"system"===e||g.value.includes(e)?c.value=e:a(`Theme "${e}" not found on the Vuetify theme instance`)}function y(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:g.value
const t=e.indexOf(c.value)
h(e[-1===t?0:(t+1)%e.length])}const b=new Proxy(c,{get:(e,t)=>Reflect.get(e,t),set:(e,t,a)=>("value"===t&&n(`theme.global.name.value = ${a}`,`theme.change('${a}')`),Reflect.set(e,t,a))})
return{install:function(e){if(l.isDisabled)return
const a=e._context.provides.usehead
if(a){function n(){return{style:[{textContent:m.value,id:l.stylesheetId,nonce:l.cspNonce||!1}]}}if(a.push){const r=a.push(n)
o&&t.watch(m,()=>{r.patch(n)})}else o?(a.addHeadObjs(t.toRef(n)),t.watchEffect(()=>a.updateDOM())):a.addHeadObjs(n())}else{function i(){xa(l.stylesheetId,l.cspNonce,m.value)}o?t.watch(m,i,{immediate:!0}):i()}},change:h,cycle:y,toggle:function(){y(arguments.length>0&&void 0!==arguments[0]?arguments[0]:["light","dark"])},isDisabled:l.isDisabled,isSystem:p,name:c,themes:i,current:v,computedThemes:d,prefix:l.prefix,themeClasses:f,styles:m,global:{name:b,current:v}}}function Ca(e){mt("provideTheme")
const a=t.inject(ha,null)
if(!a)throw new Error("Could not find Vuetify theme injection")
const l=t.toRef(()=>e.theme??a.name.value),n=t.toRef(()=>a.themes.value[l.value]),o=t.toRef(()=>a.isDisabled?void 0:`${a.prefix}theme--${l.value}`),r={...a,name:l,current:n,themeClasses:o}
return t.provide(ha,r),r}function Ea(){mt("useTheme")
const e=t.inject(ha,null)
if(!e)throw new Error("Could not find Vuetify theme injection")
return e}const Ia=vt({...pt(),...I(Zt(),["fullHeight"]),...ya()},"VApp"),_a=wt()({name:"VApp",props:Ia(),setup(e,a){let{slots:l}=a
const n=Ca(e),{layoutClasses:o,getLayoutItem:r,items:i,layoutRef:s}=ta({...e,fullHeight:!0}),{rtlClasses:u}=ga()
return Bt(()=>t.createElementVNode("div",{ref:s,class:t.normalizeClass(["v-application",n.themeClasses.value,o.value,u.value,e.class]),style:t.normalizeStyle([e.style])},[t.createElementVNode("div",{class:"v-application__wrap"},[l.default?.()])])),{getLayoutItem:r,items:i,theme:n}}}),Pa=vt({tag:{type:[String,Object,Function],default:"div"}},"tag"),Aa=vt({text:String,...pt(),...Pa()},"VToolbarTitle"),Ra=wt()({name:"VToolbarTitle",props:Aa(),setup(e,a){let{slots:l}=a
return Bt(()=>{const a=!!(l.default||l.text||e.text)
return t.createVNode(e.tag,{class:t.normalizeClass(["v-toolbar-title",e.class]),style:t.normalizeStyle(e.style)},{default:()=>[a&&t.createElementVNode("div",{class:"v-toolbar-title__placeholder"},[l.text?l.text():e.text,l.default?.()])]})}),{}}}),Ta=vt({disabled:Boolean,group:Boolean,hideOnLeave:Boolean,leaveAbsolute:Boolean,mode:String,origin:String},"transition")
function Ba(e,a,l){return wt()({name:e,props:Ta({mode:l,origin:a}),setup(a,l){let{slots:n}=l
const o={onBeforeEnter(e){a.origin&&(e.style.transformOrigin=a.origin)},onLeave(e){if(a.leaveAbsolute){const{offsetTop:t,offsetLeft:a,offsetWidth:l,offsetHeight:n}=e
e._transitionInitialStyles={position:e.style.position,top:e.style.top,left:e.style.left,width:e.style.width,height:e.style.height},e.style.position="absolute",e.style.top=`${t}px`,e.style.left=`${a}px`,e.style.width=`${l}px`,e.style.height=`${n}px`}a.hideOnLeave&&e.style.setProperty("display","none","important")},onAfterLeave(e){if(a.leaveAbsolute&&e?._transitionInitialStyles){const{position:t,top:a,left:l,width:n,height:o}=e._transitionInitialStyles
delete e._transitionInitialStyles,e.style.position=t||"",e.style.top=a||"",e.style.left=l||"",e.style.width=n||"",e.style.height=o||""}}}
return()=>{const l=a.group?t.TransitionGroup:t.Transition
return t.h(l,{name:a.disabled?"":e,css:!a.disabled,...a.group?void 0:{mode:a.mode},...a.disabled?{}:o},n.default)}}})}function Da(e,a){let l=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"in-out"
return wt()({name:e,props:{mode:{type:String,default:l},disabled:{type:Boolean,default:c()},group:Boolean},setup(l,n){let{slots:o}=n
const r=l.group?t.TransitionGroup:t.Transition
return()=>t.h(r,{name:l.disabled?"":e,css:!l.disabled,...l.disabled?{}:a},o.default)}})}function Fa(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:""
const a=arguments.length>1&&void 0!==arguments[1]&&arguments[1]?"width":"height",l=t.camelize(`offset-${a}`)
return{onBeforeEnter(e){e._parent=e.parentNode,e._initialStyle={transition:e.style.transition,overflow:e.style.overflow,[a]:e.style[a]}},onEnter(t){const n=t._initialStyle
if(!n)return
t.style.setProperty("transition","none","important"),t.style.overflow="hidden"
const o=`${t[l]}px`
t.style[a]="0",t.offsetHeight,t.style.transition=n.transition,e&&t._parent&&t._parent.classList.add(e),requestAnimationFrame(()=>{t.style[a]=o})},onAfterEnter:o,onEnterCancelled:o,onLeave(e){e._initialStyle={transition:"",overflow:e.style.overflow,[a]:e.style[a]},e.style.overflow="hidden",e.style[a]=`${e[l]}px`,e.offsetHeight,requestAnimationFrame(()=>e.style[a]="0")},onAfterLeave:n,onLeaveCancelled:n}
function n(t){e&&t._parent&&t._parent.classList.remove(e),o(t)}function o(e){if(!e._initialStyle)return
const t=e._initialStyle[a]
e.style.overflow=e._initialStyle.overflow,null!=t&&(e.style[a]=t),delete e._initialStyle}}const $a=vt({target:[Object,Array]},"v-dialog-transition"),Ma=new WeakMap,za=wt()({name:"VDialogTransition",props:$a(),setup(e,a){let{slots:l}=a
const n={onBeforeEnter(e){e.style.pointerEvents="none",e.style.visibility="hidden"},async onEnter(t,a){await new Promise(e=>requestAnimationFrame(e)),await new Promise(e=>requestAnimationFrame(e)),t.style.visibility=""
const l=Oa(e.target,t),{x:n,y:o,sx:r,sy:i,speed:s}=l
if(Ma.set(t,l),c())Ne(t,[{opacity:0},{}],{duration:125*s,easing:Ct}).finished.then(()=>a())
else{const e=Ne(t,[{transform:`translate(${n}px, ${o}px) scale(${r}, ${i})`,opacity:0},{}],{duration:225*s,easing:Ct})
La(t)?.forEach(e=>{Ne(e,[{opacity:0},{opacity:0,offset:.33},{}],{duration:450*s,easing:Nt})}),e.finished.then(()=>a())}},onAfterEnter(e){e.style.removeProperty("pointer-events")},onBeforeLeave(e){e.style.pointerEvents="none"},async onLeave(t,a){let l
await new Promise(e=>requestAnimationFrame(e)),l=!Ma.has(t)||Array.isArray(e.target)||e.target.offsetParent||e.target.getClientRects().length?Oa(e.target,t):Ma.get(t)
const{x:n,y:o,sx:r,sy:i,speed:s}=l
if(c())Ne(t,[{},{opacity:0}],{duration:85*s,easing:Et}).finished.then(()=>a())
else{Ne(t,[{},{transform:`translate(${n}px, ${o}px) scale(${r}, ${i})`,opacity:0}],{duration:125*s,easing:Et}).finished.then(()=>a()),La(t)?.forEach(e=>{Ne(e,[{},{opacity:0,offset:.2},{opacity:0}],{duration:250*s,easing:Nt})})}},onAfterLeave(e){e.style.removeProperty("pointer-events")}}
return()=>e.target?t.createVNode(t.Transition,t.mergeProps({name:"dialog-transition"},n,{css:!1}),l):t.createVNode(t.Transition,{name:"dialog-transition"},l)}})
function La(e){const t=e.querySelector(":scope > .v-card, :scope > .v-sheet, :scope > .v-list")?.children
return t&&[...t]}function Oa(e,t){const a=Se(e),l=xe(t),[n,o]=getComputedStyle(t).transformOrigin.split(" ").map(e=>parseFloat(e)),[r,i]=getComputedStyle(t).getPropertyValue("--v-overlay-anchor-origin").split(" ")
let s=a.left+a.width/2
"left"===r||"left"===i?s-=a.width/2:"right"!==r&&"right"!==i||(s+=a.width/2)
let u=a.top+a.height/2
"top"===r||"top"===i?u-=a.height/2:"bottom"!==r&&"bottom"!==i||(u+=a.height/2)
const c=a.width/l.width,d=a.height/l.height,v=Math.max(1,c,d),p=c/v||0,m=d/v||0,f=l.width*l.height/(window.innerWidth*window.innerHeight),g=f>.12?Math.min(1.5,10*(f-.12)+1):1
return{x:s-(n+l.left),y:u-(o+l.top),sx:p,sy:m,speed:g}}const ja=Ba("fab-transition","center center","out-in"),Ha=Ba("dialog-bottom-transition"),Wa=Ba("dialog-top-transition"),Ya=Ba("fade-transition"),Ua=Ba("scale-transition"),Ga=Ba("scroll-x-transition"),Ka=Ba("scroll-x-reverse-transition"),qa=Ba("scroll-y-transition"),Xa=Ba("scroll-y-reverse-transition"),Za=Ba("slide-x-transition"),Qa=Ba("slide-x-reverse-transition"),Ja=Ba("slide-y-transition"),el=Ba("slide-y-reverse-transition"),tl=Da("expand-transition",Fa()),al=Da("expand-x-transition",Fa("",!0)),ll=vt({defaults:Object,disabled:Boolean,reset:[Number,String],root:[Boolean,String],scoped:Boolean},"VDefaultsProvider"),nl=wt(!1)({name:"VDefaultsProvider",props:ll(),setup(e,a){let{slots:l}=a
const{defaults:n,disabled:o,reset:r,root:i,scoped:s}=t.toRefs(e)
return yt(n,{reset:r,root:i,scoped:s,disabled:o}),()=>l.default?.()}}),ol=vt({height:[Number,String],maxHeight:[Number,String],maxWidth:[Number,String],minHeight:[Number,String],minWidth:[Number,String],width:[Number,String]},"dimension")
function rl(e){return{dimensionStyles:t.computed(()=>{const t={},a=b(e.height),l=b(e.maxHeight),n=b(e.maxWidth),o=b(e.minHeight),r=b(e.minWidth),i=b(e.width)
return null!=a&&(t.height=a),null!=l&&(t.maxHeight=l),null!=n&&(t.maxWidth=n),null!=o&&(t.minHeight=o),null!=r&&(t.minWidth=r),null!=i&&(t.width=i),t})}}const il=vt({aspectRatio:[String,Number],contentClass:null,inline:Boolean,...pt(),...ol()},"VResponsive"),sl=wt()({name:"VResponsive",props:il(),setup(e,a){let{slots:l}=a
const{aspectStyles:n}=function(e){return{aspectStyles:t.computed(()=>{const t=Number(e.aspectRatio)
return t?{paddingBottom:String(1/t*100)+"%"}:void 0})}}(e),{dimensionStyles:o}=rl(e)
return Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-responsive",{"v-responsive--inline":e.inline},e.class]),style:t.normalizeStyle([o.value,e.style])},[t.createElementVNode("div",{class:"v-responsive__sizer",style:t.normalizeStyle(n.value)},null),l.additional?.(),l.default&&t.createElementVNode("div",{class:t.normalizeClass(["v-responsive__content",e.contentClass])},[l.default()])])),{}}})
function ul(e){return K(()=>{const{class:t,style:a}=vl(e)
return{colorClasses:t,colorStyles:a}})}function cl(e){const{colorClasses:a,colorStyles:l}=ul(()=>({text:t.toValue(e)}))
return{textColorClasses:a,textColorStyles:l}}function dl(e){const{colorClasses:a,colorStyles:l}=ul(()=>({background:t.toValue(e)}))
return{backgroundColorClasses:a,backgroundColorStyles:l}}function vl(e){const a=t.toValue(e),l=[],n={}
if(a.background)if(Ue(a.background)){if(n.backgroundColor=a.background,!a.text&&(Ue(o=a.background)&&!/^((rgb|hsl)a?\()?var\(--/.test(o))){const e=qe(a.background)
if(null==e.a||1===e.a){const t=dt(e)
n.color=t,n.caretColor=t}}}else l.push(`bg-${a.background}`)
var o
return a.text&&(Ue(a.text)?(n.color=a.text,n.caretColor=a.text):l.push(`text-${a.text}`)),{class:l,style:n}}const pl=vt({rounded:{type:[Boolean,Number,String],default:void 0},tile:Boolean},"rounded")
function ml(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:ft()
return{roundedClasses:t.computed(()=>{const l=t.isRef(e)?e.value:e.rounded,n=[]
if(!t.isRef(e)&&e.tile||!1===l)n.push("rounded-0")
else if(!0===l||""===l)n.push(`${a}--rounded`)
else if("string"==typeof l||0===l)for(const e of String(l).split(" "))n.push(`rounded-${e}`)
return n})}}const fl=vt({transition:{type:null,default:"fade-transition",validator:e=>!0!==e}},"transition"),gl=(e,a)=>{let{slots:l}=a
const{transition:n,disabled:o,group:r,...i}=e,{component:s=(r?t.TransitionGroup:t.Transition),...u}=V(n)?n:{}
let c
return c=V(n)?t.mergeProps(u,function(e){const t=["checked","disabled"]
return Object.fromEntries(Object.entries(e).filter(e=>{let[a,l]=e
return t.includes(a)?!!l:void 0!==l}))}({disabled:o,group:r}),i):t.mergeProps({name:o||!n?"":n},i),t.h(s,c,l)}
function hl(e,t){const a=e._observe?.[t.instance.$.uid]
a&&(a.observer.unobserve(e),delete e._observe[t.instance.$.uid])}const yl={mounted:function(e,t){if(!r)return
const a=t.modifiers||{},l=t.value,{handler:n,options:o}="object"==typeof l?l:{handler:l,options:{}},i=new IntersectionObserver(function(){let l=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[],o=arguments.length>1?arguments[1]:void 0
const r=e._observe?.[t.instance.$.uid]
if(!r)return
const i=l.some(e=>e.isIntersecting)
!n||a.quiet&&!r.init||a.once&&!i&&!r.init||n(i,l,o),i&&a.once?hl(e,t):r.init=!0},o)
e._observe=Object(e._observe),e._observe[t.instance.$.uid]={init:!1,observer:i},i.observe(e)},unmounted:hl},bl=vt({absolute:Boolean,alt:String,cover:Boolean,color:String,draggable:{type:[Boolean,String],default:void 0},eager:Boolean,gradient:String,lazySrc:String,options:{type:Object,default:()=>({root:void 0,rootMargin:void 0,threshold:void 0})},sizes:String,src:{type:[String,Object],default:""},crossorigin:String,referrerpolicy:String,srcset:String,position:String,...il(),...pt(),...pl(),...fl()},"VImg"),Vl=wt()({name:"VImg",directives:{vIntersect:yl},props:bl(),emits:{loadstart:e=>!0,load:e=>!0,error:e=>!0},setup(e,a){let{emit:l,slots:n}=a
const{backgroundColorClasses:o,backgroundColorStyles:i}=dl(()=>e.color),{roundedClasses:s}=ml(e),u=mt("VImg"),c=t.shallowRef(""),d=t.ref(),v=t.shallowRef(e.eager?"loading":"idle"),p=t.shallowRef(),m=t.shallowRef(),f=t.computed(()=>e.src&&"object"==typeof e.src?{src:e.src.src,srcset:e.srcset||e.src.srcset,lazySrc:e.lazySrc||e.src.lazySrc,aspect:Number(e.aspectRatio||e.src.aspect||0)}:{src:e.src,srcset:e.srcset,lazySrc:e.lazySrc,aspect:Number(e.aspectRatio||0)}),g=t.computed(()=>f.value.aspect||p.value/m.value||0)
function h(a){if((!e.eager||!a)&&(!r||a||e.eager)){if(v.value="loading",f.value.lazySrc){const e=new Image
e.src=f.value.lazySrc,S(e,null)}f.value.src&&t.nextTick(()=>{l("loadstart",d.value?.currentSrc||f.value.src),setTimeout(()=>{if(!u.isUnmounted)if(d.value?.complete){if(d.value.naturalWidth||V(),"error"===v.value)return
g.value||S(d.value,null),"loading"===v.value&&y()}else g.value||S(d.value),w()})})}}function y(){u.isUnmounted||(w(),S(d.value),v.value="loaded",l("load",d.value?.currentSrc||f.value.src))}function V(){u.isUnmounted||(v.value="error",l("error",d.value?.currentSrc||f.value.src))}function w(){const e=d.value
e&&(c.value=e.currentSrc||e.src)}t.watch(()=>e.src,()=>{h("idle"!==v.value)}),t.watch(g,(e,t)=>{!e&&t&&d.value&&S(d.value)}),t.onBeforeMount(()=>h())
let k=-1
function S(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:100
const a=()=>{if(clearTimeout(k),u.isUnmounted)return
const{naturalHeight:l,naturalWidth:n}=e
l||n?(p.value=n,m.value=l):e.complete||"loading"!==v.value||null==t?(e.currentSrc.endsWith(".svg")||e.currentSrc.startsWith("data:image/svg+xml"))&&(p.value=1,m.value=1):k=window.setTimeout(a,t)}
a()}t.onBeforeUnmount(()=>{clearTimeout(k)})
const x=t.toRef(()=>({"v-img__img--cover":e.cover,"v-img__img--contain":!e.cover})),N=()=>{if(!f.value.src||"idle"===v.value)return null
const a=t.createElementVNode("img",{class:t.normalizeClass(["v-img__img",x.value]),style:{objectPosition:e.position},crossorigin:e.crossorigin,src:f.value.src,srcset:f.value.srcset,alt:e.alt,referrerpolicy:e.referrerpolicy,draggable:e.draggable,sizes:e.sizes,ref:d,onLoad:y,onError:V},null),l=n.sources?.()
return t.createVNode(gl,{transition:e.transition,appear:!0},{default:()=>[t.withDirectives(l?t.createElementVNode("picture",{class:"v-img__picture"},[l,a]):a,[[t.vShow,"loaded"===v.value]])]})},C=()=>t.createVNode(gl,{transition:e.transition},{default:()=>[f.value.lazySrc&&"loaded"!==v.value&&t.createElementVNode("img",{class:t.normalizeClass(["v-img__img","v-img__img--preload",x.value]),style:{objectPosition:e.position},crossorigin:e.crossorigin,src:f.value.lazySrc,alt:e.alt,referrerpolicy:e.referrerpolicy,draggable:e.draggable},null)]}),E=()=>n.placeholder?t.createVNode(gl,{transition:e.transition,appear:!0},{default:()=>[("loading"===v.value||"error"===v.value&&!n.error)&&t.createElementVNode("div",{class:"v-img__placeholder"},[n.placeholder()])]}):null,I=()=>n.error?t.createVNode(gl,{transition:e.transition,appear:!0},{default:()=>["error"===v.value&&t.createElementVNode("div",{class:"v-img__error"},[n.error()])]}):null,_=()=>e.gradient?t.createElementVNode("div",{class:"v-img__gradient",style:{backgroundImage:`linear-gradient(${e.gradient})`}},null):null,P=t.shallowRef(!1)
{const e=t.watch(g,t=>{t&&(requestAnimationFrame(()=>{requestAnimationFrame(()=>{P.value=!0})}),e())})}return Bt(()=>{const a=sl.filterProps(e)
return t.withDirectives(t.createVNode(sl,t.mergeProps({class:["v-img",{"v-img--absolute":e.absolute,"v-img--booting":!P.value},o.value,s.value,e.class],style:[{width:b("auto"===e.width?p.value:e.width)},i.value,e.style]},a,{aspectRatio:g.value,"aria-label":e.alt,role:e.alt?"img":void 0}),{additional:()=>t.createElementVNode(t.Fragment,null,[t.createVNode(N,null,null),t.createVNode(C,null,null),t.createVNode(_,null,null),t.createVNode(E,null,null),t.createVNode(I,null,null)]),default:n.default}),[[yl,{handler:h,options:e.options},null,{once:!0}]])}),{currentSrc:c,image:d,state:v,naturalWidth:p,naturalHeight:m}}}),wl=vt({border:[Boolean,Number,String]},"border")
function kl(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:ft()
return{borderClasses:t.computed(()=>{const t=e.border
return!0===t||""===t?`${a}--border`:"string"==typeof t||0===t?String(t).split(" ").map(e=>`border-${e}`):[]})}}const Sl=vt({elevation:{type:[Number,String],validator(e){const t=parseInt(e)
return!isNaN(t)&&t>=0&&t<=24}}},"elevation")
function xl(e){return{elevationClasses:t.toRef(()=>{const a=t.isRef(e)?e.value:e.elevation
return null==a?[]:[`elevation-${a}`]})}}const Nl=[null,"prominent","default","comfortable","compact"],Cl=vt({absolute:Boolean,collapse:Boolean,collapsePosition:{type:String,default:"start"},color:String,density:{type:String,default:"default",validator:e=>Nl.includes(e)},extended:{type:Boolean,default:null},extensionHeight:{type:[Number,String],default:48},flat:Boolean,floating:Boolean,height:{type:[Number,String],default:64},image:String,title:String,...wl(),...pt(),...Sl(),...pl(),...Pa({tag:"header"}),...ya()},"VToolbar"),El=wt()({name:"VToolbar",props:Cl(),setup(e,a){let{slots:l}=a
const{backgroundColorClasses:n,backgroundColorStyles:o}=dl(()=>e.color),{borderClasses:r}=kl(e),{elevationClasses:i}=xl(e),{roundedClasses:s}=ml(e),{themeClasses:u}=Ca(e),{rtlClasses:c}=ga(),d=t.shallowRef(null===e.extended?!!l.extension?.():e.extended),v=t.computed(()=>parseInt(Number(e.height)+("prominent"===e.density?Number(e.height):0)-("comfortable"===e.density?8:0)-("compact"===e.density?16:0),10)),p=t.computed(()=>d.value?parseInt(Number(e.extensionHeight)+("prominent"===e.density?Number(e.extensionHeight):0)-("comfortable"===e.density?4:0)-("compact"===e.density?8:0),10):0)
return yt({VBtn:{variant:"text"}}),Bt(()=>{const a=!(!e.title&&!l.title),m=!(!l.image&&!e.image),f=l.extension?.()
return d.value=null===e.extended?!!f:e.extended,t.createVNode(e.tag,{class:t.normalizeClass(["v-toolbar",`v-toolbar--collapse-${e.collapsePosition}`,{"v-toolbar--absolute":e.absolute,"v-toolbar--collapse":e.collapse,"v-toolbar--flat":e.flat,"v-toolbar--floating":e.floating,[`v-toolbar--density-${e.density}`]:!0},n.value,r.value,i.value,s.value,u.value,c.value,e.class]),style:t.normalizeStyle([o.value,e.style])},{default:()=>[m&&t.createElementVNode("div",{key:"image",class:"v-toolbar__image"},[l.image?t.createVNode(nl,{key:"image-defaults",disabled:!e.image,defaults:{VImg:{cover:!0,src:e.image}}},l.image):t.createVNode(Vl,{key:"image-img",cover:!0,src:e.image},null)]),t.createVNode(nl,{defaults:{VTabs:{height:b(v.value)}}},{default:()=>[t.createElementVNode("div",{class:"v-toolbar__content",style:{height:b(v.value)}},[l.prepend&&t.createElementVNode("div",{class:"v-toolbar__prepend"},[l.prepend?.()]),a&&t.createVNode(Ra,{key:"title",text:e.title},{text:l.title}),l.default?.(),l.append&&t.createElementVNode("div",{class:"v-toolbar__append"},[l.append?.()])])]}),t.createVNode(nl,{defaults:{VTabs:{height:b(p.value)}}},{default:()=>[t.createVNode(tl,null,{default:()=>[d.value&&t.createElementVNode("div",{class:"v-toolbar__extension",style:{height:b(p.value)}},[f])]})]})]})}),{contentHeight:v,extensionHeight:p}}}),Il=vt({scrollTarget:{type:String},scrollThreshold:{type:[String,Number],default:300}},"scroll")
function _l(){const e=t.shallowRef(!1)
t.onMounted(()=>{window.requestAnimationFrame(()=>{e.value=!0})})
return{ssrBootStyles:t.toRef(()=>e.value?void 0:{transition:"none !important"}),isBooted:t.readonly(e)}}const Pl=vt({scrollBehavior:String,modelValue:{type:Boolean,default:!0},location:{type:String,default:"top",validator:e=>["top","bottom"].includes(e)},...Cl(),...Qt(),...Il(),height:{type:[Number,String],default:64}},"VAppBar"),Al=wt()({name:"VAppBar",props:Pl(),emits:{"update:modelValue":e=>!0},setup(e,l){let{slots:n}=l
const o=t.ref(),r=la(e,"modelValue"),i=t.computed(()=>{const t=new Set(e.scrollBehavior?.split(" ")??[])
return{hide:t.has("hide"),fullyHide:t.has("fully-hide"),inverted:t.has("inverted"),collapse:t.has("collapse"),elevate:t.has("elevate"),fadeImage:t.has("fade-image")}}),s=t.computed(()=>{const e=i.value
return e.hide||e.fullyHide||e.inverted||e.collapse||e.elevate||e.fadeImage||!r.value}),u=t.computed(()=>(o.value?.contentHeight??0)+(o.value?.extensionHeight??0)),{currentScroll:c,scrollThreshold:d,isScrollingUp:v,scrollRatio:p,isAtBottom:m,reachedBottomWhileScrollingDown:f,hasEnoughScrollableSpace:g}=function(e){let l=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{}
const{canScroll:n,layoutSize:o}=l
let r=0,i=0
const s=t.ref(null),u=t.shallowRef(0),c=t.shallowRef(0),d=t.shallowRef(0),v=t.shallowRef(!1),p=t.shallowRef(!1),m=t.shallowRef(!1),f=t.shallowRef(!1),g=t.shallowRef(!0),h=t.computed(()=>Number(e.scrollThreshold)),y=t.computed(()=>F((h.value-u.value)/h.value||0))
function b(e){return{clientHeight:"window"in e?window.innerHeight:e.clientHeight,scrollHeight:"window"in e?document.documentElement.scrollHeight:e.scrollHeight}}function V(){const e=s.value
if(!e)return
const{clientHeight:t,scrollHeight:a}=b(e),l=a-t,n=o?.value||0,r=h.value+n
g.value=l>r}function w(){V()}function k(){const e=s.value
if(!e||n&&!n.value)return
r=u.value,u.value="window"in e?e.pageYOffset:e.scrollTop
const t=e instanceof Window?document.documentElement.scrollHeight:e.scrollHeight
i!==t&&(t>i&&V(),i=t),p.value=u.value<r,d.value=Math.abs(u.value-h.value)
const{clientHeight:a,scrollHeight:l}=b(e),o=u.value+a>=l-5
!p.value&&o&&u.value>=h.value&&g.value&&(f.value=!0)
const c=Math.abs(u.value-r)>100,v=u.value<=5;(p.value&&r-u.value>1&&!o||c&&u.value<h.value||v)&&(f.value=!1),m.value=o}return t.watch(p,()=>{c.value=c.value||u.value}),t.watch(v,()=>{c.value=0}),t.onMounted(()=>{t.watch(()=>e.scrollTarget,e=>{const t=e?document.querySelector(e):window
t?t!==s.value&&(s.value?.removeEventListener("scroll",k),s.value=t,s.value.addEventListener("scroll",k,{passive:!0}),Promise.resolve().then(()=>{V()})):a(`Unable to locate element with identifier ${e}`)},{immediate:!0}),window.addEventListener("resize",w,{passive:!0})}),t.onBeforeUnmount(()=>{s.value?.removeEventListener("scroll",k),window.removeEventListener("resize",w)}),n&&t.watch(n,k,{immediate:!0}),{scrollThreshold:h,currentScroll:u,currentThreshold:d,isScrollActive:v,scrollRatio:y,isScrollingUp:p,savedScroll:c,isAtBottom:m,reachedBottomWhileScrollingDown:f,hasEnoughScrollableSpace:g}}(e,{canScroll:s,layoutSize:u}),h=t.toRef(()=>i.value.hide||i.value.fullyHide),y=t.computed(()=>e.collapse||i.value.collapse&&(i.value.inverted?p.value>0:0===p.value)),b=t.computed(()=>e.flat||i.value.fullyHide&&!r.value||i.value.elevate&&(i.value.inverted?c.value>0:0===c.value)),V=t.computed(()=>i.value.fadeImage?i.value.inverted?1-p.value:p.value:void 0),w=t.computed(()=>{if(i.value.hide&&i.value.inverted)return 0
const e=o.value?.contentHeight??0,t=o.value?.extensionHeight??0
return h.value?c.value<d.value||i.value.fullyHide?e+t:e:e+t})
aa(()=>!!e.scrollBehavior,()=>{t.watchEffect(()=>{h.value?i.value.inverted?r.value=c.value>d.value:g.value?f.value?r.value=!1:r.value=v.value&&!m.value||c.value<d.value:r.value=!0:r.value=!0})})
const{ssrBootStyles:k}=_l(),{layoutItemStyles:S}=ea({id:e.name,order:t.computed(()=>parseInt(e.order,10)),position:t.toRef(()=>e.location),layoutSize:w,elementSize:t.shallowRef(void 0),active:r,absolute:t.toRef(()=>e.absolute)})
return Bt(()=>{const a=El.filterProps(e)
return t.createVNode(El,t.mergeProps({ref:o,class:["v-app-bar",{"v-app-bar--bottom":"bottom"===e.location},e.class],style:[{...S.value,"--v-toolbar-image-opacity":V.value,height:void 0,...k.value},e.style]},a,{collapse:y.value,flat:b.value}),n)}),{}}}),Rl=[null,"default","comfortable","compact"],Tl=vt({density:{type:String,default:"default",validator:e=>Rl.includes(e)}},"density")
function Bl(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:ft()
return{densityClasses:t.toRef(()=>`${a}--density-${e.density}`)}}const Dl=["elevated","flat","tonal","outlined","text","plain"]
function Fl(e,a){return t.createElementVNode(t.Fragment,null,[e&&t.createElementVNode("span",{key:"overlay",class:t.normalizeClass(`${a}__overlay`)},null),t.createElementVNode("span",{key:"underlay",class:t.normalizeClass(`${a}__underlay`)},null)])}const $l=vt({color:String,variant:{type:String,default:"elevated",validator:e=>Dl.includes(e)}},"variant")
function Ml(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:ft()
const l=t.toRef(()=>{const{variant:l}=t.toValue(e)
return`${a}--variant-${l}`}),{colorClasses:n,colorStyles:o}=ul(()=>{const{variant:a,color:l}=t.toValue(e)
return{[["elevated","flat"].includes(a)?"background":"text"]:l}})
return{colorClasses:n,colorStyles:o,variantClasses:l}}const zl=vt({baseColor:String,divided:Boolean,direction:{type:String,default:"horizontal"},...wl(),...pt(),...Tl(),...Sl(),...pl(),...Pa(),...ya(),...$l()},"VBtnGroup"),Ll=wt()({name:"VBtnGroup",props:zl(),setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ca(e),{densityClasses:o}=Bl(e),{borderClasses:r}=kl(e),{elevationClasses:i}=xl(e),{roundedClasses:s}=ml(e)
yt({VBtn:{height:t.toRef(()=>"horizontal"===e.direction?"auto":null),baseColor:t.toRef(()=>e.baseColor),color:t.toRef(()=>e.color),density:t.toRef(()=>e.density),flat:!0,variant:t.toRef(()=>e.variant)}}),Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-btn-group",`v-btn-group--${e.direction}`,{"v-btn-group--divided":e.divided},n.value,r.value,o.value,i.value,s.value,e.class]),style:t.normalizeStyle(e.style)},l))}}),Ol=vt({modelValue:{type:null,default:void 0},multiple:Boolean,mandatory:[Boolean,String],max:Number,selectedClass:String,disabled:Boolean},"group"),jl=vt({value:null,disabled:Boolean,selectedClass:String},"group-item")
function Hl(e,a){let l=!(arguments.length>2&&void 0!==arguments[2])||arguments[2]
const n=mt("useGroupItem")
if(!n)throw new Error("[Vuetify] useGroupItem composable must be used inside a component setup function")
const o=t.useId()
t.provide(Symbol.for(`${a.description}:id`),o)
const r=t.inject(a,null)
if(!r){if(!l)return r
throw new Error(`[Vuetify] Could not find useGroup injection with symbol ${a.description}`)}const i=t.toRef(()=>e.value),s=t.computed(()=>!(!r.disabled.value&&!e.disabled))
function u(){r?.register({id:o,value:i,disabled:s},n)}function c(){r?.unregister(o)}u(),t.onBeforeUnmount(()=>c())
const d=t.computed(()=>r.isSelected(o)),v=t.computed(()=>r.items.value[0].id===o),p=t.computed(()=>r.items.value[r.items.value.length-1].id===o),m=t.computed(()=>d.value&&[r.selectedClass.value,e.selectedClass])
return t.watch(d,e=>{n.emit("group:selected",{value:e})},{flush:"sync"}),{id:o,isSelected:d,isFirst:v,isLast:p,toggle:()=>r.select(o,!d.value),select:e=>r.select(o,e),selectedClass:m,value:i,disabled:s,group:r,register:u,unregister:c}}function Wl(e,l){let n=!1
const o=t.reactive([]),r=la(e,"modelValue",[],e=>void 0===e?[]:Yl(o,null===e?[null]:B(e)),t=>{const a=function(e,t){const a=[]
return t.forEach(t=>{const l=e.findIndex(e=>e.id===t)
if(~l){const t=e[l]
a.push(void 0!==t.value?t.value:l)}}),a}(o,t)
return e.multiple?a:a[0]}),i=mt("useGroup")
function s(){const t=o.find(e=>!e.disabled)
t&&"force"===e.mandatory&&!r.value.length&&(r.value=[t.id])}function u(t){if(e.multiple&&a('This method is not supported when using "multiple" prop'),r.value.length){const e=r.value[0],a=o.findIndex(t=>t.id===e)
let l=(a+t)%o.length,n=o[l]
for(;n.disabled&&l!==a;)l=(l+t)%o.length,n=o[l]
if(n.disabled)return
r.value=[o[l].id]}else{const e=o.find(e=>!e.disabled)
e&&(r.value=[e.id])}}t.onMounted(()=>{s()}),t.onBeforeUnmount(()=>{n=!0}),t.onUpdated(()=>{for(let e=0;e<o.length;e++)o[e].useIndexAsValue&&(o[e].value=e)})
const c={register:function(e,a){const n=e,r=W(Symbol.for(`${l.description}:id`),i?.vnode).indexOf(a)
void 0===t.unref(n.value)&&(n.value=r,n.useIndexAsValue=!0),r>-1?o.splice(r,0,n):o.push(n)},unregister:function(e){if(n)return
s()
const t=o.findIndex(t=>t.id===e)
o.splice(t,1)},selected:r,select:function(t,a){const l=o.find(e=>e.id===t)
if(!a||!l?.disabled)if(e.multiple){const l=r.value.slice(),n=l.findIndex(e=>e===t),o=~n
if(a=a??!o,o&&e.mandatory&&l.length<=1)return
if(!o&&null!=e.max&&l.length+1>e.max)return
n<0&&a?l.push(t):n>=0&&!a&&l.splice(n,1),r.value=l}else{const l=r.value.includes(t)
if(e.mandatory&&l)return
if(!l&&!a)return
r.value=a??!l?[t]:[]}},disabled:t.toRef(()=>e.disabled),prev:()=>u(o.length-1),next:()=>u(1),isSelected:e=>r.value.includes(e),selectedClass:t.toRef(()=>e.selectedClass),items:t.toRef(()=>o),getItemIndex:e=>function(e,t){const a=Yl(e,[t])
return a.length?e.findIndex(e=>e.id===a[0]):-1}(o,e)}
return t.provide(l,c),c}function Yl(e,t){const a=[]
return t.forEach(t=>{const l=e.find(e=>St(t,e.value)),n=e[t]
void 0!==l?.value?a.push(l.id):n?.useIndexAsValue&&a.push(n.id)}),a}const Ul=Symbol.for("vuetify:v-btn-toggle"),Gl=vt({...zl(),...Ol()},"VBtnToggle"),Kl=wt()({name:"VBtnToggle",props:Gl(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const{isSelected:n,next:o,prev:r,select:i,selected:s}=Wl(e,Ul)
return Bt(()=>{const a=Ll.filterProps(e)
return t.createVNode(Ll,t.mergeProps({class:["v-btn-toggle",e.class]},a,{style:e.style}),{default:()=>[l.default?.({isSelected:n,next:o,prev:r,select:i,selected:s})]})}),{next:o,prev:r,select:i}}}),ql=["x-small","small","default","large","x-large"],Xl=vt({size:{type:[String,Number],default:"default"}},"size")
function Zl(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:ft()
return K(()=>{const a=e.size
let l,n
return q(ql,a)?l=`${t}--size-${a}`:a&&(n={width:b(a),height:b(a)}),{sizeClasses:l,sizeStyles:n}})}const Ql=vt({color:String,disabled:Boolean,start:Boolean,end:Boolean,icon:Dt,opacity:[String,Number],...pt(),...Xl(),...Pa({tag:"i"}),...ya()},"VIcon"),Jl=wt()({name:"VIcon",props:Ql(),setup(e,l){let{attrs:n,slots:o}=l
const r=t.shallowRef(),{themeClasses:i}=Ea(),{iconData:s}=(e=>{const l=t.inject(Ft)
if(!l)throw new Error("Missing Vuetify Icons provide!")
return{iconData:t.computed(()=>{const n=t.toValue(e)
if(!n)return{component:Mt}
let o=n
if("string"==typeof o&&(o=o.trim(),o.startsWith("$")&&(o=l.aliases?.[o.slice(1)])),o||a(`Could not find aliased icon "${n}"`),Array.isArray(o))return{component:zt,icon:o}
if("string"!=typeof o)return{component:Mt,icon:o}
const r=Object.keys(l.sets).find(e=>"string"==typeof o&&o.startsWith(`${e}:`)),i=r?o.slice(r.length+1):o
return{component:l.sets[r??l.defaultSet].component,icon:i}})}})(()=>r.value||e.icon),{sizeClasses:u}=Zl(e),{textColorClasses:c,textColorStyles:d}=cl(()=>e.color)
return Bt(()=>{const a=o.default?.()
a&&(r.value=j(a).filter(e=>e.type===t.Text&&e.children&&"string"==typeof e.children)[0]?.children)
const l=!(!n.onClick&&!n.onClickOnce)
return t.createVNode(s.value.component,{tag:e.tag,icon:s.value.icon,class:t.normalizeClass(["v-icon","notranslate",i.value,u.value,c.value,{"v-icon--clickable":l,"v-icon--disabled":e.disabled,"v-icon--start":e.start,"v-icon--end":e.end},e.class]),style:t.normalizeStyle([{"--v-icon-opacity":e.opacity},u.value?void 0:{fontSize:b(e.size),height:b(e.size),width:b(e.size)},d.value,e.style]),role:l?"button":void 0,"aria-hidden":!l,tabindex:l?e.disabled?-1:0:void 0},{default:()=>[a]})}),{}}})
function en(e,a){const l=t.ref(),n=t.shallowRef(!1)
if(r){const e=new IntersectionObserver(e=>{n.value=!!e.find(e=>e.isIntersecting)},a)
t.onScopeDispose(()=>{e.disconnect()}),t.watch(l,(t,a)=>{a&&(e.unobserve(a),n.value=!1),t&&e.observe(t)},{flush:"post"})}return{intersectionRef:l,isIntersecting:n}}const tn=vt({bgColor:String,color:String,indeterminate:[Boolean,String],rounded:Boolean,modelValue:{type:[Number,String],default:0},rotate:{type:[Number,String],default:0},width:{type:[Number,String],default:4},...pt(),...Xl(),...Pa({tag:"div"}),...ya()},"VProgressCircular"),an=wt()({name:"VProgressCircular",props:tn(),setup(e,a){let{slots:l}=a
const n=2*Math.PI*20,o=t.ref(),{themeClasses:r}=Ca(e),{sizeClasses:i,sizeStyles:s}=Zl(e),{textColorClasses:u,textColorStyles:d}=cl(()=>e.color),{textColorClasses:v,textColorStyles:p}=cl(()=>e.bgColor),{intersectionRef:m,isIntersecting:f}=en(),{resizeRef:g,contentRect:h}=Kt(),y=t.toRef(()=>F(parseFloat(e.modelValue),0,100)),V=t.toRef(()=>Number(e.width)),w=t.toRef(()=>s.value?Number(e.size):h.value?h.value.width:Math.max(V.value,32)),k=t.toRef(()=>20/(1-V.value/w.value)*2),S=t.toRef(()=>V.value/w.value*k.value),x=t.toRef(()=>{const t=(100-y.value)/100*n
return e.rounded&&y.value>0&&y.value<100?b(Math.min(n-.01,t+S.value)):b(t)}),N=t.computed(()=>{const t=Number(e.rotate)
return e.rounded?t+S.value/2/n*360:t})
return t.watchEffect(()=>{m.value=o.value,g.value=o.value}),Bt(()=>t.createVNode(e.tag,{ref:o,class:t.normalizeClass(["v-progress-circular",{"v-progress-circular--indeterminate":!!e.indeterminate,"v-progress-circular--visible":f.value,"v-progress-circular--disable-shrink":e.indeterminate&&("disable-shrink"===e.indeterminate||c())},r.value,i.value,u.value,e.class]),style:t.normalizeStyle([s.value,d.value,e.style]),role:"progressbar","aria-valuemin":"0","aria-valuemax":"100","aria-valuenow":e.indeterminate?void 0:y.value},{default:()=>[t.createElementVNode("svg",{style:{transform:`rotate(calc(-90deg + ${N.value}deg))`},xmlns:"http://www.w3.org/2000/svg",viewBox:`0 0 ${k.value} ${k.value}`},[t.createElementVNode("circle",{class:t.normalizeClass(["v-progress-circular__underlay",v.value]),style:t.normalizeStyle(p.value),fill:"transparent",cx:"50%",cy:"50%",r:20,"stroke-width":S.value,"stroke-dasharray":n,"stroke-dashoffset":0},null),t.createElementVNode("circle",{class:"v-progress-circular__overlay",fill:"transparent",cx:"50%",cy:"50%",r:20,"stroke-width":S.value,"stroke-dasharray":n,"stroke-dashoffset":x.value,"stroke-linecap":e.rounded?"round":void 0},null)]),l.default&&t.createElementVNode("div",{class:"v-progress-circular__content"},[l.default({value:y.value})])]})),{}}}),ln={center:"center",top:"bottom",bottom:"top",left:"right",right:"left"},nn=vt({location:String},"location")
function on(e){let a=arguments.length>1&&void 0!==arguments[1]&&arguments[1],l=arguments.length>2?arguments[2]:void 0
const{isRtl:n}=ga(),o=t.computed(()=>{if(!e.location)return{}
const{side:t,align:o}=fe(e.location.split(" ").length>1?e.location:`${e.location} center`,n.value)
function r(e){return l?l(e):0}const i={}
return"center"!==t&&(a?i[ln[t]]=`calc(100% - ${r(t)}px)`:i[t]=0),"center"!==o?a?i[ln[o]]=`calc(100% - ${r(o)}px)`:i[o]=0:("center"===t?i.top=i.left="50%":i[{top:"left",bottom:"left",left:"top",right:"top"}[t]]="50%",i.transform={top:"translateX(-50%)",bottom:"translateX(-50%)",left:"translateY(-50%)",right:"translateY(-50%)",center:"translate(-50%, -50%)"}[t]),i})
return{locationStyles:o}}const rn=vt({chunkCount:{type:[Number,String],default:null},chunkWidth:{type:[Number,String],default:null},chunkGap:{type:[Number,String],default:4}},"chunks")
const sn=vt({absolute:Boolean,active:{type:Boolean,default:!0},bgColor:String,bgOpacity:[Number,String],bufferValue:{type:[Number,String],default:0},bufferColor:String,bufferOpacity:[Number,String],clickable:Boolean,color:String,height:{type:[Number,String],default:4},indeterminate:Boolean,max:{type:[Number,String],default:100},modelValue:{type:[Number,String],default:0},opacity:[Number,String],reverse:Boolean,stream:Boolean,striped:Boolean,roundedBar:Boolean,...rn(),...pt(),...nn({location:"top"}),...pl(),...Pa(),...ya()},"VProgressLinear"),un=wt()({name:"VProgressLinear",props:sn(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=t.ref(),o=la(e,"modelValue"),{isRtl:r,rtlClasses:i}=ga(),{themeClasses:s}=Ca(e),{locationStyles:u}=on(e),{textColorClasses:c,textColorStyles:d}=cl(()=>e.color),{backgroundColorClasses:v,backgroundColorStyles:p}=dl(()=>e.bgColor||e.color),{backgroundColorClasses:m,backgroundColorStyles:f}=dl(()=>e.bufferColor||e.bgColor||e.color),{backgroundColorClasses:g,backgroundColorStyles:h}=dl(()=>e.color),{roundedClasses:y}=ml(e),{intersectionRef:V,isIntersecting:w}=en(),k=t.computed(()=>parseFloat(e.max)),S=t.computed(()=>parseFloat(e.height)),x=t.computed(()=>F(parseFloat(e.bufferValue)/k.value*100,0,100)),N=t.computed(()=>F(parseFloat(o.value)/k.value*100,0,100)),C=t.computed(()=>r.value!==e.reverse),E=t.computed(()=>e.indeterminate?"fade-transition":"slide-x-transition"),I=t.shallowRef(0),{hasChunks:_,chunksMaskStyles:P,snapValueToChunk:A}=function(e,a){const l=t.toRef(()=>!!e.chunkCount||!!e.chunkWidth),n=t.computed(()=>{const l=t.toValue(a)
if(!l)return 0
if(!e.chunkCount)return Number(e.chunkWidth)
const n=Number(e.chunkCount)
return(l-Number(e.chunkGap)*(n-1))/n}),o=t.toRef(()=>Number(e.chunkGap)),r=t.computed(()=>{if(!l.value)return{}
const e=b(o.value),t=b(n.value)
return{maskRepeat:"repeat-x",maskImage:`linear-gradient(90deg, #000, #000 ${t}, transparent ${t}, transparent)`,maskSize:`calc(${t} + ${e}) 100%`}})
return{hasChunks:l,chunksMaskStyles:r,snapValueToChunk:function(e){const l=t.toValue(a)
if(!l)return e
const r=100*o.value/l,i=100*(n.value+o.value)/l
return F(0,Math.floor((e+r)/i)*i-r/2,100)}}}(e,I)
aa(_,()=>{const{resizeRef:e}=Kt(e=>I.value=e[0].contentRect.width)
t.watchEffect(()=>e.value=n.value)})
const R=t.computed(()=>_.value?A(x.value):x.value),T=t.computed(()=>_.value?A(N.value):N.value)
function B(e){if(!V.value)return
const{left:t,right:a,width:l}=V.value.getBoundingClientRect(),n=C.value?l-e.clientX+(a-l):e.clientX-t
o.value=Math.round(n/l*k.value)}return t.watchEffect(()=>{V.value=n.value}),Bt(()=>t.createVNode(e.tag,{ref:n,class:t.normalizeClass(["v-progress-linear",{"v-progress-linear--absolute":e.absolute,"v-progress-linear--active":e.active&&w.value,"v-progress-linear--reverse":C.value,"v-progress-linear--rounded":e.rounded,"v-progress-linear--rounded-bar":e.roundedBar,"v-progress-linear--striped":e.striped,"v-progress-linear--clickable":e.clickable},y.value,s.value,i.value,e.class]),style:t.normalizeStyle([{bottom:"bottom"===e.location?0:void 0,top:"top"===e.location?0:void 0,height:e.active?b(S.value):0,"--v-progress-linear-height":b(S.value),...e.absolute?u.value:{}},P.value,e.style]),role:"progressbar","aria-hidden":e.active?"false":"true","aria-valuemin":"0","aria-valuemax":e.max,"aria-valuenow":e.indeterminate?void 0:Math.min(parseFloat(o.value),k.value),onClick:e.clickable&&B},{default:()=>[e.stream&&t.createElementVNode("div",{key:"stream",class:t.normalizeClass(["v-progress-linear__stream",c.value]),style:{...d.value,[C.value?"left":"right"]:b(-S.value),borderTop:`${b(S.value/2)} dotted`,opacity:parseFloat(e.bufferOpacity),top:`calc(50% - ${b(S.value/4)})`,width:b(100-x.value,"%"),"--v-progress-linear-stream-to":b(S.value*(C.value?1:-1))}},null),t.createElementVNode("div",{class:t.normalizeClass(["v-progress-linear__background",v.value]),style:t.normalizeStyle([p.value,{opacity:parseFloat(e.bgOpacity),width:e.stream?0:void 0}])},null),t.createElementVNode("div",{class:t.normalizeClass(["v-progress-linear__buffer",m.value]),style:t.normalizeStyle([f.value,{opacity:parseFloat(e.bufferOpacity),width:b(R.value,"%")}])},null),t.createVNode(t.Transition,{name:E.value},{default:()=>[e.indeterminate?t.createElementVNode("div",{class:"v-progress-linear__indeterminate"},[["long","short"].map(e=>t.createElementVNode("div",{key:e,class:t.normalizeClass(["v-progress-linear__indeterminate",e,g.value]),style:t.normalizeStyle(h.value)},null))]):t.createElementVNode("div",{class:t.normalizeClass(["v-progress-linear__determinate",g.value]),style:t.normalizeStyle([h.value,{width:b(T.value,"%")}])},null)]}),l.default&&t.createElementVNode("div",{class:"v-progress-linear__content"},[l.default({value:N.value,buffer:x.value})])]})),{}}}),cn=vt({loading:[Boolean,String]},"loader")
function dn(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:ft()
return{loaderClasses:t.toRef(()=>({[`${a}--loading`]:e.loading}))}}function vn(e,a){let{slots:l}=a
return t.createElementVNode("div",{class:t.normalizeClass(`${e.name}__loader`)},[l.default?.({color:e.color,isActive:e.active})||t.createVNode(un,{absolute:e.absolute,active:e.active,color:e.color,height:"2",indeterminate:!0},null)])}const pn=["static","relative","fixed","absolute","sticky"],mn=vt({position:{type:String,validator:e=>pn.includes(e)}},"position")
function fn(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:ft()
return{positionClasses:t.toRef(()=>e.position?`${a}--${e.position}`:void 0)}}function gn(){return mt("useRouter")?.proxy?.$router}function hn(e,a){const l=t.resolveDynamicComponent("RouterLink"),n=t.toRef(()=>!(!e.href&&!e.to)),o=t.computed(()=>n?.value||Q(a,"click")||Q(e,"click"))
if("string"==typeof l||!("useLink"in l)){const a=t.toRef(()=>e.href)
return{isLink:n,isRouterLink:t.toRef(()=>!1),isClickable:o,href:a,linkProps:t.reactive({href:a})}}const r=l.useLink({to:t.toRef(()=>e.to||""),replace:t.toRef(()=>e.replace)}),i=t.computed(()=>e.to?r:void 0),s=function(){const e=mt("useRoute")
return t.computed(()=>e?.proxy?.$route)}(),u=t.computed(()=>!!i.value&&(e.exact?s.value?i.value.isExactActive?.value&&St(i.value.route.value.query,s.value.query):i.value.isExactActive?.value??!1:i.value.isActive?.value??!1)),c=t.computed(()=>e.to?i.value?.route.value.href:e.href),d=t.toRef(()=>!!e.to)
return{isLink:n,isRouterLink:d,isClickable:o,isActive:u,route:i.value?.route,navigate:i.value?.navigate,href:c,linkProps:t.reactive({href:c,"aria-current":t.toRef(()=>u.value?"page":void 0),"aria-disabled":t.toRef(()=>e.disabled&&n.value?"true":void 0),tabindex:t.toRef(()=>e.disabled&&n.value?"-1":void 0)})}}const yn=vt({href:String,replace:Boolean,to:[String,Object],exact:Boolean},"router")
let bn=!1
const Vn=Symbol("rippleStop")
function wn(e,t){e.style.transform=t,e.style.webkitTransform=t}function kn(e){return"TouchEvent"===e.constructor.name}function Sn(e){return"KeyboardEvent"===e.constructor.name}const xn={show(e,t){let a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{}
if(!t?._ripple?.enabled)return
const l=document.createElement("span"),n=document.createElement("span")
l.appendChild(n),l.className="v-ripple__container",a.class&&(l.className+=` ${a.class}`)
const{radius:o,scale:r,x:i,y:s,centerX:u,centerY:c}=function(e,t){let a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},l=0,n=0
if(!Sn(e)){const a=t.getBoundingClientRect(),o=kn(e)?e.touches[e.touches.length-1]:e
l=o.clientX-a.left,n=o.clientY-a.top}let o=0,r=.3
t._ripple?.circle?(r=.15,o=t.clientWidth/2,o=a.center?o:o+Math.sqrt((l-o)**2+(n-o)**2)/4):o=Math.sqrt(t.clientWidth**2+t.clientHeight**2)/2
const i=(t.clientWidth-2*o)/2+"px",s=(t.clientHeight-2*o)/2+"px"
return{radius:o,scale:r,x:a.center?i:l-o+"px",y:a.center?s:n-o+"px",centerX:i,centerY:s}}(e,t,a),d=2*o+"px"
n.className="v-ripple__animation",n.style.width=d,n.style.height=d,t.appendChild(l)
const v=window.getComputedStyle(t)
v&&"static"===v.position&&(t.style.position="relative",t.dataset.previousPosition="static"),n.classList.add("v-ripple__animation--enter"),n.classList.add("v-ripple__animation--visible"),wn(n,`translate(${i}, ${s}) scale3d(${r},${r},${r})`),n.dataset.activated=String(performance.now()),requestAnimationFrame(()=>{requestAnimationFrame(()=>{n.classList.remove("v-ripple__animation--enter"),n.classList.add("v-ripple__animation--in"),wn(n,`translate(${u}, ${c}) scale3d(1,1,1)`)})})},hide(e){if(!e?._ripple?.enabled)return
const t=e.getElementsByClassName("v-ripple__animation")
if(0===t.length)return
const a=Array.from(t).findLast(e=>!e.dataset.isHiding)
if(!a)return
a.dataset.isHiding="true"
const l=performance.now()-Number(a.dataset.activated),n=Math.max(250-l,0)
setTimeout(()=>{a.classList.remove("v-ripple__animation--in"),a.classList.add("v-ripple__animation--out"),setTimeout(()=>{1===e.getElementsByClassName("v-ripple__animation").length&&e.dataset.previousPosition&&(e.style.position=e.dataset.previousPosition,delete e.dataset.previousPosition),a.parentNode?.parentNode===e&&e.removeChild(a.parentNode)},300)},n)}}
function Nn(e){return void 0===e||!!e}function Cn(e){const t={},a=e.currentTarget
if(a?._ripple&&!a._ripple.touched&&!e[Vn]){if(e[Vn]=!0,kn(e))a._ripple.touched=!0,a._ripple.isTouch=!0
else if(a._ripple.isTouch)return
if(t.center=a._ripple.centered||Sn(e),a._ripple.class&&(t.class=a._ripple.class),kn(e)){if(a._ripple.showTimerCommit)return
a._ripple.showTimerCommit=()=>{xn.show(e,a,t)},a._ripple.showTimer=window.setTimeout(()=>{a?._ripple?.showTimerCommit&&(a._ripple.showTimerCommit(),a._ripple.showTimerCommit=null)},80)}else xn.show(e,a,t)}}function En(e){e[Vn]=!0}function In(e){const t=e.currentTarget
if(t?._ripple){if(window.clearTimeout(t._ripple.showTimer),"touchend"===e.type&&t._ripple.showTimerCommit)return t._ripple.showTimerCommit(),t._ripple.showTimerCommit=null,void(t._ripple.showTimer=window.setTimeout(()=>{In(e)}))
window.setTimeout(()=>{t._ripple&&(t._ripple.touched=!1)}),xn.hide(t)}}function _n(e){const t=e.currentTarget
t?._ripple&&(t._ripple.showTimerCommit&&(t._ripple.showTimerCommit=null),window.clearTimeout(t._ripple.showTimer))}let Pn=!1
function An(e){Pn=!1,In(e)}function Rn(e){Pn&&(Pn=!1,In(e))}function Tn(e,t,a){const{value:l,modifiers:n}=t,o=Nn(l)
o||xn.hide(e),e._ripple=e._ripple??{},e._ripple.enabled=o,e._ripple.centered=n.center,e._ripple.circle=n.circle
const r=V(l)?l:{}
r.class&&(e._ripple.class=r.class)
const i=r.keys??["Enter","Space"]
if(e._ripple.keyDownHandler=e=>function(e,t){!Pn&&t.includes(e.key)&&(Pn=!0,Cn(e))}(e,i),o&&!a){if(n.stop)return e.addEventListener("touchstart",En,{passive:!0}),void e.addEventListener("mousedown",En)
e.addEventListener("touchstart",Cn,{passive:!0}),e.addEventListener("touchend",In,{passive:!0}),e.addEventListener("touchmove",_n,{passive:!0}),e.addEventListener("touchcancel",In),e.addEventListener("mousedown",Cn),e.addEventListener("mouseup",In),e.addEventListener("mouseleave",In),e.addEventListener("keydown",e._ripple.keyDownHandler),e.addEventListener("keyup",An),e.addEventListener("blur",Rn),e.addEventListener("dragstart",In,{passive:!0})}else!o&&a&&Bn(e)}function Bn(e){e.removeEventListener("touchstart",En),e.removeEventListener("mousedown",En),e.removeEventListener("touchstart",Cn),e.removeEventListener("touchend",In),e.removeEventListener("touchmove",_n),e.removeEventListener("touchcancel",In),e.removeEventListener("mousedown",Cn),e.removeEventListener("mouseup",In),e.removeEventListener("mouseleave",In),e._ripple?.keyDownHandler&&e.removeEventListener("keydown",e._ripple.keyDownHandler),e.removeEventListener("keyup",An),e.removeEventListener("blur",Rn),e.removeEventListener("dragstart",In)}const Dn={mounted:function(e,t){Tn(e,t,!1)},unmounted:function(e){Bn(e),delete e._ripple},updated:function(e,t){if(t.value===t.oldValue)return
Tn(e,t,Nn(t.oldValue))}},Fn=vt({active:{type:Boolean,default:void 0},activeColor:String,baseColor:String,symbol:{type:null,default:Ul},flat:Boolean,icon:[Boolean,String,Function,Object],prependIcon:Dt,appendIcon:Dt,block:Boolean,readonly:Boolean,slim:Boolean,stacked:Boolean,spaced:String,ripple:{type:[Boolean,Object],default:!0},text:{type:[String,Number,Boolean],default:void 0},...wl(),...pt(),...Tl(),...ol(),...Sl(),...jl(),...cn(),...nn(),...mn(),...pl(),...yn(),...Xl(),...Pa({tag:"button"}),...ya(),...$l({variant:"elevated"})},"VBtn"),$n=wt()({name:"VBtn",props:Fn(),emits:{"group:selected":e=>!0},setup(e,a){let{attrs:l,slots:n}=a
const{themeClasses:o}=Ca(e),{borderClasses:r}=kl(e),{densityClasses:i}=Bl(e),{dimensionStyles:s}=rl(e),{elevationClasses:u}=xl(e),{loaderClasses:c}=dn(e),{locationStyles:d}=on(e),{positionClasses:v}=fn(e),{roundedClasses:p}=ml(e),{sizeClasses:m,sizeStyles:f}=Zl(e),g=Hl(e,e.symbol,!1),h=hn(e,l),y=t.computed(()=>void 0!==e.active?e.active:h.isRouterLink.value?h.isActive?.value:g?.isSelected.value),b=t.toRef(()=>y.value?e.activeColor??e.color:e.color),V=t.computed(()=>({color:g?.isSelected.value&&(!h.isLink.value||h.isActive?.value)||!g||h.isActive?.value?b.value??e.baseColor:e.baseColor,variant:e.variant})),{colorClasses:w,colorStyles:k,variantClasses:S}=Ml(V),x=t.computed(()=>g?.disabled.value||e.disabled),N=t.toRef(()=>"elevated"===e.variant&&!(e.disabled||e.flat||e.border)),C=t.computed(()=>{if(void 0!==e.value&&"symbol"!=typeof e.value)return Object(e.value)===e.value?JSON.stringify(e.value,null,0):e.value})
function E(e){x.value||h.isLink.value&&(e.metaKey||e.ctrlKey||e.shiftKey||0!==e.button||"_blank"===l.target)||(h.isRouterLink.value?h.navigate?.(e):g?.toggle())}return function(e,a){t.watch(()=>e.isActive?.value,l=>{e.isLink.value&&null!=l&&a&&t.nextTick(()=>{a(l)})},{immediate:!0})}(h,g?.select),Bt(()=>{const a=h.isLink.value?"a":e.tag,l=!(!e.prependIcon&&!n.prepend),b=!(!e.appendIcon&&!n.append),V=!(!e.icon||!0===e.icon)
return t.withDirectives(t.createVNode(a,t.mergeProps(h.linkProps,{type:"a"===a?void 0:"button",class:["v-btn",g?.selectedClass.value,{"v-btn--active":y.value,"v-btn--block":e.block,"v-btn--disabled":x.value,"v-btn--elevated":N.value,"v-btn--flat":e.flat,"v-btn--icon":!!e.icon,"v-btn--loading":e.loading,"v-btn--readonly":e.readonly,"v-btn--slim":e.slim,"v-btn--stacked":e.stacked},e.spaced?["v-btn--spaced",`v-btn--spaced-${e.spaced}`]:[],o.value,r.value,w.value,i.value,u.value,c.value,v.value,p.value,m.value,S.value,e.class],style:[k.value,s.value,d.value,f.value,e.style],"aria-busy":!!e.loading||void 0,disabled:x.value&&"a"!==a||void 0,tabindex:e.loading||e.readonly?-1:void 0,onClick:E,value:C.value}),{default:()=>[Fl(!0,"v-btn"),!e.icon&&l&&t.createElementVNode("span",{key:"prepend",class:"v-btn__prepend"},[n.prepend?t.createVNode(nl,{key:"prepend-defaults",disabled:!e.prependIcon,defaults:{VIcon:{icon:e.prependIcon}}},n.prepend):t.createVNode(Jl,{key:"prepend-icon",icon:e.prependIcon},null)]),t.createElementVNode("span",{class:"v-btn__content","data-no-activator":""},[!n.default&&V?t.createVNode(Jl,{key:"content-icon",icon:e.icon},null):t.createVNode(nl,{key:"content-defaults",disabled:!V,defaults:{VIcon:{icon:e.icon}}},{default:()=>[n.default?.()??t.toDisplayString(e.text)]})]),!e.icon&&b&&t.createElementVNode("span",{key:"append",class:"v-btn__append"},[n.append?t.createVNode(nl,{key:"append-defaults",disabled:!e.appendIcon,defaults:{VIcon:{icon:e.appendIcon}}},n.append):t.createVNode(Jl,{key:"append-icon",icon:e.appendIcon},null)]),!!e.loading&&t.createElementVNode("span",{key:"loader",class:"v-btn__loader"},[n.loader?.()??t.createVNode(an,{color:"boolean"==typeof e.loading?void 0:e.loading,indeterminate:!0,width:"2"},null)])]}),[[Dn,!x.value&&e.ripple,"",{center:!!e.icon}]])}),{group:g}}}),Mn=vt({...I(Fn({icon:"$menu",variant:"text"}),["spaced"])},"VAppBarNavIcon"),zn=wt()({name:"VAppBarNavIcon",props:Mn(),setup(e,a){let{slots:l}=a
return Bt(()=>t.createVNode($n,t.mergeProps(e,{class:["v-app-bar-nav-icon"]}),l)),{}}}),Ln=wt()({name:"VAppBarTitle",props:Aa(),setup(e,a){let{slots:l}=a
return Bt(()=>t.createVNode(Ra,t.mergeProps(e,{class:"v-app-bar-title"}),l)),{}}}),On=kt("v-alert-title"),jn=vt({iconSize:[Number,String],iconSizes:{type:Array,default:()=>[["x-small",10],["small",16],["default",24],["large",28],["x-large",32]]}},"iconSize")
function Hn(e,a){return{iconSize:t.computed(()=>{const t=new Map(e.iconSizes),l=e.iconSize??a()??"default"
return t.has(l)?t.get(l):l})}}const Wn=["success","info","warning","error"],Yn=vt({border:{type:[Boolean,String],validator:e=>"boolean"==typeof e||["top","end","bottom","start"].includes(e)},borderColor:String,closable:Boolean,closeIcon:{type:Dt,default:"$close"},closeLabel:{type:String,default:"$vuetify.close"},icon:{type:[Boolean,String,Function,Object],default:null},modelValue:{type:Boolean,default:!0},prominent:Boolean,title:String,text:String,type:{type:String,validator:e=>Wn.includes(e)},...pt(),...Tl(),...ol(),...Sl(),...jn(),...nn(),...mn(),...pl(),...Pa(),...ya(),...$l({variant:"flat"})},"VAlert"),Un=wt()({name:"VAlert",props:Yn(),emits:{"click:close":e=>!0,"update:modelValue":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const o=la(e,"modelValue"),r=t.toRef(()=>{if(!1!==e.icon)return e.type?e.icon??`$${e.type}`:e.icon}),{iconSize:i}=Hn(e,()=>e.prominent?44:void 0),{themeClasses:s}=Ca(e),{colorClasses:u,colorStyles:c,variantClasses:d}=Ml(()=>({color:e.color??e.type,variant:e.variant})),{densityClasses:v}=Bl(e),{dimensionStyles:p}=rl(e),{elevationClasses:m}=xl(e),{locationStyles:f}=on(e),{positionClasses:g}=fn(e),{roundedClasses:h}=ml(e),{textColorClasses:y,textColorStyles:b}=cl(()=>e.borderColor),{t:V}=ma(),w=t.toRef(()=>({"aria-label":V(e.closeLabel),onClick(e){o.value=!1,l("click:close",e)}}))
return()=>{const a=!(!n.prepend&&!r.value),l=!(!n.title&&!e.title),V=!(!n.close&&!e.closable),k={density:e.density,icon:r.value,size:e.iconSize||e.prominent?i.value:void 0}
return o.value&&t.createVNode(e.tag,{class:t.normalizeClass(["v-alert",e.border&&{"v-alert--border":!!e.border,[`v-alert--border-${!0===e.border?"start":e.border}`]:!0},{"v-alert--prominent":e.prominent},s.value,u.value,v.value,m.value,g.value,h.value,d.value,e.class]),style:t.normalizeStyle([c.value,p.value,f.value,e.style]),role:"alert"},{default:()=>[Fl(!1,"v-alert"),e.border&&t.createElementVNode("div",{key:"border",class:t.normalizeClass(["v-alert__border",y.value]),style:t.normalizeStyle(b.value)},null),a&&t.createElementVNode("div",{key:"prepend",class:"v-alert__prepend"},[n.prepend?t.createVNode(nl,{key:"prepend-defaults",disabled:!r.value,defaults:{VIcon:{...k}}},n.prepend):t.createVNode(Jl,t.mergeProps({key:"prepend-icon"},k),null)]),t.createElementVNode("div",{class:"v-alert__content"},[l&&t.createVNode(On,{key:"title"},{default:()=>[n.title?.()??e.title]}),n.text?.()??e.text,n.default?.()]),n.append&&t.createElementVNode("div",{key:"append",class:"v-alert__append"},[n.append()]),V&&t.createElementVNode("div",{key:"close",class:"v-alert__close"},[n.close?t.createVNode(nl,{key:"close-defaults",defaults:{VBtn:{icon:e.closeIcon,size:"x-small",variant:"text"}}},{default:()=>[n.close?.({props:w.value})]}):t.createVNode($n,t.mergeProps({key:"close-btn",icon:e.closeIcon,size:"x-small",variant:"text"},w.value),null)])]})}}}),Gn=vt({start:Boolean,end:Boolean,icon:Dt,image:String,text:String,...wl(),...pt(),...Tl(),...pl(),...Xl(),...Pa(),...ya(),...$l({variant:"flat"})},"VAvatar"),Kn=wt()({name:"VAvatar",props:Gn(),setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ca(e),{borderClasses:o}=kl(e),{colorClasses:r,colorStyles:i,variantClasses:s}=Ml(e),{densityClasses:u}=Bl(e),{roundedClasses:c}=ml(e),{sizeClasses:d,sizeStyles:v}=Zl(e)
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-avatar",{"v-avatar--start":e.start,"v-avatar--end":e.end},n.value,o.value,r.value,u.value,c.value,d.value,s.value,e.class]),style:t.normalizeStyle([i.value,v.value,e.style])},{default:()=>[l.default?t.createVNode(nl,{key:"content-defaults",defaults:{VImg:{cover:!0,src:e.image},VIcon:{icon:e.icon}}},{default:()=>[l.default()]}):e.image?t.createVNode(Vl,{key:"image",src:e.image,alt:"",cover:!0},null):e.icon?t.createVNode(Jl,{key:"icon",icon:e.icon},null):e.text,Fl(!1,"v-avatar")]})),{}}}),qn=vt({text:String,onClick:Z(),...pt(),...ya()},"VLabel"),Xn=wt()({name:"VLabel",props:qn(),setup(e,a){let{slots:l}=a
return Bt(()=>t.createElementVNode("label",{class:t.normalizeClass(["v-label",{"v-label--clickable":!!e.onClick},e.class]),style:t.normalizeStyle(e.style),onClick:e.onClick},[e.text,l.default?.()])),{}}}),Zn=Symbol.for("vuetify:selection-control-group"),Qn=vt({color:String,disabled:{type:Boolean,default:null},defaultsTarget:String,error:Boolean,id:String,inline:Boolean,falseIcon:Dt,trueIcon:Dt,ripple:{type:[Boolean,Object],default:!0},multiple:{type:Boolean,default:null},name:String,readonly:{type:Boolean,default:null},modelValue:null,type:String,valueComparator:{type:Function,default:St},...pt(),...Tl(),...ya()},"SelectionControlGroup"),Jn=vt({...Qn({defaultsTarget:"VSelectionControl"})},"VSelectionControlGroup"),eo=wt()({name:"VSelectionControlGroup",props:Jn(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=la(e,"modelValue"),o=t.useId(),r=t.toRef(()=>e.id||`v-selection-control-group-${o}`),i=t.toRef(()=>e.name||r.value),s=new Set
return t.provide(Zn,{modelValue:n,forceUpdate:()=>{s.forEach(e=>e())},onForceUpdate:e=>{s.add(e),t.onScopeDispose(()=>{s.delete(e)})}}),yt({[e.defaultsTarget]:{color:t.toRef(()=>e.color),disabled:t.toRef(()=>e.disabled),density:t.toRef(()=>e.density),error:t.toRef(()=>e.error),inline:t.toRef(()=>e.inline),modelValue:n,multiple:t.toRef(()=>!!e.multiple||null==e.multiple&&Array.isArray(n.value)),name:i,falseIcon:t.toRef(()=>e.falseIcon),trueIcon:t.toRef(()=>e.trueIcon),readonly:t.toRef(()=>e.readonly),ripple:t.toRef(()=>e.ripple),type:t.toRef(()=>e.type),valueComparator:t.toRef(()=>e.valueComparator)}}),Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-selection-control-group",{"v-selection-control-group--inline":e.inline},e.class]),style:t.normalizeStyle(e.style),role:"radio"===e.type?"radiogroup":void 0},[l.default?.()])),{}}}),to=vt({label:String,baseColor:String,trueValue:null,falseValue:null,value:null,...pt(),...Qn()},"VSelectionControl")
const ao=wt()({name:"VSelectionControl",directives:{vRipple:Dn},inheritAttrs:!1,props:to(),emits:{"update:modelValue":e=>!0},setup(e,a){let{attrs:l,slots:n}=a
const{group:o,densityClasses:r,icon:i,model:s,textColorClasses:u,textColorStyles:c,backgroundColorClasses:d,backgroundColorStyles:v,trueValue:p}=function(e){const a=t.inject(Zn,void 0),{densityClasses:l}=Bl(e),n=la(e,"modelValue"),o=t.computed(()=>void 0!==e.trueValue?e.trueValue:void 0===e.value||e.value),r=t.computed(()=>void 0!==e.falseValue&&e.falseValue),i=t.computed(()=>!!e.multiple||null==e.multiple&&Array.isArray(n.value)),s=t.computed({get(){const t=a?a.modelValue.value:n.value
return i.value?B(t).some(t=>e.valueComparator(t,o.value)):e.valueComparator(t,o.value)},set(t){if(e.readonly)return
const l=t?o.value:r.value
let s=l
i.value&&(s=t?[...B(n.value),l]:B(n.value).filter(t=>!e.valueComparator(t,o.value))),a?a.modelValue.value=s:n.value=s}}),{textColorClasses:u,textColorStyles:c}=cl(()=>{if(!e.error&&!e.disabled)return s.value?e.color:e.baseColor}),{backgroundColorClasses:d,backgroundColorStyles:v}=dl(()=>!s.value||e.error||e.disabled?e.baseColor:e.color),p=t.computed(()=>s.value?e.trueIcon:e.falseIcon)
return{group:a,densityClasses:l,trueValue:o,falseValue:r,model:s,textColorClasses:u,textColorStyles:c,backgroundColorClasses:d,backgroundColorStyles:v,icon:p}}(e),m=t.useId(),f=t.shallowRef(!1),g=t.shallowRef(!1),h=t.ref(),y=t.toRef(()=>e.id||`input-${m}`),b=t.toRef(()=>!e.disabled&&!e.readonly)
function V(e){b.value&&(f.value=!0,!1!==oe(e.target,":focus-visible")&&(g.value=!0))}function w(){f.value=!1,g.value=!1}function k(e){e.stopPropagation()}function S(a){b.value?(e.readonly&&o&&t.nextTick(()=>o.forceUpdate()),s.value=a.target.checked):h.value&&(h.value.checked=s.value)}return o?.onForceUpdate(()=>{h.value&&(h.value.checked=s.value)}),Bt(()=>{const a=n.label?n.label({label:e.label,props:{for:y.value}}):e.label,[o,m]=T(l),b=t.createElementVNode("input",t.mergeProps({ref:h,checked:s.value,disabled:!!e.disabled,id:y.value,onBlur:w,onFocus:V,onInput:S,"aria-disabled":!!e.disabled,"aria-label":e.label,type:e.type,value:p.value,name:e.name,"aria-checked":"checkbox"===e.type?s.value:void 0},m),null)
return t.createElementVNode("div",t.mergeProps({class:["v-selection-control",{"v-selection-control--dirty":s.value,"v-selection-control--disabled":e.disabled,"v-selection-control--error":e.error,"v-selection-control--focused":f.value,"v-selection-control--focus-visible":g.value,"v-selection-control--inline":e.inline},r.value,e.class]},o,{style:e.style}),[t.createElementVNode("div",{class:t.normalizeClass(["v-selection-control__wrapper",u.value]),style:t.normalizeStyle(c.value)},[n.default?.({backgroundColorClasses:d,backgroundColorStyles:v}),t.withDirectives(t.createElementVNode("div",{class:t.normalizeClass(["v-selection-control__input"])},[n.input?.({model:s,textColorClasses:u,textColorStyles:c,backgroundColorClasses:d,backgroundColorStyles:v,inputNode:b,icon:i.value,props:{onFocus:V,onBlur:w,id:y.value}})??t.createElementVNode(t.Fragment,null,[i.value&&t.createVNode(Jl,{key:"icon",icon:i.value},null),b])]),[[Dn,!e.disabled&&!e.readonly&&e.ripple,null,{center:!0,circle:!0}]])]),a&&t.createVNode(Xn,{for:y.value,onClick:k},{default:()=>[a]})])}),{isFocused:f,input:h}}}),lo=vt({indeterminate:Boolean,indeterminateIcon:{type:Dt,default:"$checkboxIndeterminate"},...to({falseIcon:"$checkboxOff",trueIcon:"$checkboxOn"})},"VCheckboxBtn"),no=wt()({name:"VCheckboxBtn",props:lo(),emits:{"update:modelValue":e=>!0,"update:indeterminate":e=>!0},setup(e,a){let{slots:l}=a
const n=la(e,"indeterminate"),o=la(e,"modelValue")
function r(e){n.value&&(n.value=!1)}const i=t.toRef(()=>n.value?e.indeterminateIcon:e.falseIcon),s=t.toRef(()=>n.value?e.indeterminateIcon:e.trueIcon)
return Bt(()=>{const a=I(ao.filterProps(e),["modelValue"])
return t.createVNode(ao,t.mergeProps(a,{modelValue:o.value,"onUpdate:modelValue":[e=>o.value=e,r],class:["v-checkbox-btn",e.class],style:e.style,type:"checkbox",falseIcon:i.value,trueIcon:s.value,"aria-checked":n.value?"mixed":void 0}),l)}),{}}})
function oo(e){const{t:a}=ma()
return{InputIcon:function(l){let{name:n,color:o,...r}=l
const i={prepend:"prependAction",prependInner:"prependAction",append:"appendAction",appendInner:"appendAction",clear:"clear"}[n],s=e[`onClick:${n}`],u=s&&i?a(`$vuetify.input.${i}`,e.label??""):void 0
return t.createVNode(Jl,t.mergeProps({icon:e[`${n}Icon`],"aria-label":u,onClick:s,onKeydown:function(e){"Enter"!==e.key&&" "!==e.key||(e.preventDefault(),e.stopPropagation(),J(s,new PointerEvent("click",e)))},color:o},r),null)}}}const ro=vt({active:Boolean,color:String,messages:{type:[Array,String],default:()=>[]},...pt(),...fl({transition:{component:Ja,leaveAbsolute:!0,group:!0}})},"VMessages"),io=wt()({name:"VMessages",props:ro(),setup(e,a){let{slots:l}=a
const n=t.computed(()=>B(e.messages)),{textColorClasses:o,textColorStyles:r}=cl(()=>e.color)
return Bt(()=>t.createVNode(gl,{transition:e.transition,tag:"div",class:t.normalizeClass(["v-messages",o.value,e.class]),style:t.normalizeStyle([r.value,e.style])},{default:()=>[e.active&&n.value.map((e,a)=>t.createElementVNode("div",{class:"v-messages__message",key:`${a}-${n.value}`},[l.message?l.message({message:e}):e]))]})),{}}}),so=vt({focused:Boolean,"onUpdate:focused":Z()},"focus")
function uo(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:ft()
const l=la(e,"focused")
return{focusClasses:t.toRef(()=>({[`${a}--focused`]:l.value})),isFocused:l,focus:function(){l.value=!0},blur:function(){l.value=!1}}}const co=Symbol.for("vuetify:form"),vo=vt({disabled:Boolean,fastFail:Boolean,readonly:Boolean,modelValue:{type:Boolean,default:null},validateOn:{type:String,default:"input"}},"form")
function po(e){const a=t.inject(co,null)
return{...a,isReadonly:t.computed(()=>!!(e?.readonly??a?.isReadonly.value)),isDisabled:t.computed(()=>!!(e?.disabled??a?.isDisabled.value))}}const mo=Symbol.for("vuetify:rules")
const fo=vt({disabled:{type:Boolean,default:null},error:Boolean,errorMessages:{type:[Array,String],default:()=>[]},maxErrors:{type:[Number,String],default:1},name:String,label:String,readonly:{type:Boolean,default:null},rules:{type:Array,default:()=>[]},modelValue:null,validateOn:String,validationValue:null,...so()},"validation")
function go(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:ft(),l=arguments.length>2&&void 0!==arguments[2]?arguments[2]:t.useId()
const n=la(e,"modelValue"),o=t.computed(()=>void 0===e.validationValue?n.value:e.validationValue),r=po(e),i=function(e){const a=t.inject(mo,null)
if(!e){if(!a)throw new Error("Could not find Vuetify rules injection")
return a.aliases}return a?.resolve(e)??t.toRef(e)}(()=>e.rules),s=t.ref([]),u=t.shallowRef(!0),c=t.computed(()=>!(!B(""===n.value?null:n.value).length&&!B(""===o.value?null:o.value).length)),d=t.computed(()=>e.errorMessages?.length?B(e.errorMessages).concat(s.value).slice(0,Math.max(0,Number(e.maxErrors))):s.value),v=t.computed(()=>{let t=(e.validateOn??r.validateOn?.value)||"input"
"lazy"===t&&(t="input lazy"),"eager"===t&&(t="input eager")
const a=new Set(t?.split(" ")??[])
return{input:a.has("input"),blur:a.has("blur")||a.has("input")||a.has("invalid-input"),invalidInput:a.has("invalid-input"),lazy:a.has("lazy"),eager:a.has("eager")}}),p=t.computed(()=>!e.error&&!e.errorMessages?.length&&(!e.rules.length||(u.value?!s.value.length&&!v.value.lazy||null:!s.value.length))),m=t.shallowRef(!1),f=t.computed(()=>({[`${a}--error`]:!1===p.value,[`${a}--dirty`]:c.value,[`${a}--disabled`]:r.isDisabled.value,[`${a}--readonly`]:r.isReadonly.value})),g=mt("validation"),h=t.computed(()=>e.name??t.unref(l))
async function y(){n.value=null,await t.nextTick(),await b()}async function b(){u.value=!0,v.value.lazy?s.value=[]:await V(!v.value.eager)}async function V(){let t=arguments.length>0&&void 0!==arguments[0]&&arguments[0]
const a=[]
m.value=!0
for(const t of i.value){if(a.length>=Number(e.maxErrors??1))break
const l="function"==typeof t?t:()=>t,n=await l(o.value)
!0!==n&&(!1===n||"string"==typeof n?a.push(n||""):console.warn(`${n} is not a valid value. Rule functions must return boolean true or a string.`))}return s.value=a,m.value=!1,u.value=t,s.value}return t.onBeforeMount(()=>{r.register?.({id:h.value,vm:g,validate:V,reset:y,resetValidation:b})}),t.onBeforeUnmount(()=>{r.unregister?.(h.value)}),t.onMounted(async()=>{v.value.lazy||await V(!v.value.eager),r.update?.(h.value,p.value,d.value)}),aa(()=>v.value.input||v.value.invalidInput&&!1===p.value,()=>{t.watch(o,()=>{if(null!=o.value)V()
else if(e.focused){const a=t.watch(()=>e.focused,e=>{e||V(),a()})}})}),aa(()=>v.value.blur,()=>{t.watch(()=>e.focused,e=>{e||V()})}),t.watch([p,d],()=>{r.update?.(h.value,p.value,d.value)}),{errorMessages:d,isDirty:c,isDisabled:r.isDisabled,isReadonly:r.isReadonly,isPristine:u,isValid:p,isValidating:m,reset:y,resetValidation:b,validate:V,validationClasses:f}}const ho=vt({id:String,appendIcon:Dt,baseColor:String,centerAffix:{type:Boolean,default:!0},color:String,glow:Boolean,iconColor:[Boolean,String],prependIcon:Dt,hideDetails:[Boolean,String],hideSpinButtons:Boolean,hint:String,persistentHint:Boolean,messages:{type:[Array,String],default:()=>[]},direction:{type:String,default:"horizontal",validator:e=>["horizontal","vertical"].includes(e)},"onClick:prepend":Z(),"onClick:append":Z(),...pt(),...Tl(),...C(ol(),["maxWidth","minWidth","width"]),...ya(),...fo()},"VInput"),yo=wt()({name:"VInput",props:{...ho()},emits:{"update:modelValue":e=>!0},setup(e,a){let{attrs:l,slots:n,emit:o}=a
const{densityClasses:r}=Bl(e),{dimensionStyles:i}=rl(e),{themeClasses:s}=Ca(e),{rtlClasses:u}=ga(),{InputIcon:c}=oo(e),d=t.useId(),v=t.computed(()=>e.id||`input-${d}`),{errorMessages:p,isDirty:m,isDisabled:f,isReadonly:g,isPristine:h,isValid:y,isValidating:b,reset:V,resetValidation:w,validate:k,validationClasses:S}=go(e,"v-input",v),x=t.computed(()=>e.errorMessages?.length||!h.value&&p.value.length?p.value:e.hint&&(e.persistentHint||e.focused)?e.hint:e.messages),N=t.toRef(()=>x.value.length>0),C=t.toRef(()=>!e.hideDetails||"auto"===e.hideDetails&&(N.value||!!n.details)),E=t.computed(()=>C.value?`${v.value}-messages`:void 0),I=t.computed(()=>({id:v,messagesId:E,isDirty:m,isDisabled:f,isReadonly:g,isPristine:h,isValid:y,isValidating:b,hasDetails:C,reset:V,resetValidation:w,validate:k})),_=t.toRef(()=>e.error||e.disabled?void 0:e.focused?e.color:e.baseColor),P=t.toRef(()=>{if(e.iconColor)return!0===e.iconColor?_.value:e.iconColor})
return Bt(()=>{const a=!(!n.prepend&&!e.prependIcon),l=!(!n.append&&!e.appendIcon)
return t.createElementVNode("div",{class:t.normalizeClass(["v-input",`v-input--${e.direction}`,{"v-input--center-affix":e.centerAffix,"v-input--focused":e.focused,"v-input--glow":e.glow,"v-input--hide-spin-buttons":e.hideSpinButtons},r.value,s.value,u.value,S.value,e.class]),style:t.normalizeStyle([i.value,e.style])},[a&&t.createElementVNode("div",{key:"prepend",class:"v-input__prepend"},[n.prepend?n.prepend(I.value):e.prependIcon&&t.createVNode(c,{key:"prepend-icon",name:"prepend",color:P.value},null)]),n.default&&t.createElementVNode("div",{class:"v-input__control"},[n.default?.(I.value)]),l&&t.createElementVNode("div",{key:"append",class:"v-input__append"},[n.append?n.append(I.value):e.appendIcon&&t.createVNode(c,{key:"append-icon",name:"append",color:P.value},null)]),C.value&&t.createElementVNode("div",{id:E.value,class:"v-input__details",role:"alert","aria-live":"polite"},[t.createVNode(io,{active:N.value,messages:x.value},{message:n.message}),n.details?.(I.value)])])}),{reset:V,resetValidation:w,validate:k,isValid:y,errorMessages:p}}}),bo=Symbol("Forwarded refs")
function Vo(e,t){let a=e
for(;a;){const e=Reflect.getOwnPropertyDescriptor(a,t)
if(e)return e
a=Object.getPrototypeOf(a)}}function wo(e){for(var t=arguments.length,a=new Array(t>1?t-1:0),l=1;l<t;l++)a[l-1]=arguments[l]
return e[bo]=a,new Proxy(e,{get(e,t){if(Reflect.has(e,t))return Reflect.get(e,t)
if("symbol"!=typeof t&&!t.startsWith("$")&&!t.startsWith("__"))for(const e of a)if(e.value&&Reflect.has(e.value,t)){const a=Reflect.get(e.value,t)
return"function"==typeof a?a.bind(e.value):a}},has(e,t){if(Reflect.has(e,t))return!0
if("symbol"==typeof t||t.startsWith("$")||t.startsWith("__"))return!1
for(const e of a)if(e.value&&Reflect.has(e.value,t))return!0
return!1},set(e,t,l){if(Reflect.has(e,t))return Reflect.set(e,t,l)
if("symbol"==typeof t||t.startsWith("$")||t.startsWith("__"))return!1
for(const e of a)if(e.value&&Reflect.has(e.value,t))return Reflect.set(e.value,t,l)
return!1},getOwnPropertyDescriptor(e,t){const l=Reflect.getOwnPropertyDescriptor(e,t)
if(l)return l
if("symbol"!=typeof t&&!t.startsWith("$")&&!t.startsWith("__")){for(const e of a){if(!e.value)continue
const a=Vo(e.value,t)??("_"in e.value?Vo(e.value._?.setupState,t):void 0)
if(a)return a}for(const e of a){const a=e.value&&e.value[bo]
if(!a)continue
const l=a.slice()
for(;l.length;){const e=l.shift(),a=Vo(e.value,t)
if(a)return a
const n=e.value&&e.value[bo]
n&&l.push(...n)}}}}})}const ko=vt({...I(ho(),["direction"]),...I(lo(),["inline"])},"VCheckbox"),So=wt()({name:"VCheckbox",inheritAttrs:!1,props:ko(),emits:{"update:modelValue":e=>!0,"update:focused":e=>!0},setup(e,a){let{attrs:l,slots:n}=a
const o=la(e,"modelValue"),{isFocused:r,focus:i,blur:s}=uo(e),u=t.ref(),c=t.useId()
return Bt(()=>{const[a,d]=T(l),v=yo.filterProps(e),p=no.filterProps(e)
return t.createVNode(yo,t.mergeProps({ref:u,class:["v-checkbox",e.class]},a,v,{modelValue:o.value,"onUpdate:modelValue":e=>o.value=e,id:e.id||`checkbox-${c}`,focused:r.value,style:e.style}),{...n,default:e=>{let{id:a,messagesId:l,isDisabled:r,isReadonly:u,isValid:c}=e
return t.createVNode(no,t.mergeProps(p,{id:a.value,"aria-describedby":l.value,disabled:r.value,readonly:u.value},d,{error:!1===c.value,modelValue:o.value,"onUpdate:modelValue":e=>o.value=e,onFocus:i,onBlur:s}),n)}})}),wo({},u)}}),xo=["sm","md","lg","xl","xxl"],No=Symbol.for("vuetify:display"),Co={mobileBreakpoint:"lg",thresholds:{xs:0,sm:600,md:960,lg:1280,xl:1920,xxl:2560}}
function Eo(e){return o&&!e?window.innerWidth:"object"==typeof e&&e.clientWidth||0}function Io(e){return o&&!e?window.innerHeight:"object"==typeof e&&e.clientHeight||0}function _o(e){const t=o&&!e?window.navigator.userAgent:"ssr"
function a(e){return Boolean(t.match(e))}return{android:a(/android/i),ios:a(/iphone|ipad|ipod/i),cordova:a(/cordova/i),electron:a(/electron/i),chrome:a(/chrome/i),edge:a(/edge/i),firefox:a(/firefox/i),opera:a(/opera/i),win:a(/win/i),mac:a(/mac/i),linux:a(/linux/i),touch:i,ssr:"ssr"===t}}function Po(e,a){const{thresholds:l,mobileBreakpoint:n}=function(){return O(Co,arguments.length>0&&void 0!==arguments[0]?arguments[0]:Co)}(e),r=t.shallowRef(Io(a)),i=t.shallowRef(_o(a)),s=t.reactive({}),u=t.shallowRef(Eo(a))
function c(){r.value=Io(),u.value=Eo()}return t.watchEffect(()=>{const e=u.value<l.sm,t=u.value<l.md&&!e,a=u.value<l.lg&&!(t||e),o=u.value<l.xl&&!(a||t||e),c=u.value<l.xxl&&!(o||a||t||e),d=u.value>=l.xxl,v=e?"xs":t?"sm":a?"md":o?"lg":c?"xl":"xxl",p="number"==typeof n?n:l[n],m=u.value<p
s.xs=e,s.sm=t,s.md=a,s.lg=o,s.xl=c,s.xxl=d,s.smAndUp=!e,s.mdAndUp=!(e||t),s.lgAndUp=!(e||t||a),s.xlAndUp=!(e||t||a||o),s.smAndDown=!(a||o||c||d),s.mdAndDown=!(o||c||d),s.lgAndDown=!(c||d),s.xlAndDown=!d,s.name=v,s.height=r.value,s.width=u.value,s.mobile=m,s.mobileBreakpoint=n,s.platform=i.value,s.thresholds=l}),o&&(window.addEventListener("resize",c,{passive:!0}),t.onScopeDispose(()=>{window.removeEventListener("resize",c)},!0)),{...t.toRefs(s),update:function(){c(),i.value=_o()},ssr:!!a}}const Ao=vt({mobile:{type:Boolean,default:!1},mobileBreakpoint:[Number,String]},"display")
function Ro(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{mobile:null},a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:ft()
const l=t.inject(No)
if(!l)throw new Error("Could not find Vuetify display injection")
const n=t.computed(()=>!!e.mobile||("number"==typeof e.mobileBreakpoint?l.width.value<e.mobileBreakpoint:e.mobileBreakpoint?l.width.value<l.thresholds.value[e.mobileBreakpoint]:null===e.mobile&&l.mobile.value)),o=t.toRef(()=>a?{[`${a}--mobile`]:n.value}:{})
return{...l,displayClasses:o,mobile:n}}const To=Symbol.for("vuetify:goto")
function Bo(){return{container:void 0,duration:300,layout:!1,offset:0,easing:"easeInOutCubic",patterns:It}}function Do(e){return"string"==typeof e?document.querySelector(e):k(e)}function Fo(e,t,a){if("number"==typeof e)return t&&a?-e:e
let l=Do(e),n=0
for(;l;)n+=t?l.offsetLeft:l.offsetTop,l=l.offsetParent
return n}async function $o(e,t,l,n){const o=l?"scrollLeft":"scrollTop",r=O(n?.options??Bo(),t),i=n?.rtl.value,s=("number"==typeof e?e:Do(e))??0,u="parent"===r.container&&s instanceof HTMLElement?s.parentElement:Do(r.container)??(document.scrollingElement||document.body)
const d=c()?r.patterns.instant:"function"==typeof r.easing?r.easing:r.patterns[r.easing]
if(!d)throw new TypeError(`Easing function "${r.easing}" not found.`)
let v
if("number"==typeof s)v=Fo(s,l,i)
else if(v=Fo(s,l,i)-Fo(u,l,i),r.layout){const e=window.getComputedStyle(s).getPropertyValue("--v-layout-top")
e&&(v-=parseInt(e,10))}v+=r.offset,v=function(e,t,a,l){const{scrollWidth:n,scrollHeight:o}=e,[r,i]=e===document.scrollingElement?[window.innerWidth,window.innerHeight]:[e.offsetWidth,e.offsetHeight]
let s,u
l?a?(s=-(n-r),u=0):(s=0,u=n-r):(s=0,u=o+-i)
return F(t,s,u)}(u,v,!!i,!!l)
const p=u[o]??0
if(v===p)return Promise.resolve(v)
const m=performance.now()
return new Promise(e=>requestAnimationFrame(function t(l){const n=(l-m)/r.duration,i=Math.floor(p+(v-p)*d(F(n,0,1)))
return u[o]=i,n>=1&&Math.abs(i-u[o])<10?e(v):n>2?(a("Scroll target is not reachable"),e(u[o])):void requestAnimationFrame(t)}))}function Mo(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}
const a=t.inject(To),{isRtl:l}=ga()
if(!a)throw new Error("[Vuetify] Could not find injected goto instance")
const n={...a,rtl:t.toRef(()=>a.rtl.value||l.value)}
async function o(t,a){return $o(t,O(e,a),!1,n)}return o.horizontal=async(t,a)=>$o(t,O(e,a),!0,n),o}function zo(e,t){const a=e?"scrollWidth":"scrollHeight"
return t?.[a]||0}function Lo(e,t,a){if(!a)return 0
const{scrollLeft:l,offsetWidth:n,scrollWidth:o}=a
return e?t?o-n+l:l:a.scrollTop}function Oo(e,t){const a=e?"offsetWidth":"offsetHeight"
return t?.[a]||0}function jo(e,t){const a=e?"offsetLeft":"offsetTop"
return t?.[a]||0}const Ho=Symbol.for("vuetify:v-slide-group"),Wo=vt({centerActive:Boolean,scrollToActive:{type:Boolean,default:!0},contentClass:null,direction:{type:String,default:"horizontal"},symbol:{type:null,default:Ho},nextIcon:{type:Dt,default:"$next"},prevIcon:{type:Dt,default:"$prev"},showArrows:{type:[Boolean,String],validator:e=>"boolean"==typeof e||["always","desktop","mobile","never"].includes(e)},...pt(),...Ao({mobile:null}),...Pa(),...Ol({selectedClass:"v-slide-group-item--active"})},"VSlideGroup"),Yo=wt()({name:"VSlideGroup",props:Wo(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const{isRtl:n}=ga(),{displayClasses:r,mobile:i}=Ro(e),s=Wl(e,e.symbol),u=t.shallowRef(!1),c=t.shallowRef(0),d=t.shallowRef(0),v=t.shallowRef(0),p=t.computed(()=>"horizontal"===e.direction),{resizeRef:m,contentRect:f}=Kt(),{resizeRef:g,contentRect:h}=Kt(),y=Mo(),b=t.computed(()=>({container:m.el,duration:200,easing:"easeOutQuart"})),V=t.computed(()=>s.selected.value.length?s.items.value.findIndex(e=>e.id===s.selected.value[0]):-1),w=t.computed(()=>s.selected.value.length?s.items.value.findIndex(e=>e.id===s.selected.value[s.selected.value.length-1]):-1)
if(o){let a=-1
t.watch(()=>[s.selected.value,f.value,h.value,p.value],()=>{cancelAnimationFrame(a),a=requestAnimationFrame(()=>{if(f.value&&h.value){const e=p.value?"width":"height"
d.value=f.value[e],v.value=h.value[e],u.value=d.value+1<v.value}if(e.scrollToActive&&V.value>=0&&g.el){S(g.el.children[w.value],e.centerActive)}})})}const k=t.shallowRef(!1)
function S(e,t){let a=0
a=t?function(e){let{selectedElement:t,containerElement:a,isHorizontal:l}=e
const n=Oo(l,a)
return jo(l,t)-n/2+Oo(l,t)/2}({containerElement:m.el,isHorizontal:p.value,selectedElement:e}):function(e){let{selectedElement:t,containerElement:a,isRtl:l,isHorizontal:n}=e
const o=Oo(n,a),r=Lo(n,l,a),i=Oo(n,t),s=jo(n,t),u=.4*i
return r>s?s-u:r+o<s+i?s-o+i+u:r}({containerElement:m.el,isHorizontal:p.value,isRtl:n.value,selectedElement:e}),x(a)}function x(e){if(!o||!m.el)return
const t=Oo(p.value,m.el),a=Lo(p.value,n.value,m.el)
if(!(zo(p.value,m.el)<=t||Math.abs(e-a)<16)){if(p.value&&n.value&&m.el){const{scrollWidth:t,offsetWidth:a}=m.el
e=t-a-e}p.value?y.horizontal(e,b.value):y(e,b.value)}}function N(e){const{scrollTop:t,scrollLeft:a}=e.target
c.value=p.value?a:t}function C(e){if(k.value=!0,u.value&&g.el)for(const t of e.composedPath())for(const e of g.el.children)if(e===t)return void S(e)}function E(e){k.value=!1}let I=!1
function _(e){I||k.value||e.relatedTarget&&g.el?.contains(e.relatedTarget)||T(),I=!1}function P(){I=!0}function A(e){function t(t){e.preventDefault(),T(t)}g.el&&(p.value?"ArrowRight"===e.key?t(n.value?"prev":"next"):"ArrowLeft"===e.key&&t(n.value?"next":"prev"):"ArrowDown"===e.key?t("next"):"ArrowUp"===e.key&&t("prev"),"Home"===e.key?t("first"):"End"===e.key&&t("last"))}function R(e,t){if(!e)return
let a=e
do{a=a?.["next"===t?"nextElementSibling":"previousElementSibling"]}while(a?.hasAttribute("disabled"))
return a}function T(e){if(!g.el)return
let t
if(e)if("next"===e){if(t=R(g.el.querySelector(":focus"),e),!t)return T("first")}else if("prev"===e){if(t=R(g.el.querySelector(":focus"),e),!t)return T("last")}else"first"===e?(t=g.el.firstElementChild,t?.hasAttribute("disabled")&&(t=R(t,"next"))):"last"===e&&(t=g.el.lastElementChild,t?.hasAttribute("disabled")&&(t=R(t,"prev")))
else{t=ee(g.el)[0]}t&&t.focus({preventScroll:!0})}function B(e){const t=p.value&&n.value?-1:1,a=("prev"===e?-t:t)*d.value
let l=c.value+a
if(p.value&&n.value&&m.el){const{scrollWidth:e,offsetWidth:t}=m.el
l+=e-t}x(l)}const D=t.computed(()=>({next:s.next,prev:s.prev,select:s.select,isSelected:s.isSelected})),F=t.computed(()=>u.value||Math.abs(c.value)>0),$=t.computed(()=>{switch(e.showArrows){case"never":return!1
case"always":return!0
case"desktop":return!i.value
case!0:return F.value
case"mobile":return i.value||F.value
default:return!i.value&&F.value}}),M=t.computed(()=>Math.abs(c.value)>1),z=t.computed(()=>{if(!m.value||!F.value)return!1
const e=zo(p.value,m.el),t=function(e,t){const a=e?"clientWidth":"clientHeight"
return t?.[a]||0}(p.value,m.el)
return e-t-Math.abs(c.value)>1})
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-slide-group",{"v-slide-group--vertical":!p.value,"v-slide-group--has-affixes":$.value,"v-slide-group--is-overflowing":u.value},r.value,e.class]),style:t.normalizeStyle(e.style),tabindex:k.value||s.selected.value.length?-1:0,onFocus:_},{default:()=>[$.value&&t.createElementVNode("div",{key:"prev",class:t.normalizeClass(["v-slide-group__prev",{"v-slide-group__prev--disabled":!M.value}]),onMousedown:P,onClick:()=>M.value&&B("prev")},[l.prev?.(D.value)??t.createVNode(Ya,null,{default:()=>[t.createVNode(Jl,{icon:n.value?e.nextIcon:e.prevIcon},null)]})]),t.createElementVNode("div",{key:"container",ref:m,class:t.normalizeClass(["v-slide-group__container",e.contentClass]),onScroll:N},[t.createElementVNode("div",{ref:g,class:"v-slide-group__content",onFocusin:C,onFocusout:E,onKeydown:A},[l.default?.(D.value)])]),$.value&&t.createElementVNode("div",{key:"next",class:t.normalizeClass(["v-slide-group__next",{"v-slide-group__next--disabled":!z.value}]),onMousedown:P,onClick:()=>z.value&&B("next")},[l.next?.(D.value)??t.createVNode(Ya,null,{default:()=>[t.createVNode(Jl,{icon:n.value?e.prevIcon:e.nextIcon},null)]})])]})),{selected:s.selected,scrollTo:B,scrollOffset:c,focus:T,hasPrev:M,hasNext:z}}}),Uo=Symbol.for("vuetify:v-chip-group"),Go=vt({baseColor:String,column:Boolean,filter:Boolean,valueComparator:{type:Function,default:St},...Wo({scrollToActive:!1}),...pt(),...Ol({selectedClass:"v-chip--selected"}),...Pa(),...ya(),...$l({variant:"tonal"})},"VChipGroup"),Ko=wt()({name:"VChipGroup",props:Go(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ca(e),{isSelected:o,select:r,next:i,prev:s,selected:u}=Wl(e,Uo)
return yt({VChip:{baseColor:t.toRef(()=>e.baseColor),color:t.toRef(()=>e.color),disabled:t.toRef(()=>e.disabled),filter:t.toRef(()=>e.filter),variant:t.toRef(()=>e.variant)}}),Bt(()=>{const a=Yo.filterProps(e)
return t.createVNode(Yo,t.mergeProps(a,{class:["v-chip-group",{"v-chip-group--column":e.column},n.value,e.class],style:e.style}),{default:()=>[l.default?.({isSelected:o,select:r,next:i,prev:s,selected:u.value})]})}),{}}}),qo=vt({activeClass:String,appendAvatar:String,appendIcon:Dt,baseColor:String,closable:Boolean,closeIcon:{type:Dt,default:"$delete"},closeLabel:{type:String,default:"$vuetify.close"},draggable:Boolean,filter:Boolean,filterIcon:{type:Dt,default:"$complete"},label:Boolean,link:{type:Boolean,default:void 0},pill:Boolean,prependAvatar:String,prependIcon:Dt,ripple:{type:[Boolean,Object],default:!0},text:{type:[String,Number,Boolean],default:void 0},modelValue:{type:Boolean,default:!0},onClick:Z(),onClickOnce:Z(),...wl(),...pt(),...Tl(),...Sl(),...jl(),...pl(),...yn(),...Xl(),...Pa({tag:"span"}),...ya(),...$l({variant:"tonal"})},"VChip"),Xo=wt()({name:"VChip",directives:{vRipple:Dn},props:qo(),emits:{"click:close":e=>!0,"update:modelValue":e=>!0,"group:selected":e=>!0,click:e=>!0},setup(e,a){let{attrs:l,emit:n,slots:o}=a
const{t:r}=ma(),{borderClasses:i}=kl(e),{densityClasses:s}=Bl(e),{elevationClasses:u}=xl(e),{roundedClasses:c}=ml(e),{sizeClasses:d}=Zl(e),{themeClasses:v}=Ca(e),p=la(e,"modelValue"),m=Hl(e,Uo,!1),f=Hl(e,Ho,!1),g=hn(e,l),h=t.toRef(()=>!1!==e.link&&g.isLink.value),y=t.computed(()=>!e.disabled&&!1!==e.link&&(!!m||e.link||g.isClickable.value)),b=t.toRef(()=>({"aria-label":r(e.closeLabel),disabled:e.disabled,onClick(e){e.preventDefault(),e.stopPropagation(),p.value=!1,n("click:close",e)}}))
t.watch(p,e=>{e?(m?.register(),f?.register()):(m?.unregister(),f?.unregister())})
const{colorClasses:V,colorStyles:w,variantClasses:k}=Ml(()=>({color:!m||m.isSelected.value?e.color??e.baseColor:e.baseColor,variant:e.variant}))
function S(e){n("click",e),y.value&&(g.navigate?.(e),m?.toggle())}function x(e){"Enter"!==e.key&&" "!==e.key||(e.preventDefault(),S(e))}return()=>{const a=g.isLink.value?"a":e.tag,l=!(!e.appendIcon&&!e.appendAvatar),n=!(!l&&!o.append),r=!(!o.close&&!e.closable),f=!(!o.filter&&!e.filter)&&m,N=!(!e.prependIcon&&!e.prependAvatar),C=!(!N&&!o.prepend)
return p.value&&t.withDirectives(t.createVNode(a,t.mergeProps(g.linkProps,{class:["v-chip",{"v-chip--disabled":e.disabled,"v-chip--label":e.label,"v-chip--link":y.value,"v-chip--filter":f,"v-chip--pill":e.pill,[`${e.activeClass}`]:e.activeClass&&g.isActive?.value},v.value,i.value,V.value,s.value,u.value,c.value,d.value,k.value,m?.selectedClass.value,e.class],style:[w.value,e.style],disabled:e.disabled||void 0,draggable:e.draggable,tabindex:y.value?0:void 0,onClick:S,onKeydown:y.value&&!h.value&&x}),{default:()=>[Fl(y.value,"v-chip"),f&&t.createVNode(al,{key:"filter"},{default:()=>[t.withDirectives(t.createElementVNode("div",{class:"v-chip__filter"},[o.filter?t.createVNode(nl,{key:"filter-defaults",disabled:!e.filterIcon,defaults:{VIcon:{icon:e.filterIcon}}},o.filter):t.createVNode(Jl,{key:"filter-icon",icon:e.filterIcon},null)]),[[t.vShow,m.isSelected.value]])]}),C&&t.createElementVNode("div",{key:"prepend",class:"v-chip__prepend"},[o.prepend?t.createVNode(nl,{key:"prepend-defaults",disabled:!N,defaults:{VAvatar:{image:e.prependAvatar,start:!0},VIcon:{icon:e.prependIcon,start:!0}}},o.prepend):t.createElementVNode(t.Fragment,null,[e.prependIcon&&t.createVNode(Jl,{key:"prepend-icon",icon:e.prependIcon,start:!0},null),e.prependAvatar&&t.createVNode(Kn,{key:"prepend-avatar",image:e.prependAvatar,start:!0},null)])]),t.createElementVNode("div",{class:"v-chip__content","data-no-activator":""},[o.default?.({isSelected:m?.isSelected.value,selectedClass:m?.selectedClass.value,select:m?.select,toggle:m?.toggle,value:m?.value.value,disabled:e.disabled})??t.toDisplayString(e.text)]),n&&t.createElementVNode("div",{key:"append",class:"v-chip__append"},[o.append?t.createVNode(nl,{key:"append-defaults",disabled:!l,defaults:{VAvatar:{end:!0,image:e.appendAvatar},VIcon:{end:!0,icon:e.appendIcon}}},o.append):t.createElementVNode(t.Fragment,null,[e.appendIcon&&t.createVNode(Jl,{key:"append-icon",end:!0,icon:e.appendIcon},null),e.appendAvatar&&t.createVNode(Kn,{key:"append-avatar",end:!0,image:e.appendAvatar},null)])]),r&&t.createElementVNode("button",t.mergeProps({key:"close",class:"v-chip__close",type:"button","data-testid":"close-chip"},b.value),[o.close?t.createVNode(nl,{key:"close-defaults",defaults:{VIcon:{icon:e.closeIcon,size:"x-small"}}},o.close):t.createVNode(Jl,{key:"close-icon",icon:e.closeIcon,size:"x-small"},null)])]}),[[Dn,y.value&&e.ripple,null]])}}}),Zo=["dotted","dashed","solid","double"],Qo=vt({color:String,contentOffset:[Number,String,Array],gradient:Boolean,inset:Boolean,length:[Number,String],opacity:[Number,String],thickness:[Number,String],vertical:Boolean,variant:{type:String,default:"solid",validator:e=>Zo.includes(e)},...pt(),...ya()},"VDivider"),Jo=wt()({name:"VDivider",props:Qo(),setup(e,a){let{attrs:l,slots:n}=a
const{themeClasses:o}=Ca(e),{textColorClasses:r,textColorStyles:i}=cl(()=>e.color),s=t.computed(()=>{const t={}
return e.length&&(t[e.vertical?"height":"width"]=b(e.length)),e.thickness&&(t[e.vertical?"borderRightWidth":"borderTopWidth"]=b(e.thickness)),t}),u=t.toRef(()=>{const t=Array.isArray(e.contentOffset)?e.contentOffset[0]:e.contentOffset,a=Array.isArray(e.contentOffset)?e.contentOffset[1]:0
return{marginBlock:e.vertical&&t?b(t):void 0,marginInline:!e.vertical&&t?b(t):void 0,transform:a?`translate${e.vertical?"X":"Y"}(${b(a)})`:void 0}})
return Bt(()=>{const a=t.createElementVNode("hr",{class:t.normalizeClass([{"v-divider":!0,"v-divider--gradient":e.gradient&&!n.default,"v-divider--inset":e.inset,"v-divider--vertical":e.vertical},o.value,r.value,e.class]),style:t.normalizeStyle([s.value,i.value,{"--v-border-opacity":e.opacity},{"border-style":e.variant},e.style]),"aria-orientation":l.role&&"separator"!==l.role?void 0:e.vertical?"vertical":"horizontal",role:`${l.role||"separator"}`},null)
return n.default?t.createElementVNode("div",{class:t.normalizeClass(["v-divider__wrapper",{"v-divider__wrapper--gradient":e.gradient,"v-divider__wrapper--inset":e.inset,"v-divider__wrapper--vertical":e.vertical}])},[a,t.createElementVNode("div",{class:"v-divider__content",style:t.normalizeStyle(u.value)},[n.default()]),a]):a}),{}}}),er=Symbol.for("vuetify:list")
function tr(){let{filterable:e}=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{filterable:!1}
const a=t.inject(er,{filterable:!1,hasPrepend:t.shallowRef(!1),updateHasPrepend:()=>null}),l={filterable:a.filterable||e,hasPrepend:t.shallowRef(!1),updateHasPrepend:e=>{e&&(l.hasPrepend.value=e)}}
return t.provide(er,l),a}function ar(){return t.inject(er,null)}const lr=e=>{const a={activate:a=>{let{id:l,value:n,activated:o}=a
return l=t.toRaw(l),e&&!n&&1===o.size&&o.has(l)||(n?o.add(l):o.delete(l)),o},in:(e,t,l)=>{let n=new Set
if(null!=e)for(const o of B(e))n=a.activate({id:o,value:!0,activated:new Set(n),children:t,parents:l})
return n},out:e=>Array.from(e)}
return a},nr=e=>{const a=lr(e)
return{activate:e=>{let{activated:l,id:n,...o}=e
n=t.toRaw(n)
const r=l.has(n)?new Set([n]):new Set
return a.activate({...o,id:n,activated:r})},in:(e,t,l)=>{let n=new Set
if(null!=e){const o=B(e)
o.length&&(n=a.in(o.slice(0,1),t,l))}return n},out:(e,t,l)=>a.out(e,t,l)}},or={open:e=>{let{id:t,value:a,opened:l,parents:n}=e
if(a){const e=new Set
e.add(t)
let a=n.get(t)
for(;null!=a;)e.add(a),a=n.get(a)
return e}return l.delete(t),l},select:()=>null},rr={open:e=>{let{id:t,value:a,opened:l,parents:n}=e
if(a){let e=n.get(t)
for(l.add(t);null!=e&&e!==t;)l.add(e),e=n.get(e)
return l}return l.delete(t),l},select:()=>null},ir={open:rr.open,select:e=>{let{id:t,value:a,opened:l,parents:n}=e
if(!a)return l
const o=[]
let r=n.get(t)
for(;null!=r;)o.push(r),r=n.get(r)
return new Set(o)}},sr=e=>{const a={select:a=>{let{id:l,value:n,selected:o}=a
if(l=t.toRaw(l),e&&!n){const e=Array.from(o.entries()).reduce((e,t)=>{let[a,l]=t
return"on"===l&&e.push(a),e},[])
if(1===e.length&&e[0]===l)return o}return o.set(l,n?"on":"off"),o},in:(e,t,l,n)=>{const o=new Map
for(const r of e||[])a.select({id:r,value:!0,selected:o,children:t,parents:l,disabled:n})
return o},out:e=>{const t=[]
for(const[a,l]of e.entries())"on"===l&&t.push(a)
return t}}
return a},ur=e=>{const a=sr(e)
return{select:e=>{let{selected:l,id:n,...o}=e
n=t.toRaw(n)
const r=l.has(n)?new Map([[n,l.get(n)]]):new Map
return a.select({...o,id:n,selected:r})},in:(e,t,l,n)=>e?.length?a.in(e.slice(0,1),t,l,n):new Map,out:(e,t,l)=>a.out(e,t,l)}},cr=e=>{const a={select:a=>{let{id:l,value:n,selected:o,children:r,parents:i,disabled:s}=a
l=t.toRaw(l)
const u=new Map(o),c=[l]
for(;c.length;){const e=c.shift()
s.has(e)||o.set(t.toRaw(e),n?"on":"off"),r.has(e)&&c.push(...r.get(e))}let d=t.toRaw(i.get(l))
for(;d;){let e=!0,a=!0
for(const l of r.get(d)){const n=t.toRaw(l)
if(!s.has(n)&&("on"!==o.get(n)&&(e=!1),o.has(n)&&"off"!==o.get(n)&&(a=!1),!e&&!a))break}o.set(d,e?"on":a?"off":"indeterminate"),d=t.toRaw(i.get(d))}if(e&&!n){const e=Array.from(o.entries()).reduce((e,t)=>{let[a,l]=t
return"on"===l&&e.push(a),e},[])
if(0===e.length)return u}return o},in:(e,t,l)=>{let n=new Map
for(const o of e||[])n=a.select({id:o,value:!0,selected:n,children:t,parents:l,disabled:new Set})
return n},out:(e,t)=>{const a=[]
for(const[l,n]of e.entries())"on"!==n||t.has(l)||a.push(l)
return a}}
return a},dr=Symbol.for("vuetify:nested"),vr={id:t.shallowRef(),root:{itemsRegistration:t.ref("render"),register:()=>null,unregister:()=>null,updateDisabled:()=>null,children:t.ref(new Map),parents:t.ref(new Map),disabled:t.ref(new Set),open:()=>null,openOnSelect:()=>null,activate:()=>null,select:()=>null,activatable:t.ref(!1),selectable:t.ref(!1),opened:t.ref(new Set),activated:t.ref(new Set),selected:t.ref(new Map),selectedValues:t.ref([]),getPath:()=>[]}},pr=vt({activatable:Boolean,selectable:Boolean,activeStrategy:[String,Function,Object],selectStrategy:[String,Function,Object],openStrategy:[String,Object],opened:null,activated:null,selected:null,mandatory:Boolean,itemsRegistration:{type:String,default:"render"}},"nested"),mr=(e,a,n)=>{let o=!1
const r=t.shallowRef(new Map),i=t.shallowRef(new Map),s=t.shallowRef(new Set),u=la(e,"opened",e.opened,e=>new Set(Array.isArray(e)?e.map(e=>t.toRaw(e)):e),e=>[...e.values()]),c=t.computed(()=>{if("object"==typeof e.activeStrategy)return e.activeStrategy
if("function"==typeof e.activeStrategy)return e.activeStrategy(e.mandatory)
switch(e.activeStrategy){case"leaf":return(e=>{const a=lr(e)
return{activate:e=>{let{id:l,activated:n,children:o,...r}=e
return l=t.toRaw(l),o.has(l)?n:a.activate({id:l,activated:n,children:o,...r})},in:a.in,out:a.out}})(e.mandatory)
case"single-leaf":return(e=>{const a=nr(e)
return{activate:e=>{let{id:l,activated:n,children:o,...r}=e
return l=t.toRaw(l),o.has(l)?n:a.activate({id:l,activated:n,children:o,...r})},in:a.in,out:a.out}})(e.mandatory)
case"independent":return lr(e.mandatory)
default:return nr(e.mandatory)}}),d=t.computed(()=>{if("object"==typeof e.selectStrategy)return e.selectStrategy
if("function"==typeof e.selectStrategy)return e.selectStrategy(e.mandatory)
switch(e.selectStrategy){case"single-leaf":return(e=>{const a=ur(e)
return{select:e=>{let{id:l,selected:n,children:o,...r}=e
return l=t.toRaw(l),o.has(l)?n:a.select({id:l,selected:n,children:o,...r})},in:a.in,out:a.out}})(e.mandatory)
case"leaf":return(e=>{const a=sr(e)
return{select:e=>{let{id:l,selected:n,children:o,...r}=e
return l=t.toRaw(l),o.has(l)?n:a.select({id:l,selected:n,children:o,...r})},in:a.in,out:a.out}})(e.mandatory)
case"independent":return sr(e.mandatory)
case"single-independent":return ur(e.mandatory)
case"trunk":return(e=>{const t=cr(e)
return{select:t.select,in:t.in,out:(e,t,a)=>{const l=[]
for(const[t,n]of e.entries())if("on"===n){if(a.has(t)){const l=a.get(t)
if("on"===e.get(l))continue}l.push(t)}return l}}})(e.mandatory)
default:return cr(e.mandatory)}}),v=t.computed(()=>{if("object"==typeof e.openStrategy)return e.openStrategy
switch(e.openStrategy){case"list":return ir
case"single":return or
default:return rr}}),p=la(e,"activated",e.activated,e=>c.value.in(e,r.value,i.value),e=>c.value.out(e,r.value,i.value)),m=la(e,"selected",e.selected,e=>d.value.in(e,r.value,i.value,s.value),e=>d.value.out(e,r.value,i.value))
function f(e){const a=[]
let l=t.toRaw(e)
for(;void 0!==l;)a.unshift(l),l=i.value.get(l)
return a}t.onBeforeUnmount(()=>{o=!0})
const g=mt("nested"),h=new Set,y=function(e,t){let a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{leading:!0,trailing:!0},l=0,n=0,o=!1,r=0
function i(){clearTimeout(l),o=!1,r=0}const s=function(){for(var s=arguments.length,u=new Array(s),c=0;c<s;c++)u[c]=arguments[c]
clearTimeout(l)
const d=Date.now()
r||(r=d)
const v=d-Math.max(r,n)
function p(){n=Date.now(),l=setTimeout(i,t),e(...u)}o?v>=t?p():a.trailing&&(l=setTimeout(p,t-v)):(o=!0,a.leading&&p())}
return s.clear=i,s.immediate=e,s}(()=>{t.nextTick(()=>{r.value=new Map(r.value),i.value=new Map(i.value)})},100)
t.watch(()=>[a.value,t.toValue(n)],()=>{"props"===e.itemsRegistration&&function(){const e=new Map,l=new Map,o=new Set,u=t.toValue(n)?e=>t.toRaw(e.raw):e=>e.value,c=[...a.value]
let d=0
for(;d<c.length;){const t=c[d++],a=u(t)
if(t.children){const n=[]
for(const l of t.children){const t=u(l)
e.set(t,a),n.push(t),c.push(l)}l.set(a,n)}t.props.disabled&&o.add(a)}r.value=l,i.value=e,s.value=o}()},{immediate:!0})
const b={id:t.shallowRef(),root:{opened:u,activatable:t.toRef(()=>e.activatable),selectable:t.toRef(()=>e.selectable),activated:p,selected:m,selectedValues:t.computed(()=>{const e=[]
for(const[t,a]of m.value.entries())"on"===a&&e.push(t)
return e}),itemsRegistration:t.toRef(()=>e.itemsRegistration),register:(e,t,a,n)=>{if(h.has(e)){return void l(`Multiple nodes with the same ID\n\t${f(e).map(String).join(" -> ")}\n\t${f(t).concat(e).map(String).join(" -> ")}`)}h.add(e),t&&e!==t&&i.value.set(e,t),a&&s.value.add(e),n&&r.value.set(e,[]),null!=t&&r.value.set(t,[...r.value.get(t)||[],e]),y()},unregister:e=>{if(o)return
h.delete(e),r.value.delete(e),s.value.delete(e)
const t=i.value.get(e)
if(t){const a=r.value.get(t)??[]
r.value.set(t,a.filter(t=>t!==e))}i.value.delete(e),y()},updateDisabled:(e,t)=>{t?s.value.add(e):s.value.delete(e)},open:(e,t,a)=>{g.emit("click:open",{id:e,value:t,path:f(e),event:a})
const l=v.value.open({id:e,value:t,opened:new Set(u.value),children:r.value,parents:i.value,event:a})
l&&(u.value=l)},openOnSelect:(e,t,a)=>{const l=v.value.select({id:e,value:t,selected:new Map(m.value),opened:new Set(u.value),children:r.value,parents:i.value,event:a})
l&&(u.value=l)},select:(e,t,a)=>{g.emit("click:select",{id:e,value:t,path:f(e),event:a})
const l=d.value.select({id:e,value:t,selected:new Map(m.value),children:r.value,parents:i.value,disabled:s.value,event:a})
l&&(m.value=l),b.root.openOnSelect(e,t,a)},activate:(t,a,l)=>{if(!e.activatable)return b.root.select(t,!0,l)
g.emit("click:activate",{id:t,value:a,path:f(t),event:l})
const n=c.value.activate({id:t,value:a,activated:new Set(p.value),children:r.value,parents:i.value,event:l})
if(n.size!==p.value.size)p.value=n
else{for(const e of n)if(!p.value.has(e))return void(p.value=n)
for(const e of p.value)if(!n.has(e))return void(p.value=n)}},children:r,parents:i,disabled:s,getPath:f}}
return t.provide(dr,b),b.root},fr=(e,a,l)=>{const n=t.inject(dr,vr),o=Symbol("nested item"),r=t.computed(()=>{const a=t.toRaw(t.toValue(e))
return void 0!==a?a:o}),i={...n,id:r,open:(e,t)=>n.root.open(r.value,e,t),openOnSelect:(e,t)=>n.root.openOnSelect(r.value,e,t),isOpen:t.computed(()=>n.root.opened.value.has(r.value)),parent:t.computed(()=>n.root.parents.value.get(r.value)),activate:(e,t)=>n.root.activate(r.value,e,t),isActivated:t.computed(()=>n.root.activated.value.has(r.value)),select:(e,t)=>n.root.select(r.value,e,t),isSelected:t.computed(()=>"on"===n.root.selected.value.get(r.value)),isIndeterminate:t.computed(()=>"indeterminate"===n.root.selected.value.get(r.value)),isLeaf:t.computed(()=>!n.root.children.value.get(r.value)),isGroupActivator:n.isGroupActivator}
return t.onBeforeMount(()=>{n.isGroupActivator||"props"===n.root.itemsRegistration.value||t.nextTick(()=>{n.root.register(r.value,n.id.value,t.toValue(a),l)})}),t.onBeforeUnmount(()=>{n.isGroupActivator||"props"===n.root.itemsRegistration.value||n.root.unregister(r.value)}),t.watch(r,(e,o)=>{n.isGroupActivator||"props"===n.root.itemsRegistration.value||(n.root.unregister(o),t.nextTick(()=>{n.root.register(e,n.id.value,t.toValue(a),l)}))}),t.watch(()=>t.toValue(a),e=>{n.root.updateDisabled(r.value,e)}),l&&t.provide(dr,i),i},gr=Vt({name:"VListGroupActivator",setup(e,a){let{slots:l}=a
return(()=>{const e=t.inject(dr,vr)
t.provide(dr,{...e,isGroupActivator:!0})})(),()=>l.default?.()}}),hr=vt({activeColor:String,baseColor:String,color:String,collapseIcon:{type:Dt,default:"$collapse"},disabled:Boolean,expandIcon:{type:Dt,default:"$expand"},rawId:[String,Number],prependIcon:Dt,appendIcon:Dt,fluid:Boolean,subgroup:Boolean,title:String,value:null,...pt(),...Pa()},"VListGroup"),yr=wt()({name:"VListGroup",props:hr(),setup(e,a){let{slots:l}=a
const{isOpen:n,open:o,id:r}=fr(()=>e.value,()=>e.disabled,!0),i=t.computed(()=>`v-list-group--id-${String(e.rawId??r.value)}`),s=ar(),{isBooted:u}=_l(),c=t.inject(dr),d=t.toRef(()=>"render"===c?.root?.itemsRegistration.value)
function v(e){["INPUT","TEXTAREA"].includes(e.target?.tagName)||o(!n.value,e)}const p=t.computed(()=>({onClick:v,class:"v-list-group__header",id:i.value})),m=t.computed(()=>n.value?e.collapseIcon:e.expandIcon),f=t.computed(()=>({VListItem:{activeColor:e.activeColor,baseColor:e.baseColor,color:e.color,prependIcon:e.prependIcon||e.subgroup&&m.value,appendIcon:e.appendIcon||!e.subgroup&&m.value,title:e.title,value:e.value}}))
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-list-group",{"v-list-group--prepend":s?.hasPrepend.value,"v-list-group--fluid":e.fluid,"v-list-group--subgroup":e.subgroup,"v-list-group--open":n.value},e.class]),style:t.normalizeStyle(e.style)},{default:()=>[l.activator&&t.createVNode(nl,{defaults:f.value},{default:()=>[t.createVNode(gr,null,{default:()=>[l.activator({props:p.value,isOpen:n.value})]})]}),t.createVNode(gl,{transition:{component:tl},disabled:!u.value},{default:()=>[d.value?t.withDirectives(t.createElementVNode("div",{class:"v-list-group__items",role:"group","aria-labelledby":i.value},[l.default?.()]),[[t.vShow,n.value]]):n.value&&t.createElementVNode("div",{class:"v-list-group__items",role:"group","aria-labelledby":i.value},[l.default?.()])]})]})),{isOpen:n}}}),br=vt({opacity:[Number,String],...pt(),...Pa()},"VListItemSubtitle"),Vr=wt()({name:"VListItemSubtitle",props:br(),setup(e,a){let{slots:l}=a
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-list-item-subtitle",e.class]),style:t.normalizeStyle([{"--v-list-item-subtitle-opacity":e.opacity},e.style])},l)),{}}}),wr=kt("v-list-item-title"),kr=vt({active:{type:Boolean,default:void 0},activeClass:String,activeColor:String,appendAvatar:String,appendIcon:Dt,baseColor:String,disabled:Boolean,lines:[Boolean,String],link:{type:Boolean,default:void 0},nav:Boolean,prependAvatar:String,prependIcon:Dt,ripple:{type:[Boolean,Object],default:!0},slim:Boolean,prependGap:[Number,String],subtitle:{type:[String,Number,Boolean],default:void 0},title:{type:[String,Number,Boolean],default:void 0},value:null,onClick:Z(),onClickOnce:Z(),...wl(),...pt(),...Tl(),...ol(),...Sl(),...pl(),...yn(),...Pa(),...ya(),...$l({variant:"text"})},"VListItem"),Sr=wt()({name:"VListItem",directives:{vRipple:Dn},props:kr(),emits:{click:e=>!0},setup(e,a){let{attrs:l,slots:o,emit:r}=a
const i=hn(e,l),s=t.computed(()=>void 0===e.value?i.href.value:e.value),{activate:u,isActivated:c,select:d,isOpen:v,isSelected:p,isIndeterminate:m,isGroupActivator:f,root:g,parent:h,openOnSelect:y,id:V}=fr(s,()=>e.disabled,!1),w=ar(),k=t.computed(()=>!1!==e.active&&(e.active||i.isActive?.value||(g.activatable.value?c.value:p.value))),S=t.toRef(()=>!1!==e.link&&i.isLink.value),x=t.computed(()=>!!w&&(g.selectable.value||g.activatable.value||null!=e.value)),N=t.computed(()=>!e.disabled&&!1!==e.link&&(e.link||i.isClickable.value||x.value)),C=t.computed(()=>w?S.value?"link":x.value?"option":"listitem":void 0),E=t.computed(()=>{if(x.value)return g.activatable.value?c.value:g.selectable.value?p.value:k.value}),I=t.toRef(()=>e.rounded||e.nav),_=t.toRef(()=>e.color??e.activeColor),P=t.toRef(()=>({color:k.value?_.value??e.baseColor:e.baseColor,variant:e.variant}))
function A(){null!=h.value&&g.open(h.value,!0),y(!0)}t.watch(()=>i.isActive?.value,e=>{e&&A()}),t.onBeforeMount(()=>{i.isActive?.value&&t.nextTick(()=>A())})
const{themeClasses:R}=Ca(e),{borderClasses:T}=kl(e),{colorClasses:B,colorStyles:D,variantClasses:F}=Ml(P),{densityClasses:$}=Bl(e),{dimensionStyles:M}=rl(e),{elevationClasses:z}=xl(e),{roundedClasses:L}=ml(I),O=t.toRef(()=>e.lines?`v-list-item--${e.lines}-line`:void 0),j=t.toRef(()=>void 0!==e.ripple&&e.ripple&&w?.filterable?{keys:["Enter"]}:e.ripple),H=t.computed(()=>({isActive:k.value,select:d,isOpen:v.value,isSelected:p.value,isIndeterminate:m.value}))
function W(t){r("click",t),["INPUT","TEXTAREA"].includes(t.target?.tagName)||N.value&&(i.navigate?.(t),f||(g.activatable.value?u(!c.value,t):g.selectable.value?d(!p.value,t):null==e.value||S.value||d(!p.value,t)))}function Y(e){const t=e.target;["INPUT","TEXTAREA"].includes(t.tagName)||("Enter"===e.key||" "===e.key&&!w?.filterable)&&(e.preventDefault(),e.stopPropagation(),e.target.dispatchEvent(new MouseEvent("click",e)))}return Bt(()=>{const a=S.value?"a":e.tag,l=o.title||null!=e.title,r=o.subtitle||null!=e.subtitle,s=!(!e.appendAvatar&&!e.appendIcon),u=!(!s&&!o.append),c=!(!e.prependAvatar&&!e.prependIcon),d=!(!c&&!o.prepend)
return w?.updateHasPrepend(d),e.activeColor&&n("active-color",["color","base-color"]),t.withDirectives(t.createVNode(a,t.mergeProps(i.linkProps,{class:["v-list-item",{"v-list-item--active":k.value,"v-list-item--disabled":e.disabled,"v-list-item--link":N.value,"v-list-item--nav":e.nav,"v-list-item--slim":e.slim,[`${e.activeClass}`]:e.activeClass&&k.value},R.value,T.value,B.value,$.value,z.value,O.value,L.value,F.value,e.class],style:[{"--v-list-prepend-gap":b(e.prependGap)},D.value,M.value,e.style],tabindex:N.value?w?-2:0:void 0,"aria-selected":E.value,role:C.value,onClick:W,onKeydown:N.value&&!S.value&&Y}),{default:()=>[Fl(N.value||k.value,"v-list-item"),d&&t.createElementVNode("div",{key:"prepend",class:"v-list-item__prepend"},[o.prepend?t.createVNode(nl,{key:"prepend-defaults",disabled:!c,defaults:{VAvatar:{density:e.density,image:e.prependAvatar},VIcon:{density:e.density,icon:e.prependIcon},VListItemAction:{start:!0}}},{default:()=>[o.prepend?.(H.value)]}):t.createElementVNode(t.Fragment,null,[e.prependAvatar&&t.createVNode(Kn,{key:"prepend-avatar",density:e.density,image:e.prependAvatar},null),e.prependIcon&&t.createVNode(Jl,{key:"prepend-icon",density:e.density,icon:e.prependIcon},null)]),t.createElementVNode("div",{class:"v-list-item__spacer"},null)]),t.createElementVNode("div",{class:"v-list-item__content","data-no-activator":""},[l&&t.createVNode(wr,{key:"title"},{default:()=>[o.title?.({title:e.title})??t.toDisplayString(e.title)]}),r&&t.createVNode(Vr,{key:"subtitle"},{default:()=>[o.subtitle?.({subtitle:e.subtitle})??t.toDisplayString(e.subtitle)]}),o.default?.(H.value)]),u&&t.createElementVNode("div",{key:"append",class:"v-list-item__append"},[o.append?t.createVNode(nl,{key:"append-defaults",disabled:!s,defaults:{VAvatar:{density:e.density,image:e.appendAvatar},VIcon:{density:e.density,icon:e.appendIcon},VListItemAction:{end:!0}}},{default:()=>[o.append?.(H.value)]}):t.createElementVNode(t.Fragment,null,[e.appendIcon&&t.createVNode(Jl,{key:"append-icon",density:e.density,icon:e.appendIcon},null),e.appendAvatar&&t.createVNode(Kn,{key:"append-avatar",density:e.density,image:e.appendAvatar},null)]),t.createElementVNode("div",{class:"v-list-item__spacer"},null)])]}),[[Dn,N.value&&j.value]])}),{activate:u,isActivated:c,isGroupActivator:f,isSelected:p,list:w,select:d,root:g,id:V,link:i}}}),xr=vt({color:String,inset:Boolean,sticky:Boolean,title:String,...pt(),...Pa()},"VListSubheader"),Nr=wt()({name:"VListSubheader",props:xr(),setup(e,a){let{slots:l}=a
const{textColorClasses:n,textColorStyles:o}=cl(()=>e.color)
return Bt(()=>{const a=!(!l.default&&!e.title)
return t.createVNode(e.tag,{class:t.normalizeClass(["v-list-subheader",{"v-list-subheader--inset":e.inset,"v-list-subheader--sticky":e.sticky},n.value,e.class]),style:t.normalizeStyle([{textColorStyles:o},e.style])},{default:()=>[a&&t.createElementVNode("div",{class:"v-list-subheader__text"},[l.default?.()??e.title])]})}),{}}}),Cr=vt({items:Array,returnObject:Boolean},"VListChildren"),Er=wt()({name:"VListChildren",props:Cr(),setup(e,a){let{slots:l}=a
return tr(),()=>l.default?.()??e.items?.map(a=>{let{children:n,props:o,type:r,raw:i}=a
if("divider"===r)return l.divider?.({props:o})??t.createVNode(Jo,o,null)
if("subheader"===r)return l.subheader?.({props:o})??t.createVNode(Nr,o,null)
const s={subtitle:l.subtitle?e=>l.subtitle?.({...e,item:i}):void 0,prepend:l.prepend?e=>l.prepend?.({...e,item:i}):void 0,append:l.append?e=>l.append?.({...e,item:i}):void 0,title:l.title?e=>l.title?.({...e,item:i}):void 0},u=yr.filterProps(o)
return n?t.createVNode(yr,t.mergeProps(u,{value:e.returnObject?i:o?.value,rawId:o?.value}),{activator:a=>{let{props:n}=a
const r=t.mergeProps(o,n,{value:e.returnObject?i:o.value})
return l.header?l.header({props:r}):t.createVNode(Sr,r,s)},default:()=>t.createVNode(Er,{items:n,returnObject:e.returnObject},l)}):l.item?l.item({props:o}):t.createVNode(Sr,t.mergeProps(o,{value:e.returnObject?i:o.value}),s)})}}),Ir=vt({items:{type:Array,default:()=>[]},itemTitle:{type:[String,Array,Function],default:"title"},itemValue:{type:[String,Array,Function],default:"value"},itemChildren:{type:[Boolean,String,Array,Function],default:"children"},itemProps:{type:[Boolean,String,Array,Function],default:"props"},itemType:{type:[Boolean,String,Array,Function],default:"type"},returnObject:Boolean,valueComparator:Function},"list-items"),_r=new Set(["item","divider","subheader"])
function Pr(e,t){const a=h(t,e.itemTitle,t),l=h(t,e.itemValue,a),n=h(t,e.itemChildren),o=!0===e.itemProps?"object"!=typeof t||null==t||Array.isArray(t)?void 0:"children"in t?I(t,["children"]):t:h(t,e.itemProps)
let r=h(t,e.itemType,"item")
_r.has(r)||(r="item")
const i={title:a,value:l,...o}
return{type:r,title:String(i.title??""),value:i.value,props:i,children:"item"===r&&Array.isArray(n)?Ar(e,n):void 0,raw:t}}function Ar(e,t){const a=C(e,Pr.neededProps),l=[]
for(const e of t)l.push(Pr(a,e))
return l}function Rr(e){const a=t.computed(()=>Ar(e,e.items)),l=t.computed(()=>a.value.some(e=>null===e.value)),n=t.shallowRef(new Map),o=t.shallowRef([])
return t.watchEffect(()=>{const e=a.value,t=new Map,l=[]
for(let a=0;a<e.length;a++){const n=e[a]
if(ce(n.value)||null===n.value){let e=t.get(n.value)
e||(e=[],t.set(n.value,e)),e.push(n)}else l.push(n)}n.value=t,o.value=l}),{items:a,transformIn:function(t){const r=n.value,i=a.value,s=o.value,u=l.value,c=e.returnObject,d=!!e.valueComparator,v=e.valueComparator||St,p=C(e,Pr.neededProps),m=[]
e:for(const e of t){if(!u&&null===e)continue
if(c&&"string"==typeof e){m.push(Pr(p,e))
continue}const t=r.get(e)
if(!d&&t)m.push(...t)
else{for(const t of d?i:s)if(v(e,t.value)){m.push(t)
continue e}m.push(Pr(p,e))}}return m},transformOut:function(t){return e.returnObject?t.map(e=>{let{raw:t}=e
return t}):t.map(e=>{let{value:t}=e
return t})}}}Pr.neededProps=["itemTitle","itemValue","itemChildren","itemProps","itemType"]
const Tr=new Set(["item","divider","subheader"])
function Br(e,t){const a=ce(t)?t:h(t,e.itemTitle),l=ce(t)?t:h(t,e.itemValue,void 0),n=h(t,e.itemChildren),o=!0===e.itemProps?I(t,["children"]):h(t,e.itemProps)
let r=h(t,e.itemType,"item")
Tr.has(r)||(r="item")
const i={title:a,value:l,...o}
return{type:r,title:i.title,value:i.value,props:i,children:"item"===r&&n?Dr(e,n):void 0,raw:t}}function Dr(e,t){const a=[]
for(const l of t)a.push(Br(e,l))
return a}function Fr(e){return{items:t.computed(()=>Dr(e,e.items))}}const $r=vt({baseColor:String,activeColor:String,activeClass:String,bgColor:String,disabled:Boolean,filterable:Boolean,expandIcon:Dt,collapseIcon:Dt,lines:{type:[Boolean,String],default:"one"},slim:Boolean,prependGap:[Number,String],indent:[Number,String],nav:Boolean,"onClick:open":Z(),"onClick:select":Z(),"onUpdate:opened":Z(),...pr({selectStrategy:"single-leaf",openStrategy:"list"}),...wl(),...pt(),...Tl(),...ol(),...Sl(),...Ir(),...pl(),...Pa(),...ya(),...$l({variant:"text"})},"VList"),Mr=wt()({name:"VList",props:$r(),emits:{"update:selected":e=>!0,"update:activated":e=>!0,"update:opened":e=>!0,"click:open":e=>!0,"click:activate":e=>!0,"click:select":e=>!0},setup(e,a){let{slots:l}=a
const{items:n}=Fr(e),{themeClasses:o}=Ca(e),{backgroundColorClasses:r,backgroundColorStyles:i}=dl(()=>e.bgColor),{borderClasses:s}=kl(e),{densityClasses:u}=Bl(e),{dimensionStyles:c}=rl(e),{elevationClasses:d}=xl(e),{roundedClasses:v}=ml(e),{children:p,open:m,parents:f,select:g,getPath:h}=mr(e,n,()=>e.returnObject),y=t.toRef(()=>e.lines?`v-list--${e.lines}-line`:void 0),V=t.toRef(()=>e.activeColor),w=t.toRef(()=>e.baseColor),k=t.toRef(()=>e.color),S=t.toRef(()=>e.selectable||e.activatable)
tr({filterable:e.filterable}),yt({VListGroup:{activeColor:V,baseColor:w,color:k,expandIcon:t.toRef(()=>e.expandIcon),collapseIcon:t.toRef(()=>e.collapseIcon)},VListItem:{activeClass:t.toRef(()=>e.activeClass),activeColor:V,baseColor:w,color:k,density:t.toRef(()=>e.density),disabled:t.toRef(()=>e.disabled),lines:t.toRef(()=>e.lines),nav:t.toRef(()=>e.nav),slim:t.toRef(()=>e.slim),variant:t.toRef(()=>e.variant)}})
const x=t.shallowRef(!1),N=t.ref()
function C(e){x.value=!0}function E(e){x.value=!1}function I(e){x.value||e.relatedTarget&&N.value?.contains(e.relatedTarget)||A()}function _(e){const t=e.target
if(N.value&&("INPUT"!==t.tagName||!["Home","End"].includes(e.key))&&"TEXTAREA"!==t.tagName){if("ArrowDown"===e.key)A("next")
else if("ArrowUp"===e.key)A("prev")
else if("Home"===e.key)A("first")
else{if("End"!==e.key)return
A("last")}e.preventDefault()}}function P(e){x.value=!0}function A(e){if(N.value)return ae(N.value,e)}return Bt(()=>{const a=e.indent??(e.prependGap?Number(e.prependGap)+24:void 0)
return t.createVNode(e.tag,{ref:N,class:t.normalizeClass(["v-list",{"v-list--disabled":e.disabled,"v-list--nav":e.nav,"v-list--slim":e.slim},o.value,r.value,s.value,u.value,d.value,y.value,v.value,e.class]),style:t.normalizeStyle([{"--v-list-indent":b(a),"--v-list-group-prepend":a?"0px":void 0,"--v-list-prepend-gap":b(e.prependGap)},i.value,c.value,e.style]),tabindex:e.disabled?-1:0,role:S.value?"listbox":"list","aria-activedescendant":void 0,onFocusin:C,onFocusout:E,onFocus:I,onKeydown:_,onMousedown:P},{default:()=>[t.createVNode(Er,{items:n.value,returnObject:e.returnObject},l)]})}),{open:m,select:g,focus:A,children:p,parents:f,getPath:h}}}),zr=kt("v-list-img"),Lr=vt({start:Boolean,end:Boolean,...pt(),...Pa()},"VListItemAction"),Or=wt()({name:"VListItemAction",props:Lr(),setup(e,a){let{slots:l}=a
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-list-item-action",{"v-list-item-action--start":e.start,"v-list-item-action--end":e.end},e.class]),style:t.normalizeStyle(e.style)},l)),{}}}),jr=vt({start:Boolean,end:Boolean,...pt(),...Pa()},"VListItemMedia"),Hr=wt()({name:"VListItemMedia",props:jr(),setup(e,a){let{slots:l}=a
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-list-item-media",{"v-list-item-media--start":e.start,"v-list-item-media--end":e.end},e.class]),style:t.normalizeStyle(e.style)},l)),{}}})
function Wr(e,t){return{x:e.x+t.x,y:e.y+t.y}}function Yr(e,t){if("top"===e.side||"bottom"===e.side){const{side:a,align:l}=e
return Wr({x:"left"===l?0:"center"===l?t.width/2:"right"===l?t.width:l,y:"top"===a?0:"bottom"===a?t.height:a},t)}if("left"===e.side||"right"===e.side){const{side:a,align:l}=e
return Wr({x:"left"===a?0:"right"===a?t.width:a,y:"top"===l?0:"center"===l?t.height/2:"bottom"===l?t.height:l},t)}return Wr({x:t.width/2,y:t.height/2},t)}const Ur={static:function(){},connected:function(e,a,n){(Array.isArray(e.target.value)||function(e){for(;e;){if("fixed"===window.getComputedStyle(e).position)return!0
e=e.offsetParent}return!1}(e.target.value))&&Object.assign(n.value,{position:"fixed",top:0,[e.isRtl.value?"right":"left"]:0})
const{preferredAnchor:o,preferredOrigin:r}=K(()=>{const t=fe(a.location,e.isRtl.value),l="overlap"===a.origin?t:"auto"===a.origin?he(t):fe(a.origin,e.isRtl.value)
return t.side===l.side&&t.align===ye(l).align?{preferredAnchor:be(t),preferredOrigin:be(l)}:{preferredAnchor:t,preferredOrigin:l}}),[i,s,u,c]=["minWidth","minHeight","maxWidth","maxHeight"].map(e=>t.computed(()=>{const t=parseFloat(a[e])
return isNaN(t)?1/0:t})),d=t.computed(()=>{if(Array.isArray(a.offset))return a.offset
if("string"==typeof a.offset){const e=a.offset.split(" ").map(parseFloat)
return e.length<2&&e.push(0),e}return"number"==typeof a.offset?[a.offset,0]:[0,0]})
let v=!1,p=-1
const m=new G(4),f=new ResizeObserver(()=>{if(!v)return
if(requestAnimationFrame(e=>{e!==p&&m.clear(),requestAnimationFrame(e=>{p=e})}),m.isFull){const e=m.values()
if(St(e.at(-1),e.at(-3))&&!St(e.at(-1),e.at(-2)))return}const e=h()
e&&m.push(e.flipped)})
let g=new we({x:0,y:0,width:0,height:0})
function h(){if(v=!1,requestAnimationFrame(()=>v=!0),!e.target.value||!e.contentEl.value)return;(Array.isArray(e.target.value)||e.target.value.offsetParent||e.target.value.getClientRects().length)&&(g=Se(e.target.value))
const t=function(e,t){const a=xe(e)
t?a.x+=parseFloat(e.style.right||0):a.x-=parseFloat(e.style.left||0)
return a.y-=parseFloat(e.style.top||0),a}(e.contentEl.value,e.isRtl.value),p=At(e.contentEl.value),m=Number(a.viewportMargin)
p.length||(p.push(document.documentElement),e.contentEl.value.style.top&&e.contentEl.value.style.left||(t.x-=parseFloat(document.documentElement.style.getPropertyValue("--v-body-scroll-x")||0),t.y-=parseFloat(document.documentElement.style.getPropertyValue("--v-body-scroll-y")||0)))
const f=p.reduce((e,t)=>{const a=function(e){if(e===document.documentElement){if(visualViewport){const e=document.body.currentCSSZoom??1
return new we({x:visualViewport.scale>1?0:visualViewport.offsetLeft,y:visualViewport.scale>1?0:visualViewport.offsetTop,width:visualViewport.width*visualViewport.scale/e,height:visualViewport.height*visualViewport.scale/e})}return new we({x:0,y:0,width:document.documentElement.clientWidth,height:document.documentElement.clientHeight})}return new we(e)}(t)
return e?new we({x:Math.max(e.left,a.left),y:Math.max(e.top,a.top),width:Math.min(e.right,a.right)-Math.max(e.left,a.left),height:Math.min(e.bottom,a.bottom)-Math.max(e.top,a.top)}):a},void 0)
a.stickToTarget?(f.x+=Math.min(m,g.x),f.y+=Math.min(m,g.y),f.width=Math.max(f.width-2*m,g.x+g.width-m),f.height=Math.max(f.height-2*m,g.y+g.height-m)):(f.x+=m,f.y+=m,f.width-=2*m,f.height-=2*m)
let h={anchor:o.value,origin:r.value}
function y(e){const a=new we(t),l=Yr(e.anchor,g),n=Yr(e.origin,a)
let{x:o,y:r}=(s=n,{x:(i=l).x-s.x,y:i.y-s.y})
var i,s
switch(e.anchor.side){case"top":r-=d.value[0]
break
case"bottom":r+=d.value[0]
break
case"left":o-=d.value[0]
break
case"right":o+=d.value[0]}switch(e.anchor.align){case"top":r-=d.value[1]
break
case"bottom":r+=d.value[1]
break
case"left":o-=d.value[1]
break
case"right":o+=d.value[1]}a.x+=o,a.y+=r,a.width=Math.min(a.width,u.value),a.height=Math.min(a.height,c.value)
return{overflows:ke(a,f),x:o,y:r}}let V=0,w=0
const k={x:0,y:0},S={x:!1,y:!1}
let x=-1
for(;;){if(x++>10){l("Infinite loop detected in connectedLocationStrategy")
break}const{x:e,y:a,overflows:n}=y(h)
V+=e,w+=a,t.x+=e,t.y+=a
{const e=Ve(h.anchor),t=n.x.before||n.x.after,a=n.y.before||n.y.after
let l=!1
if(["x","y"].forEach(o=>{if("x"===o&&t&&!S.x||"y"===o&&a&&!S.y){const t={anchor:{...h.anchor},origin:{...h.origin}},a="x"===o?"y"===e?ye:he:"y"===e?he:ye
t.anchor=a(t.anchor),t.origin=a(t.origin)
const{overflows:r}=y(t);(r[o].before<=n[o].before&&r[o].after<=n[o].after||r[o].before+r[o].after<(n[o].before+n[o].after)/2)&&(h=t,l=S[o]=!0)}}),l)continue}n.x.before&&(V+=n.x.before,t.x+=n.x.before),n.x.after&&(V-=n.x.after,t.x-=n.x.after),n.y.before&&(w+=n.y.before,t.y+=n.y.before),n.y.after&&(w-=n.y.after,t.y-=n.y.after)
{const e=ke(t,f)
k.x=f.width-e.x.before-e.x.after,k.y=f.height-e.y.before-e.y.after,V+=e.x.before,t.x+=e.x.before,w+=e.y.before,t.y+=e.y.before}break}const N=Ve(h.anchor)
return Object.assign(n.value,{"--v-overlay-anchor-origin":`${h.anchor.side} ${h.anchor.align}`,transformOrigin:`${h.origin.side} ${h.origin.align}`,top:b(Kr(w)),left:e.isRtl.value?void 0:b(Kr(V)),right:e.isRtl.value?b(Kr(-V)):void 0,minWidth:b("y"===N?Math.min(i.value,g.width):i.value),maxWidth:b(qr(F(k.x,i.value===1/0?0:i.value,u.value))),maxHeight:b(qr(F(k.y,s.value===1/0?0:s.value,c.value)))}),{available:k,contentBox:t,flipped:S}}return t.watch(e.target,(e,t)=>{t&&!Array.isArray(t)&&f.unobserve(t),Array.isArray(e)?St(e,t)||h():e&&f.observe(e)},{immediate:!0}),t.watch(e.contentEl,(e,t)=>{t&&f.unobserve(t),e&&f.observe(e)},{immediate:!0}),t.onScopeDispose(()=>{f.disconnect()}),t.watch(()=>[o.value,r.value,a.offset,a.minWidth,a.minHeight,a.maxWidth,a.maxHeight],()=>h()),t.nextTick(()=>{const e=h()
if(!e)return
const{available:t,contentBox:a}=e
a.height>t.y&&requestAnimationFrame(()=>{h(),requestAnimationFrame(()=>{h()})})}),{updateLocation:h}}},Gr=vt({locationStrategy:{type:[String,Function],default:"static",validator:e=>"function"==typeof e||e in Ur},location:{type:String,default:"bottom"},origin:{type:String,default:"auto"},offset:[Number,String,Array],stickToTarget:Boolean,viewportMargin:{type:[Number,String],default:12}},"VOverlay-location-strategies")
function Kr(e){return Math.round(e*devicePixelRatio)/devicePixelRatio}function qr(e){return Math.ceil(e*devicePixelRatio)/devicePixelRatio}let Xr=!0
const Zr=[]
let Qr=-1
function Jr(){cancelAnimationFrame(Qr),Qr=requestAnimationFrame(()=>{const e=Zr.shift()
e&&e(),Zr.length?Jr():Xr=!0})}const ei={none:null,close:function(e){li(ai(e.target.value,e.contentEl.value),function(t){e.isActive.value=!1})},block:function(e,a){const l=e.root.value?.offsetParent,n=ai(e.target.value,e.contentEl.value),o=[...new Set([...At(n,a.contained?l:void 0),...At(e.contentEl.value,a.contained?l:void 0)])].filter(e=>!e.classList.contains("v-overlay-scroll-blocked")),r=window.innerWidth-document.documentElement.offsetWidth,i=(s=l||document.documentElement,Rt(s)&&s)
var s
i&&e.root.value.classList.add("v-overlay--scroll-blocked")
o.forEach((e,t)=>{e.style.setProperty("--v-body-scroll-x",b(-e.scrollLeft)),e.style.setProperty("--v-body-scroll-y",b(-e.scrollTop)),e!==document.documentElement&&e.style.setProperty("--v-scrollbar-offset",b(r)),e.classList.add("v-overlay-scroll-blocked")}),t.onScopeDispose(()=>{o.forEach((e,t)=>{const a=parseFloat(e.style.getPropertyValue("--v-body-scroll-x")),l=parseFloat(e.style.getPropertyValue("--v-body-scroll-y")),n=e.style.scrollBehavior
e.style.scrollBehavior="auto",e.style.removeProperty("--v-body-scroll-x"),e.style.removeProperty("--v-body-scroll-y"),e.style.removeProperty("--v-scrollbar-offset"),e.classList.remove("v-overlay-scroll-blocked"),e.scrollLeft=-a,e.scrollTop=-l,e.style.scrollBehavior=n}),i&&e.root.value.classList.remove("v-overlay--scroll-blocked")})},reposition:function(e,a,l){let n=!1,o=-1,r=-1
function i(t){var a
a=()=>{const a=performance.now()
e.updateLocation.value?.(t)
const l=performance.now()-a
n=l/(1e3/60)>2},!Xr||Zr.length?(Zr.push(a),Jr()):(Xr=!1,a(),Jr())}r=("undefined"==typeof requestIdleCallback?e=>e():requestIdleCallback)(()=>{l.run(()=>{li(ai(e.target.value,e.contentEl.value),e=>{n?(cancelAnimationFrame(o),o=requestAnimationFrame(()=>{o=requestAnimationFrame(()=>{i(e)})})):i(e)})})}),t.onScopeDispose(()=>{"undefined"!=typeof cancelIdleCallback&&cancelIdleCallback(r),cancelAnimationFrame(o)})}},ti=vt({scrollStrategy:{type:[String,Function],default:"block",validator:e=>"function"==typeof e||e in ei}},"VOverlay-scroll-strategies")
function ai(e,t){return Array.isArray(e)?document.elementsFromPoint(...e).find(e=>!t?.contains(e)):e??t}function li(e,a){const l=[document,...At(e)]
l.forEach(e=>{e.addEventListener("scroll",a,{passive:!0})}),t.onScopeDispose(()=>{l.forEach(e=>{e.removeEventListener("scroll",a)})})}const ni=Symbol.for("vuetify:v-menu"),oi=vt({closeDelay:[Number,String],openDelay:[Number,String]},"delay")
function ri(e,t){let a=()=>{}
function l(l,n){a?.()
const r=l?e.openDelay:e.closeDelay,i=Math.max(n?.minDelay??0,Number(r??0))
return new Promise(e=>{a=function(e,t){if(!o||0===e)return t(),()=>{}
const a=window.setTimeout(t,e)
return()=>window.clearTimeout(a)}(i,()=>{t?.(l),e(l)})})}return{clearDelay:a,runOpenDelay:function(){return l(!0)},runCloseDelay:function(e){return l(!1,e)}}}const ii=vt({target:[String,Object],activator:[String,Object],activatorProps:{type:Object,default:()=>({})},openOnClick:{type:Boolean,default:void 0},openOnHover:Boolean,openOnFocus:{type:Boolean,default:void 0},closeOnContentClick:Boolean,...oi()},"VOverlay-activator")
function si(e,a){let{isActive:l,isTop:n,contentEl:r}=a
const i=mt("useActivator"),s=t.ref()
let u=!1,c=!1,d=!0
const v=t.computed(()=>e.openOnFocus||null==e.openOnFocus&&e.openOnHover),p=t.computed(()=>e.openOnClick||null==e.openOnClick&&!e.openOnHover&&!v.value),{runOpenDelay:m,runCloseDelay:f}=ri(e,t=>{t!==(e.openOnHover&&u||v.value&&c)||e.openOnHover&&l.value&&!n.value||(l.value!==t&&(d=!0),l.value=t)}),g=t.ref(),h=e=>{e.stopPropagation(),s.value=e.currentTarget||e.target,l.value||(g.value=[e.clientX,e.clientY]),l.value=!l.value},y=e=>{u=!0,s.value=e.currentTarget||e.target,m()},b=e=>{u=!1,f()},V=e=>{!1!==oe(e.target,":focus-visible")&&(c=!0,e.stopPropagation(),s.value=e.currentTarget||e.target,m())},w=e=>{c=!1,e.stopPropagation(),f({minDelay:1})},k=t.computed(()=>{const t={}
return p.value&&(t.onClick=h),e.openOnHover&&(t.onMouseenter=y,t.onMouseleave=b),v.value&&(t.onFocus=V,t.onBlur=w),t}),S=t.computed(()=>{const a={}
if(e.openOnHover&&(a.onMouseenter=()=>{u=!0,m()},a.onMouseleave=()=>{u=!1,f()}),v.value&&(a.onFocusin=e=>{e.target.matches(":focus-visible")&&(c=!0,m())},a.onFocusout=()=>{c=!1,f({minDelay:1})}),e.closeOnContentClick){const e=t.inject(ni,null)
a.onClick=()=>{l.value=!1,e?.closeParents()}}return a}),x=t.computed(()=>{const t={}
return e.openOnHover&&(t.onMouseenter=()=>{d&&(u=!0,d=!1,m())},t.onMouseleave=()=>{u=!1,f()}),t})
t.watch(n,t=>{!t||(!e.openOnHover||u||v.value&&c)&&(!v.value||c||e.openOnHover&&u)||r.value?.contains(document.activeElement)||(l.value=!1)}),t.watch(l,e=>{e||setTimeout(()=>{g.value=void 0})},{flush:"post"})
const N=se()
t.watchEffect(()=>{N.value&&t.nextTick(()=>{s.value=N.el})})
const C=se(),E=t.computed(()=>"cursor"===e.target&&g.value?g.value:C.value?C.el:ui(e.target,i)||s.value),I=t.computed(()=>Array.isArray(E.value)?void 0:E.value)
let _
return t.watch(()=>!!e.activator,a=>{a&&o?(_=t.effectScope(),_.run(()=>{!function(e,a,l){let{activatorEl:n,activatorEvents:o}=l
function r(){let a=arguments.length>0&&void 0!==arguments[0]?arguments[0]:s(),l=arguments.length>1&&void 0!==arguments[1]?arguments[1]:e.activatorProps
a&&function(e,t){Object.keys(t).forEach(a=>{if(P(a)){const l=X(a),n=Ce.get(e)
if(null==t[a])n?.forEach(t=>{const[a,o]=t
a===l&&(e.removeEventListener(l,o),n.delete(t))})
else if(!n||![...n]?.some(e=>e[0]===l&&e[1]===t[a])){e.addEventListener(l,t[a])
const o=n||new Set
o.add([l,t[a]]),Ce.has(e)||Ce.set(e,o)}}else null==t[a]?e.removeAttribute(a):e.setAttribute(a,t[a])})}(a,t.mergeProps(o.value,l))}function i(){let a=arguments.length>0&&void 0!==arguments[0]?arguments[0]:s(),l=arguments.length>1&&void 0!==arguments[1]?arguments[1]:e.activatorProps
a&&function(e,t){Object.keys(t).forEach(t=>{if(P(t)){const a=X(t),l=Ce.get(e)
l?.forEach(t=>{const[n,o]=t
n===a&&(e.removeEventListener(a,o),l.delete(t))})}else e.removeAttribute(t)})}(a,t.mergeProps(o.value,l))}function s(){const t=ui(arguments.length>0&&void 0!==arguments[0]?arguments[0]:e.activator,a)
return n.value=t?.nodeType===Node.ELEMENT_NODE?t:void 0,n.value}t.watch(()=>e.activator,(e,a)=>{if(a&&e!==a){const e=s(a)
e&&i(e)}e&&t.nextTick(()=>r())},{immediate:!0}),t.watch(()=>e.activatorProps,()=>{r()}),t.onScopeDispose(()=>{i()})}(e,i,{activatorEl:s,activatorEvents:k})})):_&&_.stop()},{flush:"post",immediate:!0}),t.onScopeDispose(()=>{_?.stop()}),{activatorEl:s,activatorRef:N,target:E,targetEl:I,targetRef:C,activatorEvents:k,contentEvents:S,scrimEvents:x}}function ui(e,t){if(!e)return
let a
if("parent"===e){let e=t?.proxy?.$el?.parentNode
for(;e?.hasAttribute("data-no-activator");)e=e.parentNode
a=e}else a="string"==typeof e?document.querySelector(e):"$el"in e?e.$el:e
return a}const ci=vt({retainFocus:Boolean,captureFocus:Boolean,disableInitialFocus:Boolean},"focusTrap"),di=new Map
let vi=0
function pi(e){const t=document.activeElement
if("Tab"!==e.key||!t)return
const a=Array.from(di.values()).filter(e=>{let{isActive:a,contentEl:l}=e
return a.value&&l.value?.contains(t)}).map(e=>e.contentEl.value)
let l,n=t.parentElement
for(;n;){if(a.includes(n)){l=n
break}n=n.parentElement}if(!l)return
const o=ee(l).filter(e=>e.tabIndex>=0)
if(!o.length)return
const r=document.activeElement
if(1===o.length&&o[0].classList.contains("v-list")&&o[0].contains(r))return void e.preventDefault()
const i=o[0],s=o[o.length-1]
e.shiftKey&&(r===i||i.classList.contains("v-list")&&i.contains(r))&&(e.preventDefault(),s.focus()),!e.shiftKey&&(r===s||s.classList.contains("v-list")&&s.contains(r))&&(e.preventDefault(),i.focus())}function mi(e,a){let{isActive:l,localTop:n,activatorEl:r,contentEl:i}=a
const s=Symbol("trap")
let u=!1,c=-1
async function d(){u=!0,c=window.setTimeout(()=>{u=!1},100)}async function v(e){const a=e.relatedTarget,o=e.target
if(document.removeEventListener("pointerdown",d),document.removeEventListener("keydown",p),await t.nextTick(),l.value&&!u&&a!==o&&i.value&&t.toValue(n)&&![document,i.value].includes(o)&&!i.value.contains(o)){const e=ee(i.value)
e[0]?.focus()}}function p(e){if("Tab"===e.key&&(document.removeEventListener("keydown",p),l.value&&i.value&&e.target&&!i.value.contains(e.target))){const t=ee(document.documentElement)
if(e.shiftKey&&e.target===t.at(0)||!e.shiftKey&&e.target===t.at(-1)){const t=ee(i.value)
t.length>0&&(e.preventDefault(),t[0].focus())}}}const m=t.toRef(()=>l.value&&e.captureFocus&&!e.disableInitialFocus)
o&&(t.watch(()=>e.retainFocus,e=>{e?di.set(s,{isActive:l,contentEl:i}):di.delete(s)},{immediate:!0}),t.watch(m,e=>{e?(document.addEventListener("pointerdown",d),document.addEventListener("focusin",v,{once:!0}),document.addEventListener("keydown",p)):(document.removeEventListener("pointerdown",d),document.removeEventListener("focusin",v),document.removeEventListener("keydown",p))},{immediate:!0}),vi++<1&&document.addEventListener("keydown",pi)),t.onScopeDispose(()=>{di.delete(s),clearTimeout(c),document.removeEventListener("pointerdown",d),document.removeEventListener("focusin",v),document.removeEventListener("keydown",p),--vi<1&&document.removeEventListener("keydown",pi)})}function fi(){if(!o)return t.shallowRef(!1)
const{ssr:e}=Ro()
if(e){const e=t.shallowRef(!1)
return t.onMounted(()=>{e.value=!0}),e}return t.shallowRef(!0)}const gi=vt({eager:Boolean},"lazy")
function hi(e,a){const l=t.shallowRef(!1),n=t.toRef(()=>l.value||e.eager||a.value)
return t.watch(a,()=>l.value=!0),{isBooted:l,hasContent:n,onAfterLeave:function(){e.eager||(l.value=!1)}}}function yi(){const e=mt("useScopeId").vnode.scopeId
return{scopeId:e?{[e]:""}:void 0}}const bi=Symbol.for("vuetify:stack"),Vi=t.reactive([])
function wi(){return!0}function ki(e,t,a){if(!e||!1===Si(e,a))return!1
const l=xt(t)
if("undefined"!=typeof ShadowRoot&&l instanceof ShadowRoot&&l.host===e.target)return!1
const n=("object"==typeof a.value&&a.value.include||(()=>[]))()
return n.push(t),!n.some(t=>t?.contains(e.target))}function Si(e,t){return("object"==typeof t.value&&t.value.closeConditional||wi)(e)}function xi(e,t){const a=xt(e)
t(document),"undefined"!=typeof ShadowRoot&&a instanceof ShadowRoot&&t(a)}const Ni={mounted(e,t){const a=a=>function(e,t,a){const l="function"==typeof a.value?a.value:a.value.handler
e.shadowTarget=e.target,t._clickOutside.lastMousedownWasOutside&&ki(e,t,a)&&setTimeout(()=>{Si(e,a)&&l&&l(e)},0)}(a,e,t),l=a=>{e._clickOutside.lastMousedownWasOutside=ki(a,e,t)}
xi(e,e=>{e.addEventListener("click",a,!0),e.addEventListener("mousedown",l,!0)}),e._clickOutside||(e._clickOutside={lastMousedownWasOutside:!1}),e._clickOutside[t.instance.$.uid]={onClick:a,onMousedown:l}},beforeUnmount(e,t){e._clickOutside&&(xi(e,a=>{if(!a||!e._clickOutside?.[t.instance.$.uid])return
const{onClick:l,onMousedown:n}=e._clickOutside[t.instance.$.uid]
a.removeEventListener("click",l,!0),a.removeEventListener("mousedown",n,!0)}),delete e._clickOutside[t.instance.$.uid])}}
function Ci(e){const{modelValue:a,color:l,...n}=e
return t.createVNode(t.Transition,{name:"fade-transition",appear:!0},{default:()=>[e.modelValue&&t.createElementVNode("div",t.mergeProps({class:["v-overlay__scrim",e.color.backgroundColorClasses.value],style:e.color.backgroundColorStyles.value},n),null)]})}const Ei=vt({absolute:Boolean,attach:[Boolean,String,Object],closeOnBack:{type:Boolean,default:!0},contained:Boolean,contentClass:null,contentProps:null,disabled:Boolean,opacity:[Number,String],noClickAnimation:Boolean,modelValue:Boolean,persistent:Boolean,scrim:{type:[Boolean,String],default:!0},zIndex:{type:[Number,String],default:2e3},...ii(),...pt(),...ol(),...gi(),...Gr(),...ti(),...ci(),...ya(),...fl()},"VOverlay"),Ii=wt()({name:"VOverlay",directives:{vClickOutside:Ni},inheritAttrs:!1,props:{_disableGlobalStack:Boolean,...I(Ei(),["disableInitialFocus"])},emits:{"click:outside":e=>!0,"update:modelValue":e=>!0,keydown:e=>!0,afterEnter:()=>!0,afterLeave:()=>!0},setup(e,a){let{slots:l,attrs:n,emit:r}=a
const i=mt("VOverlay"),s=t.ref(),u=t.ref(),c=t.ref(),d=la(e,"modelValue"),v=t.computed({get:()=>d.value,set:t=>{t&&e.disabled||(d.value=t)}}),{themeClasses:p}=Ca(e),{rtlClasses:m,isRtl:f}=ga(),{hasContent:g,onAfterLeave:h}=hi(e,v),y=dl(()=>"string"==typeof e.scrim?e.scrim:null),{globalTop:V,localTop:w,stackStyles:k}=function(e,a,l){const n=mt("useStack"),o=!l,r=t.inject(bi,void 0),i=t.reactive({activeChildren:new Set})
t.provide(bi,i)
const s=t.shallowRef(Number(t.toValue(a)))
aa(e,()=>{const e=Vi.at(-1)?.[1]
s.value=e?e+10:Number(t.toValue(a)),o&&Vi.push([n.uid,s.value]),r?.activeChildren.add(n.uid),t.onScopeDispose(()=>{if(o){const e=t.toRaw(Vi).findIndex(e=>e[0]===n.uid)
Vi.splice(e,1)}r?.activeChildren.delete(n.uid)})})
const u=t.shallowRef(!0)
o&&t.watchEffect(()=>{const e=Vi.at(-1)?.[0]===n.uid
setTimeout(()=>u.value=e)})
const c=t.toRef(()=>!i.activeChildren.size)
return{globalTop:t.readonly(u),localTop:c,stackStyles:t.toRef(()=>({zIndex:s.value}))}}(v,()=>e.zIndex,e._disableGlobalStack),{activatorEl:S,activatorRef:x,target:N,targetEl:C,targetRef:E,activatorEvents:I,contentEvents:_,scrimEvents:P}=si(e,{isActive:v,isTop:w,contentEl:c}),{teleportTarget:A}=function(e){return{teleportTarget:t.computed(()=>{const a=e()
if(!0===a||!o)return
const l=!1===a?document.body:"string"==typeof a?document.querySelector(a):a
if(null==l)return void t.warn(`Unable to locate target ${a}`)
let n=[...l.children].find(e=>e.matches(".v-overlay-container"))
return n||(n=document.createElement("div"),n.className="v-overlay-container",l.appendChild(n)),n})}}(()=>{const t=e.attach||e.contained
if(t)return t
const a=S?.value?.getRootNode()||i.proxy?.$el?.getRootNode()
return a instanceof ShadowRoot&&a}),{dimensionStyles:R}=rl(e),T=fi(),{scopeId:B}=yi()
t.watch(()=>e.disabled,e=>{e&&(v.value=!1)})
const{contentStyles:D,updateLocation:F}=function(e,a){const l=t.ref({}),n=t.ref()
function r(e){n.value?.(e)}function i(e){n.value?.(e)}function s(e){n.value?.(e)}return o&&aa(()=>!(!a.isActive.value||!e.locationStrategy),o=>{t.watch(()=>e.locationStrategy,o),t.onScopeDispose(()=>{window.removeEventListener("resize",r),visualViewport?.removeEventListener("resize",i),visualViewport?.removeEventListener("scroll",s),n.value=void 0}),window.addEventListener("resize",r,{passive:!0}),visualViewport?.addEventListener("resize",i,{passive:!0}),visualViewport?.addEventListener("scroll",s,{passive:!0}),"function"==typeof e.locationStrategy?n.value=e.locationStrategy(a,e,l)?.updateLocation:n.value=Ur[e.locationStrategy](a,e,l)?.updateLocation}),{contentStyles:l,updateLocation:n}}(e,{isRtl:f,contentEl:c,target:N,isActive:v})
function $(t){r("click:outside",t),e.persistent?H():v.value=!1}function M(t){return v.value&&w.value&&(!e.scrim||t.target===u.value||t instanceof MouseEvent&&t.shadowTarget===u.value)}function z(t){"Escape"===t.key&&V.value&&(c.value?.contains(document.activeElement)||r("keydown",t),e.persistent?H():(v.value=!1,c.value?.contains(document.activeElement)&&S.value?.focus()))}function L(e){("Escape"!==e.key||V.value)&&r("keydown",e)}!function(e,a){if(!o)return
let l
t.watchEffect(async()=>{l?.stop(),a.isActive.value&&e.scrollStrategy&&(l=t.effectScope(),await new Promise(e=>setTimeout(e)),l.active&&l.run(()=>{"function"==typeof e.scrollStrategy?e.scrollStrategy(a,e,l):ei[e.scrollStrategy]?.(a,e,l)}))}),t.onScopeDispose(()=>{l?.stop()})}(e,{root:s,contentEl:c,targetEl:C,target:N,isActive:v,updateLocation:F}),mi(e,{isActive:v,localTop:w,contentEl:c,activatorEl:S}),o&&t.watch(v,e=>{e?window.addEventListener("keydown",z):window.removeEventListener("keydown",z)},{immediate:!0}),t.onBeforeUnmount(()=>{o&&window.removeEventListener("keydown",z)})
const O=gn()
aa(()=>e.closeOnBack,()=>{!function(e,a){let l,n,r=!1
function i(e){e.state?.replaced||(r=!0,setTimeout(()=>r=!1))}o&&e?.beforeEach&&(t.nextTick(()=>{window.addEventListener("popstate",i),l=e.beforeEach((e,t,l)=>{bn?r?a(l):l():setTimeout(()=>r?a(l):l()),bn=!0}),n=e?.afterEach(()=>{bn=!1})}),t.onScopeDispose(()=>{window.removeEventListener("popstate",i),l?.(),n?.()}))}(O,t=>{V.value&&v.value?(t(!1),e.persistent?H():v.value=!1):t()})})
const j=t.ref()
function H(){e.noClickAnimation||c.value&&Ne(c.value,[{transformOrigin:"center"},{transform:"scale(1.03)"},{transformOrigin:"center"}],{duration:150,easing:Nt})}function W(){r("afterEnter")}function Y(){h(),r("afterLeave")}return t.watch(()=>v.value&&(e.absolute||e.contained)&&null==A.value,e=>{if(e){const e=Pt(s.value)
e&&e!==document.scrollingElement&&(j.value=e.scrollTop)}}),Bt(()=>t.createElementVNode(t.Fragment,null,[l.activator?.({isActive:v.value,targetRef:E,props:t.mergeProps({ref:x},I.value,e.activatorProps)}),T.value&&g.value&&t.createVNode(t.Teleport,{disabled:!A.value,to:A.value},{default:()=>[t.createElementVNode("div",t.mergeProps({class:["v-overlay",{"v-overlay--absolute":e.absolute||e.contained,"v-overlay--active":v.value,"v-overlay--contained":e.contained},p.value,m.value,e.class],style:[k.value,{"--v-overlay-opacity":e.opacity,top:b(j.value)},e.style],ref:s,onKeydown:L},B,n),[t.createVNode(Ci,t.mergeProps({color:y,modelValue:v.value&&!!e.scrim,ref:u},P.value),null),t.createVNode(gl,{appear:!0,persisted:!0,transition:e.transition,target:N.value,onAfterEnter:W,onAfterLeave:Y},{default:()=>[t.withDirectives(t.createElementVNode("div",t.mergeProps({ref:c,class:["v-overlay__content",e.contentClass],style:[R.value,D.value]},_.value,e.contentProps),[l.default?.({isActive:v})]),[[t.vShow,v.value],[Ni,{handler:$,closeConditional:M,include:()=>[S.value]}]])]})])]})])),{activatorEl:S,scrimEl:u,target:N,animateClick:H,contentEl:c,rootEl:s,globalTop:V,localTop:w,updateLocation:F}}}),_i=vt({id:String,submenu:Boolean,...I(Ei({captureFocus:!0,closeDelay:250,closeOnContentClick:!0,locationStrategy:"connected",location:void 0,openDelay:300,scrim:!1,scrollStrategy:"reposition",transition:{component:za}}),["absolute"])},"VMenu"),Pi=wt()({name:"VMenu",props:_i(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=la(e,"modelValue"),{scopeId:o}=yi(),{isRtl:r}=ga(),i=t.useId(),s=t.toRef(()=>e.id||`v-menu-${i}`),u=t.ref(),c=t.inject(ni,null),d=t.shallowRef(new Set)
function v(e){c?.closeParents(e)}function p(t){if(!e.disabled)if("Tab"===t.key||"Enter"===t.key&&!e.closeOnContentClick){if("Enter"===t.key&&(t.target instanceof HTMLTextAreaElement||t.target instanceof HTMLInputElement&&t.target.closest("form")))return
"Enter"===t.key&&t.preventDefault()
te(ee(u.value?.contentEl,!1),t.shiftKey?"prev":"next",e=>e.tabIndex>=0)||e.retainFocus||(n.value=!1,u.value?.activatorEl?.focus())}else e.submenu&&t.key===(r.value?"ArrowRight":"ArrowLeft")&&(n.value=!1,u.value?.activatorEl?.focus())}function m(t){if(e.disabled)return
const a=u.value?.contentEl
a&&n.value?"ArrowDown"===t.key?(t.preventDefault(),t.stopImmediatePropagation(),ae(a,"next")):"ArrowUp"===t.key?(t.preventDefault(),t.stopImmediatePropagation(),ae(a,"prev")):e.submenu&&(t.key===(r.value?"ArrowRight":"ArrowLeft")?n.value=!1:t.key===(r.value?"ArrowLeft":"ArrowRight")&&(t.preventDefault(),ae(a,"first"))):(e.submenu?t.key===(r.value?"ArrowLeft":"ArrowRight"):["ArrowDown","ArrowUp"].includes(t.key))&&(n.value=!0,t.preventDefault(),setTimeout(()=>setTimeout(()=>m(t))))}t.provide(ni,{register(){d.value.add(i)},unregister(){d.value.delete(i)},closeParents(t){setTimeout(()=>{d.value.size||e.persistent||null!=t&&(!u.value?.contentEl||function(e,t){const a=e.clientX,l=e.clientY,n=t.getBoundingClientRect(),o=n.left,r=n.top,i=n.right,s=n.bottom
return a>=o&&a<=i&&l>=r&&l<=s}(t,u.value.contentEl))||(n.value=!1,c?.closeParents())},40)}}),t.onBeforeUnmount(()=>c?.unregister()),t.onDeactivated(()=>n.value=!1),t.watch(n,e=>{e?c?.register():c?.unregister()},{immediate:!0})
const f=t.computed(()=>t.mergeProps({"aria-haspopup":"menu","aria-expanded":String(n.value),"aria-controls":s.value,"aria-owns":s.value,onKeydown:m},e.activatorProps))
return Bt(()=>{const a=Ii.filterProps(e)
return t.createVNode(Ii,t.mergeProps({ref:u,id:s.value,class:["v-menu",e.class],style:e.style},a,{modelValue:n.value,"onUpdate:modelValue":e=>n.value=e,absolute:!0,activatorProps:f.value,location:e.location??(e.submenu?"end":"bottom"),"onClick:outside":v,onKeydown:p},o),{activator:l.activator,default:function(){for(var e=arguments.length,a=new Array(e),n=0;n<e;n++)a[n]=arguments[n]
return t.createVNode(nl,{root:"VMenu"},{default:()=>[l.default?.(...a)]})}})}),wo({id:s,ΨopenChildren:d},u)}}),Ai=vt({active:Boolean,disabled:Boolean,max:[Number,String],value:{type:[Number,String],default:0},...pt(),...fl({transition:{component:Ja}})},"VCounter"),Ri=wt()({name:"VCounter",functional:!0,props:Ai(),setup(e,a){let{slots:l}=a
const n=t.toRef(()=>e.max?`${e.value} / ${e.max}`:String(e.value))
return Bt(()=>t.createVNode(gl,{transition:e.transition},{default:()=>[t.withDirectives(t.createElementVNode("div",{class:t.normalizeClass(["v-counter",{"text-error":e.max&&!e.disabled&&parseFloat(e.value)>parseFloat(e.max)},e.class]),style:t.normalizeStyle(e.style)},[l.default?l.default({counter:n.value,max:e.max,value:e.value}):n.value]),[[t.vShow,e.active]])]})),{}}}),Ti=vt({floating:Boolean,...pt()},"VFieldLabel"),Bi=wt()({name:"VFieldLabel",props:Ti(),setup(e,a){let{slots:l}=a
return Bt(()=>t.createVNode(Xn,{class:t.normalizeClass(["v-field-label",{"v-field-label--floating":e.floating},e.class]),style:t.normalizeStyle(e.style)},l)),{}}}),Di=["underlined","outlined","filled","solo","solo-inverted","solo-filled","plain"],Fi=vt({appendInnerIcon:Dt,bgColor:String,clearable:Boolean,clearIcon:{type:Dt,default:"$clear"},active:Boolean,centerAffix:{type:Boolean,default:void 0},color:String,baseColor:String,dirty:Boolean,disabled:{type:Boolean,default:null},glow:Boolean,error:Boolean,flat:Boolean,iconColor:[Boolean,String],label:String,persistentClear:Boolean,prependInnerIcon:Dt,reverse:Boolean,singleLine:Boolean,variant:{type:String,default:"filled",validator:e=>Di.includes(e)},"onClick:clear":Z(),"onClick:appendInner":Z(),"onClick:prependInner":Z(),...pt(),...cn(),...pl(),...ya()},"VField"),$i=wt()({name:"VField",inheritAttrs:!1,props:{id:String,details:Boolean,labelId:String,...so(),...Fi()},emits:{"update:focused":e=>!0,"update:modelValue":e=>!0},setup(e,a){let{attrs:l,emit:n,slots:o}=a
const{themeClasses:r}=Ca(e),{loaderClasses:i}=dn(e),{focusClasses:s,isFocused:u,focus:d,blur:v}=uo(e),{InputIcon:p}=oo(e),{roundedClasses:m}=ml(e),{rtlClasses:f}=ga(),g=t.toRef(()=>e.dirty||e.active),h=t.toRef(()=>!(!e.label&&!o.label)),y=t.toRef(()=>!e.singleLine&&h.value),V=t.useId(),w=t.computed(()=>e.id||`input-${V}`),k=t.toRef(()=>e.details?`${w.value}-messages`:void 0),S=t.ref(),x=t.ref(),N=t.ref(),C=t.computed(()=>["plain","underlined"].includes(e.variant)),E=t.computed(()=>e.error||e.disabled?void 0:g.value&&u.value?e.color:e.baseColor),I=t.computed(()=>{if(e.iconColor&&(!e.glow||u.value))return!0===e.iconColor?E.value:e.iconColor}),{backgroundColorClasses:_,backgroundColorStyles:P}=dl(()=>e.bgColor),{textColorClasses:A,textColorStyles:R}=cl(E)
t.watch(g,e=>{if(y.value&&!c()){const t=S.value.$el,a=x.value.$el
requestAnimationFrame(()=>{const l=xe(t),n=a.getBoundingClientRect(),o=n.x-l.x,r=n.y-l.y-(l.height/2-n.height/2),i=n.width/.75,s=Math.abs(i-l.width)>1?{maxWidth:b(i)}:void 0,u=getComputedStyle(t),c=getComputedStyle(a),d=1e3*parseFloat(u.transitionDuration)||150,v=parseFloat(c.getPropertyValue("--v-field-label-scale")),p=c.getPropertyValue("color")
t.style.visibility="visible",a.style.visibility="hidden",Ne(t,{transform:`translate(${o}px, ${r}px) scale(${v})`,color:p,...s},{duration:d,easing:Nt,direction:e?"normal":"reverse"}).finished.then(()=>{t.style.removeProperty("visibility"),a.style.removeProperty("visibility")})})}},{flush:"post"})
const T=t.computed(()=>({isActive:g,isFocused:u,controlRef:N,iconColor:I,blur:v,focus:d})),B=t.toRef(()=>{const e=!g.value
return{"aria-hidden":e,for:e?void 0:w.value}}),D=t.toRef(()=>{const e=y.value&&g.value
return{"aria-hidden":e,for:e?void 0:w.value}})
function F(e){e.target!==document.activeElement&&e.preventDefault()}return Bt(()=>{const a="outlined"===e.variant,n=!(!o["prepend-inner"]&&!e.prependInnerIcon),u=!(!e.clearable&&!o.clear||e.disabled),c=!!(o["append-inner"]||e.appendInnerIcon||u),b=()=>o.label?o.label({...T.value,label:e.label,props:{for:w.value}}):e.label
return t.createElementVNode("div",t.mergeProps({class:["v-field",{"v-field--active":g.value,"v-field--appended":c,"v-field--center-affix":e.centerAffix??!C.value,"v-field--disabled":e.disabled,"v-field--dirty":e.dirty,"v-field--error":e.error,"v-field--glow":e.glow,"v-field--flat":e.flat,"v-field--has-background":!!e.bgColor,"v-field--persistent-clear":e.persistentClear,"v-field--prepended":n,"v-field--reverse":e.reverse,"v-field--single-line":e.singleLine,"v-field--no-label":!b(),[`v-field--variant-${e.variant}`]:!0},r.value,_.value,s.value,i.value,m.value,f.value,e.class],style:[P.value,e.style],onClick:F},l),[t.createElementVNode("div",{class:"v-field__overlay"},null),t.createVNode(vn,{name:"v-field",active:!!e.loading,color:e.error?"error":"string"==typeof e.loading?e.loading:e.color},{default:o.loader}),n&&t.createElementVNode("div",{key:"prepend",class:"v-field__prepend-inner"},[o["prepend-inner"]?o["prepend-inner"](T.value):e.prependInnerIcon&&t.createVNode(p,{key:"prepend-icon",name:"prependInner",color:I.value},null)]),t.createElementVNode("div",{class:"v-field__field","data-no-activator":""},[["filled","solo","solo-inverted","solo-filled"].includes(e.variant)&&y.value&&t.createVNode(Bi,t.mergeProps({key:"floating-label",ref:x,class:[A.value],floating:!0},B.value,{style:R.value}),{default:()=>[b()]}),h.value&&t.createVNode(Bi,t.mergeProps({key:"label",ref:S,id:e.labelId},D.value),{default:()=>[b()]}),o.default?.({...T.value,props:{id:w.value,class:"v-field__input","aria-describedby":k.value},focus:d,blur:v})??t.createElementVNode("div",{id:w.value,class:"v-field__input","aria-describedby":k.value},null)]),u&&t.createVNode(al,{key:"clear"},{default:()=>[t.withDirectives(t.createElementVNode("div",{class:"v-field__clearable",onMousedown:e=>{e.preventDefault(),e.stopPropagation()}},[t.createVNode(nl,{defaults:{VIcon:{icon:e.clearIcon}}},{default:()=>[o.clear?o.clear({...T.value,props:{onFocus:d,onBlur:v,onClick:e["onClick:clear"],tabindex:-1}}):t.createVNode(p,{name:"clear",onFocus:d,onBlur:v,tabindex:-1},null)]})]),[[t.vShow,e.dirty]])]}),c&&t.createElementVNode("div",{key:"append",class:"v-field__append-inner"},[o["append-inner"]?o["append-inner"](T.value):e.appendInnerIcon&&t.createVNode(p,{key:"append-icon",name:"appendInner",color:I.value},null)]),t.createElementVNode("div",{class:t.normalizeClass(["v-field__outline",A.value]),style:t.normalizeStyle(R.value)},[a&&t.createElementVNode(t.Fragment,null,[t.createElementVNode("div",{class:"v-field__outline__start"},null),y.value&&t.createElementVNode("div",{class:"v-field__outline__notch"},[t.createVNode(Bi,t.mergeProps({ref:x,floating:!0},B.value),{default:()=>[b()]})]),t.createElementVNode("div",{class:"v-field__outline__end"},null)]),C.value&&y.value&&t.createVNode(Bi,t.mergeProps({ref:x,floating:!0},B.value),{default:()=>[b()]})])])}),{controlRef:N,fieldIconColor:I}}}),Mi=vt({autocomplete:String},"autocomplete")
function zi(e){const a=t.useId(),l=t.shallowRef(0),n=t.toRef(()=>"suppress"===e.autocomplete),o=t.toRef(()=>{if(e.name)return n.value?`${e.name}-${a}-${l.value}`:e.name}),r=t.toRef(()=>n.value?"off":e.autocomplete)
return{isSuppressing:n,fieldAutocomplete:r,fieldName:o,update:()=>l.value=(new Date).getTime()}}function Li(e){return{onIntersect:function(t,a){if(!e.autofocus||!t)return
const l=a[0].target,n=l.matches("input,textarea")?l:l.querySelector("input,textarea")
n?.focus()}}}const Oi=["color","file","time","date","datetime-local","week","month"],ji=vt({autofocus:Boolean,counter:[Boolean,Number,String],counterValue:[Number,Function],prefix:String,placeholder:String,persistentPlaceholder:Boolean,persistentCounter:Boolean,suffix:String,role:String,type:{type:String,default:"text"},modelModifiers:Object,...Mi(),...I(ho(),["direction"]),...Fi()},"VTextField"),Hi=wt()({name:"VTextField",directives:{vIntersect:yl},inheritAttrs:!1,props:ji(),emits:{"click:control":e=>!0,"mousedown:control":e=>!0,"update:focused":e=>!0,"update:modelValue":e=>!0},setup(e,a){let{attrs:l,emit:n,slots:o}=a
const r=la(e,"modelValue"),{isFocused:i,focus:s,blur:u}=uo(e),{onIntersect:c}=Li(e),d=t.computed(()=>"function"==typeof e.counterValue?e.counterValue(r.value):"number"==typeof e.counterValue?e.counterValue:(r.value??"").toString().length),v=t.computed(()=>l.maxlength?l.maxlength:!e.counter||"number"!=typeof e.counter&&"string"!=typeof e.counter?void 0:e.counter),p=t.computed(()=>["plain","underlined"].includes(e.variant)),m=t.ref(),f=t.ref(),g=t.ref(),h=zi(e),y=t.computed(()=>Oi.includes(e.type)||e.persistentPlaceholder||i.value||e.active)
function b(){h.isSuppressing.value&&h.update(),i.value||s(),t.nextTick(()=>{g.value!==document.activeElement&&g.value?.focus()})}function V(e){n("mousedown:control",e),e.target!==g.value&&(b(),e.preventDefault())}function w(e){n("click:control",e)}function k(a){const l=a.target
if(!e.modelModifiers?.trim||!["text","search","password","tel","url"].includes(e.type))return void(r.value=l.value)
const n=l.value,o=l.selectionStart,i=l.selectionEnd
r.value=n,t.nextTick(()=>{let e=0
n.trimStart().length===l.value.length&&(e=n.length-l.value.length),null!=o&&(l.selectionStart=o-e),null!=i&&(l.selectionEnd=i-e)})}return Bt(()=>{const a=!!(o.counter||!1!==e.counter&&null!=e.counter),n=!(!a&&!o.details),[S,x]=T(l),{modelValue:N,...C}=yo.filterProps(e),E=$i.filterProps(e)
return t.createVNode(yo,t.mergeProps({ref:m,modelValue:r.value,"onUpdate:modelValue":e=>r.value=e,class:["v-text-field",{"v-text-field--prefixed":e.prefix,"v-text-field--suffixed":e.suffix,"v-input--plain-underlined":p.value},e.class],style:e.style},S,C,{centerAffix:!p.value,focused:i.value}),{...o,default:a=>{let{id:l,isDisabled:n,isDirty:d,isReadonly:v,isValid:p,hasDetails:m,reset:S}=a
return t.createVNode($i,t.mergeProps({ref:f,onMousedown:V,onClick:w,"onClick:clear":a=>function(a,l){a.stopPropagation(),b(),t.nextTick(()=>{l(),J(e["onClick:clear"],a)})}(a,S),role:e.role},I(E,["onClick:clear"]),{id:l.value,labelId:`${l.value}-label`,active:y.value||d.value,dirty:d.value||e.dirty,disabled:n.value,focused:i.value,details:m.value,error:!1===p.value}),{...o,default:a=>{let{props:{class:i,...d},controlRef:p}=a
const m=t.createElementVNode("input",t.mergeProps({ref:e=>g.value=p.value=e,value:r.value,onInput:k,autofocus:e.autofocus,readonly:v.value,disabled:n.value,name:h.fieldName.value,autocomplete:h.fieldAutocomplete.value,placeholder:e.placeholder,size:1,role:e.role,type:e.type,onFocus:s,onBlur:u,"aria-labelledby":`${l.value}-label`},d,x),null)
return t.createElementVNode(t.Fragment,null,[e.prefix&&t.createElementVNode("span",{class:"v-text-field__prefix"},[t.createElementVNode("span",{class:"v-text-field__prefix__text"},[e.prefix])]),t.withDirectives(o.default?t.createElementVNode("div",{class:t.normalizeClass(i),"data-no-activator":""},[o.default({id:l}),m]):t.cloneVNode(m,{class:i}),[[yl,c,null,{once:!0}]]),e.suffix&&t.createElementVNode("span",{class:"v-text-field__suffix"},[t.createElementVNode("span",{class:"v-text-field__suffix__text"},[e.suffix])])])}})},details:n?l=>t.createElementVNode(t.Fragment,null,[o.details?.(l),a&&t.createElementVNode(t.Fragment,null,[t.createElementVNode("span",null,null),t.createVNode(Ri,{active:e.persistentCounter||i.value,value:d.value,max:v.value,disabled:e.disabled},o.counter)])]):void 0})}),wo({},m,f,g)}}),Wi=vt({renderless:Boolean,...pt()},"VVirtualScrollItem"),Yi=wt()({name:"VVirtualScrollItem",inheritAttrs:!1,props:Wi(),emits:{"update:height":e=>!0},setup(e,a){let{attrs:l,emit:n,slots:o}=a
const{resizeRef:r,contentRect:i}=Kt(void 0,"border")
t.watch(()=>i.value?.height,e=>{null!=e&&n("update:height",e)}),Bt(()=>e.renderless?t.createElementVNode(t.Fragment,null,[o.default?.({itemRef:r})]):t.createElementVNode("div",t.mergeProps({ref:r,class:["v-virtual-scroll__item",e.class],style:e.style},l),[o.default?.()]))}}),Ui=vt({itemHeight:{type:[Number,String],default:null},itemKey:{type:[String,Array,Function],default:null},height:[Number,String]},"virtual")
function Gi(e,a){const l=Ro(),n=t.shallowRef(0)
t.watchEffect(()=>{n.value=parseFloat(e.itemHeight||0)})
const r=t.shallowRef(0),i=t.shallowRef(Math.ceil((parseInt(e.height)||l.height.value)/(n.value||16))||1),s=t.shallowRef(0),u=t.shallowRef(0),c=t.ref(),d=t.ref()
let v=0
const{resizeRef:p,contentRect:m}=Kt()
t.watchEffect(()=>{p.value=c.value})
const f=t.computed(()=>c.value===document.documentElement?l.height.value:m.value?.height||parseInt(e.height)||0),g=t.computed(()=>!!(c.value&&d.value&&f.value&&n.value))
let y=Array.from({length:a.value.length}),b=Array.from({length:a.value.length})
const V=t.shallowRef(0)
let w=-1
function k(e){return y[e]||n.value}const S=D(()=>{const e=performance.now()
b[0]=0
const t=a.value.length
for(let e=1;e<=t;e++)b[e]=(b[e-1]||0)+k(e-1)
V.value=Math.max(V.value,performance.now()-e)},V),x=t.watch(g,e=>{e&&(x(),v=d.value.offsetTop,S.immediate(),T(),~w&&t.nextTick(()=>{o&&window.requestAnimationFrame(()=>{$(w),w=-1})}))})
function N(e){e=F(e,0,a.value.length)
const t=Math.floor(e),l=e%1,n=t+1,o=b[t]||0
return o+((b[n]||o)-o)*l}function C(e){return function(e,t){let a=e.length-1,l=0,n=0,o=null,r=-1
if(e[a]<t)return a
for(;l<=a;)if(n=l+a>>1,o=e[n],o>t)a=n-1
else{if(!(o<t))return o===t?n:l
r=n,l=n+1}return r}(b,e)}t.onScopeDispose(()=>{S.clear()})
let E=0,I=0,_=0
t.watch(f,(e,t)=>{T(),e<t&&requestAnimationFrame(()=>{I=0,T()})})
let P=-1
function A(){c.value&&d.value&&(I=0,_=0,window.clearTimeout(P),T())}let R=-1
function T(){cancelAnimationFrame(R),R=requestAnimationFrame(B)}function B(){if(!c.value||!f.value||!n.value)return
const e=E-v,t=Math.sign(I),l=F(C(Math.max(0,e-100)),0,a.value.length),o=F(C(e+f.value+100)+1,l+1,a.value.length)
if((-1!==t||l<r.value)&&(1!==t||o>i.value)){const e=N(r.value)-N(l),t=N(o)-N(i.value)
Math.max(e,t)>100?(r.value=l,i.value=o):(l<=0&&(r.value=l),o>=a.value.length&&(i.value=o))}s.value=N(r.value),u.value=N(a.value.length)-N(i.value)}function $(e){const t=N(e)
!c.value||e&&!t?w=e:c.value.scrollTop=t}const M=t.computed(()=>a.value.slice(r.value,i.value).map((t,a)=>{const l=a+r.value
return{raw:t,index:l,key:h(t,e.itemKey,l)}}))
return t.watch(a,()=>{y=Array.from({length:a.value.length}),b=Array.from({length:a.value.length}),S.immediate(),T()},{deep:1}),{calculateVisibleItems:T,containerRef:c,markerRef:d,computedItems:M,paddingTop:s,paddingBottom:u,scrollToIndex:$,handleScroll:function(){if(!c.value||!d.value)return
const e=c.value.scrollTop,t=performance.now()
t-_>500?(I=Math.sign(e-E),v=d.value.offsetTop):I=e-E,E=e,_=t,window.clearTimeout(P),P=window.setTimeout(A,500),T()},handleScrollend:A,handleItemResize:function(e,t){const a=y[e],l=n.value
n.value=l?Math.min(n.value,t):t,a===t&&l===n.value||(y[e]=t,S())}}}const Ki=vt({items:{type:Array,default:()=>[]},renderless:Boolean,...Ui(),...pt(),...ol()},"VVirtualScroll"),qi=wt()({name:"VVirtualScroll",props:Ki(),setup(e,a){let{slots:l}=a
const n=mt("VVirtualScroll"),{dimensionStyles:o}=rl(e),{calculateVisibleItems:r,containerRef:i,markerRef:s,handleScroll:u,handleScrollend:c,handleItemResize:d,scrollToIndex:v,paddingTop:p,paddingBottom:m,computedItems:f}=Gi(e,t.toRef(()=>e.items))
return aa(()=>e.renderless,()=>{function e(){const e=arguments.length>0&&void 0!==arguments[0]&&arguments[0]?"addEventListener":"removeEventListener"
i.value===document.documentElement?(document[e]("scroll",u,{passive:!0}),document[e]("scrollend",c)):(i.value?.[e]("scroll",u,{passive:!0}),i.value?.[e]("scrollend",c))}t.onMounted(()=>{i.value=Pt(n.vnode.el,!0),e(!0)}),t.onScopeDispose(e)}),Bt(()=>{const a=f.value.map(a=>t.createVNode(Yi,{key:a.key,renderless:e.renderless,"onUpdate:height":e=>d(a.index,e)},{default:e=>l.default?.({item:a.raw,index:a.index,...e})}))
return e.renderless?t.createElementVNode(t.Fragment,null,[t.createElementVNode("div",{ref:s,class:"v-virtual-scroll__spacer",style:{paddingTop:b(p.value)}},null),a,t.createElementVNode("div",{class:"v-virtual-scroll__spacer",style:{paddingBottom:b(m.value)}},null)]):t.createElementVNode("div",{ref:i,class:t.normalizeClass(["v-virtual-scroll",e.class]),onScrollPassive:u,onScrollend:c,style:t.normalizeStyle([o.value,e.style])},[t.createElementVNode("div",{ref:s,class:"v-virtual-scroll__container",style:{paddingTop:b(p.value),paddingBottom:b(m.value)}},[a])])}),{calculateVisibleItems:r,scrollToIndex:v}}})
function Xi(e,a){const l=t.shallowRef(!1)
let n
return{onScrollPassive:function(e){cancelAnimationFrame(n),l.value=!0,n=requestAnimationFrame(()=>{n=requestAnimationFrame(()=>{l.value=!1})})},onKeydown:async function(n){if("Tab"===n.key&&a.value?.focus(),!["PageDown","PageUp","Home","End"].includes(n.key))return
const o=e.value?.$el
if(!o)return
"Home"!==n.key&&"End"!==n.key||o.scrollTo({top:"Home"===n.key?0:o.scrollHeight,behavior:"smooth"}),await async function(){await new Promise(e=>requestAnimationFrame(e)),await new Promise(e=>requestAnimationFrame(e)),await new Promise(e=>requestAnimationFrame(e)),await new Promise(e=>{if(l.value){const a=t.watch(l,()=>{a(),e()})}else e()})}()
const r=o.querySelectorAll(":scope > :not(.v-virtual-scroll__spacer)")
if("PageDown"===n.key||"Home"===n.key){const e=o.getBoundingClientRect().top
for(const t of r)if(t.getBoundingClientRect().top>=e){t.focus()
break}}else{const e=o.getBoundingClientRect().bottom
for(const t of[...r].reverse())if(t.getBoundingClientRect().bottom<=e){t.focus()
break}}}}}const Zi=vt({closeText:{type:String,default:"$vuetify.close"},openText:{type:String,default:"$vuetify.open"}},"autocomplete")
function Qi(e,a){const l=t.useId(),n=t.computed(()=>`menu-${l}`),o=t.toRef(()=>t.toValue(a)),r=t.toRef(()=>n.value)
return{menuId:n,ariaExpanded:o,ariaControls:r}}const Ji=vt({chips:Boolean,closableChips:Boolean,eager:Boolean,hideNoData:Boolean,hideSelected:Boolean,listProps:{type:Object},menu:Boolean,menuIcon:{type:Dt,default:"$dropdown"},menuProps:{type:Object},multiple:Boolean,noDataText:{type:String,default:"$vuetify.noDataText"},openOnClear:Boolean,itemColor:String,noAutoScroll:Boolean,...Zi(),...Ir({itemChildren:!1})},"Select"),es=vt({...Ji(),...I(ji({modelValue:null,role:"combobox"}),["validationValue","dirty"]),...fl({transition:{component:za}})},"VSelect"),ts=wt()({name:"VSelect",props:es(),emits:{"update:focused":e=>!0,"update:modelValue":e=>!0,"update:menu":e=>!0},setup(e,a){let{slots:l}=a
const{t:n}=ma(),r=t.ref(),i=t.ref(),s=t.ref(),{items:u,transformIn:c,transformOut:d}=Rr(e),v=la(e,"modelValue",[],e=>c(null===e?[null]:B(e)),t=>{const a=d(t)
return e.multiple?a:a[0]??null}),p=t.computed(()=>"function"==typeof e.counterValue?e.counterValue(v.value):"number"==typeof e.counterValue?e.counterValue:v.value.length),m=po(e),f=zi(e),g=t.computed(()=>v.value.map(e=>e.value)),h=t.shallowRef(!1),y=t.toRef(()=>e.closableChips&&!m.isReadonly.value&&!m.isDisabled.value),{InputIcon:b}=oo(e)
let V,w="",k=0
const S=t.computed(()=>e.hideSelected?u.value.filter(t=>!v.value.some(a=>(e.valueComparator||St)(a,t))):u.value),x=t.computed(()=>e.hideNoData&&!S.value.length||m.isReadonly.value||m.isDisabled.value),N=la(e,"menu"),C=t.computed({get:()=>N.value,set:e=>{N.value&&!e&&i.value?.ΨopenChildren.size||e&&x.value||(N.value=e)}}),{menuId:E,ariaExpanded:I,ariaControls:_}=Qi(0,C),P=t.computed(()=>({...e.menuProps,activatorProps:{...e.menuProps?.activatorProps||{},"aria-haspopup":"listbox"}})),A=t.ref(),R=Xi(A,r)
function T(t){e.openOnClear&&(C.value=!0)}function D(){x.value||(C.value=!C.value)}function F(e){ue(e)&&$(e)}function $(t){if(!t.key||m.isReadonly.value)return
if(["Enter"," ","ArrowDown","ArrowUp","Home","End"].includes(t.key)&&t.preventDefault(),["Enter","ArrowDown"," "].includes(t.key)&&(C.value=!0),["Escape","Tab"].includes(t.key)&&(C.value=!1),e.clearable&&"Backspace"===t.key)return t.preventDefault(),v.value=[],void T()
"Home"===t.key?A.value?.focus("first"):"End"===t.key&&A.value?.focus("last")
if(!ue(t))return
const a=performance.now()
a-V>1e3&&(w="",k=0),w+=t.key.toLowerCase(),V=a
const l=S.value
function n(){for(let e=k;e<l.length;e++){const t=l[e]
if(t.title.toLowerCase().startsWith(w))return[t,e]}}const o=function(){let e=n()
return e||(w.at(-1)===w.at(-2)&&(w=w.slice(0,-1),k++,e=n(),e)?e:(k=0,e=n(),e||(w=t.key.toLowerCase(),n())))}()
if(!o)return
const[r,i]=o
k=i,A.value?.focus(i),e.multiple||(v.value=[r])}function M(a){let l=!(arguments.length>1&&void 0!==arguments[1])||arguments[1]
if(!a.props.disabled)if(e.multiple){const t=v.value.findIndex(t=>(e.valueComparator||St)(t.value,a.value)),n=null==l?!~t:l
if(~t){const e=n?[...v.value,a]:[...v.value]
e.splice(t,1),v.value=e}else n&&(v.value=[...v.value,a])}else{const e=!1!==l
v.value=e?[a]:[],t.nextTick(()=>{C.value=!1})}}function z(e){A.value?.$el.contains(e.relatedTarget)||(C.value=!1)}function L(){e.eager&&s.value?.calculateVisibleItems()}function O(){h.value&&r.value?.focus()}function j(e){h.value=!0}function H(e){if(null==e)v.value=[]
else if(oe(r.value,":autofill")||oe(r.value,":-webkit-autofill")){const t=u.value.find(t=>t.title===e)
t&&M(t)}else r.value&&(r.value.value="")}return t.watch(C,()=>{if(!e.hideSelected&&C.value&&v.value.length){const t=S.value.findIndex(t=>v.value.some(a=>(e.valueComparator||St)(a.value,t.value)))
o&&!e.noAutoScroll&&window.requestAnimationFrame(()=>{t>=0&&s.value?.scrollToIndex(t)})}}),t.watch(u,(t,a)=>{C.value||h.value&&e.hideNoData&&!a.length&&t.length&&(C.value=!0)}),Bt(()=>{const a=!(!e.chips&&!l.chip),o=!!(!e.hideNoData||S.value.length||l["prepend-item"]||l["append-item"]||l["no-data"]),c=v.value.length>0,d=Hi.filterProps(e),m=c||!h.value&&e.label&&!e.persistentPlaceholder?void 0:e.placeholder
return t.createVNode(Hi,t.mergeProps({ref:r},d,{modelValue:v.value.map(e=>e.props.title).join(", "),name:void 0,"onUpdate:modelValue":H,focused:h.value,"onUpdate:focused":e=>h.value=e,validationValue:v.externalValue,counterValue:p.value,dirty:c,class:["v-select",{"v-select--active-menu":C.value,"v-select--chips":!!e.chips,["v-select--"+(e.multiple?"multiple":"single")]:!0,"v-select--selected":v.value.length,"v-select--selection-slot":!!l.selection},e.class],style:e.style,inputmode:"none",placeholder:m,"onClick:clear":T,"onMousedown:control":D,onBlur:z,onKeydown:$,"aria-expanded":I.value,"aria-controls":_.value}),{...l,default:r=>{let{id:c}=r
return t.createElementVNode(t.Fragment,null,[t.createElementVNode("select",{hidden:!0,multiple:e.multiple,name:f.fieldName.value},[u.value.map(e=>t.createElementVNode("option",{key:e.value,value:e.value,selected:g.value.includes(e.value)},null))]),t.createVNode(Pi,t.mergeProps({id:E.value,ref:i,modelValue:C.value,"onUpdate:modelValue":e=>C.value=e,activator:"parent",contentClass:"v-select__content",disabled:x.value,eager:e.eager,maxHeight:310,openOnClick:!1,closeOnContentClick:!1,transition:e.transition,onAfterEnter:L,onAfterLeave:O},P.value),{default:()=>[o&&t.createVNode(Mr,t.mergeProps({ref:A,selected:g.value,selectStrategy:e.multiple?"independent":"single-independent",onMousedown:e=>e.preventDefault(),onKeydown:F,onFocusin:j,tabindex:"-1",selectable:!!S.value.length,"aria-live":"polite","aria-labelledby":`${c.value}-label`,"aria-multiselectable":e.multiple,color:e.itemColor??e.color},R,e.listProps),{default:()=>[l["prepend-item"]?.(),!S.value.length&&!e.hideNoData&&(l["no-data"]?.()??t.createVNode(Sr,{key:"no-data",title:n(e.noDataText)},null)),t.createVNode(qi,{ref:s,renderless:!0,items:S.value,itemKey:"value"},{default:a=>{let{item:n,index:o,itemRef:r}=a
const i=function(e){const a={}
for(const l in e)a[t.camelize(l)]=e[l]
return a}(n.props),s=t.mergeProps(n.props,{ref:r,key:n.value,onClick:()=>M(n,null),"aria-posinset":o+1,"aria-setsize":S.value.length})
return"divider"===n.type?l.divider?.({props:n.raw,index:o})??t.createVNode(Jo,t.mergeProps(n.props,{key:`divider-${o}`}),null):"subheader"===n.type?l.subheader?.({props:n.raw,index:o})??t.createVNode(Nr,t.mergeProps(n.props,{key:`subheader-${o}`}),null):l.item?.({item:n,index:o,props:s})??t.createVNode(Sr,t.mergeProps(s,{role:"option"}),{prepend:a=>{let{isSelected:l}=a
return t.createElementVNode(t.Fragment,null,[e.multiple&&!e.hideSelected?t.createVNode(no,{key:n.value,modelValue:l,ripple:!1,tabindex:"-1","aria-hidden":!0,onClick:e=>e.preventDefault()},null):void 0,i.prependAvatar&&t.createVNode(Kn,{image:i.prependAvatar},null),i.prependIcon&&t.createVNode(Jl,{icon:i.prependIcon},null)])}})}}),l["append-item"]?.()]})]}),v.value.map((n,o)=>{function r(e){e.stopPropagation(),e.preventDefault(),M(n,!1)}const i=t.mergeProps(Xo.filterProps(n.props),{"onClick:close":r,onKeydown(e){"Enter"!==e.key&&" "!==e.key||(e.preventDefault(),e.stopPropagation(),r(e))},onMousedown(e){e.preventDefault(),e.stopPropagation()},modelValue:!0,"onUpdate:modelValue":void 0}),s=a?!!l.chip:!!l.selection,u=s?re(a?l.chip({item:n,index:o,props:i}):l.selection({item:n,index:o})):void 0
if(!s||u)return t.createElementVNode("div",{key:n.value,class:"v-select__selection"},[a?l.chip?t.createVNode(nl,{key:"chip-defaults",defaults:{VChip:{closable:y.value,size:"small",text:n.title}}},{default:()=>[u]}):t.createVNode(Xo,t.mergeProps({key:"chip",closable:y.value,size:"small",text:n.title,disabled:n.props.disabled},i),null):u??t.createElementVNode("span",{class:"v-select__selection-text"},[n.title,e.multiple&&o<v.value.length-1&&t.createElementVNode("span",{class:"v-select__selection-comma"},[t.createTextVNode(",")])])])})])},"append-inner":function(){for(var a=arguments.length,n=new Array(a),o=0;o<a;o++)n[o]=arguments[o]
return t.createElementVNode(t.Fragment,null,[l["append-inner"]?.(...n),e.menuIcon?t.createVNode(Jl,{class:"v-select__menu-icon",color:r.value?.fieldIconColor,icon:e.menuIcon,"aria-hidden":!0},null):void 0,e.appendInnerIcon&&t.createVNode(b,{key:"append-icon",name:"appendInner",color:n[0].iconColor.value},null)])}})}),wo({isFocused:h,menu:C,select:M},r)}}),as=(e,t,a)=>{if(null==e||null==t)return-1
if(!t.length)return 0
e=e.toString().toLocaleLowerCase(),t=t.toString().toLocaleLowerCase()
const l=[]
let n=e.indexOf(t)
for(;~n;)l.push([n,n+t.length]),n=e.indexOf(t,n+t.length)
return l.length?l:-1}
function ls(e,t){if(null!=e&&"boolean"!=typeof e&&-1!==e)return"number"==typeof e?[[e,e+t.length]]:Array.isArray(e[0])?e:[e]}const ns=vt({customFilter:Function,customKeyFilter:Object,filterKeys:[Array,String],filterMode:{type:String,default:"intersection"},noFilter:Boolean},"filter")
function os(e,a,l,n){const o=t.shallowRef([]),r=t.shallowRef(new Map),i=t.computed(()=>n?.transform?t.unref(a).map(e=>[e,n.transform(e)]):t.unref(a))
return t.watchEffect(()=>{const s="function"==typeof l?l():t.unref(l),u="string"!=typeof s&&"number"!=typeof s?"":String(s),c=function(e,t,a){const l=[],n=a?.default??as,o=!!a?.filterKeys&&B(a.filterKeys),r=Object.keys(a?.customKeyFilter??{}).length
if(!e?.length)return l
let i=null
e:for(let s=0;s<e.length;s++){const[u,c=u]=B(e[s]),d={},v={}
let p=-1
if((t||r>0)&&!a?.noFilter){let e=!1
if("object"==typeof u){if("divider"===u.type||"subheader"===u.type){"divider"===i?.type&&"subheader"===u.type&&l.push(i),i={index:s,matches:{},type:u.type}
continue}const m=o||Object.keys(c)
e=m.length===r
for(const e of m){const l=h(c,e),o=a?.customKeyFilter?.[e]
if(p=o?o(l,t,u):n(l,t,u),-1!==p&&!1!==p)o?d[e]=ls(p,t):v[e]=ls(p,t)
else if("every"===a?.filterMode)continue e}}else p=n(u,t,u),-1!==p&&!1!==p&&(v.title=ls(p,t))
const m=Object.keys(v).length,f=Object.keys(d).length
if(!m&&!f)continue
if("union"===a?.filterMode&&f!==r&&!m)continue
if("intersection"===a?.filterMode&&(f!==r||!m&&r>0&&!e))continue}i&&(l.push(i),i=null),l.push({index:s,matches:{...v,...d}})}return l}(i.value,u,{customKeyFilter:{...e.customKeyFilter,...t.unref(n?.customKeyFilter)},default:e.customFilter,filterKeys:e.filterKeys,filterMode:e.filterMode,noFilter:e.noFilter}),d=t.unref(a),v=[],p=new Map
c.forEach(e=>{let{index:t,matches:a}=e
const l=d[t]
v.push(l),p.set(l.value,a)}),o.value=v,r.value=p}),{filteredItems:o,filteredMatches:r,getMatches:function(e){return r.value.get(e.value)}}}function rs(e,a,l){return null!=l&&l.length?l.map((n,o)=>{const r=0===o?0:l[o-1][1],i=[t.createElementVNode("span",{class:t.normalizeClass(`${e}__unmask`)},[a.slice(r,n[0])]),t.createElementVNode("span",{class:t.normalizeClass(`${e}__mask`)},[a.slice(n[0],n[1])])]
return o===l.length-1&&i.push(t.createElementVNode("span",{class:t.normalizeClass(`${e}__unmask`)},[a.slice(n[1])])),t.createElementVNode(t.Fragment,null,[i])}):a}const is=vt({autoSelectFirst:{type:[Boolean,String]},clearOnSelect:Boolean,search:String,...ns({filterKeys:["title"]}),...Ji(),...I(ji({modelValue:null,role:"combobox"}),["validationValue","dirty"])},"VAutocomplete"),ss=wt()({name:"VAutocomplete",props:is(),emits:{"update:focused":e=>!0,"update:search":e=>!0,"update:modelValue":e=>!0,"update:menu":e=>!0},setup(e,a){let{slots:l}=a
const{t:n}=ma(),r=t.ref(),i=t.shallowRef(!1),s=t.shallowRef(!0),u=t.shallowRef(!1),c=t.ref(),d=t.ref(),v=t.shallowRef(-1),p=t.shallowRef(null),{items:m,transformIn:f,transformOut:g}=Rr(e),{textColorClasses:h,textColorStyles:y}=cl(()=>r.value?.color),{InputIcon:b}=oo(e),V=la(e,"search",""),w=la(e,"modelValue",[],e=>f(null===e?[null]:B(e)),t=>{const a=g(t)
return e.multiple?a:a[0]??null}),k=t.computed(()=>"function"==typeof e.counterValue?e.counterValue(w.value):"number"==typeof e.counterValue?e.counterValue:w.value.length),S=po(e),{filteredItems:x,getMatches:N}=os(e,m,()=>p.value??(s.value?"":V.value)),C=t.computed(()=>e.hideSelected&&null===p.value?x.value.filter(e=>!w.value.some(t=>t.value===e.value)):x.value),E=t.toRef(()=>e.closableChips&&!S.isReadonly.value&&!S.isDisabled.value),I=t.computed(()=>!(!e.chips&&!l.chip)),_=t.computed(()=>I.value||!!l.selection),P=t.computed(()=>w.value.map(e=>e.props.value)),A=t.computed(()=>C.value.find(e=>"item"===e.type&&!e.props.disabled)),R=t.computed(()=>(!0===e.autoSelectFirst||"exact"===e.autoSelectFirst&&V.value===A.value?.title)&&C.value.length>0&&!s.value&&!u.value),T=t.computed(()=>e.hideNoData&&!C.value.length||S.isReadonly.value||S.isDisabled.value),D=la(e,"menu"),F=t.computed({get:()=>D.value,set:e=>{D.value&&!e&&c.value?.ΨopenChildren.size||e&&T.value||(D.value=e)}}),{menuId:$,ariaExpanded:M,ariaControls:z}=Qi(0,F),L=t.ref(),O=Xi(L,r)
function j(t){e.openOnClear&&(F.value=!0),V.value=""}function H(){T.value||(F.value=!0)}function W(e){T.value||(i.value&&(e.preventDefault(),e.stopPropagation()),F.value=!F.value)}function Y(e){(ue(e)||"Backspace"===e.key)&&r.value?.focus()}function U(t){if(S.isReadonly.value)return
const a=r.value?.selectionStart,l=w.value.length
if(["Enter","ArrowDown","ArrowUp"].includes(t.key)&&t.preventDefault(),["Enter","ArrowDown"].includes(t.key)&&(F.value=!0),["Escape"].includes(t.key)&&(F.value=!1),R.value&&["Enter","Tab"].includes(t.key)&&A.value&&!w.value.some(e=>{let{value:t}=e
return t===A.value.value})&&ee(A.value),"ArrowDown"===t.key&&R.value&&L.value?.focus("next"),["Backspace","Delete"].includes(t.key)){if(!e.multiple&&_.value&&w.value.length>0&&!V.value)return ee(w.value[0],!1)
if(~v.value){t.preventDefault()
const e=v.value
ee(w.value[v.value],!1),v.value=e>=l-1?l-2:e}else"Backspace"!==t.key||V.value||(v.value=l-1)}else if(e.multiple)if("ArrowLeft"===t.key){if(v.value<0&&a&&a>0)return
const e=v.value>-1?v.value-1:l-1
if(w.value[e])v.value=e
else{const e=V.value?.length??null
v.value=-1,r.value?.setSelectionRange(e,e)}}else if("ArrowRight"===t.key){if(v.value<0)return
const e=v.value+1
w.value[e]?v.value=e:(v.value=-1,r.value?.setSelectionRange(0,0))}else~v.value&&ue(t)&&(v.value=-1)}function G(e){if(oe(r.value,":autofill")||oe(r.value,":-webkit-autofill")){const t=m.value.find(t=>t.title===e.target.value)
t&&ee(t)}}function K(){e.eager&&d.value?.calculateVisibleItems()}function q(){i.value&&(s.value=!0,r.value?.focus()),p.value=null}function X(e){i.value=!0,setTimeout(()=>{u.value=!0})}function Z(e){u.value=!1}function Q(t){null!=t&&(""!==t||e.multiple||_.value)||(w.value=[])}const J=t.shallowRef(!1)
function ee(a){let l=!(arguments.length>1&&void 0!==arguments[1])||arguments[1]
if(a&&!a.props.disabled)if(e.multiple){const t=w.value.findIndex(t=>(e.valueComparator||St)(t.value,a.value)),n=null==l?!~t:l
if(~t){const e=n?[...w.value,a]:[...w.value]
e.splice(t,1),w.value=e}else n&&(w.value=[...w.value,a])
e.clearOnSelect&&(V.value="")}else{const e=!1!==l
w.value=e?[a]:[],p.value=s.value?"":V.value??"",V.value=e&&!_.value?a.title:"",t.nextTick(()=>{F.value=!1,s.value=!0})}}return t.watch(i,(a,l)=>{a!==l&&(a?(J.value=!0,V.value=e.multiple||_.value?"":String(w.value.at(-1)?.props.title??""),s.value=!0,t.nextTick(()=>J.value=!1)):(e.multiple||null!=V.value||(w.value=[]),F.value=!1,!s.value&&V.value&&(p.value=V.value),V.value="",v.value=-1))}),t.watch(V,e=>{i.value&&!J.value&&(e&&(F.value=!0),s.value=!e)}),t.watch(F,t=>{if(!e.hideSelected&&t&&w.value.length&&s.value){const e=C.value.findIndex(e=>w.value.some(t=>e.value===t.value))
o&&window.requestAnimationFrame(()=>{e>=0&&d.value?.scrollToIndex(e)})}t&&(p.value=null)}),t.watch(m,(e,t)=>{F.value||i.value&&!t.length&&e.length&&(F.value=!0)}),Bt(()=>{const a=!!(!e.hideNoData||C.value.length||l["prepend-item"]||l["append-item"]||l["no-data"]),o=w.value.length>0,u=Hi.filterProps(e)
return t.createVNode(Hi,t.mergeProps({ref:r},u,{modelValue:V.value,"onUpdate:modelValue":[e=>V.value=e,Q],focused:i.value,"onUpdate:focused":e=>i.value=e,validationValue:w.externalValue,counterValue:k.value,dirty:o,onChange:G,class:["v-autocomplete","v-autocomplete--"+(e.multiple?"multiple":"single"),{"v-autocomplete--active-menu":F.value,"v-autocomplete--chips":!!e.chips,"v-autocomplete--selection-slot":!!_.value,"v-autocomplete--selecting-index":v.value>-1},e.class],style:e.style,readonly:S.isReadonly.value,placeholder:o?void 0:e.placeholder,"onClick:clear":j,"onMousedown:control":H,onKeydown:U,"aria-expanded":M.value,"aria-controls":z.value}),{...l,default:o=>{let{id:r}=o
return t.createElementVNode(t.Fragment,null,[t.createVNode(Pi,t.mergeProps({id:$.value,ref:c,modelValue:F.value,"onUpdate:modelValue":e=>F.value=e,activator:"parent",contentClass:"v-autocomplete__content",disabled:T.value,eager:e.eager,maxHeight:310,openOnClick:!1,closeOnContentClick:!1,onAfterEnter:K,onAfterLeave:q},e.menuProps),{default:()=>[a&&t.createVNode(Mr,t.mergeProps({ref:L,filterable:!0,selected:P.value,selectStrategy:e.multiple?"independent":"single-independent",onMousedown:e=>e.preventDefault(),onKeydown:Y,onFocusin:X,onFocusout:Z,tabindex:"-1",selectable:!!C.value.length,"aria-live":"polite","aria-labelledby":`${r.value}-label`,"aria-multiselectable":e.multiple,color:e.itemColor??e.color},O,e.listProps),{default:()=>[l["prepend-item"]?.(),!C.value.length&&!e.hideNoData&&(l["no-data"]?.()??t.createVNode(Sr,{key:"no-data",title:n(e.noDataText)},null)),t.createVNode(qi,{ref:d,renderless:!0,items:C.value,itemKey:"value"},{default:a=>{let{item:n,index:o,itemRef:r}=a
const i=t.mergeProps(n.props,{ref:r,key:n.value,active:!(!R.value||n!==A.value)||void 0,onClick:()=>ee(n,null),"aria-posinset":o+1,"aria-setsize":C.value.length})
return"divider"===n.type?l.divider?.({props:n.raw,index:o})??t.createVNode(Jo,t.mergeProps(n.props,{key:`divider-${o}`}),null):"subheader"===n.type?l.subheader?.({props:n.raw,index:o})??t.createVNode(Nr,t.mergeProps(n.props,{key:`subheader-${o}`}),null):l.item?.({item:n,index:o,props:i})??t.createVNode(Sr,t.mergeProps(i,{role:"option"}),{prepend:a=>{let{isSelected:l}=a
return t.createElementVNode(t.Fragment,null,[e.multiple&&!e.hideSelected?t.createVNode(no,{key:n.value,modelValue:l,ripple:!1,tabindex:"-1","aria-hidden":!0,onClick:e=>e.preventDefault()},null):void 0,n.props.prependAvatar&&t.createVNode(Kn,{image:n.props.prependAvatar},null),n.props.prependIcon&&t.createVNode(Jl,{icon:n.props.prependIcon},null)])},title:()=>s.value?n.title:rs("v-autocomplete",n.title,N(n)?.title)})}}),l["append-item"]?.()]})]}),w.value.map((a,n)=>{function o(e){e.stopPropagation(),e.preventDefault(),ee(a,!1)}const r=t.mergeProps(Xo.filterProps(a.props),{"onClick:close":o,onKeydown(e){"Enter"!==e.key&&" "!==e.key||(e.preventDefault(),e.stopPropagation(),o(e))},onMousedown(e){e.preventDefault(),e.stopPropagation()},modelValue:!0,"onUpdate:modelValue":void 0}),i=I.value?!!l.chip:!!l.selection,s=i?re(I.value?l.chip({item:a,index:n,props:r}):l.selection({item:a,index:n})):void 0
if(!i||s)return t.createElementVNode("div",{key:a.value,class:t.normalizeClass(["v-autocomplete__selection",n===v.value&&["v-autocomplete__selection--selected",h.value]]),style:t.normalizeStyle(n===v.value?y.value:{})},[I.value?l.chip?t.createVNode(nl,{key:"chip-defaults",defaults:{VChip:{closable:E.value,size:"small",text:a.title}}},{default:()=>[s]}):t.createVNode(Xo,t.mergeProps({key:"chip",closable:E.value,size:"small",text:a.title,disabled:a.props.disabled},r),null):s??t.createElementVNode("span",{class:"v-autocomplete__selection-text"},[a.title,e.multiple&&n<w.value.length-1&&t.createElementVNode("span",{class:"v-autocomplete__selection-comma"},[t.createTextVNode(",")])])])})])},"append-inner":function(){for(var a=arguments.length,n=new Array(a),o=0;o<a;o++)n[o]=arguments[o]
return t.createElementVNode(t.Fragment,null,[l["append-inner"]?.(...n),e.menuIcon?t.createVNode(Jl,{class:"v-autocomplete__menu-icon",color:r.value?.fieldIconColor,icon:e.menuIcon,onMousedown:W,onClick:ne,"aria-hidden":!0,tabindex:"-1"},null):void 0,e.appendInnerIcon&&t.createVNode(b,{key:"append-icon",name:"appendInner",color:n[0].iconColor.value},null)])}})}),wo({isFocused:i,isPristine:s,menu:F,search:V,filteredItems:x,select:ee},r)}}),us=vt({bordered:Boolean,color:String,content:[Number,String],dot:Boolean,floating:Boolean,icon:Dt,inline:Boolean,label:{type:String,default:"$vuetify.badge"},max:[Number,String],modelValue:{type:Boolean,default:!0},offsetX:[Number,String],offsetY:[Number,String],textColor:String,...pt(),...nn({location:"top end"}),...pl(),...Pa(),...ya(),...fl({transition:"scale-rotate-transition"}),...ol()},"VBadge"),cs=wt()({name:"VBadge",inheritAttrs:!1,props:us(),setup(e,a){const{backgroundColorClasses:l,backgroundColorStyles:n}=dl(()=>e.color),{roundedClasses:o}=ml(e),{t:r}=ma(),{textColorClasses:i,textColorStyles:s}=cl(()=>e.textColor),{themeClasses:u}=Ea(),{locationStyles:c}=on(e,!0,t=>(e.floating?e.dot?2:4:e.dot?8:12)+(["top","bottom"].includes(t)?Number(e.offsetY??0):["left","right"].includes(t)?Number(e.offsetX??0):0)),{dimensionStyles:d}=rl(e)
return Bt(()=>{const v=Number(e.content),p=!e.max||isNaN(v)?e.content:v<=Number(e.max)?v:`${e.max}+`,[m,f]=E(a.attrs,["aria-atomic","aria-label","aria-live","role","title"])
return t.createVNode(e.tag,t.mergeProps({class:["v-badge",{"v-badge--bordered":e.bordered,"v-badge--dot":e.dot,"v-badge--floating":e.floating,"v-badge--inline":e.inline},e.class]},f,{style:e.style}),{default:()=>[t.createElementVNode("div",{class:"v-badge__wrapper"},[a.slots.default?.(),t.createVNode(gl,{transition:e.transition},{default:()=>[t.withDirectives(t.createElementVNode("span",t.mergeProps({class:["v-badge__badge",u.value,l.value,o.value,i.value],style:[n.value,s.value,d.value,e.inline?{}:c.value],"aria-atomic":"true","aria-label":r(e.label,v),"aria-live":"polite",role:"status"},m),[e.dot?void 0:a.slots.badge?a.slots.badge?.():e.icon?t.createVNode(Jl,{icon:e.icon},null):p]),[[t.vShow,e.modelValue]])]})])]})}),{}}}),ds=vt({color:String,density:String,...pt()},"VBannerActions"),vs=wt()({name:"VBannerActions",props:ds(),setup(e,a){let{slots:l}=a
return yt({VBtn:{color:e.color,density:e.density,slim:!0,variant:"text"}}),Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-banner-actions",e.class]),style:t.normalizeStyle(e.style)},[l.default?.()])),{}}}),ps=kt("v-banner-text"),ms=vt({avatar:String,bgColor:String,color:String,icon:Dt,lines:String,stacked:Boolean,sticky:Boolean,text:String,...wl(),...pt(),...Tl(),...ol(),...Ao({mobile:null}),...Sl(),...nn(),...mn(),...pl(),...Pa(),...ya()},"VBanner"),fs=wt()({name:"VBanner",props:ms(),setup(e,a){let{slots:l}=a
const{backgroundColorClasses:n,backgroundColorStyles:o}=dl(()=>e.bgColor),{borderClasses:r}=kl(e),{densityClasses:i}=Bl(e),{displayClasses:s,mobile:u}=Ro(e),{dimensionStyles:c}=rl(e),{elevationClasses:d}=xl(e),{locationStyles:v}=on(e),{positionClasses:p}=fn(e),{roundedClasses:m}=ml(e),{themeClasses:f}=Ca(e),g=t.toRef(()=>e.color),h=t.toRef(()=>e.density)
yt({VBannerActions:{color:g,density:h}}),Bt(()=>{const a=!(!e.text&&!l.text),y=!(!e.avatar&&!e.icon),b=!(!y&&!l.prepend)
return t.createVNode(e.tag,{class:t.normalizeClass(["v-banner",{"v-banner--stacked":e.stacked||u.value,"v-banner--sticky":e.sticky,[`v-banner--${e.lines}-line`]:!!e.lines},f.value,n.value,r.value,i.value,s.value,d.value,p.value,m.value,e.class]),style:t.normalizeStyle([o.value,c.value,v.value,e.style]),role:"banner"},{default:()=>[b&&t.createElementVNode("div",{key:"prepend",class:"v-banner__prepend"},[l.prepend?t.createVNode(nl,{key:"prepend-defaults",disabled:!y,defaults:{VAvatar:{color:g.value,density:h.value,icon:e.icon,image:e.avatar}}},l.prepend):t.createVNode(Kn,{key:"prepend-avatar",color:g.value,density:h.value,icon:e.icon,image:e.avatar},null)]),t.createElementVNode("div",{class:"v-banner__content"},[a&&t.createVNode(ps,{key:"text"},{default:()=>[l.text?.()??e.text]}),l.default?.()]),l.actions&&t.createVNode(vs,{key:"actions"},l.actions)]})})}}),gs=vt({baseColor:String,bgColor:String,color:String,grow:Boolean,mode:{type:String,validator:e=>!e||["horizontal","shift"].includes(e)},height:{type:[Number,String],default:56},active:{type:Boolean,default:!0},...wl(),...pt(),...Tl(),...Sl(),...pl(),...Qt({name:"bottom-navigation"}),...Pa({tag:"header"}),...Ol({selectedClass:"v-btn--selected"}),...ya()},"VBottomNavigation"),hs=wt()({name:"VBottomNavigation",props:gs(),emits:{"update:active":e=>!0,"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ea(),{borderClasses:o}=kl(e),{backgroundColorClasses:r,backgroundColorStyles:i}=dl(()=>e.bgColor),{densityClasses:s}=Bl(e),{elevationClasses:u}=xl(e),{roundedClasses:c}=ml(e),{ssrBootStyles:d}=_l(),v=t.computed(()=>Number(e.height)-("comfortable"===e.density?8:0)-("compact"===e.density?16:0)),p=la(e,"active",e.active),{layoutItemStyles:m}=ea({id:e.name,order:t.computed(()=>parseInt(e.order,10)),position:t.toRef(()=>"bottom"),layoutSize:t.toRef(()=>p.value?v.value:0),elementSize:v,active:p,absolute:t.toRef(()=>e.absolute)})
return Wl(e,Ul),yt({VBtn:{baseColor:t.toRef(()=>e.baseColor),color:t.toRef(()=>e.color),density:t.toRef(()=>e.density),stacked:t.toRef(()=>"horizontal"!==e.mode),variant:"text"}},{scoped:!0}),Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-bottom-navigation",{"v-bottom-navigation--active":p.value,"v-bottom-navigation--grow":e.grow,"v-bottom-navigation--shift":"shift"===e.mode},n.value,r.value,o.value,s.value,u.value,c.value,e.class]),style:t.normalizeStyle([i.value,m.value,{height:b(v.value)},d.value,e.style])},{default:()=>[l.default&&t.createElementVNode("div",{class:"v-bottom-navigation__content"},[l.default()])]})),{}}}),ys=vt({fullscreen:Boolean,scrollable:Boolean,...I(Ei({captureFocus:!0,origin:"center center",scrollStrategy:"block",transition:{component:za},zIndex:2400,retainFocus:!0}),["disableInitialFocus"])},"VDialog"),bs=wt()({name:"VDialog",props:ys(),emits:{"update:modelValue":e=>!0,afterEnter:()=>!0,afterLeave:()=>!0},setup(e,a){let{emit:l,slots:n}=a
const o=la(e,"modelValue"),{scopeId:r}=yi(),i=t.ref()
function s(){l("afterEnter"),(e.scrim||e.retainFocus)&&i.value?.contentEl&&!i.value.contentEl.contains(document.activeElement)&&i.value.contentEl.focus({preventScroll:!0})}function u(){l("afterLeave")}return t.watch(o,async e=>{e||(await t.nextTick(),i.value.activatorEl?.focus({preventScroll:!0}))}),Bt(()=>{const a=Ii.filterProps(e),l=t.mergeProps({"aria-haspopup":"dialog"},e.activatorProps),c=t.mergeProps({tabindex:-1},e.contentProps)
return t.createVNode(Ii,t.mergeProps({ref:i,class:["v-dialog",{"v-dialog--fullscreen":e.fullscreen,"v-dialog--scrollable":e.scrollable},e.class],style:e.style},a,{modelValue:o.value,"onUpdate:modelValue":e=>o.value=e,"aria-modal":"true",activatorProps:l,contentProps:c,height:e.fullscreen?void 0:e.height,width:e.fullscreen?void 0:e.width,maxHeight:e.fullscreen?void 0:e.maxHeight,maxWidth:e.fullscreen?void 0:e.maxWidth,role:"dialog",onAfterEnter:s,onAfterLeave:u},r),{activator:n.activator,default:function(){for(var e=arguments.length,a=new Array(e),l=0;l<e;l++)a[l]=arguments[l]
return t.createVNode(nl,{root:"VDialog"},{default:()=>[n.default?.(...a)]})}})}),wo({},i)}}),Vs=vt({inset:Boolean,...ys({transition:"bottom-sheet-transition"})},"VBottomSheet"),ws=wt()({name:"VBottomSheet",props:Vs(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=la(e,"modelValue")
return Bt(()=>{const a=bs.filterProps(e)
return t.createVNode(bs,t.mergeProps(a,{contentClass:["v-bottom-sheet__content",e.contentClass],modelValue:n.value,"onUpdate:modelValue":e=>n.value=e,class:["v-bottom-sheet",{"v-bottom-sheet--inset":e.inset},e.class],style:e.style}),l)}),{}}}),ks=vt({divider:[Number,String],...pt()},"VBreadcrumbsDivider"),Ss=wt()({name:"VBreadcrumbsDivider",props:ks(),setup(e,a){let{slots:l}=a
return Bt(()=>t.createElementVNode("li",{"aria-hidden":"true",class:t.normalizeClass(["v-breadcrumbs-divider",e.class]),style:t.normalizeStyle(e.style)},[l?.default?.()??e.divider])),{}}}),xs=vt({active:Boolean,activeClass:String,activeColor:String,color:String,disabled:Boolean,title:String,...pt(),...C(ol(),["width","maxWidth"]),...yn(),...Pa({tag:"li"})},"VBreadcrumbsItem"),Ns=wt()({name:"VBreadcrumbsItem",props:xs(),setup(e,a){let{slots:l,attrs:n}=a
const o=hn(e,n),r=t.computed(()=>e.active||o.isActive?.value),{dimensionStyles:i}=rl(e),{textColorClasses:s,textColorStyles:u}=cl(()=>r.value?e.activeColor:e.color)
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-breadcrumbs-item",{"v-breadcrumbs-item--active":r.value,"v-breadcrumbs-item--disabled":e.disabled,[`${e.activeClass}`]:r.value&&e.activeClass},s.value,e.class]),style:t.normalizeStyle([u.value,i.value,e.style]),"aria-current":r.value?"page":void 0},{default:()=>[o.isLink.value?t.createElementVNode("a",t.mergeProps({class:"v-breadcrumbs-item--link",onClick:o.navigate},o.linkProps),[l.default?.()??e.title]):l.default?.()??e.title]})),{}}}),Cs=vt({activeClass:String,activeColor:String,bgColor:String,color:String,disabled:Boolean,divider:{type:String,default:"/"},icon:Dt,items:{type:Array,default:()=>[]},...pt(),...Tl(),...pl(),...Pa({tag:"ul"})},"VBreadcrumbs"),Es=wt()({name:"VBreadcrumbs",props:Cs(),setup(e,a){let{slots:l}=a
const{backgroundColorClasses:n,backgroundColorStyles:o}=dl(()=>e.bgColor),{densityClasses:r}=Bl(e),{roundedClasses:i}=ml(e)
yt({VBreadcrumbsDivider:{divider:t.toRef(()=>e.divider)},VBreadcrumbsItem:{activeClass:t.toRef(()=>e.activeClass),activeColor:t.toRef(()=>e.activeColor),color:t.toRef(()=>e.color),disabled:t.toRef(()=>e.disabled)}})
const s=t.computed(()=>e.items.map(e=>"string"==typeof e?{item:{title:e},raw:e}:{item:e,raw:e}))
return Bt(()=>{const a=!(!l.prepend&&!e.icon)
return t.createVNode(e.tag,{class:t.normalizeClass(["v-breadcrumbs",n.value,r.value,i.value,e.class]),style:t.normalizeStyle([o.value,e.style])},{default:()=>[a&&t.createElementVNode("li",{key:"prepend",class:"v-breadcrumbs__prepend"},[l.prepend?t.createVNode(nl,{key:"prepend-defaults",disabled:!e.icon,defaults:{VIcon:{icon:e.icon,start:!0}}},l.prepend):t.createVNode(Jl,{key:"prepend-icon",start:!0,icon:e.icon},null)]),s.value.map((e,a,n)=>{let{item:o,raw:r}=e
return t.createElementVNode(t.Fragment,null,[l.item?.({item:o,index:a})??t.createVNode(Ns,t.mergeProps({key:a,disabled:a>=n.length-1},"string"==typeof o?{title:o}:o),{default:l.title?()=>l.title?.({item:o,index:a}):void 0}),a<n.length-1&&t.createVNode(Ss,null,{default:l.divider?()=>l.divider?.({item:r,index:a}):void 0})])}),l.default?.()]})}),{}}}),Is=vt({active:{type:Boolean,default:void 0},activeColor:String,activeIcon:[String,Function,Object],activeVariant:String,baseVariant:{type:String,default:"tonal"},disabled:Boolean,height:[Number,String],width:[Number,String],hideOverlay:Boolean,icon:[String,Function,Object],iconColor:String,loading:Boolean,opacity:[Number,String],readonly:Boolean,rotate:[Number,String],size:{type:[Number,String],default:"default"},sizes:{type:Array,default:()=>[["x-small",16],["small",24],["default",40],["large",48],["x-large",56]]},text:{type:[String,Number,Boolean],default:void 0},...wl(),...pt(),...Sl(),...jn(),...pl(),...Pa({tag:"button"}),...ya(),...$l({variant:"flat"})},"VIconBtn"),_s=wt()({name:"VIconBtn",props:Is(),emits:{"update:active":e=>!0},setup(e,a){let{attrs:l,slots:n}=a
const o=la(e,"active"),{themeClasses:r}=Ca(e),{borderClasses:i}=kl(e),{elevationClasses:s}=xl(e),{roundedClasses:u}=ml(e),{colorClasses:c,colorStyles:d,variantClasses:v}=Ml(()=>({color:(()=>{if(!e.disabled)return o.value?e.activeColor??e.color??"surface-variant":e.color})(),variant:void 0===o.value?e.variant:o.value?e.activeVariant??e.variant:e.baseVariant??e.variant})),p=new Map(e.sizes)
function m(){e.disabled||e.readonly||void 0===o.value||"a"===e.tag&&l.href||(o.value=!o.value)}return Bt(()=>{const a=o.value?e.activeIcon??e.icon:e.icon,l=e.size,f=p.has(l)?p.get(l):l,g=e.height??f,h=e.width??f,{iconSize:y}=Hn(e,()=>new Map(e.iconSizes).get(l)),V={icon:a,size:y.value,color:e.iconColor,opacity:e.opacity}
return t.createVNode(e.tag,{type:"button"===e.tag?"button":void 0,class:t.normalizeClass([{"v-icon-btn":!0,"v-icon-btn--active":o.value,"v-icon-btn--disabled":e.disabled,"v-icon-btn--loading":e.loading,"v-icon-btn--readonly":e.readonly,[`v-icon-btn--${e.size}`]:!0},r.value,c.value,i.value,s.value,u.value,v.value,e.class]),style:t.normalizeStyle([{"--v-icon-btn-rotate":b(e.rotate,"deg"),"--v-icon-btn-height":b(g),"--v-icon-btn-width":b(h)},d.value,e.style]),tabindex:e.disabled||e.readonly?-1:0,onClick:m},{default:()=>[Fl(!e.hideOverlay,"v-icon-btn"),t.createElementVNode("div",{class:"v-icon-btn__content","data-no-activator":""},[!n.default&&a?t.createVNode(Jl,t.mergeProps({key:"content-icon"},V),null):t.createVNode(nl,{key:"content-defaults",disabled:!a,defaults:{VIcon:{...V}}},{default:()=>n.default?.()??t.toDisplayString(e.text)})]),!!e.loading&&t.createElementVNode("span",{key:"loader",class:"v-icon-btn__loader"},[n.loader?.()??t.createVNode(an,{color:"boolean"==typeof e.loading?void 0:e.loading,indeterminate:"disable-shrink",width:"2",size:y.value},null)])]})}),{}}})
const Ps=/^(\d{4})-(\d{1,2})(-(\d{1,2}))?([^\d]+(\d{1,2}))?(:(\d{1,2}))?(:(\d{1,2}))?$/,As=/(\d\d?)(:(\d\d?)|)(:(\d\d?)|)/,Rs=[0,31,28,31,30,31,30,31,31,30,31,30,31],Ts=[0,31,29,31,30,31,30,31,31,30,31,30,31]
function Bs(e){const t=Zs(e)
return t.day=1,Ks(t),qs(t),t}function Ds(e){const t=Zs(e)
return t.day=Xs(t.year,t.month),Ks(t),qs(t),t}function Fs(e){return isFinite(parseInt(e))}function $s(e){if("number"==typeof e)return e
if("string"==typeof e){const t=As.exec(e)
return!!t&&60*parseInt(t[1])+parseInt(t[3]||0)}return"object"==typeof e&&("number"==typeof e.hour&&"number"==typeof e.minute&&60*e.hour+e.minute)}function Ms(e){return"number"==typeof e&&isFinite(e)||"string"==typeof e&&!!Ps.exec(e)||e instanceof Date}function zs(e){let t=arguments.length>1&&void 0!==arguments[1]&&arguments[1],a=arguments.length>2?arguments[2]:void 0
if("number"==typeof e&&isFinite(e)&&(e=new Date(e)),e instanceof Date){const t=Ls(e)
return a&&Ws(t,a,t.hasTime),t}if("string"!=typeof e){if(t)throw new Error(`${e} is not a valid timestamp. It must be a Date, number of milliseconds since Epoch, or a string in the format of YYYY-MM-DD or YYYY-MM-DD hh:mm. Zero-padding is optional and seconds are ignored.`)
return null}const l=Ps.exec(e)
if(!l){if(t)throw new Error(`${e} is not a valid timestamp. It must be a Date, number of milliseconds since Epoch, or a string in the format of YYYY-MM-DD or YYYY-MM-DD hh:mm. Zero-padding is optional and seconds are ignored.`)
return null}const n={date:e,time:"",year:parseInt(l[1]),month:parseInt(l[2]),day:parseInt(l[4])||1,hour:parseInt(l[6])||0,minute:parseInt(l[8])||0,weekday:0,hasDay:!!l[4],hasTime:!(!l[6]||!l[8]),past:!1,present:!1,future:!1}
return Ks(n),qs(n),a&&Ws(n,a,n.hasTime),n}function Ls(e){return qs({date:"",time:"",year:e.getFullYear(),month:e.getMonth()+1,day:e.getDate(),weekday:e.getDay(),hour:e.getHours(),minute:e.getMinutes(),hasDay:!0,hasTime:!0,past:!1,present:!0,future:!1})}function Os(e){return 1e4*e.year+100*e.month+e.day}function js(e){return 100*e.hour+e.minute}function Hs(e){return 1e4*Os(e)+js(e)}function Ws(e,t){let a=arguments.length>2&&void 0!==arguments[2]&&arguments[2],l=Os(t),n=Os(e),o=l===n
return e.hasTime&&a&&o&&(l=js(t),n=js(e),o=l===n),e.past=n<l,e.present=o,e.future=n>l,e}function Ys(e){return e instanceof Date||"number"==typeof e&&isFinite(e)}function Us(e,t,a){return e.hasTime!==t&&(e.hasTime=t,t||(e.hour=23,e.minute=59,e.time=Js(e))),e}function Gs(e,t,a){return e.hasTime=!0,e.hour=0,e.minute=0,eu(e,t),qs(e),a&&Ws(e,a,!0),e}function Ks(e){return e.weekday=function(e){if(e.hasDay){const t=Math.floor,a=e.day,l=(e.month+9)%12+1,n=t(e.year/100),o=e.year%100-(e.month<=2?1:0)
return((a+t(2.6*l-.2)-2*n+o+t(o/4)+t(n/4))%7+7)%7}return e.weekday}(e),e}function qs(e){return e.time=Js(e),e.date=function(e){let t=`${Qs(e.year,4)}-${Qs(e.month,2)}`
e.hasDay&&(t+=`-${Qs(e.day,2)}`)
return t}(e),e}function Xs(e,t){return function(e){return e%4==0&&e%100!=0||e%400==0}(e)?Ts[t]:Rs[t]}function Zs(e){if(null==e)return null
const{date:t,time:a,year:l,month:n,day:o,weekday:r,hour:i,minute:s,hasDay:u,hasTime:c,past:d,present:v,future:p}=e
return{date:t,time:a,year:l,month:n,day:o,weekday:r,hour:i,minute:s,hasDay:u,hasTime:c,past:d,present:v,future:p}}function Qs(e,t){let a=String(e)
for(;a.length<t;)a="0"+a
return a}function Js(e){return e.hasTime?`${Qs(e.hour,2)}:${Qs(e.minute,2)}`:""}function eu(e,t){for(e.minute+=t;e.minute>=60;)e.minute-=60,e.hour++,e.hour>=24&&(tu(e),e.hour=0)
return e}function tu(e){return e.day++,e.weekday=(e.weekday+1)%7,e.day>28&&e.day>Xs(e.year,e.month)&&(e.day=1,e.month++,e.month>12&&(e.month=1,e.year++)),e}function au(e){return e.day--,e.weekday=(e.weekday+6)%7,e.day<1&&(e.month--,e.month<1&&(e.year--,e.month=12),e.day=Xs(e.year,e.month)),e}function lu(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:tu,a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:1
for(;--a>=0;)t(e)
return e}function nu(e,t){let a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:tu,l=arguments.length>3&&void 0!==arguments[3]?arguments[3]:6
for(;e.weekday!==t&&--l>=0;)a(e)
return e}function ou(e){const t=`${Qs(e.hour,2)}:${Qs(e.minute,2)}`,a=e.date
return new Date(`${a}T${t}:00+00:00`)}function ru(e,t,a,l){let n=arguments.length>4&&void 0!==arguments[4]?arguments[4]:42,o=arguments.length>5&&void 0!==arguments[5]?arguments[5]:0
const r=Os(t),i=[]
let s=Zs(e),u=0,c=u===r
if(r<Os(e))throw new Error("End date is earlier than start date.")
for(;(!c||i.length<o)&&i.length<n;){if(u=Os(s),c=c||u===r,0===l[s.weekday]){s=tu(s)
continue}const e=Zs(s)
qs(e),Ws(e,a),i.push(e),s=lu(s,tu,l[s.weekday])}if(!i.length)throw new Error("No dates found using specified start date, end date, and weekdays.")
return i}function iu(e,t){const a=(e,t)=>""
return"undefined"==typeof Intl||void 0===Intl.DateTimeFormat?a:(a,l)=>{try{return new Intl.DateTimeFormat(e||void 0,t(a,l)).format(ou(a))}catch(e){return""}}}function su(e){const t=e.slice(-2).toUpperCase()
switch(!0){case"GB-alt-variant"===e:return{firstDay:0,firstWeekSize:4}
case"001"===e:return{firstDay:1,firstWeekSize:1}
case"AG AS BD BR BS BT BW BZ CA CO DM DO ET GT GU HK HN ID IL IN JM JP KE\n    KH KR LA MH MM MO MT MX MZ NI NP PA PE PH PK PR PY SA SG SV TH TT TW UM US\n    VE VI WS YE ZA ZW".includes(t):return{firstDay:0,firstWeekSize:1}
case"AI AL AM AR AU AZ BA BM BN BY CL CM CN CR CY EC GE HR KG KZ LB LK LV\n    MD ME MK MN MY NZ RO RS SI TJ TM TR UA UY UZ VN XK".includes(t):return{firstDay:1,firstWeekSize:1}
case"AD AN AT AX BE BG CH CZ DE DK EE ES FI FJ FO FR GB GF GP GR HU IE IS\n    IT LI LT LU MC MQ NL NO PL RE RU SE SK SM VA".includes(t):return{firstDay:1,firstWeekSize:4}
case"AE AF BH DJ DZ EG IQ IR JO KW LY OM QA SD SY".includes(t):return{firstDay:6,firstWeekSize:1}
case"MV"===t:return{firstDay:5,firstWeekSize:1}
case"PT"===t:return{firstDay:0,firstWeekSize:4}
default:return null}}function uu(e,t,l){let n=(l??su(t)?.firstDay??0)%7;[0,1,2,3,4,5,6].includes(n)||(a("Invalid firstDayOfWeek, expected discrete number in range [0-6]"),n=0)
const o=new Date(e)
for(;o.getDay()!==n;)o.setDate(o.getDate()-1)
return o}function cu(e){return new Date(e.getFullYear(),e.getMonth(),1)}function du(e){return new Date(e.getFullYear(),e.getMonth()+1,0)}const vu=/^([12]\d{3}-([1-9]|0[1-9]|1[0-2])-([1-9]|0[1-9]|[12]\d|3[01]))$/
function pu(e){if(null==e)return new Date
if(e instanceof Date)return e
if("string"==typeof e){let t
if(vu.test(e))return function(e){const t=e.split("-").map(Number)
return new Date(t[0],t[1]-1,t[2])}(e)
if(t=Date.parse(e),!isNaN(t))return new Date(t)}return null}const mu=new Date(2e3,0,2)
function fu(e,t,a,l){const n=pu(e)??new Date,o=l?.[t]
if("function"==typeof o)return o(n,t,a)
let r={}
switch(t){case"fullDate":r={year:"numeric",month:"short",day:"numeric"}
break
case"fullDateWithWeekday":r={weekday:"long",year:"numeric",month:"long",day:"numeric"}
break
case"normalDate":return`${n.getDate()} ${new Intl.DateTimeFormat(a,{month:"long"}).format(n)}`
case"normalDateWithWeekday":r={weekday:"short",day:"numeric",month:"short"}
break
case"shortDate":r={month:"short",day:"numeric"}
break
case"year":r={year:"numeric"}
break
case"month":r={month:"long"}
break
case"monthShort":r={month:"short"}
break
case"monthAndYear":r={month:"long",year:"numeric"}
break
case"monthAndDate":r={month:"long",day:"numeric"}
break
case"weekday":r={weekday:"long"}
break
case"weekdayShort":r={weekday:"short"}
break
case"dayOfMonth":return new Intl.NumberFormat(a).format(n.getDate())
case"hours12h":r={hour:"numeric",hour12:!0}
break
case"hours24h":r={hour:"numeric",hour12:!1}
break
case"minutes":r={minute:"numeric"}
break
case"seconds":r={second:"numeric"}
break
case"fullTime":r={hour:"numeric",minute:"numeric"}
break
case"fullTime12h":r={hour:"numeric",minute:"numeric",hour12:!0}
break
case"fullTime24h":r={hour:"numeric",minute:"numeric",hour12:!1}
break
case"fullDateTime":r={year:"numeric",month:"short",day:"numeric",hour:"numeric",minute:"numeric"}
break
case"fullDateTime12h":r={year:"numeric",month:"short",day:"numeric",hour:"numeric",minute:"numeric",hour12:!0}
break
case"fullDateTime24h":r={year:"numeric",month:"short",day:"numeric",hour:"numeric",minute:"numeric",hour12:!1}
break
case"keyboardDate":r={year:"numeric",month:"2-digit",day:"2-digit"}
break
case"keyboardDateTime":return r={year:"numeric",month:"2-digit",day:"2-digit",hour:"numeric",minute:"numeric"},new Intl.DateTimeFormat(a,r).format(n).replace(/, /g," ")
case"keyboardDateTime12h":return r={year:"numeric",month:"2-digit",day:"2-digit",hour:"numeric",minute:"numeric",hour12:!0},new Intl.DateTimeFormat(a,r).format(n).replace(/, /g," ")
case"keyboardDateTime24h":return r={year:"numeric",month:"2-digit",day:"2-digit",hour:"numeric",minute:"numeric",hour12:!1},new Intl.DateTimeFormat(a,r).format(n).replace(/, /g," ")
default:r=o??{timeZone:"UTC",timeZoneName:"short"}}return new Intl.DateTimeFormat(a,r).format(n)}function gu(e,t){const a=new Date(e)
return a.setDate(a.getDate()+t),a}function hu(e){return e.getFullYear()}function yu(e,t,a,l){const n=su(t),o=a??n?.firstDay??0,r=n?.firstWeekSize??1
return void 0!==l?function(e,t,a,l){const n=(7+l-a)%7,o=uu(e,t,a),r=gu(o,6)
function i(e){return(7+new Date(e,0,1).getDay()-a)%7}let s=hu(o)
s<hu(r)&&i(s+1)<=n&&s++
const u=new Date(s,0,1),c=i(s),d=gu(u,c<=n?-c:7-c)
return 1+wu(Su(o),ku(d),"weeks")}(e,t,o,l):function(e,t,a,l){const n=uu(e,t,a),o=gu(uu(e,t,a),6)
function r(e){const l=new Date(e,0,1)
return 7-wu(l,uu(l,t,a),"days")}let i=hu(n)
i<hu(o)&&r(i+1)>=l&&i++
const s=new Date(i,0,1),u=r(i),c=gu(s,u>=l?u-7:u)
return 1+wu(Su(n),ku(c),"weeks")}(e,t,o,r)}function bu(e,t){return e.getTime()>t.getTime()}function Vu(e,t){return e.getTime()===t.getTime()}function wu(e,t,a){const l=new Date(e),n=new Date(t)
switch(a){case"years":return l.getFullYear()-n.getFullYear()
case"quarters":return Math.floor((l.getMonth()-n.getMonth()+12*(l.getFullYear()-n.getFullYear()))/4)
case"months":return l.getMonth()-n.getMonth()+12*(l.getFullYear()-n.getFullYear())
case"weeks":return Math.floor((l.getTime()-n.getTime())/6048e5)
case"days":return Math.floor((l.getTime()-n.getTime())/864e5)
case"hours":return Math.floor((l.getTime()-n.getTime())/36e5)
case"minutes":return Math.floor((l.getTime()-n.getTime())/6e4)
case"seconds":return Math.floor((l.getTime()-n.getTime())/1e3)
default:return l.getTime()-n.getTime()}}function ku(e){return new Date(e.getFullYear(),e.getMonth(),e.getDate(),0,0,0,0)}function Su(e){return new Date(e.getFullYear(),e.getMonth(),e.getDate(),23,59,59,999)}class xu{constructor(e){this.locale=e.locale,this.formats=e.formats}date(e){return pu(e)}toJsDate(e){return e}toISO(e){return function(e,t){const a=e.toJsDate(t)
return`${a.getFullYear()}-${z(String(a.getMonth()+1),2,"0")}-${z(String(a.getDate()),2,"0")}`}(this,e)}parseISO(e){return function(e){const[t,a,l]=e.split("-").map(Number)
return new Date(t,a-1,l)}(e)}addMinutes(e,t){return function(e,t){const a=new Date(e)
return a.setMinutes(a.getMinutes()+t),a}(e,t)}addHours(e,t){return function(e,t){const a=new Date(e)
return a.setHours(a.getHours()+t),a}(e,t)}addDays(e,t){return gu(e,t)}addWeeks(e,t){return function(e,t){const a=new Date(e)
return a.setDate(a.getDate()+7*t),a}(e,t)}addMonths(e,t){return function(e,t){const a=new Date(e)
return a.setDate(1),a.setMonth(a.getMonth()+t),a}(e,t)}getWeekArray(e,t){const a=void 0!==t?Number(t):void 0
return function(e,t,a){const l=[]
let n=[]
const o=cu(e),r=du(e),i=a??su(t)?.firstDay??0,s=(o.getDay()-i+7)%7,u=(r.getDay()-i+7)%7
for(let e=0;e<s;e++){const t=new Date(o)
t.setDate(t.getDate()-(s-e)),n.push(t)}for(let t=1;t<=r.getDate();t++){const a=new Date(e.getFullYear(),e.getMonth(),t)
n.push(a),7===n.length&&(l.push(n),n=[])}for(let e=1;e<7-u;e++){const t=new Date(r)
t.setDate(t.getDate()+e),n.push(t)}return n.length>0&&l.push(n),l}(e,this.locale,a)}startOfWeek(e,t){const a=void 0!==t?Number(t):void 0
return uu(e,this.locale,a)}endOfWeek(e){return function(e,t){const a=new Date(e),l=((su(t)?.firstDay??0)+6)%7
for(;a.getDay()!==l;)a.setDate(a.getDate()+1)
return a}(e,this.locale)}startOfMonth(e){return cu(e)}endOfMonth(e){return du(e)}format(e,t){return fu(e,t,this.locale,this.formats)}isEqual(e,t){return Vu(e,t)}isValid(e){return function(e){const t=new Date(e)
return t instanceof Date&&!isNaN(t.getTime())}(e)}isWithinRange(e,t){return function(e,t){return bu(e,t[0])&&function(e,t){return e.getTime()<t.getTime()}(e,t[1])}(e,t)}isAfter(e,t){return bu(e,t)}isAfterDay(e,t){return function(e,t){return bu(ku(e),ku(t))}(e,t)}isBefore(e,t){return!bu(e,t)&&!Vu(e,t)}isSameDay(e,t){return function(e,t){return e.getDate()===t.getDate()&&e.getMonth()===t.getMonth()&&e.getFullYear()===t.getFullYear()}(e,t)}isSameMonth(e,t){return function(e,t){return e.getMonth()===t.getMonth()&&e.getFullYear()===t.getFullYear()}(e,t)}isSameYear(e,t){return function(e,t){return e.getFullYear()===t.getFullYear()}(e,t)}setMinutes(e,t){return function(e,t){const a=new Date(e)
return a.setMinutes(t),a}(e,t)}setHours(e,t){return function(e,t){const a=new Date(e)
return a.setHours(t),a}(e,t)}setMonth(e,t){return function(e,t){const a=new Date(e)
return a.setMonth(t),a}(e,t)}setDate(e,t){return function(e,t){const a=new Date(e)
return a.setDate(t),a}(e,t)}setYear(e,t){return function(e,t){const a=new Date(e)
return a.setFullYear(t),a}(e,t)}getDiff(e,t,a){return wu(e,t,a)}getWeekdays(e,t){const a=void 0!==e?Number(e):void 0
return function(e,t,a){const l=t??su(e)?.firstDay??0
return y(7).map(t=>{const n=new Date(mu)
return n.setDate(mu.getDate()+l+t),new Intl.DateTimeFormat(e,{weekday:a??"narrow"}).format(n)})}(this.locale,a,t)}getYear(e){return hu(e)}getMonth(e){return function(e){return e.getMonth()}(e)}getWeek(e,t,a){const l=void 0!==t?Number(t):void 0,n=void 0!==a?Number(a):void 0
return yu(e,this.locale,l,n)}getDate(e){return function(e){return e.getDate()}(e)}getNextMonth(e){return function(e){return new Date(e.getFullYear(),e.getMonth()+1,1)}(e)}getPreviousMonth(e){return function(e){return new Date(e.getFullYear(),e.getMonth()-1,1)}(e)}getHours(e){return function(e){return e.getHours()}(e)}getMinutes(e){return function(e){return e.getMinutes()}(e)}startOfDay(e){return ku(e)}endOfDay(e){return Su(e)}startOfYear(e){return function(e){return new Date(e.getFullYear(),0,1)}(e)}endOfYear(e){return function(e){return new Date(e.getFullYear(),11,31)}(e)}}const Nu=Symbol.for("vuetify:date-options"),Cu=Symbol.for("vuetify:date-adapter")
function Eu(e,t,a){const l=[`${e.toISO(a??t).split("T")[0]}T00:00:00Z`,`${e.toISO(t).split("T")[0]}T00:00:00Z`]
return"string"==typeof e.date()?e.getDiff(l[0],l[1],"days"):e.getDiff(e.date(l[0]),e.date(l[1]),"days")}function Iu(e,a){const l=t.reactive("function"==typeof e.adapter?new e.adapter({locale:e.locale[a.current.value]??a.current.value,formats:e.formats}):e.adapter)
return t.watch(a.current,t=>{l.locale=e.locale[t]??t??l.locale}),l}function _u(){const e=t.inject(Nu)
if(!e)throw new Error("[Vuetify] Could not find injected date options")
return Iu(e,ma())}const Pu=vt({start:{type:[String,Number,Date],validate:Ms,default:()=>Ls(new Date).date},end:{type:[String,Number,Date],validate:Ms},weekdays:{type:[Array,String],default:()=>[0,1,2,3,4,5,6],validate:function(e){if("string"==typeof e&&(e=e.split(",")),Array.isArray(e)){const t=e.map(e=>parseInt(e))
if(t.length>7||0===t.length)return!1
const a={}
let l=!1
for(let e=0;e<t.length;e++){const n=t[e]
if(!isFinite(n)||n<0||n>=7)return!1
if(e>0){const a=n-t[e-1]
if(a<0){if(l)return!1
l=!0}else if(0===a)return!1}if(a[n])return!1
a[n]=!0}return!0}return!1}},firstDayOfWeek:[Number,String],firstDayOfYear:[Number,String],weekdayFormat:{type:Function,default:null},dayFormat:{type:Function,default:null},locale:String,now:{type:String,validator:Ms},type:{type:String,default:"month"}},"VCalendar-base")
function Au(e){const{times:a,updateTimes:l}=function(e){const a=t.reactive({now:zs("0000-00-00 00:00",!0),today:zs("0000-00-00",!0)}),l=t.computed(()=>e.now&&Ms(e.now)?zs(e.now,!0):null)
function n(){a.now.present=a.today.present=!0,a.now.past=a.today.past=!1,a.now.future=a.today.future=!1}function o(){return Ls(new Date)}function r(e,t){e.date!==t.date&&(t.year=e.year,t.month=e.month,t.day=e.day,t.weekday=e.weekday,t.date=e.date)}function i(e,t){e.time!==t.time&&(t.hour=e.hour,t.minute=e.minute,t.time=e.time)}function s(){const e=l.value||o()
r(e,a.now),i(e,a.now),r(e,a.today)}return t.watch(l,s),s(),n(),{times:a,parsedNow:l,updateTimes:s,setPresent:n,getNow:o,updateDay:r,updateTime:i}}({now:e.now}),n=fa(e),o=_u(),r=t.computed(()=>"month"===e.type?Bs(zs(e.start,!0)):zs(e.start,!0)),i=t.computed(()=>{const t=r.value,a=e.end&&zs(e.end)||t,l=Hs(a)<Hs(t)?t:a
return"month"===e.type?Ds(l):l}),s=t.computed(()=>Ms(e.modelValue)?zs(e.modelValue,!0):r.value||a.today),u=t.computed(()=>{const t=Array.isArray(e.weekdays)?e.weekdays:(e.weekdays||"").split(",").map(e=>parseInt(e,10)),a=o.toJsDate(o.startOfWeek(o.date(),e.firstDayOfWeek)).getDay()
return[...t.toSorted().filter(e=>e>=a),...t.toSorted().filter(e=>e<a)]}),c=t.computed(()=>{const t=s.value,a=parseInt(String(e.categoryDays))||1
switch(e.type){case"day":return[t.weekday]
case"4day":return[t.weekday,(t.weekday+1)%7,(t.weekday+2)%7,(t.weekday+3)%7]
case"category":return Array.from({length:a},(e,a)=>(t.weekday+a)%7)
default:return u.value}}),d=t.computed(()=>function(e){const t=[1,1,1,1,1,1,1],a=[0,0,0,0,0,0,0]
for(let t=0;t<e.length;t++)a[e[t]]=1
for(let e=0;e<7;e++){let l=1
for(let t=1;t<7&&!a[(e+t)%7];t++)l++
t[e]=a[e]*l}return t}(u.value)),v=t.computed(()=>ru(r.value,i.value,a.today,d.value)),p=t.computed(()=>e.dayFormat?e.dayFormat:iu(n.current.value,()=>({timeZone:"UTC",day:"numeric"}))),m=t.computed(()=>e.weekdayFormat?e.weekdayFormat:iu(n.current.value,(e,t)=>({timeZone:"UTC",weekday:t?"short":"long"})))
return{times:a,locale:n,parsedValue:s,parsedWeekdays:u,effectiveWeekdays:c,weekdaySkips:d,parsedStart:r,parsedEnd:i,days:v,dayFormatter:p,weekdayFormatter:m,getColorProps:function(e){return vl(e)},getRelativeClasses:function(e){let t=arguments.length>1&&void 0!==arguments[1]&&arguments[1]
return{"v-present":e.present,"v-past":e.past,"v-future":e.future,"v-outside":t}},getWeekNumber:function(t){return o.getWeek(o.date(t.date),e.firstDayOfWeek,e.firstDayOfYear)},getStartOfWeek:function(e){return function(e,t,a){const l=Zs(e)
return nu(l,t[0],au),qs(l),a&&Ws(l,a,l.hasTime),l}(e,u.value,a.today)},getEndOfWeek:function(e){return function(e,t,a){const l=Zs(e)
return nu(l,t[t.length-1]),qs(l),a&&Ws(l,a,l.hasTime),l}(e,u.value,a.today)},getFormatter:function(e){return iu(n.current.value,()=>e)},updateTimes:l}}const Ru=vt({maxDays:{type:Number,default:7},intervalHeight:{type:[Number,String],default:48,validate:Fs},intervalWidth:{type:[Number,String],default:60,validate:Fs},intervalMinutes:{type:[Number,String],default:60,validate:Fs},firstInterval:{type:[Number,String],default:0,validate:Fs},firstTime:{type:[Number,String,Object],validate:function(e){return"number"==typeof e&&isFinite(e)||!!As.exec(e)||"object"==typeof e&&isFinite(e.hour)&&isFinite(e.minute)}},intervalCount:{type:[Number,String],default:24,validate:Fs},intervalFormat:{type:Function,default:null},intervalStyle:{type:Function,default:null},showIntervalLabel:{type:Function,default:null}},"VCalendar-intervals")
function Tu(e){const a=Au(e),l=t.shallowRef(),n=t.computed(()=>parseInt(String(e.firstInterval||0))),o=t.computed(()=>parseInt(String(e.intervalMinutes||60))),r=t.computed(()=>parseInt(String(e.intervalCount||24))),i=t.computed(()=>parseFloat(String(e.intervalHeight||48))),s=t.computed(()=>$s(e.firstTime)),u=t.computed(()=>{const e=s.value
return!1!==e&&e>=0&&e<=1440?e:n.value*o.value}),c=t.computed(()=>r.value*i.value),d=t.computed(()=>ru(a.parsedStart.value,a.parsedEnd.value,a.times.today,a.weekdaySkips.value,e.maxDays)),v=t.computed(()=>{const e=d.value,t=u.value,l=o.value,n=r.value,i=a.times.now
return e.map(e=>function(e,t,a,l,n){const o=[]
for(let r=0;r<l;r++){const l=t+r*a,i=Zs(e)
o.push(Gs(i,l,n))}return o}(e,t,l,n,i))}),p=t.computed(()=>e.intervalFormat?e.intervalFormat:iu(a.locale.current.value,(e,t)=>t?0===e.minute?{timeZone:"UTC",hour:"numeric"}:{timeZone:"UTC",hour:"numeric",minute:"2-digit"}:{timeZone:"UTC",hour:"2-digit",minute:"2-digit"}))
function m(e){return e/o.value*i.value}function f(e){let t=arguments.length>1&&void 0!==arguments[1]&&arguments[1]
const a=!1!==t
let l=g(e,"boolean"!=typeof t?t:void 0)
return!1===l||(l*=c.value,a?l<0?l=0:l>c.value&&(l=c.value):l<0?l+=c.value:l>c.value&&(l-=c.value)),l}function g(e,t){let a=$s(e)
if(!1===a)return!1
const l=r.value*o.value
if(t&&"object"==typeof e&&"day"in e){a+=(Os(e)-Os(t))*l}return(a-u.value)/l}return{...a,scrollAreaRef:l,parsedFirstInterval:n,parsedIntervalMinutes:o,parsedIntervalCount:r,parsedIntervalHeight:i,parsedFirstTime:s,firstMinute:u,bodyHeight:c,days:d,intervals:v,intervalFormatter:p,showIntervalLabelDefault:function(e){const t=v.value[0][0]
return!(t.hour===e.hour&&t.minute===e.minute)},intervalStyleDefault:function(e){},getTimestampAtEvent:function(e,t){const l=Zs(t),n=e.currentTarget.getBoundingClientRect(),r=u.value,s=e,c=e,d=s.changedTouches||s.touches,v=((d&&d[0]?d[0].clientY:c.clientY)-n.top)/i.value
return Gs(l,r+Math.floor(v*o.value),a.times.now)},getSlotScope:function(e){const t=Zs(e)
return t.timeToY=f,t.timeDelta=g,t.minutesToPixels=m,t.week=d.value,t.intervalRange=[u.value,u.value+r.value*o.value],t},scrollToTime:function(e){const t=f(e),a=l.value
return!(!1===t||!a)&&(a.scrollTop=t,!0)},minutesToPixels:m,timeToY:f,timeDelta:g}}const Bu={mounted:function(e,t){const a=t.value,l={passive:!t.modifiers?.active}
window.addEventListener("resize",a,l),e._onResize=Object(e._onResize),e._onResize[t.instance.$.uid]={handler:a,options:l},t.modifiers?.quiet||a()},unmounted:function(e,t){if(!e._onResize?.[t.instance.$.uid])return
const{handler:a,options:l}=e._onResize[t.instance.$.uid]
window.removeEventListener("resize",a,l),delete e._onResize[t.instance.$.uid]}},Du=Vt({name:"VCalendarDaily",directives:{vResize:Bu},props:{color:String,shortWeekdays:{type:Boolean,default:!0},shortIntervals:{type:Boolean,default:!0},hideHeader:Boolean,...Pu(),...Ru()},setup(e,a){let{slots:l,attrs:n}=a
const o=t.ref(0),r=t.ref(),i=Tu(e)
function s(){t.nextTick(u)}function u(){o.value=c()}function c(){return i.scrollAreaRef.value&&r.value?i.scrollAreaRef.value.offsetWidth-r.value.offsetWidth:0}function d(){const a=b(e.intervalWidth)
return t.createElementVNode("div",{class:"v-calendar-daily__intervals-head",style:{width:a}},[l["interval-header"]?.()])}function v(e,a){const l=_t(n,":day",t=>({nativeEvent:t,...i.getSlotScope(e)}))
return t.createElementVNode("div",t.mergeProps({key:e.date,class:["v-calendar-daily_head-day",i.getRelativeClasses(e)]},l),[m(e),f(e),p(e,a)])}function p(e,t){return l["day-header"]?.({week:i.days.value,...e,index:t})??[]}function m(a){const l=a.present?e.color:void 0
return t.createElementVNode("div",t.mergeProps(i.getColorProps({text:l}),{class:"v-calendar-daily_head-weekday"}),[i.weekdayFormatter.value(a,e.shortWeekdays)])}function f(e){return t.createElementVNode("div",{class:"v-calendar-daily_head-day-label"},[l["day-label-header"]?.(e)??g(e)])}function g(a){const l=_t(n,":date",e=>({nativeEvent:e,...a}))
return t.createVNode(_s,t.mergeProps({active:a.present,activeColor:e.color,variant:"outlined",baseVariant:"text","onUpdate:active":ne},l),{default:()=>[i.dayFormatter.value(a,!1)]})}function h(e){return l["day-body"]?.(i.getSlotScope(e))??[]}function y(e){return i.intervals.value[e].map(V)}function V(a){const n=b(e.intervalHeight),o=e.intervalStyle||i.intervalStyleDefault
return t.createElementVNode("div",{class:"v-calendar-daily__day-interval",key:a.time,style:t.normalizeStyle([{height:n},o(a)])},[l.interval?.(i.getSlotScope(a))])}function w(){const a=b(e.intervalWidth),l=_t(n,":interval",e=>({nativeEvent:e,...i.getTimestampAtEvent(e,i.parsedStart.value)}))
return t.createElementVNode("div",t.mergeProps({class:"v-calendar-daily__intervals-body",style:{width:a}},l),[k()])}function k(){return i.intervals.value.length?i.intervals.value[0].map(S):null}function S(a){const l=b(e.intervalHeight),n=e.shortIntervals,o=(e.showIntervalLabel||i.showIntervalLabelDefault)(a)?i.intervalFormatter.value(a,n):void 0
return t.createElementVNode("div",{key:a.time,class:"v-calendar-daily__interval",style:{height:l}},[t.createElementVNode("div",{class:"v-calendar-daily__interval-text"},[o])])}return t.onMounted(s),Bt(()=>t.withDirectives(t.createElementVNode("div",{class:t.normalizeClass(["v-calendar-daily",n.class]),onDragstart:e=>e.preventDefault()},[e.hideHeader?void 0:t.createElementVNode("div",{class:"v-calendar-daily__head",style:{marginRight:o.value+"px"}},[d(),i.days.value.map(v)]),t.createElementVNode("div",{class:"v-calendar-daily__body"},[t.createElementVNode("div",{ref:i.scrollAreaRef,class:"v-calendar-daily__scroll-area"},[t.createElementVNode("div",{ref:r,class:"v-calendar-daily__pane",style:{height:b(i.bodyHeight.value)}},[t.createElementVNode("div",{class:"v-calendar-daily__day-container"},[w(),l.days?.()??i.days.value.map((e,a)=>{const l=_t(n,":time",t=>({nativeEvent:t,...i.getSlotScope(i.getTimestampAtEvent(t,e))}))
return t.createElementVNode("div",t.mergeProps({key:e.date,class:["v-calendar-daily__day",i.getRelativeClasses(e)]},l),[y(a),h(e)])})])])])])]),[[Bu,u,void 0,{quiet:!0}]])),{...i,scrollPush:o,pane:r,init:s,onResize:u,getScrollPush:c}}})
function Fu(e,t){return"string"==typeof e?e.split(/\s*,\s/):Array.isArray(e)?e.map(e=>{if("string"==typeof e)return e
const a="string"==typeof e.categoryName?e.categoryName:function(e,t){return"function"==typeof t?t(e):"string"==typeof t&&"object"==typeof e&&e?e[t]:"string"==typeof e?e:""}(e,t)
return{...e,categoryName:a}}):[]}const $u=Vt({name:"VCalendarCategory",props:{categories:{type:[Array,String],default:""},categoryText:[String,Function],categoryForInvalid:{type:String,default:""},...Pu(),...Ru()},setup(e,a){let{slots:l,attrs:n}=a
const o=Tu(e),r=t.computed(()=>Fu(e.categories,e.categoryText))
function i(t,a){return{...t,category:"object"==typeof a&&a&&a.categoryName===e.categoryForInvalid?null:a}}function s(e){return t.createElementVNode("div",{class:"v-calendar-category__columns"},[r.value.map(a=>function(e,a){const r="object"==typeof a.category?a.category.categoryName:a.category,s=_t(n,":dayCategory",()=>i(o.getSlotScope(e)||e,a.category))
return t.createElementVNode("div",t.mergeProps({class:"v-calendar-category__column-header"},s),[l.category?.(a)??u(r),l["day-header"]?.(a)])}(e,i(e,a)))])}function u(a){return t.createElementVNode("div",{class:"v-calendar-category__category"},[null===a?e.categoryForInvalid:a])}function c(){const e=[]
return o.days.value.forEach((a,l)=>{const i=new Array(r.value.length||1)
i.fill(a),e.push(...i.map((e,a)=>function(e,a,l){const i=r.value[l],s=_t(n,":time",t=>o.getSlotScope(o.getTimestampAtEvent(t,e)))
return t.createElementVNode("div",t.mergeProps({key:e.date+"-"+l,class:["v-calendar-daily__day",o.getRelativeClasses(e)]},s),[d(a,i),v(e,i)])}(e,l,a)))}),e}function d(a,n){return o.intervals.value[a].map(a=>function(a,n){const r=b(e.intervalHeight),s=e.intervalStyle||o.intervalStyleDefault
return t.createElementVNode("div",{key:a.time,class:"v-calendar-daily__day-interval",style:t.normalizeStyle([{height:r},s({...a,category:n})])},[l.interval?.(i(o.getSlotScope(a),n))])}(a,n))}function v(e,a){return t.createElementVNode("div",{class:"v-calendar-category__columns"},[p(e,a)])}function p(e,a){const r=_t(n,":timeCategory",t=>i(o.getSlotScope(o.getTimestampAtEvent(t,e)),a))
return t.createElementVNode("div",t.mergeProps({class:"v-calendar-category__column"},r),[l["day-body"]?.(i(o.getSlotScope(e),a))])}return Bt(()=>t.createVNode(Du,t.mergeProps({class:["v-calendar-daily","v-calendar-category"]},e),{...l,days:c,"day-header":s})),{...o,parsedCategories:r}}}),Mu={control:"ctrl",command:"cmd",option:"alt",up:"arrowup",down:"arrowdown",left:"arrowleft",right:"arrowright",esc:"escape",spacebar:" ",space:" ",return:"enter",del:"delete",minus:"-",hyphen:"-"}
function zu(e){const t=e.toLowerCase()
return Mu[t]||t}function Lu(e){let t=arguments.length>1&&void 0!==arguments[1]&&arguments[1]
const l={keys:[],separators:[]}
if(!e)return t||a("Invalid hotkey combination: empty string provided"),l
if(e.length>1&&["+","/","_"].some(t=>e.startsWith(t))&&!["++","//","__"].some(t=>e.startsWith(t))||e.includes("++")||e.includes("__")||"+"===e||"_"===e||e.length>1&&(e.endsWith("+")||e.endsWith("_"))&&e.at(-2)!==e.at(-1)||"++"===e||"--"===e||"__"===e)return t||a(`Invalid hotkey combination: "${e}" has invalid structure`),l
const n=[],o=[]
let r=""
const i=e=>{r&&(e&&o.push(e),n.push(zu(r)),r="")}
for(let t=0;t<e.length;t++){const a=e[t],l=e[t+1];["+","/","_","-"].includes(a)?a===l?(i(a),n.push(a),t++):["+","/","_"].includes(a)?i(a):r+=a:r+=a}i()
return n.some(e=>e.length>1&&e.includes("-")&&"--"!==e)?(t||a(`Invalid hotkey combination: "${e}" has invalid structure`),l):0===n.length&&e?{keys:[zu(e)],separators:o}:{keys:n,separators:o}}function Ou(e){if(!e)return a("Invalid hotkey sequence: empty string provided"),[]
const t=e.startsWith("-")&&!["---","--+"].includes(e),l=e.endsWith("-")&&!e.endsWith("+-")&&!e.endsWith("_-")&&"-"!==e&&"---"!==e
if(t||l)return a(`Invalid hotkey sequence: "${e}" contains invalid combinations`),[]
const n=[]
let o="",r=0
for(;r<e.length;){const t=e[r]
if("-"===t){const a=e[r-1],l=r>1?e[r-2]:void 0;["+","_"].includes(a)&&!["+","/"].includes(l??"")?(o+=t,r++):(o?(n.push(o),o=""):n.push("-"),r++)}else o+=t,r++}o&&n.push(o)
const i=[]
let s=0
for(const e of n)"-"===e?(s%2==0&&i.push("-"),s++):(s=0,i.push(e))
return i.every(e=>Lu(e,!0).keys.length>0)?i:(a(`Invalid hotkey sequence: "${e}" contains invalid combinations`),[])}const ju={"credit-card":"#### - #### - #### - ####",date:"##/##/####","date-time":"##/##/#### ##:##","iso-date":"####-##-##","iso-date-time":"####-##-## ##:##",phone:"(###) ### - ####",social:"###-##-####",time:"##:##","time-with-seconds":"##:##:##"},Hu={"#":{pattern:/[0-9]/},A:{pattern:/[A-Z]/i,convert:e=>e.toUpperCase()},a:{pattern:/[a-z]/i,convert:e=>e.toLowerCase()},N:{pattern:/[0-9A-Z]/i,convert:e=>e.toUpperCase()},n:{pattern:/[0-9a-z]/i,convert:e=>e.toLowerCase()},X:{pattern:/[-!$%^&*()_+|~=`{}[\]:";'<>?,./\\ ]/}}
const Wu=Vt({name:"VCalendarWeekly",props:{minWeeks:{validate:Fs,default:1},monthFormat:Function,showWeek:Boolean,color:String,shortWeekdays:{type:Boolean,default:!0},showMonthOnFirst:{type:Boolean,default:!0},shortMonths:{type:Boolean,default:!0},hideHeader:Boolean,...Pu()},setup(e,a){let{slots:l,attrs:n}=a
const o=Au(e),r=Ea(),i=t.computed(()=>parseInt(String(e.minWeeks))),s=t.computed(()=>{const e=i.value*o.parsedWeekdays.value.length
return ru(o.getStartOfWeek(o.parsedStart.value),o.getEndOfWeek(o.parsedEnd.value),o.times.today,o.weekdaySkips.value,Number.MAX_SAFE_INTEGER,e)}),u=t.computed(()=>{const e=o.times.today
return ru(o.getStartOfWeek(e),o.getEndOfWeek(e),e,o.weekdaySkips.value,o.parsedWeekdays.value.length,o.parsedWeekdays.value.length)}),c=t.computed(()=>e.monthFormat?e.monthFormat:iu(o.locale.current.value,(e,t)=>({timeZone:"UTC",month:t?"short":"long"})))
function d(e){const t=Os(e)
return t<Os(o.parsedStart.value)||t>Os(o.parsedEnd.value)}function v(){const a=u.value.map(p)
return e.showWeek&&a.unshift(t.createElementVNode("div",{class:"v-calendar-weekly__head-weeknumber"},null)),a}function p(a,l){const n=d(s.value[l]),r=a.present?e.color:void 0
return t.createElementVNode("div",t.mergeProps(o.getColorProps({text:r}),{key:a.date,class:["v-calendar-weekly__head-weekday",o.getRelativeClasses(a,n)],role:"columnheader"}),[o.weekdayFormatter.value(a,e.shortWeekdays)])}function m(){const e=s.value,t=o.parsedWeekdays.value.length,a=[]
for(let l=0;l<e.length;l+=t)a.push(f(e.slice(l,l+t),g(e[l])))
return a}function f(a,r){const i=a.map((e,r)=>function(e,a,r){const i=d(e),s=_t(n,":day",t=>({nativeEvent:t,...e}))
return t.createElementVNode("div",t.mergeProps({key:e.date,class:["v-calendar-weekly__day",o.getRelativeClasses(e,i)],role:"cell"},s),[h(e),l.day?.({outside:i,index:a,week:r,...e})])}(e,r,a))
return e.showWeek&&i.unshift(function(e){return t.createElementVNode("div",{class:"v-calendar-weekly__weeknumber"},[t.createElementVNode("small",null,[String(e)])])}(r)),t.createElementVNode("div",{key:a[0].date,class:"v-calendar-weekly__week",role:"row"},[i])}function g(e){return o.getWeekNumber(e)}function h(e){return t.createElementVNode("div",{class:"v-calendar-weekly__day-label"},[l["day-label"]?.(e)??y(e)])}function y(a){const l=1===a.day&&e.showMonthOnFirst,r=_t(n,":date",e=>({nativeEvent:e,...a}))
return t.createVNode(_s,t.mergeProps({active:a.present,activeColor:e.color,variant:"outlined",baseVariant:"text","onUpdate:active":ne},r),{default:()=>[l?c.value(a,e.shortMonths)+" "+o.dayFormatter.value(a,!1):o.dayFormatter.value(a,!1)]})}return Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-calendar-weekly",r.themeClasses.value]),onDragstart:e=>e.preventDefault()},[e.hideHeader?void 0:t.createElementVNode("div",{class:"v-calendar-weekly__head",role:"row"},[v()]),m()])),{...o,days:s,todayWeek:u,monthFormatter:c,isOutside:d}}})
function Yu(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0
const a=e.map(e=>({event:e,columnCount:0,column:0,left:0,width:100}))
return a.sort((e,a)=>Math.max(t,e.event.startTimestampIdentifier)-Math.max(t,a.event.startTimestampIdentifier)||a.event.endTimestampIdentifier-e.event.endTimestampIdentifier),a}function Uu(e,t,a,l){return!(arguments.length>4&&void 0!==arguments[4])||arguments[4]?!(e>=l||t<=a):!(e>l||t<a)}function Gu(e){e.forEach(t=>{t.visuals.forEach(t=>{t.columnCount=e.length})})}function Ku(e){return[e.startTimestampIdentifier,e.endTimestampIdentifier]}function qu(e){return[e.startIdentifier,e.endIdentifier]}function Xu(e,t){return[Math.max(t,e.startTimestampIdentifier),Math.min(t+864e5,e.endTimestampIdentifier)]}function Zu(e){const t={groups:[],min:-1,max:-1,reset:()=>{t.groups=[],t.min=t.max=-1},getVisuals:function(a,l,n){let o=arguments.length>3&&void 0!==arguments[3]&&arguments[3];(a.weekday===e||o)&&t.reset()
const r=Yu(l,Hs(a))
return r.forEach(e=>{const[a,l]=n?Ku(e.event):qu(e.event)
t.groups.length>0&&!Uu(a,l,t.min,t.max,n)&&(Gu(t.groups),t.reset())
let o=function(e,t,a,l){for(let n=0;n<e.length;n++){const o=e[n]
let r=!1
if(Uu(t,a,o.start,o.end,l))for(let e=0;e<o.visuals.length;e++){const n=o.visuals[e],[i,s]=l?Ku(n.event):qu(n.event)
if(Uu(t,a,i,s,l)){r=!0
break}}if(!r)return n}return-1}(t.groups,a,l,n);-1===o&&(o=t.groups.length,t.groups.push({start:a,end:l,visuals:[]}))
const r=t.groups[o]
r.visuals.push(e),r.start=Math.min(r.start,a),r.end=Math.max(r.end,l),e.column=o,-1===t.min?(t.min=a,t.max=l):(t.min=Math.min(t.min,a),t.max=Math.max(t.max,l))}),Gu(t.groups),n&&t.reset(),r}}
return t}const Qu=100
function Ju(e,t){for(const a of e){const{visual:l,parent:n}=a,o=rc(a)+1,r=n?n.visual.left:0,i=Qu-r,s=Math.min(5,Qu/o),u=ec(a,e),c=i/(o-a.index+1),d=i/(o-a.index+(a.sibling?1:0))*u
n&&(l.left=a.sibling?r+c:r+s),l.width=nc(a,e,t)?Qu-l.left:Math.min(Qu-l.left,1.7*d)}}function ec(e,t){if(!e.children.length)return 1
const a=e.index+t.length
return e.children.reduce((e,t)=>Math.min(e,t.index),a)-e.index}function tc(e,t){const a=function(e,t){const a=[]
for(const l of t)Uu(e.start,e.end,l.start,l.end)&&a.push(l.index)
return a}(e,t)
a.sort()
for(let e=0;e<a.length;e++)if(e<a[e])return e
return!1}function ac(e,t,a,l){let n=arguments.length>4&&void 0!==arguments[4]&&arguments[4]
const o=[]
for(const n of t)n.index>=a&&n.index<=l&&Uu(e.start,e.end,n.start,n.end)&&o.push(n)
if(n&&o.length>0){const e=o.reduce((e,t)=>Math.min(e,t.index),o[0].index)
return o.filter(t=>t.index===e)}return o}function lc(e,t){let a=null
for(const l of t)Uu(e.start,e.end,l.start,l.end)&&(null===a||l.index>a.index)&&(a=l)
return a}function nc(e,t,a){for(const l of t)if(l!==e&&l.index>e.index&&Uu(e.start,ic(e.start,a),l.start,l.end))return!1
return!0}function oc(e,t){const[a,l]=Xu(e.event,t)
return{parent:null,sibling:!0,index:0,visual:e,start:a,end:l,children:[]}}function rc(e){let t=e.index
for(const a of e.children){const e=rc(a)
e>t&&(t=e)}return t}function ic(e,t){const a=e%100,l=a+t
return e-a+100*Math.floor(l/60)+l%60}const sc={stack:(e,t,a)=>{const l=Zu(t)
return(e,t,n,o)=>{if(!n)return l.getVisuals(e,t,n,o)
const r=Hs(e),i=Yu(t,r),s=function(e,t){const a=[]
for(const l of e){const[e,n]=Xu(l.event,t)
let o=!1
for(const t of a)if(Uu(e,n,t.start,t.end)){t.visuals.push(l),t.end=Math.max(t.end,n),o=!0
break}o||a.push({start:e,end:n,visuals:[l]})}return a}(i,r)
for(const e of s){const t=[]
for(const l of e.visuals){const e=oc(l,r),n=tc(e,t)
if(!1===n){const l=lc(e,t)
l&&(e.parent=l,e.sibling=Uu(e.start,e.end,l.start,ic(l.start,a)),e.index=l.index+1,l.children.push(e))}else{const[l]=ac(e,t,n-1,n-1),o=ac(e,t,n+1,n+t.length,!0)
e.children=o,e.index=n,l&&(e.parent=l,e.sibling=Uu(e.start,e.end,l.start,ic(l.start,a)),l.children.push(e))
for(const t of o){t.parent===l&&(t.parent=e)
t.index-e.index<=1&&e.sibling&&Uu(e.start,ic(e.start,a),t.start,t.end)&&(t.sibling=!0)}}t.push(e)}Ju(t,a)}return i.sort((e,t)=>e.left-t.left||e.event.startTimestampIdentifier-t.event.startTimestampIdentifier),i}},column:(e,t,a)=>{const l=Zu(t)
return(e,t,a,n)=>{const o=l.getVisuals(e,t,a,n)
return a&&o.forEach(e=>{e.left=100*e.column/e.columnCount,e.width=100/e.columnCount}),o}}}
function uc(e,t){return t>=e.startIdentifier&&t<=e.endIdentifier}function cc(e,t,a,l){return a===e.startIdentifier||l===t.weekday&&uc(e,a)}const dc=vt({events:{type:Array,default:()=>[]},eventStart:{type:String,default:"start"},eventEnd:{type:String,default:"end"},eventTimed:{type:[String,Function],default:"timed"},eventCategory:{type:[String,Function],default:"category"},eventHeight:{type:Number,default:20},eventColor:{type:[String,Function],default:"primary"},eventTextColor:{type:[String,Function]},eventName:{type:[String,Function],default:"name"},eventOverlapThreshold:{type:[String,Number],default:60},eventOverlapMode:{type:[String,Function],default:"stack",validate:e=>e in sc||"function"==typeof e},eventMore:{type:Boolean,default:!0},eventMoreText:{type:String,default:"$vuetify.calendar.moreEvents"},eventRipple:{type:[Boolean,Object],default:null},eventMarginBottom:{type:Number,default:1}},"VCalendar-events")
function vc(e,a,l){const n=Au(e),o=t.computed(()=>!Array.isArray(e.events)||0===e.events.length),r=t.computed(()=>"category"===e.type),i=t.computed(()=>"function"==typeof e.eventTimed?e.eventTimed:t=>!!t[e.eventTimed]),s=t.computed(()=>"function"==typeof e.eventCategory?e.eventCategory:t=>t[e.eventCategory]),u=t.computed(()=>e.events?e.events.map((t,a)=>function(e,t,a,l){let n=arguments.length>4&&void 0!==arguments[4]&&arguments[4],o=arguments.length>5&&void 0!==arguments[5]&&arguments[5]
const r=e[a],i=e[l],s=zs(r,!0),u=i?zs(i,!0):s,c=Ys(r)?Us(s,n):s,d=Ys(i)?Us(u,n):u,v=Os(c),p=Hs(c),m=Os(d),f=c.hasTime?0:2359
return{input:e,start:c,startIdentifier:v,startTimestampIdentifier:p,end:d,endIdentifier:m,endTimestampIdentifier:Hs(d)+f,allDay:!c.hasTime,index:t,category:o}}(t,a,e.eventStart||"",e.eventEnd||"",i.value(t),!!r.value&&s.value(t))):[]),c=t.computed(()=>parseInt(String(e.eventOverlapThreshold||0))),d=t.computed(()=>"function"==typeof e.eventTextColor?e.eventTextColor:()=>e.eventTextColor),v=t.computed(()=>"function"==typeof e.eventName?e.eventName:(t,a)=>t.input[e.eventName]||""),p=t.computed(()=>"function"==typeof e.eventOverlapMode?e.eventOverlapMode:sc[e.eventOverlapMode]),m=t.computed(()=>n.effectiveWeekdays.value)
function f(t){return"function"==typeof e.eventColor?e.eventColor(t):t.color||e.eventColor}const g=t.ref([])
function h(){const e={},t=g.value
return t&&t.length?(t.forEach(t=>{const a=t.getAttribute("data-date")
t.parentElement&&a&&(a in e||(e[a]={parent:t.parentElement,more:null,events:[]}),t.getAttribute("data-more")?e[a].more=t:(e[a].events.push(t),t.style.display=""))}),e):e}function y(t,a){let{event:l}=t
const n=e.eventHeight||0,o=e.eventMarginBottom||0,i=Os(a),s=a.week,u=i===l.startIdentifier
let c=i===l.endIdentifier,d=95
if(!r.value)for(let e=a.index+1;e<s.length;e++){const t=Os(s[e])
if(!(l.endIdentifier>=t)){c=!0
break}d+=100,c=c||t===l.endIdentifier}return V(l,{eventParsed:l,day:a,start:u,end:c,timed:!1},!1,{class:["v-event",{"v-event-start":u,"v-event-end":c}],style:{height:`${n}px`,width:`${d}%`,marginBottom:`${o}px`},"data-date":a.date})}function b(t,a){let{event:l,left:n,width:o}=t
const r=a.timeDelta(l.start,a),i=a.timeDelta(l.end,a)
if(!1===i||!1===r||i<0||r>=1||function(e,t){return"00:00"===e.end.time&&e.end.date===t.date&&e.start.date!==t.date}(l,a))return!1
const s=Os(a),u=l.startIdentifier>=s,c=l.endIdentifier>s,d=a.timeToY(l.start,a),v=a.timeToY(l.end,a)
return V(l,{eventParsed:l,day:a,start:u,end:c,timed:!0},!0,{class:"v-event-timed",style:{top:`${d}px`,height:`${Math.max(e.eventHeight||0,v-d)}px`,left:`${n}%`,width:`${o}%`}})}function V(o,r,i,s){const u=a.event,p=d.value(o.input),m=f(o.input),h=o.start.hour<12&&o.end.hour>=12,y=(b=o.start,525600*((V=o.end).year-b.year)+43800*(V.month-b.month)+1440*(V.day-b.day)+60*(V.hour-b.hour)+(V.minute-b.minute)<=c.value)
var b,V
const k=(e,t)=>n.getFormatter({timeZone:"UTC",hour:"numeric",minute:e.minute>0?"numeric":void 0})(e,!0),S=()=>k(o.start)+" - "+k(o.end),x=()=>{const e=v.value(o,i)
if(o.start.hasTime){if(i){const a=S(),l=y?", ":t.createElementVNode("br",null,null)
return t.createElementVNode("span",{class:"v-event-summary"},[t.createElementVNode("strong",null,[e]),l,a])}{const a=k(o.start)
return t.createElementVNode("span",{class:"v-event-summary"},[t.createElementVNode("strong",null,[a]),t.createTextVNode(" "),e])}}return t.createElementVNode("span",{class:"v-event-summary"},[e])},N={...r,event:o.input,outside:r.day.outside,singline:y,overlapsNoon:h,formatTime:k,timeSummary:S,eventSummary:x},C=_t(l,":event",e=>({...N,nativeEvent:e}))
return t.withDirectives(t.createElementVNode("div",t.mergeProps(n.getColorProps({text:p,background:m}),C,s,{ref_for:!0,ref:g}),[u?.(N)??w(x)]),[[Dn,e.eventRipple??!0]])}function w(e){return t.createElementVNode("div",{class:"pl-1"},[e()])}function k(a){const l=(e.eventHeight||0)+(e.eventMarginBottom||0)
return t.createElementVNode("div",{style:{height:`${l}px`},"data-date":a.date,ref_for:!0,ref:g},null)}function S(a){const n=e.eventHeight||0,o=e.eventMarginBottom||0,r=_t(l,":more",e=>({nativeEvent:e,...a}))
return t.withDirectives(t.createElementVNode("div",t.mergeProps({class:["v-event-more pl-1",{"v-outside":a.outside}],"data-date":a.date,"data-more":"1",style:{display:"none",height:`${n}px`,marginBottom:`${o}px`},ref_for:!0,ref:g},r),null),[[Dn,e.eventRipple??!0]])}function x(e,t){return!r.value||"object"==typeof t&&t.categoryName&&t.categoryName===e.category||"string"==typeof e.category&&t===e.category||"string"!=typeof e.category&&null===t}function N(e){const t=Os(e),a=m.value[0]
return u.value.filter(l=>cc(l,e,t,a))}function C(e){const t=Os(e),a=m.value[0]
return u.value.filter(l=>l.allDay&&(r.value?uc(l,t):cc(l,e,t,a))&&x(l,e.category))}function E(e){return u.value.filter(t=>!t.allDay&&function(e,t,a){if(a){const l=eu(Zs(t),a[0]),n=eu(Zs(t),a[1]),o=e.startTimestampIdentifier<Hs(n),r=e.endTimestampIdentifier>Hs(l)
return o&&r}return uc(e,Os(t))}(t,e,e.intervalRange)&&x(t,e.category))}return{...n,noEvents:o,parsedEvents:u,parsedEventOverlapThreshold:c,eventTimedFunction:i,eventCategoryFunction:s,eventTextColorFunction:d,eventNameFunction:v,eventModeFunction:p,eventWeekdays:m,categoryMode:r,eventColorFunction:f,eventsRef:g,updateEventVisibility:function(){if(o.value||!e.eventMore)return
const t=e.eventHeight||0,a=h()
for(const l in a){const{parent:o,events:r,more:i}=a[l]
if(!i)break
const s=o.getBoundingClientRect(),u=r.length-1,c=r.map(e=>({event:e,bottom:e.getBoundingClientRect().bottom})).sort((e,t)=>e.bottom-t.bottom)
let d=0
for(let e=0;e<=u;e++){const a=c[e].bottom;(e===u?a>s.bottom:a+t>s.bottom)&&(c[e].event.style.display="none",d++)}d?(i.style.display="",i.innerHTML=n.locale.t(e.eventMoreText,d)):i.style.display="none"}},getEventsMap:h,genDayEvent:y,genTimedEvent:b,genEvent:V,genName:w,genPlaceholder:k,genMore:S,getVisibleEvents:function(){const e=n.days.value,t=Os(e[0]),a=Os(e[e.length-1])
return u.value.filter(e=>function(e,t,a){return t<=e.endIdentifier&&a>=e.startIdentifier}(e,t,a))},isEventForCategory:x,getEventsForDay:N,getEventsForDayAll:C,getEventsForDayTimed:E,getScopedSlots:function(){if(o.value)return{...a}
const l=p.value(u.value,m.value[0],c.value),n=e=>!!e,i=(e,t,a,o)=>{const i=t(e),s=l(e,i,o,r.value)
if(o)return s.map(t=>a(t,e)).filter(n)
const u=[]
return s.forEach((t,l)=>{for(;u.length<t.column;)u.push(k(e))
const n=a(t,e)
n&&u.push(n)}),u}
return{...a,day:t=>{let l=i(t,N,y,!1)
if(l&&l.length>0&&e.eventMore&&l.push(S(t)),a.day){const e=a.day(t)
e&&(l=l?l.concat(e):e)}return l},"day-header":e=>{let t=i(e,C,y,!1)
if(a["day-header"]){const l=a["day-header"](e)
l&&(t=t?t.concat(l):l)}return t},"day-body":e=>{const l=i(e,E,b,!0)
let n=[t.createElementVNode("div",{class:"v-event-timed-container"},[l])]
if(a["day-body"]){const t=a["day-body"](e)
t&&(n=n.concat(t))}return n}}}}}const pc=wt()({name:"VCalendar",directives:{vResize:Bu},props:{modelValue:{type:[String,Number,Date],validate:Ms},categoryDays:{type:[Number,String],default:1,validate:e=>isFinite(parseInt(e))&&parseInt(e)>0},categories:{type:[Array,String],default:""},categoryText:{type:[String,Function]},maxDays:{type:Number,default:7},categoryHideDynamic:{type:Boolean},categoryShowAll:{type:Boolean},categoryForInvalid:{type:String,default:""},...Pu(),...dc()},setup(e,a){let{slots:l,attrs:n,emit:o}=a
const r=t.ref(),i=vc(e,l,n),s=t.ref(null),u=t.ref(null),c=t.computed(()=>parseInt(String(e.categoryDays))||1),d=t.computed(()=>Fu(e.categories,e.categoryText)),v=t.computed(()=>{const t=i.parsedValue.value
let a=null,l=e.maxDays,n=d.value,o=t,r=t
switch(e.type){case"month":a=Wu,o=Bs(t),r=Ds(t)
break
case"week":a=Du,o=i.getStartOfWeek(t),r=i.getEndOfWeek(t),l=7
break
case"day":a=Du,l=1
break
case"4day":a=Du,r=lu(Zs(r),tu,3),qs(r),l=4
break
case"custom-weekly":a=Wu,o=i.parsedStart.value||t,r=i.parsedEnd.value
break
case"custom-daily":a=Du,o=i.parsedStart.value||t,r=i.parsedEnd.value
break
case"category":const s=c.value
a=$u,r=lu(Zs(r),tu,s),qs(r),l=s,n=V(n)
break
default:const u=e.type
throw new Error(`${u} is not a valid Calendar type`)}return{component:a,start:o,end:r,maxDays:l,categories:n}}),p=t.computed(()=>i.effectiveWeekdays.value),m=t.computed(()=>"category"===e.type),f=t.computed(()=>i.getFormatter({timeZone:"UTC",month:"long"})),g=t.computed(()=>i.getFormatter({timeZone:"UTC",month:"short"})),h=t.computed(()=>{const{start:e,end:t}=v.value,a=e.year!==t.year,l=a||e.month!==t.month
return a?g.value(e,!0)+" "+e.year+" - "+g.value(t,!0)+" "+t.year:l?g.value(e,!0)+" - "+g.value(t,!0)+" "+t.year:f.value(e,!1)+" "+e.year})
function y(){const{start:e,end:t}=v.value
s.value&&u.value&&e.date===s.value.date&&t.date===u.value.date||(s.value=e,u.value=t,o("change",{start:e,end:t}))}function b(){let t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1
const a=Zs(i.parsedValue.value),l=t>0,n=l?tu:au,r=l?31:1
let s=l?t:-t
for(;--s>=0;)switch(e.type){case"month":a.day=r,n(a)
break
case"week":lu(a,n,7)
break
case"day":lu(a,n,1)
break
case"4day":lu(a,n,4)
break
case"category":lu(a,n,c.value)}Ks(a),qs(a),Ws(a,i.times.now),e.modelValue instanceof Date?o("update:modelValue",ou(a)):"number"==typeof e.modelValue?o("update:modelValue",ou(a).getTime()):o("update:modelValue",a.date),o("moved",a)}function V(t){if(!i.noEvents.value){const a=t.reduce((e,t,a)=>("object"==typeof t&&t.categoryName?e[t.categoryName]={index:a,count:0}:"string"==typeof t&&(e[t]={index:a,count:0}),e),{})
if(!e.categoryHideDynamic||!e.categoryShowAll){let l=t.length
i.parsedEvents.value.forEach(t=>{let n=t.category
"string"!=typeof n&&(n=e.categoryForInvalid),n&&(n in a?a[n].count++:e.categoryHideDynamic||(a[n]={index:l++,count:1}))})}if(!e.categoryShowAll)for(const e in a)0===a[e].count&&delete a[e]
t=t.filter(e=>"object"==typeof e&&e.categoryName?a.hasOwnProperty(e.categoryName):"string"==typeof e&&a.hasOwnProperty(e))}return t}return t.watch(v,y),t.onMounted(()=>{i.updateEventVisibility(),y()}),t.onUpdated(()=>{window.requestAnimationFrame(i.updateEventVisibility)}),Bt(()=>{const{start:a,end:l,maxDays:s,component:u,categories:c}=v.value
return t.withDirectives(t.createVNode(u,t.mergeProps({ref:r,class:["v-calendar",{"v-calendar-events":!i.noEvents.value}],role:"grid"},u.filterProps(e),{start:a.date,end:l.date,maxDays:s,weekdays:i.effectiveWeekdays.value,categories:c,"onClick:date":(e,t)=>{n["onUpdate:modelValue"]&&o("update:modelValue",t.date)}}),i.getScopedSlots()),[[Bu,i.updateEventVisibility,void 0,{quiet:!0}]])}),wo({...i,lastStart:s,lastEnd:u,parsedCategoryDays:c,renderProps:v,eventWeekdays:p,categoryMode:m,title:h,monthLongFormatter:f,monthShortFormatter:g,parsedCategories:d,checkChange:y,move:b,next:function(){b(arguments.length>0&&void 0!==arguments[0]?arguments[0]:1)},prev:function(){b(-(arguments.length>0&&void 0!==arguments[0]?arguments[0]:1))},getCategoryList:V},r)}}),mc=vt({...pt(),...Pa()},"VCardActions"),fc=wt()({name:"VCardActions",props:mc(),setup(e,a){let{slots:l}=a
return yt({VBtn:{slim:!0,variant:"text"}}),Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-card-actions",e.class]),style:t.normalizeStyle(e.style)},l)),{}}}),gc=vt({opacity:[Number,String],...pt(),...Pa()},"VCardSubtitle"),hc=wt()({name:"VCardSubtitle",props:gc(),setup(e,a){let{slots:l}=a
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-card-subtitle",e.class]),style:t.normalizeStyle([{"--v-card-subtitle-opacity":e.opacity},e.style])},l)),{}}}),yc=kt("v-card-title"),bc=vt({appendAvatar:String,appendIcon:Dt,prependAvatar:String,prependIcon:Dt,subtitle:{type:[String,Number,Boolean],default:void 0},title:{type:[String,Number,Boolean],default:void 0},...pt(),...Tl(),...Pa()},"VCardItem"),Vc=wt()({name:"VCardItem",props:bc(),setup(e,a){let{slots:l}=a
return Bt(()=>{const a=!(!e.prependAvatar&&!e.prependIcon),n=!(!a&&!l.prepend),o=!(!e.appendAvatar&&!e.appendIcon),r=!(!o&&!l.append),i=!(null==e.title&&!l.title),s=!(null==e.subtitle&&!l.subtitle)
return t.createVNode(e.tag,{class:t.normalizeClass(["v-card-item",e.class]),style:t.normalizeStyle(e.style)},{default:()=>[n&&t.createElementVNode("div",{key:"prepend",class:"v-card-item__prepend"},[l.prepend?t.createVNode(nl,{key:"prepend-defaults",disabled:!a,defaults:{VAvatar:{density:e.density,image:e.prependAvatar},VIcon:{density:e.density,icon:e.prependIcon}}},l.prepend):t.createElementVNode(t.Fragment,null,[e.prependAvatar&&t.createVNode(Kn,{key:"prepend-avatar",density:e.density,image:e.prependAvatar},null),e.prependIcon&&t.createVNode(Jl,{key:"prepend-icon",density:e.density,icon:e.prependIcon},null)])]),t.createElementVNode("div",{class:"v-card-item__content"},[i&&t.createVNode(yc,{key:"title"},{default:()=>[l.title?.()??t.toDisplayString(e.title)]}),s&&t.createVNode(hc,{key:"subtitle"},{default:()=>[l.subtitle?.()??t.toDisplayString(e.subtitle)]}),l.default?.()]),r&&t.createElementVNode("div",{key:"append",class:"v-card-item__append"},[l.append?t.createVNode(nl,{key:"append-defaults",disabled:!o,defaults:{VAvatar:{density:e.density,image:e.appendAvatar},VIcon:{density:e.density,icon:e.appendIcon}}},l.append):t.createElementVNode(t.Fragment,null,[e.appendIcon&&t.createVNode(Jl,{key:"append-icon",density:e.density,icon:e.appendIcon},null),e.appendAvatar&&t.createVNode(Kn,{key:"append-avatar",density:e.density,image:e.appendAvatar},null)])])]})}),{}}}),wc=vt({opacity:[Number,String],...pt(),...Pa()},"VCardText"),kc=wt()({name:"VCardText",props:wc(),setup(e,a){let{slots:l}=a
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-card-text",e.class]),style:t.normalizeStyle([{"--v-card-text-opacity":e.opacity},e.style])},l)),{}}}),Sc=vt({appendAvatar:String,appendIcon:Dt,disabled:Boolean,flat:Boolean,hover:Boolean,image:String,link:{type:Boolean,default:void 0},prependAvatar:String,prependIcon:Dt,ripple:{type:[Boolean,Object],default:!0},subtitle:{type:[String,Number,Boolean],default:void 0},text:{type:[String,Number,Boolean],default:void 0},title:{type:[String,Number,Boolean],default:void 0},...wl(),...pt(),...Tl(),...ol(),...Sl(),...cn(),...nn(),...mn(),...pl(),...yn(),...Pa(),...ya(),...$l({variant:"elevated"})},"VCard"),xc=wt()({name:"VCard",directives:{vRipple:Dn},props:Sc(),setup(e,a){let{attrs:l,slots:n}=a
const{themeClasses:o}=Ca(e),{borderClasses:r}=kl(e),{colorClasses:i,colorStyles:s,variantClasses:u}=Ml(e),{densityClasses:c}=Bl(e),{dimensionStyles:d}=rl(e),{elevationClasses:v}=xl(e),{loaderClasses:p}=dn(e),{locationStyles:m}=on(e),{positionClasses:f}=fn(e),{roundedClasses:g}=ml(e),h=hn(e,l),y=t.shallowRef(void 0)
return t.watch(()=>e.loading,(e,t)=>{y.value=e||"string"!=typeof t?"boolean"==typeof e?void 0:e:t},{immediate:!0}),Bt(()=>{const a=!1!==e.link&&h.isLink.value,l=!e.disabled&&!1!==e.link&&(e.link||h.isClickable.value),b=a?"a":e.tag,V=!(!n.title&&null==e.title),w=!(!n.subtitle&&null==e.subtitle),k=V||w,S=!!(n.append||e.appendAvatar||e.appendIcon),x=!!(n.prepend||e.prependAvatar||e.prependIcon),N=!(!n.image&&!e.image),C=k||x||S,E=!(!n.text&&null==e.text)
return t.withDirectives(t.createVNode(b,t.mergeProps(h.linkProps,{class:["v-card",{"v-card--disabled":e.disabled,"v-card--flat":e.flat,"v-card--hover":e.hover&&!(e.disabled||e.flat),"v-card--link":l},o.value,r.value,i.value,c.value,v.value,p.value,f.value,g.value,u.value,e.class],style:[s.value,d.value,m.value,e.style],onClick:l&&h.navigate,tabindex:e.disabled?-1:void 0}),{default:()=>[N&&t.createElementVNode("div",{key:"image",class:"v-card__image"},[n.image?t.createVNode(nl,{key:"image-defaults",disabled:!e.image,defaults:{VImg:{cover:!0,src:e.image}}},n.image):t.createVNode(Vl,{key:"image-img",cover:!0,src:e.image},null)]),t.createVNode(vn,{name:"v-card",active:!!e.loading,color:y.value},{default:n.loader}),C&&t.createVNode(Vc,{key:"item",prependAvatar:e.prependAvatar,prependIcon:e.prependIcon,title:e.title,subtitle:e.subtitle,appendAvatar:e.appendAvatar,appendIcon:e.appendIcon},{default:n.item,prepend:n.prepend,title:n.title,subtitle:n.subtitle,append:n.append}),E&&t.createVNode(kc,{key:"text"},{default:()=>[n.text?.()??e.text]}),n.default?.(),n.actions&&t.createVNode(fc,null,{default:n.actions}),Fl(l,"v-card")]}),[[Dn,l&&e.ripple]])}),{}}})
function Nc(e,t){const a=e.changedTouches[0]
t.touchendX=a.clientX,t.touchendY=a.clientY,t.end?.({originalEvent:e,...t}),(e=>{const{touchstartX:t,touchendX:a,touchstartY:l,touchendY:n}=e
e.offsetX=a-t,e.offsetY=n-l,Math.abs(e.offsetY)<.5*Math.abs(e.offsetX)&&(e.left&&a<t-16&&e.left(e),e.right&&a>t+16&&e.right(e)),Math.abs(e.offsetX)<.5*Math.abs(e.offsetY)&&(e.up&&n<l-16&&e.up(e),e.down&&n>l+16&&e.down(e))})(t)}const Cc={mounted:function(e,t){const a=t.value,l=a?.parent?e.parentElement:e,n=a?.options??{passive:!0},o=t.instance?.$.uid
if(!l||void 0===o)return
const r=function(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}
const t={touchstartX:0,touchstartY:0,touchendX:0,touchendY:0,touchmoveX:0,touchmoveY:0,offsetX:0,offsetY:0,left:e.left,right:e.right,up:e.up,down:e.down,start:e.start,move:e.move,end:e.end}
return{touchstart:e=>function(e,t){const a=e.changedTouches[0]
t.touchstartX=a.clientX,t.touchstartY=a.clientY,t.start?.({originalEvent:e,...t})}(e,t),touchend:e=>Nc(e,t),touchmove:e=>function(e,t){const a=e.changedTouches[0]
t.touchmoveX=a.clientX,t.touchmoveY=a.clientY,t.move?.({originalEvent:e,...t})}(e,t)}}(t.value)
l._touchHandlers=l._touchHandlers??Object.create(null),l._touchHandlers[o]=r,x(r).forEach(e=>{l.addEventListener(e,r[e],n)})},unmounted:function(e,t){const a=t.value?.parent?e.parentElement:e,l=t.instance?.$.uid
if(!a?._touchHandlers||void 0===l)return
const n=a._touchHandlers[l]
x(n).forEach(e=>{a.removeEventListener(e,n[e])}),delete a._touchHandlers[l]}},Ec=Symbol.for("vuetify:v-window"),Ic=Symbol.for("vuetify:v-window-group"),_c=vt({continuous:Boolean,nextIcon:{type:[Boolean,String,Function,Object],default:"$next"},prevIcon:{type:[Boolean,String,Function,Object],default:"$prev"},reverse:Boolean,showArrows:{type:[Boolean,String],validator:e=>"boolean"==typeof e||"hover"===e},verticalArrows:[Boolean,String],touch:{type:[Object,Boolean],default:void 0},direction:{type:String,default:"horizontal"},modelValue:null,disabled:Boolean,selectedClass:{type:String,default:"v-window-item--active"},mandatory:{type:[Boolean,String],default:"force"},crossfade:Boolean,transitionDuration:Number,...pt(),...Pa(),...ya()},"VWindow"),Pc=wt()({name:"VWindow",directives:{vTouch:Cc},props:_c(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ca(e),{isRtl:r}=ga(),{t:i}=ma(),s=Wl(e,Ic),u=t.ref(),d=t.computed(()=>r.value?!e.reverse:e.reverse),v=t.shallowRef(!1),p=t.computed(()=>{if(e.crossfade)return"v-window-crossfade-transition"
return`v-window-${"vertical"===e.direction?"y":"x"}${(d.value?!v.value:v.value)?"-reverse":""}-transition`}),m=t.shallowRef(0),f=t.ref(void 0),g=t.computed(()=>s.items.value.findIndex(e=>s.selected.value.includes(e.id)))
t.watch(g,(e,a)=>{let l
const n={left:0,top:0}
o&&a>=0&&(l=Pt(u.value),n.left=l?.scrollLeft,n.top=l?.scrollTop)
const r=s.items.value.length,i=r-1
v.value=r<=2?e<a:(e!==i||0!==a)&&(0===e&&a===i||e<a),t.nextTick(()=>{if(!o||!l)return
l.scrollTop!==n.top&&l.scrollTo({...n,behavior:"instant"}),requestAnimationFrame(()=>{if(!l)return
l.scrollTop!==n.top&&l.scrollTo({...n,behavior:"instant"})})})},{flush:"sync"}),t.provide(Ec,{transition:p,isReversed:v,transitionCount:m,transitionHeight:f,rootRef:u})
const h=t.toRef(()=>e.continuous||0!==g.value),y=t.toRef(()=>e.continuous||g.value!==s.items.value.length-1)
function V(){h.value&&s.prev()}function w(){y.value&&s.next()}const k=t.computed(()=>{const a=[],n={icon:r.value?e.nextIcon:e.prevIcon,class:"v-window__"+(d.value?"right":"left"),onClick:s.prev,"aria-label":i("$vuetify.carousel.prev")}
a.push(h.value?l.prev?l.prev({props:n}):t.createVNode($n,n,null):t.createElementVNode("div",null,null))
const o={icon:r.value?e.prevIcon:e.nextIcon,class:"v-window__"+(d.value?"left":"right"),onClick:s.next,"aria-label":i("$vuetify.carousel.next")}
return a.push(y.value?l.next?l.next({props:o}):t.createVNode($n,o,null):t.createElementVNode("div",null,null)),a}),S=t.computed(()=>{if(!1===e.touch)return e.touch
return{...{left:()=>{d.value?V():w()},right:()=>{d.value?w():V()},start:e=>{let{originalEvent:t}=e
t.stopPropagation()}},...!0===e.touch?{}:e.touch}})
return Bt(()=>t.withDirectives(t.createVNode(e.tag,{ref:u,class:t.normalizeClass(["v-window",{"v-window--show-arrows-on-hover":"hover"===e.showArrows,"v-window--vertical-arrows":!!e.verticalArrows,"v-window--crossfade":!!e.crossfade},n.value,e.class]),style:t.normalizeStyle([e.style,{"--v-window-transition-duration":c()?null:b(e.transitionDuration,"ms")}])},{default:()=>[t.createElementVNode("div",{class:"v-window__container",style:{height:f.value}},[l.default?.({group:s}),!1!==e.showArrows&&t.createElementVNode("div",{class:t.normalizeClass(["v-window__controls",{"v-window__controls--left":"left"===e.verticalArrows||!0===e.verticalArrows},{"v-window__controls--right":"right"===e.verticalArrows}])},[k.value])]),l.additional?.({group:s})]}),[[Cc,S.value]])),{group:s}}}),Ac=vt({color:String,cycle:Boolean,delimiterIcon:{type:Dt,default:"$delimiter"},height:{type:[Number,String],default:500},hideDelimiters:Boolean,hideDelimiterBackground:Boolean,interval:{type:[Number,String],default:6e3,validator:e=>Number(e)>0},progress:[Boolean,String],verticalDelimiters:[Boolean,String],..._c({continuous:!0,mandatory:"force",showArrows:!0})},"VCarousel"),Rc=wt()({name:"VCarousel",props:Ac(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=la(e,"modelValue"),{t:o}=ma(),r=t.ref()
let i=-1
function s(){e.cycle&&r.value&&(i=window.setTimeout(r.value.group.next,Number(e.interval)>0?Number(e.interval):6e3))}function u(){window.clearTimeout(i),window.requestAnimationFrame(s)}return t.watch(n,u),t.watch(()=>e.interval,u),t.watch(()=>e.cycle,e=>{e?u():window.clearTimeout(i)}),t.onMounted(s),Bt(()=>{const a=Pc.filterProps(e)
return t.createVNode(Pc,t.mergeProps({ref:r},a,{modelValue:n.value,"onUpdate:modelValue":e=>n.value=e,class:["v-carousel",{"v-carousel--hide-delimiter-background":e.hideDelimiterBackground,"v-carousel--vertical-delimiters":e.verticalDelimiters},e.class],style:[{height:b(e.height)},e.style]}),{default:l.default,additional:a=>{let{group:r}=a
return t.createElementVNode(t.Fragment,null,[!e.hideDelimiters&&t.createElementVNode("div",{class:"v-carousel__controls",style:{left:"left"===e.verticalDelimiters&&e.verticalDelimiters?0:"auto",right:"right"===e.verticalDelimiters?0:"auto"}},[r.items.value.length>0&&t.createVNode(nl,{defaults:{VBtn:{color:e.color,icon:e.delimiterIcon,size:"x-small",variant:"text"}},scoped:!0},{default:()=>[r.items.value.map((e,a)=>{const n={id:`carousel-item-${e.id}`,"aria-label":o("$vuetify.carousel.ariaLabel.delimiter",a+1,r.items.value.length),class:["v-carousel__controls__item",r.isSelected(e.id)&&"v-btn--active"],onClick:()=>r.select(e.id,!0)}
return l.item?l.item({props:n,item:e}):t.createVNode($n,t.mergeProps(e,n),null)})]})]),e.progress&&t.createVNode(un,{absolute:!0,class:"v-carousel__progress",color:"string"==typeof e.progress?e.progress:void 0,modelValue:(r.getItemIndex(n.value)+1)/r.items.value.length*100},null)])},prev:l.prev,next:l.next})}),{}}}),Tc=vt({reverseTransition:{type:[Boolean,String],default:void 0},transition:{type:[Boolean,String],default:void 0},...pt(),...jl(),...gi()},"VWindowItem"),Bc=wt()({name:"VWindowItem",directives:{vTouch:Cc},props:Tc(),emits:{"group:selected":e=>!0},setup(e,a){let{slots:l}=a
const n=t.inject(Ec),o=Hl(e,Ic),{isBooted:r}=_l()
if(!n||!o)throw new Error("[Vuetify] VWindowItem must be used inside VWindow")
const i=t.shallowRef(!1),s=t.computed(()=>r.value&&(n.isReversed.value?!1!==e.reverseTransition:!1!==e.transition))
function u(){i.value&&n&&(i.value=!1,n.transitionCount.value>0&&(n.transitionCount.value-=1,0===n.transitionCount.value&&(n.transitionHeight.value=void 0)))}function c(){!i.value&&n&&(i.value=!0,0===n.transitionCount.value&&(n.transitionHeight.value=b(n.rootRef.value?.clientHeight)),n.transitionCount.value+=1)}function d(){u()}function v(e){i.value&&t.nextTick(()=>{s.value&&i.value&&n&&(n.transitionHeight.value=b(e.clientHeight))})}const p=t.computed(()=>{const t=n.isReversed.value?e.reverseTransition:e.transition
return!!s.value&&{name:"string"!=typeof t?n.transition.value:t,onBeforeEnter:c,onAfterEnter:u,onEnterCancelled:d,onBeforeLeave:c,onAfterLeave:u,onLeaveCancelled:d,onEnter:v}}),{hasContent:m}=hi(e,o.isSelected)
return Bt(()=>t.createVNode(gl,{transition:p.value,disabled:!r.value},{default:()=>[t.withDirectives(t.createElementVNode("div",{class:t.normalizeClass(["v-window-item",o.selectedClass.value,e.class]),style:t.normalizeStyle(e.style)},[m.value&&l.default?.()]),[[t.vShow,o.isSelected.value]])]})),{groupItem:o}}}),Dc=vt({...bl(),...Tc()},"VCarouselItem"),Fc=wt()({name:"VCarouselItem",inheritAttrs:!1,props:Dc(),setup(e,a){let{slots:l,attrs:n}=a
Bt(()=>{const a=Vl.filterProps(e),o=Bc.filterProps(e)
return t.createVNode(Bc,t.mergeProps({class:["v-carousel-item",e.class]},o),{default:()=>[t.createVNode(Vl,t.mergeProps(n,a),l)]})})}}),$c=kt("v-code","code"),Mc=Vt({name:"VColorPickerCanvas",props:vt({color:{type:Object},disabled:Boolean,dotSize:{type:[Number,String],default:10},height:{type:[Number,String],default:150},width:{type:[Number,String],default:300},...pt()},"VColorPickerCanvas")(),emits:{"update:color":e=>!0,"update:position":e=>!0},setup(e,a){let{emit:l}=a
const n=t.shallowRef(!1),o=t.ref(),r=t.shallowRef(parseFloat(e.width)),i=t.shallowRef(parseFloat(e.height)),s=t.ref({x:0,y:0}),u=t.computed({get:()=>s.value,set(t){if(!o.value)return
const{x:a,y:n}=t
s.value=t,l("update:color",{h:e.color?.h??0,s:F(a,0,r.value)/r.value,v:1-F(n,0,i.value)/i.value,a:e.color?.a??1})}}),c=t.computed(()=>{const{x:t,y:a}=u.value,l=parseInt(e.dotSize,10)/2
return{width:b(e.dotSize),height:b(e.dotSize),transform:`translate(${b(t-l)}, ${b(a-l)})`}}),{resizeRef:d}=Kt(e=>{if(!d.el?.offsetParent)return
const{width:t,height:a}=e[0].contentRect
r.value=Math.round(t),i.value=Math.round(a)})
function v(t){"mousedown"===t.type&&t.preventDefault(),e.disabled||(p(t),window.addEventListener("mousemove",p),window.addEventListener("mouseup",m),window.addEventListener("touchmove",p),window.addEventListener("touchend",m))}function p(t){if(e.disabled||!o.value)return
n.value=!0
const a=function(e){return"touches"in e?{clientX:e.touches[0].clientX,clientY:e.touches[0].clientY}:{clientX:e.clientX,clientY:e.clientY}}(t)
!function(e,t,a){const{left:l,top:n,width:o,height:r}=a
u.value={x:F(e-l,0,o),y:F(t-n,0,r)}}(a.clientX,a.clientY,o.value.getBoundingClientRect())}function m(){window.removeEventListener("mousemove",p),window.removeEventListener("mouseup",m),window.removeEventListener("touchmove",p),window.removeEventListener("touchend",m)}function f(){if(!o.value)return
const t=o.value,a=t.getContext("2d")
if(!a)return
const l=a.createLinearGradient(0,0,t.width,0)
l.addColorStop(0,"hsla(0, 0%, 100%, 1)"),l.addColorStop(1,`hsla(${e.color?.h??0}, 100%, 50%, 1)`),a.fillStyle=l,a.fillRect(0,0,t.width,t.height)
const n=a.createLinearGradient(0,0,0,t.height)
n.addColorStop(0,"hsla(0, 0%, 0%, 0)"),n.addColorStop(1,"hsla(0, 0%, 0%, 1)"),a.fillStyle=n,a.fillRect(0,0,t.width,t.height)}return t.watch(()=>e.color?.h,f,{immediate:!0}),t.watch(()=>[r.value,i.value],(e,t)=>{f(),s.value={x:u.value.x*e[0]/t[0],y:u.value.y*e[1]/t[1]}},{flush:"post"}),t.watch(()=>e.color,()=>{n.value?n.value=!1:s.value=e.color?{x:e.color.s*r.value,y:(1-e.color.v)*i.value}:{x:0,y:0}},{deep:!0,immediate:!0}),t.onMounted(()=>f()),Bt(()=>t.createElementVNode("div",{ref:d,class:t.normalizeClass(["v-color-picker-canvas",e.class]),style:t.normalizeStyle(e.style),onMousedown:v,onTouchstartPassive:v},[t.createElementVNode("canvas",{ref:o,width:r.value,height:i.value},null),e.color&&t.createElementVNode("div",{class:t.normalizeClass(["v-color-picker-canvas__dot",{"v-color-picker-canvas__dot--disabled":e.disabled}]),style:t.normalizeStyle(c.value)},null)])),{}}})
const zc={h:0,s:0,v:0,a:1},Lc={inputProps:{type:"number",min:0},inputs:[{label:"R",max:255,step:1,getValue:e=>Math.round(e.r),getColor:(e,t)=>({...e,r:Number(t)}),localeKey:"redInput"},{label:"G",max:255,step:1,getValue:e=>Math.round(e.g),getColor:(e,t)=>({...e,g:Number(t)}),localeKey:"greenInput"},{label:"B",max:255,step:1,getValue:e=>Math.round(e.b),getColor:(e,t)=>({...e,b:Number(t)}),localeKey:"blueInput"},{label:"A",max:1,step:.01,getValue:e=>{let{a:t}=e
return null!=t?Math.round(100*t)/100:1},getColor:(e,t)=>({...e,a:Number(t)}),localeKey:"alphaInput"}],to:Xe,from:Qe},Oc={inputProps:{type:"number",min:0},inputs:[{label:"H",max:360,step:1,getValue:e=>Math.round(e.h),getColor:(e,t)=>({...e,h:Number(t)}),localeKey:"hueInput"},{label:"S",max:1,step:.01,getValue:e=>Math.round(100*e.s)/100,getColor:(e,t)=>({...e,s:Number(t)}),localeKey:"saturationInput"},{label:"L",max:1,step:.01,getValue:e=>Math.round(100*e.l)/100,getColor:(e,t)=>({...e,l:Number(t)}),localeKey:"lightnessInput"},{label:"A",max:1,step:.01,getValue:e=>{let{a:t}=e
return null!=t?Math.round(100*t)/100:1},getColor:(e,t)=>({...e,a:Number(t)}),localeKey:"alphaInput"}],to:Je,from:et},jc={inputProps:{type:"text"},inputs:[{label:"HEXA",getValue:e=>e,getColor:(e,t)=>t,localeKey:"hexaInput"}],to:rt,from:function(e){return Qe(ot(e))}},Hc={rgb:{...Lc,inputs:Lc.inputs?.slice(0,3)},rgba:Lc,hsl:{...Oc,inputs:Oc.inputs.slice(0,3)},hsla:Oc,hex:{...jc,inputs:[{label:"HEX",getValue:e=>e.slice(0,7),getColor:(e,t)=>t,localeKey:"hexInput"}]},hexa:jc},Wc=e=>{let{label:a,...l}=e
return t.createElementVNode("div",{class:"v-color-picker-edit__input"},[t.createElementVNode("input",t.normalizeProps(t.guardReactiveProps(l)),null),t.createElementVNode("span",null,[a])])},Yc=Vt({name:"VColorPickerEdit",props:vt({color:Object,disabled:Boolean,mode:{type:String,default:"rgba",validator:e=>Object.keys(Hc).includes(e)},modes:{type:Array,default:()=>Object.keys(Hc),validator:e=>Array.isArray(e)&&e.every(e=>Object.keys(Hc).includes(e))},...pt()},"VColorPickerEdit")(),emits:{"update:color":e=>!0,"update:mode":e=>!0},setup(e,a){let{emit:l}=a
const{t:n}=ma(),o=t.computed(()=>e.modes.map(e=>({...Hc[e],name:e}))),r=t.computed(()=>{const t=o.value.find(t=>t.name===e.mode)
if(!t)return[]
const a=e.color?t.to(e.color):null
return t.inputs?.map(o=>{let{getValue:r,getColor:i,localeKey:s,...u}=o
return{...t.inputProps,...u,ariaLabel:n(`$vuetify.colorPicker.ariaLabel.${s}`),disabled:e.disabled,value:a&&r(a),onChange:e=>{const n=e.target
n&&l("update:color",t.from(i(a??t.to(zc),n.value)))}}})})
return Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-color-picker-edit",e.class]),style:t.normalizeStyle(e.style)},[r.value?.map(e=>t.createVNode(Wc,e,null)),o.value.length>1&&t.createVNode($n,{icon:"$unfold",size:"x-small",variant:"plain","aria-label":n("$vuetify.colorPicker.ariaLabel.changeFormat"),onClick:()=>{const t=o.value.findIndex(t=>t.name===e.mode)
l("update:mode",o.value[(t+1)%o.value.length].name)}},null)])),{}}}),Uc=Symbol.for("vuetify:v-slider")
function Gc(e,t,a){const l="vertical"===a,n=t.getBoundingClientRect(),o="touches"in e?e.touches[0]:e
return l?o.clientY-(n.top+n.height/2):o.clientX-(n.left+n.width/2)}const Kc=vt({disabled:{type:Boolean,default:null},error:Boolean,readonly:{type:Boolean,default:null},max:{type:[Number,String],default:100},min:{type:[Number,String],default:0},step:{type:[Number,String],default:0},thumbColor:String,thumbLabel:{type:[Boolean,String],default:void 0,validator:e=>"boolean"==typeof e||"always"===e},thumbSize:{type:[Number,String],default:20},showTicks:{type:[Boolean,String],default:!1,validator:e=>"boolean"==typeof e||"always"===e},ticks:{type:[Array,Object]},tickSize:{type:[Number,String],default:2},color:String,trackColor:String,trackFillColor:String,trackSize:{type:[Number,String],default:4},direction:{type:String,default:"horizontal",validator:e=>["vertical","horizontal"].includes(e)},reverse:Boolean,noKeyboard:Boolean,...pl(),...Sl({elevation:2}),ripple:{type:Boolean,default:!0}},"Slider"),qc=e=>{const a=t.computed(()=>parseFloat(e.min)),l=t.computed(()=>parseFloat(e.max)),n=t.computed(()=>Number(e.step)>0?parseFloat(e.step):0),o=t.computed(()=>Math.max($(n.value),$(a.value)))
return{min:a,max:l,step:n,decimals:o,roundValue:function(e){if(e=parseFloat(e),n.value<=0)return e
const t=F(e,a.value,l.value),r=a.value%n.value
let i=Math.round((t-r)/n.value)*n.value+r
return t>i&&i+n.value>l.value&&(i=l.value),parseFloat(Math.min(i,l.value).toFixed(o.value))}}},Xc=e=>{let{props:a,steps:l,onSliderStart:n,onSliderMove:o,onSliderEnd:r,getActiveThumb:i}=e
const s=po(a),{isRtl:u}=ga(),c=t.toRef(()=>a.reverse),d=t.computed(()=>"vertical"===a.direction),v=t.computed(()=>d.value!==c.value),{min:p,max:m,step:f,decimals:g,roundValue:h}=l,b=t.computed(()=>parseInt(a.thumbSize,10)),V=t.computed(()=>parseInt(a.tickSize,10)),w=t.computed(()=>parseInt(a.trackSize,10)),k=t.computed(()=>(m.value-p.value)/f.value),S=t.computed(()=>a.error||s.isDisabled.value?void 0:a.thumbColor??a.color),x=t.computed(()=>a.error||s.isDisabled.value?void 0:a.thumbColor),N=t.computed(()=>a.error||s.isDisabled.value?void 0:a.trackColor??a.color),C=t.computed(()=>a.error||s.isDisabled.value?void 0:a.trackFillColor??a.color),E=t.shallowRef(!1),I=t.shallowRef(0),_=t.ref(),P=t.ref()
function A(e){const t=_.value?.$el
if(!t)return
const l="vertical"===a.direction,n=l?"top":"left",o=l?"height":"width",r=l?"clientY":"clientX",{[n]:i,[o]:s}=t.getBoundingClientRect(),c=function(e,t){return"touches"in e&&e.touches.length?e.touches[0][t]:"changedTouches"in e&&e.changedTouches.length?e.changedTouches[0][t]:e[t]}(e,r)
let d=F((c-i-I.value)/s)||0
return(l?v.value:v.value!==u.value)&&(d=1-d),h(p.value+d*(m.value-p.value))}const R=e=>{const t=A(e)
null!=t&&r({value:t}),E.value=!1,I.value=0},T=e=>{const l=A(e)
P.value=i(e),P.value&&(E.value=!0,P.value.contains(e.target)?I.value=Gc(e,P.value,a.direction):(I.value=0,null!=l&&o({value:l})),null!=l&&n({value:l}),t.nextTick(()=>P.value?.focus()))},B={passive:!0,capture:!0}
function D(e){const t=A(e)
null!=t&&o({value:t})}function $(e){e.stopPropagation(),e.preventDefault(),R(e),window.removeEventListener("mousemove",D,B),window.removeEventListener("mouseup",$)}function M(e){R(e),window.removeEventListener("touchmove",D,B),e.target?.removeEventListener("touchend",M)}t.onScopeDispose(()=>{window.removeEventListener("touchmove",D),window.removeEventListener("mousemove",D),window.removeEventListener("mouseup",$)})
const z=e=>{const t=(e-p.value)/(m.value-p.value)*100
return F(isNaN(t)?0:t,0,100)},L=t.toRef(()=>a.showTicks),O=t.computed(()=>L.value?a.ticks?Array.isArray(a.ticks)?a.ticks.map(e=>({value:e,position:z(e),label:e.toString()})):Object.keys(a.ticks).map(e=>({value:parseFloat(e),position:z(parseFloat(e)),label:a.ticks[e]})):k.value!==1/0?y(k.value+1).map(e=>{const t=p.value+e*f.value
return{value:t,position:z(t)}}):[]:[]),j=t.computed(()=>O.value.some(e=>{let{label:t}=e
return!!t})),H={activeThumbRef:P,color:t.toRef(()=>a.color),decimals:g,disabled:s.isDisabled,direction:t.toRef(()=>a.direction),elevation:t.toRef(()=>a.elevation),hasLabels:j,isReversed:c,indexFromEnd:v,min:p,max:m,mousePressed:E,noKeyboard:t.toRef(()=>a.noKeyboard),numTicks:k,onSliderMousedown:function(e){0===e.button&&(e.preventDefault(),T(e),window.addEventListener("mousemove",D,B),window.addEventListener("mouseup",$,{passive:!1}))},onSliderTouchstart:function(e){T(e),window.addEventListener("touchmove",D,B),e.target?.addEventListener("touchend",M,{passive:!1})},parsedTicks:O,parseMouseMove:A,position:z,readonly:s.isReadonly,rounded:t.toRef(()=>a.rounded),roundValue:h,showTicks:L,startOffset:I,step:f,thumbSize:b,thumbColor:S,thumbLabelColor:x,thumbLabel:t.toRef(()=>a.thumbLabel),ticks:t.toRef(()=>a.ticks),tickSize:V,trackColor:N,trackContainerRef:_,trackFillColor:C,trackSize:w,vertical:d}
return t.provide(Uc,H),H},Zc=vt({focused:Boolean,max:{type:Number,required:!0},min:{type:Number,required:!0},modelValue:{type:Number,required:!0},position:{type:Number,required:!0},ripple:{type:[Boolean,Object],default:!0},name:String,noKeyboard:Boolean,...pt()},"VSliderThumb"),Qc=wt()({name:"VSliderThumb",directives:{vRipple:Dn},props:Zc(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l,emit:n}=a
const o=t.inject(Uc),{isRtl:r,rtlClasses:i}=ga()
if(!o)throw new Error("[Vuetify] v-slider-thumb must be used inside v-slider or v-range-slider")
const{min:s,max:u,thumbColor:c,thumbLabelColor:d,step:v,disabled:p,thumbSize:m,thumbLabel:f,direction:g,isReversed:h,vertical:y,readonly:V,elevation:w,mousePressed:k,decimals:x,indexFromEnd:N}=o,C=t.computed(()=>p.value?void 0:w.value),{elevationClasses:E}=xl(C),{textColorClasses:I,textColorStyles:_}=cl(c),{backgroundColorClasses:P,backgroundColorStyles:A}=dl(d),{pageup:R,pagedown:T,end:B,home:D,left:F,right:$,down:M,up:z}=S,L=[R,T,B,D,F,$,M,z],O=t.computed(()=>v.value?[1,2,3]:[1,5,10])
function j(t){const a=function(t,a){if(e.noKeyboard||p.value)return
if(!L.includes(t.key))return
t.preventDefault()
const l=v.value||.1,n=(u.value-s.value)/l
if([F,$,M,z].includes(t.key)){const e=(y.value?[r.value?F:$,h.value?M:z]:N.value!==r.value?[F,z]:[$,z]).includes(t.key)?1:-1,o=t.shiftKey?2:t.ctrlKey?1:0;-1!==e||a!==u.value||o||Number.isInteger(n)?a+=e*l*O.value[o]:a-=n%1*l}else t.key===D?a=s.value:t.key===B?a=u.value:a-=(t.key===T?1:-1)*l*(n>100?n/10:10)
return Math.max(e.min,Math.min(e.max,a))}(t,e.modelValue)
null!=a&&n("update:modelValue",a)}return Bt(()=>{const a=b(N.value?100-e.position:e.position,"%")
return t.createElementVNode("div",{class:t.normalizeClass(["v-slider-thumb",{"v-slider-thumb--focused":e.focused,"v-slider-thumb--pressed":e.focused&&k.value},e.class,i.value]),style:t.normalizeStyle([{"--v-slider-thumb-position":a,"--v-slider-thumb-size":b(m.value)},e.style]),role:"slider",tabindex:p.value?-1:0,"aria-label":e.name,"aria-valuemin":s.value,"aria-valuemax":u.value,"aria-valuenow":e.modelValue,"aria-readonly":!!V.value,"aria-orientation":g.value,onKeydown:V.value?void 0:j},[t.createElementVNode("div",{class:t.normalizeClass(["v-slider-thumb__surface",I.value,E.value]),style:t.normalizeStyle(_.value)},null),t.withDirectives(t.createElementVNode("div",{class:t.normalizeClass(["v-slider-thumb__ripple",I.value]),style:t.normalizeStyle(_.value)},null),[[Dn,e.ripple,null,{circle:!0,center:!0}]]),t.createVNode(Ua,{origin:"bottom center"},{default:()=>[t.withDirectives(t.createElementVNode("div",{class:"v-slider-thumb__label-container"},[t.createElementVNode("div",{class:t.normalizeClass(["v-slider-thumb__label",P.value]),style:t.normalizeStyle(A.value)},[t.createElementVNode("div",null,[l["thumb-label"]?.({modelValue:e.modelValue})??e.modelValue.toFixed(v.value?x.value:1)]),t.createElementVNode("div",{class:"v-slider-thumb__label-wedge"},null)])]),[[t.vShow,f.value&&e.focused||"always"===f.value]])]})])}),{}}}),Jc=vt({start:{type:Number,required:!0},stop:{type:Number,required:!0},...pt()},"VSliderTrack"),ed=wt()({name:"VSliderTrack",props:Jc(),emits:{},setup(e,a){let{slots:l}=a
const n=t.inject(Uc)
if(!n)throw new Error("[Vuetify] v-slider-track must be inside v-slider or v-range-slider")
const{color:o,parsedTicks:r,rounded:i,showTicks:s,tickSize:u,trackColor:c,trackFillColor:d,trackSize:v,vertical:p,min:m,max:f,indexFromEnd:g}=n,{roundedClasses:h}=ml(i),{backgroundColorClasses:y,backgroundColorStyles:V}=dl(d),{backgroundColorClasses:w,backgroundColorStyles:k}=dl(c),S=t.computed(()=>`inset-${p.value?"block":"inline"}-${g.value?"end":"start"}`),x=t.computed(()=>p.value?"height":"width"),N=t.computed(()=>({[S.value]:"0%",[x.value]:"100%"})),C=t.computed(()=>e.stop-e.start),E=t.computed(()=>({[S.value]:b(e.start,"%"),[x.value]:b(C.value,"%")})),I=t.computed(()=>{if(!s.value)return[]
return(p.value?r.value.slice().reverse():r.value).map((a,n)=>{const o=a.value!==m.value&&a.value!==f.value?b(a.position,"%"):void 0
return t.createElementVNode("div",{key:a.value,class:t.normalizeClass(["v-slider-track__tick",{"v-slider-track__tick--filled":a.position>=e.start&&a.position<=e.stop,"v-slider-track__tick--first":a.value===m.value,"v-slider-track__tick--last":a.value===f.value}]),style:{[S.value]:o}},[(a.label||l["tick-label"])&&t.createElementVNode("div",{class:"v-slider-track__tick-label"},[l["tick-label"]?.({tick:a,index:n})??a.label])])})})
return Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-slider-track",h.value,e.class]),style:t.normalizeStyle([{"--v-slider-track-size":b(v.value),"--v-slider-tick-size":b(u.value)},e.style])},[t.createElementVNode("div",{class:t.normalizeClass(["v-slider-track__background",w.value,{"v-slider-track__background--opacity":!!o.value||!d.value}]),style:{...N.value,...k.value}},null),t.createElementVNode("div",{class:t.normalizeClass(["v-slider-track__fill",y.value]),style:{...E.value,...V.value}},null),s.value&&t.createElementVNode("div",{class:t.normalizeClass(["v-slider-track__ticks",{"v-slider-track__ticks--always-show":"always"===s.value}])},[I.value])])),{}}}),td=vt({...so(),...Kc(),...ho(),modelValue:{type:[Number,String],default:0}},"VSlider"),ad=wt()({name:"VSlider",inheritAttrs:!1,props:td(),emits:{"update:focused":e=>!0,"update:modelValue":e=>!0,start:e=>!0,end:e=>!0},setup(e,a){let{slots:l,emit:n,attrs:o}=a
const r=t.ref(),i=t.ref(),{rtlClasses:s}=ga(),u=qc(e),c=la(e,"modelValue",void 0,e=>u.roundValue(null==e?u.min.value:e)),{min:d,max:v,mousePressed:p,roundValue:m,onSliderMousedown:f,onSliderTouchstart:g,trackContainerRef:h,position:y,hasLabels:b,disabled:V,readonly:w,noKeyboard:k}=Xc({props:e,steps:u,onSliderStart:()=>{V.value||w.value||n("start",c.value)},onSliderEnd:e=>{let{value:t}=e
const a=m(t)
V.value||w.value||(c.value=a),n("end",a)},onSliderMove:e=>{let{value:t}=e
V.value||w.value||(c.value=m(t))},getActiveThumb:()=>r.value?.$el}),{isFocused:S,focus:x,blur:N}=uo(e),C=t.computed(()=>y(c.value))
return Bt(()=>{const a=yo.filterProps(e),[n,u]=T(o),m=!!(e.label||l.label||l.prepend)
return t.createVNode(yo,t.mergeProps({ref:i,class:["v-slider",{"v-slider--has-labels":!!l["tick-label"]||b.value,"v-slider--focused":S.value,"v-slider--pressed":p.value,"v-slider--disabled":V.value},s.value,e.class],style:e.style},a,n,{focused:S.value}),{...l,prepend:m?a=>t.createElementVNode(t.Fragment,null,[l.label?.(a)??(e.label?t.createVNode(Xn,{id:a.id.value,class:"v-slider__label",text:e.label},null):void 0),l.prepend?.(a)]):void 0,default:a=>{let{id:n,messagesId:o}=a
return t.createElementVNode("div",{class:"v-slider__container",onMousedown:w.value?void 0:f,onTouchstartPassive:w.value?void 0:g},[t.createElementVNode("input",{id:n.value,name:e.name||n.value,disabled:V.value,readonly:w.value,tabindex:"-1",value:c.value},null),t.createVNode(ed,{ref:h,start:0,stop:C.value},{"tick-label":l["tick-label"]}),t.createVNode(Qc,t.mergeProps({ref:r,"aria-describedby":o.value,focused:S.value,noKeyboard:k.value,min:d.value,max:v.value,modelValue:c.value,"onUpdate:modelValue":e=>c.value=e,position:C.value,elevation:e.elevation,onFocus:x,onBlur:N,ripple:e.ripple,name:e.name},u),{"thumb-label":l["thumb-label"]})])}})}),wo({focus:()=>r.value?.$el.focus()},i)}}),ld=vt({color:{type:Object},disabled:Boolean,hideAlpha:Boolean,hideEyeDropper:Boolean,eyeDropperIcon:{type:Dt,default:"$eyeDropper"},...pt()},"VColorPickerPreview"),nd=Vt({name:"VColorPickerPreview",props:ld(),emits:{"update:color":e=>!0},setup(e,a){let{emit:l}=a
const{t:n}=ma(),o=new AbortController
async function r(){if(!s||e.disabled)return
const t=new window.EyeDropper
try{const a=Qe(qe((await t.open({signal:o.signal})).sRGBHex))
l("update:color",{...e.color??zc,...a})}catch(e){}}return t.onUnmounted(()=>o.abort()),Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-color-picker-preview",{"v-color-picker-preview--hide-alpha":e.hideAlpha},e.class]),style:t.normalizeStyle(e.style)},[s&&!e.hideEyeDropper&&t.createElementVNode("div",{class:"v-color-picker-preview__eye-dropper",key:"eyeDropper"},[t.createVNode($n,{"aria-label":n("$vuetify.colorPicker.ariaLabel.eyedropper"),density:"comfortable",disabled:e.disabled,icon:e.eyeDropperIcon,variant:"plain",onClick:r},null)]),t.createElementVNode("div",{class:"v-color-picker-preview__dot"},[t.createElementVNode("div",{style:{background:at(e.color??zc)}},null)]),t.createElementVNode("div",{class:"v-color-picker-preview__sliders"},[t.createVNode(ad,{class:"v-color-picker-preview__track v-color-picker-preview__hue","aria-label":n("$vuetify.colorPicker.ariaLabel.hueSlider"),modelValue:e.color?.h,"onUpdate:modelValue":t=>l("update:color",{...e.color??zc,h:t}),step:1,min:0,max:360,disabled:e.disabled,thumbSize:14,trackSize:8,trackFillColor:"white",hideDetails:!0},null),!e.hideAlpha&&t.createVNode(ad,{class:"v-color-picker-preview__track v-color-picker-preview__alpha","aria-label":n("$vuetify.colorPicker.ariaLabel.alphaSlider"),modelValue:e.color?.a??1,"onUpdate:modelValue":t=>l("update:color",{...e.color??zc,a:t}),step:.01,min:0,max:1,disabled:e.disabled,thumbSize:14,trackSize:8,trackFillColor:"white",hideDetails:!0},null)])])),{}}})
var od={red:{base:"#f44336",lighten5:"#ffebee",lighten4:"#ffcdd2",lighten3:"#ef9a9a",lighten2:"#e57373",lighten1:"#ef5350",darken1:"#e53935",darken2:"#d32f2f",darken3:"#c62828",darken4:"#b71c1c",accent1:"#ff8a80",accent2:"#ff5252",accent3:"#ff1744",accent4:"#d50000"},pink:{base:"#e91e63",lighten5:"#fce4ec",lighten4:"#f8bbd0",lighten3:"#f48fb1",lighten2:"#f06292",lighten1:"#ec407a",darken1:"#d81b60",darken2:"#c2185b",darken3:"#ad1457",darken4:"#880e4f",accent1:"#ff80ab",accent2:"#ff4081",accent3:"#f50057",accent4:"#c51162"},purple:{base:"#9c27b0",lighten5:"#f3e5f5",lighten4:"#e1bee7",lighten3:"#ce93d8",lighten2:"#ba68c8",lighten1:"#ab47bc",darken1:"#8e24aa",darken2:"#7b1fa2",darken3:"#6a1b9a",darken4:"#4a148c",accent1:"#ea80fc",accent2:"#e040fb",accent3:"#d500f9",accent4:"#aa00ff"},deepPurple:{base:"#673ab7",lighten5:"#ede7f6",lighten4:"#d1c4e9",lighten3:"#b39ddb",lighten2:"#9575cd",lighten1:"#7e57c2",darken1:"#5e35b1",darken2:"#512da8",darken3:"#4527a0",darken4:"#311b92",accent1:"#b388ff",accent2:"#7c4dff",accent3:"#651fff",accent4:"#6200ea"},indigo:{base:"#3f51b5",lighten5:"#e8eaf6",lighten4:"#c5cae9",lighten3:"#9fa8da",lighten2:"#7986cb",lighten1:"#5c6bc0",darken1:"#3949ab",darken2:"#303f9f",darken3:"#283593",darken4:"#1a237e",accent1:"#8c9eff",accent2:"#536dfe",accent3:"#3d5afe",accent4:"#304ffe"},blue:{base:"#2196f3",lighten5:"#e3f2fd",lighten4:"#bbdefb",lighten3:"#90caf9",lighten2:"#64b5f6",lighten1:"#42a5f5",darken1:"#1e88e5",darken2:"#1976d2",darken3:"#1565c0",darken4:"#0d47a1",accent1:"#82b1ff",accent2:"#448aff",accent3:"#2979ff",accent4:"#2962ff"},lightBlue:{base:"#03a9f4",lighten5:"#e1f5fe",lighten4:"#b3e5fc",lighten3:"#81d4fa",lighten2:"#4fc3f7",lighten1:"#29b6f6",darken1:"#039be5",darken2:"#0288d1",darken3:"#0277bd",darken4:"#01579b",accent1:"#80d8ff",accent2:"#40c4ff",accent3:"#00b0ff",accent4:"#0091ea"},cyan:{base:"#00bcd4",lighten5:"#e0f7fa",lighten4:"#b2ebf2",lighten3:"#80deea",lighten2:"#4dd0e1",lighten1:"#26c6da",darken1:"#00acc1",darken2:"#0097a7",darken3:"#00838f",darken4:"#006064",accent1:"#84ffff",accent2:"#18ffff",accent3:"#00e5ff",accent4:"#00b8d4"},teal:{base:"#009688",lighten5:"#e0f2f1",lighten4:"#b2dfdb",lighten3:"#80cbc4",lighten2:"#4db6ac",lighten1:"#26a69a",darken1:"#00897b",darken2:"#00796b",darken3:"#00695c",darken4:"#004d40",accent1:"#a7ffeb",accent2:"#64ffda",accent3:"#1de9b6",accent4:"#00bfa5"},green:{base:"#4caf50",lighten5:"#e8f5e9",lighten4:"#c8e6c9",lighten3:"#a5d6a7",lighten2:"#81c784",lighten1:"#66bb6a",darken1:"#43a047",darken2:"#388e3c",darken3:"#2e7d32",darken4:"#1b5e20",accent1:"#b9f6ca",accent2:"#69f0ae",accent3:"#00e676",accent4:"#00c853"},lightGreen:{base:"#8bc34a",lighten5:"#f1f8e9",lighten4:"#dcedc8",lighten3:"#c5e1a5",lighten2:"#aed581",lighten1:"#9ccc65",darken1:"#7cb342",darken2:"#689f38",darken3:"#558b2f",darken4:"#33691e",accent1:"#ccff90",accent2:"#b2ff59",accent3:"#76ff03",accent4:"#64dd17"},lime:{base:"#cddc39",lighten5:"#f9fbe7",lighten4:"#f0f4c3",lighten3:"#e6ee9c",lighten2:"#dce775",lighten1:"#d4e157",darken1:"#c0ca33",darken2:"#afb42b",darken3:"#9e9d24",darken4:"#827717",accent1:"#f4ff81",accent2:"#eeff41",accent3:"#c6ff00",accent4:"#aeea00"},yellow:{base:"#ffeb3b",lighten5:"#fffde7",lighten4:"#fff9c4",lighten3:"#fff59d",lighten2:"#fff176",lighten1:"#ffee58",darken1:"#fdd835",darken2:"#fbc02d",darken3:"#f9a825",darken4:"#f57f17",accent1:"#ffff8d",accent2:"#ffff00",accent3:"#ffea00",accent4:"#ffd600"},amber:{base:"#ffc107",lighten5:"#fff8e1",lighten4:"#ffecb3",lighten3:"#ffe082",lighten2:"#ffd54f",lighten1:"#ffca28",darken1:"#ffb300",darken2:"#ffa000",darken3:"#ff8f00",darken4:"#ff6f00",accent1:"#ffe57f",accent2:"#ffd740",accent3:"#ffc400",accent4:"#ffab00"},orange:{base:"#ff9800",lighten5:"#fff3e0",lighten4:"#ffe0b2",lighten3:"#ffcc80",lighten2:"#ffb74d",lighten1:"#ffa726",darken1:"#fb8c00",darken2:"#f57c00",darken3:"#ef6c00",darken4:"#e65100",accent1:"#ffd180",accent2:"#ffab40",accent3:"#ff9100",accent4:"#ff6d00"},deepOrange:{base:"#ff5722",lighten5:"#fbe9e7",lighten4:"#ffccbc",lighten3:"#ffab91",lighten2:"#ff8a65",lighten1:"#ff7043",darken1:"#f4511e",darken2:"#e64a19",darken3:"#d84315",darken4:"#bf360c",accent1:"#ff9e80",accent2:"#ff6e40",accent3:"#ff3d00",accent4:"#dd2c00"},brown:{base:"#795548",lighten5:"#efebe9",lighten4:"#d7ccc8",lighten3:"#bcaaa4",lighten2:"#a1887f",lighten1:"#8d6e63",darken1:"#6d4c41",darken2:"#5d4037",darken3:"#4e342e",darken4:"#3e2723"},blueGrey:{base:"#607d8b",lighten5:"#eceff1",lighten4:"#cfd8dc",lighten3:"#b0bec5",lighten2:"#90a4ae",lighten1:"#78909c",darken1:"#546e7a",darken2:"#455a64",darken3:"#37474f",darken4:"#263238"},grey:{base:"#9e9e9e",lighten5:"#fafafa",lighten4:"#f5f5f5",lighten3:"#eeeeee",lighten2:"#e0e0e0",lighten1:"#bdbdbd",darken1:"#757575",darken2:"#616161",darken3:"#424242",darken4:"#212121"},shades:{black:"#000000",white:"#ffffff",transparent:"#ffffff00"}}
const rd=vt({swatches:{type:Array,default:()=>function(e){return Object.keys(e).map(t=>{const a=e[t]
return a.base?[a.base,a.darken4,a.darken3,a.darken2,a.darken1,a.lighten1,a.lighten2,a.lighten3,a.lighten4,a.lighten5]:[a.black,a.white,a.transparent]})}(od)},disabled:Boolean,color:Object,maxHeight:[Number,String],...pt()},"VColorPickerSwatches")
const id=Vt({name:"VColorPickerSwatches",props:rd(),emits:{"update:color":e=>!0},setup(e,a){let{emit:l}=a
return Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-color-picker-swatches",e.class]),style:t.normalizeStyle([{maxHeight:b(e.maxHeight)},e.style])},[t.createElementVNode("div",null,[e.swatches.map(a=>t.createElementVNode("div",{class:"v-color-picker-swatches__swatch"},[a.map(a=>{const n=qe(a),o=Qe(n),r=tt(n)
return t.createElementVNode("div",{class:t.normalizeClass(["v-color-picker-swatches__color",{"v-color-picker-swatches__color--disabled":e.disabled}]),onClick:()=>function(t){!e.disabled&&t&&l("update:color",t)}(o)},[t.createElementVNode("div",{style:{background:r}},[e.color&&St(e.color,o)?t.createVNode(Jl,{size:"x-small",icon:"$success",color:ct(a,"#FFFFFF")>2?"white":"black"},null):void 0])])})]))])])),{}}}),sd=kt("v-picker-title"),ud=vt({color:String,...wl(),...pt(),...ol(),...Sl(),...nn(),...mn(),...pl(),...Pa(),...ya()},"VSheet"),cd=wt()({name:"VSheet",props:ud(),setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ca(e),{backgroundColorClasses:o,backgroundColorStyles:r}=dl(()=>e.color),{borderClasses:i}=kl(e),{dimensionStyles:s}=rl(e),{elevationClasses:u}=xl(e),{locationStyles:c}=on(e),{positionClasses:d}=fn(e),{roundedClasses:v}=ml(e)
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-sheet",n.value,o.value,i.value,u.value,d.value,v.value,e.class]),style:t.normalizeStyle([r.value,s.value,c.value,e.style])},l)),{}}}),dd=vt({bgColor:String,divided:Boolean,landscape:Boolean,title:String,hideHeader:Boolean,hideTitle:Boolean,...ud()},"VPicker"),vd=wt()({name:"VPicker",props:dd(),setup(e,a){let{slots:l}=a
const{backgroundColorClasses:n,backgroundColorStyles:o}=dl(()=>e.color)
return Bt(()=>{const a=cd.filterProps(e),r=!(e.hideTitle||!e.title&&!l.title)
return t.createVNode(cd,t.mergeProps(a,{color:e.bgColor,class:["v-picker",{"v-picker--divided":e.divided,"v-picker--landscape":e.landscape,"v-picker--with-actions":!!l.actions},e.class],style:e.style}),{default:()=>[!e.hideHeader&&t.createElementVNode("div",{key:"header",class:t.normalizeClass(["v-picker__header-wrapper",n.value]),style:t.normalizeStyle([o.value])},[r&&t.createVNode(sd,{key:"picker-title"},{default:()=>[l.title?.()??e.title]}),l.header&&t.createElementVNode("div",{class:"v-picker__header"},[l.header()])]),t.createElementVNode("div",{class:"v-picker__body"},[l.default?.()]),l.actions&&t.createVNode(nl,{defaults:{VBtn:{slim:!0,variant:"text"}}},{default:()=>[t.createElementVNode("div",{class:"v-picker__actions"},[l.actions()])]})]})}),{}}}),pd=Vt({name:"VColorPicker",props:vt({canvasHeight:{type:[String,Number],default:150},disabled:Boolean,dotSize:{type:[Number,String],default:10},hideCanvas:Boolean,hideSliders:Boolean,hideInputs:Boolean,mode:{type:String,default:"rgba",validator:e=>Object.keys(Hc).includes(e)},modes:{type:Array,default:()=>Object.keys(Hc),validator:e=>Array.isArray(e)&&e.every(e=>Object.keys(Hc).includes(e))},showSwatches:Boolean,swatches:Array,swatchesMaxHeight:{type:[Number,String],default:150},modelValue:{type:[Object,String]},...dd({hideHeader:!0}),...C(ld(),["hideEyeDropper","eyeDropperIcon"])},"VColorPicker")(),emits:{"update:modelValue":e=>!0,"update:mode":e=>!0},setup(e,l){let{slots:n}=l
const o=la(e,"mode"),r=t.ref(null),i=la(e,"modelValue",void 0,e=>{if(null==e||""===e)return null
let t
try{t=Qe(qe(e))}catch(e){return a(e),null}return t},t=>t?function(e,t){if(null==t||"string"==typeof t){const a=1!==e.a
if(t?.startsWith("rgb(")){const{r:t,g:l,b:n,a:o}=Xe(e)
return`rgb(${t} ${l} ${n}`+(a?` / ${o})`:")")}if(t?.startsWith("hsl(")){const{h:t,s:l,l:n,a:o}=Je(e)
return`hsl(${t} ${Math.round(100*l)} ${Math.round(100*n)}`+(a?` / ${o})`:")")}const l=rt(e)
return 1===e.a?l.slice(0,7):l}if("object"==typeof t){let a
return N(t,["r","g","b"])?a=Xe(e):N(t,["h","s","l"])?a=Je(e):N(t,["h","s","v"])&&(a=e),function(e,t){if(t){const{a:t,...a}=e
return a}return e}(a,!N(t,["a"])&&1===e.a)}return e}(t,e.modelValue):null),s=t.computed(()=>i.value?{...i.value,h:r.value??i.value.h}:null),{rtlClasses:u}=ga()
let c=!0
t.watch(i,e=>{c?e&&(r.value=e.h):c=!0},{immediate:!0})
const d=e=>{c=!1,r.value=e.h,i.value=e}
return t.onBeforeMount(()=>{e.modes.includes(o.value)||(o.value=e.modes[0])}),yt({VSlider:{color:void 0,trackColor:void 0,trackFillColor:void 0}}),Bt(()=>{const a=vd.filterProps(e)
return t.createVNode(vd,t.mergeProps(a,{class:["v-color-picker",u.value,e.class],style:[{"--v-color-picker-color-hsv":at({...s.value??zc,a:1})},e.style]}),{...n,default:()=>t.createElementVNode(t.Fragment,null,[!e.hideCanvas&&t.createVNode(Mc,{key:"canvas",color:s.value,"onUpdate:color":d,disabled:e.disabled,dotSize:e.dotSize,width:e.width,height:e.canvasHeight},null),(!e.hideSliders||!e.hideInputs)&&t.createElementVNode("div",{key:"controls",class:"v-color-picker__controls"},[!e.hideSliders&&t.createVNode(nd,{key:"preview",color:s.value,"onUpdate:color":d,hideAlpha:!o.value.endsWith("a"),disabled:e.disabled,hideEyeDropper:e.hideEyeDropper,eyeDropperIcon:e.eyeDropperIcon},null),!e.hideInputs&&t.createVNode(Yc,{key:"edit",modes:e.modes,mode:o.value,"onUpdate:mode":e=>o.value=e,color:s.value,"onUpdate:color":d,disabled:e.disabled},null)]),e.showSwatches&&t.createVNode(id,{key:"swatches",color:s.value,"onUpdate:color":d,maxHeight:e.swatchesMaxHeight,swatches:e.swatches,disabled:e.disabled},null)])})}),{}}}),md=vt({alwaysFilter:Boolean,autoSelectFirst:{type:[Boolean,String]},clearOnSelect:{type:Boolean,default:!0},delimiters:Array,...ns({filterKeys:["title"]}),...Ji({hideNoData:!0,returnObject:!0}),...I(ji({modelValue:null,role:"combobox"}),["validationValue","dirty"])},"VCombobox"),fd=wt()({name:"VCombobox",props:md(),emits:{"update:focused":e=>!0,"update:modelValue":e=>!0,"update:search":e=>!0,"update:menu":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const{t:r}=ma(),i=t.ref(),s=t.shallowRef(!1),u=t.shallowRef(!0),c=t.shallowRef(!1),d=t.ref(),v=t.ref(),p=t.shallowRef(-1)
let m=!1
const{items:f,transformIn:g,transformOut:h}=Rr(e),{textColorClasses:y,textColorStyles:b}=cl(()=>i.value?.color),{InputIcon:V}=oo(e),w=la(e,"modelValue",[],e=>g(B(e)),t=>{const a=h(t)
return e.multiple?a:a[0]??null}),k=po(e),S=t.toRef(()=>e.closableChips&&!k.isReadonly.value&&!k.isDisabled.value),x=t.computed(()=>!(!e.chips&&!n.chip)),N=t.computed(()=>x.value||!!n.selection),C=t.shallowRef(e.multiple||N.value?"":w.value[0]?.title??""),E=t.shallowRef(null),I=t.computed({get:()=>C.value,set:async a=>{if(C.value=a??"",null===a||""===a&&!e.multiple&&!N.value?w.value=[]:e.multiple||N.value||(w.value=[Pr(e,a)],t.nextTick(()=>v.value?.scrollToIndex(0))),a&&e.multiple&&e.delimiters?.length){const e=te(a)
e.length>1&&(ae(e),C.value="")}a||(p.value=-1),u.value=!a}}),_=t.computed(()=>"function"==typeof e.counterValue?e.counterValue(w.value):"number"==typeof e.counterValue?e.counterValue:e.multiple?w.value.length:I.value.length),{filteredItems:P,getMatches:A}=os(e,f,()=>E.value??(e.alwaysFilter||!u.value?I.value:"")),T=t.computed(()=>e.hideSelected&&null===E.value?P.value.filter(e=>!w.value.some(t=>t.value===e.value)):P.value),D=t.computed(()=>e.hideNoData&&!T.value.length||k.isReadonly.value||k.isDisabled.value),F=la(e,"menu"),$=t.computed({get:()=>F.value,set:e=>{F.value&&!e&&d.value?.ΨopenChildren.size||e&&D.value||(F.value=e)}}),{menuId:M,ariaExpanded:z,ariaControls:L}=Qi(0,$)
t.watch(C,e=>{m?t.nextTick(()=>m=!1):s.value&&!$.value&&($.value=!0),l("update:search",e)}),t.watch(w,t=>{e.multiple||N.value||(C.value=t[0]?.title??"")})
const O=t.computed(()=>w.value.map(e=>e.value)),j=t.computed(()=>T.value.find(e=>"item"===e.type&&!e.props.disabled)),H=t.computed(()=>(!0===e.autoSelectFirst||"exact"===e.autoSelectFirst&&I.value===j.value?.title)&&T.value.length>0&&!u.value&&!c.value),W=t.ref(),Y=Xi(W,i)
function U(a){m=!0,t.nextTick(()=>m=!1),e.openOnClear&&($.value=!0)}function G(){D.value||($.value=!0)}function K(e){D.value||(s.value&&(e.preventDefault(),e.stopPropagation()),$.value=!$.value)}function q(e){(ue(e)||"Backspace"===e.key)&&i.value?.focus()}function X(t){if(function(e){return e.isComposing&&R.includes(e.key)}(t)||k.isReadonly.value)return
const a=i.value?.selectionStart,l=w.value.length
if(["Enter","ArrowDown","ArrowUp"].includes(t.key)&&t.preventDefault(),["Enter","ArrowDown"].includes(t.key)&&($.value=!0),["Escape"].includes(t.key)&&($.value=!1),H.value&&["Enter","Tab"].includes(t.key)&&j.value&&!w.value.some(e=>{let{value:t}=e
return t===j.value.value})&&ee(j.value),"ArrowDown"===t.key&&H.value&&W.value?.focus("next"),"Enter"===t.key&&I.value&&(ee(Pr(e,I.value),!0,!0),N.value&&(C.value="")),["Backspace","Delete"].includes(t.key)){if(!e.multiple&&N.value&&w.value.length>0&&!I.value)return ee(w.value[0],!1)
if(~p.value){t.preventDefault()
const e=p.value
ee(w.value[p.value],!1),p.value=e>=l-1?l-2:e}else"Backspace"!==t.key||I.value||(p.value=l-1)}else if(e.multiple)if("ArrowLeft"===t.key){if(p.value<0&&a&&a>0)return
const e=p.value>-1?p.value-1:l-1
w.value[e]?p.value=e:(p.value=-1,i.value?.setSelectionRange(I.value.length,I.value.length))}else if("ArrowRight"===t.key){if(p.value<0)return
const e=p.value+1
w.value[e]?p.value=e:(p.value=-1,i.value?.setSelectionRange(0,0))}else~p.value&&ue(t)&&(p.value=-1)}function Z(t){const a=te(t?.clipboardData?.getData("Text")??"")
a.length>1&&e.multiple&&(t.preventDefault(),ae(a))}function Q(){e.eager&&v.value?.calculateVisibleItems()}function J(){s.value&&i.value?.focus(),u.value=!0,E.value=null}function ee(a){let l=!(arguments.length>1&&void 0!==arguments[1])||arguments[1],n=arguments.length>2&&void 0!==arguments[2]&&arguments[2]
if(a&&!a.props.disabled)if(e.multiple){const t=w.value.findIndex(t=>(e.valueComparator||St)(t.value,a.value)),n=null==l?!~t:l
if(~t){const e=n?[...w.value,a]:[...w.value]
e.splice(t,1),w.value=e}else n&&(w.value=[...w.value,a])
e.clearOnSelect&&(I.value="")}else{const o=!1!==l
w.value=o?[a]:[],u.value&&!e.alwaysFilter||!C.value||(E.value=C.value),C.value=o&&!N.value?a.title:"",t.nextTick(()=>{$.value=n,u.value=!0})}}function te(t){const a=["\n",...e.delimiters??[]].map(de).join("|")
return t.split(new RegExp(`(?:${a})+`))}async function ae(a){for(let l of a)l=l.trim(),l&&(ee(Pr(e,l)),await t.nextTick())}function le(e){s.value=!0,setTimeout(()=>{c.value=!0})}function oe(e){c.value=!1}return t.watch(s,(t,a)=>{if(!t&&t!==a&&(p.value=-1,$.value=!1,I.value)){if(e.multiple)return void ee(Pr(e,I.value))
if(!N.value)return
w.value.some(e=>{let{title:t}=e
return t===I.value})?C.value="":ee(Pr(e,I.value))}}),t.watch($,t=>{if(!e.hideSelected&&t&&w.value.length&&u.value){const t=T.value.findIndex(t=>w.value.some(a=>(e.valueComparator||St)(a.value,t.value)))
o&&window.requestAnimationFrame(()=>{t>=0&&v.value?.scrollToIndex(t)})}t&&(E.value=null)}),t.watch(f,(e,t)=>{$.value||s.value&&!t.length&&e.length&&($.value=!0)}),Bt(()=>{const a=!!(!e.hideNoData||T.value.length||n["prepend-item"]||n["append-item"]||n["no-data"]),l=w.value.length>0,o=Hi.filterProps(e)
return t.createVNode(Hi,t.mergeProps({ref:i},o,{modelValue:I.value,"onUpdate:modelValue":e=>I.value=e,focused:s.value,"onUpdate:focused":e=>s.value=e,validationValue:w.externalValue,counterValue:_.value,dirty:l,class:["v-combobox",{"v-combobox--active-menu":$.value,"v-combobox--chips":!!e.chips,"v-combobox--selection-slot":!!N.value,"v-combobox--selecting-index":p.value>-1,["v-combobox--"+(e.multiple?"multiple":"single")]:!0},e.class],style:e.style,readonly:k.isReadonly.value,placeholder:l?void 0:e.placeholder,"onClick:clear":U,"onMousedown:control":G,onKeydown:X,onPaste:Z,"aria-expanded":z.value,"aria-controls":L.value}),{...n,default:l=>{let{id:o}=l
return t.createElementVNode(t.Fragment,null,[t.createVNode(Pi,t.mergeProps({id:M.value,ref:d,modelValue:$.value,"onUpdate:modelValue":e=>$.value=e,activator:"parent",contentClass:"v-combobox__content",disabled:D.value,eager:e.eager,maxHeight:310,openOnClick:!1,closeOnContentClick:!1,onAfterEnter:Q,onAfterLeave:J},e.menuProps),{default:()=>[a&&t.createVNode(Mr,t.mergeProps({ref:W,filterable:!0,selected:O.value,selectStrategy:e.multiple?"independent":"single-independent",onMousedown:e=>e.preventDefault(),selectable:!!T.value.length,onKeydown:q,onFocusin:le,onFocusout:oe,tabindex:"-1","aria-live":"polite","aria-labelledby":`${o.value}-label`,"aria-multiselectable":e.multiple,color:e.itemColor??e.color},Y,e.listProps),{default:()=>[n["prepend-item"]?.(),!T.value.length&&!e.hideNoData&&(n["no-data"]?.()??t.createVNode(Sr,{key:"no-data",title:r(e.noDataText)},null)),t.createVNode(qi,{ref:v,renderless:!0,items:T.value,itemKey:"value"},{default:a=>{let{item:l,index:o,itemRef:r}=a
const i=t.mergeProps(l.props,{ref:r,key:l.value,active:!(!H.value||l!==j.value)||void 0,onClick:()=>ee(l,null),"aria-posinset":o+1,"aria-setsize":T.value.length})
return"divider"===l.type?n.divider?.({props:l.raw,index:o})??t.createVNode(Jo,t.mergeProps(l.props,{key:`divider-${o}`}),null):"subheader"===l.type?n.subheader?.({props:l.raw,index:o})??t.createVNode(Nr,t.mergeProps(l.props,{key:`subheader-${o}`}),null):n.item?.({item:l,index:o,props:i})??t.createVNode(Sr,t.mergeProps(i,{role:"option"}),{prepend:a=>{let{isSelected:n}=a
return t.createElementVNode(t.Fragment,null,[e.multiple&&!e.hideSelected?t.createVNode(no,{key:l.value,modelValue:n,ripple:!1,tabindex:"-1","aria-hidden":!0,onClick:e=>e.preventDefault()},null):void 0,l.props.prependAvatar&&t.createVNode(Kn,{image:l.props.prependAvatar},null),l.props.prependIcon&&t.createVNode(Jl,{icon:l.props.prependIcon},null)])},title:()=>u.value?l.title:rs("v-combobox",l.title,A(l)?.title)})}}),n["append-item"]?.()]})]}),w.value.map((a,l)=>{function o(e){e.stopPropagation(),e.preventDefault(),ee(a,!1)}const r=t.mergeProps(Xo.filterProps(a.props),{"onClick:close":o,onKeydown(e){"Enter"!==e.key&&" "!==e.key||(e.preventDefault(),e.stopPropagation(),o(e))},onMousedown(e){e.preventDefault(),e.stopPropagation()},modelValue:!0,"onUpdate:modelValue":void 0}),i=x.value?!!n.chip:!!n.selection,s=i?re(x.value?n.chip({item:a,index:l,props:r}):n.selection({item:a,index:l})):void 0
if(!i||s)return t.createElementVNode("div",{key:a.value,class:t.normalizeClass(["v-combobox__selection",l===p.value&&["v-combobox__selection--selected",y.value]]),style:t.normalizeStyle(l===p.value?b.value:{})},[x.value?n.chip?t.createVNode(nl,{key:"chip-defaults",defaults:{VChip:{closable:S.value,size:"small",text:a.title}}},{default:()=>[s]}):t.createVNode(Xo,t.mergeProps({key:"chip",closable:S.value,size:"small",text:a.title,disabled:a.props.disabled},r),null):s??t.createElementVNode("span",{class:"v-combobox__selection-text"},[a.title,e.multiple&&l<w.value.length-1&&t.createElementVNode("span",{class:"v-combobox__selection-comma"},[t.createTextVNode(",")])])])})])},"append-inner":function(){for(var a=arguments.length,l=new Array(a),o=0;o<a;o++)l[o]=arguments[o]
return t.createElementVNode(t.Fragment,null,[n["append-inner"]?.(...l),e.hideNoData&&!e.items.length||!e.menuIcon?void 0:t.createVNode(Jl,{class:"v-combobox__menu-icon",color:i.value?.fieldIconColor,icon:e.menuIcon,onMousedown:K,onClick:ne,"aria-hidden":!0,tabindex:"-1"},null),e.appendInnerIcon&&t.createVNode(V,{key:"append-icon",name:"appendInner",color:l[0].iconColor.value},null)])}})}),wo({isFocused:s,isPristine:u,menu:$,search:I,selectionIndex:p,filteredItems:P,select:ee},i)}}),gd=vt({modelValue:null,color:String,cancelText:{type:String,default:"$vuetify.confirmEdit.cancel"},okText:{type:String,default:"$vuetify.confirmEdit.ok"},disabled:{type:[Boolean,Array],default:void 0},hideActions:Boolean},"VConfirmEdit"),hd=wt()({name:"VConfirmEdit",props:gd(),emits:{cancel:()=>!0,save:e=>!0,"update:modelValue":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const o=la(e,"modelValue"),r=t.ref()
t.watchEffect(()=>{r.value=structuredClone(ve(o.value))})
const{t:i}=ma(),s=t.computed(()=>St(o.value,r.value))
function u(t){return"boolean"==typeof e.disabled?e.disabled:Array.isArray(e.disabled)?e.disabled.includes(t):s.value}const c=t.computed(()=>u("save")),d=t.computed(()=>u("cancel"))
function v(){o.value=r.value,l("save",r.value)}function p(){r.value=structuredClone(ve(o.value)),l("cancel")}function m(a){return t.createElementVNode(t.Fragment,null,[t.createVNode($n,t.mergeProps({disabled:d.value,variant:"text",color:e.color,onClick:p,text:i(e.cancelText)},a),null),t.createVNode($n,t.mergeProps({disabled:c.value,variant:"text",color:e.color,onClick:v,text:i(e.okText)},a),null)])}let f=!1
return Bt(()=>t.createElementVNode(t.Fragment,null,[n.default?.({model:r,save:v,cancel:p,isPristine:s.value,get actions(){return f=!0,m}}),!e.hideActions&&!f&&m()])),{save:v,cancel:p,isPristine:s}}}),yd=vt({expandOnClick:Boolean,showExpand:Boolean,expanded:{type:Array,default:()=>[]}},"DataTable-expand"),bd=Symbol.for("vuetify:datatable:expanded")
function Vd(e){const a=t.toRef(()=>e.expandOnClick),l=la(e,"expanded",e.expanded,e=>new Set(e),e=>[...e.values()])
function n(e,a){const n=new Set(l.value),o=t.toRaw(e.value)
if(a)n.add(o)
else{const e=[...l.value].find(e=>t.toRaw(e)===o)
n.delete(e)}l.value=n}function o(e){const a=t.toRaw(e.value)
return[...l.value].some(e=>t.toRaw(e)===a)}const r={expand:n,expanded:l,expandOnClick:a,isExpanded:o,toggleExpand:function(e){n(e,!o(e))}}
return t.provide(bd,r),r}function wd(){const e=t.inject(bd)
if(!e)throw new Error("foo")
return e}const kd=vt({groupBy:{type:Array,default:()=>[]}},"DataTable-group"),Sd=Symbol.for("vuetify:data-table-group")
function xd(e){return{groupBy:la(e,"groupBy")}}function Nd(e){const{disableSort:a,groupBy:l,sortBy:n}=e,o=t.ref(new Set)
function r(e){return o.value.has(e.id)}const i={sortByWithGroups:t.computed(()=>l.value.map(e=>({...e,order:e.order??!1})).concat(a?.value?[]:n.value)),toggleGroup:function(e){const t=new Set(o.value)
r(e)?t.delete(e.id):t.add(e.id),o.value=t},opened:o,groupBy:l,extractRows:function(e){return function e(t){const a=[]
for(const l of t.items)"type"in l&&"group"===l.type?a.push(...e(l)):a.push(l)
return[...new Set(a)]}({items:e})},isGroupOpen:r}
return t.provide(Sd,i),i}function Cd(){const e=t.inject(Sd)
if(!e)throw new Error("Missing group!")
return e}function Ed(e,t){let a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:0,l=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"root"
if(!t.length)return[]
const n=function(e,t){if(!e.length)return[]
const a=new Map
for(const l of e){const e=g(l.raw,t)
a.has(e)||a.set(e,[]),a.get(e).push(l)}return a}(e,t[0]),o=[],r=t.slice(1)
return n.forEach((e,n)=>{const i=t[0],s=`${l}_${i}_${n}`
o.push({depth:a,id:s,key:i,value:n,items:r.length?Ed(e,r,a+1,s):e,type:"group"})}),o}function Id(e,t,a){const l=[]
for(const n of e)"type"in n&&"group"===n.type?(null!=n.value&&l.push(n),(t.has(n.id)||null==n.value)&&(l.push(...Id(n.items,t,a)),a&&l.push({...n,type:"group-summary"}))):l.push(n)
return l}function _d(e,a,l,n){return{flatItems:t.computed(()=>{if(!a.value.length)return e.value
return Id(Ed(e.value,a.value.map(e=>e.key)),l.value,t.toValue(n))})}}function Pd(e){let{page:a,itemsPerPage:l,sortBy:n,groupBy:o,search:r}=e
const i=mt("VDataTable")
let s=null
t.watch(()=>({page:a.value,itemsPerPage:l.value,sortBy:n.value,groupBy:o.value,search:r.value}),e=>{St(s,e)||(s&&s.search!==e.search&&(a.value=1),i.emit("update:options",e),s=e)},{deep:!0,immediate:!0})}const Ad=vt({page:{type:[Number,String],default:1},itemsPerPage:{type:[Number,String],default:10}},"DataTable-paginate"),Rd=Symbol.for("vuetify:data-table-pagination")
function Td(e){return{page:la(e,"page",void 0,e=>Number(e??1)),itemsPerPage:la(e,"itemsPerPage",void 0,e=>Number(e??10))}}function Bd(e){const{page:a,itemsPerPage:l,itemsLength:n}=e,o=t.computed(()=>-1===l.value?0:l.value*(a.value-1)),r=t.computed(()=>-1===l.value?n.value:Math.min(n.value,o.value+l.value)),i=t.computed(()=>-1===l.value||0===n.value?1:Math.ceil(n.value/l.value))
t.watch([a,i],()=>{a.value>i.value&&(a.value=i.value)})
const s={page:a,itemsPerPage:l,startIndex:o,stopIndex:r,pageCount:i,itemsLength:n,nextPage:function(){a.value=F(a.value+1,1,i.value)},prevPage:function(){a.value=F(a.value-1,1,i.value)},setPage:function(e){a.value=F(e,1,i.value)},setItemsPerPage:function(e){l.value=e,a.value=1}}
return t.provide(Rd,s),s}function Dd(e){const a=mt("usePaginatedItems"),{items:l,startIndex:n,stopIndex:o,itemsPerPage:r}=e,i=t.computed(()=>r.value<=0?l.value:l.value.slice(n.value,o.value))
return t.watch(i,e=>{a.emit("update:currentItems",e)},{immediate:!0}),{paginatedItems:i}}const Fd={showSelectAll:!1,allSelected:()=>[],select:e=>{let{items:t,value:a}=e
return new Set(a?[t[0]?.value]:[])},selectAll:e=>{let{selected:t}=e
return t}},$d={showSelectAll:!0,allSelected:e=>{let{currentPage:t}=e
return t},select:e=>{let{items:t,value:a,selected:l}=e
for(const e of t)a?l.add(e.value):l.delete(e.value)
return l},selectAll:e=>{let{value:t,currentPage:a,selected:l}=e
return $d.select({items:a,value:t,selected:l})}},Md={showSelectAll:!0,allSelected:e=>{let{allItems:t}=e
return t},select:e=>{let{items:t,value:a,selected:l}=e
for(const e of t)a?l.add(e.value):l.delete(e.value)
return l},selectAll:e=>{let{value:t,allItems:a}=e
return new Set(t?a.map(e=>e.value):[])}},zd=vt({showSelect:Boolean,selectStrategy:{type:[String,Object],default:"page"},modelValue:{type:Array,default:()=>[]},valueComparator:Function},"DataTable-select"),Ld=Symbol.for("vuetify:data-table-selection")
function Od(e,a){let{allItems:l,currentPage:n}=a
const o=la(e,"modelValue",e.modelValue,t=>{const a=e.valueComparator
return a?new Set(B(t).map(e=>l.value.find(t=>a(e,t.value))?.value??e)):new Set(B(t).map(e=>ce(e)?l.value.find(t=>e===t.value)?.value??e:l.value.find(t=>St(e,t.value))?.value??e))},e=>[...e.values()]),r=t.computed(()=>l.value.filter(e=>e.selectable)),i=t.computed(()=>n.value.filter(e=>e.selectable)),s=t.computed(()=>{if("object"==typeof e.selectStrategy)return e.selectStrategy
switch(e.selectStrategy){case"single":return Fd
case"all":return Md
default:return $d}}),u=t.shallowRef(null)
function c(e){return B(e).every(e=>o.value.has(e.value))}function d(e,t){const a=s.value.select({items:e,value:t,selected:new Set(o.value)})
o.value=a}const v=t.computed(()=>o.value.size>0),p=t.computed(()=>{const e=s.value.allSelected({allItems:r.value,currentPage:i.value})
return!!e.length&&c(e)}),m={toggleSelect:function(t,a,l){const o=[]
if(a=a??n.value.findIndex(e=>e.value===t.value),"single"!==e.selectStrategy&&l?.shiftKey&&null!==u.value){const[e,t]=[u.value,a].sort((e,t)=>e-t)
o.push(...n.value.slice(e,t+1).filter(e=>e.selectable))}else o.push(t),u.value=a
d(o,!c([t]))},select:d,selectAll:function(e){const t=s.value.selectAll({value:e,allItems:r.value,currentPage:i.value,selected:new Set(o.value)})
o.value=t},isSelected:c,isSomeSelected:function(e){return B(e).some(e=>o.value.has(e.value))},someSelected:v,allSelected:p,showSelectAll:t.toRef(()=>s.value.showSelectAll),lastSelectedIndex:u,selectStrategy:s}
return t.provide(Ld,m),m}function jd(){const e=t.inject(Ld)
if(!e)throw new Error("Missing selection!")
return e}const Hd=vt({initialSortOrder:{type:String,default:"asc",validator:e=>!e||["asc","desc"].includes(e)},sortBy:{type:Array,default:()=>[]},customKeySort:Object,multiSort:{type:[Boolean,Object],default:!1},mustSort:Boolean},"DataTable-sort"),Wd=Symbol.for("vuetify:data-table-sort")
function Yd(e){const a=t.toRef(()=>e.initialSortOrder),l=la(e,"sortBy"),n=t.toRef(()=>e.mustSort)
return{initialSortOrder:a,sortBy:l,multiSort:t.toRef(()=>e.multiSort),mustSort:n}}function Ud(e){const{initialSortOrder:a,sortBy:l,mustSort:n,multiSort:o,page:r}=e
const i={sortBy:l,toggleSort:(e,t)=>{if(null==e.key)return
let i=l.value.map(e=>({...e}))??[]
const s=i.find(t=>t.key===e.key),u=a.value,c="desc"===a.value?"asc":"desc"
if(s)s.order===c?n.value&&1===i.length?s.order=a.value:i=i.filter(t=>t.key!==e.key):s.order=c
else{const{active:a,mode:l}=function(e,t){if(!V(e))return{active:!!e}
const{key:a,mode:l,modifier:n}=e,o="alt"===n&&t?.altKey||"shift"===n&&t?.shiftKey
return{active:!a||t?.ctrlKey||t?.metaKey||!1,mode:o?"append"===l?"prepend":"append":l}}(o.value,t)
a?"prepend"===l?i.unshift({key:e.key,order:u}):i.push({key:e.key,order:u}):i=[{key:e.key,order:u}]}l.value=i,r&&(r.value=1)},isSorted:function(e){return!!l.value.find(t=>t.key===e.key)}}
return t.provide(Wd,i),i}function Gd(){const e=t.inject(Wd)
if(!e)throw new Error("Missing sort!")
return e}function Kd(e,a,l,n){const o=ma(),r=t.computed(()=>l.value.length?function(e,t,a,l){const n=new Intl.Collator(a,{sensitivity:"accent",usage:"sort"}),o=e.map(e=>[e,l?.transform?l.transform(e):e])
return o.sort((e,a)=>{for(let o=0;o<t.length;o++){let r=!1
const i=t[o].key,s=t[o].order??"asc"
if(!1===s)continue
let u=g(e[1],i),c=g(a[1],i),d=e[0].raw,v=a[0].raw
if("desc"===s&&([u,c]=[c,u],[d,v]=[v,d]),l?.sortRawFunctions?.[i]){const e=l.sortRawFunctions[i](d,v)
if(null==e)continue
if(r=!0,e)return e}if(l?.sortFunctions?.[i]){const e=l.sortFunctions[i](u,c)
if(null==e)continue
if(r=!0,e)return e}if(!r&&(u instanceof Date&&c instanceof Date&&(u=u.getTime(),c=c.getTime()),[u,c]=[u,c].map(e=>null!=e?e.toString().toLocaleLowerCase():e),u!==c))return le(u)&&le(c)?0:le(u)?-1:le(c)?1:isNaN(u)||isNaN(c)?n.compare(u,c):Number(u)-Number(c)}return 0}).map(e=>{let[t]=e
return t})}(a.value,l.value,o.current.value,{transform:n?.transform,sortFunctions:{...e.customKeySort,...n?.sortFunctions?.value},sortRawFunctions:n?.sortRawFunctions?.value}):a.value)
return{sortedItems:r}}const qd=vt({items:{type:Array,default:()=>[]},itemValue:{type:[String,Array,Function],default:"id"},itemSelectable:{type:[String,Array,Function],default:null},returnObject:Boolean},"DataIterator-items")
function Xd(e,t){return{type:"item",value:e.returnObject?t:h(t,e.itemValue),selectable:h(t,e.itemSelectable,!0),raw:t}}function Zd(e){const a=t.computed(()=>function(e,t){const a=[]
for(const l of t)a.push(Xd(e,l))
return a}(e,e.items))
return{items:a}}const Qd=vt({search:String,loading:Boolean,...pt(),...qd(),...zd(),...Hd(),...Ad({itemsPerPage:5}),...yd(),...kd(),...ns(),...Pa(),...fl({transition:{component:Ya,hideOnLeave:!0}})},"VDataIterator"),Jd=wt()({name:"VDataIterator",props:Qd(),emits:{"update:modelValue":e=>!0,"update:groupBy":e=>!0,"update:page":e=>!0,"update:itemsPerPage":e=>!0,"update:sortBy":e=>!0,"update:options":e=>!0,"update:expanded":e=>!0,"update:currentItems":e=>!0},setup(e,a){let{slots:l}=a
const n=la(e,"groupBy"),o=t.toRef(()=>e.search),{items:r}=Zd(e),{filteredItems:i}=os(e,r,o,{transform:e=>e.raw}),{initialSortOrder:s,sortBy:u,multiSort:c,mustSort:d}=Yd(e),{page:v,itemsPerPage:p}=Td(e),{toggleSort:m}=Ud({initialSortOrder:s,sortBy:u,multiSort:c,mustSort:d,page:v}),{sortByWithGroups:f,opened:g,extractRows:h,isGroupOpen:y,toggleGroup:b}=Nd({groupBy:n,sortBy:u}),{sortedItems:V}=Kd(e,i,f,{transform:e=>e.raw}),{flatItems:w}=_d(V,n,g,!1),k=t.toRef(()=>w.value.length),{startIndex:S,stopIndex:x,pageCount:N,prevPage:C,nextPage:E,setItemsPerPage:I,setPage:_}=Bd({page:v,itemsPerPage:p,itemsLength:k}),{paginatedItems:P}=Dd({items:w,startIndex:S,stopIndex:x,itemsPerPage:p}),A=t.computed(()=>h(P.value)),{isSelected:R,select:T,selectAll:B,toggleSelect:D}=Od(e,{allItems:r,currentPage:A}),{isExpanded:F,toggleExpand:$}=Vd(e)
Pd({page:v,itemsPerPage:p,sortBy:u,groupBy:n,search:o})
const M=t.computed(()=>({page:v.value,itemsPerPage:p.value,sortBy:u.value,pageCount:N.value,toggleSort:m,prevPage:C,nextPage:E,setPage:_,setItemsPerPage:I,isSelected:R,select:T,selectAll:B,toggleSelect:D,isExpanded:F,toggleExpand:$,isGroupOpen:y,toggleGroup:b,items:A.value,itemsCount:i.value.length,groupedItems:P.value}))
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-data-iterator",{"v-data-iterator--loading":e.loading},e.class]),style:t.normalizeStyle(e.style)},{default:()=>[l.header?.(M.value),t.createVNode(gl,{transition:e.transition},{default:()=>[e.loading?t.createVNode(vn,{key:"loader",name:"v-data-iterator",active:!0},{default:e=>l.loader?.(e)}):t.createElementVNode("div",{key:"items"},[P.value.length?l.default?.(M.value):l["no-data"]?.()])]}),l.footer?.(M.value)]})),{}}})
const ev=vt({activeColor:String,start:{type:[Number,String],default:1},modelValue:{type:Number,default:e=>e.start},disabled:Boolean,length:{type:[Number,String],default:1,validator:e=>e%1==0},totalVisible:[Number,String],firstIcon:{type:Dt,default:"$first"},prevIcon:{type:Dt,default:"$prev"},nextIcon:{type:Dt,default:"$next"},lastIcon:{type:Dt,default:"$last"},ariaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.root"},pageAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.page"},currentPageAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.currentPage"},firstAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.first"},previousAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.previous"},nextAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.next"},lastAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.last"},ellipsis:{type:String,default:"..."},showFirstLastPage:Boolean,...wl(),...pt(),...Tl(),...Sl(),...pl(),...Xl(),...Pa({tag:"nav"}),...ya(),...$l({variant:"text"})},"VPagination"),tv=wt()({name:"VPagination",props:ev(),emits:{"update:modelValue":e=>!0,first:e=>!0,prev:e=>!0,next:e=>!0,last:e=>!0},setup(e,a){let{slots:l,emit:n}=a
const o=la(e,"modelValue"),{t:r,n:i}=ma(),{isRtl:s}=ga(),{themeClasses:u}=Ca(e),{width:c}=Ro(),d=t.shallowRef(-1)
yt(void 0,{scoped:!0})
const{resizeRef:v}=Kt(e=>{if(!e.length)return
const{target:t,contentRect:a}=e[0],l=t.querySelector(".v-pagination__list > *")
if(!l)return
const n=a.width,o=l.offsetWidth+2*parseFloat(getComputedStyle(l).marginRight)
d.value=g(n,o)}),p=t.computed(()=>parseInt(e.length,10)),m=t.computed(()=>parseInt(e.start,10)),f=t.computed(()=>null!=e.totalVisible?parseInt(e.totalVisible,10):d.value>=0?d.value:g(c.value,58))
function g(t,a){const l=e.showFirstLastPage?5:3
return Math.max(0,Math.floor(Number(((t-a*l)/a).toFixed(2))))}const h=t.computed(()=>{if(p.value<=0||isNaN(p.value)||p.value>Number.MAX_SAFE_INTEGER)return[]
if(f.value<=0)return[]
if(1===f.value)return[o.value]
if(p.value<=f.value)return y(p.value,m.value)
const t=f.value%2==0,a=t?f.value/2:Math.floor(f.value/2),l=t?a:a+1,n=p.value-a
if(l-o.value>=0)return[...y(Math.max(1,f.value-1),m.value),e.ellipsis,p.value]
if(o.value-n>=(t?1:0)){const t=f.value-1,a=p.value-t+m.value
return[m.value,e.ellipsis,...y(t,a)]}{const t=Math.max(1,f.value-2),a=1===t?o.value:o.value-Math.ceil(t/2)+m.value
return[m.value,e.ellipsis,...y(t,a),e.ellipsis,p.value]}})
function b(e,t,a){e.preventDefault(),o.value=t,a&&n(a,t)}const{refs:V,updateRef:w}=function(){const e=t.ref([])
return t.onBeforeUpdate(()=>e.value=[]),{refs:e,updateRef:function(t,a){e.value[a]=t}}}()
yt({VPaginationBtn:{color:t.toRef(()=>e.color),border:t.toRef(()=>e.border),density:t.toRef(()=>e.density),size:t.toRef(()=>e.size),variant:t.toRef(()=>e.variant),rounded:t.toRef(()=>e.rounded),elevation:t.toRef(()=>e.elevation)}})
const k=t.computed(()=>h.value.map((t,a)=>{const l=e=>w(e,a)
if("string"==typeof t)return{isActive:!1,key:`ellipsis-${a}`,page:t,props:{ref:l,ellipsis:!0,icon:!0,disabled:!0}}
{const a=t===o.value
return{isActive:a,key:t,page:i(t),props:{ref:l,ellipsis:!1,icon:!0,disabled:!!e.disabled||Number(e.length)<2,color:a?e.activeColor:e.color,"aria-current":a,"aria-label":r(a?e.currentPageAriaLabel:e.pageAriaLabel,t),onClick:e=>b(e,t)}}}})),x=t.computed(()=>{const t=!!e.disabled||o.value<=m.value,a=!!e.disabled||o.value>=m.value+p.value-1
return{first:e.showFirstLastPage?{icon:s.value?e.lastIcon:e.firstIcon,onClick:e=>b(e,m.value,"first"),disabled:t,"aria-label":r(e.firstAriaLabel),"aria-disabled":t}:void 0,prev:{icon:s.value?e.nextIcon:e.prevIcon,onClick:e=>b(e,o.value-1,"prev"),disabled:t,"aria-label":r(e.previousAriaLabel),"aria-disabled":t},next:{icon:s.value?e.prevIcon:e.nextIcon,onClick:e=>b(e,o.value+1,"next"),disabled:a,"aria-label":r(e.nextAriaLabel),"aria-disabled":a},last:e.showFirstLastPage?{icon:s.value?e.firstIcon:e.lastIcon,onClick:e=>b(e,m.value+p.value-1,"last"),disabled:a,"aria-label":r(e.lastAriaLabel),"aria-disabled":a}:void 0}})
function N(){const e=o.value-m.value
V.value[e]?.$el.focus()}function C(a){a.key===S.left&&!e.disabled&&o.value>Number(e.start)?(o.value=o.value-1,t.nextTick(N)):a.key===S.right&&!e.disabled&&o.value<m.value+p.value-1&&(o.value=o.value+1,t.nextTick(N))}return Bt(()=>t.createVNode(e.tag,{ref:v,class:t.normalizeClass(["v-pagination",u.value,e.class]),style:t.normalizeStyle(e.style),role:"navigation","aria-label":r(e.ariaLabel),onKeydown:C,"data-test":"v-pagination-root"},{default:()=>[t.createElementVNode("ul",{class:"v-pagination__list"},[e.showFirstLastPage&&t.createElementVNode("li",{key:"first",class:"v-pagination__first","data-test":"v-pagination-first"},[l.first?l.first(x.value.first):t.createVNode($n,t.mergeProps({_as:"VPaginationBtn"},x.value.first),null)]),t.createElementVNode("li",{key:"prev",class:"v-pagination__prev","data-test":"v-pagination-prev"},[l.prev?l.prev(x.value.prev):t.createVNode($n,t.mergeProps({_as:"VPaginationBtn"},x.value.prev),null)]),k.value.map((e,a)=>t.createElementVNode("li",{key:e.key,class:t.normalizeClass(["v-pagination__item",{"v-pagination__item--is-active":e.isActive}]),"data-test":"v-pagination-item"},[l.item?l.item(e):t.createVNode($n,t.mergeProps({_as:"VPaginationBtn"},e.props),{default:()=>[e.page]})])),t.createElementVNode("li",{key:"next",class:"v-pagination__next","data-test":"v-pagination-next"},[l.next?l.next(x.value.next):t.createVNode($n,t.mergeProps({_as:"VPaginationBtn"},x.value.next),null)]),e.showFirstLastPage&&t.createElementVNode("li",{key:"last",class:"v-pagination__last","data-test":"v-pagination-last"},[l.last?l.last(x.value.last):t.createVNode($n,t.mergeProps({_as:"VPaginationBtn"},x.value.last),null)])])]})),{}}}),av=vt({color:String,prevIcon:{type:Dt,default:"$prev"},nextIcon:{type:Dt,default:"$next"},firstIcon:{type:Dt,default:"$first"},lastIcon:{type:Dt,default:"$last"},itemsPerPageText:{type:String,default:"$vuetify.dataFooter.itemsPerPageText"},pageText:{type:String,default:"$vuetify.dataFooter.pageText"},firstPageLabel:{type:String,default:"$vuetify.dataFooter.firstPage"},prevPageLabel:{type:String,default:"$vuetify.dataFooter.prevPage"},nextPageLabel:{type:String,default:"$vuetify.dataFooter.nextPage"},lastPageLabel:{type:String,default:"$vuetify.dataFooter.lastPage"},itemsPerPageOptions:{type:Array,default:()=>[{value:10,title:"10"},{value:25,title:"25"},{value:50,title:"50"},{value:100,title:"100"},{value:-1,title:"$vuetify.dataFooter.itemsPerPageAll"}]},showCurrentPage:Boolean},"VDataTableFooter"),lv=wt()({name:"VDataTableFooter",props:av(),setup(e,a){let{slots:l}=a
const{t:n}=ma(),{page:o,pageCount:r,startIndex:i,stopIndex:s,itemsLength:u,itemsPerPage:c,setItemsPerPage:d}=function(){const e=t.inject(Rd)
if(!e)throw new Error("Missing pagination!")
return e}(),v=t.computed(()=>e.itemsPerPageOptions.map(e=>"number"==typeof e?{value:e,title:-1===e?n("$vuetify.dataFooter.itemsPerPageAll"):String(e)}:{...e,title:isNaN(Number(e.title))?n(e.title):e.title}))
return Bt(()=>{const a=tv.filterProps(e)
return t.createElementVNode("div",{class:"v-data-table-footer"},[l.prepend?.(),t.createElementVNode("div",{class:"v-data-table-footer__items-per-page"},[t.createElementVNode("span",null,[n(e.itemsPerPageText)]),t.createVNode(ts,{items:v.value,itemColor:e.color,modelValue:c.value,"onUpdate:modelValue":e=>d(Number(e)),density:"compact",variant:"outlined","aria-label":n(e.itemsPerPageText),hideDetails:!0},null)]),t.createElementVNode("div",{class:"v-data-table-footer__info"},[t.createElementVNode("div",null,[n(e.pageText,u.value?i.value+1:0,s.value,u.value)])]),t.createElementVNode("div",{class:"v-data-table-footer__pagination"},[t.createVNode(tv,t.mergeProps({modelValue:o.value,"onUpdate:modelValue":e=>o.value=e,density:"comfortable",firstAriaLabel:e.firstPageLabel,lastAriaLabel:e.lastPageLabel,length:r.value,nextAriaLabel:e.nextPageLabel,previousAriaLabel:e.prevPageLabel,rounded:!0,showFirstLastPage:!0,totalVisible:e.showCurrentPage?1:0,variant:"plain"},I(a,["color"])),null)])])}),{}}}),nv=(ov={align:{type:String,default:"start"},fixed:{type:[Boolean,String],default:!1},fixedOffset:[Number,String],fixedEndOffset:[Number,String],height:[Number,String],lastFixed:Boolean,firstFixedEnd:Boolean,noPadding:Boolean,indent:[Number,String],empty:Boolean,tag:String,width:[Number,String],maxWidth:[Number,String],nowrap:Boolean},rv=(e,a)=>{let{slots:l}=a
const n=e.tag??"td",o="string"==typeof e.fixed?e.fixed:e.fixed?"start":"none"
return t.createVNode(n,{class:t.normalizeClass(["v-data-table__td",{"v-data-table-column--fixed":"start"===o,"v-data-table-column--fixed-end":"end"===o,"v-data-table-column--last-fixed":e.lastFixed,"v-data-table-column--first-fixed-end":e.firstFixedEnd,"v-data-table-column--no-padding":e.noPadding,"v-data-table-column--nowrap":e.nowrap,"v-data-table-column--empty":e.empty},`v-data-table-column--align-${e.align}`]),style:{height:b(e.height),width:b(e.width),maxWidth:b(e.maxWidth),left:"start"===o?b(e.fixedOffset||null):void 0,right:"end"===o?b(e.fixedEndOffset||null):void 0,paddingInlineStart:e.indent?b(e.indent):void 0}},{default:()=>[l.default?.()]})},rv.props=ov,rv)
var ov,rv
const iv=vt({headers:Array},"DataTable-header"),sv=Symbol.for("vuetify:data-table-headers"),uv={title:"",sortable:!1},cv={...uv,width:48}
function dv(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[]
if(e.children)for(const a of e.children)dv(a,t)
else t.push(e)
return t}function vv(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:new Set
for(const a of e)a.key&&t.add(a.key),a.children&&vv(a.children,t)
return t}function pv(e){if(e.key)return"data-table-group"===e.key?uv:["data-table-expand","data-table-select"].includes(e.key)?cv:void 0}function mv(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0
return e.children?Math.max(t,...e.children.map(e=>mv(e,t+1))):t}function fv(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0
if(!e)return t
if(e.children){e.fixedOffset=t
for(const a of e.children)t=fv(a,t)}else e.fixed&&"end"!==e.fixed&&(e.fixedOffset=t,t+=parseFloat(e.width||"0")||0)
return t}function gv(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0
if(!e)return t
if(e.children){e.fixedEndOffset=t
for(const a of e.children)t=gv(a,t)}else"end"===e.fixed&&(e.fixedEndOffset=t,t+=parseFloat(e.width||"0")||0)
return t}function hv(e,t){const a=[]
let l=0
const n=function(){const e=(arguments.length>0&&void 0!==arguments[0]?arguments[0]:[]).map(e=>({element:e,priority:0}))
return{enqueue:(t,a)=>{let l=!1
for(let n=0;n<e.length;n++)if(e[n].priority>a){e.splice(n,0,{element:t,priority:a}),l=!0
break}l||e.push({element:t,priority:a})},size:()=>e.length,count:()=>{let t=0
if(!e.length)return 0
const a=Math.floor(e[0].priority)
for(let l=0;l<e.length;l++)Math.floor(e[l].priority)===a&&(t+=1)
return t},dequeue:()=>e.shift()}}(e)
for(;n.size()>0;){let e=n.count()
const o=[]
let r=1
for(;e>0;){const{element:a,priority:i}=n.dequeue(),s=t-l-mv(a)
if(o.push({...a,rowspan:s??1,colspan:a.children?dv(a).length:1}),a.children)for(const e of a.children){const t=i%1+r/Math.pow(10,l+2)
n.enqueue(e,l+s+t)}r+=1,e-=1}l+=1,a.push(o)}return{columns:e.map(e=>dv(e)).flat(),headers:a}}function yv(e){const t=[]
for(const a of e){const e={...pv(a),...a},l=e.key??("string"==typeof e.value?e.value:null),n=e.value??l??null,o={...e,key:l,value:n,sortable:e.sortable??(null!=e.key||!!e.sort),children:e.children?yv(e.children):void 0}
t.push(o)}return t}function bv(e,a){const n=t.ref([]),o=t.ref([]),r=t.ref({}),i=t.ref({}),s=t.ref({})
t.watchEffect(()=>{const u=(e.headers||Object.keys(e.items[0]??{}).map(e=>({key:e,title:t.capitalize(e)}))).slice(),c=vv(u)
a?.groupBy?.value.length&&!c.has("data-table-group")&&u.unshift({key:"data-table-group",title:"Group"}),a?.showSelect?.value&&!c.has("data-table-select")&&u.unshift({key:"data-table-select"}),a?.showExpand?.value&&!c.has("data-table-expand")&&u.push({key:"data-table-expand"})
const d=yv(u)
!function(e){let t=!1
function a(e,n){let o=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"none"
if(e)if("none"!==o&&(e.fixed=o),!0===e.fixed&&(e.fixed="start"),e.fixed===n)if(e.children)if("start"===n)for(let t=e.children.length-1;t>=0;t--)a(e.children[t],n,n)
else for(let t=0;t<e.children.length;t++)a(e.children[t],n,n)
else t||"start"!==n?t||"end"!==n?isNaN(Number(e.width))?l(`Multiple fixed columns should have a static width (key: ${e.key})`):e.minWidth=Math.max(Number(e.width)||0,Number(e.minWidth)||0):e.firstFixedEnd=!0:e.lastFixed=!0,t=!0
else if(e.children)if("start"===n)for(let t=e.children.length-1;t>=0;t--)a(e.children[t],n)
else for(let t=0;t<e.children.length;t++)a(e.children[t],n)
else t=!1}for(let t=e.length-1;t>=0;t--)a(e[t],"start")
for(let t=0;t<e.length;t++)a(e[t],"end")
let n=0
for(let t=0;t<e.length;t++)n=fv(e[t],n)
let o=0
for(let t=e.length-1;t>=0;t--)o=gv(e[t],o)}(d)
const v=Math.max(...d.map(e=>mv(e)))+1,p=hv(d,v)
n.value=p.headers,o.value=p.columns
const m=p.headers.flat(1)
for(const e of m)e.key&&(e.sortable&&(e.sort&&(r.value[e.key]=e.sort),e.sortRaw&&(i.value[e.key]=e.sortRaw)),e.filter&&(s.value[e.key]=e.filter))})
const u={headers:n,columns:o,sortFunctions:r,sortRawFunctions:i,filterFunctions:s}
return t.provide(sv,u),u}function Vv(){const e=t.inject(sv)
if(!e)throw new Error("Missing headers!")
return e}const wv=vt({color:String,disableSort:Boolean,fixedHeader:Boolean,multiSort:Boolean,initialSortOrder:String,sortAscIcon:{type:Dt,default:"$sortAsc"},sortDescIcon:{type:Dt,default:"$sortDesc"},headerProps:{type:Object},sticky:Boolean,...Tl(),...Ao(),...cn()},"VDataTableHeaders"),kv=wt()({name:"VDataTableHeaders",props:wv(),setup(e,a){let{slots:l}=a
const{t:n}=ma(),{toggleSort:o,sortBy:r,isSorted:i}=Gd(),{someSelected:s,allSelected:u,selectAll:c,showSelectAll:d}=jd(),{columns:v,headers:p}=Vv(),{loaderClasses:m}=dn(e)
function f(t,a){if(!e.sticky&&!e.fixedHeader&&!t.fixed)return
const l="string"==typeof t.fixed?t.fixed:t.fixed?"start":"none"
return{position:"sticky",left:"start"===l?b(t.fixedOffset):void 0,right:"end"===l?b(t.fixedEndOffset):void 0,top:e.sticky||e.fixedHeader?`calc(var(--v-table-header-height) * ${a})`:void 0}}function g(t){const a=r.value.find(e=>e.key===t.key)
return!a&&"asc"===e.initialSortOrder||"asc"===a?.order?e.sortAscIcon:e.sortDescIcon}const{backgroundColorClasses:h,backgroundColorStyles:y}=dl(()=>e.color),{displayClasses:V,mobile:w}=Ro(e),k=t.computed(()=>({headers:p.value,columns:v.value,toggleSort:o,isSorted:i,sortBy:r.value,someSelected:s.value,allSelected:u.value,selectAll:c,getSortIcon:g})),S=t.computed(()=>["v-data-table__th",{"v-data-table__th--sticky":e.sticky||e.fixedHeader},V.value,m.value]),x=a=>{let{column:n,x:v,y:p}=a
const m="data-table-select"===n.key||"data-table-expand"===n.key,V="data-table-group"===n.key&&0===n.width&&!n.title,w=t.mergeProps(e.headerProps??{},n.headerProps??{})
return t.createVNode(nv,t.mergeProps({tag:"th",align:n.align,class:[{"v-data-table__th--sortable":n.sortable&&!e.disableSort,"v-data-table__th--sorted":i(n),"v-data-table__th--fixed":n.fixed},...S.value],style:{width:b(n.width),minWidth:b(n.minWidth),maxWidth:b(n.maxWidth),...f(n,p)},colspan:n.colspan,rowspan:n.rowspan,fixed:n.fixed,nowrap:n.nowrap,lastFixed:n.lastFixed,firstFixedEnd:n.firstFixedEnd,noPadding:m,empty:V,tabindex:n.sortable?0:void 0,onClick:n.sortable?e=>o(n,e):void 0,onKeydown:n.sortable?t=>function(t,a){"Enter"!==t.key||e.disableSort||o(a,t)}(t,n):void 0},w),{default:()=>{const a=`header.${n.key}`,v={column:n,selectAll:c,isSorted:i,toggleSort:o,sortBy:r.value,someSelected:s.value,allSelected:u.value,getSortIcon:g}
return l[a]?l[a](v):V?"":"data-table-select"===n.key?l["header.data-table-select"]?.(v)??(d.value&&t.createVNode(no,{color:e.color,density:e.density,modelValue:u.value,indeterminate:s.value&&!u.value,"onUpdate:modelValue":c},null)):t.createElementVNode("div",{class:"v-data-table-header__content"},[t.createElementVNode("span",null,[n.title]),n.sortable&&!e.disableSort&&t.createVNode(Jl,{key:"icon",class:"v-data-table-header__sort-icon",icon:g(n)},null),e.multiSort&&i(n)&&t.createElementVNode("div",{key:"badge",class:t.normalizeClass(["v-data-table-header__sort-badge",...h.value]),style:t.normalizeStyle(y.value)},[r.value.findIndex(e=>e.key===n.key)+1])])}})},N=()=>{const a=t.computed(()=>v.value.filter(t=>t?.sortable&&!e.disableSort)),l=v.value.find(e=>"data-table-select"===e.key)
return t.createVNode(nv,t.mergeProps({tag:"th",class:[...S.value],colspan:p.value.length+1},e.headerProps),{default:()=>[t.createElementVNode("div",{class:"v-data-table-header__content"},[t.createVNode(ts,{chips:!0,color:e.color,class:"v-data-table__td-sort-select",clearable:!0,density:"default",items:a.value,label:n("$vuetify.dataTable.sortBy"),multiple:e.multiSort,variant:"underlined","onClick:clear":()=>r.value=[]},{append:l?()=>t.createVNode(no,{color:e.color,density:"compact",modelValue:u.value,indeterminate:s.value&&!u.value,"onUpdate:modelValue":()=>c(!u.value)},null):void 0,chip:e=>t.createVNode(Xo,{onClick:e.item.raw?.sortable?()=>o(e.item.raw):void 0,onMousedown:e=>{e.preventDefault(),e.stopPropagation()}},{default:()=>[e.item.title,t.createVNode(Jl,{class:t.normalizeClass(["v-data-table__td-sort-icon",i(e.item.raw)&&"v-data-table__td-sort-icon-active"]),icon:g(e.item.raw),size:"small"},null)]})})])]})}
Bt(()=>w.value?t.createElementVNode("tr",null,[t.createVNode(N,null,null)]):t.createElementVNode(t.Fragment,null,[l.headers?l.headers(k.value):p.value.map((e,a)=>t.createElementVNode("tr",null,[e.map((e,l)=>t.createVNode(x,{column:e,x:l,y:a},null))])),e.loading&&t.createElementVNode("tr",{class:"v-data-table-progress"},[t.createElementVNode("th",{colspan:v.value.length},[t.createVNode(vn,{name:"v-data-table-progress",absolute:!0,active:!0,color:"boolean"==typeof e.loading||"true"===e.loading?e.color:e.loading,indeterminate:!0},{default:l.loader})])])]))}}),Sv=vt({item:{type:Object,required:!0},groupCollapseIcon:{type:Dt,default:"$tableGroupCollapse"},groupExpandIcon:{type:Dt,default:"$tableGroupExpand"},...Tl()},"VDataTableGroupHeaderRow"),xv=wt()({name:"VDataTableGroupHeaderRow",props:Sv(),setup(e,a){let{slots:l}=a
const{isGroupOpen:n,toggleGroup:o,extractRows:r}=Cd(),{isSelected:i,isSomeSelected:s,select:u}=jd(),{columns:c}=Vv(),d=t.computed(()=>r([e.item])),v=t.toRef(()=>c.value.length-(c.value.some(e=>"data-table-select"===e.key)?1:0))
return()=>t.createElementVNode("tr",{class:"v-data-table-group-header-row",style:{"--v-data-table-group-header-row-depth":e.item.depth}},[c.value.map(a=>{if("data-table-group"===a.key){const a=n(e.item)?e.groupCollapseIcon:e.groupExpandIcon,r=()=>o(e.item)
return l["data-table-group"]?.({item:e.item,count:d.value.length,props:{icon:a,onClick:r}})??t.createVNode(nv,{class:"v-data-table-group-header-row__column",colspan:v.value},{default:()=>[t.createVNode($n,{size:"small",variant:"text",icon:a,onClick:r},null),t.createElementVNode("span",null,[e.item.value]),t.createElementVNode("span",null,[t.createTextVNode("("),d.value.length,t.createTextVNode(")")])]})}if("data-table-select"===a.key){const a=d.value.filter(e=>e.selectable),n=a.length>0&&i(a),o=s(a)&&!n,r=e=>u(a,e)
return l["data-table-select"]?.({props:{modelValue:n,indeterminate:o,"onUpdate:modelValue":r}})??t.createVNode(nv,{class:"v-data-table__td--select-row",noPadding:!0},{default:()=>[t.createVNode(no,{density:e.density,disabled:0===a.length,modelValue:n,indeterminate:o,"onUpdate:modelValue":r},null)]})}return""})])}}),Nv=vt({color:String,index:Number,item:Object,cellProps:[Object,Function],collapseIcon:{type:Dt,default:"$collapse"},expandIcon:{type:Dt,default:"$expand"},onClick:Z(),onContextmenu:Z(),onDblclick:Z(),...Tl(),...Ao()},"VDataTableRow"),Cv=wt()({name:"VDataTableRow",props:Nv(),setup(e,a){let{slots:l}=a
const{displayClasses:n,mobile:o}=Ro(e,"v-data-table__tr"),{isSelected:r,toggleSelect:i,someSelected:s,allSelected:u,selectAll:c}=jd(),{isExpanded:d,toggleExpand:v}=wd(),{toggleSort:p,sortBy:m,isSorted:f}=Gd(),{columns:h}=Vv()
Bt(()=>t.createElementVNode("tr",{class:t.normalizeClass(["v-data-table__tr",{"v-data-table__tr--clickable":!!(e.onClick||e.onContextmenu||e.onDblclick)},n.value]),onClick:e.onClick,onContextmenu:e.onContextmenu,onDblclick:e.onDblclick},[e.item&&h.value.map((a,n)=>{const h=e.item,y=`item.${a.key}`,b=`header.${a.key}`,V={index:e.index,item:h.raw,internalItem:h,value:g(h.columns,a.key),column:a,isSelected:r,toggleSelect:i,isExpanded:d,toggleExpand:v},w={column:a,selectAll:c,isSorted:f,toggleSort:p,sortBy:m.value,someSelected:s.value,allSelected:u.value,getSortIcon:()=>""},k="function"==typeof e.cellProps?e.cellProps({index:V.index,item:V.item,internalItem:V.internalItem,value:V.value,column:a}):e.cellProps,S="function"==typeof a.cellProps?a.cellProps({index:V.index,item:V.item,internalItem:V.internalItem,value:V.value}):a.cellProps,x="data-table-select"===a.key||"data-table-expand"===a.key,N="data-table-group"===a.key&&0===a.width&&!a.title
return t.createVNode(nv,t.mergeProps({align:a.align,indent:a.indent,class:{"v-data-table__td--expanded-row":"data-table-expand"===a.key,"v-data-table__td--select-row":"data-table-select"===a.key},fixed:a.fixed,fixedOffset:a.fixedOffset,fixedEndOffset:a.fixedEndOffset,lastFixed:a.lastFixed,firstFixedEnd:a.firstFixedEnd,maxWidth:o.value?void 0:a.maxWidth,noPadding:x,empty:N,nowrap:a.nowrap,width:o.value?void 0:a.width},k,S),{default:()=>{if("data-table-select"===a.key)return l["item.data-table-select"]?.({...V,props:{color:e.color,disabled:!h.selectable,modelValue:r([h]),onClick:t.withModifiers(()=>i(h),["stop"])}})??t.createVNode(no,{color:e.color,disabled:!h.selectable,density:e.density,modelValue:r([h]),onClick:t.withModifiers(t=>i(h,e.index,t),["stop"])},null)
if("data-table-expand"===a.key)return l["item.data-table-expand"]?.({...V,props:{icon:d(h)?e.collapseIcon:e.expandIcon,size:"small",variant:"text",onClick:t.withModifiers(()=>v(h),["stop"])}})??t.createVNode($n,{icon:d(h)?e.collapseIcon:e.expandIcon,size:"small",variant:"text",onClick:t.withModifiers(()=>v(h),["stop"])},null)
if(l[y]&&!o.value)return l[y](V)
const n=t.toDisplayString(V.value)
return o.value?t.createElementVNode(t.Fragment,null,[t.createElementVNode("div",{class:"v-data-table__td-title"},[l[b]?.(w)??a.title]),t.createElementVNode("div",{class:"v-data-table__td-value"},[l[y]?.(V)??n])]):n}})})]))}}),Ev=vt({color:String,loading:[Boolean,String],loadingText:{type:String,default:"$vuetify.dataIterator.loadingText"},hideNoData:Boolean,items:{type:Array,default:()=>[]},noDataText:{type:String,default:"$vuetify.noDataText"},rowProps:[Object,Function],cellProps:[Object,Function],...C(Nv(),["collapseIcon","expandIcon","density"]),...C(Sv(),["groupCollapseIcon","groupExpandIcon","density"]),...Ao()},"VDataTableRows"),Iv=wt()({name:"VDataTableRows",inheritAttrs:!1,props:Ev(),setup(e,a){let{attrs:l,slots:n}=a
const{columns:o}=Vv(),{expandOnClick:r,toggleExpand:i,isExpanded:s}=wd(),{isSelected:u,toggleSelect:c}=jd(),{toggleGroup:d,isGroupOpen:v}=Cd(),{t:p}=ma(),{mobile:m}=Ro(e)
return Bt(()=>{const a=C(e,["groupCollapseIcon","groupExpandIcon","density"])
return!e.loading||e.items.length&&!n.loading?e.loading||e.items.length||e.hideNoData?t.createElementVNode(t.Fragment,null,[e.items.map((p,f)=>{if("group"===p.type){const e={index:f,item:p,columns:o.value,isExpanded:s,toggleExpand:i,isSelected:u,toggleSelect:c,toggleGroup:d,isGroupOpen:v}
return n["group-header"]?n["group-header"](e):t.createVNode(xv,t.mergeProps({key:`group-header_${p.id}`,item:p},_t(l,":groupHeader",()=>e),a),n)}if("group-summary"===p.type){const e={index:f,item:p,columns:o.value,toggleGroup:d}
return n["group-summary"]?.(e)??""}const g={index:p.virtualIndex??f,item:p.raw,internalItem:p,columns:o.value,isExpanded:s,toggleExpand:i,isSelected:u,toggleSelect:c},h={...g,props:t.mergeProps({key:`item_${p.key??p.index}`,onClick:r.value?()=>{i(p)}:void 0,index:f,item:p,color:e.color,cellProps:e.cellProps,collapseIcon:e.collapseIcon,expandIcon:e.expandIcon,density:e.density,mobile:m.value},_t(l,":row",()=>g),"function"==typeof e.rowProps?e.rowProps({item:g.item,index:g.index,internalItem:g.internalItem}):e.rowProps)}
return t.createElementVNode(t.Fragment,{key:h.props.key},[n.item?n.item(h):t.createVNode(Cv,h.props,n),s(p)&&n["expanded-row"]?.(g)])})]):t.createElementVNode("tr",{class:"v-data-table-rows-no-data",key:"no-data"},[t.createElementVNode("td",{colspan:o.value.length},[n["no-data"]?.()??p(e.noDataText)])]):t.createElementVNode("tr",{class:"v-data-table-rows-loading",key:"loading"},[t.createElementVNode("td",{colspan:o.value.length},[n.loading?.()??p(e.loadingText)])])}),{}}}),_v=vt({fixedHeader:Boolean,fixedFooter:Boolean,height:[Number,String],hover:Boolean,striped:{type:String,default:null,validator:e=>["even","odd"].includes(e)},...pt(),...Tl(),...Pa(),...ya()},"VTable"),Pv=wt()({name:"VTable",props:_v(),setup(e,a){let{slots:l,emit:n}=a
const{themeClasses:o}=Ca(e),{densityClasses:r}=Bl(e)
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-table",{"v-table--fixed-height":!!e.height,"v-table--fixed-header":e.fixedHeader,"v-table--fixed-footer":e.fixedFooter,"v-table--has-top":!!l.top,"v-table--has-bottom":!!l.bottom,"v-table--hover":e.hover,"v-table--striped-even":"even"===e.striped,"v-table--striped-odd":"odd"===e.striped},o.value,r.value,e.class]),style:t.normalizeStyle(e.style)},{default:()=>[l.top?.(),l.default?t.createElementVNode("div",{class:"v-table__wrapper",style:{height:b(e.height)}},[t.createElementVNode("table",null,[l.default()])]):l.wrapper?.(),l.bottom?.()]})),{}}}),Av=vt({items:{type:Array,default:()=>[]},itemValue:{type:[String,Array,Function],default:"id"},itemSelectable:{type:[String,Array,Function],default:null},rowProps:[Object,Function],cellProps:[Object,Function],returnObject:Boolean},"DataTable-items")
function Rv(e,t,a){return t.map((t,l)=>function(e,t,a,l){const n=e.returnObject?t:h(t,e.itemValue),o=h(t,e.itemSelectable,!0),r=l.reduce((e,a)=>(null!=a.key&&(e[a.key]=h(t,a.value)),e),{})
return{type:"item",key:e.returnObject?h(t,e.itemValue):n,index:a,value:n,selectable:o,columns:r,raw:t}}(e,t,l,a))}function Tv(e,a){return{items:t.computed(()=>Rv(e,e.items,a.value))}}const Bv=vt({...Ev(),hideDefaultBody:Boolean,hideDefaultFooter:Boolean,hideDefaultHeader:Boolean,width:[String,Number],search:String,...yd(),...kd(),...iv(),...Av(),...zd(),...Hd(),...I(wv(),["multiSort","initialSortOrder"]),..._v()},"DataTable"),Dv=vt({...Ad(),...Bv(),...ns(),...av()},"VDataTable"),Fv=wt()({name:"VDataTable",props:Dv(),emits:{"update:modelValue":e=>!0,"update:page":e=>!0,"update:itemsPerPage":e=>!0,"update:sortBy":e=>!0,"update:options":e=>!0,"update:groupBy":e=>!0,"update:expanded":e=>!0,"update:currentItems":e=>!0},setup(e,a){let{attrs:l,slots:n}=a
const{groupBy:o}=xd(e),{initialSortOrder:r,sortBy:i,multiSort:s,mustSort:u}=Yd(e),{page:c,itemsPerPage:d}=Td(e),{disableSort:v}=t.toRefs(e),{columns:p,headers:m,sortFunctions:f,sortRawFunctions:g,filterFunctions:h}=bv(e,{groupBy:o,showSelect:t.toRef(()=>e.showSelect),showExpand:t.toRef(()=>e.showExpand)}),{items:y}=Tv(e,p),b=t.toRef(()=>e.search),{filteredItems:V}=os(e,y,b,{transform:e=>e.columns,customKeyFilter:h}),{toggleSort:w}=Ud({initialSortOrder:r,sortBy:i,multiSort:s,mustSort:u,page:c}),{sortByWithGroups:k,opened:S,extractRows:x,isGroupOpen:N,toggleGroup:C}=Nd({groupBy:o,sortBy:i,disableSort:v}),{sortedItems:E}=Kd(e,V,k,{transform:e=>({...e.raw,...e.columns}),sortFunctions:f,sortRawFunctions:g}),{flatItems:_}=_d(E,o,S,()=>!!n["group-summary"]),P=t.computed(()=>_.value.length),{startIndex:A,stopIndex:R,pageCount:T,setItemsPerPage:B}=Bd({page:c,itemsPerPage:d,itemsLength:P}),{paginatedItems:D}=Dd({items:_,startIndex:A,stopIndex:R,itemsPerPage:d}),F=t.computed(()=>x(D.value)),{isSelected:$,select:M,selectAll:z,toggleSelect:L,someSelected:O,allSelected:j}=Od(e,{allItems:y,currentPage:F}),{isExpanded:H,toggleExpand:W}=Vd(e)
Pd({page:c,itemsPerPage:d,sortBy:i,groupBy:o,search:b}),yt({VDataTableRows:{hideNoData:t.toRef(()=>e.hideNoData),noDataText:t.toRef(()=>e.noDataText),loading:t.toRef(()=>e.loading),loadingText:t.toRef(()=>e.loadingText)}})
const Y=t.computed(()=>({page:c.value,itemsPerPage:d.value,sortBy:i.value,pageCount:T.value,toggleSort:w,setItemsPerPage:B,someSelected:O.value,allSelected:j.value,isSelected:$,select:M,selectAll:z,toggleSelect:L,isExpanded:H,toggleExpand:W,isGroupOpen:N,toggleGroup:C,items:F.value.map(e=>e.raw),internalItems:F.value,groupedItems:D.value,columns:p.value,headers:m.value}))
return Bt(()=>{const a=lv.filterProps(e),o=kv.filterProps(I(e,["multiSort"])),r=Iv.filterProps(e),i=Pv.filterProps(e)
return t.createVNode(Pv,t.mergeProps({class:["v-data-table",{"v-data-table--show-select":e.showSelect,"v-data-table--loading":e.loading},e.class],style:e.style},i,{fixedHeader:e.fixedHeader||e.sticky}),{top:()=>n.top?.(Y.value),default:()=>n.default?n.default(Y.value):t.createElementVNode(t.Fragment,null,[n.colgroup?.(Y.value),!e.hideDefaultHeader&&t.createElementVNode("thead",{key:"thead"},[t.createVNode(kv,t.mergeProps(o,{multiSort:!!e.multiSort}),n)]),n.thead?.(Y.value),!e.hideDefaultBody&&t.createElementVNode("tbody",null,[n["body.prepend"]?.(Y.value),n.body?n.body(Y.value):t.createVNode(Iv,t.mergeProps(l,r,{items:D.value}),n),n["body.append"]?.(Y.value)]),n.tbody?.(Y.value),n.tfoot?.(Y.value)]),bottom:()=>n.bottom?n.bottom(Y.value):!e.hideDefaultFooter&&t.createElementVNode(t.Fragment,null,[t.createVNode(Jo,null,null),t.createVNode(lv,a,{prepend:n["footer.prepend"]})])})}),{}}}),$v=vt({...I(Bv(),["hideDefaultFooter"]),...kd(),...Ui(),...ns()},"VDataTableVirtual"),Mv=wt()({name:"VDataTableVirtual",props:$v(),emits:{"update:modelValue":e=>!0,"update:sortBy":e=>!0,"update:options":e=>!0,"update:groupBy":e=>!0,"update:expanded":e=>!0},setup(e,a){let{attrs:l,slots:n}=a
const{groupBy:o}=xd(e),{initialSortOrder:r,sortBy:i,multiSort:s,mustSort:u}=Yd(e),{disableSort:c}=t.toRefs(e),{columns:d,headers:v,filterFunctions:p,sortFunctions:m,sortRawFunctions:f}=bv(e,{groupBy:o,showSelect:t.toRef(()=>e.showSelect),showExpand:t.toRef(()=>e.showExpand)}),{items:g}=Tv(e,d),h=t.toRef(()=>e.search),{filteredItems:y}=os(e,g,h,{transform:e=>e.columns,customKeyFilter:p}),{toggleSort:V}=Ud({initialSortOrder:r,sortBy:i,multiSort:s,mustSort:u}),{sortByWithGroups:w,opened:k,extractRows:S,isGroupOpen:x,toggleGroup:N}=Nd({groupBy:o,sortBy:i,disableSort:c}),{sortedItems:C}=Kd(e,y,w,{transform:e=>({...e.raw,...e.columns}),sortFunctions:m,sortRawFunctions:f}),{flatItems:E}=_d(C,o,k,()=>!!n["group-summary"]),_=t.computed(()=>S(E.value)),{isSelected:P,select:A,selectAll:R,toggleSelect:T,someSelected:B,allSelected:D}=Od(e,{allItems:_,currentPage:_}),{isExpanded:F,toggleExpand:$}=Vd(e),{containerRef:M,markerRef:z,paddingTop:L,paddingBottom:O,computedItems:j,handleItemResize:H,handleScroll:W,handleScrollend:Y,calculateVisibleItems:U,scrollToIndex:G}=Gi(e,E),K=t.computed(()=>j.value.map(e=>({...e.raw,virtualIndex:e.index})))
Pd({sortBy:i,page:t.shallowRef(1),itemsPerPage:t.shallowRef(-1),groupBy:o,search:h}),yt({VDataTableRows:{hideNoData:t.toRef(()=>e.hideNoData),noDataText:t.toRef(()=>e.noDataText),loading:t.toRef(()=>e.loading),loadingText:t.toRef(()=>e.loadingText)}})
const q=t.computed(()=>({sortBy:i.value,toggleSort:V,someSelected:B.value,allSelected:D.value,isSelected:P,select:A,selectAll:R,toggleSelect:T,isExpanded:F,toggleExpand:$,isGroupOpen:x,toggleGroup:N,items:_.value.map(e=>e.raw),internalItems:_.value,groupedItems:E.value,columns:d.value,headers:v.value}))
return Bt(()=>{const a=kv.filterProps(I(e,["multiSort"])),o=Iv.filterProps(e),r=Pv.filterProps(e)
return t.createVNode(Pv,t.mergeProps({class:["v-data-table",{"v-data-table--loading":e.loading},e.class],style:e.style},r,{fixedHeader:e.fixedHeader||e.sticky}),{top:()=>n.top?.(q.value),wrapper:()=>t.createElementVNode("div",{ref:M,onScrollPassive:W,onScrollend:Y,class:"v-table__wrapper",style:{height:b(e.height)}},[t.createElementVNode("table",null,[n.colgroup?.(q.value),!e.hideDefaultHeader&&t.createElementVNode("thead",{key:"thead"},[t.createVNode(kv,t.mergeProps(a,{multiSort:!!e.multiSort}),n)]),n.thead?.(q.value),!e.hideDefaultBody&&t.createElementVNode("tbody",{key:"tbody"},[t.createElementVNode("tr",{ref:z,style:{height:b(L.value),border:0}},[t.createElementVNode("td",{colspan:d.value.length,style:{height:0,border:0}},null)]),n["body.prepend"]?.(q.value),t.createVNode(Iv,t.mergeProps(l,o,{items:K.value}),{...n,item:e=>t.createVNode(Yi,{key:e.internalItem.index,renderless:!0,"onUpdate:height":t=>H(e.internalItem.index,t)},{default:a=>{let{itemRef:l}=a
return n.item?.({...e,itemRef:l})??t.createVNode(Cv,t.mergeProps(e.props,{ref:l,key:e.internalItem.index,index:e.index}),n)}})}),n["body.append"]?.(q.value),t.createElementVNode("tr",{style:{height:b(O.value),border:0}},[t.createElementVNode("td",{colspan:d.value.length,style:{height:0,border:0}},null)])]),n.tbody?.(q.value),n.tfoot?.(q.value)])]),bottom:()=>n.bottom?.(q.value)})}),{calculateVisibleItems:U,scrollToIndex:G}}}),zv=vt({itemsLength:{type:[Number,String],required:!0},...Ad(),...Bv(),...av()},"VDataTableServer"),Lv=wt()({name:"VDataTableServer",props:zv(),emits:{"update:modelValue":e=>!0,"update:page":e=>!0,"update:itemsPerPage":e=>!0,"update:sortBy":e=>!0,"update:options":e=>!0,"update:expanded":e=>!0,"update:groupBy":e=>!0},setup(e,a){let{attrs:l,slots:n}=a
const{groupBy:o}=xd(e),{initialSortOrder:r,sortBy:i,multiSort:s,mustSort:u}=Yd(e),{page:c,itemsPerPage:d}=Td(e),{disableSort:v}=t.toRefs(e),p=t.computed(()=>parseInt(e.itemsLength,10)),{columns:m,headers:f}=bv(e,{groupBy:o,showSelect:t.toRef(()=>e.showSelect),showExpand:t.toRef(()=>e.showExpand)}),{items:g}=Tv(e,m),{toggleSort:h}=Ud({initialSortOrder:r,sortBy:i,multiSort:s,mustSort:u,page:c}),{opened:y,isGroupOpen:b,toggleGroup:V,extractRows:w}=Nd({groupBy:o,sortBy:i,disableSort:v}),{pageCount:k,setItemsPerPage:S}=Bd({page:c,itemsPerPage:d,itemsLength:p}),{flatItems:x}=_d(g,o,y,()=>!!n["group-summary"]),{isSelected:N,select:C,selectAll:E,toggleSelect:_,someSelected:P,allSelected:A}=Od(e,{allItems:g,currentPage:g}),{isExpanded:R,toggleExpand:T}=Vd(e),B=t.computed(()=>w(g.value))
Pd({page:c,itemsPerPage:d,sortBy:i,groupBy:o,search:t.toRef(()=>e.search)}),t.provide("v-data-table",{toggleSort:h,sortBy:i}),yt({VDataTableRows:{hideNoData:t.toRef(()=>e.hideNoData),noDataText:t.toRef(()=>e.noDataText),loading:t.toRef(()=>e.loading),loadingText:t.toRef(()=>e.loadingText)}})
const D=t.computed(()=>({page:c.value,itemsPerPage:d.value,sortBy:i.value,pageCount:k.value,toggleSort:h,setItemsPerPage:S,someSelected:P.value,allSelected:A.value,isSelected:N,select:C,selectAll:E,toggleSelect:_,isExpanded:R,toggleExpand:T,isGroupOpen:b,toggleGroup:V,items:B.value.map(e=>e.raw),internalItems:B.value,groupedItems:x.value,columns:m.value,headers:f.value}))
Bt(()=>{const a=lv.filterProps(e),o=kv.filterProps(I(e,["multiSort"])),r=Iv.filterProps(e),i=Pv.filterProps(e)
return t.createVNode(Pv,t.mergeProps({class:["v-data-table",{"v-data-table--loading":e.loading},e.class],style:e.style},i,{fixedHeader:e.fixedHeader||e.sticky}),{top:()=>n.top?.(D.value),default:()=>n.default?n.default(D.value):t.createElementVNode(t.Fragment,null,[n.colgroup?.(D.value),!e.hideDefaultHeader&&t.createElementVNode("thead",{key:"thead",class:"v-data-table__thead",role:"rowgroup"},[t.createVNode(kv,t.mergeProps(o,{multiSort:!!e.multiSort}),n)]),n.thead?.(D.value),!e.hideDefaultBody&&t.createElementVNode("tbody",{class:"v-data-table__tbody",role:"rowgroup"},[n["body.prepend"]?.(D.value),n.body?n.body(D.value):t.createVNode(Iv,t.mergeProps(l,r,{items:x.value}),n),n["body.append"]?.(D.value)]),n.tbody?.(D.value),n.tfoot?.(D.value)]),bottom:()=>n.bottom?n.bottom(D.value):!e.hideDefaultFooter&&t.createElementVNode(t.Fragment,null,[t.createVNode(Jo,null,null),t.createVNode(lv,a,{prepend:n["footer.prepend"]})])})})}}),Ov=vt({fluid:{type:Boolean,default:!1},...pt(),...ol(),...Pa()},"VContainer"),jv=wt()({name:"VContainer",props:Ov(),setup(e,a){let{slots:l}=a
const{rtlClasses:n}=ga(),{dimensionStyles:o}=rl(e)
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-container",{"v-container--fluid":e.fluid},n.value,e.class]),style:t.normalizeStyle([o.value,e.style])},l)),{}}}),Hv=xo.reduce((e,t)=>(e[t]={type:[Boolean,String,Number],default:!1},e),{}),Wv=xo.reduce((e,a)=>(e["offset"+t.capitalize(a)]={type:[String,Number],default:null},e),{}),Yv=xo.reduce((e,a)=>(e["order"+t.capitalize(a)]={type:[String,Number],default:null},e),{}),Uv={col:Object.keys(Hv),offset:Object.keys(Wv),order:Object.keys(Yv)}
function Gv(e,t,a){let l=e
if(null!=a&&!1!==a){if(t){l+=`-${t.replace(e,"")}`}return"col"===e&&(l="v-"+l),"col"!==e||""!==a&&!0!==a?(l+=`-${a}`,l.toLowerCase()):l.toLowerCase()}}const Kv=["auto","start","end","center","baseline","stretch"],qv=vt({cols:{type:[Boolean,String,Number],default:!1},...Hv,offset:{type:[String,Number],default:null},...Wv,order:{type:[String,Number],default:null},...Yv,alignSelf:{type:String,default:null,validator:e=>Kv.includes(e)},...pt(),...Pa()},"VCol"),Xv=wt()({name:"VCol",props:qv(),setup(e,a){let{slots:l}=a
const n=t.computed(()=>{const t=[]
let a
for(a in Uv)Uv[a].forEach(l=>{const n=e[l],o=Gv(a,l,n)
o&&t.push(o)})
const l=t.some(e=>e.startsWith("v-col-"))
return t.push({"v-col":!l||!e.cols,[`v-col-${e.cols}`]:e.cols,[`offset-${e.offset}`]:e.offset,[`order-${e.order}`]:e.order,[`align-self-${e.alignSelf}`]:e.alignSelf}),t})
return()=>t.h(e.tag,{class:[n.value,e.class],style:e.style},l.default?.())}}),Zv=["start","end","center"],Qv=["space-between","space-around","space-evenly"]
function Jv(e,a){return xo.reduce((l,n)=>(l[e+t.capitalize(n)]=a(),l),{})}const ep=[...Zv,"baseline","stretch"],tp=e=>ep.includes(e),ap=Jv("align",()=>({type:String,default:null,validator:tp})),lp=[...Zv,...Qv],np=e=>lp.includes(e),op=Jv("justify",()=>({type:String,default:null,validator:np})),rp=[...Zv,...Qv,"stretch"],ip=e=>rp.includes(e),sp=Jv("alignContent",()=>({type:String,default:null,validator:ip})),up={align:Object.keys(ap),justify:Object.keys(op),alignContent:Object.keys(sp)},cp={align:"align",justify:"justify",alignContent:"align-content"}
function dp(e,t,a){let l=cp[e]
if(null!=a){if(t){l+=`-${t.replace(e,"")}`}return l+=`-${a}`,l.toLowerCase()}}const vp=vt({dense:Boolean,noGutters:Boolean,align:{type:String,default:null,validator:tp},...ap,justify:{type:String,default:null,validator:np},...op,alignContent:{type:String,default:null,validator:ip},...sp,...pt(),...Pa()},"VRow"),pp=wt()({name:"VRow",props:vp(),setup(e,a){let{slots:l}=a
const n=t.computed(()=>{const t=[]
let a
for(a in up)up[a].forEach(l=>{const n=e[l],o=dp(a,l,n)
o&&t.push(o)})
return t.push({"v-row--no-gutters":e.noGutters,"v-row--dense":e.dense,[`align-${e.align}`]:e.align,[`justify-${e.justify}`]:e.justify,[`align-content-${e.alignContent}`]:e.alignContent}),t})
return()=>t.h(e.tag,{class:["v-row",n.value,e.class],style:e.style},l.default?.())}}),mp=kt("v-spacer","div","VSpacer"),fp=vt({active:{type:[String,Array],default:void 0},controlHeight:[Number,String],controlVariant:{type:String,default:"docked"},noMonthPicker:Boolean,disabled:{type:[Boolean,String,Array],default:null},nextIcon:{type:Dt,default:"$next"},prevIcon:{type:Dt,default:"$prev"},modeIcon:{type:Dt,default:"$subgroup"},text:String,monthText:String,yearText:String,viewMode:{type:String,default:"month"}},"VDatePickerControls"),gp=wt()({name:"VDatePickerControls",props:fp(),emits:{"click:year":()=>!0,"click:month":()=>!0,"click:prev":()=>!0,"click:next":()=>!0,"click:prev-year":()=>!0,"click:next-year":()=>!0},setup(e,a){let{emit:l,slots:n}=a
const{t:o}=ma(),r=t.computed(()=>Array.isArray(e.disabled)?e.disabled.includes("text"):!!e.disabled),i=t.computed(()=>Array.isArray(e.disabled)?e.disabled.includes("mode"):!!e.disabled),s=t.computed(()=>Array.isArray(e.disabled)?e.disabled.includes("prev-month"):!!e.disabled),u=t.computed(()=>Array.isArray(e.disabled)?e.disabled.includes("next-month"):!!e.disabled),c=t.computed(()=>Array.isArray(e.disabled)?e.disabled.includes("prev-year"):!!e.disabled),d=t.computed(()=>Array.isArray(e.disabled)?e.disabled.includes("next-year"):!!e.disabled)
function v(){l("click:prev")}function p(){l("click:next")}function m(){l("click:prev-year")}function f(){l("click:next-year")}function g(){l("click:year")}function h(){l("click:month")}return Bt(()=>{const a=t.createVNode($n,{"data-testid":"prev-month",disabled:s.value,icon:e.prevIcon,"aria-label":o("$vuetify.datePicker.ariaLabel.previousMonth"),onClick:v},null),l=t.createVNode($n,{"data-testid":"next-month",disabled:u.value,icon:e.nextIcon,"aria-label":o("$vuetify.datePicker.ariaLabel.nextMonth"),onClick:p},null),y=t.createVNode($n,{"data-testid":"prev-year",disabled:c.value,icon:e.prevIcon,"aria-label":o("$vuetify.datePicker.ariaLabel.previousYear"),onClick:m},null),V=t.createVNode($n,{"data-testid":"next-year",disabled:d.value,icon:e.nextIcon,"aria-label":o("$vuetify.datePicker.ariaLabel.nextYear"),onClick:f},null),w=t.createVNode($n,{class:"v-date-picker-controls__only-month-btn","data-testid":"month-btn",density:"default",disabled:r.value,text:e.monthText,appendIcon:e.modeIcon,rounded:!0,"aria-label":o("$vuetify.datePicker.ariaLabel.selectMonth"),onClick:h},null),k=t.createVNode($n,{class:"v-date-picker-controls__only-year-btn","data-testid":"year-btn",density:"default",disabled:i.value,text:e.yearText,appendIcon:e.modeIcon,rounded:!0,"aria-label":o("$vuetify.datePicker.ariaLabel.selectYear"),onClick:g},null),S=t.createVNode($n,{class:"v-date-picker-controls__year-btn","data-testid":"year-btn",density:"default",disabled:i.value,text:e.text,appendIcon:e.modeIcon,rounded:!0,"aria-label":o("$vuetify.datePicker.ariaLabel.selectYear"),onClick:g},null),x=t.createElementVNode(t.Fragment,null,[t.createVNode($n,{class:"v-date-picker-controls__month-btn","data-testid":"month-btn",height:"36",disabled:r.value,text:e.text,rounded:!0,"aria-label":o("$vuetify.datePicker.ariaLabel.selectMonth"),onClick:h},null),t.createVNode($n,{class:"v-date-picker-controls__mode-btn","data-testid":"year-btn",disabled:i.value,icon:e.modeIcon,"aria-label":o("$vuetify.datePicker.ariaLabel.selectYear"),onClick:g},null)]),N={viewMode:e.viewMode,disabled:Array.isArray(e.disabled)?e.disabled:[],monthYearText:e.text??"",monthText:e.monthText??"",yearText:e.yearText??"",openMonths:h,openYears:g,prevMonth:v,nextMonth:p,prevYear:m,nextYear:f},C=t.createElementVNode(t.Fragment,null,[e.noMonthPicker?S:x,t.createVNode(mp,null,null),t.createElementVNode("div",{class:"v-date-picker-controls__month"},[a,l])]),E=t.createElementVNode(t.Fragment,null,[t.createElementVNode("div",{class:"v-date-picker-controls__month"},[a,w,l]),t.createVNode(mp,null,null),t.createElementVNode("div",{class:"v-date-picker-controls__year"},[y,k,V])])
return t.createVNode(nl,{defaults:{VBtn:{density:"comfortable",variant:"text"}}},{default:()=>[t.createElementVNode("div",{class:t.normalizeClass(["v-date-picker-controls",`v-date-picker-controls--variant-${e.controlVariant}`]),style:{"--v-date-picker-controls-height":b(e.controlHeight)}},[n.default?.(N)??t.createElementVNode(t.Fragment,null,["modal"===e.controlVariant&&C,"docked"===e.controlVariant&&E])])]})}),{}}}),hp=vt({appendIcon:Dt,color:String,header:String,transition:String,onClick:Z()},"VDatePickerHeader"),yp=wt()({name:"VDatePickerHeader",props:hp(),emits:{click:()=>!0,"click:append":()=>!0},setup(e,a){let{emit:l,slots:n}=a
const{backgroundColorClasses:o,backgroundColorStyles:r}=dl(()=>e.color)
function i(){l("click")}function s(){l("click:append")}return Bt(()=>{const a=!(!n.default&&!e.header),l=!(!n.append&&!e.appendIcon)
return t.createElementVNode("div",{class:t.normalizeClass(["v-date-picker-header",{"v-date-picker-header--clickable":!!e.onClick},o.value]),style:t.normalizeStyle(r.value),onClick:i},[n.prepend&&t.createElementVNode("div",{key:"prepend",class:"v-date-picker-header__prepend"},[n.prepend()]),a&&t.createVNode(gl,{key:"content",name:e.transition},{default:()=>[t.createElementVNode("div",{key:e.header,class:"v-date-picker-header__content"},[n.default?.()??e.header])]}),l&&t.createElementVNode("div",{class:"v-date-picker-header__append"},[n.append?t.createVNode(nl,{key:"append-defaults",disabled:!e.appendIcon,defaults:{VBtn:{icon:e.appendIcon,variant:"text"}}},{default:()=>[n.append?.()]}):t.createVNode($n,{key:"append-btn",icon:e.appendIcon,variant:"text",onClick:s},null)])])}),{}}}),bp=vt({allowedDates:[Array,Function],disabled:{type:Boolean,default:null},displayValue:null,modelValue:Array,month:[Number,String],max:null,min:null,showAdjacentMonths:Boolean,year:[Number,String],weekdays:{type:Array,default:()=>[0,1,2,3,4,5,6]},weeksInMonth:{type:String,default:"dynamic"},firstDayOfWeek:{type:[Number,String],default:void 0},firstDayOfYear:{type:[Number,String],default:void 0},weekdayFormat:String},"calendar")
function Vp(e){const a=_u(),l=t.computed(()=>{if(!e.min)return null
const t=a.date(e.min)
return a.isValid(t)?t:null}),n=t.computed(()=>{if(!e.max)return null
const t=a.date(e.max)
return a.isValid(t)?t:null})
return{minDate:l,maxDate:n,clampDate:function(e){return l.value&&a.isBefore(e,l.value)?l.value:n.value&&a.isAfter(e,n.value)?n.value:e},isInAllowedRange:function(e){return(!l.value||a.isAfter(e,l.value))&&(!n.value||a.isBefore(e,n.value))}}}const wp=vt({color:String,hideWeekdays:Boolean,multiple:[Boolean,Number,String],showWeek:Boolean,transition:{type:String,default:"picker-transition"},reverseTransition:{type:String,default:"picker-reverse-transition"},events:{type:[Array,Function,Object],default:()=>null},eventColor:{type:[Array,Function,Object,String],default:()=>null},...I(bp(),["displayValue"])},"VDatePickerMonth"),kp=wt()({name:"VDatePickerMonth",props:wp(),emits:{"update:modelValue":e=>!0,"update:month":e=>!0,"update:year":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const o=t.ref(),{t:r}=ma(),{daysInMonth:i,model:s,weekNumbers:u,weekdayLabels:c}=function(e){const a=_u(),l=la(e,"modelValue",[],e=>B(e).map(e=>a.date(e))),n=t.computed(()=>e.displayValue?a.date(e.displayValue):l.value.length>0?a.date(l.value[0]):e.min?a.date(e.min):Array.isArray(e.allowedDates)?a.date(e.allowedDates[0]):a.date()),o=la(e,"year",void 0,e=>{const t=null!=e?Number(e):a.getYear(n.value)
return a.startOfYear(a.setYear(a.date(),t))},e=>a.getYear(e)),r=la(e,"month",void 0,e=>{const t=null!=e?Number(e):a.getMonth(n.value),l=a.setYear(a.startOfMonth(a.date()),a.getYear(o.value))
return a.setMonth(l,t)},e=>a.getMonth(e)),i=t.computed(()=>{const t=a.toJsDate(a.startOfWeek(a.date(),e.firstDayOfWeek)).getDay()
return a.getWeekdays(e.firstDayOfWeek,e.weekdayFormat).filter((a,l)=>e.weekdays.includes((l+t)%7))}),s=t.computed(()=>{const t=a.getWeekArray(r.value,e.firstDayOfWeek),l=t.flat()
if("static"===e.weeksInMonth&&l.length<42){const e=l[l.length-1]
let n=[]
for(let o=1;o<=42-l.length;o++)n.push(a.addDays(e,o)),o%7==0&&(t.push(n),n=[])}return t})
function u(t,n){return t.filter(t=>e.weekdays.includes(a.toJsDate(t).getDay())).map((t,o)=>{const i=a.toISO(t),s=!a.isSameMonth(t,r.value),u=a.isSameDay(t,a.startOfMonth(r.value)),c=a.isSameDay(t,a.endOfMonth(r.value)),d=a.isSameDay(t,r.value),v=e.weekdays.length
return{date:t,formatted:a.format(t,"keyboardDate"),isAdjacent:s,isDisabled:f(t),isEnd:c,isHidden:s&&!e.showAdjacentMonths,isSame:d,isSelected:l.value.some(e=>a.isSameDay(t,e)),isStart:u,isToday:a.isSameDay(t,n),isWeekEnd:o%v===v-1,isWeekStart:o%v===0,isoDate:i,localized:a.format(t,"dayOfMonth"),month:a.getMonth(t),year:a.getYear(t)}})}const c=t.computed(()=>{const t=a.startOfWeek(n.value,e.firstDayOfWeek),l=[]
for(let e=0;e<=6;e++)l.push(a.addDays(t,e))
return u(l,a.date())}),d=t.computed(()=>u(s.value.flat(),a.date())),v=t.computed(()=>s.value.map(t=>t.length?a.getWeek(t[0],e.firstDayOfWeek,e.firstDayOfYear):null)),{minDate:p,maxDate:m}=Vp(e)
function f(t){if(e.disabled)return!0
const l=a.date(t)
return!((!p.value||!a.isBefore(a.endOfDay(l),p.value))&&(!m.value||!a.isAfter(l,m.value))&&(Array.isArray(e.allowedDates)&&e.allowedDates.length>0?e.allowedDates.some(e=>a.isSameDay(a.date(e),l)):"function"!=typeof e.allowedDates||e.allowedDates(l)))}return{displayValue:n,daysInMonth:d,daysInWeek:c,genDays:u,model:l,weeksInMonth:s,weekdayLabels:i,weekNumbers:v}}(e),d=_u(),v=t.shallowRef(),p=t.shallowRef(),m=t.shallowRef(!1),f=t.toRef(()=>m.value?e.reverseTransition:e.transition)
"range"===e.multiple&&s.value.length>0&&(v.value=s.value[0],s.value.length>1&&(p.value=s.value[s.value.length-1]))
const g=t.computed(()=>{const t=["number","string"].includes(typeof e.multiple)?Number(e.multiple):1/0
return s.value.length>=t})
function h(e){const t=d.startOfDay(e)
if(0===s.value.length?v.value=void 0:1===s.value.length&&(v.value=s.value[0],p.value=void 0),v.value)if(p.value)v.value=e,p.value=void 0,s.value=[v.value]
else{if(d.isSameDay(t,v.value))return v.value=void 0,void(s.value=[])
d.isBefore(t,v.value)?(p.value=d.endOfDay(v.value),v.value=t):p.value=d.endOfDay(t),s.value=function(e,t,a){const l=Eu(e,t,a),n=[t]
for(let a=1;a<l;a++){const l=e.addDays(t,a)
n.push(l)}return a&&n.push(e.endOfDay(a)),n}(d,v.value,p.value)}else v.value=t,s.value=[v.value]}function y(e){const t=d.format(e.date,"fullDateWithWeekday"),a=e.isToday?"currentDate":"selectDate"
return r(`$vuetify.datePicker.ariaLabel.${a}`,t)}function b(t){"range"===e.multiple?h(t):e.multiple?function(e){const t=s.value.findIndex(t=>d.isSameDay(t,e))
if(-1===t)s.value=[...s.value,e]
else{const e=[...s.value]
e.splice(t,1),s.value=e}}(t):s.value=[t]}function V(a){const l=function(t){const{events:a,eventColor:l}=e
let n,o=[]
return n=Array.isArray(a)?a.includes(t):a instanceof Function?a(t)||!1:a&&a[t]||!1,n?(!0!==n?o=B(n):"string"==typeof l?o=[l]:"function"==typeof l?o=B(l(t)):Array.isArray(l)?o=l:"object"==typeof l&&null!==l&&(o=B(l[t])),o.length?o.filter(Boolean).map(e=>"string"==typeof e?e:"surface-variant"):["surface-variant"]):[]}(a)
return l.length?t.createElementVNode("div",{class:"v-date-picker-month__events"},[l.map(e=>t.createVNode(cs,{dot:!0,color:e},null))]):null}t.watch(i,(e,t)=>{t&&(m.value=d.isBefore(e[0].date,t[0].date))}),Bt(()=>t.createElementVNode("div",{class:"v-date-picker-month",style:{"--v-date-picker-days-in-week":e.weekdays.length}},[e.showWeek&&t.createElementVNode("div",{key:"weeks",class:"v-date-picker-month__weeks"},[!e.hideWeekdays&&t.createElementVNode("div",{key:"hide-week-days",class:"v-date-picker-month__day"},[t.createTextVNode(" ")]),u.value.map(e=>t.createElementVNode("div",{class:t.normalizeClass(["v-date-picker-month__day","v-date-picker-month__day--adjacent"])},[e]))]),t.createVNode(gl,{name:f.value},{default:()=>[t.createElementVNode("div",{ref:o,key:i.value[0].date?.toString(),class:"v-date-picker-month__days"},[!e.hideWeekdays&&c.value.map(e=>t.createElementVNode("div",{class:t.normalizeClass(["v-date-picker-month__day","v-date-picker-month__weekday"])},[e])),i.value.map((a,l)=>{const o={props:{class:"v-date-picker-month__day-btn",color:a.isSelected||a.isToday?e.color:void 0,disabled:a.isDisabled,icon:!0,ripple:!1,variant:a.isSelected?"flat":a.isToday?"outlined":"text","aria-label":y(a),"aria-current":a.isToday?"date":void 0,onClick:()=>b(a.date)},item:a,i:l}
return g.value&&!a.isSelected&&(a.isDisabled=!0),t.createElementVNode("div",{class:t.normalizeClass(["v-date-picker-month__day",{"v-date-picker-month__day--adjacent":a.isAdjacent,"v-date-picker-month__day--hide-adjacent":a.isHidden,"v-date-picker-month__day--selected":a.isSelected,"v-date-picker-month__day--week-end":a.isWeekEnd,"v-date-picker-month__day--week-start":a.isWeekStart}]),"data-v-date":a.isDisabled?void 0:a.isoDate},[(e.showAdjacentMonths||!a.isAdjacent)&&(n.day?.(o)??t.createVNode($n,o.props,{default:()=>[a.localized,V(a.isoDate)]}))])})])]})]))}}),Sp=vt({color:String,height:[String,Number],min:null,max:null,modelValue:Number,year:Number,allowedMonths:[Array,Function]},"VDatePickerMonths"),xp=wt()({name:"VDatePickerMonths",props:Sp(),emits:{"update:modelValue":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const o=_u(),r=la(e,"modelValue"),i=t.computed(()=>{let t=o.startOfYear(o.date())
return e.year&&(t=o.setYear(t,e.year)),y(12).map(a=>{const l=o.format(t,"monthShort"),n=o.format(t,"month"),r=!!(!function(t){if(Array.isArray(e.allowedMonths)&&e.allowedMonths.length)return e.allowedMonths.includes(t)
if("function"==typeof e.allowedMonths)return e.allowedMonths(t)
return!0}(a)||e.min&&o.isAfter(o.startOfMonth(o.date(e.min)),t)||e.max&&o.isAfter(t,o.startOfMonth(o.date(e.max))))
return t=o.getNextMonth(t),{isDisabled:r,text:l,label:n,value:a}})})
return t.watchEffect(()=>{r.value=r.value??o.getMonth(o.date())}),Bt(()=>t.createElementVNode("div",{class:"v-date-picker-months",style:{height:b(e.height)}},[t.createElementVNode("div",{class:"v-date-picker-months__content"},[i.value.map((a,o)=>{const i={active:r.value===o,ariaLabel:a.label,color:r.value===o?e.color:void 0,disabled:a.isDisabled,rounded:!0,text:a.text,variant:r.value===a.value?"flat":"text",onClick:()=>function(e){if(r.value===e)return void l("update:modelValue",r.value)
r.value=e}(o)}
return n.month?.({month:a,i:o,props:i})??t.createVNode($n,t.mergeProps({key:"month"},i),null)})])])),{}}}),Np=vt({color:String,height:[String,Number],min:null,max:null,modelValue:Number,allowedYears:[Array,Function]},"VDatePickerYears"),Cp=wt()({name:"VDatePickerYears",props:Np(),directives:{vIntersect:yl},emits:{"update:modelValue":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const o=_u(),r=la(e,"modelValue"),i=t.shallowRef(!1),s=t.computed(()=>{const t=o.getYear(o.date())
let a=t-100,l=t+52
e.min&&(a=o.getYear(o.date(e.min))),e.max&&(l=o.getYear(o.date(e.max)))
let n=o.startOfYear(o.date())
return n=o.setYear(n,a),y(l-a+1,a).map(e=>{const t=o.format(n,"year")
return n=o.setYear(n,o.getYear(n)+1),{text:t,value:e,isDisabled:!d(e)}})})
t.watchEffect(()=>{r.value=r.value??o.getYear(o.date())})
const u=se()
function c(){u.el?.scrollIntoView({block:"center"})}function d(t){return Array.isArray(e.allowedYears)&&e.allowedYears.length?e.allowedYears.includes(t):"function"!=typeof e.allowedYears||e.allowedYears(t)}return Bt(()=>t.withDirectives(t.createElementVNode("div",{class:"v-date-picker-years",style:{height:b(e.height)}},[t.createElementVNode("div",{class:"v-date-picker-years__content",onFocus:()=>u.el?.focus(),onFocusin:()=>i.value=!0,onFocusout:()=>i.value=!1,tabindex:i.value?-1:0},[s.value.map((a,o)=>{const i={ref:r.value===a.value?u:void 0,active:r.value===a.value,color:r.value===a.value?e.color:void 0,rounded:!0,text:a.text,disabled:a.isDisabled,variant:r.value===a.value?"flat":"text",onClick:()=>{r.value!==a.value?r.value=a.value:l("update:modelValue",r.value)}}
return n.year?.({year:a,i:o,props:i})??t.createVNode($n,t.mergeProps({key:"month"},i),null)})])]),[[yl,{handler:c},null,{once:!0}]])),{}}}),Ep=vt({header:{type:String,default:"$vuetify.datePicker.header"},headerColor:String,headerDateFormat:{type:String,default:"normalDateWithWeekday"},landscapeHeaderWidth:[Number,String],...I(fp(),["active","monthText","yearText"]),...wp({weeksInMonth:"static"}),...I(Sp(),["modelValue"]),...I(Np(),["modelValue"]),...dd({title:"$vuetify.datePicker.title"}),modelValue:null},"VDatePicker"),Ip=wt()({name:"VDatePicker",props:Ep(),emits:{"update:modelValue":e=>!0,"update:month":e=>!0,"update:year":e=>!0,"update:viewMode":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const o=_u(),{t:r}=ma(),{rtlClasses:i}=ga(),s=la(e,"modelValue",void 0,e=>B(e).map(e=>o.date(e)),t=>e.multiple?t:t[0]),u=la(e,"viewMode"),{minDate:c,maxDate:d,clampDate:v}=Vp(e),p=t.computed(()=>{const e=o.date(),t=s.value?.[0]?o.date(s.value[0]):v(e)
return t&&o.isValid(t)?t:e}),m=t.toRef(()=>e.headerColor??e.color),f=la(e,"month"),g=t.computed({get:()=>Number(f.value??o.getMonth(o.startOfMonth(p.value))),set:e=>f.value=e}),h=la(e,"year"),y=t.computed({get:()=>Number(h.value??o.getYear(o.startOfYear(o.setMonth(p.value,g.value)))),set:e=>h.value=e}),V=t.shallowRef(!1),w=t.computed(()=>{if(e.multiple&&s.value.length>1)return r("$vuetify.datePicker.itemsSelected",s.value.length)
const t=s.value[0]&&o.isValid(s.value[0])?o.format(o.date(s.value[0]),e.headerDateFormat):r(e.header)
return e.landscape&&3===t.split(" ").length?t.replace(" ","\n"):t}),k=t.toRef(()=>{let e=o.date()
return e=o.setDate(e,1),e=o.setMonth(e,g.value),e=o.setYear(e,y.value),e}),S=t.toRef(()=>o.format(k.value,"monthAndYear")),x=t.toRef(()=>o.format(k.value,"monthShort")),N=t.toRef(()=>o.format(k.value,"year")),C=t.toRef(()=>`date-picker-header${V.value?"-reverse":""}-transition`),E=t.computed(()=>{if(e.disabled)return!0
const t=[]
if("month"!==u.value)t.push("prev-month","next-month","prev-year","next-year")
else{let e=o.date()
if(e=o.startOfMonth(e),e=o.setMonth(e,g.value),e=o.setYear(e,y.value),c.value){const a=o.addDays(o.startOfMonth(e),-1),l=o.addDays(o.startOfYear(e),-1)
o.isAfter(c.value,a)&&t.push("prev-month"),o.isAfter(c.value,l)&&t.push("prev-year")}if(d.value){const a=o.addDays(o.endOfMonth(e),1),l=o.addDays(o.endOfYear(e),1)
o.isAfter(a,d.value)&&t.push("next-month"),o.isAfter(l,d.value)&&t.push("next-year")}}return t}),_=t.computed(()=>e.allowedYears||R),P=t.computed(()=>e.allowedMonths||T)
function A(t,a){const l=e.allowedDates
if("function"!=typeof l)return!0
const n=1+Eu(o,t,a)
for(let e=0;e<n;e++)if(l(o.addDays(t,e)))return!0
return!1}function R(t){if("function"==typeof e.allowedDates){const e=o.parseISO(`${t}-01-01`)
return A(e,o.endOfYear(e))}if(Array.isArray(e.allowedDates)&&e.allowedDates.length){for(const a of e.allowedDates)if(o.getYear(o.date(a))===t)return!0
return!1}return!0}function T(t){if("function"==typeof e.allowedDates){const e=String(t+1).padStart(2,"0"),a=o.parseISO(`${y.value}-${e}-01`)
return A(a,o.endOfMonth(a))}if(Array.isArray(e.allowedDates)&&e.allowedDates.length){for(const a of e.allowedDates)if(o.getYear(o.date(a))===y.value&&o.getMonth(o.date(a))===t)return!0
return!1}return!0}function D(){g.value<11?g.value++:(y.value++,g.value=0,H()),j()}function F(){g.value>0?g.value--:(y.value--,g.value=11,H()),j()}function $(){if(y.value++,d.value){const e=String(g.value+1).padStart(2,"0"),t=o.parseISO(`${y.value}-${e}-01`)
o.isAfter(t,d.value)&&(g.value=o.getMonth(d.value))}H()}function M(){if(y.value--,c.value){const e=String(g.value+1).padStart(2,"0"),t=o.endOfMonth(o.parseISO(`${y.value}-${e}-01`))
o.isAfter(c.value,t)&&(g.value=o.getMonth(c.value))}H()}function z(){u.value="month"}function L(){u.value="months"===u.value?"month":"months"}function O(){u.value="year"===u.value?"month":"year"}function j(){"months"===u.value&&L()}function H(){"year"===u.value&&O()}return t.watch(s,(e,t)=>{const a=B(t),l=B(e)
if(!l.length)return
const n=o.date(a[a.length-1]),r=o.date(l[l.length-1])
if(o.isSameDay(n,r))return
const i=o.getMonth(r),s=o.getYear(r)
i!==g.value&&(g.value=i,j()),s!==y.value&&(y.value=s,H()),V.value=o.isBefore(n,r)}),Bt(()=>{const a=vd.filterProps(e),l=I(gp.filterProps(e),["viewMode"]),o=yp.filterProps(e),v=kp.filterProps(e),p=I(xp.filterProps(e),["modelValue"]),f=I(Cp.filterProps(e),["modelValue"]),h={color:m.value,header:w.value,transition:C.value}
return t.createVNode(vd,t.mergeProps(a,{color:m.value,class:["v-date-picker",`v-date-picker--${u.value}`,{"v-date-picker--show-week":e.showWeek},i.value,e.class],style:[{"--v-date-picker-landscape-header-width":b(e.landscapeHeaderWidth)},e.style]}),{title:()=>n.title?.()??t.createElementVNode("div",{class:"v-date-picker__title"},[r(e.title)]),header:()=>n.header?t.createVNode(nl,{defaults:{VDatePickerHeader:{...h}}},{default:()=>[n.header?.(h)]}):t.createVNode(yp,t.mergeProps({key:"header"},o,h,{onClick:"month"!==u.value?z:void 0}),{prepend:n.prepend,append:n.append}),default:()=>t.createElementVNode(t.Fragment,null,[t.createVNode(gp,t.mergeProps(l,{disabled:E.value,viewMode:u.value,text:S.value,monthText:x.value,yearText:N.value,"onClick:next":D,"onClick:prev":F,"onClick:nextYear":$,"onClick:prevYear":M,"onClick:month":L,"onClick:year":O}),{default:n.controls}),t.createVNode(Ya,{hideOnLeave:!0},{default:()=>["months"===u.value?t.createVNode(xp,t.mergeProps({key:"date-picker-months"},p,{modelValue:g.value,"onUpdate:modelValue":[e=>g.value=e,j],min:c.value,max:d.value,year:y.value,allowedMonths:P.value}),{month:n.month}):"year"===u.value?t.createVNode(Cp,t.mergeProps({key:"date-picker-years"},f,{modelValue:y.value,"onUpdate:modelValue":[e=>y.value=e,H],min:c.value,max:d.value,allowedYears:_.value}),{year:n.year}):t.createVNode(kp,t.mergeProps({key:"date-picker-month"},v,{modelValue:s.value,"onUpdate:modelValue":e=>s.value=e,month:g.value,"onUpdate:month":[e=>g.value=e,j],year:y.value,"onUpdate:year":[e=>y.value=e,H],min:c.value,max:d.value}),{day:n.day})]})]),actions:n.actions})}),{}}}),_p=vt({actionText:String,bgColor:String,color:String,icon:Dt,image:String,justify:{type:String,default:"center"},headline:String,title:String,text:String,textWidth:{type:[Number,String],default:500},href:String,to:String,...pt(),...ol(),...Xl({size:void 0}),...ya()},"VEmptyState"),Pp=wt()({name:"VEmptyState",props:_p(),emits:{"click:action":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const{themeClasses:o}=Ca(e),{backgroundColorClasses:r,backgroundColorStyles:i}=dl(()=>e.bgColor),{dimensionStyles:s}=rl(e),{displayClasses:u}=Ro()
function c(e){l("click:action",e)}return Bt(()=>{const a=!(!n.actions&&!e.actionText),l=!(!n.headline&&!e.headline),d=!(!n.title&&!e.title),v=!(!n.text&&!e.text),p=!!(n.media||e.image||e.icon),m=e.size||(e.image?200:96)
return t.createElementVNode("div",{class:t.normalizeClass(["v-empty-state",{[`v-empty-state--${e.justify}`]:!0},o.value,r.value,u.value,e.class]),style:t.normalizeStyle([i.value,s.value,e.style])},[p&&t.createElementVNode("div",{key:"media",class:"v-empty-state__media"},[n.media?t.createVNode(nl,{key:"media-defaults",defaults:{VImg:{src:e.image,height:m},VIcon:{size:m,icon:e.icon}}},{default:()=>[n.media()]}):t.createElementVNode(t.Fragment,null,[e.image?t.createVNode(Vl,{key:"image",src:e.image,height:m},null):e.icon?t.createVNode(Jl,{key:"icon",color:e.color,size:m,icon:e.icon},null):void 0])]),l&&t.createElementVNode("div",{key:"headline",class:"v-empty-state__headline"},[n.headline?.()??e.headline]),d&&t.createElementVNode("div",{key:"title",class:"v-empty-state__title"},[n.title?.()??e.title]),v&&t.createElementVNode("div",{key:"text",class:"v-empty-state__text",style:{maxWidth:b(e.textWidth)}},[n.text?.()??e.text]),n.default&&t.createElementVNode("div",{key:"content",class:"v-empty-state__content"},[n.default()]),a&&t.createElementVNode("div",{key:"actions",class:"v-empty-state__actions"},[t.createVNode(nl,{defaults:{VBtn:{class:"v-empty-state__action-btn",color:e.color??"surface-variant",href:e.href,text:e.actionText,to:e.to}}},{default:()=>[n.actions?.({props:{onClick:c}})??t.createVNode($n,{onClick:c},null)]})])])}),{}}}),Ap=Symbol.for("vuetify:v-expansion-panel"),Rp=vt({...pt(),...gi()},"VExpansionPanelText"),Tp=wt()({name:"VExpansionPanelText",props:Rp(),setup(e,a){let{slots:l}=a
const n=t.inject(Ap)
if(!n)throw new Error("[Vuetify] v-expansion-panel-text needs to be placed inside v-expansion-panel")
const{hasContent:o,onAfterLeave:r}=hi(e,n.isSelected)
return Bt(()=>t.createVNode(tl,{onAfterLeave:r},{default:()=>[t.withDirectives(t.createElementVNode("div",{class:t.normalizeClass(["v-expansion-panel-text",e.class]),style:t.normalizeStyle(e.style)},[l.default&&o.value&&t.createElementVNode("div",{class:"v-expansion-panel-text__wrapper"},[l.default?.()])]),[[t.vShow,n.isSelected.value]])]})),{}}}),Bp=vt({color:String,expandIcon:{type:Dt,default:"$expand"},collapseIcon:{type:Dt,default:"$collapse"},hideActions:Boolean,focusable:Boolean,static:Boolean,ripple:{type:[Boolean,Object],default:!1},readonly:Boolean,...pt(),...ol()},"VExpansionPanelTitle"),Dp=wt()({name:"VExpansionPanelTitle",directives:{vRipple:Dn},props:Bp(),setup(e,a){let{slots:l}=a
const n=t.inject(Ap)
if(!n)throw new Error("[Vuetify] v-expansion-panel-title needs to be placed inside v-expansion-panel")
const{backgroundColorClasses:o,backgroundColorStyles:r}=dl(()=>e.color),{dimensionStyles:i}=rl(e),s=t.computed(()=>({collapseIcon:e.collapseIcon,disabled:n.disabled.value,expanded:n.isSelected.value,expandIcon:e.expandIcon,readonly:e.readonly})),u=t.toRef(()=>n.isSelected.value?e.collapseIcon:e.expandIcon)
return Bt(()=>t.withDirectives(t.createElementVNode("button",{class:t.normalizeClass(["v-expansion-panel-title",{"v-expansion-panel-title--active":n.isSelected.value,"v-expansion-panel-title--focusable":e.focusable,"v-expansion-panel-title--static":e.static},o.value,e.class]),style:t.normalizeStyle([r.value,i.value,e.style]),type:"button",tabindex:n.disabled.value?-1:void 0,disabled:n.disabled.value,"aria-expanded":n.isSelected.value,onClick:e.readonly?void 0:n.toggle},[t.createElementVNode("span",{class:"v-expansion-panel-title__overlay"},null),l.default?.(s.value),!e.hideActions&&t.createVNode(nl,{defaults:{VIcon:{icon:u.value}}},{default:()=>[t.createElementVNode("span",{class:"v-expansion-panel-title__icon"},[l.actions?.(s.value)??t.createVNode(Jl,null,null)])]})]),[[Dn,e.ripple]])),{}}}),Fp=vt({title:String,text:String,bgColor:String,...Sl(),...jl(),...pl(),...Pa(),...Bp(),...Rp()},"VExpansionPanel"),$p=wt()({name:"VExpansionPanel",props:Fp(),emits:{"group:selected":e=>!0},setup(e,a){let{slots:l}=a
const n=Hl(e,Ap),{backgroundColorClasses:o,backgroundColorStyles:r}=dl(()=>e.bgColor),{elevationClasses:i}=xl(e),{roundedClasses:s}=ml(e),u=t.toRef(()=>n?.disabled.value||e.disabled),c=t.computed(()=>n.group.items.value.reduce((e,t,a)=>(n.group.selected.value.includes(t.id)&&e.push(a),e),[])),d=t.computed(()=>{const e=n.group.items.value.findIndex(e=>e.id===n.id)
return!n.isSelected.value&&c.value.some(t=>t-e===1)}),v=t.computed(()=>{const e=n.group.items.value.findIndex(e=>e.id===n.id)
return!n.isSelected.value&&c.value.some(t=>t-e===-1)})
return t.provide(Ap,n),Bt(()=>{const a=!(!l.text&&!e.text),c=!(!l.title&&!e.title),p=Dp.filterProps(e),m=Tp.filterProps(e)
return t.createVNode(e.tag,{class:t.normalizeClass(["v-expansion-panel",{"v-expansion-panel--active":n.isSelected.value,"v-expansion-panel--before-active":d.value,"v-expansion-panel--after-active":v.value,"v-expansion-panel--disabled":u.value},s.value,o.value,e.class]),style:t.normalizeStyle([r.value,e.style])},{default:()=>[t.createElementVNode("div",{class:t.normalizeClass(["v-expansion-panel__shadow",...i.value])},null),t.createVNode(nl,{defaults:{VExpansionPanelTitle:{...p},VExpansionPanelText:{...m}}},{default:()=>[c&&t.createVNode(Dp,{key:"title"},{default:()=>[l.title?l.title():e.title]}),a&&t.createVNode(Tp,{key:"text"},{default:()=>[l.text?l.text():e.text]}),l.default?.()]})]})}),{groupItem:n}}}),Mp=["default","accordion","inset","popout"],zp=vt({flat:Boolean,...Ol(),...C(Fp(),["bgColor","collapseIcon","color","eager","elevation","expandIcon","focusable","hideActions","readonly","ripple","rounded","tile","static"]),...ya(),...pt(),...Pa(),variant:{type:String,default:"default",validator:e=>Mp.includes(e)}},"VExpansionPanels"),Lp=wt()({name:"VExpansionPanels",props:zp(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const{next:n,prev:o}=Wl(e,Ap),{themeClasses:r}=Ca(e),i=t.toRef(()=>e.variant&&`v-expansion-panels--variant-${e.variant}`)
return yt({VExpansionPanel:{bgColor:t.toRef(()=>e.bgColor),collapseIcon:t.toRef(()=>e.collapseIcon),color:t.toRef(()=>e.color),eager:t.toRef(()=>e.eager),elevation:t.toRef(()=>e.elevation),expandIcon:t.toRef(()=>e.expandIcon),focusable:t.toRef(()=>e.focusable),hideActions:t.toRef(()=>e.hideActions),readonly:t.toRef(()=>e.readonly),ripple:t.toRef(()=>e.ripple),rounded:t.toRef(()=>e.rounded),static:t.toRef(()=>e.static)}}),Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-expansion-panels",{"v-expansion-panels--flat":e.flat,"v-expansion-panels--tile":e.tile},r.value,i.value,e.class]),style:t.normalizeStyle(e.style)},{default:()=>[l.default?.({prev:o,next:n})]})),{next:n,prev:o}}}),Op=vt({app:Boolean,appear:Boolean,extended:Boolean,layout:Boolean,offset:Boolean,modelValue:{type:Boolean,default:!0},...I(Fn({active:!0}),["location","spaced"]),...Qt(),...nn(),...fl({transition:"fab-transition"})},"VFab"),jp=wt()({name:"VFab",props:Op(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=la(e,"modelValue"),o=t.shallowRef(56),r=t.ref(),{resizeRef:i}=Kt(e=>{e.length&&(o.value=e[0].target.clientHeight)}),s=t.toRef(()=>e.app||e.absolute),u=t.computed(()=>!!s.value&&(e.location?.split(" ").shift()??"bottom")),c=t.computed(()=>!!s.value&&(e.location?.split(" ")[1]??"end"))
aa(()=>e.app,()=>{const a=ea({id:e.name,order:t.computed(()=>parseInt(e.order,10)),position:u,layoutSize:t.computed(()=>e.layout?o.value+24:0),elementSize:t.computed(()=>o.value+24),active:t.computed(()=>e.app&&n.value),absolute:t.toRef(()=>e.absolute)})
t.watchEffect(()=>{r.value=a.layoutItemStyles.value})})
const d=t.ref()
return Bt(()=>{const a=$n.filterProps(e)
return t.createElementVNode("div",{ref:d,class:t.normalizeClass(["v-fab",{"v-fab--absolute":e.absolute,"v-fab--app":!!e.app,"v-fab--extended":e.extended,"v-fab--offset":e.offset,[`v-fab--${u.value}`]:s.value,[`v-fab--${c.value}`]:s.value},e.class]),style:t.normalizeStyle([e.app?{...r.value}:{height:e.absolute?"100%":"inherit"},e.style])},[t.createElementVNode("div",{class:"v-fab__container"},[t.createVNode(gl,{appear:e.appear,transition:e.transition},{default:()=>[t.withDirectives(t.createVNode($n,t.mergeProps({ref:i},a,{active:void 0,location:void 0}),l),[[t.vShow,e.active]])]})])])}),{}}})
function Hp(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:""
return new Promise((a,l)=>{if(e.isFile){e.file(e=>a([{file:e,path:t}]),l)}else if(e.isDirectory){e.createReader().readEntries(async e=>{const l=[]
for(const a of e)l.push(...await Hp(a,Wp(t,a)))
a(l)})}})}function Wp(e,t){return t.isDirectory?`${e}/${t.name}`:e}const Yp=vt({filterByType:String},"file-accept")
const Up=vt({chips:Boolean,counter:Boolean,counterSizeString:{type:String,default:"$vuetify.fileInput.counterSize"},counterString:{type:String,default:"$vuetify.fileInput.counter"},hideInput:Boolean,multiple:Boolean,showSize:{type:[Boolean,Number,String],default:!1,validator:e=>"boolean"==typeof e||[1e3,1024].includes(Number(e))},truncateLength:{type:[Number,String],default:22},...I(ho({prependIcon:"$file"}),["direction"]),modelValue:{type:[Array,Object],default:e=>e.multiple?[]:null,validator:e=>B(e).every(e=>null!=e&&"object"==typeof e)},...Yp(),...Fi({clearable:!0})},"VFileInput"),Gp=wt()({name:"VFileInput",inheritAttrs:!1,props:Up(),emits:{"click:control":e=>!0,"mousedown:control":e=>!0,"update:focused":e=>!0,"update:modelValue":e=>!0,rejected:e=>!0},setup(e,a){let{attrs:l,emit:n,slots:o}=a
const{t:r}=ma(),{filterAccepted:i}=function(e){const a=t.computed(()=>e.filterByType?function(e){const t=e.split(",").map(e=>e.trim().toLowerCase()),a=t.filter(e=>e.startsWith(".")),l=t.filter(e=>e.endsWith("/*")),n=t.filter(e=>!a.includes(e)&&!l.includes(e))
return e=>{const t=e.name.split(".").at(-1)?.toLowerCase()??"",o=e.type.split("/").at(0)?.toLowerCase()??""
return n.includes(e.type)||a.includes(`.${t}`)||l.includes(`${o}/*`)}}(e.filterByType):null)
return{filterAccepted:function(e){if(a.value){const t=e.filter(a.value)
return{accepted:t,rejected:e.filter(e=>!t.includes(e))}}return{accepted:e,rejected:[]}}}}(e),s=la(e,"modelValue",e.modelValue,e=>B(e),t=>!e.multiple&&Array.isArray(t)?t[0]:t),{isFocused:u,focus:c,blur:d}=uo(e),v=t.computed(()=>"boolean"!=typeof e.showSize?e.showSize:void 0),p=t.computed(()=>(s.value??[]).reduce((e,t)=>{let{size:a=0}=t
return e+a},0)),m=t.computed(()=>L(p.value,v.value)),f=t.computed(()=>(s.value??[]).map(t=>{const{name:a="",size:l=0}=t,n=function(t){if(t.length<Number(e.truncateLength))return t
const a=Math.floor((Number(e.truncateLength)-1)/2)
return`${t.slice(0,a)}…${t.slice(t.length-a)}`}(a)
return e.showSize?`${n} (${L(l,v.value)})`:n})),g=t.computed(()=>{const t=s.value?.length??0
return e.showSize?r(e.counterSizeString,t,m.value):r(e.counterString,t)}),h=t.ref(),y=t.ref(),b=t.ref(),V=t.toRef(()=>u.value||e.active),w=t.computed(()=>["plain","underlined"].includes(e.variant)),k=t.shallowRef(!1),{handleDrop:S,hasFilesOrFolders:x}={handleDrop:async function(e){const t=[],a=[...e.dataTransfer?.items??[]].filter(e=>"file"===e.kind).map(e=>e.webkitGetAsEntry()).filter(Boolean)
if(a.length)for(const e of a){const a=await Hp(e,Wp(".",e))
t.push(...a.map(e=>e.file))}else t.push(...e.dataTransfer?.files??[])
return t},hasFilesOrFolders:function(e){return[...e.dataTransfer?.items??[]].filter(e=>"file"===e.kind).map(e=>e.webkitGetAsEntry()).filter(Boolean).length>0||[...e.dataTransfer?.files??[]].length>0}}
function N(){b.value!==document.activeElement&&b.value?.focus(),u.value||c()}function C(e){b.value?.click()}function E(e){n("mousedown:control",e)}function I(e){b.value?.click(),n("click:control",e)}function _(a){a.stopPropagation(),N(),t.nextTick(()=>{s.value=[],J(e["onClick:clear"],a)})}function P(e){e.preventDefault(),e.stopImmediatePropagation(),k.value=!0}function A(e){e.preventDefault(),k.value=!1}async function R(e){if(e.preventDefault(),e.stopImmediatePropagation(),k.value=!1,!b.value||!x(e))return
F(await S(e))}function D(t){if(t.target&&!t.repack)if(e.filterByType)F([...t.target.files])
else{const e=t.target
s.value=[...e.files??[]]}}function F(e){const t=new DataTransfer,{accepted:a,rejected:l}=i(e)
l.length&&n("rejected",l)
for(const e of a)t.items.add(e)
b.value.files=t.files,s.value=[...t.files]
const o=new Event("change",{bubbles:!0})
o.repack=!0,b.value.dispatchEvent(o)}return t.watch(s,e=>{(!Array.isArray(e)||!e.length)&&b.value&&(b.value.value="")}),Bt(()=>{const a=!(!o.counter&&!e.counter),n=!(!a&&!o.details),[r,i]=T(l),{modelValue:c,...v}=yo.filterProps(e),S={...$i.filterProps(e),"onClick:clear":_},x=void 0!==l.webkitdirectory&&!1!==l.webkitdirectory,B=l.accept?String(l.accept):void 0,F=x?void 0:e.filterByType??B
return t.createVNode(yo,t.mergeProps({ref:h,modelValue:e.multiple?s.value:s.value[0],class:["v-file-input",{"v-file-input--chips":!!e.chips,"v-file-input--dragging":k.value,"v-file-input--hide":e.hideInput,"v-input--plain-underlined":w.value},e.class],style:e.style,"onClick:prepend":C},r,v,{centerAffix:!w.value,focused:u.value}),{...o,default:a=>{let{id:l,isDisabled:n,isDirty:r,isReadonly:c,isValid:v,hasDetails:g}=a
return t.createVNode($i,t.mergeProps({ref:y,prependIcon:e.prependIcon,onMousedown:E,onClick:I,"onClick:prependInner":e["onClick:prependInner"],"onClick:appendInner":e["onClick:appendInner"]},S,{id:l.value,active:V.value||r.value,dirty:r.value||e.dirty,disabled:n.value,focused:u.value,details:g.value,error:!1===v.value,onDragover:P,onDrop:R}),{...o,default:a=>{let{props:{class:l,...r},controlRef:u}=a
return t.createElementVNode(t.Fragment,null,[t.createElementVNode("input",t.mergeProps({ref:e=>b.value=u.value=e,type:"file",accept:F,readonly:c.value,disabled:n.value,multiple:e.multiple,name:e.name,onClick:e=>{e.stopPropagation(),c.value&&e.preventDefault(),N()},onChange:D,onDragleave:A,onFocus:N,onBlur:d},r,i),null),t.createElementVNode("div",{class:t.normalizeClass(l)},[!!s.value?.length&&!e.hideInput&&(o.selection?o.selection({fileNames:f.value,totalBytes:p.value,totalBytesReadable:m.value}):e.chips?f.value.map(e=>t.createVNode(Xo,{key:e,size:"small",text:e},null)):f.value.join(", "))])])}})},details:n?l=>t.createElementVNode(t.Fragment,null,[o.details?.(l),a&&t.createElementVNode(t.Fragment,null,[t.createElementVNode("span",null,null),t.createVNode(Ri,{active:!!s.value?.length,value:g.value,disabled:e.disabled},o.counter)])]):void 0})}),wo({},h,y,b)}}),Kp=vt({app:Boolean,color:String,height:{type:[Number,String],default:"auto"},...wl(),...pt(),...Sl(),...Qt(),...pl(),...Pa({tag:"footer"}),...ya()},"VFooter"),qp=wt()({name:"VFooter",props:Kp(),setup(e,a){let{slots:l}=a
const n=t.ref(),{themeClasses:o}=Ca(e),{backgroundColorClasses:r,backgroundColorStyles:i}=dl(()=>e.color),{borderClasses:s}=kl(e),{elevationClasses:u}=xl(e),{roundedClasses:c}=ml(e),d=t.shallowRef(32),{resizeRef:v}=Kt(e=>{e.length&&(d.value=e[0].target.clientHeight)}),p=t.computed(()=>"auto"===e.height?d.value:parseInt(e.height,10))
return aa(()=>e.app,()=>{const a=ea({id:e.name,order:t.computed(()=>parseInt(e.order,10)),position:t.toRef(()=>"bottom"),layoutSize:p,elementSize:t.computed(()=>"auto"===e.height?void 0:p.value),active:t.toRef(()=>e.app),absolute:t.toRef(()=>e.absolute)})
t.watchEffect(()=>{n.value=a.layoutItemStyles.value})}),Bt(()=>t.createVNode(e.tag,{ref:v,class:t.normalizeClass(["v-footer",o.value,r.value,s.value,u.value,c.value,e.class]),style:t.normalizeStyle([i.value,e.app?n.value:{height:b(e.height)},e.style])},l)),{}}}),Xp=vt({...pt(),...vo()},"VForm"),Zp=wt()({name:"VForm",props:Xp(),emits:{"update:modelValue":e=>!0,submit:e=>!0},setup(e,l){let{slots:n,emit:o}=l
const r=function(e){const l=la(e,"modelValue"),n=t.toRef(()=>e.disabled),o=t.toRef(()=>e.readonly),r=t.shallowRef(!1),i=t.ref([]),s=t.ref([])
return t.watch(i,()=>{let e=0,t=0
const a=[]
for(const l of i.value)!1===l.isValid?(t++,a.push({id:l.id,errorMessages:l.errorMessages})):!0===l.isValid&&e++
s.value=a,l.value=!(t>0)&&(e===i.value.length||null)},{deep:!0,flush:"post"}),t.provide(co,{register:e=>{let{id:l,vm:n,validate:o,reset:r,resetValidation:s}=e
i.value.some(e=>e.id===l)&&a(`Duplicate input name "${l}"`),i.value.push({id:l,validate:o,reset:r,resetValidation:s,vm:t.markRaw(n),isValid:null,errorMessages:[]})},unregister:e=>{i.value=i.value.filter(t=>t.id!==e)},update:(e,t,a)=>{const l=i.value.find(t=>t.id===e)
l&&(l.isValid=t,l.errorMessages=a)},isDisabled:n,isReadonly:o,isValidating:r,isValid:l,items:i,validateOn:t.toRef(()=>e.validateOn)}),{errors:s,isDisabled:n,isReadonly:o,isValidating:r,isValid:l,items:i,validate:async function(){const t=[]
let a=!0
s.value=[],r.value=!0
for(const l of i.value){const n=await l.validate()
if(n.length>0&&(a=!1,t.push({id:l.id,errorMessages:n})),!a&&e.fastFail)break}return s.value=t,r.value=!1,{valid:a,errors:s.value}},reset:function(){i.value.forEach(e=>e.reset())},resetValidation:function(){i.value.forEach(e=>e.resetValidation())}}}(e),i=t.ref()
function s(e){e.preventDefault(),r.reset()}function u(e){const t=e,a=r.validate()
t.then=a.then.bind(a),t.catch=a.catch.bind(a),t.finally=a.finally.bind(a),o("submit",t),t.defaultPrevented||a.then(e=>{let{valid:t}=e
t&&i.value?.submit()}),t.preventDefault()}return Bt(()=>t.createElementVNode("form",{ref:i,class:t.normalizeClass(["v-form",e.class]),style:t.normalizeStyle(e.style),novalidate:!0,onReset:s,onSubmit:u},[n.default?.(r)])),wo(r,i)}}),Qp=vt({color:String,...wl(),...pt(),...pl(),...Pa({tag:"kbd"}),...ya(),...Sl()},"VKbd"),Jp=wt()({name:"VKbd",props:Qp(),setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ca(e),{borderClasses:o}=kl(e),{roundedClasses:r}=ml(e),{backgroundColorClasses:i,backgroundColorStyles:s}=dl(()=>e.color),{elevationClasses:u}=xl(e)
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-kbd",n.value,i.value,o.value,u.value,r.value,e.class]),style:t.normalizeStyle([s.value,e.style])},l)),{}}})
function em(e,t,a){const l=a&&e.mac?e.mac:e.default,n="icon"===t&&!l.icon||"symbol"===t&&!l.symbol?"text":t
let o=l[n]??l.text
return"text"===n&&"string"==typeof o&&o.startsWith("$")&&!o.startsWith("$vuetify.")&&(o=o.slice(1).toUpperCase()),"icon"===n?["icon",o]:[n,o]}const tm={ctrl:{mac:{symbol:"⌃",icon:"$ctrl",text:"$vuetify.hotkey.ctrl"},default:{text:"Ctrl"}},meta:{mac:{symbol:"⌘",icon:"$command",text:"$vuetify.hotkey.command"},default:{text:"Ctrl"}},cmd:{mac:{symbol:"⌘",icon:"$command",text:"$vuetify.hotkey.command"},default:{text:"Ctrl"}},shift:{mac:{symbol:"⇧",icon:"$shift",text:"$vuetify.hotkey.shift"},default:{text:"Shift"}},alt:{mac:{symbol:"⌥",icon:"$alt",text:"$vuetify.hotkey.option"},default:{text:"Alt"}},enter:{default:{symbol:"↵",icon:"$enter",text:"$vuetify.hotkey.enter"}},arrowup:{default:{symbol:"↑",icon:"$arrowup",text:"$vuetify.hotkey.upArrow"}},arrowdown:{default:{symbol:"↓",icon:"$arrowdown",text:"$vuetify.hotkey.downArrow"}},arrowleft:{default:{symbol:"←",icon:"$arrowleft",text:"$vuetify.hotkey.leftArrow"}},arrowright:{default:{symbol:"→",icon:"$arrowright",text:"$vuetify.hotkey.rightArrow"}},backspace:{default:{symbol:"⌫",icon:"$backspace",text:"$vuetify.hotkey.backspace"}},escape:{default:{text:"$vuetify.hotkey.escape"}}," ":{mac:{symbol:"␣",icon:"$space",text:"$vuetify.hotkey.space"},default:{text:"$vuetify.hotkey.space"}},"-":{default:{text:"-"}}},am=vt({keys:String,displayMode:{type:String,default:"icon"},keyMap:{type:Object,default:()=>tm},platform:{type:String,default:"auto"},inline:Boolean,disabled:Boolean,prefix:String,suffix:String,variant:{type:String,default:"elevated",validator:e=>["elevated","flat","tonal","outlined","text","plain","contained"].includes(e)},...pt(),...ya(),...wl(),...pl(),...Sl(),color:String},"VHotkey"),lm=Symbol("VHotkey:AND_DELINEATOR"),nm=Symbol("VHotkey:SLASH_DELINEATOR"),om=Symbol("VHotkey:THEN_DELINEATOR")
function rm(e,t,a,l){const n=a.toLowerCase()
if(n in e){const o=em(e[n],t,l)
return"text"===o[0]&&"string"==typeof o[1]&&o[1].startsWith("$")&&!o[1].startsWith("$vuetify.")?["text",o[1].replace("$","").toUpperCase(),a]:[...o,a]}return["text",a.toUpperCase(),a]}const im=wt()({name:"VHotkey",props:am(),setup(e){const{t:a}=ma(),{themeClasses:l}=Ca(e),{rtlClasses:n}=ga(),{borderClasses:o}=kl(e),{roundedClasses:r}=ml(e),{elevationClasses:i}=xl(e),{colorClasses:s,colorStyles:u,variantClasses:c}=Ml(()=>({color:e.color,variant:"contained"===e.variant?"elevated":e.variant})),d=t.computed(()=>"auto"===e.platform?"undefined"!=typeof navigator&&/macintosh/i.test(navigator.userAgent):"mac"===e.platform),v=t.computed(()=>e.keys?e.keys.split(" ").map(t=>{const a=[],l=Ou(t)
for(let t=0;t<l.length;t++){const n=l[t]
t>0&&a.push(om)
const{keys:o,separators:r}=Lu(n)
for(let t=0;t<o.length;t++){const l=o[t]
t>0&&a.push("/"===r[t-1]?nm:lm),a.push(rm(e.keyMap,e.displayMode,l,d.value))}}return a}):[]),p=t.computed(()=>{if(!e.keys)return""
const t=v.value.map(t=>{const l=[]
for(const n of t)if(Array.isArray(n)){const t="icon"===n[0]||"symbol"===n[0]?rm(O(tm,e.keyMap),"text",String(n[1]),d.value)[1]:n[1]
l.push(m(t))}else n===lm?l.push(a("$vuetify.hotkey.plus")):n===nm?l.push(a("$vuetify.hotkey.or")):n===om&&l.push(a("$vuetify.hotkey.then"))
return l.join(" ")}).join(", ")
return a("$vuetify.hotkey.shortcut",t)})
function m(e){return e.startsWith("$vuetify.")?a(e):e}function f(t){if("text"===e.displayMode)return
const a=function(e,t,a){const l=t.toLowerCase()
if(l in e){const t=em(e[l],"text",a)
return"string"==typeof t[1]?t[1]:String(t[1])}return t.toUpperCase()}(e.keyMap,String(t[2]),d.value)
return m(a)}Bt(()=>{const d=t.createElementVNode(t.Fragment,null,[e.prefix&&t.createElementVNode("span",{key:"prefix",class:"v-hotkey__prefix"},[e.prefix]),v.value.map((l,n)=>t.createElementVNode("span",{class:"v-hotkey__combination",key:n},[l.map((l,n)=>Array.isArray(l)?function(a,l){const n="contained"===e.variant,c=n?"kbd":Jp,d=["v-hotkey__key",`v-hotkey__key-${a[0]}`,...n?["v-hotkey__key--nested"]:[o.value,r.value,i.value,s.value]]
return t.createVNode(c,{key:l,class:t.normalizeClass(d),style:t.normalizeStyle(n?void 0:u.value),"aria-hidden":"true",title:f(a)},{default:()=>["icon"===a[0]?t.createVNode(Jl,{icon:a[1],"aria-hidden":"true"},null):m(a[1])]})}(l,n):function(e,l){return t.createElementVNode("span",{key:l,class:"v-hotkey__divider","aria-hidden":"true"},[e===lm?"+":e===nm?"/":a("$vuetify.hotkey.then")])}(l,n)),n<v.value.length-1&&t.createElementVNode("span",{"aria-hidden":"true"},[t.createTextVNode(" ")])])),e.suffix&&t.createElementVNode("span",{key:"suffix",class:"v-hotkey__suffix"},[e.suffix])])
return t.createElementVNode("div",{class:t.normalizeClass(["v-hotkey",{"v-hotkey--disabled":e.disabled,"v-hotkey--inline":e.inline,"v-hotkey--contained":"contained"===e.variant},l.value,n.value,c.value,e.class]),style:t.normalizeStyle(e.style),role:"img","aria-label":p.value},["contained"!==e.variant?d:t.createVNode(Jp,{key:"contained",class:t.normalizeClass(["v-hotkey__contained-wrapper",o.value,r.value,i.value,s.value]),style:t.normalizeStyle(u.value),"aria-hidden":"true"},{default:()=>[d]})])})}}),sm=vt({disabled:Boolean,modelValue:{type:Boolean,default:null},...oi()},"VHover"),um=wt()({name:"VHover",props:sm(),emits:{"update:modelValue":e=>!0},setup(e,t){let{slots:a}=t
const l=la(e,"modelValue"),{runOpenDelay:n,runCloseDelay:o}=ri(e,t=>!e.disabled&&(l.value=t))
return()=>a.default?.({isHovering:l.value,props:{onMouseenter:n,onMouseleave:o}})}}),cm=vt({color:String,direction:{type:String,default:"vertical",validator:e=>["vertical","horizontal"].includes(e)},side:{type:String,default:"end",validator:e=>["start","end","both"].includes(e)},mode:{type:String,default:"intersect",validator:e=>["intersect","manual"].includes(e)},margin:[Number,String],loadMoreText:{type:String,default:"$vuetify.infiniteScroll.loadMore"},emptyText:{type:String,default:"$vuetify.infiniteScroll.empty"},...ol(),...Pa()},"VInfiniteScroll"),dm=Vt({name:"VInfiniteScrollIntersect",props:{side:{type:String,required:!0},rootMargin:String},emits:{intersect:(e,t)=>!0},setup(e,a){let{emit:l}=a
const{intersectionRef:n,isIntersecting:o}=en()
return t.watch(o,async t=>{l("intersect",e.side,t)}),Bt(()=>t.createElementVNode("div",{class:"v-infinite-scroll-intersect",style:{"--v-infinite-margin-size":e.rootMargin},ref:n},[t.createTextVNode(" ")])),{}}}),vm=wt()({name:"VInfiniteScroll",props:cm(),emits:{load:e=>!0},setup(e,a){let{slots:l,emit:n}=a
const o=t.ref(),r=t.shallowRef("ok"),i=t.shallowRef("ok"),s=t.computed(()=>b(e.margin)),u=t.shallowRef(!1)
function c(t){if(!o.value)return
const a="vertical"===e.direction?"scrollTop":"scrollLeft"
o.value[a]=t}function d(){if(!o.value)return 0
const t="vertical"===e.direction?"scrollTop":"scrollLeft"
return o.value[t]}function v(){if(!o.value)return 0
const t="vertical"===e.direction?"scrollHeight":"scrollWidth"
return o.value[t]}function p(e,t){"start"===e?r.value=t:"end"===e?i.value=t:"both"===e&&(r.value=t,i.value=t)}t.onMounted(()=>{o.value&&("start"===e.side?c(v()):"both"===e.side&&c(v()/2-function(){if(!o.value)return 0
const t="vertical"===e.direction?"clientHeight":"clientWidth"
return o.value[t]}()/2))})
let m=0
function f(e,t){u.value=t,u.value&&g(e)}function g(a){if("manual"!==e.mode&&!u.value)return
const l=function(e){return"start"===e?r.value:i.value}(a)
o.value&&!["empty","loading"].includes(l)&&(m=v(),p(a,"loading"),n("load",{side:a,done:function(l){p(a,l),t.nextTick(()=>{"empty"!==l&&"error"!==l&&("ok"===l&&"start"===a&&c(v()-m+d()),"manual"!==e.mode&&t.nextTick(()=>{window.requestAnimationFrame(()=>{window.requestAnimationFrame(()=>{window.requestAnimationFrame(()=>{g(a)})})})}))})}}))}const{t:h}=ma()
function y(a,n){if(e.side!==a&&"both"!==e.side)return
const o=()=>g(a),r={side:a,props:{onClick:o,color:e.color}}
return"error"===n?l.error?.(r):"empty"===n?l.empty?.(r)??t.createElementVNode("div",null,[h(e.emptyText)]):"manual"===e.mode?"loading"===n?l.loading?.(r)??t.createVNode(an,{indeterminate:!0,color:e.color},null):l["load-more"]?.(r)??t.createVNode($n,{variant:"outlined",color:e.color,onClick:o},{default:()=>[h(e.loadMoreText)]}):l.loading?.(r)??t.createVNode(an,{indeterminate:!0,color:e.color},null)}const{dimensionStyles:V}=rl(e)
return Bt(()=>{const a=e.tag,n="start"===e.side||"both"===e.side,u="end"===e.side||"both"===e.side,c="intersect"===e.mode
return t.createVNode(a,{ref:o,class:t.normalizeClass(["v-infinite-scroll",`v-infinite-scroll--${e.direction}`,{"v-infinite-scroll--start":n,"v-infinite-scroll--end":u}]),style:t.normalizeStyle(V.value)},{default:()=>[t.createElementVNode("div",{class:"v-infinite-scroll__side"},[y("start",r.value)]),n&&c&&t.createVNode(dm,{key:"start",side:"start",onIntersect:f,rootMargin:s.value},null),l.default?.(),u&&c&&t.createVNode(dm,{key:"end",side:"end",onIntersect:f,rootMargin:s.value},null),t.createElementVNode("div",{class:"v-infinite-scroll__side"},[y("end",i.value)])]})}),{reset:function(a){const l=a??e.side
p(l,"ok"),t.nextTick(()=>{"end"!==l&&c(v()-m+d()),"manual"!==e.mode&&t.nextTick(()=>{window.requestAnimationFrame(()=>{window.requestAnimationFrame(()=>{window.requestAnimationFrame(()=>{"both"===l?(g("start"),g("end")):g(l)})})})})})}}}}),pm=Symbol.for("vuetify:v-item-group"),mm=vt({...pt(),...Ol({selectedClass:"v-item--selected"}),...Pa(),...ya()},"VItemGroup"),fm=wt()({name:"VItemGroup",props:mm(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ca(e),{isSelected:o,select:r,next:i,prev:s,selected:u}=Wl(e,pm)
return()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-item-group",n.value,e.class]),style:t.normalizeStyle(e.style)},{default:()=>[l.default?.({isSelected:o,select:r,next:i,prev:s,selected:u.value})]})}}),gm=wt()({name:"VItem",props:jl(),emits:{"group:selected":e=>!0},setup(e,t){let{slots:a}=t
const{isSelected:l,select:n,toggle:o,selectedClass:r,value:i,disabled:s}=Hl(e,pm)
return()=>a.default?.({isSelected:l.value,selectedClass:r.value,select:n,toggle:o,value:i.value,disabled:s.value})}}),hm=vt({...pt(),...ol(),...Zt()},"VLayout"),ym=wt()({name:"VLayout",props:hm(),setup(e,a){let{slots:l}=a
const{layoutClasses:n,layoutStyles:o,getLayoutItem:r,items:i,layoutRef:s}=ta(e),{dimensionStyles:u}=rl(e)
return Bt(()=>t.createElementVNode("div",{ref:s,class:t.normalizeClass([n.value,e.class]),style:t.normalizeStyle([u.value,o.value,e.style])},[l.default?.()])),{getLayoutItem:r,items:i}}}),bm=vt({position:{type:String,required:!0},size:{type:[Number,String],default:300},modelValue:Boolean,...pt(),...Qt()},"VLayoutItem"),Vm=wt()({name:"VLayoutItem",props:bm(),setup(e,a){let{slots:l}=a
const{layoutItemStyles:n}=ea({id:e.name,order:t.computed(()=>parseInt(e.order,10)),position:t.toRef(()=>e.position),elementSize:t.toRef(()=>e.size),layoutSize:t.toRef(()=>e.size),active:t.toRef(()=>e.modelValue),absolute:t.toRef(()=>e.absolute)})
return()=>t.createElementVNode("div",{class:t.normalizeClass(["v-layout-item",e.class]),style:t.normalizeStyle([n.value,e.style])},[l.default?.()])}}),wm=vt({modelValue:Boolean,options:{type:Object,default:()=>({root:void 0,rootMargin:void 0,threshold:void 0})},...pt(),...ol(),...Pa(),...fl({transition:"fade-transition"})},"VLazy"),km=wt()({name:"VLazy",directives:{vIntersect:yl},props:wm(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const{dimensionStyles:n}=rl(e),o=la(e,"modelValue")
function r(e){o.value||(o.value=e)}return Bt(()=>t.withDirectives(t.createVNode(e.tag,{class:t.normalizeClass(["v-lazy",e.class]),style:t.normalizeStyle([n.value,e.style])},{default:()=>[o.value&&t.createVNode(gl,{transition:e.transition,appear:!0},{default:()=>[l.default?.()]})]}),[[yl,{handler:r,options:e.options},null]])),{}}}),Sm=vt({locale:String,fallbackLocale:String,messages:Object,rtl:{type:Boolean,default:void 0},...pt()},"VLocaleProvider"),xm=wt()({name:"VLocaleProvider",props:Sm(),setup(e,a){let{slots:l}=a
const{rtlClasses:n}=fa(e)
return Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-locale-provider",n.value,e.class]),style:t.normalizeStyle(e.style)},[l.default?.()])),{}}}),Nm=vt({scrollable:Boolean,...pt(),...ol(),...Pa({tag:"main"})},"VMain"),Cm=wt()({name:"VMain",props:Nm(),setup(e,a){let{slots:l}=a
const{dimensionStyles:n}=rl(e),{mainStyles:o}=Jt(),{ssrBootStyles:r}=_l()
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-main",{"v-main--scrollable":e.scrollable},e.class]),style:t.normalizeStyle([o.value,r.value,n.value,e.style])},{default:()=>[e.scrollable?t.createElementVNode("div",{class:"v-main__scroller"},[l.default?.()]):l.default?.()]})),{}}})
function Em(e){return(e<0?-1:1)*Math.sqrt(Math.abs(e))*1.41421356237}function Im(e){if(e.length<2)return 0
if(2===e.length)return e[1].t===e[0].t?0:(e[1].d-e[0].d)/(e[1].t-e[0].t)
let t=0
for(let a=e.length-1;a>0;a--){if(e[a].t===e[a-1].t)continue
const l=Em(t),n=(e[a].d-e[a-1].d)/(e[a].t-e[a-1].t)
t+=(n-l)*Math.abs(n),a===e.length-1&&(t*=.5)}return 1e3*Em(t)}function _m(){const e={}
return{addMovement:function(t){Array.from(t.changedTouches).forEach(a=>{(e[a.identifier]??(e[a.identifier]=new G(20))).push([t.timeStamp,a])})},endTouch:function(t){Array.from(t.changedTouches).forEach(t=>{delete e[t.identifier]})},getVelocity:function(t){const a=e[t]?.values().reverse()
if(!a)throw new Error(`No samples for touch id ${t}`)
const l=a[0],n=[],o=[]
for(const e of a){if(l[0]-e[0]>100)break
n.push({t:e[0],d:e[1].clientX}),o.push({t:e[0],d:e[1].clientY})}return{x:Im(n),y:Im(o),get direction(){const{x:e,y:t}=this,[a,l]=[Math.abs(e),Math.abs(t)]
return a>l&&e>=0?"right":a>l&&e<=0?"left":l>a&&t>=0?"down":l>a&&t<=0?"up":function(){throw new Error}()}}}}}function Pm(){throw new Error}const Am=["start","end","left","right","top","bottom"],Rm=vt({color:String,disableResizeWatcher:Boolean,disableRouteWatcher:Boolean,expandOnHover:Boolean,floating:Boolean,modelValue:{type:Boolean,default:null},permanent:Boolean,rail:{type:Boolean,default:null},railWidth:{type:[Number,String],default:56},scrim:{type:[Boolean,String],default:!0},image:String,temporary:Boolean,persistent:Boolean,touchless:Boolean,width:{type:[Number,String],default:256},location:{type:String,default:"start",validator:e=>Am.includes(e)},sticky:Boolean,...wl(),...pt(),...oi(),...Ao({mobile:null}),...Sl(),...Qt(),...pl(),...I(ci(),["disableInitialFocus"]),...Pa({tag:"nav"}),...ya()},"VNavigationDrawer"),Tm=wt()({name:"VNavigationDrawer",props:Rm(),emits:{"update:modelValue":e=>!0,"update:rail":e=>!0},setup(e,a){let{attrs:l,emit:n,slots:o}=a
const{isRtl:r}=ga(),{themeClasses:i}=Ca(e),{borderClasses:s}=kl(e),{backgroundColorClasses:u,backgroundColorStyles:c}=dl(()=>e.color),{elevationClasses:d}=xl(e),{displayClasses:v,mobile:p}=Ro(e),{roundedClasses:m}=ml(e),f=gn(),g=la(e,"modelValue",null,e=>!!e),{ssrBootStyles:h}=_l(),{scopeId:y}=yi(),V=t.ref(),w=t.shallowRef(!1),{runOpenDelay:k,runCloseDelay:S}=ri(e,e=>{w.value=e}),x=t.computed(()=>e.rail&&e.expandOnHover&&w.value?Number(e.width):Number(e.rail?e.railWidth:e.width)),N=t.computed(()=>ge(e.location,r.value)),C=t.toRef(()=>e.persistent),E=t.computed(()=>!e.permanent&&(p.value||e.temporary)),I=t.computed(()=>e.sticky&&!E.value&&"bottom"!==N.value)
mi(e,{isActive:g,localTop:E,contentEl:V}),aa(()=>e.expandOnHover&&null!=e.rail,()=>{t.watch(w,e=>n("update:rail",!e))}),aa(()=>!e.disableResizeWatcher,()=>{t.watch(E,a=>!e.permanent&&t.nextTick(()=>g.value=!a))}),aa(()=>!e.disableRouteWatcher&&!!f,()=>{t.watch(f.currentRoute,()=>E.value&&(g.value=!1))}),t.watch(()=>e.permanent,e=>{e&&(g.value=!0)}),null!=e.modelValue||E.value||(g.value=e.permanent||!p.value)
const{isDragging:_,dragProgress:P}=function(e){let{el:a,isActive:l,isTemporary:n,width:o,touchless:r,position:i}=e
t.onMounted(()=>{window.addEventListener("touchstart",b,{passive:!0}),window.addEventListener("touchmove",V,{passive:!1}),window.addEventListener("touchend",w,{passive:!0})}),t.onBeforeUnmount(()=>{window.removeEventListener("touchstart",b),window.removeEventListener("touchmove",V),window.removeEventListener("touchend",w)})
const s=t.computed(()=>["left","right"].includes(i.value)),{addMovement:u,endTouch:c,getVelocity:d}=_m()
let v=!1
const p=t.shallowRef(!1),m=t.shallowRef(0),f=t.shallowRef(0)
let g
function h(e,t){return("left"===i.value?e:"right"===i.value?document.documentElement.clientWidth-e:"top"===i.value?e:"bottom"===i.value?document.documentElement.clientHeight-e:Pm())-(t?o.value:0)}function y(e){let t=!(arguments.length>1&&void 0!==arguments[1])||arguments[1]
const a="left"===i.value?(e-f.value)/o.value:"right"===i.value?(document.documentElement.clientWidth-e-f.value)/o.value:"top"===i.value?(e-f.value)/o.value:"bottom"===i.value?(document.documentElement.clientHeight-e-f.value)/o.value:Pm()
return t?F(a):a}function b(e){if(r.value)return
const t=e.changedTouches[0].clientX,a=e.changedTouches[0].clientY,d="left"===i.value?t<25:"right"===i.value?t>document.documentElement.clientWidth-25:"top"===i.value?a<25:"bottom"===i.value?a>document.documentElement.clientHeight-25:Pm(),p=l.value&&("left"===i.value?t<o.value:"right"===i.value?t>document.documentElement.clientWidth-o.value:"top"===i.value?a<o.value:"bottom"===i.value?a>document.documentElement.clientHeight-o.value:Pm());(d||p||l.value&&n.value)&&(g=[t,a],f.value=h(s.value?t:a,l.value),m.value=y(s.value?t:a),v=f.value>-20&&f.value<80,c(e),u(e))}function V(e){const t=e.changedTouches[0].clientX,a=e.changedTouches[0].clientY
if(v){if(!e.cancelable)return void(v=!1)
const l=Math.abs(t-g[0]),n=Math.abs(a-g[1]);(s.value?l>n&&l>3:n>l&&n>3)?(p.value=!0,v=!1):(s.value?n:l)>3&&(v=!1)}if(!p.value)return
e.preventDefault(),u(e)
const l=y(s.value?t:a,!1)
m.value=Math.max(0,Math.min(1,l)),l>1?f.value=h(s.value?t:a,!0):l<0&&(f.value=h(s.value?t:a,!1))}function w(e){if(v=!1,!p.value)return
u(e),p.value=!1
const t=d(e.changedTouches[0].identifier),a=Math.abs(t.x),n=Math.abs(t.y),o=s.value?a>n&&a>400:n>a&&n>3
l.value=o?t.direction===({left:"right",right:"left",top:"down",bottom:"up"}[i.value]||Pm()):m.value>.5}const k=t.computed(()=>p.value?{transform:"left"===i.value?`translateX(calc(-100% + ${m.value*o.value}px))`:"right"===i.value?`translateX(calc(100% - ${m.value*o.value}px))`:"top"===i.value?`translateY(calc(-100% + ${m.value*o.value}px))`:"bottom"===i.value?`translateY(calc(100% - ${m.value*o.value}px))`:Pm(),transition:"none"}:void 0)
return aa(p,()=>{const e=a.value?.style.transform??null,l=a.value?.style.transition??null
t.watchEffect(()=>{a.value?.style.setProperty("transform",k.value?.transform||"none"),a.value?.style.setProperty("transition",k.value?.transition||null)}),t.onScopeDispose(()=>{a.value?.style.setProperty("transform",e),a.value?.style.setProperty("transition",l)})}),{isDragging:p,dragProgress:m,dragStyles:k}}({el:V,isActive:g,isTemporary:E,width:x,touchless:t.toRef(()=>e.touchless),position:N}),A=t.computed(()=>{const t=E.value?0:e.rail&&e.expandOnHover?Number(e.railWidth):x.value
return _.value?t*P.value:t}),{layoutItemStyles:R,layoutItemScrimStyles:T}=ea({id:e.name,order:t.computed(()=>parseInt(e.order,10)),position:N,layoutSize:A,elementSize:x,active:t.readonly(g),disableTransitions:t.toRef(()=>_.value),absolute:t.computed(()=>e.absolute||I.value&&"string"!=typeof B.value)}),{isStuck:B,stickyStyles:D}=function(e){let{rootEl:a,isSticky:l,layoutItemStyles:n}=e
const o=t.shallowRef(!1),r=t.shallowRef(0),i=t.computed(()=>{const e="boolean"==typeof o.value?"top":o.value
return[l.value?{top:"auto",bottom:"auto",height:void 0}:void 0,o.value?{[e]:b(r.value)}:{top:n.value.top}]})
t.onMounted(()=>{t.watch(l,e=>{e?window.addEventListener("scroll",u,{passive:!0}):window.removeEventListener("scroll",u)},{immediate:!0})}),t.onBeforeUnmount(()=>{window.removeEventListener("scroll",u)})
let s=0
function u(){const e=s>window.scrollY?"up":"down",t=a.value.getBoundingClientRect(),l=parseFloat(n.value.top??0),i=window.scrollY-Math.max(0,r.value-l),u=t.height+Math.max(r.value,l)-window.scrollY-window.innerHeight,c=parseFloat(getComputedStyle(a.value).getPropertyValue("--v-body-scroll-y"))||0
t.height<window.innerHeight-l?(o.value="top",r.value=l):"up"===e&&"bottom"===o.value||"down"===e&&"top"===o.value?(r.value=window.scrollY+t.top-c,o.value=!0):"down"===e&&u<=0?(r.value=0,o.value="bottom"):"up"===e&&i<=0&&(c?"top"!==o.value&&(r.value=-i+c+l,o.value="top"):(r.value=t.top+i,o.value="top")),s=window.scrollY}return{isStuck:o,stickyStyles:i}}({rootEl:V,isSticky:I,layoutItemStyles:R}),$=dl(()=>"string"==typeof e.scrim?e.scrim:null),M=t.computed(()=>({..._.value?{opacity:.2*P.value,transition:"none"}:void 0,...T.value}))
return yt({VList:{bgColor:"transparent"}}),Bt(()=>{const a=o.image||e.image
return t.createElementVNode(t.Fragment,null,[t.createVNode(e.tag,t.mergeProps({ref:V,onMouseenter:k,onMouseleave:S,class:["v-navigation-drawer",`v-navigation-drawer--${N.value}`,{"v-navigation-drawer--expand-on-hover":e.expandOnHover,"v-navigation-drawer--floating":e.floating,"v-navigation-drawer--is-hovering":w.value,"v-navigation-drawer--rail":e.rail,"v-navigation-drawer--temporary":E.value,"v-navigation-drawer--persistent":C.value,"v-navigation-drawer--active":g.value,"v-navigation-drawer--sticky":I.value},i.value,u.value,s.value,v.value,d.value,m.value,e.class],style:[c.value,R.value,h.value,D.value,e.style],inert:!g.value},y,l),{default:()=>[a&&t.createElementVNode("div",{key:"image",class:"v-navigation-drawer__img"},[o.image?t.createVNode(nl,{key:"image-defaults",disabled:!e.image,defaults:{VImg:{alt:"",cover:!0,height:"inherit",src:e.image}}},o.image):t.createVNode(Vl,{key:"image-img",alt:"",cover:!0,height:"inherit",src:e.image},null)]),o.prepend&&t.createElementVNode("div",{class:"v-navigation-drawer__prepend"},[o.prepend?.()]),t.createElementVNode("div",{class:"v-navigation-drawer__content"},[o.default?.()]),o.append&&t.createElementVNode("div",{class:"v-navigation-drawer__append"},[o.append?.()])]}),t.createVNode(t.Transition,{name:"fade-transition"},{default:()=>[E.value&&(_.value||g.value)&&!!e.scrim&&t.createElementVNode("div",t.mergeProps({class:["v-navigation-drawer__scrim",$.backgroundColorClasses.value],style:[M.value,$.backgroundColorStyles.value],onClick:()=>{C.value||(g.value=!1)}},y),null)]})])}),{isStuck:B}}}),Bm=Vt({name:"VNoSsr",setup(e,t){let{slots:a}=t
const l=fi()
return()=>l.value&&a.default?.()}})
const Dm=vt({controlVariant:{type:String,default:"default"},inset:Boolean,hideInput:Boolean,modelValue:{type:Number,default:null},min:{type:Number,default:Number.MIN_SAFE_INTEGER},max:{type:Number,default:Number.MAX_SAFE_INTEGER},step:{type:Number,default:1},precision:{type:Number,default:0},minFractionDigits:{type:Number,default:null},decimalSeparator:{type:String,validator:e=>!e||1===e.length},...I(ji(),["modelValue","validationValue"])},"VNumberInput"),Fm=wt()({name:"VNumberInput",props:{...Dm()},emits:{"update:focused":e=>!0,"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=t.ref(),{holdStart:o,holdStop:r}=function(e){let{toggleUpDown:a}=e,l=-1,n=-1
function o(){window.clearTimeout(l),window.clearInterval(n),window.removeEventListener("pointerup",o),document.removeEventListener("blur",o)}function r(e){a("up"===e)}return t.onScopeDispose(o),t.onScopeDispose(o),{holdStart:function(e){o(),r(e),window.addEventListener("pointerup",o),document.addEventListener("blur",o),l=window.setTimeout(()=>{n=window.setInterval(()=>r(e),50)},500)},holdStop:o}}({toggleUpDown:I}),i=po(e),s=t.computed(()=>i.isDisabled.value||i.isReadonly.value),u=t.shallowRef(e.focused),{decimalSeparator:c}=ma(),d=t.computed(()=>e.decimalSeparator?.[0]||c.value)
function v(t){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:e.precision,l=!(arguments.length>2&&void 0!==arguments[2])||arguments[2]
const n=null==a?String(t):t.toFixed(a)
if(u.value&&l)return Number(n).toString().replace(".",d.value)
if(null===e.minFractionDigits||null!==a&&a<e.minFractionDigits)return n.replace(".",d.value)
let[o,r]=n.split(".")
return r=(r??"").padEnd(e.minFractionDigits,"0").replace(new RegExp(`(?<=\\d{${e.minFractionDigits}})0+$`,"g"),""),[o,r].filter(Boolean).join(d.value)}const p=la(e,"modelValue",null,e=>e??null,t=>null==t?t??null:F(Number(t),e.min,e.max)),m=t.shallowRef(null),f=t.shallowRef(null)
t.watch(p,e=>{u.value&&!s.value&&Number(m.value?.replace(d.value,"."))===e||(null==e?(m.value=null,f.value=null):isNaN(e)||(m.value=v(e),f.value=Number(m.value.replace(d.value,"."))))},{immediate:!0})
const g=t.computed({get:()=>m.value,set(t){if(null===t||""===t)return p.value=null,m.value=null,void(f.value=null)
const a=Number(t.replace(d.value,"."))
isNaN(a)||(m.value=t,f.value=a,a<=e.max&&a>=e.min&&(p.value=a))}}),h=t.computed(()=>{if(null===f.value)return!1
const t=Number(m.value?.replace(d.value,"."))
return t!==F(t,e.min,e.max)}),y=t.computed(()=>!s.value&&(p.value??0)+e.step<=e.max),b=t.computed(()=>!s.value&&(p.value??0)-e.step>=e.min),V=t.computed(()=>e.hideInput?"stacked":e.controlVariant),w=t.toRef(()=>"split"===V.value?"$plus":"$collapse"),k=t.toRef(()=>"split"===V.value?"$minus":"$expand"),S=t.toRef(()=>"split"===V.value?"default":"small"),x=t.toRef(()=>"stacked"===V.value?"auto":"100%"),N={props:{onClick:A,onPointerup:R,onPointerdown:T,onPointercancel:R}},C={props:{onClick:A,onPointerup:R,onPointerdown:B,onPointercancel:R}}
function E(e){if(null==e)return 0
const t=e.toString(),a=t.indexOf(".")
return~a?t.length-a:0}function I(){let t=!(arguments.length>0&&void 0!==arguments[0])||arguments[0]
if(s.value)return
if(null==p.value)return void(g.value=v(F(0,e.min,e.max)))
let a=Math.max(E(p.value),E(e.step))
null!=e.precision&&(a=Math.max(a,e.precision)),t?y.value&&(g.value=v(p.value+e.step,a)):b.value&&(g.value=v(p.value-e.step,a))}function _(a){if(!a.data)return
const l=a.target,{value:n,selectionStart:o,selectionEnd:r}=l??{},i=n?n.slice(0,o)+a.data+n.slice(r):a.data,s=function(e,t,a){const l=new RegExp(`[\\d\\-${de(a)}]`),n=e.split("").filter(e=>l.test(e)).filter((e,t,l)=>0===t&&/[-]/.test(e)||e===a&&t===l.indexOf(e)||/\d/.test(e)).join("")
if(0===t)return n.split(a)[0]
const o=new RegExp(`${de(a)}\\d`)
if(null!==t&&o.test(n)){const e=n.split(a)
return[e[0],e[1].substring(0,t)].join(a)}return n}(i,e.precision,d.value)
if(new RegExp(`^-?\\d*${de(d.value)}?\\d*$`).test(i)||(a.preventDefault(),l.value=s,t.nextTick(()=>g.value=s)),null!=e.precision){if(i.split(d.value)[1]?.length>e.precision){a.preventDefault(),l.value=s,t.nextTick(()=>g.value=s)
const e=(o??0)+a.data.length
l.setSelectionRange(e,e)}0===e.precision&&i.endsWith(d.value)&&(a.preventDefault(),l.value=s,t.nextTick(()=>g.value=s))}}async function P(e){["Enter","ArrowLeft","ArrowRight","Backspace","Delete","Tab"].includes(e.key)||e.ctrlKey||["ArrowDown","ArrowUp"].includes(e.key)&&(e.preventDefault(),e.stopPropagation(),D(),await t.nextTick(),"ArrowDown"===e.key?I(!1):I())}function A(e){e.stopPropagation()}function R(e){const t=e.currentTarget
t?.releasePointerCapture(e.pointerId),e.preventDefault(),r()}function T(e){const t=e.currentTarget
t?.setPointerCapture(e.pointerId),e.preventDefault(),e.stopPropagation(),o("up")}function B(e){const t=e.currentTarget
t?.setPointerCapture(e.pointerId),e.preventDefault(),e.stopPropagation(),o("down")}function D(){if(s.value)return
if(!n.value)return
const t=n.value.value,a=Number(t.replace(d.value,"."))
t&&!isNaN(a)?g.value=v(F(a,e.min,e.max)):g.value=null}function $(){s.value||(g.value=null===p.value||isNaN(p.value)?null:v(p.value,e.precision,!1))}function M(){s.value||(null===p.value||isNaN(p.value)?g.value=null:g.value=p.value.toString().replace(".",d.value))}function z(){D()}return t.watch(()=>e.precision,()=>$()),t.watch(()=>e.minFractionDigits,()=>$()),t.onMounted(()=>{D()}),Bt(()=>{const{modelValue:a,type:o,...r}=Hi.filterProps(e)
function i(){return l.increment?t.createVNode(nl,{key:"increment-defaults",defaults:{VBtn:{disabled:!y.value,height:x.value,size:S.value,icon:w.value,variant:"text"}}},{default:()=>[l.increment(N)]}):t.createVNode($n,{"aria-hidden":"true","data-testid":"increment",disabled:!y.value,height:x.value,icon:w.value,key:"increment-btn",onClick:A,onPointerdown:T,onPointerup:R,onPointercancel:R,size:S.value,variant:"text",tabindex:"-1"},null)}function s(){return l.decrement?t.createVNode(nl,{key:"decrement-defaults",defaults:{VBtn:{disabled:!b.value,height:x.value,size:S.value,icon:k.value,variant:"text"}}},{default:()=>[l.decrement(C)]}):t.createVNode($n,{"aria-hidden":"true","data-testid":"decrement",disabled:!b.value,height:x.value,icon:k.value,key:"decrement-btn",onClick:A,onPointerdown:B,onPointerup:R,onPointercancel:R,size:S.value,variant:"text",tabindex:"-1"},null)}function c(){return t.createElementVNode("div",{class:"v-number-input__control"},[s(),t.createVNode(Jo,{vertical:"stacked"!==V.value},null),i()])}function d(){return e.hideInput||e.inset?void 0:t.createVNode(Jo,{vertical:!0},null)}const v="split"===V.value?t.createElementVNode("div",{class:"v-number-input__control"},[t.createVNode(Jo,{vertical:!0},null),i()]):e.reverse||"hidden"===V.value?void 0:t.createElementVNode(t.Fragment,null,[d(),c()]),m=l["append-inner"]||v,f="split"===V.value?t.createElementVNode("div",{class:"v-number-input__control"},[s(),t.createVNode(Jo,{vertical:!0},null)]):e.reverse&&"hidden"!==V.value?t.createElementVNode(t.Fragment,null,[c(),d()]):void 0,E=l["prepend-inner"]||f
return t.createVNode(Hi,t.mergeProps({ref:n},r,{modelValue:g.value,"onUpdate:modelValue":e=>g.value=e,focused:u.value,"onUpdate:focused":e=>u.value=e,validationValue:p.value,error:e.error||h.value||void 0,onBeforeinput:_,onFocus:M,onBlur:z,onKeydown:P,class:["v-number-input",{"v-number-input--default":"default"===V.value,"v-number-input--hide-input":e.hideInput,"v-number-input--inset":e.inset,"v-number-input--reverse":e.reverse,"v-number-input--split":"split"===V.value,"v-number-input--stacked":"stacked"===V.value},e.class],style:e.style,inputmode:"decimal"}),{...l,"append-inner":m?function(){for(var e=arguments.length,a=new Array(e),n=0;n<e;n++)a[n]=arguments[n]
return t.createElementVNode(t.Fragment,null,[l["append-inner"]?.(...a),v])}:void 0,"prepend-inner":E?function(){for(var e=arguments.length,a=new Array(e),n=0;n<e;n++)a[n]=arguments[n]
return t.createElementVNode(t.Fragment,null,[f,l["prepend-inner"]?.(...a)])}:void 0})}),wo({},n)}}),$m=vt({autofocus:Boolean,divider:String,focusAll:Boolean,label:{type:String,default:"$vuetify.input.otp"},length:{type:[Number,String],default:6},modelValue:{type:[Number,String],default:void 0},placeholder:String,type:{type:String,default:"number"},...ol(),...so(),...C(Fi({variant:"outlined"}),["baseColor","bgColor","class","color","disabled","error","loading","rounded","style","theme","variant"])},"VOtpInput"),Mm=wt()({name:"VOtpInput",props:$m(),emits:{finish:e=>!0,"update:focused":e=>!0,"update:modelValue":e=>!0},setup(e,a){let{attrs:l,emit:n,slots:o}=a
const{dimensionStyles:r}=rl(e),{isFocused:i,focus:s,blur:u}=uo(e),c=la(e,"modelValue","",e=>null==e?[]:String(e).split(""),e=>e.join("")),{t:d}=ma(),v=t.computed(()=>Number(e.length)),p=t.computed(()=>Array(v.value).fill(0)),m=t.ref(-1),f=t.ref(),g=t.ref([]),h=t.computed(()=>g.value[m.value])
let y=!1
function b(){if(S(h.value.value))return void(h.value.value="")
if(y)return
const e=c.value.slice(),t=h.value.value
e[m.value]=t
let a=null
m.value>c.value.length?a=c.value.length+1:m.value+1!==v.value&&(a="next"),c.value=e,a&&ae(f.value,a)}function V(){y=!1,b()}function w(e){const t=c.value.slice(),a=m.value
let l=null;["ArrowLeft","ArrowRight","Backspace","Delete"].includes(e.key)&&(e.preventDefault(),"ArrowLeft"===e.key?l="prev":"ArrowRight"===e.key?l="next":["Backspace","Delete"].includes(e.key)&&(t[m.value]="",c.value=t,m.value>0&&"Backspace"===e.key?l="prev":requestAnimationFrame(()=>{g.value[a]?.select()})),requestAnimationFrame(()=>{null!=l&&ae(f.value,l)}))}function k(){u(),m.value=-1}function S(t){return"number"===e.type&&/[^0-9]/g.test(t)}return aa(()=>e.autofocus,()=>{const e=t.effectScope()
e.run(()=>{const{intersectionRef:a,isIntersecting:l}=en()
t.watchEffect(()=>{a.value=g.value[0]}),t.watch(l,t=>{t&&(a.value?.focus(),e.stop())})})}),yt({VField:{color:t.toRef(()=>e.color),bgColor:t.toRef(()=>e.color),baseColor:t.toRef(()=>e.baseColor),disabled:t.toRef(()=>e.disabled),error:t.toRef(()=>e.error),variant:t.toRef(()=>e.variant),rounded:t.toRef(()=>e.rounded)}},{scoped:!0}),t.watch(c,e=>{e.length===v.value&&n("finish",e.join(""))},{deep:!0}),t.watch(m,e=>{e<0||t.nextTick(()=>{g.value[e]?.select()})}),Bt(()=>{const[a,n]=T(l)
return t.createElementVNode("div",t.mergeProps({class:["v-otp-input",{"v-otp-input--divided":!!e.divider},e.class],style:[e.style]},a),[t.createElementVNode("div",{ref:f,class:"v-otp-input__content",style:t.normalizeStyle([r.value])},[p.value.map((a,l)=>t.createElementVNode(t.Fragment,null,[e.divider&&0!==l&&t.createElementVNode("span",{class:"v-otp-input__divider"},[e.divider]),t.createVNode($i,{focused:i.value&&e.focusAll||m.value===l,key:l},{...o,loader:void 0,default:()=>t.createElementVNode("input",{ref:e=>g.value[l]=e,"aria-label":d(e.label,l+1),autofocus:0===l&&e.autofocus,autocomplete:"one-time-code",class:t.normalizeClass(["v-otp-input__field"]),disabled:e.disabled,inputmode:"number"===e.type?"numeric":"text",min:"number"===e.type?0:void 0,maxlength:0===l?v.value:"1",placeholder:e.placeholder,type:"number"===e.type?"text":e.type,value:c.value[l],onInput:b,onFocus:e=>function(e,t){s(),m.value=t}(0,l),onBlur:k,onKeydown:w,onCompositionstart:()=>y=!0,onCompositionend:V,onPaste:e=>function(e,t){t.preventDefault(),t.stopPropagation()
const a=t?.clipboardData?.getData("Text").trim().slice(0,v.value)??"",l=a.length-1==-1?e:a.length-1
S(a)||(c.value=a.split(""),m.value=l)}(l,e)},null)})])),t.createElementVNode("input",t.mergeProps({class:"v-otp-input-input",type:"hidden"},n,{value:c.value.join("")}),null),t.createVNode(Ii,{contained:!0,contentClass:"v-otp-input__loader",modelValue:!!e.loading,persistent:!0},{default:()=>[o.loader?.()??t.createVNode(an,{color:"boolean"==typeof e.loading?void 0:e.loading,indeterminate:!0,size:"24",width:"2"},null)]}),o.default?.()])])}),{blur:()=>{g.value?.some(e=>e.blur())},focus:()=>{g.value?.[0].focus()},reset:function(){c.value=[]},isFocused:i}}})
const zm=vt({scale:{type:[Number,String],default:.5},...pt()},"VParallax"),Lm=wt()({name:"VParallax",props:zm(),setup(e,a){let{slots:l}=a
const{intersectionRef:n,isIntersecting:o}=en(),{resizeRef:r,contentRect:i}=Kt(),{height:s}=Ro(),u=t.ref()
let d
t.watchEffect(()=>{n.value=r.value=u.value?.$el}),t.watch(o,e=>{e?(d=Pt(n.value),d=d===document.scrollingElement?document:d,d.addEventListener("scroll",m,{passive:!0}),m()):d.removeEventListener("scroll",m)}),t.onBeforeUnmount(()=>{d?.removeEventListener("scroll",m)}),t.watch(s,m),t.watch(()=>i.value?.height,m)
const v=t.computed(()=>1-F(Number(e.scale)))
let p=-1
function m(){o.value&&!c()&&(cancelAnimationFrame(p),p=requestAnimationFrame(()=>{const e=(u.value?.$el).querySelector(".v-img__img")
if(!e)return
const t=d instanceof Document?document.documentElement.clientHeight:d.clientHeight,a=d instanceof Document?window.scrollY:d.scrollTop,l=n.value.getBoundingClientRect().top+a,o=i.value.height,r=(s=(a-(l+(o-t)/2))*v.value,Math.floor(Math.abs(s))*Math.sign(s))
var s
const c=Math.max(1,(v.value*(t-o)+o)/o)
e.style.setProperty("transform",`translateY(${r}px) scale(${c})`)}))}return Bt(()=>t.createVNode(Vl,{class:t.normalizeClass(["v-parallax",{"v-parallax--active":o.value},e.class]),style:t.normalizeStyle(e.style),ref:u,cover:!0,onLoadstart:m,onLoad:m},l)),{}}}),Om=vt({...to({falseIcon:"$radioOff",trueIcon:"$radioOn"})},"VRadio"),jm=wt()({name:"VRadio",props:Om(),setup(e,a){let{slots:l}=a
return Bt(()=>{const a=ao.filterProps(e)
return t.createVNode(ao,t.mergeProps(a,{class:["v-radio",e.class],style:e.style,type:"radio"}),l)}),{}}}),Hm=vt({height:{type:[Number,String],default:"auto"},...I(ho(),["direction"]),...I(Qn(),["multiple"]),trueIcon:{type:Dt,default:"$radioOn"},falseIcon:{type:Dt,default:"$radioOff"},type:{type:String,default:"radio"}},"VRadioGroup"),Wm=wt()({name:"VRadioGroup",inheritAttrs:!1,props:Hm(),emits:{"update:modelValue":e=>!0},setup(e,a){let{attrs:l,slots:n}=a
const o=t.useId(),r=t.computed(()=>e.id||`radio-group-${o}`),i=la(e,"modelValue"),s=t.ref()
return Bt(()=>{const[a,o]=T(l),u=yo.filterProps(e),c=ao.filterProps(e),d=n.label?n.label({label:e.label,props:{for:r.value}}):e.label
return t.createVNode(yo,t.mergeProps({ref:s,class:["v-radio-group",e.class],style:e.style},a,u,{modelValue:i.value,"onUpdate:modelValue":e=>i.value=e,id:r.value}),{...n,default:a=>{let{id:l,messagesId:r,isDisabled:s,isReadonly:u}=a
return t.createElementVNode(t.Fragment,null,[d&&t.createVNode(Xn,{id:l.value},{default:()=>[d]}),t.createVNode(eo,t.mergeProps(c,{id:l.value,"aria-describedby":r.value,defaultsTarget:"VRadio",trueIcon:e.trueIcon,falseIcon:e.falseIcon,type:e.type,disabled:s.value,readonly:u.value,"aria-labelledby":d?l.value:void 0,multiple:!1},o,{modelValue:i.value,"onUpdate:modelValue":e=>i.value=e}),n)])}})}),wo({},s)}}),Ym=vt({...so(),...ho(),...Kc(),strict:Boolean,modelValue:{type:Array,default:()=>[0,0]}},"VRangeSlider"),Um=wt()({name:"VRangeSlider",inheritAttrs:!1,props:Ym(),emits:{"update:focused":e=>!0,"update:modelValue":e=>!0,end:e=>!0,start:e=>!0},setup(e,a){let{slots:l,emit:n,attrs:o}=a
const r=t.ref(),i=t.ref(),s=t.ref(),{rtlClasses:u}=ga()
const c=qc(e),d=la(e,"modelValue",void 0,e=>e?.length?e.map(e=>c.roundValue(e)):[0,0]),{activeThumbRef:v,hasLabels:p,max:m,min:f,mousePressed:g,onSliderMousedown:h,onSliderTouchstart:y,position:b,trackContainerRef:V,disabled:w,readonly:k}=Xc({props:e,steps:c,onSliderStart:()=>{w.value||k.value?v.value?.blur():n("start",d.value)},onSliderEnd:t=>{let{value:a}=t
if(w.value||k.value)v.value?.blur()
else{const t=v.value===r.value?.$el?[a,d.value[1]]:[d.value[0],a]
!e.strict&&t[0]<t[1]&&(d.value=t)}n("end",d.value)},onSliderMove:t=>{let{value:a}=t
const[l,n]=d.value
w.value||k.value?v.value?.blur():(e.strict||l!==n||l===f.value||(v.value=a>l?i.value?.$el:r.value?.$el,v.value?.focus()),v.value===r.value?.$el?d.value=[Math.min(a,n),n]:d.value=[l,Math.max(l,a)])},getActiveThumb:function(t){if(!r.value||!i.value)return
const a=Gc(t,r.value.$el,e.direction),l=Gc(t,i.value.$el,e.direction),n=Math.abs(a),o=Math.abs(l)
return n<o||n===o&&a<0?r.value.$el:i.value.$el}}),{isFocused:S,focus:x,blur:N}=uo(e),C=t.computed(()=>b(d.value[0])),E=t.computed(()=>b(d.value[1]))
return Bt(()=>{const a=yo.filterProps(e),[n,c]=T(o),b=!!(e.label||l.label||l.prepend)
return t.createVNode(yo,t.mergeProps({class:["v-slider","v-range-slider",{"v-slider--has-labels":!!l["tick-label"]||p.value,"v-slider--focused":S.value,"v-slider--pressed":g.value,"v-slider--disabled":w.value},u.value,e.class],style:e.style,ref:s},a,n,{focused:S.value}),{...l,prepend:b?a=>t.createElementVNode(t.Fragment,null,[l.label?.(a)??(e.label?t.createVNode(Xn,{class:"v-slider__label",text:e.label},null):void 0),l.prepend?.(a)]):void 0,default:a=>{let{id:n,messagesId:o}=a
return t.createElementVNode("div",{class:"v-slider__container",onMousedown:k.value?void 0:h,onTouchstartPassive:k.value?void 0:y},[t.createElementVNode("input",{id:`${n.value}_start`,name:e.name||n.value,disabled:w.value,readonly:k.value,tabindex:"-1",value:d.value[0]},null),t.createElementVNode("input",{id:`${n.value}_stop`,name:e.name||n.value,disabled:w.value,readonly:k.value,tabindex:"-1",value:d.value[1]},null),t.createVNode(ed,{ref:V,start:C.value,stop:E.value},{"tick-label":l["tick-label"]}),t.createVNode(Qc,t.mergeProps({ref:r,"aria-describedby":o.value,focused:S&&v.value===r.value?.$el,modelValue:d.value[0],"onUpdate:modelValue":e=>d.value=[e,d.value[1]],onFocus:e=>{x(),v.value=r.value?.$el,m.value!==f.value&&d.value[0]===d.value[1]&&d.value[1]===f.value&&e.relatedTarget!==i.value?.$el&&(r.value?.$el.blur(),i.value?.$el.focus())},onBlur:()=>{N(),v.value=void 0},min:f.value,max:d.value[1],position:C.value,ripple:e.ripple},c),{"thumb-label":l["thumb-label"]}),t.createVNode(Qc,t.mergeProps({ref:i,"aria-describedby":o.value,focused:S&&v.value===i.value?.$el,modelValue:d.value[1],"onUpdate:modelValue":e=>d.value=[d.value[0],e],onFocus:e=>{x(),v.value=i.value?.$el,m.value!==f.value&&d.value[0]===d.value[1]&&d.value[0]===m.value&&e.relatedTarget!==r.value?.$el&&(i.value?.$el.blur(),r.value?.$el.focus())},onBlur:()=>{N(),v.value=void 0},min:d.value[0],max:m.value,position:E.value,ripple:e.ripple},c),{"thumb-label":l["thumb-label"]})])}})}),wo({focus:()=>r.value?.$el.focus()},s)}}),Gm=vt({name:String,itemAriaLabel:{type:String,default:"$vuetify.rating.ariaLabel.item"},activeColor:String,color:String,clearable:Boolean,disabled:Boolean,emptyIcon:{type:Dt,default:"$ratingEmpty"},fullIcon:{type:Dt,default:"$ratingFull"},halfIncrements:Boolean,hover:Boolean,length:{type:[Number,String],default:5},readonly:Boolean,modelValue:{type:[Number,String],default:0},itemLabels:Array,itemLabelPosition:{type:String,default:"top",validator:e=>["top","bottom"].includes(e)},ripple:Boolean,...pt(),...Tl(),...Xl(),...Pa(),...ya()},"VRating"),Km=wt()({name:"VRating",props:Gm(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const{t:n}=ma(),{themeClasses:o}=Ca(e),r=t.ref(),i=la(e,"modelValue"),s=t.computed(()=>F(parseFloat(i.value),0,Number(e.length))),u=t.computed(()=>y(Number(e.length),1)),c=t.computed(()=>u.value.flatMap(t=>e.halfIncrements?[t-.5,t]:[t])),d=t.shallowRef(-1),v=t.computed(()=>c.value.map(t=>{const a=e.hover&&d.value>-1,l=s.value>=t,n=d.value>=t,o=(a?n:l)?e.fullIcon:e.emptyIcon,r=e.activeColor??e.color
return{isFilled:l,isHovered:n,icon:o,color:l||n?r:e.color}})),p=t.computed(()=>[0,...c.value].map(t=>({onMouseenter:e.hover?function(){d.value=t}:void 0,onMouseleave:e.hover?function(){d.value=-1}:void 0,onClick:function(){e.disabled||e.readonly||(i.value=s.value===t&&e.clearable?0:t)}}))),m=t.computed(()=>e.halfIncrements?1+2*Math.floor(Math.max(0,Number(i.value??0)-.5)):Math.floor(Math.max(0,Number(i.value??0)-1)))
function f(){const e=r.value?.querySelector('[tabindex="0"]')
e?.focus()}function g(a){if(e.disabled||e.readonly)return
if(a.ctrlKey||a.altKey)return
const l=e.halfIncrements?.5:1
if("ArrowRight"===a.key){const a=Math.min(Number(e.length),Number(i.value??0)+l)
i.value=a,t.nextTick(()=>f())}if("ArrowLeft"===a.key){const e=Math.max(0,Number(i.value??0)-l)
i.value=e,t.nextTick(()=>f())}}const h=t.useId(),b=t.computed(()=>e.name??`v-rating-${h}`)
function V(a){let{value:o,index:r,showStar:i=!0}=a
const{onMouseenter:u,onMouseleave:c,onClick:d}=p.value[r+1],f=`${b.value}-${String(o).replace(".","-")}`,h=r===m.value,y={color:v.value[r]?.color,density:e.density,disabled:e.disabled,icon:v.value[r]?.icon,ripple:e.ripple,size:e.size,variant:"plain",tabindex:h?0:-1,onKeydown:g}
return t.createElementVNode(t.Fragment,null,[t.createElementVNode("label",{for:f,class:t.normalizeClass({"v-rating__item--half":e.halfIncrements&&o%1>0,"v-rating__item--full":e.halfIncrements&&o%1==0}),onMouseenter:u,onMouseleave:c,onClick:d},[t.createElementVNode("span",{class:"v-rating__hidden"},[n(e.itemAriaLabel,o,e.length)]),i?l.item?l.item({...v.value[r],props:y,value:o,index:r,rating:s.value}):t.createVNode($n,t.mergeProps({"aria-label":n(e.itemAriaLabel,o,e.length)},y),null):void 0]),t.createElementVNode("input",{class:"v-rating__hidden",name:b.value,id:f,type:"radio",value:o,checked:s.value===o,tabindex:-1,readonly:e.readonly,disabled:e.disabled},null)])}function w(e){return l["item-label"]?l["item-label"](e):e.label?t.createElementVNode("span",null,[e.label]):t.createElementVNode("span",null,[t.createTextVNode(" ")])}return Bt(()=>{const a=!!e.itemLabels?.length||l["item-label"]
return t.createVNode(e.tag,{class:t.normalizeClass(["v-rating",{"v-rating--hover":e.hover,"v-rating--readonly":e.readonly},o.value,e.class]),style:t.normalizeStyle(e.style),ref:r},{default:()=>[t.createVNode(V,{value:0,index:-1,showStar:!1},null),u.value.map((l,n)=>t.createElementVNode("div",{class:"v-rating__wrapper"},[a&&"top"===e.itemLabelPosition?w({value:l,index:n,label:e.itemLabels?.[n]}):void 0,t.createElementVNode("div",{class:"v-rating__item"},[e.halfIncrements?t.createElementVNode(t.Fragment,null,[t.createVNode(V,{value:l-.5,index:2*n},null),t.createVNode(V,{value:l,index:2*n+1},null)]):t.createVNode(V,{value:l,index:n},null)]),a&&"bottom"===e.itemLabelPosition?w({value:l,index:n,label:e.itemLabels?.[n]}):void 0]))]})}),{}}}),qm={actions:"button@2",article:"heading, paragraph",avatar:"avatar",button:"button",card:"image, heading","card-avatar":"image, list-item-avatar",chip:"chip","date-picker":"list-item, heading, divider, date-picker-options, date-picker-days, actions","date-picker-options":"text, avatar@2","date-picker-days":"avatar@28",divider:"divider",heading:"heading",image:"image","list-item":"text","list-item-avatar":"avatar, text","list-item-two-line":"sentences","list-item-avatar-two-line":"avatar, sentences","list-item-three-line":"paragraph","list-item-avatar-three-line":"avatar, paragraph",ossein:"ossein",paragraph:"text@3",sentences:"text@2",subtitle:"text",table:"table-heading, table-thead, table-tbody, table-tfoot","table-heading":"chip, text","table-thead":"heading@6","table-tbody":"table-row-divider@6","table-row-divider":"table-row, divider","table-row":"text@6","table-tfoot":"text@2, avatar@2",text:"text"}
function Xm(e){let a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[]
return t.createElementVNode("div",{class:t.normalizeClass(["v-skeleton-loader__bone",`v-skeleton-loader__${e}`])},[a])}function Zm(e){const[t,a]=e.split("@")
return Array.from({length:a}).map(()=>Qm(t))}function Qm(e){let t=[]
if(!e)return t
const a=qm[e]
if(e===a);else{if(e.includes(","))return Jm(e)
if(e.includes("@"))return Zm(e)
a.includes(",")?t=Jm(a):a.includes("@")?t=Zm(a):a&&t.push(Qm(a))}return[Xm(e,t)]}function Jm(e){return e.replace(/\s/g,"").split(",").map(Qm)}const ef=vt({boilerplate:Boolean,color:String,loading:Boolean,loadingText:{type:String,default:"$vuetify.loading"},type:{type:[String,Array],default:"ossein"},...ol(),...Sl(),...ya()},"VSkeletonLoader"),tf=wt()({name:"VSkeletonLoader",inheritAttrs:!1,props:ef(),setup(e,a){let{attrs:l,slots:n}=a
const{backgroundColorClasses:o,backgroundColorStyles:r}=dl(()=>e.color),{dimensionStyles:i}=rl(e),{elevationClasses:s}=xl(e),{themeClasses:u}=Ca(e),{t:c}=ma(),d=t.computed(()=>Qm(B(e.type).join(",")))
return Bt(()=>{const a=!n.default||e.loading,v=e.boilerplate||!a?{}:{ariaLive:"polite",ariaLabel:c(e.loadingText),role:"alert"}
return a?t.createElementVNode("div",t.mergeProps({class:["v-skeleton-loader",{"v-skeleton-loader--boilerplate":e.boilerplate},u.value,o.value,s.value],style:[r.value,i.value]},v,l),[d.value]):t.createElementVNode(t.Fragment,null,[n.default?.()])}),{}}}),af=wt()({name:"VSlideGroupItem",props:jl(),emits:{"group:selected":e=>!0},setup(e,t){let{slots:a}=t
const l=Hl(e,Ho)
return()=>a.default?.({isSelected:l.isSelected.value,select:l.select,toggle:l.toggle,selectedClass:l.selectedClass.value})}})
const lf=vt({multiLine:Boolean,text:String,timer:[Boolean,String],timeout:{type:[Number,String],default:5e3},vertical:Boolean,...nn({location:"bottom"}),...mn(),...pl(),...$l(),...ya(),...I(Ei({transition:"v-snackbar-transition"}),["persistent","noClickAnimation","retainFocus","captureFocus","disableInitialFocus","scrim","scrollStrategy","stickToTarget","viewportMargin"])},"VSnackbar"),nf=wt()({name:"VSnackbar",props:lf(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=la(e,"modelValue"),{positionClasses:o}=fn(e),{scopeId:r}=yi(),{themeClasses:i}=Ca(e),{colorClasses:s,colorStyles:u,variantClasses:c}=Ml(e),{roundedClasses:d}=ml(e),v=function(e){const a=t.shallowRef(e())
let l=-1
function n(){clearInterval(l)}return t.onScopeDispose(n),{clear:n,time:a,start:function(t){const o=t?getComputedStyle(t):{transitionDuration:.2},r=1e3*parseFloat(o.transitionDuration)||200
if(n(),a.value<=0)return
const i=performance.now()
l=window.setInterval(()=>{const t=performance.now()-i+r
a.value=Math.max(e()-t,0),a.value<=0&&n()},r)},reset:function(){n(),t.nextTick(()=>a.value=e())}}}(()=>Number(e.timeout)),p=t.ref(),m=t.ref(),f=t.shallowRef(!1),g=t.shallowRef(0),h=t.ref(),y=t.inject(qt,void 0)
aa(()=>!!y,()=>{const e=Jt()
t.watchEffect(()=>{h.value=e.mainStyles.value})}),t.watch(n,V),t.watch(()=>e.timeout,V),t.onMounted(()=>{n.value&&V()})
let b=-1
function V(){v.reset(),window.clearTimeout(b)
const t=Number(e.timeout)
if(!n.value||-1===t)return
const a=k(m.value)
v.start(a),b=window.setTimeout(()=>{n.value=!1},t)}function w(){f.value=!0,v.reset(),window.clearTimeout(b)}function S(){f.value=!1,V()}function x(e){g.value=e.touches[0].clientY}function N(e){Math.abs(g.value-e.changedTouches[0].clientY)>50&&(n.value=!1)}function C(){f.value&&S()}const E=t.computed(()=>e.location.split(" ").reduce((e,t)=>(e[`v-snackbar--${t}`]=!0,e),{}))
return Bt(()=>{const a=Ii.filterProps(e),g=!!(l.default||l.text||e.text)
return t.createVNode(Ii,t.mergeProps({ref:p,class:["v-snackbar",{"v-snackbar--active":n.value,"v-snackbar--multi-line":e.multiLine&&!e.vertical,"v-snackbar--timer":!!e.timer,"v-snackbar--vertical":e.vertical},E.value,o.value,e.class],style:[h.value,e.style]},a,{modelValue:n.value,"onUpdate:modelValue":e=>n.value=e,contentProps:t.mergeProps({class:["v-snackbar__wrapper",i.value,s.value,d.value,c.value],style:[u.value],onPointerenter:w,onPointerleave:S},a.contentProps),persistent:!0,noClickAnimation:!0,scrim:!1,scrollStrategy:"none",_disableGlobalStack:!0,onTouchstartPassive:x,onTouchend:N,onAfterLeave:C},r),{default:()=>[Fl(!1,"v-snackbar"),e.timer&&!f.value&&t.createElementVNode("div",{key:"timer",class:"v-snackbar__timer"},[t.createVNode(un,{ref:m,color:"string"==typeof e.timer?e.timer:"info",max:e.timeout,modelValue:v.time.value},null)]),g&&t.createElementVNode("div",{key:"content",class:"v-snackbar__content",role:"status","aria-live":"polite"},[l.text?.()??e.text,l.default?.()]),l.actions&&t.createVNode(nl,{defaults:{VBtn:{variant:"text",ripple:!1,slim:!0}}},{default:()=>[t.createElementVNode("div",{class:"v-snackbar__actions"},[l.actions({isActive:n})])]})],activator:l.activator})}),wo({},p)}}),of=vt({closable:[Boolean,String],closeText:{type:String,default:"$vuetify.dismiss"},modelValue:{type:Array,default:()=>[]},...I(lf(),["modelValue"])},"VSnackbarQueue"),rf=wt()({name:"VSnackbarQueue",props:of(),emits:{"update:modelValue":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const{t:o}=ma(),r=t.shallowRef(!1),i=t.shallowRef(!1),s=t.shallowRef()
function u(){e.modelValue.length?c():(s.value=void 0,i.value=!1)}function c(){const[a,...n]=e.modelValue
l("update:modelValue",n),s.value="string"==typeof a?{text:a}:a,t.nextTick(()=>{r.value=!0})}function d(){r.value=!1}t.watch(()=>e.modelValue.length,(e,t)=>{!i.value&&e>t&&c()}),t.watch(r,e=>{e&&(i.value=!0)})
const v=t.computed(()=>({color:"string"==typeof e.closable?e.closable:void 0,text:o(e.closeText)}))
Bt(()=>{const a=!(!e.closable&&!n.actions),{modelValue:l,...o}=nf.filterProps(e)
return t.createElementVNode(t.Fragment,null,[i.value&&!!s.value&&(n.default?t.createVNode(nl,{defaults:{VSnackbar:s.value}},{default:()=>[n.default({item:s.value})]}):t.createVNode(nf,t.mergeProps(o,s.value,{modelValue:r.value,"onUpdate:modelValue":e=>r.value=e,onAfterLeave:u}),{text:n.text?()=>n.text?.({item:s.value}):void 0,actions:a?()=>t.createElementVNode(t.Fragment,null,[n.actions?t.createVNode(nl,{defaults:{VBtn:v.value}},{default:()=>[n.actions({item:s.value,props:{onClick:d}})]}):t.createVNode($n,t.mergeProps(v.value,{onClick:d}),null)]):void 0}))])})}}),sf=vt({autoDraw:Boolean,autoDrawDuration:[Number,String],autoDrawEasing:{type:String,default:"ease"},color:String,gradient:{type:Array,default:()=>[]},gradientDirection:{type:String,validator:e=>["top","bottom","left","right"].includes(e),default:"top"},height:{type:[String,Number],default:75},labels:{type:Array,default:()=>[]},labelSize:{type:[Number,String],default:7},lineWidth:{type:[String,Number],default:4},id:String,itemValue:{type:String,default:"value"},modelValue:{type:Array,default:()=>[]},min:[String,Number],max:[String,Number],padding:{type:[String,Number],default:8},showLabels:Boolean,smooth:[Boolean,String,Number],width:{type:[Number,String],default:300}},"Line"),uf=vt({autoLineWidth:Boolean,...sf()},"VBarline"),cf=wt()({name:"VBarline",props:uf(),setup(e,a){let{slots:l}=a
const n=t.useId(),o=t.computed(()=>e.id||`barline-${n}`),r=t.computed(()=>Number(e.autoDrawDuration)||500),i=t.computed(()=>Boolean(e.showLabels||e.labels.length>0||!!l?.label)),s=t.computed(()=>parseFloat(e.lineWidth)||4),u=t.computed(()=>Math.max(e.modelValue.length*s.value,Number(e.width))),d=t.computed(()=>({minX:0,maxX:u.value,minY:0,maxY:parseInt(e.height,10)})),v=t.computed(()=>e.modelValue.map(t=>h(t,e.itemValue,t)))
function p(t,a){const{minX:l,maxX:n,minY:o,maxY:r}=a,i=t.length
let s=null!=e.max?Number(e.max):Math.max(...t),u=null!=e.min?Number(e.min):Math.min(...t)
u>0&&null==e.min&&(u=0),s<0&&null==e.max&&(s=0)
const c=n/(1===i?2:i),d=(r-o)/(s-u||1),v=r-Math.abs(u*d)
return t.map((e,t)=>{const a=Math.abs(d*e)
return{x:l+t*c,y:v-a+Number(e<0)*a,height:a,value:e}})}const m=t.computed(()=>{const t=[],a=p(v.value,d.value),l=a.length
for(let n=0;t.length<l;n++){const l=a[n]
let o=e.labels[n]
o||(o="object"==typeof l?l.value:l),t.push({x:l.x,value:String(o)})}return t}),f=t.computed(()=>p(v.value,d.value)),g=t.computed(()=>1===f.value.length?(d.value.maxX-s.value)/2:(Math.abs(f.value[0].x-f.value[1].x)-s.value)/2),y=t.computed(()=>"boolean"==typeof e.smooth?e.smooth?2:0:Number(e.smooth))
Bt(()=>{const a=e.gradient.slice().length?e.gradient.slice().reverse():[""]
return t.createElementVNode("svg",{display:"block"},[t.createElementVNode("defs",null,[t.createElementVNode("linearGradient",{id:o.value,gradientUnits:"userSpaceOnUse",x1:"left"===e.gradientDirection?"100%":"0",y1:"top"===e.gradientDirection?"100%":"0",x2:"right"===e.gradientDirection?"100%":"0",y2:"bottom"===e.gradientDirection?"100%":"0"},[a.map((e,l)=>t.createElementVNode("stop",{offset:l/Math.max(a.length-1,1),"stop-color":e||"currentColor"},null))])]),t.createElementVNode("clipPath",{id:`${o.value}-clip`},[f.value.map(a=>t.createElementVNode("rect",{x:a.x+g.value,y:a.y,width:s.value,height:a.height,rx:y.value,ry:y.value},[e.autoDraw&&!c()&&t.createElementVNode(t.Fragment,null,[t.createElementVNode("animate",{attributeName:"y",from:a.y+a.height,to:a.y,dur:`${r.value}ms`,fill:"freeze"},null),t.createElementVNode("animate",{attributeName:"height",from:"0",to:a.height,dur:`${r.value}ms`,fill:"freeze"},null)])]))]),i.value&&t.createElementVNode("g",{key:"labels",style:{textAnchor:"middle",dominantBaseline:"mathematical",fill:"currentColor"}},[m.value.map((a,n)=>t.createElementVNode("text",{x:a.x+g.value+s.value/2,y:parseInt(e.height,10)-2+(parseInt(e.labelSize,10)||5.25),"font-size":Number(e.labelSize)||7},[l.label?.({index:n,value:a.value})??a.value]))]),t.createElementVNode("g",{"clip-path":`url(#${o.value}-clip)`,fill:`url(#${o.value})`},[t.createElementVNode("rect",{x:0,y:0,width:Math.max(e.modelValue.length*s.value,Number(e.width)),height:e.height},null)])])})}})
function df(e,t){let a=arguments.length>2&&void 0!==arguments[2]&&arguments[2],l=arguments.length>3&&void 0!==arguments[3]?arguments[3]:75
if(0===e.length)return""
const n=e.shift(),o=e[e.length-1]
return(a?`M${n.x} ${l-n.x+2} L${n.x} ${n.y}`:`M${n.x} ${n.y}`)+e.map((a,l)=>{const o=e[l+1],r=e[l-1]||n,i=o&&(u=a,c=r,vf((s=o).x+c.x)===vf(2*u.x)&&vf(s.y+c.y)===vf(2*u.y))
var s,u,c
if(!o||i)return`L${a.x} ${a.y}`
const d=Math.min(pf(r,a),pf(o,a)),v=d/2<t?d/2:t,p=mf(r,a,v),m=mf(o,a,v)
return`L${p.x} ${p.y}S${a.x} ${a.y} ${m.x} ${m.y}`}).join("")+(a?`L${o.x} ${l-n.x+2} Z`:"")}function vf(e){return parseInt(e,10)}function pf(e,t){return Math.sqrt(Math.pow(t.x-e.x,2)+Math.pow(t.y-e.y,2))}function mf(e,t,a){const l=e.x-t.x,n=e.y-t.y,o=Math.sqrt(l*l+n*n),r=l/o,i=n/o
return{x:t.x+r*a,y:t.y+i*a}}const ff=vt({fill:Boolean,...sf()},"VTrendline"),gf=wt()({name:"VTrendline",props:ff(),setup(e,a){let{slots:l}=a
const n=t.useId(),o=t.computed(()=>e.id||`trendline-${n}`),r=t.computed(()=>Number(e.autoDrawDuration)||(e.fill?500:2e3)),i=t.ref(0),s=t.ref(null)
function u(t,a){const{minX:l,maxX:n,minY:o,maxY:r}=a
1===t.length&&(t=[t[0],t[0]])
const i=t.length,s=null!=e.max?Number(e.max):Math.max(...t),u=null!=e.min?Number(e.min):Math.min(...t),c=(n-l)/(i-1),d=(r-o)/(s-u||1)
return t.map((e,t)=>({x:l+t*c,y:r-(e-u)*d,value:e}))}const d=t.computed(()=>Boolean(e.showLabels||e.labels.length>0||!!l?.label)),v=t.computed(()=>parseFloat(e.lineWidth)||4),p=t.computed(()=>Number(e.width)),m=t.computed(()=>{const t=Number(e.padding)
return{minX:t,maxX:p.value-t,minY:t,maxY:parseInt(e.height,10)-t}}),f=t.computed(()=>e.modelValue.map(t=>h(t,e.itemValue,t))),g=t.computed(()=>{const t=[],a=u(f.value,m.value),l=a.length
for(let n=0;t.length<l;n++){const l=a[n]
let o=e.labels[n]
o||(o="object"==typeof l?l.value:l),t.push({x:l.x,value:String(o)})}return t})
function y(t){const a="boolean"==typeof e.smooth?e.smooth?8:0:Number(e.smooth)
return df(u(f.value,m.value),a,t,parseInt(e.height,10))}t.watch(()=>e.modelValue,async()=>{if(await t.nextTick(),!e.autoDraw||!s.value||c())return
const a=s.value,l=a.getTotalLength()
e.fill?(a.style.transformOrigin="bottom center",a.style.transition="none",a.style.transform="scaleY(0)",a.getBoundingClientRect(),a.style.transition=`transform ${r.value}ms ${e.autoDrawEasing}`,a.style.transform="scaleY(1)"):(a.style.strokeDasharray=`${l}`,a.style.strokeDashoffset=`${l}`,a.getBoundingClientRect(),a.style.transition=`stroke-dashoffset ${r.value}ms ${e.autoDrawEasing}`,a.style.strokeDashoffset="0"),i.value=l},{immediate:!0}),Bt(()=>{const a=e.gradient.slice().length?e.gradient.slice().reverse():[""]
return t.createElementVNode("svg",{display:"block","stroke-width":parseFloat(e.lineWidth)??4},[t.createElementVNode("defs",null,[t.createElementVNode("linearGradient",{id:o.value,gradientUnits:"userSpaceOnUse",x1:"left"===e.gradientDirection?"100%":"0",y1:"top"===e.gradientDirection?"100%":"0",x2:"right"===e.gradientDirection?"100%":"0",y2:"bottom"===e.gradientDirection?"100%":"0"},[a.map((e,l)=>t.createElementVNode("stop",{offset:l/Math.max(a.length-1,1),"stop-color":e||"currentColor"},null))])]),d.value&&t.createElementVNode("g",{key:"labels",style:{textAnchor:"middle",dominantBaseline:"mathematical",fill:"currentColor"}},[g.value.map((a,n)=>t.createElementVNode("text",{x:a.x+v.value/2+v.value/2,y:parseInt(e.height,10)-4+(parseInt(e.labelSize,10)||5.25),"font-size":Number(e.labelSize)||7},[l.label?.({index:n,value:a.value})??a.value]))]),t.createElementVNode("path",{ref:s,d:y(e.fill),fill:e.fill?`url(#${o.value})`:"none",stroke:e.fill?"none":`url(#${o.value})`},null),e.fill&&t.createElementVNode("path",{d:y(!1),fill:"none",stroke:e.color??e.gradient?.[0]},null)])})}}),hf=vt({type:{type:String,default:"trend"},...uf(),...ff()},"VSparkline"),yf=wt()({name:"VSparkline",props:hf(),setup(e,a){let{slots:l}=a
const{textColorClasses:n,textColorStyles:o}=cl(()=>e.color),r=t.computed(()=>Boolean(e.showLabels||e.labels.length>0||!!l?.label)),i=t.computed(()=>{let t=parseInt(e.height,10)
return r.value&&(t+=1.5*parseInt(e.labelSize,10)),t})
Bt(()=>{const a="trend"===e.type?gf:cf,r="trend"===e.type?gf.filterProps(e):cf.filterProps(e)
return t.createVNode(a,t.mergeProps({key:e.type,class:n.value,style:o.value,viewBox:`0 0 ${e.width} ${parseInt(i.value,10)}`},r),l)})}}),bf=vt({...pt(),..._i({offset:8,minWidth:0,openDelay:0,closeDelay:100,location:"top center",transition:"scale-transition"})},"VSpeedDial"),Vf=wt()({name:"VSpeedDial",props:bf(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=la(e,"modelValue"),o=t.ref(),r=t.computed(()=>{const[t,a="center"]=e.location?.split(" ")??[]
return`${t} ${a}`}),i=t.computed(()=>({[`v-speed-dial__content--${r.value.replace(" ","-")}`]:!0}))
return Bt(()=>{const a=Pi.filterProps(e)
return t.createVNode(Pi,t.mergeProps(a,{modelValue:n.value,"onUpdate:modelValue":e=>n.value=e,class:e.class,style:e.style,contentClass:["v-speed-dial__content",i.value,e.contentClass],location:r.value,ref:o,transition:"fade-transition"}),{...l,default:a=>t.createVNode(nl,{defaults:{VBtn:{size:"small"}}},{default:()=>[t.createVNode(gl,{appear:!0,group:!0,transition:e.transition},{default:()=>[l.default?.(a)]})]})})}),{}}}),wf=Symbol.for("vuetify:v-stepper"),kf=vt({color:String,disabled:{type:[Boolean,String],default:!1},prevText:{type:String,default:"$vuetify.stepper.prev"},nextText:{type:String,default:"$vuetify.stepper.next"}},"VStepperActions"),Sf=wt()({name:"VStepperActions",props:kf(),emits:{"click:prev":()=>!0,"click:next":()=>!0},setup(e,a){let{emit:l,slots:n}=a
const{t:o}=ma()
function r(){l("click:prev")}function i(){l("click:next")}return Bt(()=>{const a={onClick:r},l={onClick:i}
return t.createElementVNode("div",{class:"v-stepper-actions"},[t.createVNode(nl,{defaults:{VBtn:{disabled:["prev",!0].includes(e.disabled),text:o(e.prevText),variant:"text"}}},{default:()=>[n.prev?.({props:a})??t.createVNode($n,a,null)]}),t.createVNode(nl,{defaults:{VBtn:{color:e.color,disabled:["next",!0].includes(e.disabled),text:o(e.nextText),variant:"tonal"}}},{default:()=>[n.next?.({props:l})??t.createVNode($n,l,null)]})])}),{}}}),xf=kt("v-stepper-header"),Nf=vt({color:String,title:String,subtitle:String,complete:Boolean,completeIcon:{type:Dt,default:"$complete"},editable:Boolean,editIcon:{type:Dt,default:"$edit"},error:Boolean,errorIcon:{type:Dt,default:"$error"},icon:Dt,ripple:{type:[Boolean,Object],default:!0},rules:{type:Array,default:()=>[]}},"StepperItem"),Cf=vt({...Nf(),...jl()},"VStepperItem"),Ef=wt()({name:"VStepperItem",directives:{vRipple:Dn},props:Cf(),emits:{"group:selected":e=>!0},setup(e,a){let{slots:l}=a
const n=Hl(e,wf,!0),o=t.computed(()=>n?.value.value??e.value),r=t.computed(()=>e.rules.every(e=>!0===e())),i=t.computed(()=>!e.disabled&&e.editable),s=t.computed(()=>!e.disabled&&e.editable),u=t.computed(()=>e.error||!r.value),c=t.computed(()=>e.complete||e.rules.length>0&&r.value),d=t.computed(()=>u.value?e.errorIcon:c.value?e.completeIcon:n.isSelected.value&&e.editable?e.editIcon:e.icon),v=t.computed(()=>({canEdit:s.value,hasError:u.value,hasCompleted:c.value,title:e.title,subtitle:e.subtitle,step:o.value,value:e.value}))
return Bt(()=>{const a=(!n||n.isSelected.value||c.value||s.value)&&!u.value&&!e.disabled,r=!(null==e.title&&!l.title),p=!(null==e.subtitle&&!l.subtitle)
return t.withDirectives(t.createElementVNode("button",{class:t.normalizeClass(["v-stepper-item",{"v-stepper-item--complete":c.value,"v-stepper-item--disabled":e.disabled,"v-stepper-item--error":u.value},n?.selectedClass.value]),disabled:!e.editable,type:"button",onClick:function(){n?.toggle()}},[i.value&&Fl(!0,"v-stepper-item"),t.createVNode(Kn,{key:"stepper-avatar",class:"v-stepper-item__avatar",color:a?e.color:void 0,size:24},{default:()=>[l.icon?.(v.value)??(d.value?t.createVNode(Jl,{icon:d.value},null):o.value)]}),t.createElementVNode("div",{class:"v-stepper-item__content"},[r&&t.createElementVNode("div",{key:"title",class:"v-stepper-item__title"},[l.title?.(v.value)??e.title]),p&&t.createElementVNode("div",{key:"subtitle",class:"v-stepper-item__subtitle"},[l.subtitle?.(v.value)??e.subtitle]),l.default?.(v.value)])]),[[Dn,e.editable&&e.ripple,null]])}),{}}}),If=vt({...I(_c(),["continuous","nextIcon","prevIcon","showArrows","touch","mandatory"])},"VStepperWindow"),_f=wt()({name:"VStepperWindow",props:If(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=t.inject(wf,null),o=la(e,"modelValue"),r=t.computed({get:()=>null==o.value&&n?n.items.value.find(e=>n.selected.value.includes(e.id))?.value:o.value,set(e){o.value=e}})
return Bt(()=>{const a=Pc.filterProps(e)
return t.createVNode(Pc,t.mergeProps({_as:"VStepperWindow"},a,{modelValue:r.value,"onUpdate:modelValue":e=>r.value=e,class:["v-stepper-window",e.class],style:e.style,mandatory:!1,touch:!1}),l)}),{}}}),Pf=vt({...Tc()},"VStepperWindowItem"),Af=wt()({name:"VStepperWindowItem",props:Pf(),setup(e,a){let{slots:l}=a
return Bt(()=>{const a=Bc.filterProps(e)
return t.createVNode(Bc,t.mergeProps({_as:"VStepperWindowItem"},a,{class:["v-stepper-window-item",e.class],style:e.style}),l)}),{}}}),Rf=vt({altLabels:Boolean,bgColor:String,completeIcon:Dt,editIcon:Dt,editable:Boolean,errorIcon:Dt,hideActions:Boolean,items:{type:Array,default:()=>[]},itemTitle:{type:[String,Array,Function],default:"title"},itemValue:{type:[String,Array,Function],default:"value"},itemProps:{type:[Boolean,String,Array,Function],default:"props"},nonLinear:Boolean,flat:Boolean,...Ao()},"Stepper"),Tf=vt({...Rf(),...Ol({mandatory:"force",selectedClass:"v-stepper-item--selected"}),...ud(),...C(kf(),["prevText","nextText"])},"VStepper"),Bf=wt()({name:"VStepper",props:Tf(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const{items:n,next:o,prev:r,selected:i}=Wl(e,wf),{displayClasses:s,mobile:u}=Ro(e),{completeIcon:c,editIcon:d,errorIcon:v,color:p,editable:m,prevText:f,nextText:g}=t.toRefs(e),y=t.computed(()=>e.items.map((t,a)=>{const l={title:h(t,e.itemTitle,t),value:h(t,e.itemValue,a+1),...!0===e.itemProps?t:h(t,e.itemProps)}
return{title:l.title,value:l.value,props:l,raw:t}})),b=t.computed(()=>n.value.findIndex(e=>i.value.includes(e.id)))
return yt({VStepperItem:{editable:m,errorIcon:v,completeIcon:c,editIcon:d,prevText:f,nextText:g},VStepperActions:{color:p,disabled:t.computed(()=>e.disabled?e.disabled:0===b.value?"prev":b.value===n.value.length-1&&"next"),prevText:f,nextText:g}}),Bt(()=>{const a=cd.filterProps(e),n=!(!l.header&&!e.items.length),i=e.items.length>0,c=!(e.hideActions||!i&&!l.actions)
return t.createVNode(cd,t.mergeProps(a,{color:e.bgColor,class:["v-stepper",{"v-stepper--alt-labels":e.altLabels,"v-stepper--flat":e.flat,"v-stepper--non-linear":e.nonLinear,"v-stepper--mobile":u.value},s.value,e.class],style:e.style}),{default:()=>[n&&t.createVNode(xf,{key:"stepper-header"},{default:()=>[y.value.map((e,a)=>{let{raw:n,...o}=e
return t.createElementVNode(t.Fragment,null,[!!a&&t.createVNode(Jo,null,null),t.createVNode(Ef,o.props,{default:l[`header-item.${o.value}`]??l.header,icon:l.icon,title:l.title,subtitle:l.subtitle})])})]}),i&&t.createVNode(_f,{key:"stepper-window"},{default:()=>[y.value.map(e=>t.createVNode(Af,{value:e.value},{default:()=>l[`item.${e.value}`]?.(e)??l.item?.(e)}))]}),l.default?.({prev:r,next:o}),c&&(l.actions?.({next:o,prev:r})??t.createVNode(Sf,{key:"stepper-actions","onClick:prev":r,"onClick:next":o},l))]})}),{prev:r,next:o}}}),Df=vt({indeterminate:Boolean,inset:Boolean,flat:Boolean,loading:{type:[Boolean,String],default:!1},...ho(),...to()},"VSwitch"),Ff=wt()({name:"VSwitch",inheritAttrs:!1,props:Df(),emits:{"update:focused":e=>!0,"update:modelValue":e=>!0,"update:indeterminate":e=>!0},setup(e,a){let{attrs:l,slots:n}=a
const o=la(e,"indeterminate"),r=la(e,"modelValue"),{loaderClasses:i}=dn(e),{isFocused:s,focus:c,blur:d}=uo(e),v=t.ref(),p=t.ref(),m=u&&window.matchMedia("(forced-colors: active)").matches,f=t.toRef(()=>"string"==typeof e.loading&&""!==e.loading?e.loading:e.color),g=t.useId(),h=t.toRef(()=>e.id||`switch-${g}`)
function y(){o.value&&(o.value=!1)}function b(e){e.stopPropagation(),e.preventDefault(),v.value?.input?.click()}return Bt(()=>{const[a,u]=T(l),g=yo.filterProps(e),V=ao.filterProps(e)
return t.createVNode(yo,t.mergeProps({ref:p,class:["v-switch",{"v-switch--flat":e.flat},{"v-switch--inset":e.inset},{"v-switch--indeterminate":o.value},i.value,e.class]},a,g,{modelValue:r.value,"onUpdate:modelValue":e=>r.value=e,id:h.value,focused:s.value,style:e.style}),{...n,default:a=>{let{id:l,messagesId:i,isDisabled:s,isReadonly:p,isValid:g}=a
const h={model:r,isValid:g}
return t.createVNode(ao,t.mergeProps({ref:v},V,{modelValue:r.value,"onUpdate:modelValue":[e=>r.value=e,y],id:l.value,"aria-describedby":i.value,type:"checkbox","aria-checked":o.value?"mixed":void 0,disabled:s.value,readonly:p.value,onFocus:c,onBlur:d},u),{...n,default:e=>{let{backgroundColorClasses:a,backgroundColorStyles:l}=e
return t.createElementVNode("div",{class:t.normalizeClass(["v-switch__track",m?void 0:a.value]),style:t.normalizeStyle(l.value),onClick:b},[n["track-true"]&&t.createElementVNode("div",{key:"prepend",class:"v-switch__track-true"},[n["track-true"](h)]),n["track-false"]&&t.createElementVNode("div",{key:"append",class:"v-switch__track-false"},[n["track-false"](h)])])},input:a=>{let{inputNode:l,icon:o,backgroundColorClasses:r,backgroundColorStyles:i}=a
return t.createElementVNode(t.Fragment,null,[l,t.createElementVNode("div",{class:t.normalizeClass(["v-switch__thumb",{"v-switch__thumb--filled":o||e.loading},e.inset||m?void 0:r.value]),style:t.normalizeStyle(e.inset?void 0:i.value)},[n.thumb?t.createVNode(nl,{defaults:{VIcon:{icon:o,size:"x-small"}}},{default:()=>[n.thumb({...h,icon:o})]}):t.createVNode(Ua,null,{default:()=>[e.loading?t.createVNode(vn,{name:"v-switch",active:!0,color:!1===g.value?void 0:f.value},{default:e=>n.loader?n.loader(e):t.createVNode(an,{active:e.isActive,color:e.color,indeterminate:!0,size:"16",width:"2"},null)}):o&&t.createVNode(Jl,{key:String(o),icon:o,size:"x-small"},null)]})])])}})}})}),wo({},p)}}),$f=vt({color:String,height:[Number,String],window:Boolean,...pt(),...Sl(),...Qt(),...pl(),...Pa(),...ya()},"VSystemBar"),Mf=wt()({name:"VSystemBar",props:$f(),setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ca(e),{backgroundColorClasses:o,backgroundColorStyles:r}=dl(()=>e.color),{elevationClasses:i}=xl(e),{roundedClasses:s}=ml(e),{ssrBootStyles:u}=_l(),c=t.computed(()=>e.height??(e.window?32:24)),{layoutItemStyles:d}=ea({id:e.name,order:t.computed(()=>parseInt(e.order,10)),position:t.shallowRef("top"),layoutSize:c,elementSize:c,active:t.computed(()=>!0),absolute:t.toRef(()=>e.absolute)})
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-system-bar",{"v-system-bar--window":e.window},n.value,o.value,i.value,s.value,e.class]),style:t.normalizeStyle([r.value,d.value,u.value,e.style])},l)),{}}}),zf=Symbol.for("vuetify:v-tabs"),Lf=vt({fixed:Boolean,sliderColor:String,sliderTransition:String,sliderTransitionDuration:[String,Number],hideSlider:Boolean,inset:Boolean,direction:{type:String,default:"horizontal"},...I(Fn({selectedClass:"v-tab--selected",variant:"text"}),["active","block","flat","location","position","symbol"])},"VTab"),Of=wt()({name:"VTab",props:Lf(),setup(e,a){let{slots:l,attrs:n}=a
const{textColorClasses:o,textColorStyles:r}=cl(()=>e.sliderColor),{backgroundColorClasses:i,backgroundColorStyles:s}=dl(()=>e.sliderColor),u=t.ref(),c=t.ref(),d=t.computed(()=>"horizontal"===e.direction),v=t.computed(()=>u.value?.group?.isSelected.value??!1)
function p(e,t){return{opacity:[0,1]}}function m(t,a){return"vertical"===e.direction?{transform:["scaleY(0)","scaleY(1)"]}:{transform:["scaleX(0)","scaleX(1)"]}}function f(e,t){const a=t.getBoundingClientRect(),l=e.getBoundingClientRect(),n=d.value?"x":"y",o=d.value?"X":"Y",r=d.value?"right":"bottom",i=d.value?"width":"height",s=a[n]>l[n]?a[r]-l[r]:a[n]-l[n],u=Math.sign(s)>0?d.value?"right":"bottom":Math.sign(s)<0?d.value?"left":"top":"center",c=(Math.abs(s)+(Math.sign(s)<0?a[i]:l[i]))/Math.max(a[i],l[i])||0
return{transform:[`translate${o}(${s}px) scale${o}(${a[i]/l[i]||0})`,`translate${o}(${s/1.5}px) scale${o}(${(c-1)/1.5+1})`,"none"],transformOrigin:Array(3).fill(u)}}function g(t){let{value:a}=t
if(a){const t=u.value?.$el.parentElement?.querySelector(".v-tab--selected .v-tab__slider"),a=c.value
if(!t||!a)return
const l=getComputedStyle(t).color,n={fade:p,grow:m,shift:f}[e.sliderTransition??"shift"]??f,o=Number(e.sliderTransitionDuration)||({fade:400,grow:350,shift:225}[e.sliderTransition??"shift"]??225)
Ne(a,{backgroundColor:[l,"currentcolor"],...n(a,t)},{duration:o,easing:Nt})}}return Bt(()=>{const a=$n.filterProps(e)
return t.createVNode($n,t.mergeProps({symbol:zf,ref:u,class:["v-tab",e.class,v.value&&e.inset?i.value:[]],style:[e.style,v.value&&e.inset?s.value:[]],tabindex:v.value?0:-1,role:"tab","aria-selected":String(v.value),active:!1},a,n,{block:e.fixed,maxWidth:e.fixed?300:void 0,"onGroup:selected":g}),{...l,default:()=>t.createElementVNode(t.Fragment,null,[l.default?.()??e.text,!e.hideSlider&&t.createElementVNode("div",{ref:c,class:t.normalizeClass(["v-tab__slider",o.value]),style:t.normalizeStyle(r.value)},null)])})}),wo({},u)}}),jf=vt({...I(_c(),["continuous","nextIcon","prevIcon","showArrows","touch","mandatory"])},"VTabsWindow"),Hf=wt()({name:"VTabsWindow",props:jf(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=t.inject(zf,null),o=la(e,"modelValue"),r=t.computed({get:()=>null==o.value&&n?n.items.value.find(e=>n.selected.value.includes(e.id))?.value:o.value,set(e){o.value=e}})
return Bt(()=>{const a=Pc.filterProps(e)
return t.createVNode(Pc,t.mergeProps({_as:"VTabsWindow"},a,{modelValue:r.value,"onUpdate:modelValue":e=>r.value=e,class:["v-tabs-window",e.class],style:e.style,mandatory:!1,touch:!1}),l)}),{}}}),Wf=vt({...Tc()},"VTabsWindowItem"),Yf=wt()({name:"VTabsWindowItem",props:Wf(),setup(e,a){let{slots:l}=a
return Bt(()=>{const a=Bc.filterProps(e)
return t.createVNode(Bc,t.mergeProps({_as:"VTabsWindowItem"},a,{class:["v-tabs-window-item",e.class],style:e.style}),l)}),{}}})
const Uf=vt({alignTabs:{type:String,default:"start"},color:String,fixedTabs:Boolean,items:{type:Array,default:()=>[]},stacked:Boolean,bgColor:String,grow:Boolean,height:{type:[Number,String],default:void 0},hideSlider:Boolean,inset:Boolean,insetPadding:[String,Number],insetRadius:[String,Number],sliderColor:String,...C(Lf(),["spaced","sliderTransition","sliderTransitionDuration"]),...Wo({mandatory:"force",selectedClass:"v-tab-item--selected"}),...Tl(),...Pa()},"VTabs"),Gf=wt()({name:"VTabs",props:Uf(),emits:{"update:modelValue":e=>!0},setup(e,a){let{attrs:l,slots:n}=a
const o=la(e,"modelValue"),r=t.computed(()=>function(e){return e?e.map(e=>V(e)?e:{text:e,value:e}):[]}(e.items)),{densityClasses:i}=Bl(e),{backgroundColorClasses:s,backgroundColorStyles:u}=dl(()=>e.bgColor),{scopeId:c}=yi()
return yt({VTab:{color:t.toRef(e,"color"),direction:t.toRef(e,"direction"),stacked:t.toRef(e,"stacked"),fixed:t.toRef(e,"fixedTabs"),inset:t.toRef(e,"inset"),sliderColor:t.toRef(e,"sliderColor"),sliderTransition:t.toRef(e,"sliderTransition"),sliderTransitionDuration:t.toRef(e,"sliderTransitionDuration"),hideSlider:t.toRef(e,"hideSlider")}}),Bt(()=>{const a=Yo.filterProps(e),d=!!(n.window||e.items.length>0)
return t.createElementVNode(t.Fragment,null,[t.createVNode(Yo,t.mergeProps(a,{modelValue:o.value,"onUpdate:modelValue":e=>o.value=e,class:["v-tabs",`v-tabs--${e.direction}`,`v-tabs--align-tabs-${e.alignTabs}`,{"v-tabs--fixed-tabs":e.fixedTabs,"v-tabs--grow":e.grow,"v-tabs--inset":e.inset,"v-tabs--stacked":e.stacked},i.value,s.value,e.class],style:[{"--v-tabs-height":b(e.height),"--v-tabs-inset-padding":e.inset?b(e.insetPadding):void 0,"--v-tabs-inset-radius":e.inset?b(e.insetRadius):void 0},u.value,e.style],role:"tablist",symbol:zf},c,l),{default:n.default??(()=>r.value.map(a=>n.tab?.({item:a})??t.createVNode(Of,t.mergeProps(a,{key:a.text,value:a.value,spaced:e.spaced}),{default:n[`tab.${a.value}`]?()=>n[`tab.${a.value}`]?.({item:a}):void 0}))),prev:n.prev,next:n.next}),d&&t.createVNode(Hf,t.mergeProps({modelValue:o.value,"onUpdate:modelValue":e=>o.value=e,key:"tabs-window"},c),{default:()=>[r.value.map(e=>n.item?.({item:e})??t.createVNode(Yf,{value:e.value},{default:()=>n[`item.${e.value}`]?.({item:e})})),n.window?.()]})])}),{}}}),Kf=vt({autoGrow:Boolean,autofocus:Boolean,counter:[Boolean,Number,String],counterValue:Function,prefix:String,placeholder:String,persistentPlaceholder:Boolean,persistentCounter:Boolean,noResize:Boolean,rows:{type:[Number,String],default:5,validator:e=>!isNaN(parseFloat(e))},maxHeight:{type:[Number,String],validator:e=>!isNaN(parseFloat(e))},maxRows:{type:[Number,String],validator:e=>!isNaN(parseFloat(e))},suffix:String,modelModifiers:Object,...Mi(),...I(ho(),["direction"]),...Fi()},"VTextarea"),qf=wt()({name:"VTextarea",directives:{vIntersect:yl},inheritAttrs:!1,props:Kf(),emits:{"click:control":e=>!0,"mousedown:control":e=>!0,"update:focused":e=>!0,"update:modelValue":e=>!0,"update:rows":e=>!0},setup(e,a){let{attrs:l,emit:n,slots:o}=a
const r=la(e,"modelValue"),{isFocused:i,focus:s,blur:u}=uo(e),{onIntersect:c}=Li(e),d=t.computed(()=>"function"==typeof e.counterValue?e.counterValue(r.value):(r.value||"").toString().length),v=t.computed(()=>l.maxlength?l.maxlength:!e.counter||"number"!=typeof e.counter&&"string"!=typeof e.counter?void 0:e.counter),p=t.ref(),m=t.ref(),f=t.shallowRef(""),g=t.ref(),h=t.ref(0),{platform:y}=Ro(),V=zi(e),w=t.computed(()=>e.persistentPlaceholder||i.value||e.active)
function k(){V.isSuppressing.value&&V.update(),g.value!==document.activeElement&&g.value?.focus(),i.value||s()}function S(e){k(),n("click:control",e)}function x(e){n("mousedown:control",e)}function N(a){a.stopPropagation(),k(),t.nextTick(()=>{r.value="",J(e["onClick:clear"],a)})}function C(a){const l=a.target
if(!e.modelModifiers?.trim)return void(r.value=l.value)
const n=l.value,o=l.selectionStart,i=l.selectionEnd
r.value=n,t.nextTick(()=>{let e=0
n.trimStart().length===l.value.length&&(e=n.length-l.value.length),null!=o&&(l.selectionStart=o-e),null!=i&&(l.selectionEnd=i-e)})}const E=t.ref(),I=t.ref(Number(e.rows)),_=t.computed(()=>["plain","underlined"].includes(e.variant))
function P(){t.nextTick(()=>{if(!g.value)return
if(y.value.firefox)return void(h.value=12)
const{offsetWidth:e,clientWidth:t}=g.value
h.value=Math.max(0,e-t)}),e.autoGrow&&t.nextTick(()=>{if(!E.value||!m.value)return
const t=getComputedStyle(E.value),a=getComputedStyle(m.value.$el),l=parseFloat(t.getPropertyValue("--v-field-padding-top"))+parseFloat(t.getPropertyValue("--v-input-padding-top"))+parseFloat(t.getPropertyValue("--v-field-padding-bottom")),n=E.value.scrollHeight,o=parseFloat(t.lineHeight),r=F(n??0,Math.max(parseFloat(e.rows)*o+l,parseFloat(a.getPropertyValue("--v-input-control-height"))),e.maxHeight?parseFloat(e.maxHeight):parseFloat(e.maxRows)*o+l||1/0)
I.value=Math.floor((r-l)/o),f.value=b(r)})}let A
return t.watchEffect(()=>{e.autoGrow||(I.value=Number(e.rows))}),t.onMounted(P),t.watch(r,P),t.watch(()=>e.rows,P),t.watch(()=>e.maxHeight,P),t.watch(()=>e.maxRows,P),t.watch(()=>e.density,P),t.watch(I,e=>{n("update:rows",e)}),t.watch(E,e=>{e?(A=new ResizeObserver(P),A.observe(E.value)):A?.disconnect()}),t.onBeforeUnmount(()=>{A?.disconnect()}),Bt(()=>{const a=!!(o.counter||e.counter||e.counterValue),n=!(!a&&!o.details),[s,y]=T(l),{modelValue:P,...A}=yo.filterProps(e),R={...$i.filterProps(e),"onClick:clear":N}
return t.createVNode(yo,t.mergeProps({ref:p,modelValue:r.value,"onUpdate:modelValue":e=>r.value=e,class:["v-textarea v-text-field",{"v-textarea--prefixed":e.prefix,"v-textarea--suffixed":e.suffix,"v-text-field--prefixed":e.prefix,"v-text-field--suffixed":e.suffix,"v-textarea--auto-grow":e.autoGrow,"v-textarea--no-resize":e.noResize||e.autoGrow,"v-input--plain-underlined":_.value},e.class],style:[{"--v-textarea-max-height":e.maxHeight?b(e.maxHeight):void 0,"--v-textarea-scroll-bar-width":b(h.value)},e.style]},s,A,{centerAffix:1===I.value&&!_.value,focused:i.value}),{...o,default:a=>{let{id:l,isDisabled:n,isDirty:s,isReadonly:d,isValid:v,hasDetails:p}=a
return t.createVNode($i,t.mergeProps({ref:m,style:{"--v-textarea-control-height":f.value},onClick:S,onMousedown:x,"onClick:prependInner":e["onClick:prependInner"],"onClick:appendInner":e["onClick:appendInner"]},R,{id:l.value,active:w.value||s.value,labelId:`${l.value}-label`,centerAffix:1===I.value&&!_.value,dirty:s.value||e.dirty,disabled:n.value,focused:i.value,details:p.value,error:!1===v.value}),{...o,default:a=>{let{props:{class:o,...i},controlRef:s}=a
return t.createElementVNode(t.Fragment,null,[e.prefix&&t.createElementVNode("span",{class:"v-text-field__prefix"},[e.prefix]),t.withDirectives(t.createElementVNode("textarea",t.mergeProps({ref:e=>g.value=s.value=e,class:o,value:r.value,onInput:C,autofocus:e.autofocus,readonly:d.value,disabled:n.value,placeholder:e.placeholder,rows:e.rows,name:V.fieldName.value,autocomplete:V.fieldAutocomplete.value,onFocus:k,onBlur:u,"aria-labelledby":`${l.value}-label`},i,y),null),[[yl,{handler:c},null,{once:!0}]]),e.autoGrow&&t.withDirectives(t.createElementVNode("textarea",{class:t.normalizeClass([o,"v-textarea__sizer"]),id:`${i.id}-sizer`,"onUpdate:modelValue":e=>r.value=e,ref:E,readonly:!0,"aria-hidden":"true"},null),[[t.vModelText,r.value]]),e.suffix&&t.createElementVNode("span",{class:"v-text-field__suffix"},[e.suffix])])}})},details:n?l=>t.createElementVNode(t.Fragment,null,[o.details?.(l),a&&t.createElementVNode(t.Fragment,null,[t.createElementVNode("span",null,null),t.createVNode(Ri,{active:e.persistentCounter||i.value,value:d.value,max:v.value,disabled:e.disabled},o.counter)])]):void 0})}),wo({},p,m,g)}}),Xf=vt({withBackground:Boolean,...pt(),...ya(),...Pa()},"VThemeProvider"),Zf=wt()({name:"VThemeProvider",props:Xf(),setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ca(e)
return()=>e.withBackground?t.createVNode(e.tag,{class:t.normalizeClass(["v-theme-provider",n.value,e.class]),style:t.normalizeStyle(e.style)},{default:()=>[l.default?.()]}):l.default?.()}}),Qf=vt({dotColor:String,fillDot:Boolean,hideDot:Boolean,icon:Dt,iconColor:String,lineColor:String,...pt(),...pl(),...Xl(),...Sl()},"VTimelineDivider"),Jf=wt()({name:"VTimelineDivider",props:Qf(),setup(e,a){let{slots:l}=a
const{sizeClasses:n,sizeStyles:o}=Zl(e,"v-timeline-divider__dot"),{backgroundColorStyles:r,backgroundColorClasses:i}=dl(()=>e.dotColor),{roundedClasses:s}=ml(e,"v-timeline-divider__dot"),{elevationClasses:u}=xl(e),{backgroundColorClasses:c,backgroundColorStyles:d}=dl(()=>e.lineColor)
return Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-timeline-divider",{"v-timeline-divider--fill-dot":e.fillDot},e.class]),style:t.normalizeStyle(e.style)},[t.createElementVNode("div",{class:t.normalizeClass(["v-timeline-divider__before",c.value]),style:t.normalizeStyle(d.value)},null),!e.hideDot&&t.createElementVNode("div",{key:"dot",class:t.normalizeClass(["v-timeline-divider__dot",u.value,s.value,n.value]),style:t.normalizeStyle(o.value)},[t.createElementVNode("div",{class:t.normalizeClass(["v-timeline-divider__inner-dot",i.value,s.value]),style:t.normalizeStyle(r.value)},[l.default?t.createVNode(nl,{key:"icon-defaults",disabled:!e.icon,defaults:{VIcon:{color:e.iconColor,icon:e.icon,size:e.size}}},l.default):t.createVNode(Jl,{key:"icon",color:e.iconColor,icon:e.icon,size:e.size},null)])]),t.createElementVNode("div",{class:t.normalizeClass(["v-timeline-divider__after",c.value]),style:t.normalizeStyle(d.value)},null)])),{}}}),eg=vt({density:String,dotColor:String,fillDot:Boolean,hideDot:Boolean,hideOpposite:{type:Boolean,default:void 0},icon:Dt,iconColor:String,lineInset:[Number,String],side:{type:String,validator:e=>null==e||["start","end"].includes(e)},...pt(),...ol(),...Sl(),...pl(),...Xl(),...Pa()},"VTimelineItem"),tg=wt()({name:"VTimelineItem",props:eg(),setup(e,a){let{slots:l}=a
const{dimensionStyles:n}=rl(e),o=t.shallowRef(0),r=t.ref()
return t.watch(r,e=>{e&&(o.value=e.$el.querySelector(".v-timeline-divider__dot")?.getBoundingClientRect().width??0)},{flush:"post"}),Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-timeline-item",{"v-timeline-item--fill-dot":e.fillDot,"v-timeline-item--side-start":"start"===e.side,"v-timeline-item--side-end":"end"===e.side},e.class]),style:t.normalizeStyle([{"--v-timeline-dot-size":b(o.value),"--v-timeline-line-inset":e.lineInset?`calc(var(--v-timeline-dot-size) / 2 + ${b(e.lineInset)})`:b(0)},e.style])},[t.createElementVNode("div",{class:"v-timeline-item__body",style:t.normalizeStyle(n.value)},[l.default?.()]),t.createVNode(Jf,{ref:r,hideDot:e.hideDot,icon:e.icon,iconColor:e.iconColor,size:e.size,elevation:e.elevation,dotColor:e.dotColor,fillDot:e.fillDot,rounded:e.rounded},{default:l.icon}),"compact"!==e.density&&t.createElementVNode("div",{class:"v-timeline-item__opposite"},[!e.hideOpposite&&l.opposite?.()])])),{}}}),ag=vt({align:{type:String,default:"center",validator:e=>["center","start"].includes(e)},direction:{type:String,default:"vertical",validator:e=>["vertical","horizontal"].includes(e)},justify:{type:String,default:"auto",validator:e=>["auto","center"].includes(e)},side:{type:String,validator:e=>null==e||["start","end"].includes(e)},lineThickness:{type:[String,Number],default:2},lineColor:String,truncateLine:{type:String,validator:e=>["start","end","both"].includes(e)},...C(eg({lineInset:0}),["dotColor","fillDot","hideOpposite","iconColor","lineInset","size"]),...pt(),...Tl(),...Pa(),...ya()},"VTimeline"),lg=wt()({name:"VTimeline",props:ag(),setup(e,a){let{slots:l}=a
const{themeClasses:n}=Ca(e),{densityClasses:o}=Bl(e),{rtlClasses:r}=ga()
yt({VTimelineDivider:{lineColor:t.toRef(()=>e.lineColor)},VTimelineItem:{density:t.toRef(()=>e.density),dotColor:t.toRef(()=>e.dotColor),fillDot:t.toRef(()=>e.fillDot),hideOpposite:t.toRef(()=>e.hideOpposite),iconColor:t.toRef(()=>e.iconColor),lineColor:t.toRef(()=>e.lineColor),lineInset:t.toRef(()=>e.lineInset),size:t.toRef(()=>e.size)}})
const i=t.computed(()=>{const t=e.side?e.side:"default"!==e.density?"end":null
return t&&`v-timeline--side-${t}`}),s=t.computed(()=>{const t=["v-timeline--truncate-line-start","v-timeline--truncate-line-end"]
switch(e.truncateLine){case"both":return t
case"start":return t[0]
case"end":return t[1]
default:return null}})
return Bt(()=>t.createVNode(e.tag,{class:t.normalizeClass(["v-timeline",`v-timeline--${e.direction}`,`v-timeline--align-${e.align}`,`v-timeline--justify-${e.justify}`,s.value,{"v-timeline--inset-line":!!e.lineInset},n.value,o.value,i.value,r.value,e.class]),style:t.normalizeStyle([{"--v-timeline-line-thickness":b(e.lineThickness)},e.style])},l)),{}}}),ng=vt({allowedValues:Function,ampm:Boolean,color:String,disabled:Boolean,displayedValue:null,double:Boolean,format:{type:Function,default:e=>e},max:{type:Number,required:!0},min:{type:Number,required:!0},scrollable:Boolean,readonly:Boolean,rotate:{type:Number,default:0},step:{type:Number,default:1},modelValue:{type:Number}},"VTimePickerClock"),og=wt()({name:"VTimePickerClock",props:ng(),emits:{change:e=>!0,input:e=>!0},setup(e,a){let{emit:l}=a
const n=t.ref(null),o=t.ref(null),r=t.ref(void 0),i=t.ref(!1),s=t.ref(null),u=t.ref(null),c=D(e=>l("change",e),750),{textColorClasses:d,textColorStyles:v}=cl(()=>e.color),{backgroundColorClasses:p,backgroundColorStyles:m}=dl(()=>e.color),f=t.computed(()=>e.max-e.min+1),g=t.computed(()=>e.double?f.value/2:f.value),h=t.computed(()=>360/g.value),y=t.computed(()=>h.value*Math.PI/180),b=t.computed(()=>null==e.modelValue?e.min:e.modelValue),V=t.computed(()=>.62),w=t.computed(()=>{const t=[]
for(let a=e.min;a<=e.max;a+=e.step)t.push(a)
return t})
function k(e){r.value!==e&&(r.value=e),l("input",e)}function S(t){return!e.allowedValues||e.allowedValues(t)}function x(t){if(!e.scrollable||e.disabled)return
t.preventDefault()
const a=Math.sign(-t.deltaY||1)
let l=b.value
do{l+=a,l=(l-e.min+f.value)%f.value+e.min}while(!S(l)&&l!==b.value)
l!==e.displayedValue&&k(l),c(l)}function N(t){return e.double&&t-e.min>=g.value}function C(e){return N(e)?V.value:1}function E(t,a){const l=(Math.round(t/h.value)+(a?g.value:0))%f.value+e.min
return t<360-h.value/2?l:a?e.max-g.value+1:e.min}function I(t){const{x:a,y:l}=function(t){const a=e.rotate*Math.PI/180
return{x:Math.sin((t-e.min)*y.value+a)*C(t),y:-Math.cos((t-e.min)*y.value+a)*C(t)}}(t)
return{left:`${Math.round(50+50*a)}%`,top:`${Math.round(50+50*l)}%`}}function _(e,t){const a=t.x-e.x,l=t.y-e.y
return Math.sqrt(a*a+l*l)}function P(e){null===s.value&&(s.value=e),u.value=e,k(e)}function A(t){if(t.preventDefault(),!i.value&&"click"!==t.type||!n.value)return
const{width:a,top:l,left:r}=n.value?.getBoundingClientRect(),{width:s}=o.value?.getBoundingClientRect()??{width:0},{clientX:u,clientY:c}="touches"in t?t.touches[0]:t,d={x:a/2,y:-a/2},v={x:u-r,y:l-c},p=Math.round(function(e,t){const a=2*Math.atan2(t.y-e.y-_(e,t),t.x-e.x)
return Math.abs(180*a/Math.PI)}(d,v)-e.rotate+360)%360,m=e.double&&_(d,v)<(s+s*V.value)/4,f=Math.ceil(15/h.value)
let g
for(let e=0;e<f;e++){if(g=E(p+e*h.value,m),S(g))return P(g)
if(g=E(p-e*h.value,m),S(g))return P(g)}}function R(t){e.disabled||(t.preventDefault(),window.addEventListener("mousemove",A),window.addEventListener("touchmove",A),window.addEventListener("mouseup",T),window.addEventListener("touchend",T),s.value=null,u.value=null,i.value=!0,A(t))}function T(e){e.stopPropagation(),B(),i.value=!1,null!==u.value&&S(u.value)&&l("change",u.value)}function B(){window.removeEventListener("mousemove",A),window.removeEventListener("touchmove",A),window.removeEventListener("mouseup",T),window.removeEventListener("touchend",T)}t.watch(()=>e.modelValue,e=>{r.value=e}),t.onScopeDispose(B),Bt(()=>t.createElementVNode("div",{class:t.normalizeClass([{"v-time-picker-clock":!0,"v-time-picker-clock--indeterminate":null==e.modelValue,"v-time-picker-clock--readonly":e.readonly}]),onMousedown:R,onTouchstart:R,onWheel:x,ref:n},[t.createElementVNode("div",{class:"v-time-picker-clock__inner",ref:o},[t.createElementVNode("div",{class:t.normalizeClass([{"v-time-picker-clock__hand":!0,"v-time-picker-clock__hand--inner":N(e.modelValue)},d.value]),style:t.normalizeStyle([{transform:`rotate(${e.rotate+h.value*(b.value-e.min)}deg) scaleY(${C(b.value)})`},v.value])},null),w.value.map(a=>{const l=a===b.value
return t.createElementVNode("div",{class:t.normalizeClass([{"v-time-picker-clock__item":!0,"v-time-picker-clock__item--active":l,"v-time-picker-clock__item--disabled":e.disabled||!S(a)},l&&p.value]),style:t.normalizeStyle([I(a),l&&m.value])},[t.createElementVNode("span",null,[e.format(a)])])})])]))}}),rg=vt({active:Boolean,color:String,disabled:Boolean,label:String,modelValue:String,readonly:Boolean},"VTimePickerField"),ig=wt()({name:"VTimePickerField",inheritAttrs:!1,props:rg(),emits:{"update:modelValue":e=>!0},setup(e,a){let{emit:l,attrs:n}=a
const{textColorClasses:o,textColorStyles:r}=cl(()=>e.color),i=t.ref(),s=t.shallowRef(!1)
function u(e){if(["Backspace","Delete"].includes(e.key)){e.preventDefault()
e.target.value="",l("update:modelValue",null)}}return Bt(()=>t.createElementVNode("div",null,[t.createVNode(Hi,t.mergeProps({ref:i,_as:"VTimePickerField",autocomplete:"off",class:["v-time-picker-controls__time__field",{"v-time-picker-controls__time__field--active":e.active},e.active?o.value:[]],style:e.active?r.value:[],disabled:e.disabled,variant:"solo-filled",inputmode:"numeric",hideDetails:!0,flat:!0,modelValue:e.modelValue??(s.value?"":"--"),"onUpdate:modelValue":e=>l("update:modelValue",e),onKeydown:u,onFocus:()=>s.value=!0,onBlur:()=>s.value=!1},n),null),t.createElementVNode("div",{class:"v-time-picker-controls__field-label"},[e.label])])),wo({},i)}})
function sg(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:2
return String(e).padStart(t,"0")}function ug(e){return e?(e-1)%12+1:12}function cg(e,t){return e%12+("pm"===t?12:0)}function dg(e){const t=e.replaceAll(/\D/g,"")
return t.length>0?Number(t):null}function vg(e,t){return 59===e&&t?0:0!==e||t?e+(t?1:-1):59}const pg=vt({ampm:Boolean,color:String,disabled:Boolean,hour:[Number,String],minute:[Number,String],second:[Number,String],period:String,readonly:Boolean,useSeconds:Boolean,value:Number,viewMode:String},"VTimePickerControls"),mg=wt()({name:"VTimePickerControls",props:pg(),emits:{"update:period":e=>!0,"update:viewMode":e=>!0,"update:hour":e=>!0,"update:minute":e=>!0,"update:second":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const{t:o}=ma(),r=t=>{if(null==t||isNaN(Number(t)))return null
const a=Number(t)
return e.ampm?sg(ug(a)):sg(a)},i=t=>{if(isNaN(Number(t))||null==t||""===t)return null
const a="string"==typeof t?dg(t):Number(t)
return null===a?null:e.ampm?cg(a,e.period??"am"):F(a,0,23)},s=la(e,"hour",void 0,r,i),u=e=>null==e||isNaN(Number(e))?null:sg(`${e}`),c=e=>{if(isNaN(Number(e))||null==e||""===e)return null
const t="string"==typeof e?dg(e):Number(e)
return null!==t?F(t,0,59):null},d=la(e,"minute",void 0,u,c),v=la(e,"second",void 0,u,c)
function p(t){if(!["ArrowUp","ArrowDown"].includes(t.key))return
t.preventDefault(),t.stopPropagation()
const a=Number(s.value??0),n=e.ampm?e.period??"am":null,{value:o,togglePeriod:r}=function(e,t,a){if(a){if(12===e&&t)return{value:1}
if(11===e&&t)return{value:12,togglePeriod:!0}
if(12===e&&!t)return{value:11,togglePeriod:!0}
if(1===e&&!t)return{value:12}}else{if(23===e&&t)return{value:0}
if(0===e&&!t)return{value:23}}return{value:e+(t?1:-1)}}(a,"ArrowUp"===t.key,n)
s.value=sg(o),r&&l("update:period","am"===e.period?"pm":"am")}function m(e){["ArrowUp","ArrowDown"].includes(e.key)&&(e.preventDefault(),e.stopPropagation(),d.value=vg(Number(d.value),"ArrowUp"===e.key))}function f(e){["ArrowUp","ArrowDown"].includes(e.key)&&(e.preventDefault(),e.stopPropagation(),v.value=vg(Number(v.value),"ArrowUp"===e.key))}function g(t,a,l){return n=>{if(!n.data)return
const o=n.target,{value:r,selectionStart:i,selectionEnd:s}=o??{}
if(null===dg(n.data))return void n.preventDefault()
const u=r?r.slice(0,i)+n.data+r.slice(s):n.data
if(u.length>2){if(i===s&&0===s&&n.data.trim().startsWith("0"))return n.preventDefault(),o.value=u.trim().substring(0,2),l(o.value),void(1===n.data.trim().length&&o.setSelectionRange(1,1))
if(i===s&&1===s&&r.startsWith("0"))return n.preventDefault(),o.value=u.trim().substring(0,2),void l(o.value)
const t="hour"===e.viewMode?e.ampm?12:23:59
if(dg(u)>t)return n.preventDefault(),o.value=sg(String(dg(n.data)).substring(0,2)),void l(o.value)}const c=t(u)
a(c)&&n.preventDefault()}}const h=t.ref(),y=t.ref(),b=t.ref()
t.watch(()=>e.viewMode,(e,t)=>{switch(t){case"hour":h.value.blur()
break
case"minute":y.value.blur()
break
case"second":b.value.blur()}})
const V=g(i,e=>r(e)===s.value,e=>s.value=e),w=g(c,e=>u(e)===d.value,e=>d.value=e),k=g(c,e=>u(e)===v.value,e=>v.value=e)
return Bt(()=>t.createElementVNode("div",{class:"v-time-picker-controls"},[t.createElementVNode("div",{class:t.normalizeClass({"v-time-picker-controls__time":!0,"v-time-picker-controls__time--with-ampm":e.ampm,"v-time-picker-controls__time--with-seconds":e.useSeconds})},[t.createVNode(ig,{ref:h,active:"hour"===e.viewMode,color:e.color,disabled:e.disabled,label:o("$vuetify.timePicker.hour"),modelValue:s.value,"onUpdate:modelValue":e=>s.value=e,onKeydown:p,onBeforeinput:V,onFocus:()=>l("update:viewMode","hour")},null),t.createElementVNode("span",{class:"v-time-picker-controls__time__separator"},[t.createTextVNode(":")]),t.createVNode(ig,{ref:y,active:"minute"===e.viewMode,color:e.color,disabled:e.disabled,label:o("$vuetify.timePicker.minute"),modelValue:d.value,"onUpdate:modelValue":e=>d.value=e,onKeydown:m,onBeforeinput:w,onFocus:()=>l("update:viewMode","minute")},null),e.useSeconds&&t.createElementVNode("span",{key:"secondsDivider",class:"v-time-picker-controls__time__separator"},[t.createTextVNode(":")]),e.useSeconds&&t.createVNode(ig,{key:"secondsVal",ref:b,active:"second"===e.viewMode,color:e.color,disabled:e.disabled,label:o("$vuetify.timePicker.second"),modelValue:v.value,"onUpdate:modelValue":e=>v.value=e,onKeydown:f,onBeforeinput:k,onFocus:()=>l("update:viewMode","second")},null),e.ampm&&t.createElementVNode("div",{class:"v-time-picker-controls__ampm"},[t.createVNode($n,{active:"am"===e.period,color:"am"===e.period?e.color:void 0,class:t.normalizeClass({"v-time-picker-controls__ampm__am":!0,"v-time-picker-controls__ampm__btn":!0,"v-time-picker-controls__ampm__btn__active":"am"===e.period}),disabled:e.disabled,text:o("$vuetify.timePicker.am"),variant:e.disabled&&"am"===e.period?"elevated":"tonal",onClick:()=>"am"!==e.period?l("update:period","am"):null},null),t.createVNode($n,{active:"pm"===e.period,color:"pm"===e.period?e.color:void 0,class:t.normalizeClass({"v-time-picker-controls__ampm__pm":!0,"v-time-picker-controls__ampm__btn":!0,"v-time-picker-controls__ampm__btn__active":"pm"===e.period}),disabled:e.disabled,text:o("$vuetify.timePicker.pm"),variant:e.disabled&&"pm"===e.period?"elevated":"tonal",onClick:()=>"pm"!==e.period?l("update:period","pm"):null},null)])])])),{}}}),fg=y(24),gg=y(12),hg=gg.map(e=>e+12)
y(60)
const yg=vt({allowedHours:[Function,Array],allowedMinutes:[Function,Array],allowedSeconds:[Function,Array],disabled:Boolean,format:{type:String,default:"ampm"},max:String,min:String,viewMode:{type:String,default:"hour"},period:{type:String,default:"am",validator:e=>["am","pm"].includes(e)},modelValue:null,readonly:Boolean,scrollable:Boolean,useSeconds:Boolean,variant:{type:String,default:"dial"},...I(dd({title:"$vuetify.timePicker.title"}),["landscape"]),...Tl()},"VTimePicker"),bg=wt()({name:"VTimePicker",props:yg(),emits:{"update:hour":e=>!0,"update:minute":e=>!0,"update:period":e=>!0,"update:second":e=>!0,"update:modelValue":e=>!0,"update:viewMode":e=>!0},setup(e,a){let{emit:l,slots:n}=a
const{t:o}=ma(),{densityClasses:r}=Bl(e),i=t.ref(null),s=t.ref(null),u=t.ref(null),c=t.ref(null),d=t.ref(null),v=t.ref(null),p=la(e,"period","am"),m=la(e,"viewMode","hour"),f=t.ref(null),g=t.ref(null),h=t.computed(()=>{let t
if(t=e.allowedHours instanceof Array?t=>e.allowedHours.includes(t):e.allowedHours,!e.min&&!e.max)return t
const a=e.min?Number(e.min.split(":")[0]):0,l=e.max?Number(e.max.split(":")[0]):23
return e=>e>=Number(a)&&e<=Number(l)&&(!t||t(e))}),y=t.computed(()=>{let t
const a=!h.value||null===i.value||h.value(i.value)
if(t=e.allowedMinutes instanceof Array?t=>e.allowedMinutes.includes(t):e.allowedMinutes,!e.min&&!e.max)return a?t:()=>!1
const[l,n]=e.min?e.min.split(":").map(Number):[0,0],[o,r]=e.max?e.max.split(":").map(Number):[23,59],s=60*l+Number(n),u=60*o+Number(r)
return e=>{const l=60*i.value+e
return l>=s&&l<=u&&a&&(!t||t(e))}}),b=t.computed(()=>{let t
const a=(!h.value||null===i.value||h.value(i.value))&&(!y.value||null===s.value||y.value(s.value))
if(t=e.allowedSeconds instanceof Array?t=>e.allowedSeconds.includes(t):e.allowedSeconds,!e.min&&!e.max)return a?t:()=>!1
const[l,n,o]=e.min?e.min.split(":").map(Number):[0,0,0],[r,u,c]=e.max?e.max.split(":").map(Number):[23,59,59],d=3600*l+60*n+Number(o||0),v=3600*r+60*u+Number(c||0)
return e=>{const l=3600*i.value+60*s.value+e
return l>=d&&l<=v&&a&&(!t||t(e))}}),V=t.computed(()=>"ampm"===e.format),w=t.toRef(()=>null!==e.modelValue&&null===i.value&&null===s.value&&(!e.useSeconds||null===u.value))
function k(){const t=S()
null!==t&&t!==e.modelValue&&l("update:modelValue",t),w.value&&l("update:modelValue",null)}function S(){return null==i.value||null==s.value||e.useSeconds&&null==u.value?null:`${sg(i.value)}:${sg(s.value)}`+(e.useSeconds?`:${sg(u.value)}`:"")}function x(e){if(null==e||""===e)i.value=null,s.value=null,u.value=null
else if(e instanceof Date)i.value=e.getHours(),s.value=e.getMinutes(),u.value=e.getSeconds()
else{const[t,,a,,l,n]=e.trim().toLowerCase().match(/^(\d+):(\d+)(:(\d+))?([ap]m)?$/)||new Array(6)
i.value=n?cg(parseInt(t,10),n):parseInt(t,10),s.value=parseInt(a,10),u.value=parseInt(l||0,10)}p.value=null==i.value||i.value<12?"am":"pm"}function N(e){if(p.value=e,null!=i.value){const e=i.value+("am"===p.value?-12:12)
i.value=function(e,t){const a=h.value
if(!a)return t
const l=V.value?t<12?gg:hg:fg
return((l.find(e=>a((e+t)%l.length+l[0]))||0)+t)%l.length+l[0]}(0,e)}return l("update:period",e),k(),!0}function C(e){"hour"===m.value?i.value=V.value?cg(e,p.value):e:"minute"===m.value?s.value=e:u.value=e}function E(t){switch(m.value||"hour"){case"hour":l("update:hour",t)
break
case"minute":l("update:minute",t)
break
case"second":l("update:second",t)}const a=null!==i.value&&null!==s.value&&(!e.useSeconds||null!==u.value)
if("hour"===m.value?m.value="minute":e.useSeconds&&"minute"===m.value&&(m.value="second"),i.value===c.value&&s.value===d.value&&(!e.useSeconds||u.value===v.value))return
null!==S()&&(c.value=i.value,d.value=s.value,e.useSeconds&&(v.value=u.value),a&&k())}t.watch(i,k),t.watch(s,k),t.watch(u,k),t.watch(()=>e.period,e=>N(e)),t.watch(()=>e.modelValue,e=>x(e)),t.watch(()=>e.useSeconds,(e,t)=>{t&&!e&&"second"===m.value&&(m.value="minute"),e||null===u.value||(u.value=null)}),t.onMounted(()=>{x(e.modelValue)}),Bt(()=>{const a=I(vd.filterProps(e),["hideHeader"]),l=mg.filterProps(e),c=og.filterProps(I(e,["format","modelValue","min","max"]))
return t.createVNode(vd,t.mergeProps(a,{color:void 0,class:["v-time-picker",`v-time-picker--variant-${e.variant}`,e.class,r.value],hideHeader:e.hideHeader&&"input"!==e.variant,style:e.style}),{title:()=>n.title?.()??t.createElementVNode("div",{class:"v-time-picker__title"},[o(e.title)]),header:()=>t.createVNode(mg,t.mergeProps(l,{ampm:V.value,hour:i.value,minute:s.value,period:p.value,second:u.value,viewMode:m.value,"onUpdate:hour":e=>i.value=e,"onUpdate:minute":e=>s.value=e,"onUpdate:period":e=>N(e),"onUpdate:second":e=>u.value=e,"onUpdate:viewMode":e=>m.value=e,ref:f}),null),default:()=>t.createVNode(og,t.mergeProps(c,{allowedValues:"hour"===m.value?h.value:"minute"===m.value?y.value:b.value,double:"hour"===m.value&&!V.value,format:"hour"===m.value?V.value?ug:e=>e:e=>sg(e,2),max:"hour"===m.value?V.value&&"am"===p.value?11:23:59,min:"hour"===m.value&&V.value&&"pm"===p.value?12:0,size:20,step:"hour"===m.value?1:5,modelValue:"hour"===m.value?i.value:"minute"===m.value?s.value:u.value,onChange:E,onInput:C,ref:g}),null),actions:n.actions})})}}),Vg=vt({...pt(),...$l({variant:"text"})},"VToolbarItems"),wg=wt()({name:"VToolbarItems",props:Vg(),setup(e,a){let{slots:l}=a
return yt({VBtn:{color:t.toRef(()=>e.color),height:"inherit",variant:t.toRef(()=>e.variant)}}),Bt(()=>t.createElementVNode("div",{class:t.normalizeClass(["v-toolbar-items",e.class]),style:t.normalizeStyle(e.style)},[l.default?.()])),{}}}),kg=vt({id:String,interactive:Boolean,text:String,...I(Ei({closeOnBack:!1,location:"end",locationStrategy:"connected",eager:!0,minWidth:0,offset:10,openOnClick:!1,openOnHover:!0,origin:"auto",scrim:!1,scrollStrategy:"reposition",transition:null}),["absolute","retainFocus","captureFocus","disableInitialFocus"])},"VTooltip"),Sg=wt()({name:"VTooltip",props:kg(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a
const n=la(e,"modelValue"),{scopeId:o}=yi(),r=t.useId(),i=t.toRef(()=>e.id||`v-tooltip-${r}`),s=t.ref(),u=t.computed(()=>e.location.split(" ").length>1?e.location:e.location+" center"),c=t.computed(()=>"auto"===e.origin||"overlap"===e.origin||e.origin.split(" ").length>1||e.location.split(" ").length>1?e.origin:e.origin+" center"),d=t.toRef(()=>null!=e.transition?e.transition:n.value?"scale-transition":"fade-transition"),v=t.computed(()=>t.mergeProps({"aria-describedby":i.value},e.activatorProps))
return Bt(()=>{const a=Ii.filterProps(e)
return t.createVNode(Ii,t.mergeProps({ref:s,class:["v-tooltip",{"v-tooltip--interactive":e.interactive},e.class],style:e.style,id:i.value},a,{modelValue:n.value,"onUpdate:modelValue":e=>n.value=e,transition:d.value,absolute:!0,location:u.value,origin:c.value,role:"tooltip",activatorProps:v.value,_disableGlobalStack:!0},o),{activator:l.activator,default:function(){for(var t=arguments.length,a=new Array(t),n=0;n<t;n++)a[n]=arguments[n]
return l.default?.(...a)??e.text}})}),wo({},s)}}),xg=vt({...I(hr({collapseIcon:"$treeviewCollapse",expandIcon:"$treeviewExpand"}),["subgroup"])},"VTreeviewGroup"),Ng=wt()({name:"VTreeviewGroup",props:xg(),setup(e,a){let{slots:l}=a
const n=t.ref(),o=t.computed(()=>n.value?.isOpen?e.collapseIcon:e.expandIcon),r=t.computed(()=>({VTreeviewItem:{prependIcon:void 0,appendIcon:void 0,toggleIcon:o.value}}))
return Bt(()=>{const a=yr.filterProps(e)
return t.createVNode(yr,t.mergeProps(a,{ref:n,class:["v-treeview-group",e.class],subgroup:!0}),{...l,activator:l.activator?e=>t.createElementVNode(t.Fragment,null,[t.createVNode(nl,{defaults:r.value},{default:()=>[l.activator?.(e)]})]):void 0})}),{}}}),Cg=Symbol.for("vuetify:v-treeview"),Eg=vt({loading:Boolean,hideActions:Boolean,hasCustomPrepend:Boolean,indentLines:Array,toggleIcon:Dt,...kr({slim:!0})},"VTreeviewItem"),Ig=wt()({name:"VTreeviewItem",props:Eg(),emits:{toggleExpand:e=>!0},setup(e,a){let{slots:l,emit:n}=a
const o=t.inject(Cg,{visibleIds:t.ref()}).visibleIds,r=t.ref(),i=t.computed(()=>r.value?.root.activatable.value&&r.value?.isGroupActivator),s=t.computed(()=>r.value?.link.isClickable.value||null!=e.value&&!!r.value?.list),u=t.computed(()=>!e.disabled&&!1!==e.link&&(e.link||s.value||i.value)),c=t.computed(()=>o.value&&!o.value.has(t.toRaw(r.value?.id)))
function d(e){u.value&&i.value&&r.value?.activate(!r.value?.isActivated,e)}function v(e){e.preventDefault(),e.stopPropagation(),n("toggleExpand",e)}return Bt(()=>{const a=Sr.filterProps(e),n=l.prepend||e.toggleIcon||e.indentLines||e.prependIcon||e.prependAvatar
return t.createVNode(Sr,t.mergeProps({ref:r},a,{active:r.value?.isActivated||void 0,class:["v-treeview-item",{"v-treeview-item--activatable-group-activator":i.value,"v-treeview-item--filtered":c.value},e.class],ripple:!1,onClick:d}),{...l,prepend:n?a=>t.createElementVNode(t.Fragment,null,[e.indentLines&&e.indentLines.length>0?t.createElementVNode("div",{key:"indent-lines",class:"v-treeview-indent-lines",style:{"--v-indent-parts":e.indentLines.length}},[e.indentLines.map(e=>t.createElementVNode("div",{class:t.normalizeClass(`v-treeview-indent-line v-treeview-indent-line--${e}`)},null))]):"",!e.hideActions&&t.createVNode(Or,{start:!0},{default:()=>[e.toggleIcon?t.createElementVNode(t.Fragment,null,[l.toggle?t.createVNode(nl,{key:"prepend-defaults",defaults:{VBtn:{density:"compact",icon:e.toggleIcon,variant:"text",loading:e.loading},VProgressCircular:{indeterminate:"disable-shrink",size:20,width:2}}},{default:()=>[l.toggle({...a,loading:e.loading,props:{onClick:v}})]}):t.createVNode($n,{key:"prepend-toggle",density:"compact",icon:e.toggleIcon,loading:e.loading,variant:"text",onClick:v},{loader:()=>t.createVNode(an,{indeterminate:"disable-shrink",size:"20",width:"2"},null)})]):t.createElementVNode("div",{class:"v-treeview-item__level"},null)]}),e.hasCustomPrepend?t.createVNode(nl,{key:"prepend-defaults",defaults:{VAvatar:{density:e.density,image:e.appendAvatar},VIcon:{density:e.density,icon:e.appendIcon},VListItemAction:{start:!0}}},{default:()=>[l.prepend?.(a)]}):t.createElementVNode(t.Fragment,null,[l.prepend?.(a),e.prependAvatar&&t.createVNode(Kn,{key:"prepend-avatar",density:e.density,image:e.prependAvatar},null),e.prependIcon&&t.createVNode(Jl,{key:"prepend-icon",density:e.density,icon:e.prependIcon},null)])]):void 0})}),wo({},r)}}),_g=vt({fluid:Boolean,disabled:Boolean,loadChildren:Function,loadingIcon:{type:String,default:"$loading"},items:Array,openOnClick:{type:Boolean,default:void 0},indeterminateIcon:{type:Dt,default:"$checkboxIndeterminate"},falseIcon:Dt,trueIcon:Dt,returnObject:Boolean,activatable:Boolean,selectable:Boolean,selectedColor:String,selectStrategy:[String,Function,Object],index:Number,isLastGroup:Boolean,separateRoots:Boolean,parentIndentLines:Array,indentLinesVariant:String,path:{type:Array,default:()=>[]},...C(Eg(),["hideActions"]),...Tl()},"VTreeviewChildren"),Pg=wt()({name:"VTreeviewChildren",props:_g(),setup(e,a){let{slots:l}=a
const n=t.reactive(new Set),o=t.ref([]),r=t.computed(()=>!e.disabled&&(null!=e.openOnClick?e.openOnClick:e.selectable&&!e.activatable))
async function i(t){try{if(!e.items?.length||!e.loadChildren)return
0===t?.children?.length&&(n.add(t.value),await e.loadChildren(t.raw))}finally{n.delete(t.value)}}function s(t,a){e.selectable&&t(a)}return()=>l.default?.()??e.items?.map((a,u,c)=>{const{children:d,props:v}=a,p=n.has(a.value),m=!!c.at(u+1)?.children,f=e.path?.length??0,g=c.length-1===u,h={index:u,depth:f,isFirst:0===u,isLast:g,path:[...e.path,u],hideAction:e.hideActions},y=function(e){let{depth:t,isLast:a,isLastGroup:l,leafLinks:n,separateRoots:o,parentIndentLines:r,variant:i}=e
const s=a&&(!l||o||t>1)
return r&&t?"simple"===i?{leaf:[...r,"line"],node:[...r,"line"],children:[...r,"line"],footer:[...r,"line","line"]}:{leaf:[...r,s?"last-leaf":"leaf",...n?["leaf-link"]:[]],node:[...r,s?"last-leaf":"leaf"],children:[...r,s?"none":"line"],footer:[...r,s?"none":"line"]}:{leaf:void 0,node:void 0,children:r,footer:!r||s&&"simple"!==i?["none"]:[...r,o?"none":"line"]}}({depth:f,isLast:g,isLastGroup:e.isLastGroup,leafLinks:!e.hideActions&&!e.fluid,separateRoots:e.separateRoots,parentIndentLines:e.parentIndentLines,variant:e.indentLinesVariant}),b={toggle:l.toggle?e=>l.toggle?.({...e,...h,item:a.raw,internalItem:a,loading:p}):void 0,prepend:n=>t.createElementVNode(t.Fragment,null,[e.selectable&&(!d||d&&!["leaf","single-leaf"].includes(e.selectStrategy))&&t.createVNode(Or,{start:!0},{default:()=>[t.createVNode(no,{key:a.value,modelValue:n.isSelected,disabled:e.disabled||v.disabled,loading:p,color:e.selectedColor,density:e.density,indeterminate:n.isIndeterminate,indeterminateIcon:e.indeterminateIcon,falseIcon:e.falseIcon,trueIcon:e.trueIcon,"onUpdate:modelValue":e=>s(n.select,e),onClick:e=>e.stopPropagation(),onKeydown:e=>{["Enter","Space"].includes(e.key)&&(e.stopPropagation(),s(n.select,n.isSelected))}},null)]}),l.prepend?.({...n,...h,item:a.raw,internalItem:a})]),append:l.append?e=>l.append?.({...e,...h,item:a.raw,internalItem:a}):void 0,title:l.title?e=>l.title?.({...e,item:a.raw,internalItem:a}):void 0,subtitle:l.subtitle?e=>l.subtitle?.({...e,item:a.raw,internalItem:a}):void 0},V=Ng.filterProps(v),w=Pg.filterProps({...e,...h}),k={hideActions:e.hideActions,indentLines:y.footer}
return d?t.createVNode(Ng,t.mergeProps(V,{value:e.returnObject?a.raw:V?.value,rawId:V?.value}),{activator:n=>{let{props:c}=n
const d={...v,...c,value:v?.value,hideActions:e.hideActions,indentLines:y.node,onToggleExpand:[()=>i(a),c.onClick],onClick:e.disabled||v.disabled?void 0:r.value?[()=>i(a),c.onClick]:()=>s(o.value[u]?.select,!o.value[u]?.isSelected)}
return ie(l.header,{props:d,item:a.raw,internalItem:a,loading:p},()=>t.createVNode(Ig,t.mergeProps({ref:e=>o.value[u]=e},d,{hasCustomPrepend:!!l.prepend,value:e.returnObject?a.raw:v.value,loading:p}),b))},default:()=>t.createElementVNode(t.Fragment,null,[t.createVNode(Pg,t.mergeProps(w,{items:d,indentLinesVariant:e.indentLinesVariant,parentIndentLines:y.children,isLastGroup:m,returnObject:e.returnObject}),l),l.footer?.({props:k,item:a.raw,internalItem:a,loading:p})])}):ie(l.item,{props:v,item:a.raw,internalItem:a},()=>"divider"===a.type?ie(l.divider,{props:a.raw},()=>t.createVNode(Jo,a.props,null)):"subheader"===a.type?ie(l.subheader,{props:a.raw},()=>t.createVNode(Nr,a.props,null)):t.createVNode(Ig,t.mergeProps(v,{hasCustomPrepend:!!l.prepend,hideActions:e.hideActions,indentLines:y.leaf,value:e.returnObject?t.toRaw(a.raw):v.value}),b))})}})
function Ag(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[]
for(const a of e)t.push(a),a.children&&Ag(a.children,t)
return t}const Rg=vt({openAll:Boolean,indentLines:[Boolean,String],search:String,hideNoData:Boolean,noDataText:{type:String,default:"$vuetify.noDataText"},...ns({filterKeys:["title"]}),...I(_g(),["index","path","indentLinesVariant","parentIndentLines","isLastGroup"]),...I($r({collapseIcon:"$treeviewCollapse",expandIcon:"$treeviewExpand",slim:!0}),["nav","openStrategy"]),modelValue:Array},"VTreeview"),Tg=wt()({name:"VTreeview",props:Rg(),emits:{"update:opened":e=>!0,"update:activated":e=>!0,"update:selected":e=>!0,"update:modelValue":e=>!0,"click:open":e=>!0,"click:select":e=>!0},setup(e,a){let{slots:l,emit:n}=a
const{t:o}=ma(),{items:r}=Fr(e),i=t.toRef(()=>e.activeColor),s=t.toRef(()=>e.baseColor),u=t.toRef(()=>e.color),c=la(e,"activated"),d=la(e,"selected"),v=t.computed({get:()=>e.modelValue??d.value,set(e){d.value=e,n("update:modelValue",e)}}),p=t.ref(),m=t.computed(()=>e.openAll?V(r.value):e.opened),f=t.computed(()=>Ag(r.value)),g=t.toRef(()=>e.search),{filteredItems:h}=os(e,f,g),y=t.computed(()=>{if(!g.value)return null
const a=p.value?.getPath
return a?new Set(h.value.flatMap(l=>{const n=e.returnObject?l.raw:l.props.value
return[...a(n),...b(n)].map(t.toRaw)})):null})
function b(e){const t=[],a=(p.value?.children.get(e)??[]).slice()
for(;a.length;){const e=a.shift()
e&&(t.push(e),a.push(...(p.value?.children.get(e)??[]).slice()))}return t}function V(a){let l=[]
for(const n of a)n.children&&(l.push(e.returnObject?t.toRaw(n.raw):n.value),n.children&&(l=l.concat(V(n.children))))
return l}return t.provide(Cg,{visibleIds:y}),yt({VTreeviewGroup:{activeColor:i,baseColor:s,color:u,collapseIcon:t.toRef(()=>e.collapseIcon),expandIcon:t.toRef(()=>e.expandIcon)},VTreeviewItem:{activeClass:t.toRef(()=>e.activeClass),activeColor:i,baseColor:s,color:u,density:t.toRef(()=>e.density),disabled:t.toRef(()=>e.disabled),lines:t.toRef(()=>e.lines),variant:t.toRef(()=>e.variant)}}),Bt(()=>{const a=Mr.filterProps(e),n=Pg.filterProps(e),i="boolean"==typeof e.indentLines?"default":e.indentLines
return t.createVNode(Mr,t.mergeProps({ref:p},a,{class:["v-treeview",{"v-treeview--fluid":e.fluid},e.class],openStrategy:"multiple",style:e.style,opened:m.value,activated:c.value,"onUpdate:activated":e=>c.value=e,selected:v.value,"onUpdate:selected":e=>v.value=e}),{default:()=>[0===y.value?.size&&!e.hideNoData&&(l["no-data"]?.()??t.createVNode(Sr,{key:"no-data",title:o(e.noDataText)},null)),t.createVNode(Pg,t.mergeProps(n,{density:e.density,returnObject:e.returnObject,items:r.value,parentIndentLines:e.indentLines?[]:void 0,indentLinesVariant:i}),l)]})}),{}}}),Bg=wt()({name:"VValidation",props:fo(),emits:{"update:modelValue":e=>!0},setup(e,t){let{slots:a}=t
const l=go(e,"validation")
return()=>a.default?.(l)}})
var Dg=Object.freeze({__proto__:null,VAlert:Un,VAlertTitle:On,VApp:_a,VAppBar:Al,VAppBarNavIcon:zn,VAppBarTitle:Ln,VAutocomplete:ss,VAvatar:Kn,VBadge:cs,VBanner:fs,VBannerActions:vs,VBannerText:ps,VBottomNavigation:hs,VBottomSheet:ws,VBreadcrumbs:Es,VBreadcrumbsDivider:Ss,VBreadcrumbsItem:Ns,VBtn:$n,VBtnGroup:Ll,VBtnToggle:Kl,VCalendar:pc,VCard:xc,VCardActions:fc,VCardItem:Vc,VCardSubtitle:hc,VCardText:kc,VCardTitle:yc,VCarousel:Rc,VCarouselItem:Fc,VCheckbox:So,VCheckboxBtn:no,VChip:Xo,VChipGroup:Ko,VClassIcon:Ot,VCode:$c,VCol:Xv,VColorPicker:pd,VCombobox:fd,VComponentIcon:Mt,VConfirmEdit:hd,VContainer:jv,VCounter:Ri,VDataIterator:Jd,VDataTable:Fv,VDataTableFooter:lv,VDataTableHeaders:kv,VDataTableRow:Cv,VDataTableRows:Iv,VDataTableServer:Lv,VDataTableVirtual:Mv,VDatePicker:Ip,VDatePickerControls:gp,VDatePickerHeader:yp,VDatePickerMonth:kp,VDatePickerMonths:xp,VDatePickerYears:Cp,VDefaultsProvider:nl,VDialog:bs,VDialogBottomTransition:Ha,VDialogTopTransition:Wa,VDialogTransition:za,VDivider:Jo,VEmptyState:Pp,VExpandTransition:tl,VExpandXTransition:al,VExpansionPanel:$p,VExpansionPanelText:Tp,VExpansionPanelTitle:Dp,VExpansionPanels:Lp,VFab:jp,VFabTransition:ja,VFadeTransition:Ya,VField:$i,VFieldLabel:Bi,VFileInput:Gp,VFooter:qp,VForm:Zp,VHotkey:im,VHover:um,VIcon:Jl,VImg:Vl,VInfiniteScroll:vm,VInput:yo,VItem:gm,VItemGroup:fm,VKbd:Jp,VLabel:Xn,VLayout:ym,VLayoutItem:Vm,VLazy:km,VLigatureIcon:Lt,VList:Mr,VListGroup:yr,VListImg:zr,VListItem:Sr,VListItemAction:Or,VListItemMedia:Hr,VListItemSubtitle:Vr,VListItemTitle:wr,VListSubheader:Nr,VLocaleProvider:xm,VMain:Cm,VMenu:Pi,VMessages:io,VNavigationDrawer:Tm,VNoSsr:Bm,VNumberInput:Fm,VOtpInput:Mm,VOverlay:Ii,VPagination:tv,VParallax:Lm,VProgressCircular:an,VProgressLinear:un,VRadio:jm,VRadioGroup:Wm,VRangeSlider:Um,VRating:Km,VResponsive:sl,VRow:pp,VScaleTransition:Ua,VScrollXReverseTransition:Ka,VScrollXTransition:Ga,VScrollYReverseTransition:Xa,VScrollYTransition:qa,VSelect:ts,VSelectionControl:ao,VSelectionControlGroup:eo,VSheet:cd,VSkeletonLoader:tf,VSlideGroup:Yo,VSlideGroupItem:af,VSlideXReverseTransition:Qa,VSlideXTransition:Za,VSlideYReverseTransition:el,VSlideYTransition:Ja,VSlider:ad,VSnackbar:nf,VSnackbarQueue:rf,VSpacer:mp,VSparkline:yf,VSpeedDial:Vf,VStepper:Bf,VStepperActions:Sf,VStepperHeader:xf,VStepperItem:Ef,VStepperWindow:_f,VStepperWindowItem:Af,VSvgIcon:zt,VSwitch:Ff,VSystemBar:Mf,VTab:Of,VTable:Pv,VTabs:Gf,VTabsWindow:Hf,VTabsWindowItem:Yf,VTextField:Hi,VTextarea:qf,VThemeProvider:Zf,VTimePicker:bg,VTimePickerClock:og,VTimePickerControls:mg,VTimeline:lg,VTimelineItem:tg,VToolbar:El,VToolbarItems:wg,VToolbarTitle:Ra,VTooltip:Sg,VTreeview:Tg,VTreeviewGroup:Ng,VTreeviewItem:Ig,VValidation:Bg,VVirtualScroll:qi,VWindow:Pc,VWindowItem:Bc})
function Fg(e,t){e._mutate?.[t.instance.$.uid]&&(e._mutate[t.instance.$.uid].observer.disconnect(),delete e._mutate[t.instance.$.uid])}const $g={mounted:function(e,t){const a=t.modifiers||{},l=t.value,{once:n,immediate:o,...r}=a,i=!Object.keys(r).length,{handler:s,options:u}="object"==typeof l?l:{handler:l,options:{attributes:r?.attr??i,characterData:r?.char??i,childList:r?.child??i,subtree:r?.sub??i}},c=new MutationObserver(function(){let a=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[],l=arguments.length>1?arguments[1]:void 0
s?.(a,l),n&&Fg(e,t)})
o&&s?.([],c),e._mutate=Object(e._mutate),e._mutate[t.instance.$.uid]={observer:c},c.observe(e,u)},unmounted:Fg}
function Mg(e,t){const{self:a=!1}=t.modifiers??{},l=t.value,n="object"==typeof l&&l.options||{passive:!0},o="function"==typeof l||"handleEvent"in l?l:l.handler,r=a?e:t.arg?document.querySelector(t.arg):window
r&&(r.addEventListener("scroll",o,n),e._onScroll=Object(e._onScroll),e._onScroll[t.instance.$.uid]={handler:o,options:n,target:a?void 0:r})}function zg(e,t){if(!e._onScroll?.[t.instance.$.uid])return
const{handler:a,options:l,target:n=e}=e._onScroll[t.instance.$.uid]
n.removeEventListener("scroll",a,l),delete e._onScroll[t.instance.$.uid]}const Lg={mounted:Mg,unmounted:zg,updated:function(e,t){t.value!==t.oldValue&&(zg(e,t),Mg(e,t))}}
const Og=function(e,a){const n=function(e,a){return function(n,o,r){const i="function"==typeof a?a(o):a,s=o.value?.text??o.value??i?.text,u=V(o.value)?o.value:{},c=()=>s??n.textContent,d=(r.ctx===o.instance.$?function(e,t){const a=new Set,n=t=>{for(const l of t){if(!l)continue
if(l===e||l.el&&e.el&&l.el===e.el)return!0
let t
if(a.add(l),l.suspense?t=n([l.ssContent]):Array.isArray(l.children)?t=n(l.children):l.component?.vnode&&(t=n([l.component?.subTree])),t)return t
a.delete(l)}return!1}
if(!n([t.subTree]))return l("Could not find original vnode, component will not inherit provides"),t
const o=Array.from(a).reverse()
for(const e of o)if(e.component)return e.component
return t}(r,o.instance.$)?.provides:r.ctx?.provides)??o.instance.$.provides,v=t.h(e,t.mergeProps(i,u),c)
v.appContext=Object.assign(Object.create(null),o.instance.$.appContext,{provides:d}),t.render(v,n)}}("string"==typeof e?t.resolveComponent(e):e,a)
return{mounted:n,updated:n,unmounted(e){t.render(null,e)}}}(Sg,e=>({activator:(V(e.value)?!e.value.text:["",!1,null].includes(e.value))?null:"parent",location:e.arg?.replace("-"," "),text:"boolean"==typeof e.value?void 0:e.value}))
var jg=Object.freeze({__proto__:null,ClickOutside:Ni,Intersect:yl,Mutate:$g,Resize:Bu,Ripple:Dn,Scroll:Lg,Tooltip:Og,Touch:Cc})
function Hg(e){const t={svg:{component:zt},class:{component:Ot}},a=e?.defaultSet??"mdi"
return"mdi"!==a||t.mdi||(t.mdi=Ht),O({defaultSet:a,sets:t,aliases:{...jt,vuetify:["M8.2241 14.2009L12 21L22 3H14.4459L8.2241 14.2009Z",["M7.26303 12.4733L7.00113 12L2 3H12.5261C12.5261 3 12.5261 3 12.5261 3L7.26303 12.4733Z",.6]],"vuetify-outline":"svg:M7.26 12.47 12.53 3H2L7.26 12.47ZM14.45 3 8.22 14.2 12 21 22 3H14.45ZM18.6 5 12 16.88 10.51 14.2 15.62 5ZM7.26 8.35 5.4 5H9.13L7.26 8.35Z","vuetify-play":["m6.376 13.184-4.11-7.192C1.505 4.66 2.467 3 4.003 3h8.532l-.953 1.576-.006.01-.396.677c-.429.732-.214 1.507.194 2.015.404.503 1.092.878 1.869.806a3.72 3.72 0 0 1 1.005.022c.276.053.434.143.523.237.138.146.38.635-.25 2.09-.893 1.63-1.553 1.722-1.847 1.677-.213-.033-.468-.158-.756-.406a4.95 4.95 0 0 1-.8-.927c-.39-.564-1.04-.84-1.66-.846-.625-.006-1.316.27-1.693.921l-.478.826-.911 1.506Z",["M9.093 11.552c.046-.079.144-.15.32-.148a.53.53 0 0 1 .43.207c.285.414.636.847 1.046 1.2.405.35.914.662 1.516.754 1.334.205 2.502-.698 3.48-2.495l.014-.028.013-.03c.687-1.574.774-2.852-.005-3.675-.37-.391-.861-.586-1.333-.676a5.243 5.243 0 0 0-1.447-.044c-.173.016-.393-.073-.54-.257-.145-.18-.127-.316-.082-.392l.393-.672L14.287 3h5.71c1.536 0 2.499 1.659 1.737 2.992l-7.997 13.996c-.768 1.344-2.706 1.344-3.473 0l-3.037-5.314 1.377-2.278.004-.006.004-.007.481-.831Z",.6]]}},e)}function Wg(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}
const{blueprint:a,...l}=e,n=O(a,l),{aliases:r={},components:i={},directives:s={}}=n,u=t.effectScope()
return u.run(()=>{const e=function(e){return t.ref(e)}(n.defaults),a=Po(n.display,n.ssr),l=Na(n.theme),c=Hg(n.icons),d=pa(n.locale),v=function(e,t){const a=O({adapter:xu,locale:{af:"af-ZA",bg:"bg-BG",ca:"ca-ES",ckb:"",cs:"cs-CZ",de:"de-DE",el:"el-GR",en:"en-US",et:"et-EE",fa:"fa-IR",fi:"fi-FI",hr:"hr-HR",hu:"hu-HU",he:"he-IL",id:"id-ID",it:"it-IT",ja:"ja-JP",ko:"ko-KR",lv:"lv-LV",lt:"lt-LT",nl:"nl-NL",no:"no-NO",pl:"pl-PL",pt:"pt-PT",ro:"ro-RO",ru:"ru-RU",sk:"sk-SK",sl:"sl-SI",srCyrl:"sr-SP",srLatn:"sr-SP",sv:"sv-SE",th:"th-TH",tr:"tr-TR",az:"az-AZ",uk:"uk-UA",vi:"vi-VN",zhHans:"zh-CN",zhHant:"zh-TW"}},e)
return{options:a,instance:Iu(a,t)}}(n.date,d),p=function(e,t){return{rtl:t.isRtl,options:O(Bo(),e)}}(n.goTo,d)
return{install:function(u){for(const e in s)u.directive(e,s[e])
for(const e in i)u.component(e,i[e])
for(const e in r)u.component(e,Vt({...r[e],name:e,aliasName:r[e].name}))
const m=t.effectScope()
if(m.run(()=>{l.install(u)}),u.onUnmount(()=>m.stop()),u.provide(gt,e),u.provide(No,a),u.provide(ha,l),u.provide(Ft,c),u.provide(va,d),u.provide(Nu,v.options),u.provide(Cu,v.instance),u.provide(To,p),o&&n.ssr)if(u.$nuxt)u.$nuxt.hook("app:suspense:resolve",()=>{a.update()})
else{const{mount:e}=u
u.mount=function(){const l=e(...arguments)
return t.nextTick(()=>a.update()),u.mount=e,l}}("boolean"!=typeof __VUE_OPTIONS_API__||__VUE_OPTIONS_API__)&&u.mixin({computed:{$vuetify(){return t.reactive({defaults:Yg.call(this,gt),display:Yg.call(this,No),theme:Yg.call(this,ha),icons:Yg.call(this,Ft),locale:Yg.call(this,va),date:Yg.call(this,Cu)})}}})},unmount:function(){u.stop()},defaults:e,display:a,theme:l,icons:c,locale:d,date:v,goTo:p}})}function Yg(e){const t=this.$,a=t.parent?.provides??t.vnode.appContext?.provides
if(a&&e in a)return a[e]}Wg.version="3.11.8"
const Ug=function(){return Wg({components:Dg,directives:jg,...arguments.length>0&&void 0!==arguments[0]?arguments[0]:{}})},Gg="3.11.8"
Ug.version=Gg,e.blueprints=Gt,e.components=Dg,e.createVuetify=Ug,e.directives=jg,e.useDate=_u,e.useDefaults=function(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=arguments.length>1?arguments[1]:void 0
const{props:a,provideSubDefaults:l}=bt(e,t)
return l(),a},e.useDisplay=Ro,e.useGoTo=Mo,e.useHotkey=function(e,a){let l=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{}
if(!o)return function(){}
const{event:n="keydown",inputs:r=!1,preventDefault:i=!0,sequenceTimeout:s=1e3}=l,u=navigator?.userAgent?.includes("Macintosh")??!1
let c,d=0,v=!1,p=0
function m(){p=0,clearTimeout(d)}function f(e){const l=c[p]
if(l&&!function(){if(t.toValue(r))return!1
const e=document.activeElement
return e&&("INPUT"===e.tagName||"TEXTAREA"===e.tagName||e.isContentEditable||"true"===e.contentEditable)}())if(function(e,t,a){const{modifiers:l,actualKey:n}=function(e){const t=["ctrl","shift","alt","meta","cmd"],{keys:a}=Lu(e.toLowerCase())
if(0===a.length)return{modifiers:Object.fromEntries(t.map(e=>[e,!1])),actualKey:void 0}
const l=Object.fromEntries(t.map(e=>[e,!1]))
let n
for(const e of a)t.includes(e)?l[e]=!0:n=e
return{modifiers:l,actualKey:n}}(t),o=l.ctrl||!a&&(l.cmd||l.meta),r=a&&(l.cmd||l.meta)
return e.ctrlKey===o&&e.metaKey===r&&e.shiftKey===l.shift&&e.altKey===l.alt&&e.key.toLowerCase()===n?.toLowerCase()}(e,l,u))if(t.toValue(i)&&e.preventDefault(),v){if(clearTimeout(d),p++,p===c.length)return a(e),void m()
d=window.setTimeout(m,t.toValue(s))}else a(e)
else v&&m()}function g(){window.removeEventListener(t.toValue(n),f),clearTimeout(d)}return t.watch(()=>t.toValue(e),e=>{if(g(),e){const a=Ou(e.toLowerCase())
v=a.length>1,c=a,m(),window.addEventListener(t.toValue(n),f)}},{immediate:!0}),t.watch(()=>t.toValue(n),(e,t)=>{t&&c&&c.length>0&&(window.removeEventListener(t,f),window.addEventListener(e,f))}),t.onScopeDispose(g,!0),g},e.useLayout=Jt,e.useLocale=ma,e.useMask=function(e){const a=t.computed(()=>"string"==typeof e.mask?e.mask in ju?ju[e.mask]:e.mask:e.mask?.mask??""),l=t.computed(()=>({...Hu,...V(e.mask)?e.mask.tokens:null}))
function n(e){return e in l.value}function o(e,t){if(null==t||!n(e))return!1
const a=l.value[e]
return a.pattern?a.pattern.test(t):a.test(t)}function r(e,t){const a=l.value[e]
return a.convert?a.convert(t):t}function i(e){const t=e?.trim().replace(/\s+/g," ")
if(null==t)return""
if(!a.value.length||!t.length)return t
let l=0,i=0,s=""
for(;i<a.value.length;){const e=a.value[i],u=t[l]
if("\\"!==e){if(n(e)){if(!o(e,u))break
s+=r(e,u),l++}else s+=e,u===e&&l++
i++}else s+=a.value[i+1],i+=2}return s}function s(e){if(null==e)return null
if(!a.value.length||!e.length)return e
let t=0,l=0,n=""
for(;;){const r=a.value[l],i=e[t]
if(null==i)break
if(null!=r)if("\\"!==r)if(o(r,i))n+=i,t++,l++
else if(r===i)t++,l++
else for(;;){const e=a.value[l++]
if(null==e||o(e,i))break}else i===a.value[l+1]&&t++,l+=2
else n+=i,t++}return n}function u(e){return!!e&&s(e)===s(i(e))}return{isValid:u,isComplete:function(e){return!!e&&(i(e).length===a.value.length&&u(e))},mask:i,unmask:s}},e.useRtl=ga,e.useTheme=Ea,e.version=Gg})
//# sourceMappingURL=vuetify.min.js.map
