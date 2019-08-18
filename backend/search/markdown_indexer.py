import hashlib

import mistune
import re

from search import client


class CustomRenderer(mistune.Renderer):

    def __init__(self, title, source):
        super().__init__()

        self.title = title
        self.source = source

        self.current_header = []
        self.tables = []
        self.lists = []

        # Insert the document title
        self._insert_content([], None, type='title')

    def header(self, text, level, raw=None):
        self._insert_header(text, level)
        self._insert_content(self.current_header, None, type='header')

        return super().header(text, level, raw)

    def paragraph(self, text):
        # Insert only if not an image or a link alone
        if not re.compile('^<(img|a).*>$').search(text):
            self._insert_content(self.current_header, text, type='paragraph')

        return super().paragraph(text)

    def _insert_content(self, headers, content, type):
        doc = {
            'source': self.source,
            'type': type,
            'title': self.title,
            'link': self.title + ("#" + str(headers[0]['h']) if headers else ''),
            'importance': len(headers) + (1 if content else 0)
        }

        for header in headers:
            level = header['level']
            h = header['h']

            doc['h' + str(level)] = h

        if content:
            doc['content'] = content

        # We hash the content of the file so we are sure not to index 2 times the same file
        file_string = self.title + ''.join([h['h'] for h in headers]) + (content if content else '')
        doc['objectID'] = hashlib.md5(file_string.encode("utf-8")).hexdigest()

        client.insert_doc(doc)

    def _insert_header(self, text, level):
        if self.current_header:
            if self.current_header[-1].get('level') == level:
                self.current_header.pop()
                self.current_header.append({
                    'h': text,
                    'level': level
                })

            elif self.current_header[-1].get('level') > level:
                self.current_header.pop()
                self._insert_header(text, level)

            elif self.current_header[-1].get('level') < level:
                self.current_header.append({
                    'h': text,
                    'level': level
                })

        else:
            self.current_header.append({
                'h': text,
                'level': level
            })

    #
    # NOT NEEDED
    #

    # TODO: we do not index code as hard to deal with it (blocks can be huge so hard to display them in the search)
    def block_code(self, code, lang=None):
        return super().block_code(code, lang)

    # TODO: same problem with tables
    def table(self, header, body):
        return super().table(header, body)

    # TODO: same problem with lists, although more manageable
    def list(self, body, ordered=True):
        return super().list(body, ordered)

    def image(self, src, title, text):
        return super().image(src, title, text)

    def inline_html(self, html):
        return super().inline_html(html)

    def codespan(self, text): # inline code
        return super().codespan(text)

    def text(self, text):
        return super().text(text)

    def autolink(self, link, is_email=False):
        return super().autolink(link, is_email)

    def link(self, link, title, text):
        return super().link(link, title, text)

    def table_cell(self, content, **flags):
        return super().table_cell(content, flags)

    def table_row(self, content):
        return super().table_row(content)

    def list_item(self, text):
        return super().list_item(text)


def insert_markdown_doc(source, title, content):
    renderer = CustomRenderer(title, source)
    markdown = mistune.Markdown(renderer=renderer)
    markdown(content)
