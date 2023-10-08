# -*- coding: utf-8 -*-

# Copyright (c) 2017 Mr.Page
# Permission is hereby granted, free of charge, to any person obtaininga copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals

from docutils import nodes
from docutils.parsers.rst import directives, Directive

from . import config

import os


class UnityWebgl(Directive):
    required_arguments = 1
    optional_arguments = 4

    option_spec = {
        'width': directives.positive_int,
        'height': directives.positive_int,
        'gameroot': directives.unchanged_required,
        'template': directives.unchanged_required,
    }

    final_argument_whitespace = False
    has_content = False

    def load_template(self, game, gamesroot, templatepath, width, height):
        """What does this do?"""

        print('loading template')
        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, 'template.txt'))
        with open(filepath, 'r') as template:
            """opens template.txt"""
            data = template.read()
            return data.format(game, gamesroot, templatepath, width, height)
            """the template.txt has several places with {n} that get replaced with the n-th
            argument of data.format(...). This appears to create html code that would include a
            unity player instance"""

    def run(self):
        """This is method runs when whatever builds the website
        from the .rst reaches the .. unitywebgl:: directive."""

        # load config

        game = self.arguments[0].strip()
        games_path = config.GAMES_ROOT_DIR
        template_path = config.TEMPLATE_PATH
        width = config.DEFAULT_WIDTH
        height = config.DEFAULT_HEIGHT

        # get params

        if 'width' in self.options:
            width = self.options['width']
        if 'height' in self.options:
            height = self.options['height']
        if 'gameroot' in self.options:
            games_path = self.options['gameroot']
        if 'template' in self.options:
            template_path = self.options['template']

        # remove slashes

        games_path = games_path.rstrip('/')
        template_path = template_path.rstrip('/')

        html = self.load_template(game, games_path, template_path, width, height)
        """This line will run with game='xanadu-quest', games_path='games/xanadu-quest/Build',
        template_path='games/xanadu-quest/TemplateData', width=default,height=default.
        
        The returned value stored into html is html code that should run the unity player."""

        return [
            nodes.raw('', html, format='html')]


def register():
    directives.register_directive('unitywebgl', UnityWebgl)
