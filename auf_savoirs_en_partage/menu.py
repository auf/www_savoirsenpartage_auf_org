# coding: utf-8

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu import items, Menu

class CustomMenu(Menu):
    """
    Custom Menu for sep admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children.append(items.MenuItem(
            title=_('Dashboard'),
            url=reverse('admin:index')
        ))
        self.children.append(items.AppList(
            title=_('Applications'),
            exclude_list=('django.contrib',)
        ))
        self.children.append(items.AppList(
            title=_('Administration'),
            include_list=('django.contrib',)
        ))
        self.children.append(items.MenuItem(
            title='Statistiques',
            url=reverse('stats')
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
