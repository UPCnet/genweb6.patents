# -*- coding: utf-8 -*-
import re
from genweb6.patents import _
from zope.i18nmessageid.message import MessageFactory
from plone.app.dexterity import textindexer
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from plone.dexterity.interfaces import IDexteritySchema

from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import implementer, invariant, Invalid  # noqa F401


def max_length_validator(max_length):
    _pl = MessageFactory("plone")

    def validator(value):
        filtered = re.sub(r'<[^>]*>', '', value.raw)
        filtered = filtered.replace('\r\n', '').replace('\n', '')
        if len(filtered) > max_length:
            raise Invalid(
                _pl(
                    "msg_text_too_long",
                    default="Text is too long. (Maximum ${max} characters.)",
                    mapping={"max": max_length},
                )
            )
        return True

    return validator


class ITechOffer(model.Schema, IDexteritySchema):
    textindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Title"),
        description=u"",
        required=True
    )

    textindexer.searchable('description')
    description = schema.Text(
        title=_(u"Description"),
        description=u"",
        required=False
    )

    textindexer.searchable('ref_num')
    ref_num = schema.TextLine(
        title=_(u"Reference number"),
        description=u"",
        required=True,
    )

    textindexer.searchable('challenge')
    challenge = RichText(
        title=_(u"The Challenge"),
        description=_(u"challenge_description"),
        constraint=max_length_validator(1100)
    )

    textindexer.searchable('technology')
    technology = RichText(
        title=_(u"Technology"),
        description=_(u"technology_description"),
        constraint=max_length_validator(850)
    )

    textindexer.searchable('advantages')
    advantages = RichText(
        title=_(u"Innovative advantages"),
        description=_(u"advantages_description"),
        constraint=max_length_validator(1100)
    )

    textindexer.searchable('dev_stage')
    dev_stage = RichText(
        title=_(u"Current stage of development"),
        description=_(u"dev_stage_description"),
        constraint=max_length_validator(450)
    )

    textindexer.searchable('applications')
    applications = RichText(
        title=_(u"Applications and Target Market"),
        description=_(u"applications_description"),
        constraint=max_length_validator(400)
    )

    image = namedfile.NamedBlobImage(
        title=_(u"Lead Image"),
        description=u"",
        required=False,
    )

    image1 = namedfile.NamedBlobImage(
        title=_(u"First picture"),
        required=False
    )
    caption1 = schema.TextLine(
        title=_(u"First picture caption"),
        required=False
    )
    image2 = namedfile.NamedBlobImage(
        title=_(u"Second picture"),
        required=False
    )
    caption2 = schema.TextLine(
        title=_(u"Second image caption"),
        required=False
    )

    opportunity = schema.Choice(
        title=_(u"Business Opportunity"),
        vocabulary="genweb6.patents.vocabularies.business_opportunity"
    )
    other_opportunity = schema.TextLine(
        title=_(u"Specify Business Opportunity"),
        description=_(u"Fill this field if you selected 'Others' for 'Business Opportunity'"),
        required=False
    )

    patent_status = schema.Choice(
        title=_(u"Patent Status"),
        vocabulary="genweb6.patents.vocabularies.patent_status"
    )

    # XXX: Queremos validar esta condición?
    @invariant
    def other_opportunityInvariant(data):
        if not bool(data.other_opportunity) and data.opportunity == "Others":
            raise Invalid(_("'Specify business opportunity' field required when 'Others' is selected"
                            + " for 'Business Opportunity'"))


@implementer(ITechOffer)
class TechOffer(Item):

    @property
    def b_icon_expr(self):
        return "file-earmark-richtext"
