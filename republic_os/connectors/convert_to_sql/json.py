import re
import html
import json
from classes import *
from utils import *
import aiosqlite
from dateutil import parser
import inflect

p = inflect.engine()


class JsonItem:

    def __init__(self, data):
        self._columns = []
        self._keys_list = list(data.keys())
        self._query_statement = None
        self._insert_segment = None
        self._values_segment = None
        self._nested_key = None
        self._parent_item = None
        self._children = None
        # If there's only one key, and the key matches the name of the file/table_name,
        # then we assume the actual record is attached to that key.
        if len(self._keys_list) == 1:
            if not type(data[self._keys_list[0]]) is str:
                # This means we have a single key on each record that points to the real record data.
                # For example:
                # {
                #   "dmConversation": {
                #       "conversationId": "XXXXXX",
                #       "messages": [
                #           {
                #               "messageId": "XXXX1",
                #               "text": "Hello world!"
                #           },
                #           {
                #               "messageId": "XXXX2",
                #               "text": "Goodbye world!"
                #           }
                #       ]
                #   }
                # }
                # So we need to go down a level (dmConversation) and parse that object instead.
                self._nested_key = self._keys_list[0]
                self._record = data[self._nested_key]
                if type(self._record) is not list:
                    self._keys_list = list(self._record.keys())
                    self._record['json_key'] = self._nested_key
            else:
                self._record = data
        else:
            self._record = data
        # Local here means ids that are generated and used by the data source
        local_id = None
        local_id_prop = None
        if not type(self._record) is str:
            if 'id' in self._record:
                local_id_prop = 'id'
                local_id = self._record['id']
            elif 'Id' in self._record:
                local_id_prop = 'Id'
                local_id = self._record['Id']
            else:
                for key in self._keys_list:
                    if key is None:
                        return
                    match = re.search('(id|_ID|Id|_id)$', key)
                    if match and match.group():
                        local_id_prop = key
                        local_id = self._record[key]
            self._local_id = local_id
            self._local_id_prop = local_id_prop

    @property
    def record(self):
        return self._record

    @record.setter
    def record(self, value):
        self._record = value

    @property
    def local_id(self):
        return self._local_id

    @property
    def local_id_prop(self):
        return self._local_id_prop

    @property
    def keys_list(self):
        return self._keys_list

    @property
    def nested_key(self):
        return self._nested_key

    @property
    def columns(self):
        return self._columns

    def get_fk_property(self):
        fk_property = None
        for key in self._keys_list:
            match = re.search('(Id)$', key)
            if match and match.group():
                fk_property = key
        return fk_property

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    def add_child_item(self, child_item):
        self._children.append(child_item)

    @property
    def parent_item(self):
        return self._parent_item

    @parent_item.setter
    def parent_item(self, value):
        self._parent_item = value

    @property
    def query_statement(self):
        return self._query_statement

    @query_statement.setter
    def query_statement(self, value):
        self._query_statement = value

    @property
    def insert_segment(self):
        return self._insert_segment

    def update_insert_segment(self, value):
        self._insert_segment += value

    @insert_segment.setter
    def insert_segment(self, value):
        self._insert_segment = value

    @property
    def values_segment(self):
        return self._values_segment

    @values_segment.setter
    def values_segment(self, value):
        self._values_segment = value

    def update_values_segment(self, value):
        self._values_segment += value

    def update_segments(self, column, index, is_relationship=False):
        # If this is the last key we're looking at, we need to close off the query and
        # insert statements.
        if (is_relationship or column.value is None) and (index + 1) == len(self._keys_list):
            # Remove any trailing AND, and then close the statements
            if self._query_statement.endswith(' AND '):
                self._query_statement = self.query_statement[0:-5]
            if self._insert_segment.endswith(','):
                self._insert_segment = self.insert_segment[0:-1]
                self._insert_segment += ')'
            if self._values_segment.endswith(','):
                self._values_segment = self.values_segment[0:-1]
                self._values_segment += ')'
            return

        if is_relationship:
            return

        self._insert_segment += f'"{column.name}"'

        if column.value is None:
            self._query_statement += f'"{column.name}" IS ""'
            self._values_segment += f"''"

        if type(column.value) is bool:
            value = str(column.value).lower()
            self._query_statement += f'"{column.name}" IS "{value}"'
            self._values_segment += f"'{value}'"
            # print(f'[78] len(keys_list): {len(keys_list)} i+1: {i}')

        # Check if string is a number
        if type(column.value) is str and not column.value.isnumeric():
            try:
                column.value = float(column.value)
            except ValueError:
                pass

        if type(column.value) is str and column.value.isnumeric():
            try:
                column.value = int(column.value)
            except ValueError:
                pass

        if type(column.value) is str:
            # First check if this is a date string
            is_date = True

            # Arbitrarily deciding that if there are more than 50 characters,
            # then even if there's a date string in there, it's not exclusively
            # a date field
            if len(column.value) > 25:
                is_date = False

            # If it's all numbers, let's assume it's not
            match = re.search('^\\d+$', column.value)
            if match and match.group():
                is_date = False

            if not is_date:
                self._query_statement += f'"{column.name}" IS "{html.escape(column.value)}"'
                self._values_segment += f"'{html.escape(column.value)}'"

            if is_date:

                try:
                    date = parser.parse(column.value, fuzzy=True)
                except parser.ParserError:
                    is_date = False
                    date = None
                except OverflowError:
                    is_date = False
                    date = None

                if not is_date or not date:
                    self._query_statement += f'"{column.name}" IS "{html.escape(column.value)}"'
                    self._values_segment += f"'{html.escape(column.value)}'"

                if is_date and date:
                    self._query_statement += f'"{column.name}" IS "{date}"'
                    self._values_segment += f"'{date}'"

        if type(column.value) is dict or type(column.value) is list:
            self._query_statement += f'"{column.name}" IS "{html.escape(json.dumps(column.value))}"'
            self._values_segment += f"'{html.escape(json.dumps(column.value))}'"

        if type(column.value) is int:
            self._query_statement += f'"{column.name}" IS {column.value}'
            self._values_segment += f'{column.value}'

        if type(column.value) is float:
            self._query_statement += f'"{column.name}" IS {column.value}'
            self._values_segment += f'{column.value}'

        if len(self._keys_list) > (index + 1):
            self._query_statement += ' AND '
            self._insert_segment += ','
            self._values_segment += ','

        if (index + 1) == len(self._keys_list):
            self._insert_segment += ')'
            self._values_segment += ')'


def get_first_record(data, table: Table, parent_item: JsonItem or None = None, ) -> JsonItem:
    if type(data[0]) is str:
        if parent_item:
            fk_property = None
            if parent_item.nested_key and parent_item.nested_key:
                singular_table_name = p.singular_noun(parent_item.nested_key)
                if singular_table_name:
                    fk_property = singular_table_name + '_id'
            custom_data = {
                'value': data[0],
            }
            if fk_property:
                custom_data[fk_property] = parent_item.local_id

            return JsonItem(custom_data)
        else:
            return JsonItem({
                'value': data[0],
            })
    else:
        return JsonItem(data[0])


async def process_relationship(db, file_converter, table, column, first_record, relationship_params=None) -> Relationship:

    await create_table(db, column.relationship_table_name)

    new_table = Table(column.relationship_table_name)

    file_converter.add_table(new_table)

    if relationship_params is not None:
        relationship_params.append((column, new_table, first_record))

    relationship = file_converter.get_relationship(
        column.relationship_table_name,
        column.name,
        first_record.nested_key,
    )

    if not relationship:
        # Create a dict to save us some loop cycles later
        # relationship = Relationship(new_table.name, table.name, column.name, fk_property)
        fk_id_column_name = p.singular_noun(new_table.name)
        if not fk_id_column_name:
            fk_id_column_name = new_table.name
        fk_id_column_name += '_id'
        join_on_prop = p.singular_noun(table.name)
        if not join_on_prop:
            join_on_prop = table.name
        join_on_prop += '_id'

        relationship = Relationship(new_table.name, table.name, fk_id_column_name, join_on_prop)

    file_converter.add_relationship(relationship)

    return relationship


async def init_relationships(db: aiosqlite.Connection, data, file_converter: FileConverter, table: Table,
                             parent_item: JsonItem or None = None):
    # Analyze the first record to see what data types we have.
    # Do we need to create any relations and other tables?
    if len(data) == 0:
        return

    first_record = get_first_record(data, table, parent_item)

    if parent_item and first_record.nested_key != parent_item.nested_key:
        first_record.parent_item = parent_item

    relationship_params = []

    # Running this on the first record to find all relationships.
    for i in range(len(first_record.keys_list)):
        column_name = first_record.keys_list[i]

        if type(first_record.record) is list:
            print('list')

        column = Column(column_name, first_record.record[column_name])

        table.add_column(column)

        if column.relationship_table_name:
            await process_relationship(db, file_converter, table, column, first_record, relationship_params)

        # print(f'column.name: {column.name}')
        # print(f'column.value_type not in [dict, list]: {column.value_type not in [dict, list]}')

        if column.value_type not in [dict, list]:
            # print(f'column.name: {column.name}')
            # print('made it past the if')
            # Here we initiate all the columns for the table based on the
            # properties of `data`
            cursor = await db.execute(f'PRAGMA table_info("{table.name}")')

            column_exists = False

            results = await cursor.fetchall()

            for row in results:
                if row[1] == column_name:
                    column_exists = True

            # If a column doesn't exist for the property yet, create it
            if not column_exists:
                await db.execute(f'ALTER TABLE {table.name} ADD COLUMN {column.name}')
                # await db.commit()
                print(f'Added {column.name} to {table.name}')

    for params in relationship_params:
        (column_param, table_param, first_record_param) = params
        # Recursively run this function since structures can be nested.
        # This walks the tree of the `data`
        await init_relationships(db, column_param.value, file_converter, table_param, first_record_param)


async def extract_relationship_records(db, file_converter: FileConverter, json_item: JsonItem, relationship: Relationship,
                                 column: Column):
    for item in column.value:
        # If we're just passed a string, we have to beef it up with more relevant info
        # so that later we can attach it to the record it came from
        if type(item) is str:
            join_on_prop = None
            if relationship.join_on_property_name:
                join_on_prop = relationship.join_on_property_name

            item_to_add = JsonItem({
                'value': item,
                join_on_prop: json_item.local_id
            })
        else:
            item_to_add = JsonItem(item)

        item_to_add.parent_item = json_item

        for i in range(len(item_to_add.keys_list)):
            column_name = item_to_add.keys_list[i]
            nested_column = Column(column_name, item_to_add.record[column_name])

            if nested_column.relationship_table_name:

                table = Table(column.relationship_table_name)

                # print(f'in relationship for {nested_column.name} {nested_column.relationship_table_name} {relationship.related_table_name} {column.name}')

                item_relationship = file_converter.get_relationship(
                    nested_column.relationship_table_name,
                    column.name,
                    nested_column.name,
                )

                if not item_relationship:
                    item_relationship = await process_relationship(db, file_converter, table, nested_column, item_to_add, )

                # Here we handle the situation where the column points to a relationship.
                if item_relationship:
                    # TODO: We assume here that column_value is a list. Any further validation needed?

                    await extract_relationship_records(db, file_converter, item_to_add, item_relationship, nested_column)
                    # Once we extract the records, we need to properly edit the SQL statements.
                    # print(f'[172] [{datetime.now()}] {item_relationship.records}')
                    # json_item.update_segments(column, i, True)

        relationship_from_file_converter = file_converter.get_relationship(
            relationship.table_name,
            relationship.related_table_name,
            relationship.related_fk_column_name,
        )

        relationship_from_file_converter.items.append(item_to_add)
        relationship_from_file_converter.records.append(item_to_add.record)


async def add_column(db: aiosqlite.Connection, table_name, column_name):
    cursor = await db.execute(f'PRAGMA table_info("{table_name}")')

    column_exists = False

    rows = await cursor.fetchall()
    for row in rows:
        if row[1] == column_name:
            column_exists = True

    # If a column doesn't exist for the property yet, create it
    if not column_exists:
        await db.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name}')
        await db.commit()
        # print(f'Added {column_name} to {table_name}')


async def process_item(db: aiosqlite.Connection, file_converter: FileConverter, item: dict, table: Table, item_obj: JsonItem or None = None ):

    if item_obj is not None:
        json_item = item_obj
    else:
        json_item = JsonItem(item)

    # Sometimes we get an empty record
    if len(json_item.keys_list) == 0:
        return

    json_item.query_statement = f'SELECT COUNT(*) as count FROM {table.name} WHERE '
    json_item.insert_segment = f'INSERT INTO {table.name}('
    json_item.values_segment = 'VALUES ('

    for i in range(len(json_item.keys_list)):

        column_name = json_item.keys_list[i]
        column = Column(column_name, json_item.record[column_name])

        # print(column_name)

        if column.relationship_table_name:

            # print(f'in relationship for {column.name}')

            # Here we have already processed the relationships and just need to add the record
            # via SQL statement
            if item_obj:
                json_item.update_segments(column, i, True)
                # Move to the next column to avoid any unnecessary processing
                continue

            item_relationship = file_converter.get_relationship(
                column.relationship_table_name,
                table.name,
                column.name,
            )

            if not item_relationship:

                item_relationship = await process_relationship(db, file_converter, table, column, json_item, )

            # Here we handle the situation where the column points to a relationship.
            if item_relationship:
                # TODO: We assume here that column_value is a list. Any further validation needed?

                await extract_relationship_records(db, file_converter, json_item, item_relationship, column)
                # Once we extract the records, we need to properly edit the SQL statements.
                # print(f'[172] [{datetime.now()}] {item_relationship.records}')
                json_item.update_segments(column, i, True)
                # Move to the next column to avoid any unnecessary processing
                continue

        # print(f'[481] Calling add_column with table.name: {table.name} and column_name: {column_name}')

        await add_column(db, table.name, column_name)

        # Assemble SQL statements from column names and values
        json_item.update_segments(column, i)

    print(json_item.query_statement)

    # Check if the row exists
    cursor = await db.execute(json_item.query_statement)

    rowcount = 0

    rows = await cursor.fetchall()

    for query_result in rows:
        rowcount = query_result[0]

    # print(f'rowcount: {rowcount}')

    # If row doesn't exist, insert it
    if rowcount == 0:
        # print(f'{json_item.insert_segment} {json_item.values_segment}')
        # try:
        await db.execute(f'{json_item.insert_segment} {json_item.values_segment}')
        await db.commit()
        # print('inserted')

        # except sqlite3.OperationalError:
        #     print('Error inserting into database')


async def init_data(db, file_converter, filename, data, table_name):

    await create_table(db, table_name)

    table = Table(table_name)

    file_converter.add_table(table)

    first_record = get_first_record(data, table)

    await init_relationships(db, data, file_converter, table, first_record)

    # Loop through each item and add a row in the db for it
    for item in data:
        # print(item)
        await process_item(db, file_converter, item, table)

    # Now add the relationships that we collected before
    for relationship in file_converter.relationships:
        # print(f'[244] [{datetime.now()}] table_name: {relationship.table_name} num of records: {len(relationship.records)}')
        await create_table(db, relationship.table_name)

        relationship_table = Table(relationship.table_name)

        file_converter.add_table(relationship_table)

        await init_relationships(db, relationship.records, file_converter, relationship_table)

        for related_item in relationship.items:
            # If there's a parent_item, add it to the record and key_list so that the fk column
            # is created and populated
            if related_item.parent_item:
                related_item.record[relationship.join_on_property_name] = related_item.parent_item.local_id
                if relationship.join_on_property_name not in related_item.keys_list:
                    related_item.keys_list.append(relationship.join_on_property_name)

            await process_item(db, file_converter, related_item.record, relationship_table, related_item)


# Run this method once per .json file. Assumes .json file contains
# a single array of the same model/structure/type of data
async def json_to_sql(filename: str, db: aiosqlite.Connection, source_dir: str):
    # cursor: aiosqlite.Cursor = await db.cursor()

    file_converter = FileConverter(filename, source_dir)

    with open(file_converter.file_path, mode='r') as json_file:

        data = json.load(json_file)

        if not type(data) is list and not type(data) is dict:
            print(f'Parsed JSON from {file_converter.file_path} is not a list.')
            return

        if len(data) == 0:
            print(f'Parsed JSON from {file_converter.file_path} is an empty list.')
            return

        print(filename)

        key_is_data_type = False

        # If data is a dict, we need to do more analysis to determine the structure
        if type(data) is dict:
            data_keys_list = list(data.keys())
            key_is_data_type = True
            for key in data_keys_list:
                if type(data[key]) is not list:
                    key_is_data_type = False
                    break

            if not key_is_data_type:
                print(f'Parsed JSON from {file_converter.file_path} has an unknown data structure.')
                return

        if not key_is_data_type:

            table_name = filename.replace(' ', '_').replace('-', '_').replace('.json', '').lower()

            await init_data(db, file_converter, filename, data, table_name)

        if key_is_data_type:

            for key in data_keys_list:
                nested_data = data[key]

                if len(nested_data) == 0:
                    continue

                await init_data(db, file_converter, filename, nested_data, key)


def get_record_and_key(item: dict or list, found_at_key: str or None = None) -> (dict, str or None):
    if type(item) is list:
        return item, found_at_key

    item_keys = list(item.keys())

    # If there's only one key, and the key matches the name of the file/table_name,
    # then we assume the actual record is attached to that key.
    if len(item_keys) == 1:
        key_for_record = item_keys[0]
        record = item[key_for_record]
        # Make this recursive in case we get a bunch of nested single keys
        # {
        #     "ad": {
        #         "adsUserData": {
        #             "adEngagements": {
        #                 "engagements": [
        #                     {
        #                         "impressionAttributes": {
        #                             "deviceInfo": {
        #                                 "osType": "Desktop"
        #                             },
        #                             "displayLocation": "Trends",
        #                             "promotedTrendInfo": {
        #                                 "trendId": "86141",
        #                                 "name": "#Severance",
        #                                 "description": "Watch exclusively on Apple TV+"
        #                             },
        #                             "advertiserInfo": {
        #                                 "advertiserName": "Apple TV+",
        #                                 "screenName": "@AppleTVPlus"
        #                             },
        #                             "impressionTime": "2022-02-19 20:34:12"
        #                         },
        #                         "engagementAttributes": [
        #                             {
        #                                 "engagementTime": "2022-02-19 20:34:16",
        #                                 "engagementType": "TrendView"
        #                             }
        #                         ]
        #                     }
        #                 ]
        #             }
        #         }
        #     }
        # }
        return get_record_and_key(record, key_for_record)

    return item, found_at_key or None
