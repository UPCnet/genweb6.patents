import re
from zope.i18nmessageid.message import MessageFactory

_pl = MessageFactory("plone")


def maxLengthValidatorNoTags(max_length, value):
    filtered = re.sub(r'<[^>]*>', '', value.raw)
    filtered = filtered.replace('\r\n', '').replace('\n', '')
    # True if no validation errors are found (i.e. the length is less than max_length)
    return len(filtered) <= max_length


def maxLegnthNoTagsGeneric(max_length, value, **kwargs):
    if not maxLengthValidatorNoTags(max_length, value):
        return _pl(
                    "msg_text_too_long",
                    default="Text is too long. (Maximum ${max} characters.)",
                    mapping={"max": max_length},
                )


# No se puede validar la longitud maxima de un richtext sin tener en cuenta tags de html
# de otra forma en el easyform. Cada campo de texto que necesite esta validacion debe tener
# su propio validator con la longitud fijada. No se puede hacer un validator generico
# que reciba la longitud como parametro
def maxLengthNoTags500(value, **kwargs):
    return maxLegnthNoTagsGeneric(500, value, **kwargs)


def maxLengthNoTags1500(value, **kwargs):
    return maxLegnthNoTagsGeneric(1500, value, **kwargs)
