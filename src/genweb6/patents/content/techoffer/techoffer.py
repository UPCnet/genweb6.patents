# -*- coding: utf-8 -*-

from plone.app.contenttypes import _
from plone.app.dexterity import textindexer
from plone.app.textfield import RichText
from plone.dexterity.content import Item

from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from genweb6.patents import _ as _GwP


class ITechOffer(model.Schema):
    # Dublin core adds:
    #   title = schema.TextLine(...)
    #   description = schema.Text(...)

    # textindexer.searchable('title')
    # textindexer.searchable('description')

    textindexer.searchable('ref_num')
    ref_num = schema.TextLine(
        title=_(u"Reference number"),
        description=u"",
        required=True,
    )
    
    category = schema.Choice(
        title=_(u"Category"),
        values=[
            'a',
            'b',
            'c'
        ]
    )

    textindexer.searchable('solution')
    solution = RichText(
        title=_(u"Solution"),
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
        values=[
            "Technology available to be licensed",
            "Technology available to be licensed with technical cooperation",
            "Others"
        ]
    )

    patent_status = schema.Choice(
        title=_(u"Patent Status"),
        values=[
            "Not possibility of patent",
            "Pending of protection",
            "Applied patent",
            "PCT application",
            "Approved patent",
            "Denied patent",
            "Other forms of protection",
            "Industrial secret",
        ]
    )

@implementer(ITechOffer)
class TechOffer(Item):

    @property
    def b_icon_expr(self):
        return "file-earmark-richtext"
