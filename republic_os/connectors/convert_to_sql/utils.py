import re
import aiosqlite
from dateutil import parser


def get_table_name_from_path(file_path: str) -> str or None:
    # Get filename from file_path
    match = re.search('\/([^\/]+)$', file_path)

    if not match or len(match.groups()) == 0:
        return

    filename = match.groups()[0]

    filename = filename.replace('.csv', '').replace('.json', '')

    # The filename is the basis for the table name so we want to be
    # as pure as possible
    try:

        (date, ignored_text) = parser.parse(filename, fuzzy_with_tokens=True)

        filename = ignored_text[0]

    except parser.ParserError:
        # We didn't find a date
        pass

    if 'Daily Sp' in file_path:
        print('stop')

    # Remove string endings of spaces, _, -, numbers, etc.
    filename = re.sub('([\W]+)$', '', filename)
    filename = re.sub('([\s\d_-]+)$', '', filename)

    return filename.replace(' ', '_').lower()


def row_has_values(row):
    has_values = True
    for value in row:
        if value in (None, ''):
            has_values = False
    return has_values


async def create_table(db: aiosqlite.Connection, table_name: str):
    # Get file and check if table exists in DB
    cursor: aiosqlite.Cursor = await db.execute(f'SELECT COUNT(*) as count FROM sqlite_master WHERE tbl_name IS "{table_name}"')

    rows = await cursor.fetchall()

    rowcount = 0

    for row in rows:
        rowcount = row[0]

    # print(f'rowcount: {rowcount}')

    # If not, create it
    if rowcount == 0:
        # Here there are no tables yet so we know we need to create one
        create_table_sql = f'CREATE TABLE {table_name}(id INTEGER PRIMARY KEY AUTOINCREMENT)'
        await db.execute(create_table_sql)
