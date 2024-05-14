import httpx

from src.settings import settings


async def fetch_google_user_info(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        token_url = "https://accounts.google.com/o/oauth2/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID.get_secret_value(),
            "client_secret": settings.GOOGLE_CLIENT_SECRET.get_secret_value(),
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        response = await client.post(url=token_url, data=data)
        if response.status_code == httpx.codes.OK:
            access_token = response.json().get("access_token")
            user_info = await client.get(
                url="https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if user_info.status_code == httpx.codes.OK:
                return user_info.json()
            elif user_info.status_code == httpx.codes.BAD_REQUEST:
                raise ValueError("Bad Request: Invalid request parameters")
            else:
                raise ValueError(f"An error occurred: {user_info.status_code}")
        elif response.status_code == httpx.codes.BAD_REQUEST:
            raise ValueError("Bad Request: Invalid request parameters")
        else:
            raise ValueError(f"An error occurred: {response.status_code}")
