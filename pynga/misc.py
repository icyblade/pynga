import re


def handle_alterinfo(alterinfo_raw):
    alterinfo_extracted = map(
        lambda x: x.split(' '),
        re.findall('\[(.+?)\]', alterinfo_raw)
    )
    result = []
    for alterinfo in alterinfo_extracted:
        action = alterinfo[0][0]
        if action == 'E':  # edit
            assert len(alterinfo) == 3
            assert alterinfo[1] == alterinfo[2] == '0'
            result.append({
                'action': action,
                'edit_timestamp': int(alterinfo[0][1:])
            })
        elif action == 'A':  # add point
            assert 4 <= len(alterinfo) <= 5
            result.append({
                'action': action,
                'reputation': int(alterinfo[0][1:]),  # 声望
                'rvrc': float(alterinfo[1]),  # 威望
                'gold': float(alterinfo[2]),  # 金钱
                'log_id': int(alterinfo[3]),
                'info': alterinfo[4] if len(alterinfo) == 5 else '',
            })
        elif action == 'U':  # undo
            assert len(alterinfo) == 3
            result.append({
                'action': action,
                'reputation': int(alterinfo[0][1:]),  # 声望
                'rvrc': float(alterinfo[1]),  # 威望
                'gold': float(alterinfo[2]),  # 金钱
            })
        else:
            raise NotImplementedError(f'Invalid action: {action}')

    return result
