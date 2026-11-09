// يجهز مشروع Android بعد `npx cap add android`
const fs = require('fs');
const path = require('path');
const OLIVE = '#ACB607';

const main = 'android/app/src/main';
const res = path.join(main, 'res');

// 1) الأيقونات
fs.cpSync('resources/res', res, { recursive: true, force: true });

// 2) شاشة الإقلاع: لون واحد بدل شعار Capacitor
const solid = fs.readFileSync('resources/splash-solid.png');
for (const d of fs.readdirSync(res)) {
  if (!d.startsWith('drawable')) continue;
  const f = path.join(res, d, 'splash.png');
  if (fs.existsSync(f)) fs.writeFileSync(f, solid);
}

// 3) AndroidManifest: اتجاه عمودي + صلاحية الاهتزاز
const mf = path.join(main, 'AndroidManifest.xml');
let x = fs.readFileSync(mf, 'utf8');
if (!x.includes('android:screenOrientation')) {
  x = x.replace('<activity', '<activity\n            android:screenOrientation="portrait"');
}
if (!x.includes('android.permission.VIBRATE')) {
  x = x.replace('</manifest>', '    <uses-permission android:name="android.permission.VIBRATE" />\n</manifest>');
}
fs.writeFileSync(mf, x);

// 4) ألوان شريط الحالة وشاشة الإقلاع
const st = path.join(res, 'values/styles.xml');
if (fs.existsSync(st)) {
  let s = fs.readFileSync(st, 'utf8');
  if (!s.includes('android:statusBarColor')) {
    s = s.replace(/(<style name="AppTheme\.NoActionBar"[^>]*>)/,
      `$1\n        <item name="android:statusBarColor">${OLIVE}</item>\n        <item name="android:navigationBarColor">${OLIVE}</item>`);
  }
  if (!s.includes('windowSplashScreenBackground')) {
    s = s.replace(/(<style name="AppTheme\.NoActionBarLaunch"[^>]*parent="Theme\.SplashScreen"[^>]*>)/,
      `$1\n        <item name="windowSplashScreenBackground">${OLIVE}</item>`);
  }
  fs.writeFileSync(st, s);
}
console.log('Android project prepared');
