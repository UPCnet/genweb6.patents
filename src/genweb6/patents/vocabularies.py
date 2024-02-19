# -*- coding: utf-8 -*-


from genweb6.patents import _
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import implementer
from zope.component import getUtility
from plone.registry.interfaces import IRegistry


@implementer(IVocabularyFactory)
class PatentStatus:
    def __call__(self, *args, **kwargs):
        terms = []
        registry = getUtility(IRegistry)
        records = registry.get('genweb6.patents.patentStatusValues', None)
        if records:
            for record in records:
                terms.append(SimpleTerm(
                    value=record,
                    title=record
                ))
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class BusinessOpportunity:
    def __call__(self, *args, **kwargs):
        terms = []
        registry = getUtility(IRegistry)
        records = registry.get('genweb6.patents.businessOpportunityValues', None)
        if records:
            for record in records:
                terms.append(SimpleTerm(
                    value=record,
                    title=record
                ))
        terms.append(
            SimpleTerm(
                value="Others",
                title=_("Others")
            )
        )
        return SimpleVocabulary(terms)
