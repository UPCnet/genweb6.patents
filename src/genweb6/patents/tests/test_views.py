# -*- coding: utf-8 -*-
import unittest
from genweb6.patents.testing import GENWEB6_PATENTS_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone import api
# from zope.component import getMultiAdapter, getAdapter
from Products.CMFPlone.utils import get_installer
from typing import Literal


class ViewsIntegrationTest(unittest.TestCase):
    layer = GENWEB6_PATENTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.installer = get_installer(self.portal, self.layer['request'])
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(type='Folder', id='ca', title='ca', container=self.portal)
        self.portal.portal_workflow.setDefaultChain('simple_publication_workflow')
        self.maxDiff = None
        self.next_techoffer_num = 1

    def _create_techoffer(self, container=None, title=None, tags=None, state: Literal['draft', 'published'] = 'draft'):
        if not title:
            title = f'TechOffer {self.next_techoffer_num}'
            self.next_techoffer_num = self.next_techoffer_num = 1

        container = container if container is not None else self.portal
        tags = tags if tags is not None else ()

        to = api.content.create(
            type='TechOffer',
            title=title,
            subject=tags,
            container=container,
        )

        if state == 'published':
            api.content.transition(to, transition='publish')

        return to

    def test_configure_techoffer_missing_addons(self):
        self.installer.uninstall_product('collective.easyform')
        self.installer.uninstall_product('collective.easyformplugin.createdx')
        view = api.content.get_view(
            name='configure_techoffer',
            context=self.portal,
            request=self.request
        )
        expected_response = (
            "Form not created.\n"
            + "There are missing products: ['collective.easyform', 'collective.easyformplugin.createdx']"
        )

        # view returned expected response
        self.assertEqual(expected_response, view())
        # no new contents were created
        self.assertIsNone(self.portal['ca'].get('patents-py'))

    def test_configure_techoffer_missing_1_addon(self):
        self.installer.uninstall_product('collective.easyformplugin.createdx')

        view = api.content.get_view(
            name='configure_techoffer',
            context=self.portal,
            request=self.request
        )

        expected_response = "Form not created.\nThere are missing products: ['collective.easyformplugin.createdx']"

        # check that the view returned expected response
        self.assertEqual(expected_response, view())
        # check that no new contents were created
        self.assertIsNone(self.portal['ca'].get('patents-py'))

    def test_configure_techoffer_success(self):
        view = api.content.get_view(
            name='configure_techoffer',
            context=self.portal,
            request=self.request
        )

        # check that initially there is no patents-py folder
        self.assertIsNone(self.portal['ca'].get('patents-py'))

        expected_response = (
            f'Patents are located at {self.portal.absolute_url()}/ca/patents\n\n'

            + f"Technological offers are located at {self.portal.absolute_url()}/ca/patents/nova-oferta-tecnologica\n\n"

            + 'Create technological offer form is available at '
            + f'{self.portal.absolute_url()}/ca/patents/nova-oferta-tecnologica/create-technological-offer\n\n'

            + 'Collection of technological offers in draft state is available at '
            + f'{self.portal.absolute_url()}/ca/patents/nova-oferta-tecnologica/technological-offers-to-review'
        )

        # check that the view returned expected response
        self.assertEqual(expected_response, view())

        # check that patents folder was created successfully
        patents = self.portal['ca']['patents']
        self.assertIsNotNone(patents)
        self.assertEqual(patents.portal_type, 'Folder')

        # check that oferta tecnologica folder was created successfully
        techoffer = patents['nova-oferta-tecnologica']
        self.assertIsNotNone(techoffer)
        self.assertEqual(techoffer.portal_type, 'Folder')
        self.assertEqual(techoffer.getLayout(), 'techoffer_filter')

        # check that create-technological-offer form was created successfully
        easyform = techoffer['create-technological-offer']
        self.assertIsNotNone(easyform)
        self.assertEqual(easyform.portal_type, 'EasyForm')

        # check that a non-default field is present in the form's xml fields model
        form_field = (
            '<field name="advantages" type="plone.app.textfield.RichText" '
            + 'easyform:serverSide="False" easyform:validators="maxLengthNoTags1100" '
            + 'easyform:THidden="False">'
        )
        self.assertIn(form_field, easyform.fields_model)

        # check that technological-offers-to-review collection was created successfully
        collection = techoffer['technological-offers-to-review']
        self.assertIsNotNone(collection)
        self.assertEqual(collection.portal_type, 'Collection')

        # check that collection query is correct
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
        self.assertEqual(collection.query, collection_query)

    def test_configure_techoffer_overrides(self):
        view = api.content.get_view(
            name='configure_techoffer',
            context=self.portal,
            request=self.request
        )

        techoffer_title = 'New title, should not be changed.'
        easyform_title = 'New title for easyform, should be changed.'
        collection_title = 'New title for collection, should be changed.'
        test_folder_title = 'Test folder, should not be deleted'

        # create contents by calling the view
        view()

        # modify some created contents data
        techoffer = api.content.get('/ca/patents/nova-oferta-tecnologica')
        self.assertIsNotNone(techoffer)
        techoffer.setLayout('list_view')
        techoffer.title = techoffer_title

        easyform = techoffer['create-technological-offer']
        easyform.title = easyform_title

        collection = techoffer['technological-offers-to-review']
        collection.title = collection_title

        # create contents inside nova-oferta-tecnologica to check it is not deleted
        api.content.create(
            type='Folder',
            id='test-folder',
            title=test_folder_title,
            container=techoffer
        )

        # extract some info to compare it after the second call to view
        techoffer_created_at = techoffer.creation_date
        easyform_created_at = easyform.creation_date
        collection_created_at = collection.creation_date

        import transaction
        transaction.commit()

        # check new info saved
        techoffer = api.content.get('/ca/patents/nova-oferta-tecnologica')
        easyform = techoffer['create-technological-offer']
        collection = techoffer['technological-offers-to-review']

        self.assertEqual(techoffer.title, techoffer_title)
        self.assertEqual(techoffer.getLayout(), 'list_view')
        self.assertEqual(easyform.title, easyform_title)
        self.assertEqual(collection.title, collection_title)
        self.assertEqual(techoffer.creation_date, techoffer_created_at)
        self.assertEqual(easyform.creation_date, easyform_created_at)
        self.assertEqual(collection.creation_date, collection_created_at)

        # second call to the view
        view()

        # get new data
        techoffer = api.content.get('/ca/patents/nova-oferta-tecnologica')
        easyform = techoffer['create-technological-offer']
        collection = techoffer['technological-offers-to-review']
        test_folder = techoffer['test-folder']

        # Check that techoffer was not deleted, just changed the layout
        self.assertEqual(techoffer.title, techoffer_title)
        self.assertEqual(techoffer.getLayout(), 'techoffer_filter')
        self.assertEqual(techoffer.creation_date, techoffer_created_at)

        # Check that easyform was deleted and all changed info was reset
        self.assertNotEqual(easyform.title, easyform_title)
        self.assertNotEqual(easyform.creation_date, easyform_created_at)

        # Check that collection was deleted and all changed info was reset
        self.assertNotEqual(collection.title, collection_title)
        self.assertNotEqual(collection.creation_date, collection_created_at)

        # Check that the created content inside techoffer still exists
        self.assertIsNotNone(test_folder)
        self.assertEqual(test_folder.title, test_folder_title)

    def test_techoffer_filter_get_content_empty(self):
        view = api.content.get_view(
            name='techoffer_filter',
            context=self.portal,
            request=self.request
        )

        self.assertEqual(len(view.get_content()), 0)

    def test_techoffer_filter_get_content_draft_only(self):
        view = api.content.get_view(
            name='techoffer_filter',
            context=self.portal,
            request=self.request
        )

        self._create_techoffer(state='draft')
        self._create_techoffer(state='draft')

        self.assertEqual(len(view.get_content()), 0)

    def test_techoffer_filter_get_content_draft_and_published(self):
        view = api.content.get_view(
            name='techoffer_filter',
            context=self.portal,
            request=self.request
        )

        states = ['draft', 'draft', 'published', 'published']
        for state in states:
            self._create_techoffer(state=state)

        self.assertEqual(len(view.get_content()), 2)

    def test_techoffer_filter_get_tags_empty(self):
        view = api.content.get_view(
            name='techoffer_filter',
            context=self.portal,
            request=self.request
        )

        self.assertEqual(len(view.get_tags()), 0)

    def test_techoffer_filter_get_tags_draft_only(self):
        view = api.content.get_view(
            name='techoffer_filter',
            context=self.portal,
            request=self.request
        )

        self._create_techoffer(tags=['a'], state='draft')
        self._create_techoffer(tags=['b'], state='draft')

        self.assertEqual(len(view.get_tags()), 0)

    def test_techoffer_filter_get_tags_draft_and_published(self):
        view = api.content.get_view(
            name='techoffer_filter',
            context=self.portal,
            request=self.request
        )

        tags_and_states = (('a', 'draft'), ('b', 'draft'), ('c', 'published'), ('d', 'published'))

        for tags, state in tags_and_states:
            self._create_techoffer(tags=tags, state=state)

        self.assertEqual(len(view.get_tags()), 2)
        self.assertEqual(view.get_tags(), ['c', 'd'])

    def test_techoffer_filter_get_tags_multiple_tags_per_content(self):
        view = api.content.get_view(
            name='techoffer_filter',
            context=self.portal,
            request=self.request
        )

        tags_list = (['a', 'b'], ['c'], ['d'], ['e', 'f', 'g'])

        for tags in tags_list:
            self._create_techoffer(tags=tags, state='published')

        self.assertEqual(len(view.get_tags()), 7)
        self.assertEqual(view.get_tags(), ['a', 'b', 'c', 'd', 'e', 'f', 'g'])

    def test_techoffer_filter_get_container_path(self):
        view = api.content.get_view(
            name='techoffer_filter',
            context=self.portal,
            request=self.request
        )
        self.assertEqual(view.get_container_path(), self.portal.absolute_url() + '/techoffer_filter_query')

    def test_techoffer_filter_get_draft_collection_path(self):
        view = api.content.get_view(
            name='techoffer_filter',
            context=self.portal,
            request=self.request
        )
        self.assertEqual(
            view.get_draft_collection_path(), self.portal.absolute_url() + '/technological-offers-to-review'
        )

    def test_techoffer_filter_query_get_content_with_tags_no_filter(self):
        self.request.form['t'] = 'b,f'
        view = api.content.get_view(
            name='techoffer_filter_query',
            context=self.portal,
            request=self.request
        )

        tags_list = (['a', 'b'], ['c'], ['d'], ['b'], [], ['f'])

        for tags in tags_list:
            self._create_techoffer(tags=tags, state='published')

        self.assertEqual(len(view.get_content(filtered=False)), 6)

    def test_techoffer_filter_query_get_content_with_tag(self):
        self.request.form['t'] = 'b'
        view = api.content.get_view(
            name='techoffer_filter_query',
            context=self.portal,
            request=self.request
        )

        tags_list = (['a', 'b'], ['c'], ['d'], ['b'], [], ['f'])

        for tags in tags_list:
            self._create_techoffer(tags=tags, state='published')

        self.assertEqual(len(view.get_content()), 2)

    def test_techoffer_filter_query_get_content_with_multiple_tags(self):
        self.request.form['t'] = 'b,a'
        view = api.content.get_view(
            name='techoffer_filter_query',
            context=self.portal,
            request=self.request
        )

        tags_list = (['a', 'b'], ['b'], ['a'], ['c', 'a'], ['c', 'd', 'a', 'b'], [], ['f'])

        for tags in tags_list:
            self._create_techoffer(tags=tags, state='published')

        self.assertEqual(len(view.get_content()), 2)

    def test_techoffer_filter_query_get_content_with_query_no_filter(self):
        self.request.form['q'] = 'techoffer 1'
        view = api.content.get_view(
            name='techoffer_filter_query',
            context=self.portal,
            request=self.request
        )

        titles = ('techoffer 1', 'another techoffer', 'third techoffer')
        for title in titles:
            self._create_techoffer(title=title, state='published')

        self.assertEqual(len(view.get_content(filtered=False)), 3)

    def test_techoffer_filter_query_get_content_with_query(self):
        self.request.form['q'] = 'techoffer 1'
        view = api.content.get_view(
            name='techoffer_filter_query',
            context=self.portal,
            request=self.request
        )

        titles = ('techoffer 1', 'another techoffer', 'third techoffer')
        for title in titles:
            self._create_techoffer(title=title, state='published')

        self.assertEqual(len(view.get_content()), 1)

    def test_techoffer_filter_query_get_content_with_query_multiple_results(self):
        self.request.form['q'] = 'techoffer 1'
        view = api.content.get_view(
            name='techoffer_filter_query',
            context=self.portal,
            request=self.request
        )

        titles = ('techoffer 1', 'techoffer 2', 'techoffer 10', 'techoffer 12')
        for title in titles:
            self._create_techoffer(title=title, state='published')

        self.assertEqual(len(view.get_content()), 3)

    def test_techoffer_filter_query_get_content_with_query_and_tags(self):
        self.request.form['q'] = 'techoffer 1'
        self.request.form['t'] = 'b'
        view = api.content.get_view(
            name='techoffer_filter_query',
            context=self.portal,
            request=self.request
        )

        titles = ('techoffer 1', 'techoffer 2', 'techoffer 10', 'techoffer 12')
        tags = (['a', 'b'], ['b'], ['b', 'c'], ['a'])

        for title, tags in zip(titles, tags):
            self._create_techoffer(title=title, tags=tags, state='published')

        self.assertEqual(len(view.get_content()), 2)

    def test_techoffer_filter_query_param_is_formatted_correctly(self):
        self.request.form['q'] = '　?+-* test+(test)'
        view = api.content.get_view(
            name='techoffer_filter_query',
            context=self.portal,
            request=self.request
        )
        self.assertEqual(view.query, 'test AND "("test")"*')
