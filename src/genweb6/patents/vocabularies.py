# -*- coding: utf-8 -*-


from genweb6.patents import _
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import implementer


patent_status_vocabulary = SimpleVocabulary([
    SimpleTerm(value="Not possibility of patent", title=_("Not possibility of patent")),
    SimpleTerm(value="Pending of protection", title=_("Pending of protection")),
    SimpleTerm(value="Applied patent", title=_("Applied patent")),
    SimpleTerm(value="PCT application", title=_("PCT application")),
    SimpleTerm(value="Approved patent", title=_("Approved patent")),
    SimpleTerm(value="Denied patent", title=_("Denied patent")),
    SimpleTerm(value="Other forms of protection", title=_("Other forms of protection")),
    SimpleTerm(value="Industrial secret", title=_("Industrial secret")),
])


business_opportunity_vocabulary = SimpleVocabulary([
    SimpleTerm(
        value="Technology available to be licensed",
        title=_("Technology available to be licensed")
    ),

    SimpleTerm(
        value="Technology available to be licensed with technical cooperation",
        title=_("Technology available to be licensed with technical cooperation")
    ),

    SimpleTerm(
        value="Others",
        title=_("Others")
    )
])


@implementer(IVocabularyFactory)
class PatentStatus:
    def __call__(self, *args, **kwargs):
        return patent_status_vocabulary


@implementer(IVocabularyFactory)
class BusinessOpportunity:
    def __call__(self, *args, **kwargs):
        return business_opportunity_vocabulary
