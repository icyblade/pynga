# pynga
NGA 各项功能的 Python 实现

## NGA 类

构造函数为 `nga = NGA(登陆用户的UID，登陆用户的CID)`

有 method

- `u = User(uid)`
  
  new 一个 uid 的用户对象
- `f = Forum(fid)`
  
  new 一个 fid 的版面对象
- `t = Thread(tid)`
  
  new 一个 tid 的帖子对象
- `[fid] = get_all_fids()`
  
  获取所有公开版面列表

## User 类

有 attribute

- `user_info`
  
  raw json
- `username`
  
  用户名
- `group`
  
  用户组 ID

有 method

- `[(id, typ, source_uid, target_uid, target_tid, target_pid, description, timestamp)] = get_admin_log_done(start_datetime=None)`
  
  返回 start_datetime 直到现在的该用户的操作记录
  
  如果没有指定 start_datetime ，则返回一天之内的该用户的操作记录

## Forum 类

有 method

- `[uid] = get_wardens(sub=False)`
  
  返回当前版面的所有版主 UID 列表
  
  如果 sub == True，则只返回所有副版主的 UID 列表

## Thread 类

有 method

- `p = Post(pid)`
  
  new 一个 pid 的回复对象
- `fid = get_fid()`
  
  返回本贴所在的版面 FID
- `[(pid, postdatetimestamp, uid, 楼层序号)] = get_replies()`
  
  返回本贴内的所有回复
- `[(pid, postdatetimestamp, uid, 楼层序号)] = get_replies_in_page(page)`
  
  返回本贴第 page 页内的所有回复

## Post 类

有 method

- `[(pid, postdatetimestamp, uid)] = get_comments()`
  > 返回本回复的所有贴条

## NGAApp 类

还没做好 :-)