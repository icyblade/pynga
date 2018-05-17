from pynga import NGA


forum = NGA().Forum(-7, page_limit=1)
for tid, thread in forum.threads.items():
    hit = thread.subject.find('雷霆崖') != -1
    print('!' if hit else 'X' + ' ' + thread.subject)
