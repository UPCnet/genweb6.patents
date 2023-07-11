import unittest
from genweb6.patents.testing import GENWEB6_PATENTS_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone import api
from zope.component import getMultiAdapter, getAdapter
from Products.CMFPlone.utils import get_installer

class ViewsIntegrationTest(unittest.TestCase):
    layer = GENWEB6_PATENTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.installer = get_installer(self.portal, self.layer['request'])
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(type='Folder', id='ca', title='ca', container=self.portal)
    
    def test_configure_techoffer_missing_addons(self):
        view = api.content.get_view(
            name='configure_techoffer',
            context=self.portal,
            request=self.request
        )
        expected_response = "Form not created.\nThere are missing products: ['collective.easyform', 'collective.easyformplugin.createdx']"
        
        # view returned expected response
        self.assertEqual(expected_response, view())
        # no new contents were created
        self.assertIsNone(self.portal['ca'].get('patents-py'))

    def test_configure_techoffer_missing_1_addon(self):
        self.installer.install_product('collective.easyform')

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
        self.installer.install_product('collective.easyform')
        self.installer.install_product('collective.easyformplugin.createdx')

        view = api.content.get_view(
            name='configure_techoffer',
            context=self.portal,
            request=self.request
        ) 

        # check that initially there is no patents-py folder
        self.assertIsNone(self.portal['ca'].get('patents-py')) 

        expected_response = f'Patents are located at {self.portal.absolute_url()}/ca/patents-py\n' +\
                            f'Create technological offer form is available at {self.portal.absolute_url()}/ca/patents-py/create-technological-offer'

        # check that the view returned expected response
        self.assertEqual(expected_response, view())

        # check that patents-py folder was created successfully
        patents = self.portal['ca']['patents-py']
        self.assertIsNotNone(patents)
        self.assertEquals(patents.portal_type, 'Folder')
        self.assertEquals(patents.getLayout(), 'techoffer_filter')

        # check that create-technological-offer form was created successfully
        easyform = patents['create-technological-offer']
        self.assertIsNotNone(easyform)
        self.assertEquals(easyform.portal_type, 'EasyForm')

        # check that a non-default field is present in the form's xml fields model
        form_field = '<field name="advantages" type="plone.app.textfield.RichText">'
        self.assertIn(form_field, easyform.fields_model)