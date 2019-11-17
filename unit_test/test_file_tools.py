from project import file_tools


def test_get_lists():
    # 如果没用用file_tools.就会报错
    list_processor = file_tools.lists_processer()
    lists = list_processor.get_lists()
    assert len(lists) == 4
