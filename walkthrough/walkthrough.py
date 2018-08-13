"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String, List, Float
from xblock.fragment import Fragment
from django.template import Context, Template
from django.template.loader import get_template


def _resource_string(path):
    """Handy helper for getting resources from our kit."""
    data = pkg_resources.resource_string(__name__, path)
    return data.decode("utf8")

class WalkthroughXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )


    def build_fragment(
        self,
        template,
        contect_dict,
    ):
        context = Context(contect_dict)
        fragment = Fragment(template.render(context))
        return fragment

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the WalkthroughXBlock, shown to students
        when viewing courses.
        """
        context = context or {}
        context.update(
            {
                'class_name': 'try',
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
