from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

import unicodedata


class TechOfferFilterView(BrowserView):
    """ Filtered content search view for every folder. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.query =  self._format_query(self.request.form.get('q', ''))

        self.tags = self.request.form.get('t', '') or []
        if self.tags:
            self.tags = self.tags.split(',')

    def get_content(self, filtered=True):
        catalog = getToolByName(self.context, 'portal_catalog')

        kw = {}
        if filtered:
            if self.tags:
                kw['Subject'] = {'query': self.tags, 'operator': 'and'}
            if self.query:
                kw['SearchableText'] = self.query
    
        return catalog(portal_type="TechOffer", sort_on='getObjPositionInParent', **kw)
    
    def get_tags(self):
        tags = []
        for res in self.get_content(filtered=False):
            tags += list(set(res.Subject))

        listTags = list(dict.fromkeys(tags))
        listTags.sort(key=lambda key: unicodedata.normalize('NFKD', key).encode('ascii', errors='ignore'))

        return listTags

    def get_container_path(self):
        return self.context.absolute_url() + '/techoffer_filter_query'

    def _format_query(self, query):
        if not query:
            return ''

        multispace = u'　'
        for char in ('?', '-', '+', '*', multispace):
            query = query.replace(char, ' ')

        r_query = query.split()
        r_query = " AND ".join(r_query)

        bad_chars = ["(", ")"]
        for char in bad_chars:
            r_query = r_query.replace(char, f'"{char}"')
        r_query = r_query + '*'

        return r_query