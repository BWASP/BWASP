from flask_restx import fields
import json


class StringToJSON(fields.Raw):
    def format(self, value):
        return value
