# -*- coding: utf-8 -*-
from zope.interface import implementer_only

import z3c.form.browser.text
import z3c.form.interfaces
import z3c.form.widget
import zope.schema.interfaces

from genweb6.patents import _
from genweb6.patents.widgets.maxlengthtextfield.maxlengthtextfield import MaxLengthTextFieldWidget


class IMaxLengthTextAreaFieldWidget(z3c.form.interfaces.ITextWidget):
    pass


@implementer_only(IMaxLengthTextAreaFieldWidget)
class MaxLengthTextAreaFieldWidget(MaxLengthTextFieldWidget):
    pass
