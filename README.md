# Implementation order (frontend only)

App shell, routes, auth provider, Axios instance + interceptors, React Query client.

Metadata endpoints (cities/localities), AutocompleteInput.

Price Estimator page (form, validation, result, navigation to analyzer/compare).

Locality Analyzer (form, map, amenities/weather rendering).

Smart Location Suggestor (form → list).

Compare Properties (inputs → table, gallery).

Investment Advisor (forecast chart + coverage messages).

User Portal (bookmarks, alerts CRUD, settings; optimistic updates).

Admin Panel (summary, updater with job status, logs with pagination).

Error boundary, toasts, accessibility checks, E2E smoke tests.

# check list

App skeleton (CRA) + routing ✅

Global Axios instance + React Query

Auth flows + token strategy decided

Price Estimator UI + mock API + real endpoint

Locality Analyzer + Google Maps integration

Suggest Locations UI

Compare UI

Bookmarks & Alerts UI

Admin: update triggers + logs view

Loading / empty / error states everywhere

Form validation and debounce

Image handling + lazy load

Pagination / infinite scroll

Logging/monitoring & CI build

Security: HTTPS, CSRF + CORS config
