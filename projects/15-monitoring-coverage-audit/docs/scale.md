# What I'd do differently at a different scale

## Now: 8 services
- Which check found the most important gap?

## 10×: ~100 services
- Scanner runs in CI on every catalog change and nightly; results in a dashboard with trends.
- Monitoring-as-code templates per service type, so meeting the standard is the default (project 08).

## 100×: firm-wide
- The standard is versioned and reviewed yearly; exceptions expire automatically.
- Synthetic monitoring from multiple locations, including from trading venues' perspective.

## The one-paragraph version for interviews

>
