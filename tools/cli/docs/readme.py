#!/usr/bin/python3.9
import os

from pytablewriter import MarkdownTableWriter

from src.core.config import create_env_list_from_schema, root_dir


def main():
    readme_filepath = root_dir + '/config/README.md'
    env_list = create_env_list_from_schema()
    header = ['name', 'type']
    payload = [[env.name, env.type] for env in env_list]
    writer = MarkdownTableWriter(
        headers=header,
        value_matrix=payload,
        margin=1
    )
    table = writer.dumps()
    table_split = table.split('\n')
    table_split[1] = table_split[1].replace(' ', '-')
    table = '\n'.join(table_split)
    if os.path.exists(readme_filepath):
        os.remove(readme_filepath)
    file_payload = """# ENV LIST \n\n""" + table
    file = open(readme_filepath, "a")
    file.write(file_payload)
    file.close()


if __name__ == '__main__':
    main()
