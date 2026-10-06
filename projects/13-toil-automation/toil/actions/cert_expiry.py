"""Example of a finished, read-only action: report TLS certificates that expire soon."""
import datetime as dt
import socket
import ssl

from toil.framework import Action, Step


class CertExpiry(Action):
    name = "cert-expiry"
    help = "report TLS certificates expiring within N days (read-only)"

    def add_arguments(self, parser):
        parser.add_argument("hosts", nargs="+", help="host[:port] to check")
        parser.add_argument("--days", type=int, default=21)

    def plan(self, args):
        steps = []
        for target in args.hosts:
            host, _, port = target.partition(":")
            try:
                expires = self._expiry(host, int(port or 443))
                left = (expires - dt.datetime.now(dt.UTC)).days
                status = "EXPIRING" if left <= args.days else "ok"
                detail = f"{status}: expires {expires:%Y-%m-%d} ({left} days)"
                steps.append(Step(target, detail, changes_something=False))
            except (OSError, ssl.SSLError) as exc:
                steps.append(Step(target, f"UNKNOWN: {exc}", changes_something=False))
        return steps

    @staticmethod
    def _expiry(host: str, port: int) -> dt.datetime:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as tls:
                not_after = tls.getpeercert()["notAfter"]
        return dt.datetime.fromtimestamp(ssl.cert_time_to_seconds(not_after), dt.UTC)
