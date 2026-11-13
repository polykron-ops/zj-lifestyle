"""Difficulty labels (visual read of the 40-SKU sample, cs 2026-11-13) and the pilot allocation weighted on the eligible population."""
import csv, collections
D='C:/Dev/zj-lifestyle/'
EASY={2,3,4,13,14,18,19,29,30,32,33,34,37,38,39}; MED={1,5,6,11,12,20,28,31,35,36}
rows=list(csv.reader(open(D+'data/source_sample.csv',encoding='utf8'))); h=rows[0]; body=rows[1:]
out=[]
for r in body:
    n=int(r[0]); d='easy' if n in EASY else 'medium' if n in MED else 'hard'; out.append(r+[d])
csv.writer(open(D+'data/source_sample.csv','w',newline='',encoding='utf8')).writerows([h+['difficulty']]+out)
c=collections.Counter(r[-1] for r in out); print('difficulty',c,{k:'%.0f%%'%(100*v/len(out)) for k,v in c.items()})
print('by letter-family x difficulty',collections.Counter((r[2].split('/')[0],r[-1]) for r in out))
pop=list(csv.DictReader(open(D+'data/dataset_2485.csv',encoding='utf8')))
byl=collections.Counter(r['family'].split('/')[0] for r in pop); N=len(pop)
# largest remainder over 28 slots
T=28; q={k:T*v/N for k,v in byl.items()}; a={k:int(x) for k,x in q.items()}
for k in sorted(q,key=lambda k:q[k]-a[k],reverse=True)[:T-sum(a.values())]: a[k]+=1
print('pilot 28:',a,'| quota (unrounded):',{k:round(x,2) for k,x in q.items()})
