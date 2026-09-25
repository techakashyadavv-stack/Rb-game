"""Minimal reader for the Roblox binary place format (.rbxl).

Decodes INST / PROP / PRNT chunks, keeping only String/Bool/Enum properties,
which is enough to rebuild the tree and pull script sources.
"""
import struct, sys, json
import lz4.block, zstandard

def interleaved(buf, n, size=4):
    out = []
    for i in range(n):
        v = 0
        for b in range(size):
            v = (v << 8) | buf[b * n + i]
        out.append(v)
    return out

def untransform(v):
    return (v >> 1) ^ -(v & 1)

def refs(buf, n):
    vals = [untransform(x) for x in interleaved(buf, n)]
    acc, out = 0, []
    for v in vals:
        acc += v
        out.append(acc)
    return out

class R:
    def __init__(s, b): s.b, s.p = b, 0
    def take(s, n):
        d = s.b[s.p:s.p + n]; s.p += n; return d
    def u8(s): return s.take(1)[0]
    def u32(s): return struct.unpack('<I', s.take(4))[0]
    def str(s): return s.take(s.u32())

def read(path):
    data = open(path, 'rb').read()
    assert data[:8] == b'<roblox!'
    p = 32
    classes, inst, children = {}, {}, {}
    while p < len(data):
        name = data[p:p + 4]; clen, ulen = struct.unpack('<II', data[p + 4:p + 12]); p += 16
        if clen == 0:
            body = data[p:p + ulen]; p += ulen
        else:
            raw = data[p:p + clen]; p += clen
            if raw[:4] == b'\x28\xb5\x2f\xfd':
                body = zstandard.ZstdDecompressor().decompress(raw, max_output_size=ulen)
            else:
                body = lz4.block.decompress(raw, uncompressed_size=ulen)
        r = R(body)
        if name == b'INST':
            cid = r.u32(); cname = r.str().decode(); r.u8(); n = r.u32()
            ids = refs(r.take(4 * n), n)
            classes[cid] = (cname, ids)
            for i in ids:
                inst[i] = {'ClassName': cname, 'props': {}, 'parent': None}
        elif name == b'PROP':
            cid = r.u32(); pname = r.str().decode(); t = r.u8()
            ids = classes[cid][1]; n = len(ids)
            vals = None
            if t == 0x01:
                vals = [r.str() for _ in range(n)]
                vals = [v.decode('utf-8', 'replace') for v in vals]
            elif t == 0x02:
                vals = [bool(x) for x in r.take(n)]
            elif t == 0x12:
                vals = interleaved(r.take(4 * n), n)
            if vals is not None:
                for i, v in zip(ids, vals):
                    inst[i]['props'][pname] = v
        elif name == b'PRNT':
            r.u8(); n = r.u32()
            c = refs(r.take(4 * n), n); pa = refs(r.take(4 * n), n)
            for ci, pi in zip(c, pa):
                inst[ci]['parent'] = pi
                children.setdefault(pi, []).append(ci)
        elif name == b'END\x00':
            break
    return inst, children

if __name__ == '__main__':
    inst, children = read(sys.argv[1])
    def walk(i, d):
        o = inst[i]
        extra = ''
        if 'Source' in o['props']:
            extra = f"  [{len(o['props']['Source'])} chars]"
        print('  ' * d + f"{o['props'].get('Name', '?')} ({o['ClassName']}){extra}")
        for c in children.get(i, []):
            walk(c, d + 1)
    for root in children.get(-1, []):
        walk(root, 0)
