from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from savoirs.models import Record
from savoirs.admin_views import RecordDashboard

# to activate your index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_INDEX_DASHBOARD = 'auf_savoirs_en_partage.dashboard.CustomIndexDashboard'

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for auf_savoirs_en_partage.
    """
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        # append another link list module for "support".
        #self.children.append(modules.LinkList(
        #    title=_('Support'),
        #    children=[
        #        {
        #            'title': _(u'Reporter un probleme JUTDA'),
        #            'url': 'http://jutda.auf.org/',
        #            'external': True,
        #        },
        #    ]
        #))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            title=_('Applications'),
            exclude_list=('django.contrib',),
        ))

        # append an app list module for "Administration"
        #self.children.append(modules.AppList(
        #    title=_('Administration'),
        #    include_list=('django.contrib',),
        #))

        # append a recent actions module
        #self.children.append(modules.RecentActions(
        #    title=_('Recent Actions'),
        #    limit=5
        #))

        # append another link list module for "RecordDashboard".
        ref_dash = RecordDashboard(context)
        self.children.append(modules.LinkList(
            title=_('Reference a completer') + " (%d restantes)" % ref_dash.total_a_faire(),
            children=ref_dash.a_traiter()
        ))


# to activate your app index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'auf_savoirs_en_partage.dashboard.CustomAppIndexDashboard'

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for auf_savoirs_en_partage.
    """
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.children.append(modules.ModelList(
            title=self.app_title,
            include_list=self.models,
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            include_list=self.get_app_content_types(),
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
