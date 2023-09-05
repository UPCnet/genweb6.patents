# -*- coding: utf-8 -*-
from pathlib import Path
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import get_installer
from Products.Five.browser import BrowserView

import unicodedata


class TechOfferFilterView(BrowserView):
    """ Filtered content search view for every folder. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.query = self._format_query(self.request.form.get('q', ''))

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

        return catalog(portal_type="TechOffer", review_state='published', sort_on='getObjPositionInParent', **kw)

    def get_tags(self):
        tags = []
        for res in self.get_content(filtered=False):
            tags += list(set(res.Subject))

        listTags = list(dict.fromkeys(tags))
        listTags.sort(key=lambda key: unicodedata.normalize('NFKD', key).encode('ascii', errors='ignore'))

        return listTags

    def get_container_path(self):
        return self.context.absolute_url() + '/techoffer_filter_query'

    def get_draft_collection_path(self):
        return self.context.absolute_url() + '/technological-offers-to-review'

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


class configure_techoffer(BrowserView):
    """
Configura la pàgina de patents:
    - Crea les carpetes .../patents  (si no existeix)
    - Estableix com a vista de ../patents el filtre de oferta tecnològica
    - Crea el formulari .../patents/create-technological-offer, que s'encarrega de crear ofertes tecnològiques.
        - Si el formulari ja existeix, es sobreescriu (es perden tots els canvis fets)
    """

    def __call__(self):
        tags = (
            "Aerospace",
            "Information and communication technologies (IoT, Networks )",
            "Healthcare",
            "Chemical and materials ",
            "Energy and Environment",
            "Leisure and Entertainment",
            "Food and Agriculture",
            "Supply chain and Logistics",
            "Engineering and Industrial",
            "Construction, Mining and Metals",
            "Semiconductor and Electronics",
            "Automotive and Transportation ",
        )

        qi = get_installer(self.context)

        required_products = ['genweb6.patents', 'collective.easyform', 'collective.easyformplugin.createdx']
        missing_products = list(filter(lambda prod: not qi.is_product_installed(prod), required_products))
        if missing_products:
            return f'Form not created.\nThere are missing products: {missing_products}'

        # La ruta hacia el directorio de este "views.py". Se tiene que tener esto en cuenta
        # en el caso de que se mueva esta vista, porque no se encontrarán los xml de "xml_form_config"
        current_path = Path(__file__).parent

        xml_config_path = current_path / 'xml_form_config'
        with open(xml_config_path / 'FieldsModel.xml', 'r') as f:
            fields_model = f.read()
        with open(xml_config_path / 'ActionModel.xml', 'r') as f:
            actions_model = f.read()

        patents = api.content.get('/ca/nova-patents')
        if not patents:
            patents = api.content.create(
                type='Folder',
                id='nova-patents',
                title='Patents (Nova versió)',
                container=api.content.get('/ca')
            )

        techoffer = patents.get("oferta-tecnologica")
        if not techoffer:
            techoffer = api.content.create(
                type='Folder',
                id='oferta-tecnologica',
                title='Oferta Tecnològica/Technological Offer (Nova versió)',
                container=patents,
                subject=tags
            )

        techoffer.setLayout('techoffer_filter')

        easyform = techoffer.get("create-technological-offer")
        if easyform:
            api.content.delete(easyform)

        easyform = api.content.create(
            type='EasyForm',
            id='create-technological-offer',
            title='Crear Oferta Tecnològica (Create Technological Offer)',
            fields_model=fields_model,
            actions_model=actions_model,
            container=techoffer,
            exclude_from_nav=False,
            thankstitle="Gràcies",
            thanksdescription="S'ha creat una nova oferta tecnològica. Es revisarà el més aviat possible.",
            showAll=False,
            showFields=['title'],
            includeEmpties=True
        )

        collection_query = [
            {
                'i': 'review_state',
                'o': 'plone.app.querystring.operation.selection.any',
                'v': ['esborrany', 'visible']
            },
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.any',
                'v': ['TechOffer']
            }
        ]

        collection = techoffer.get("technological-offers-to-review")
        if collection:
            api.content.delete(collection)

        collection = api.content.create(
            type='Collection',
            id='technological-offers-to-review',
            title='Ofertes tecnològiques per revisar/Technological offers to review',
            query=collection_query,
            container=techoffer,
            exclude_from_nav=True
        )

        import transaction
        transaction.commit()

        return f"Patents are located at {patents.absolute_url()}\n\n" + \
               f"Technological offers are located at {techoffer.absolute_url()}\n\n" + \
               f"Create technological offer form is available at {easyform.absolute_url()}\n\n" + \
               f"Collection of technological offers in draft state is available at {collection.absolute_url()}"
