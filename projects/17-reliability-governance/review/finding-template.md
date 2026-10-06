# Writing a finding that gets fixed

A good finding is **specific, evidenced, and asks for one thing**. Template:

> **What:** <the fact, with numbers: "AnyErrors on positions-api paged 41 times last week; 2 were actionable">
> **Impact:** <why it matters: "≈ 6 hours of on-call interruption; real issues get missed in the noise">
> **Ask:** <one concrete change: "delete it, or change it to a burn-rate alert on positions-api's SLO">
> **Owner / due:** <team, date>
> **Help offered:** <what SRE will do: "we'll pair on the new rule on Tuesday">

Bad: "positions-api alerting is noisy, please improve."
