from datetime import datetime

from pynga.user import AdminLog


def test_adminlog():
    log = AdminLog((
        '{"0":123,"1":19,"2":456,"3":789,"4":987,'
        '"5":"test_action","6":1515495369}'
    ))
    assert log.log_id == 123
    assert log.type == '移动主题'
    assert log.source_uid == 456
    assert log.target_uid == 789
    assert log.tid == 987
    assert log.message == 'test_action'
    assert log.time == datetime(2018, 1, 9, 18, 56, 9)
    assert repr(log) == '<pynga.user.AdminLog, id=123>'
