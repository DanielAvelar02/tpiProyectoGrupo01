var staticCacheName = 'djangopwa-v3';

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(staticCacheName).then(function(cache) {
            return cache.addAll([
                '/',
                '/static/manifest.json',
                '/static/images/favicon.png',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
                'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
                'https://code.jquery.com/jquery-3.5.1.slim.min.js',
                'https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js',
                'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js'
            ]);
        })
    );
});

self.addEventListener('activate', function(event) {
    var cacheWhitelist = [staticCacheName];
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request)
            .then(function(response) {
                // Si la solicitud fue exitosa, la almacenamos en caché
                if (response.status === 200) {
                    const responseClone = response.clone();
                    caches.open(staticCacheName)
                        .then(function(cache) {
                            cache.put(event.request, responseClone);
                        });
                }
                return response;
            })
            .catch(function() {
                // Si falla la solicitud, intentamos recuperarla del caché
                return caches.match(event.request)
                    .then(function(response) {
                        return response || caches.match('/');
                    });
            })
    );
});