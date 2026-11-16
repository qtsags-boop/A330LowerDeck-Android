"""Build the GitHub Pages site (installable web app / PWA) from the Android asset index.html."""
import os, re, shutil, sys
sha = (sys.argv[1] if len(sys.argv) > 1 else 'dev')[:12]
out = '_site'
shutil.rmtree(out, ignore_errors=True); os.makedirs(out + '/icons')
html = open('app/src/main/assets/index.html', encoding='utf-8').read()
head = '''<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#14222e">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="A330 Hầm hàng">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
'''
reg = '''<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
}
if (window.navigator.standalone === true || matchMedia('(display-mode: standalone)').matches) document.documentElement.classList.add('standalone');
</script>
'''
assert '</head>' in html and '</body>' in html
html = html.replace('</head>', head + '</head>', 1)
i = html.rfind('</body>'); html = html[:i] + reg + html[i:]
open(out + '/index.html', 'w', encoding='utf-8').write(html)
open(out + '/sw.js', 'w').write(open('pwa/sw.js').read().replace('__VERSION__', sha))
shutil.copy('pwa/manifest.webmanifest', out)
for f in os.listdir('pwa/icons'): shutil.copy('pwa/icons/' + f, out + '/icons/')
open(out + '/.nojekyll', 'w').close()
print('site built:', sorted(os.listdir(out)), len(html) // 1024, 'KB')
