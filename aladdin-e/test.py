import aladdin
    


cas="10025-82-8"
lst=aladdin.fn_aladdin(cas)
for x in lst:
    print (x)
    print (type(x))
    print (x['cas'])
    print (x['purity'])