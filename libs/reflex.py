import re
from libs.errors import KeywordSyntaxError
import importlib


class ReactData:

    def __init__(self, text):
        self.text = text

    def _get_variable(self):
        r = re.findall(r"\$\{(.*)\}$", self.text, re.I | re.M)
        if len(r) == 1:
            return r

    def reflex_variable(self):
        text = self.text
        if isinstance(text, str) is False:
            return text
        text_vars = self._get_variable()
        if text_vars:
            for var in text_vars:
                s_text = var.split('|')
                if len(s_text) > 1:
                    arg_find = re.findall(r"\((.*)\)$", ''.join(s_text[: -1]), re.I | re.M)
                    if len(arg_find) > 1:
                        raise KeywordSyntaxError
                    try:
                        mod = importlib.import_module(s_text[-1])
                        func_text = "{}.{}".format("mod", s_text[0])
                        value = eval(func_text)
                        sub_str = '${%s}' % var
                        text = str(text).replace(sub_str, value)
                    except ModuleNotFoundError:
                        raise KeywordSyntaxError
        return text