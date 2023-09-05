# -*- coding: utf-8 -*-
from genweb6.patents import _
from plone.app.dexterity import textindexer
from plone.app.textfield import RichText
from plone.dexterity.content import Item

from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import implementer, invariant, Invalid  # noqa F401


class ITechOffer(model.Schema):
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
        max_length=800
    )

    textindexer.searchable('technology')
    technology = RichText(
        title=_(u"Technology"),
        max_length=600
    )

    textindexer.searchable('advantages')
    advantages = RichText(
        title=_(u"Innovative advantages"),
        max_length=1000
    )

    textindexer.searchable('dev_stage')
    dev_stage = RichText(
        title=_(u"Current stage of development"),
        max_length=350
    )

    textindexer.searchable('applications')
    applications = RichText(
        title=_(u"Applications and Target Market"),
        max_length=400
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
        vocabulary="genweb.patents.vocabularies.business_opportunity"
    )
    other_opportunity = schema.TextLine(
        title=_(u"Specify Business Opportunity"),
        description=_(u"Fill this field if you selected 'Others' for 'Business Opportunity'"),
        required=False
    )

    patent_status = schema.Choice(
        title=_(u"Patent Status"),
        vocabulary="genweb.patents.vocabularies.patent_status"
    )

    # XXX: Queremos validar esta condición?
    @invariant
    def other_opportunityInvariant(data):
        if not bool(data.other_opportunity) and data.opportunity == "Others":
            raise Invalid(_("'Specify business opportunity' field required when 'Others' is selected" +
                            " for 'Business Opportunity'"))


@implementer(ITechOffer)
class TechOffer(Item):

    @property
    def b_icon_expr(self):
        return "file-earmark-richtext"
