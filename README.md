# Implementation order (frontend only)

App shell, routes, auth provider

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

# new checklist

Frontend Blueprint (UX + Structure)
A. Global Layout & Navigation
Header (persistent)

Left: Propalyze logo → /

Center: Global Search (single input with “Address / Property URL / ID”).

CTA: “Search”

Optional “Advanced filters” icon → opens Filters Drawer (city, BHK, budget, property type)

Right:

“About”, “Contact” (simple links)

Auth area

If logged out: “Login” / “Sign up”

If logged in: avatar dropdown → “User Portal”, “Admin” (if role=admin), “Logout”

Mobile: collapse center/right into a hamburger menu; search stays visible.

Footer (persistent)

Brief tagline

Links: About, Contact, Terms, Privacy

Disclaimer

Global UI Patterns

Loader (centered spinner)

Toast (success/error)

ConfirmDialog (for destructive admin actions)

EmptyState (no results, errors with retry)

ErrorBoundary around routes

Skeletons for charts/cards while loading

B. Home (Landing) /

Purpose: short story + launchpad. No duplicate navbar links—this is a showcase.

Hero block

Headline: “Propalyze — AI for smarter real estate decisions”

Subhead: one-liner value prop

Primary CTA: “Search a property”

Secondary CTAs: “Estimate price”, “Analyze locality”

Feature grid (cards)

6 feature cards → link to: Price Estimator / Investment Advisor / Locality Analyzer / Smart Location Suggestor / Risk Checker / Compare Properties

Each card: icon + short description + “Open”

How it works

3 steps: Search → Analyze → Decide (1–2 sentences each)

Insights (optional, when backend ready)

“Trending localities” list (top 5)

“Market snapshot” mini chart (last 12 months average)

Trust

Short disclaimer + small logos (optional)

C. Search /search

Purpose: the fastest way to jump into a property or area.

Top bar search (same as header, duplicated here centered & larger)

Input supports: MagicBricks/99acres URL, internal Property ID, or free-text address

“Advanced filters” drawer:

City (autocomplete), BHK, Budget min/max, Property type, Furnishing, Age

Results

Left column (filters): chips + toggles, “Reset filters”

Right column (list):

PropertyCard per result:
thumbnail, price, BHK, area, price/sqft, locality, badges (Verified/Risky), quick actions:

“Estimate Price”

“Analyze Locality”

“Compare” (adds to compare tray)

Compare Tray (sticky bottom when ≥1 selected): shows selected items with “Compare Now”

Empty / error states with guidance (“Try a broader search”, “Paste a property URL”).

D. Price Estimator /price-estimator

Two-column layout.

Left: Form

City (autocomplete), Locality (dependent), Property Type, BHK, Area, Furnishing, Builder (optional), Age (optional)

Buttons: “Estimate Price”, “Reset”

Right: Result (after submit)

PriceRangeCard: “₹X – ₹Y” + confidence %

“Model insight” bullets (e.g., important features)

Mini line chart: local price trend (12 months)

Actions: “Analyze this locality”, “Compare with another property”

E. Investment Advisor /investment-advisor

Form row: City, Locality, Property Type, Horizon (1–5y), “Forecast”

Output

ChartCard: Line chart (history + forecast with confidence band)

Stats row: CAGR, median forecast, downside case

Narrative: short interpretation + disclaimer

If insufficient data → show “Not enough history” empty state.

F. Locality Analyzer /locality-analysis

Input

Either City + Locality or lat/lon (hidden by default, “Use coordinates” toggle)

“Analyze”

Output (cards grid)

Amenity Proximity: counts + top 3 nearest (schools, hospitals, transit, groceries)

Environment: AQI, humidity, temperature (and noise/mosquito if available)

Commute (optional): distance/time to a typed landmark

Livability Score: aggregate with sub-scores (safety/connectivity/environment)

Actions: “Suggest properties here”, “Track locality”

G. Smart Location Suggestor /smart-location-suggestor

Filters

Budget range, Property Type, Preferred City, Min Yield %, Growth Potential (Low/Med/High)

“Suggest”

Results

LocalityCard list: name, city, avg price/sqft, rental yield, growth score, quick actions (“View listings”, “Analyze”)

H. Risk Checker /risk-checker

Input

Property URL or ID

“Check risk”

Output

Verdict badge: Low / Suspicious / Unknown

Flags list (rule hits & anomaly explanations)

Evidence snippets (e.g., “Price < 30% of area median”)

Action: “Compare with similar”, “Report listing” (optional)

I. Compare Properties /compare-property

Selectors

Two search inputs (URL/ID), with inline result preview

“Swap” button

Comparison

Header summary: two PriceRangeCards side-by-side

Table sections:

Basics (BHK, area, price, price/sqft)

Locality (scores, amenities)

Financials (estimated fair price vs asking, yield, age)

Media (small gallery)

“Save comparison” (if logged in)

J. User Portal /user

Tabs

Saved Searches

Alerts (create/update/delete: e.g., “Notify me if price < ₹80L”)

Bookmarks (properties/localities)

Settings (password, logout)

Each tab: list with empty states & actions.

K. Admin Panel /admin (protected)

Dashboard

Cards: total properties, total cities, last sync

Small chart: listings/day last week

Data Updater

Buttons: Update All, Update City (select), Update Locality (select city → locality)

Show progress state (queued/running/completed)

Logs

Paginated table: time, type, message, status

Filters: error/warn/info

L. Auth /login, /signup

Login

Username/Email, Password, “Remember me”

On submit → POST /api/login

Backend sets HttpOnly refresh cookie

Backend may also set short-lived access cookie or return access token in JSON (your call)

After login → fetch /api/me to get user object; store in AuthContext (in-memory)

Signup

Basic fields → POST /api/signup, then auto-login or redirect to /login

Logout

Call /api/logout (backend clears cookies), clear in-memory user state.

Reusable Components (no styling specifics, just behavior & props)

Button, Input, Select, Checkbox, Range – controlled form elements

SearchBar

props: placeholder, onSearch, withAdvanced

behavior: Enter key triggers search, “Advanced” toggles drawer

FeatureCard – title, description, icon, onClick

PropertyCard – shows listing summary + actions

LocalityCard – stats + actions

StatCard – label + value (+ delta)

ChartCard – wraps Recharts line/area bar charts

Tabs – controlled active key

Table – sortable header, empty state, pagination

Toast – global notifications (success/error/info)

Modal / Drawer – for filters and confirms

Loader / Skeleton – generic loading indicators

EmptyState – message + optional retry action

Badge/Chip – for status (Risky, Verified, New)

Data & State Flow (your chosen approach: “normal method”)

You prefer no React Query and no global Axios instance. We can still keep things clean with a small request helper (not an Axios instance) and local component state.

Minimal request helper (fetch with credentials)
// src/utils/request.js
export async function request(path, options = {}) {
const res = await fetch(`http://localhost:8000/api${path}`, {
credentials: "include", // send cookies
headers: { "Content-Type": "application/json", ...(options.headers || {}) },
...options,
});
if (!res.ok) {
const message = await res.text().catch(() => res.statusText);
throw new Error(message || `HTTP ${res.status}`);
}
const isJSON = res.headers.get("content-type")?.includes("application/json");
return isJSON ? res.json() : res.text();
}

Use it directly in components with useState/useEffect.

No global Axios, no custom hooks folder required.

In a page (example)
// inside a component
const [cities, setCities] = useState([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");

useEffect(() => {
let cancelled = false;
setLoading(true);
request("/cities")
.then(data => { if (!cancelled) setCities(data); })
.catch(err => { if (!cancelled) setError(err.message); })
.finally(() => !cancelled && setLoading(false));
return () => { cancelled = true; };
}, []);

Auth (cookie-based)

On app start, call /api/me to populate AuthContext.user

Use credentials: "include" everywhere; backend reads cookies.

For protected pages, a PrivateRoute checks user (or shows Loader until /api/me resolves).

File Structure (no hooks folder, simple & scalable)

Interaction Details & States (important for a polished feel)

All forms:

Disable submit while loading

Inline field errors (required/malformed input)

Top-level error banner on network failure

Success toast on completion

Charts (Recharts):

Show Skeleton while loading

Empty chart message if no points

Tooltip + legend, responsive container

Lists & tables:

Pagination (client or server), sortable columns where useful

EmptyState with “Try adjusting filters”

Compare: prevent submit until 2 valid selections

Admin: All actions confirm via ConfirmDialog; show background “task running” status.

Accessibility:

Proper <label htmlFor> on inputs

Keyboard focus states, escape to close modals

aria-live="polite" on toasts
