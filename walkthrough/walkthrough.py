"""
This is the core logic for the walkthrough xblock, which introduces students to
a course through a digital tour.
"""
import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String, List, Float
from xblock.fragment import Fragment
from django.template import Context, Template
from django.template.loader import get_template
from xblockutils.studio_editable import StudioEditableXBlockMixin

def _resource_string(path):
    """Handy helper for getting resources from our kit."""
    data = pkg_resources.resource_string(__name__, path)
    return data.decode("utf8")

class WalkthroughXBlock(XBlock, StudioEditableXBlockMixin):
    """
    Allows students to tour through the course and get familiar with the
    platform.
    """

    button_label = String(
        display_name=('Button label'),
        help=('This is the text that will appear on the button'),
        default='Begin walkthrough',
        scope=Scope.settings,
    )

    intro = String(
        display_name=('Introduction text'),
        help=('This is the introduction that will precede the button'
            ' and explain its presence to the user'),
        default='Click the button below to learn how to navigate the platform!',
        scope=Scope.settings,
    )

    steps = List(
        display_name=('Steps in the walkthrough'),
        help=('Data representing the steps that the XBlock goes through'),
        default=[{'step': 1, 'message':'help'}],
        scope=Scope.settings,
    )

    editable_fields = (
        'button_label',
        'intro',
        'steps',
    )

    def build_fragment(
        self,
        template,
        contect_dict,
    ):
        context = Context(contect_dict)
        fragment = Fragment(template.render(context))
        return fragment

    def student_view(self, context=None):
        """
        The primary view of the WalkthroughXBlock, shown to students
        when viewing courses.
        """
        context = context or {}
        context.update(
            {
                'button_label': self.button_label,
                'intro': self.intro,
            }
        )
        template = get_template('walkthrough.html')
        fragment = self.build_fragment(
            template,
            context
        )
        fragment.add_css(
            _resource_string(
                'static/css/walkthrough.css'
            ),
        )
        fragment.add_javascript(_resource_string('static/js/src/walkthrough.js'))
        fragment.initialize_js('WalkthroughXBlock')
        return fragment

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("WalkthroughXBlock",
             """<walkthrough/>
             """),
            ("Multiple WalkthroughXBlock",
             """<vertical_demo>
                <walkthrough/>
                <walkthrough/>
                <walkthrough/>
                </vertical_demo>
             """),
        ]
