"""TODO (you): free disk space safely on hosts that are filling up.

Before writing it, ask: should this exist at all? Maybe the fix is log rotation in project 11's baseline role,
in which case the right outcome is deleting this stub (ADR-0003: when not to automate).
"""
from toil.framework import Action


class DiskCleanup(Action):
    name = "disk-cleanup"
    help = "remove known-safe files when disks are nearly full [NOT WRITTEN YET]"

    def plan(self, args):
        raise SystemExit("disk-cleanup: not implemented yet (see the docstring in this file)")
