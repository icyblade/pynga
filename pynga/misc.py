import re
import warnings


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
            result.append({
                'action': action,
                'by_uid': alterinfo[1],
                'by_username': alterinfo[2],
                'edit_timestamp': int(alterinfo[0][1:])
            })
        elif action == 'A':  # add point
            assert len(alterinfo) in {4, 5}
            result.append({
                'action': action,
                'reputation': int(alterinfo[0][1:]),  # 声望
                'rvrc': float(alterinfo[1]),  # 威望
                'gold': float(alterinfo[2]),  # 金钱
                'log_id': int(alterinfo[3]),
                'info': alterinfo[4] if len(alterinfo) == 5 else '',
            })
        elif action == 'U':  # undo
            assert len(alterinfo) in {3, 4}
            if alterinfo[0][1:].find('/') != -1:
                reputation = alterinfo[0][1:].split('/')
                assert len(set(reputation)) == 1
                reputation = int(reputation[0])
            else:
                reputation = int(alterinfo[0][1:])
            result.append({
                'action': action,
                'reputation': reputation,  # 声望
                'rvrc': float(alterinfo[1]),  # 威望
                'gold': float(alterinfo[2]),  # 金钱
            })
        elif action == 'L':  # LesserNuke
            assert len(alterinfo) == 6
            warnings.warn(f'Action {action} is not fully implemented yet.')
        else:
            raise NotImplementedError(f'Invalid action: {action}')

    return result
