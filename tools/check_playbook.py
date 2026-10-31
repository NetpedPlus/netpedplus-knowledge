"""ตรวจรูปแบบ playbook ของ NetPED+ ก่อน push (ใช้ Python ล้วน ไม่ต้องลงอะไรเพิ่ม)
ใช้:  python tools/check_playbook.py                 ตรวจทุกไฟล์ใน playbooks/
      python tools/check_playbook.py playbooks/x.md  ตรวจเฉพาะไฟล์
ผล: ERROR = ต้องแก้ก่อน push / WARN = ควรดู   exit 1 ถ้ามี ERROR
"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILTIN = {"f5-bigip-17", "f5-ltm-asm-build", "f5-ops-advanced", "fortigate-7.4", "huawei-ac-wlan", "huawei-vrp-switch",
           "imaster-nce-campus", "kaspersky-scan-engine", "paloalto-panos", "qradar-7.5", "routing-concepts",
           "sophos-sfos-21", "windows-ad-dhcp-dns"}
FAMILIES = set("""arista_eos aruba_aos8 aruba_aos_switch aruba_aoscx checkpoint_gaia cisco_asa cisco_ios cisco_nxos cisco_sb
dell_os10 extreme_exos f5_tmsh fortinet_fortios hpe_comware huawei_ac huawei_ce huawei_vrp_s juniper_junos juniper_srx linux
mikrotik_ros7 paloalto_panos ruckus_fastiron ruijie_rgos sonicwall_sonicos sophos_sfos tplink_jetstream""".split())
WRITE = re.compile(r"^\s*(system-view|configure|config |conf t|set |delete |undo |reset |reboot|restart|shutdown|save|commit|"
                   r"write |copy |modify |create |tmsh (create|modify|delete|save)|execute (reboot|factoryreset|formatlogdisk|restore|shutdown)|execute .*\b(add|clear|delete|disk-quota|reset|set)\b)", re.I)
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
SAFE_IP = re.compile(r"^(10\.0\.0\.|192\.0\.2\.|198\.51\.100\.|203\.0\.113\.|0\.0\.0\.0|255\.|127\.0\.0\.1|224\.)")
SECRET = re.compile(r"(password|passwd|secret|community|pre-shared|psk)\s+(?!<)\S{3,}", re.I)
NEGATE = re.compile(r"ไม่มีจริง|ไม่ใช่|ห้าม|ไม่เกี่ยว|≠|แทน|ผิด")


def load_bad() -> list:
    """tools/known_bad.tsv: ระดับ / families / regex / ที่ถูก — คำสั่งที่เคยแต่งขึ้นใน PR ก่อนๆ"""
    rules = []
    f = ROOT / "tools" / "known_bad.tsv"
    if not f.exists():
        return rules
    for n, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if not ln.strip() or ln.startswith("#"):
            continue
        parts = ln.split("\t")
        if len(parts) != 4 or parts[0] not in ("ERROR", "WARN"):
            raise SystemExit(f"known_bad.tsv บรรทัด {n}: ต้องมี 4 ช่องคั่นด้วย TAB (ระดับ, families, regex, ข้อความ)")
        rules.append((parts[0], parts[1].strip(), re.compile(parts[2], re.I), parts[3].strip()))
    return rules


BAD = load_bad()


def check(p: pathlib.Path, ids: dict) -> tuple[list, list]:
    err, warn = [], []
    t = p.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", t, re.S)
    if not m:
        return ["ไม่มีหัวไฟล์ --- ... ---"], []
    head = dict(re.findall(r"^(\w+):[ \t]*(.*?)[ \t]*(?:#.*)?$", m.group(1), re.M))
    for k in ("id", "title", "versions", "sources"):
        if not head.get(k):
            err.append(f"หัวไฟล์ไม่มี {k}")
    if not head.get("triggers"):
        err.append("หัวไฟล์ไม่มี triggers (เคสที่พิมพ์ถามโดยไม่ผูกอุปกรณ์จะไม่ได้ playbook นี้)")
    pid = head.get("id", "")
    if pid in BUILTIN:
        err.append(f"id '{pid}' ซ้ำกับ playbook ที่มากับโปรแกรม")
    if pid in ids:
        err.append(f"id '{pid}' ซ้ำกับ {ids[pid]}")
    ids[pid] = p.name
    for f in [x.strip() for x in head.get("families", "").split(",") if x.strip()]:
        if f not in FAMILIES:
            err.append(f"families '{f}' ไม่มีในโปรแกรม")
    if p.name.startswith("_"):
        warn.append("ชื่อไฟล์ขึ้นต้นด้วย _ โปรแกรมจะไม่โหลด")
    huawei_s = "huawei_vrp_s" in head.get("families", "")
    secs = re.split(r"^## ", t[m.end():], flags=re.M)[1:]
    if not secs:
        err.append("ไม่มีหัวข้อ ## เลย")
    for s in secs:
        name = s.splitlines()[0].strip()
        tag = f"[{name[:40]}]"
        if " — " in name:
            err.append(f"{tag} ชื่อหัวข้อมี ' — '")
        if not re.search(r"^คำค้น:\s*\S", s, re.M):
            err.append(f"{tag} ไม่มีบรรทัด คำค้น:")
        src = re.search(r"^ที่มา:.*", s, re.M)
        if not src:
            err.append(f"{tag} ไม่มีบรรทัด ที่มา:")
        elif "https://" not in src.group(0):
            warn.append(f"{tag} ที่มา: ไม่มี URL https://")
        if len(s) > 2600:
            err.append(f"{tag} ยาว {len(s)} ตัวอักษร (เกิน ~2,500 ให้แยกหัวข้อ)")
        blk = re.search(r"^คำสั่งตรวจ:\s*\n```[^\n]*\n(.*?)```", s, re.S | re.M)
        if not blk and not re.search(r"(?m)^ตรวจใน (GUI|Controller)\s*:", s):
            err.append(f"{tag} ไม่มีบล็อก คำสั่งตรวจ: (อ่านอย่างเดียว) — ย้าย config ไป 'วิธีแก้' แล้วใส่ show / get / display แทน อย่าลบบล็อก (อุปกรณ์ที่ตรวจได้แค่ทาง GUI ใช้บรรทัด 'ตรวจใน GUI:' แทน)")
        fences = [m.start() for m in re.finditer(r"(?m)^[ \t]*```", s)]   # รวมบล็อกที่ย่อหน้า (เคยหลุดใน PR #17–19)
        for k in range(0, len(fences) - 1, 2):                       # ทุกบล็อกโค้ดต้องเป็น "คำสั่งตรวจ:" (โปรแกรมอ่านทุกบรรทัดในบล็อกเป็นคำสั่ง)
            prev = s[:fences[k]].rstrip("\n").rsplit("\n", 1)[-1].strip()
            if not prev.startswith("คำสั่งตรวจ"):
                err.append(f"{tag} มีบล็อกโค้ดที่ไม่ใช่ คำสั่งตรวจ: (บรรทัดก่อนบล็อก: '{prev[:30]}') — คำสั่ง config ใส่ใน `...` ในวิธีแก้, ตัวอย่าง output ห้ามใส่")
        if re.search(r"[\u4e00-\u9fff\u3040-\u30ff]", s):
            err.append(f"{tag} มีอักษรจีน / ญี่ปุ่นปน — ใช้ไทย / อังกฤษเท่านั้น")
        if re.search(r"ตัวอย่าง\s*output|example output|sample output", s, re.I):
            err.append(f"{tag} มี 'ตัวอย่าง output' — ห้ามใส่ output ที่ไม่ได้คัดลอกจากเอกสาร (LESSONS)")
        if huawei_s and any(re.search(r"\bcommit\b", ln) and not re.search(r"ไม่ต้อง|ไม่มี|ไม่ใช้|ห้าม", ln) for ln in s.splitlines()):
            err.append(f"{tag} มี `commit` — Huawei S series (VRP V200) คำสั่งมีผลทันที ไม่มี commit (ใช้ save)")
        if blk:
            for line in blk.group(1).splitlines():
                if WRITE.search(line):
                    err.append(f"{tag} คำสั่งตรวจไม่ใช่อ่านอย่างเดียว: {line.strip()[:60]}")
                if SECRET.search(line):
                    err.append(f"{tag} มีรหัส / community ในคำสั่งตรวจ")
    fams = head.get("families", "")
    for n, ln in enumerate(t.splitlines(), 1):
        if NEGATE.search(ln) or re.match(r"(triggers|คำค้น):", ln):   # คำที่ผู้ใช้อาจพิมพ์ค้น ไม่ใช่คำแนะนำ
            continue
        for lvl, scope, rx, fix in BAD:
            if scope != "*" and not any(x.strip() in fams for x in scope.split(",")):
                continue
            hit = rx.search(ln)
            if hit:
                (err if lvl == "ERROR" else warn).append(f"บรรทัด {n}: '{hit.group(0).strip()[:40]}' — {fix}")
    for ip in IPV4.findall(t):
        if not SAFE_IP.match(ip) and not ip.startswith("0."):
            warn.append(f"พบ IP {ip} — ถ้าเป็นของลูกค้าให้เปลี่ยนเป็น 10.0.0.x / <ip>")
    for x in SECRET.findall(t):
        warn.append(f"พบคำว่า '{x}' ตามด้วยค่า — ตรวจว่าไม่ใช่รหัสจริง")
    return err, sorted(set(warn))


def main():
    files = [pathlib.Path(a) for a in sys.argv[1:]] or sorted((ROOT / "playbooks").glob("*.md"))
    ids, bad = {}, 0
    for p in files:
        e, w = check(p, ids)
        print(("FAIL " if e else "ok   ") + p.name)
        for x in e:
            print("  ERROR", x)
        for x in w:
            print("  WARN ", x)
        bad += bool(e)
    print(f"\nตรวจ {len(files)} ไฟล์, ต้องแก้ {bad} ไฟล์")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
