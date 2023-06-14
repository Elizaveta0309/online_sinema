from abc import ABC, abstractmethod


class MainStorage(ABC):
    @abstractmethod
    def get_event(self):
        """Get mailing list."""

    @abstractmethod
    def update_event(self):
        """Update mailing list."""
