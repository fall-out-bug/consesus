"""Daemon process implementation."""

import asyncio
import signal
from dataclasses import dataclass

from sdp.daemon.pid_manager import PIDManager


@dataclass(frozen=True)
class DaemonConfig:
    """Configuration for SDP daemon process."""

    watch_enabled: bool = False
    pid_file: str = ".sdp/daemon.pid"
    log_file: str = ".sdp/daemon.log"
    poll_interval: float = 1.0


class Daemon:
    """SDP daemon process for background task execution."""

    def __init__(self, config: DaemonConfig) -> None:
        """Initialize daemon with configuration.

        Args:
            config: Daemon configuration
        """
        self._config = config
        self._running = False
        self._pid_manager = PIDManager(config.pid_file)

    def run(self) -> None:
        """Run daemon event loop."""
        self._running = True

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._shutdown)
        signal.signal(signal.SIGINT, self._shutdown)

        # Main event loop
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            while self._running:
                try:
                    loop.run_until_complete(asyncio.sleep(self._config.poll_interval))
                except KeyboardInterrupt:
                    break
        finally:
            loop.close()
            # Cleanup PID file on exit
            self._pid_manager.remove()

    def _shutdown(self, signum: int, frame) -> None:
        """Handle shutdown signal.

        Args:
            signum: Signal number received
            frame: Current stack frame
        """
        self._running = False
