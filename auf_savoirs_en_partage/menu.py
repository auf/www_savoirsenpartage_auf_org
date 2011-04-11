# coding: utf-8

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu import items, Menu

class CustomMenu(Menu):
    """
    Custom Menu for sep admin site.
    """

    statistiques = items.MenuItem(title='Statistiques', url=reverse('stats'))

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

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        request = context['request']
        if request.user.has_perm('savoirs.statistiques'):
            self.children.append(self.statistiques)
