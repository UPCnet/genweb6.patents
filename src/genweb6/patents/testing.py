# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import genweb6.patents


class Genweb6PatentsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import collective.easyform
        self.loadZCML(package=collective.easyform)
        import collective.easyformplugin.createdx
        self.loadZCML(package=collective.easyformplugin.createdx)
        self.loadZCML(package=genweb6.patents)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'genweb6.patents:default')


GENWEB6_PATENTS_FIXTURE = Genweb6PatentsLayer()

GENWEB6_PATENTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GENWEB6_PATENTS_FIXTURE,),
    name='Genweb6PatentsLayer:IntegrationTesting',
)


GENWEB6_PATENTS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GENWEB6_PATENTS_FIXTURE,),
    name='Genweb6PatentsLayer:FunctionalTesting',
)


GENWEB6_PATENTS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        GENWEB6_PATENTS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='Genweb6PatentsLayer:AcceptanceTesting',
)
