import kmenu
def apply(get,img,errors):
    t=get('DAT/TIT_DT.BIN'); kmenu.build(t)
    import kmsg; kmsg.apply(t,'TIT'); kmsg.apply(get('DAT/MGAME_DT.BIN'),'MGAME')
    sy=get('DAT/SYS.BIN')  # in-game option menu: same sprites as TIT_DT at -0xa83c
    for o in (0xe460,0xe700,0xe9a0,0xdc80,0xdf20,0xe1c0): sy[o-0xa83c:o-0xa83c+0x280]=t[o:o+0x280]
    import kslot,kload,json
    kslot.apply(get('DAT/SLOT_DT.BIN'))
    import kslotmsg,kslotui; kslotmsg.apply(get('DAT/SLOT_DT.BIN')); kslotui.apply(get('DAT/SLOT_DT.BIN'))
    mp=json.load(open('loadmap.json'))
    kload.patch(get('DAT/SAVE.BIN'),mp,box=True)
    kload.patch(get('DAT/LOAD.BIN'),mp,box=False)
    # text mode: also play voice
    import voicetext
    for e in img.dir_entries():
        n=e['name']
        if n.startswith('PRG/MEN') and n.endswith('.BIN'):
            if not voicetext.patch(get(n)): errors.append('voicetext: pattern not found in '+n)
