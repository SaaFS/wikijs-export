import os
from typing import Any, Optional
from dataclasses import dataclass
from pendulum import datetime
import pandoc
from .config import BASE_DIR

@dataclass
class Page:
   id: int
   path: str
   hash: str
   title: str
   description: str
   is_private: bool
   is_published: bool
   private_NS: str
   publish_start_date: Optional[datetime]
   publish_end_date: Optional[datetime]
   content: str
   render: str
   toc: list[dict[str, str | list]]
   content_type: str
   created_at: datetime
   updated_at: datetime
   editor_key: str
   locale_code: str
   author_id: int
   creator_id: int
   extra: dict[str, str]

@dataclass
class User:
   id: int
   email: str
   name: str


class PageParser:
   """Takes pages from Wiki.js database and creates rst, md, and html files from them"""
   def __init__(self, pages: list[tuple[Any]], users: list[tuple[Any]]):
      self.pages: list[Page] = []
      self.users: list[User] = []

      for page in pages:
         self.pages.append(Page(*page))

      for user in users:
         self.users.append(User(*user[:3]))

      self.export_data()

   def generate_md(self, page: Page, author: str) -> str:
      markdown_text = \
      f'''Title: {page.title}
Date: {page.created_at}
Modified: {page.updated_at}
Author: {author}
Lang: {page.locale_code}
Summary: {page.description}

{page.content}
'''

      return markdown_text

   def generate_rst(self, page: Page, author: str, rst_body: str) -> str:
      rst_text = \
      f'''{page.title}
##############

:date: {page.created_at}
:modified: {page.updated_at}
:slug: {page.hash}
:author: {author}
:summary: {page.description}
:lang: {page.locale_code}

{rst_body}
'''
      return rst_text

   def generate_html(self, page: Page, author: str, html_body) -> str:

      # We space the data so it will line up
      spaced_html_body = '\n'.join([f'      {x}' for x in html_body.split('\n')])
      html_text = \
      f'''<html lang="{page.locale_code}">
   <head>
      <title>{page.title}</title>
      <meta name="date" content="{page.created_at}" />
      <meta name="modified" content="{page.updated_at}" />
      <meta name="author" content="{author}" />
      <meta name="lang" content="{page.locale_code}" />
      <meta name="summary" content="{page.description}" />
   </head>
   <body>
{spaced_html_body}
   </body>
</html>
'''
      return html_text

   def export_data(self):
      for page in self.pages:
         print(page)
         author: str
         page_name: str = page.path

         for user in self.users:
            if user.id == page.author_id:
               author = f'{user.name} <{user.email}>'

         if not author:
            author = 'Unknown Author'

         md_file_contents = self.generate_md(page, author)

         os.makedirs(name=os.path.dirname((BASE_DIR / f'exports/{page_name}.md').resolve()), exist_ok=True)

         with open(f'exports/{page_name}.md', 'w') as f:
            f.write(md_file_contents)

         html_output = self.generate_html(page, author, pandoc.write(pandoc.read(source=page.content), format="html"))
         with open(f'exports/{page_name}.html', 'w') as f:
            f.write(html_output)

         rst_output = self.generate_rst(page, author, pandoc.write(pandoc.read(source=page.content), format="rst"))

         with open(f'exports/{page_name}.rst', 'w') as f:
            f.write(rst_output)
