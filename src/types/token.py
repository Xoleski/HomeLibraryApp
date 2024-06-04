from .base import DTO

__all__ = [
    "TokenPairDTO",
    "RefreshTokenDTO",
]


class TokenPairDTO(DTO):
    access_token: str
    refresh_token: str
    token_type: str
    
    
class RefreshTokenDTO(DTO):
    refresh_token: str
