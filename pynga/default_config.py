from .__version__ import __version__

DEBUG_LEVEL = 'WARNING'
USER_AGENT = f'pynga/{__version__}'
MAX_THREAD = 100
HOST = 'https://bbs.nga.cn'
TIMEZONE = 'Asia/Shanghai'
FORUM_PAGE_SLOW_QUERY_LIMIT = 500
ADMIN_LOG_TYPE_MAPPER = {
    '2': '评分',
    '3': '举报',
    '4': '改变标题',
    '6': '修改密码',
    '7': '签名/头像',
    '9': '删除回复',
    '10': '删除主题',
    '11': '精华主题',
    '12': '发布徽章',
    '13': '改变用户组',
    '14': 'LesserNuke',
    '15': '锁定主题',
    '16': '修改版面设置',
    '17': '修改用户组设置',
    '18': '修改声望设置',
    '19': '移动主题',
    '20': 'Nuke',
    '21': '封禁版面',
    '22': '提前主题',
    '23': '镜像主题',
    '26': '修改头衔或注册时间',
    '27': '置顶主题',
    '28': '用户验证',
    '29': '取消操作',
    '31': '延时操作',
    '32': '论坛改动',
    '33': '物品交易',
    '34': '新建物品',
    '35': '物品兑换码使用',
    '36': '物品使用',
    '37': '用户声望设置',
    '38': '下注',
    '39': '完成任务',
    '40': '投票结算',
    '41': '重置email',
    '42': 'buff',
    '43': '审核未通过'
}
