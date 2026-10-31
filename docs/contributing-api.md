# Investigating undocumented endpoints

Read before researching API behavior. Never execute writes to discover behavior;
live tests require the user's request and must remain read-only.

1. Start with the relevant HTML: the event host for event features or
   `https://cosplay2.ru/` for portal features. Read inline scripts and `globals`;
   discover current script URLs from the page instead of hard-coding bundle hashes.
2. Search downloaded sources with `rg` for paths and features. Follow AngularJS states,
   `templateUrl`, resolves and `$ocLazyLoad` into `/js/` and `/html/`. Templates may
   contain inline controllers and API calls; no match in a bundle does not prove disuse.
3. Trace `$http.get`, `$http.post` and `$upload.upload` through callers. Confirm methods,
   paths, query/body fields, defaults, omissions and conversions. For forms, inspect
   initialization, `ng-model`, `ng-options`, radios, watchers and submission. For uploads,
   inspect `fileFormDataName`, accompanying data and success handlers. Mirror serialization
   but omit `wid`, added by `poolIdInjector`; do not wrap its `/api/pool/get` poll.
4. Trace response consumers: `$http.then` receives `res.data`, while `.success` receives
   the body. Identify wrapper keys and returned IDs. Extract closed enum sets from
   explicit constants/options in unminified frontend sources, not examples.
5. Compare local HAR bodies when available. Check `response.content.encoding` and decode
   base64 when needed; script bodies may be absent. Read downloaded text as UTF-8.
   Frontend field usage does not guarantee presence in API payloads; unobserved shapes
   stay `Any`.
6. Add offline tests for both clients covering serialization, unwrapping and upload fields.
   Document confirmed behavior, quirks and uncertainty on the relevant `docs/api/` page;
   wire fields and enums belong in `docs/api-schemas.md`. Omit research logs/source registers.

Fetch public assets without local credentials. Use temporary downloads and remove them
afterward. Never commit captures, session data or personal information; use synthetic fixtures.
