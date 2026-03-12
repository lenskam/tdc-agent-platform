from typing import Optional
import hashlib
import secrets


def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """
    Hash a password using SHA-256 with salt.
    
    Args:
        password: Plain text password
        salt: Optional salt (generated if not provided)
        
    Returns:
        Tuple of (hashed_password, salt)
    """
    if salt is None:
        salt = secrets.token_hex(16)
    
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return pwd_hash, salt


def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hashed password
        salt: Salt used in hashing
        
    Returns:
        True if password matches, False otherwise
    """
    pwd_hash, _ = hash_password(plain_password, salt)
    return pwd_hash == hashed_password


def generate_random_password(length: int = 16) -> str:
    """
    Generate a random secure password.
    
    Args:
        length: Password length
        
    Returns:
        Random password string
    """
    return secrets.token_urlsafe(length)
