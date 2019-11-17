from practice_dir.addFunc import add

def test_add():
    assert add(1, 1) == 2
    assert add('1', '2') == '1+2'