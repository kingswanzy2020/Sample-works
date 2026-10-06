# Game days

1. Start the landscape: `docker compose up -d --build` in `landscape/`.
2. The **game master** (ideally someone else, or you with a script that hides the choice) runs
   `python gameday/game_master.py run`. Responders don't see the terminal.
3. Responders work from alerts, dashboards and runbooks only, and keep an incident timeline.
4. End with `game_master.py clear`, then `reveal`, and compare the timeline with the injection log.
5. Write the incident record (`incidents/`) and a postmortem.

Solo? Run `run` with a large `--delay-max` in another terminal, then go do something else until an alert reaches you.
