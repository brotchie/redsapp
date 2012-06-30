#!/usr/bin/env python

import sys

from jinja2 import Environment, PackageLoader, nodes
from jinja2.ext import Extension
from jinja2.exceptions import TemplateSyntaxError

import sparkup

class JQueryMobile(Extension):
    tags = {'mobile'}

    def parse(self, parser):
        parser.stream.skip(1)
        role = parser.stream.next()
        if role.value == 'page':
            pageid = parser.stream.next()
            #return self.environment.parse(
            #    '<div data-role="page" id="{{%s}}"></div>' % (pageid.value,))
            return nodes.Output([nodes.TemplateData('<div data-role="page" id="'),
                                 nodes.Name(pageid.value, 'load'),
                                 nodes.TemplateData('"></div>')])
        else:
            parser.fail('Invalid mobile role %r.' % (role,))

def sparkup_filter(value):
    p = sparkup.Parser(sparkup.Options(None, []))
    p.load_string(value)
    return p.render()

def main():
    assert len(sys.argv) == 2
    env = Environment(loader=PackageLoader('redsapp', 'templates'),
                      extensions=[JQueryMobile])
    env.filters['sparkup'] = sparkup_filter
    env.line_statement_prefix = '%'

    template = env.get_template(sys.argv[1])
    print template.render()

if __name__ == '__main__':
    main()
