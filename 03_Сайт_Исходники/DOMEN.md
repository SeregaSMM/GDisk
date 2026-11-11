# Перед публикацией: заменить домен

Во всех файлах домен-заглушка — `example.com`. Замените на свой одной командой
из корня папки сайта:

```bash
grep -rl 'example.com' . --include='*.html' --include='*.xml' --include='*.txt' \
  | xargs sed -i 's|example\.com|ваш-домен.рф|g'
```

Проверка, что не осталось:

```bash
grep -rn 'example.com' . || echo "чисто"
```

Где домен встречается: `sitemap.xml`, `robots.txt`, теги `<link rel="canonical">`
и `og:url` в HTML-страницах.

## Что ещё сделать при выкладке

- Включить сжатие gzip/brotli — HTML статьи 147 КБ сжимается примерно в 6 раз.
- Заголовок `Cache-Control` для `assets/*` — они меняются редко, можно ставить `max-age=31536000`.
- Проверить, что `assets/img/*.webp` отдаётся с типом `image/webp`.
