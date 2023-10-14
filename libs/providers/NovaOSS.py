import requests

from libs.providers.BaseProvider import BaseProvider
from libs.tools.logger import log, LogType


class NovaOSS(BaseProvider):
    def __init__(self, api_key: str, system_prompt: str = ""):
        super().__init__("api.nova-oss.com", api_key, system_prompt=system_prompt)
        self.credits = 0

    def refresh_provider_info(self):
        super().refresh_provider_info()
        try:
            self.credits = requests.get(
                "https://api.nova-oss.com/v1/account/credits",
                headers={"Authorization": "Bearer " + self.api_key}
            ).json()["credits"]
        except:
            log("Failed to get Nova-OSS Credits")
