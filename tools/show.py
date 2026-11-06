import json,sys
j=json.load(open('ja.json'))
for nm in sys.argv[1:]:
    print('=====',nm)
    for i,t in enumerate(j[nm]): print(f'#{i} '+t.replace('\n　','/').replace('\n','/').replace('▼/','▼'))
