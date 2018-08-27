"""
This is the core logic for the walkthrough xblock, which introduces students to
a course through a digital tour.
"""
import json
import os
from StringIO import StringIO
from xml.dom import minidom
import pkg_resources
from django.template import Context
from django.template.loader import get_template
from lxml import etree
from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment
import xmltodict


def _resource_string(path):
    """Handy helper for getting resources from our kit."""
    data = pkg_resources.resource_string(__name__, path)
    return data.decode("utf8")


def _load_resource(resource_path):
    """
    Gets the content of a resource
    """
    resource_content = pkg_resources.resource_string(
        __name__,
        resource_path,
    )
    return unicode(resource_content)


class WalkthroughXBlock(XBlock):
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
        default=('Click the button below to learn how to navigate the '
                 'platform!'),
        scope=Scope.settings,
    )

    steps = String(
        display_name=('Steps in the walkthrough'),
        help=('Data representing the steps that the XBlock goes through'),
        default=_load_resource('walkthrough.xml'),
        scope=Scope.content,
    )

    def build_fragment(
            self,
            template,
            context_dict,
    ):
        """
        Build the fragment by passing the context into the template
        """
        context = Context(context_dict)
        fragment = Fragment(template.render(context))
        return fragment

    def xml_to_json(self):
        """
        Convert steps from xml to json
        """
        final_steps = []
        doc = xmltodict.parse(self.steps)
        steps = doc['walkthrough']['step']
        if isinstance(steps, list):
            for step in doc['walkthrough']['step']:
                final_steps.append(json.dumps(dict(step)))
        else:
            final_steps.append(json.dumps(dict(steps)))
        return json.dumps(final_steps)

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
                'steps': self.xml_to_json(),
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
        fragment.add_javascript(
            _resource_string('static/js/src/walkthrough.js')
        )
        fragment.initialize_js('WalkthroughXBlock')
        return fragment

    def studio_view(self, context=None):
        context = context or {}
        context.update(
            {
                'button_label': self.button_label,
                'intro': self.intro,
                'steps': self.steps,
            }
        )
        template = get_template('edit.html')
        fragment = self.build_fragment(
            template,
            context
        )
        fragment.add_javascript(
            _resource_string('static/js/src/edit.js')
        )
        fragment.initialize_js('WalkthroughXBlockEdit')
        return fragment

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):
        self.button_label = submissions['button_label']
        self.intro = submissions['intro']
        xml_content = submissions['steps']
        try:
            etree.parse(StringIO(xml_content))
            self.steps = xml_content
        except etree.XMLSyntaxError as error:
            return {
                'result': 'error',
                'message': error.message,
            }
        return {
            'result': 'success',
        }

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
