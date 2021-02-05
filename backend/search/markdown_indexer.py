import hashlib

import mistune
import re

from search import client
from tools import logger
from utils.exceptions.search_exceptions import IndexingException


class CustomRenderer(mistune.Renderer):

    def __init__(self, title, source):
        super().__init__()

        self.title = title
        self.source = source

        self.current_header = []
        self.tables = []
        self.lists = []

        # Insert the document title
        self._insert_document([], None, type='title')

    def header(self, text, level, raw=None):
        self._add_header(text, level)
        self._insert_document(self.current_header, None, type='header')

        return super().header(text, level, raw)

    def paragraph(self, text):
        # Insert only if not an image or a link alone
        if not re.compile('^<(img|a).*>$').search(text):
            self._insert_document(self.current_header, text, type='paragraph')

        return super().paragraph(text)

    def _add_header(self, text, level):
        if self.current_header:
            if self.current_header[-1].get('level') == level:
                self.current_header.pop()
                self.current_header.append({
                    'h': text,
                    'level': level
                })

            elif self.current_header[-1].get('level') > level:
                self.current_header.pop()
                self._add_header(text, level)

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
    # Inserters into the documents
    #

    def _insert_document(self, headers, content, type):
        """
        Main method inserting all the field into using the search client
        """
        doc = {
            'title': self.title,
            'source': self.source,
            'type': type,
        }

        self._insert_headers(doc, headers)
        self._insert_content(doc, content)
        self._insert_link(doc, headers)
        self._insert_importance(doc, headers, content)
        self._insert_document_hash(doc, headers, content)

        client.insert_doc(doc)

    def _insert_headers(self, doc, headers):
        """
        We insert headers based on their level of depth
        """

        for header in headers:
            level = header['level']
            h = header['h']

            doc['h' + str(level)] = h

    def _insert_content(self, doc, content):
        """
        We insert content only when it exists (it is not present for titles)
        """
        if content:
            doc['content'] = content

    def _insert_link(self, doc, headers):
        """
        We generate a link to the first header of the document
        FIXME: we can go the a second or third layer of depth when linking to a document part
        """
        doc['link'] = self.title + ("#" + str(headers[0]['h']) if headers else ''),

    def _insert_importance(self, doc, headers, content):
        """
        The importance is defined as a number between 0 and 7, where 0 is for document title and 7 is for a paragraph
        inside 5 layers of titles. The lowest the importance is, the higher the result will be shown for the same result
        (see algolia tie-breaking algorithm)
        """
        doc['importance'] = len(headers) + (1 if content else 0)

    def _insert_document_hash(self, doc, headers, content):
        """
         We hash the content of the file so we are sure not to index 2 times the same file
        """
        file_string = self.title + ''.join([h['h'] for h in headers]) + (content if content else '')
        doc['objectID'] = hashlib.md5(file_string.encode("utf-8")).hexdigest()


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

    success = True

    try:
        markdown(content)
    except IndexingException:
        logger.get_logger().exception("Failed to index markdown document %s", title)
        success = False

    return success
