Requirements:
Poetry
Python 3.10
pandoc 2.17.1.1 or lower (2.18 doesn't work with the python library)

Change .env.example to .env and add DB credentials

Run:

poetry install
poetry run python -m wikijs-export

Outputs are now in the exports folder, named by the page's "path", like home.md, home.rst, home.html

Now has 

--backend postgres|sqlite (default: postgres)
--input absolute or relative path to .sqlite file (default: ../blog_data/og_wiki.sqlite)
