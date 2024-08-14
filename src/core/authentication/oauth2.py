from authlib.integrations.starlette_client import OAuth
from starlette.config import Config


class VdreamOAuth(OAuth):
    name = 'google'
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration'
    client_kwargs = {'scope': 'openid profile email'}
    GOOGLE_CLIENT_ID = None
    GOOGLE_CLIENT_SECRET = None
    GOOGLE_REDIRECT_URI = None
    _oauth = None

    def __init__(self, **kwargs):
        self.GOOGLE_CLIENT_ID = kwargs.get("GOOGLE_CLIENT_ID")
        self.GOOGLE_CLIENT_SECRET = kwargs.get("GOOGLE_CLIENT_SECRET")
        self.GOOGLE_REDIRECT_URI = kwargs.get("GOOGLE_REDIRECT_URI")

        starlette_config = Config(
            environ={'GOOGLE_CLIENT_ID': self.GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': self.GOOGLE_CLIENT_SECRET})
        super().__init__(starlette_config)
        self.register(name=self.name, server_metadata_url=self.server_metadata_url, client_kwargs=self.client_kwargs)

    async def redirect_url(self, request):
        return await self.google.authorize_redirect(request, self.GOOGLE_REDIRECT_URI)

    async def callback_url(self, request):
        return await self.google.authorize_access_token(request)
