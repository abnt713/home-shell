__author__ = 'alisonbento'

import basedao

import src.entities.hsgroup as hsgroup

class GroupDAO(basedao.BaseDAO):

    def __init__(self, connection):
        basedao.BaseDAO.__init__(self, connection, 'hs_groups', 'group_id')

    def convert_row_to_object(self, entity_row):
        group = hsgroup.HomeShellGroup()

        group.id = entity_row['group_id']
        group.name = entity_row['name']
        group.author_id = entity_row['author_id']
        group.created = entity_row['created']
        group.modified = entity_row['modified']

        return group