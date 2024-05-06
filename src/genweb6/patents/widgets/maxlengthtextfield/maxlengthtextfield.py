# -*- coding: utf-8 -*-
from zope.interface import implementer_only

import z3c.form.browser.text
import z3c.form.interfaces
import z3c.form.widget
import zope.schema.interfaces

from genweb6.patents import _


class IMaxLengthTextFieldWidget(z3c.form.interfaces.ITextWidget):
    pass


@implementer_only(IMaxLengthTextFieldWidget)
class MaxLengthTextFieldWidget(z3c.form.browser.text.TextWidget):
    klass = u'maxlengthtext-widget'

    def update(self):
        super().update()
        z3c.form.browser.widget.addFieldClass(self)

        self.max_length = self.field.max_length
        self.max_length_exceeded_text = _(
            "max_length_exceeded",
            default=u"Maximum length of ${max} characters exceeded.",
            mapping={'max': self.max_length}
        )
