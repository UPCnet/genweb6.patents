# -*- coding: utf-8 -*-
from plone import api
from collective.easyform.api import get_context


def createdx_onSuccess(self, fields, request):
    """Create item on successful form submission"""
    context = get_context(self)
    current_user = api.user.get_current()

    with api.env.adopt_user(user=current_user):
        with api.env.adopt_roles(roles=["Manager"]):
            self.createDXItem(fields, request, context)
