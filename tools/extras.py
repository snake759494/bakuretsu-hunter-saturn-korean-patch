import kmenu
def apply(get,img,errors):
    t=get('DAT/TIT_DT.BIN'); kmenu.build(t)
    import kslot,kload,json
    kslot.apply(get('DAT/SLOT_DT.BIN'))
    mp=json.load(open('loadmap.json'))
    kload.patch(get('DAT/SAVE.BIN'),mp,box=True)
    kload.patch(get('DAT/LOAD.BIN'),mp,box=False)
