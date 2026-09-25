"""Re-export every script in the place file into src/ (run from the repo root).

Usage: python tools/export_scripts.py "place/Roblox Demo.rbxl"
Fails loudly if copies of a shared script (checkpoints, kill parts) have drifted apart.
"""
import sys, os
from rbxl import read
inst, ch = read(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else "."
def path(i):
    p=[]
    while i not in (-1,None): p.append(inst[i]['props'].get('Name','?')); i=inst[i]['parent']
    return '/'.join(reversed(p))
by = {path(i)+'#'+o['props'].get('ScriptGuid',''): o for i,o in inst.items() if 'Source' in o['props']}
def src(pred):
    s={o['props']['Source'] for k,o in by.items() if pred(k,o)}
    assert len(s)==1, s; return s.pop()
files = {
 'src/ServerScriptService/leaderstats.server.luau': src(lambda k,o:k.startswith('ServerScriptService/leaderstats')),
 'src/ServerScriptService/SpawnScript.server.luau': src(lambda k,o:k.startswith('ServerScriptService/Spawn Script')),
 'src/ServerScriptService/Skiplevel.server.luau': src(lambda k,o:k.startswith('ServerScriptService/Skiplevel')),
 'src/StarterGui/ScreenGui/Frame/TextButton/SkipLevelButton.client.luau': src(lambda k,o:o['ClassName']=='LocalScript'),
 'src/Workspace/Checkpoints/Checkpoint.server.luau': src(lambda k,o:k.startswith('Workspace/Checkpoints/')),
 'src/Workspace/Level 3 - parts/KillPart.server.luau': src(lambda k,o:'Level 3' in k and 'Orientation' not in o['props']['Source']),
 'src/Workspace/Level 3 - parts/SpinningKillPart.server.luau': src(lambda k,o:'Level 3' in k and 'Orientation' in o['props']['Source']),
 'src/Workspace/MovingPlatforms/MovingPlatformZ.server.luau': src(lambda k,o:k.startswith('Workspace/Part/') and '(0, 0, 10)' in o['props']['Source']),
 'src/Workspace/MovingPlatforms/MovingPlatformY.server.luau': src(lambda k,o:k.startswith('Workspace/Part/') and '(0, 15, 0)' in o['props']['Source']),
}
for f,s in files.items():
    p=os.path.join(out,f); os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,'w',encoding='utf-8',newline='').write(s)
    print(f, len(s))
