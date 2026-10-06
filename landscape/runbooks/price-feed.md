# Runbook: price-feed

Last updated: 2024-11-02

If prices are stale, restart the feed handler:

    ssh pricefeed-prod-03 'sudo systemctl restart feedhandler'

If that doesn't work, check ZooKeeper.

Contact: Pieter (team lead)
