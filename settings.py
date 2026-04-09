from pathlib import Path
from typing import Self

from pydantic import BaseModel, HttpUrl, Field
from pydantic_settings import BaseSettings
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
    
class Webhook(BaseModel):
    """Discord webhook adapter"""
    
    name: str = "MeshMapper"
    """Name of the webhook for messages"""
    
    url: HttpUrl
    """URL of the webhook"""
    
    regions: list[str] | None = None
    """Regions to process, all regions if None"""

class Settings(BaseSettings):
    webhooks: list[Webhook] = Field(default_factory=list)
    
    @classmethod
    def load_settings(cls: type[Self], path: str | Path = Path("config.yaml")) -> Self:
        """Load settings from a yaml config.
    
        Args:
            path: Path to the config file
            
        Return:
            Singleton instance of settings
        """
        path = Path(path)
        if not path.exists():
            raise ValueError(f"Config file not found: {path}")
        with path.open() as f:
            data = yaml.load(f, Loader=Loader)
        return cls(**data)