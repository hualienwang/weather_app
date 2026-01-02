from fastapi import Header, HTTPException, status

async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header"
        )
    from database import validate_api_key
    if not validate_api_key(x_api_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or inactive API key"
        )
    from database import get_api_key_id
    return get_api_key_id(x_api_key)