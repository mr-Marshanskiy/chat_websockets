import base64
import secrets

from django.core.files.base import ContentFile


class TypeHandlerService:

    @staticmethod
    def convert_file_to_obj(attachment):
        if not attachment:
            return None
        file_str, file_ext = attachment['data'], attachment['format']
        return ContentFile(
            base64.b64decode(file_str),
            name=f'{secrets.token_hex(8)}.{file_ext}'
        )
