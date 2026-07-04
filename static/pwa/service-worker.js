self.addEventListener('install', function(event) {
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('push', function(event) {
  var data = {};
  if (event.data) {
    try { data = event.data.json(); } catch (error) { data = {title: 'تنبيه', body: event.data.text()}; }
  }
  var title = data.title || 'تنبيه من المذكر اليومي';
  var options = {
    body: data.body || 'لديك تنبيه جديد.',
    icon: '/static/img/logo.jpg',
    badge: '/static/img/logo.jpg',
    dir: 'rtl',
    lang: 'ar',
    data: { url: data.url || '/' }
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  var url = event.notification.data && event.notification.data.url ? event.notification.data.url : '/';
  event.waitUntil(clients.matchAll({type: 'window', includeUncontrolled: true}).then(function(clientList) {
    for (var i = 0; i < clientList.length; i++) {
      var client = clientList[i];
      if ('focus' in client) {
        client.navigate(url);
        return client.focus();
      }
    }
    if (clients.openWindow) { return clients.openWindow(url); }
  }));
});
