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
                   r"write |copy |modify |create |tmsh (create|modify|delete|save)|execute (reboot|factoryreset|formatlogdisk))", re.I)
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
SAFE_IP = re.compile(r"^(10\.0\.0\.|192\.0\.2\.|198\.51\.100\.|203\.0\.113\.|0\.0\.0\.0|255\.|127\.0\.0\.1|224\.)")
SECRET = re.compile(r"(password|passwd|secret|community|pre-shared|psk)\s+(?!<)\S{3,}", re.I)


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
        if blk:
            for line in blk.group(1).splitlines():
                if WRITE.search(line):
                    err.append(f"{tag} คำสั่งตรวจไม่ใช่อ่านอย่างเดียว: {line.strip()[:60]}")
                if SECRET.search(line):
                    err.append(f"{tag} มีรหัส / community ในคำสั่งตรวจ")
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
