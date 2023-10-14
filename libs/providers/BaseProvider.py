import traceback
from enum import Enum

import openai
import requests

from libs.tools.logger import LogType, log


class Status(Enum):
    NORMAL = 0
    ERR = 1


class StdSignal(object):
    def __init__(self, content, stat: Status = Status.NORMAL):
        self.content = content
        self.stat = stat


class BaseProvider(object):
    def __init__(self, api_host: str, api_key: str = "", name: str = "", system_prompt: str = ""):
        self.name = name
        self.api_host = "https://" + api_host + "/v1"
        self.api_key = api_keypip install python-lsp-server
        self.models = None
        self.context = [{"role": "system", "content": system_prompt}]
        self.refresh_provider_info()

    def refresh_provider_info(self):
        try:
            self.get_models()
            openai.api_base = self.api_host
            openai.api_key = self.api_key
        except:
            log(traceback.format_exc(), LogType.ERROR)
            log("Failed to refresh provider info!", LogType.WARN)

    def get_models(self):
        self.models = requests.get(self.api_host + "/models",
                                   headers={"Authorization": "Bearer " + self.api_key}).json()

    def send_message(self, message: str, model_name: str = "gpt-3.5-turbo", stream: bool = True):
        if message is not None and not message == "":
            self._send_message(message, model_name, stream)

    def _send_message(self, message: str, model_name: str = "gpt-3.5-turbo", stream: bool = True) -> StdSignal:
        self.refresh_provider_info()
        try:
            reply = ""
            self.context.append(
                "role": "user", "content": message})
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=self.context,
                stream=stream
            )
            for chunk in response:
                try:
                    reply += chunk.choices[0].delta.content
                except AttributeError:
                    self.context.append({'role': 'assistant', 'content': str(reply)})
            return StdSignal()
        except openai.error.APIError:
            return StdSignal("很抱歉，出错了！\n您的OpenAI API返回了一个错误！\n" + traceback.format_exc(), Status.ERR)
        except openai.error.InvalidRequestError:
            return StdSignal(
                "很抱歉，出错了！\n您可能没有选择模型又或者是你的API不支持你选择的模型！\n" + traceback.format_exc(),
                Status.ERR)
        except openai.error.APIConnectionError:
            return StdSignal(
                "很抱歉，出错了！\n您的OpenAI API可能格式有误或不存在，请检查您的API地址。\n如果API地址确认无误，但您仍然能看到这个错误窗口，那么请询问API提供者！\n" +
                traceback.format_exc(), Status.ERR)
        except openai.error.AuthenticationError:
            return StdSignal(
                "很抱歉，出错了！\n您的API Key可能有误、无效、不存在，又可能是API提供者跑路了。\n如果API Key确认无误，但您仍然能看到这个错误窗口，那么请询问API提供者！\n" +
                traceback.format_exc(), Status.ERR)
        except Exception:
            return StdSignal(
                "很抱歉，出错了！\n您的API Key可能有误、无效、不存在，又可能是API提供者跑路了。\n如果API Key确认无误，但您仍然能看到这个错误窗口，那么请询问API提供者！\n" +
                traceback.format_exc(), Status.ERR)

    def clear_context(self):
        self.context = [self.context[0]]
