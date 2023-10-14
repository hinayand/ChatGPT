from libs.providers.BaseProvider import BaseProvider


class OpenAIAPI(BaseProvider):
    def __init__(self, api_host: str, api_key: str = "", name: str = "", system_prompt: str = ""):
        super().__init__(api_host, api_key, name, system_prompt)
