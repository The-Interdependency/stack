import sys
from fractions import Fraction
def varint(d,i):
    v=0;s=0
    while True:
        b=d[i];v|=(b&0x7f)<<s;s+=7;i+=1
        if b<0x80:return v,i
def parse(k,verbose=False):
    import os
    d=open(f'{k}.S2' if os.path.exists(f'{k}.S2') else f'{k}.S','rb').read()
    j=d.find(b'WNC\x01')
    i=j+4
    hl=d[i];i+=1
    h=d[i:i+hl];i+=hl
    hdr=[]
    a,i=varint(d,i);hdr.append(a)
    b,i=varint(d,i);hdr.append(b)
    c,i=varint(d,i);hdr.append(c)
    recs=[]
    while i<len(d):
        tl=d[i]
        if tl not in (1,2,3,4) : break
        tok=d[i+1:i+1+tl]
        try: t=tok.decode('utf-8')
        except: break
        i+=1+tl
        num,i=varint(d,i);den,i=varint(d,i)
        circ=d[i];i+=1
        bl,i=varint(d,i)
        z=d[i];i+=1
        nb=(bl+7)//8
        pay=d[i:i+nb];i+=nb
        recs.append((t,num,den,circ,bl,z,pay))
    return d,j,h,hdr,recs,i
if __name__=='__main__':
    k=sys.argv[1]
    d,j,h,hdr,recs,i=parse(k)
    print(k,'WNC at',j,'hash',h,'hdr',hdr,'records',len(recs),'end',i,'of',len(d))
    for r in recs[:12]+recs[-5:]:
        t,num,den,c,bl,z,p=r
        print(' U+%04X'%ord(t[0]) if len(t)==1 else repr(t),num,den,'%.5f'%(num/den),'c',c,'bits',bl,'z',z,p.hex())
    print('next bytes',d[i:i+64])
