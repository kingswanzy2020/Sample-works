from toil.actions.cert_expiry import CertExpiry
from toil.actions.disk_cleanup import DiskCleanup
from toil.actions.market_readiness import MarketReadiness
from toil.actions.restart_stuck_consumer import RestartStuckConsumer

ALL = [CertExpiry(), MarketReadiness(), RestartStuckConsumer(), DiskCleanup()]
