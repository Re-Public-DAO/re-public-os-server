
class Column:

    def __init__(self, name, value):
        self._name = name
        self._value = value
        self._value_type = type(value)
        if self._value_type is list:
            # Detect plural name and get singular version
            self._relationship_table_name = name
        else:
            self._relationship_table_name = None

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def value_type(self):
        return self._value_type

    @property
    def relationship_table_name(self):
        return self._relationship_table_name


class Relationship:

    def __init__(self, table_name, related_table_name, related_fk_column_name, join_on_property_name):
        self._table_name = table_name
        self._related_table_name = related_table_name
        self._related_fk_column_name = related_fk_column_name
        self._join_on_property_name = join_on_property_name
        self._records = []
        self._items = []
        self._nested_key = None

    @property
    def table_name(self):
        return self._table_name

    @property
    def related_table_name(self):
        return self._related_table_name

    @property
    def related_fk_column_name(self):
        return self._related_fk_column_name

    @property
    def nested_key(self):
        return self._nested_key

    @nested_key.setter
    def nested_key(self, value):
        self._nested_key = value

    @property
    def records(self):
        return self._records

    @property
    def items(self):
        return self._items

    @property
    def join_on_property_name(self):
        return self._join_on_property_name


class Table:

    def __init__(self, name):
        self._columns = []
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def columns(self):
        return self._columns

    def add_column(self, column):
        self._columns.append(column)


class FileConverter:

    def __init__(self, filename, source_dir,):
        self._tables = []
        self._filename = filename
        self._file_path = f'{source_dir}/{filename}'
        self._relationships = []
        self._data = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def relationships(self):
        return self._relationships
    
    @relationships.getter
    def relationships(self,):
        return self._relationships

    def get_relationship(self, table_name, related_table_name, related_fk_column_name) -> Relationship or None:
        relationship = None
        for existing_relationship in self._relationships:
            if (
                existing_relationship.table_name == table_name and
                existing_relationship.related_table_name == related_table_name and
                existing_relationship.related_fk_column_name == related_fk_column_name
            ):
                relationship = existing_relationship
                break
        return relationship

    def add_relationship(self, relationship):
        found_relationship = None
        # Make sure we don't already have the relationship
        for existing_relationship in self._relationships:
            if (
                existing_relationship.table_name == relationship.table_name and
                existing_relationship.related_table_name == relationship.related_table_name and
                existing_relationship.related_fk_column_name == relationship.related_fk_column_name
            ):
                found_relationship = existing_relationship
        if not found_relationship:
            self._relationships.append(relationship)

    @property
    def filename(self):
        return self._filename

    @property
    def file_path(self):
        return self._file_path

    @property
    def tables(self):
        return self._tables

    def add_table(self, table):
        # Make sure we don't already have the table
        for existing_table in self._tables:
            if existing_table.name == table.name:
                return
        self._tables.append(table)
