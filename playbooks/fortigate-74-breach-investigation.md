---
id: fortigate-74-breach-investigation
title: FortiGate 7.4 — ตรวจว่าอุปกรณ์ขอบเครือข่ายโดนเจาะแล้วหรือยัง
families: fortinet_fortios
triggers: fortigate breach investigate, fortigate compromised check, fortigate threat detection, fortigate security event review
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/876272/security-events-log-page, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/668197/log-related-diagnose-commands, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/345190/dashboards-and-monitors
---

# FortiGate 7.4 — ตรวจว่าอุปกรณ์ขอบเครือข่ายโดนเจาะแล้วหรือยัง

คำค้น: fortigate breach investigate, fortigate compromised check, fortigate threat detection, fortigate security event review
อาการ: ได้รับแจ้งว่าอุปกรณ์ขอบเครือข่ายอาจโดนโจมตีหรือเจาะระบบ — ต้องตรวจสอบ security event, log, session ว่ามีเหตุการณ์ผิดปกติหรือไม่

---

## 1. ตรวจ FortiView / ภาพรวมการโจมตี (GUI-only)

คำค้น: fortigate fortiview sources, fortiview sessions, fortiview top source destination, fortiview cloud application
อาการ: ต้องดูภาพรวมการโจมตีจาก FortiView — ใช้เป็นจุดเริ่มต้นที่ดีสุด

คำสั่งตรวจ:
```
# FortiView มีเฉพาะใน GUI ไม่มีคำสั่ง CLI
```

ตรวจใน GUI:
- *Dashboard > FortiView > FortiView Sources* — ดู source IP ที่เป็น top attacker
- *Dashboard > FortiView > FortiView Sessions* — ดู sessions ทั้งหมด
- *Dashboard > FortiView > Top Source and Top Destination Firewall Objects monitors* — ดู IP ที่ส่ง/receive traffic มากที่สุด
- *Dashboard > FortiView > Cloud Application View* — ดู cloud application ที่ใช้ traffic มากที่สุด

ที่มา: [Dashboards and Monitors — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/345190/dashboards-and-monitors)

---

## 2. ตรวจ Security Events Log (GUI-only)

คำค้น: fortigate security events log page, fortigate log viewer security, fortigate security event
อาการ: ต้องดู security events (Malware, IPS, Web Filter, Email) ทั้งหมดจาก log viewer

คำสั่งตรวจ:
```
# Security Events Log มีเฉพาะใน GUI ไม่มีคำสั่ง CLI
```

ตรวจใน GUI:
- *Log & Report > Security Events* — ดูเหตุการณ์ security ทั้งหมด
- *Summary* tab — ดูเหตุการณ์ที่พบบ่อยที่สุด
- *Logs* tab — ดูรายละเอียดแต่ละเหตุการณ์

ที่มา: [Security Events log page — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/876272/security-events-log-page)

---

## 3. ตรวจ Log แต่ละหมวดด้วย Execute Log Filter

คำค้น: fortigate execute log filter device disk, execute log filter category, execute log filter field, execute log display
อาการ: ต้องตรวจ log แต่ละหมวดแยกกันด้วย CLI

คำสั่งตรวจ:
```
execute log filter device disk
execute log filter category event
execute log filter field action login
execute log display
```

อ่านผล:
- `device disk` = ดู log จาก disk (device = 0, disk = 1, fortianalyzer = 2)
- `category event` = ดู event log (login/logout events)
- `field action login` = กรองเฉพาะ login events
- `log display` = แสดง log ที่ filter แล้ว

ที่มา: [Log-related diagnostic commands — FortiOS 7.4.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/668197/log-related-diagnose-commands)

---

## 4. ตรวจ Active Sessions / Connections ที่น่าสงสัย

คำค้น: fortigate diagnose sys session list, fortigate active sessions check, fortigate suspicious session, fortigate diagnose sys session filter
อาการ: ต้องดูว่า sessions ที่กำลังเปิดอยู่ มี connections จากภายนอกที่ไม่ได้รับอนุญาต หรือ connections ที่ผิดปกติหรือไม่

คำสั่งตรวจ:
```
diagnose sys session filter clear
diagnose sys session list
```

อ่านผล:
- ต้องเห็น session ทั้งหมดที่ open อยู่
- ดูว่า session ใดมาจาก IP ภายนอก
- ดูว่า session ใดมี destination port ที่ไม่ปกติ

ที่มา: [Log-related diagnostic commands — FortiOS 7.4.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/668197/log-related-diagnose-commands)

---

## 5. สรุป / การตอบสนองเบื้องต้น

คำค้น: fortigate incident response, fortigate block compromised ip, fortigate quarantine infected
อาการ: เมื่อพบเหตุการณ์ที่น่าสงสัย ต้องดำเนินการตอบสนองทันที

คำสั่งตรวจ:
```
diagnose sys session list
```

อ่านผล:
- ต้องเห็น session ที่กำลังเปิดอยู่ทั้งหมด

ตรวจใน GUI:
- *Dashboard > FortiView > FortiView Sources* — ดู top attacker

วิธีแก้:
1. **หยุดการแพร่กระจาย** — กักเครื่อง/บล็อก IP: อ้าง playbook: `fortigate-74-ransomware-response` §1
2. **บล็อก IOC** — เพิ่ม Threat Feed: อ้าง playbook: `fortigate-74-ransomware-response` §2
3. **ตรวจสอบการเข้าถึงเพิ่มเติม** — เปลี่ยน password admin: อ้าง playbook: `fortigate-74-harden-admin` §1
4. **ตรวจสอบความเสียหาย** — ดู FortiView > FortiView Sessions > ดู top talkers

ที่มา: [FortiOS 7.4 Ransomware Response Playbook](https://github.com/NetpedPlus/netpedplus-knowledge/blob/main/playbooks/fortigate-74-ransomware-response.md)

---

## บทเรียน

คำค้น: fortigate breach investigation lessons, fortigate security event check, fortigate fortiview guide
อาการ: บทเรียนจากการตรวจว่าอุปกรณ์โดนเจาะหรือไม่

คำสั่งตรวจ:
```
diagnose sys session list
```

อ่านผล:
- ต้องเห็น session ที่กำลังเปิดอยู่ทั้งหมด

ตรวจใน GUI:
- *Log & Report > Security Events* — ดูเหตุการณ์ security ทั้งหมด
- *Dashboard > FortiView > FortiView Sources* — ดู top attacker
- *Dashboard > FortiView > FortiView Sessions* — ดู sessions ทั้งหมด

ที่มา: [Security Events log page — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/876272/security-events-log-page)

- การตรวจว่าอุปกรณ์โดนเจาะหรือไม่ ต้องดู FortiView เป็นจุดเริ่มต้น (GUI-only)
- ใช้ FortiView > FortiView Sources ดู top attacker
- ใช้ FortiView > FortiView Sessions ดู sessions ทั้งหมด
- ใช้ FortiView > Top Source and Top Destination Firewall Objects monitors ดู top IP
- ใช้ FortiView > Cloud Application View ดู cloud application ที่ใช้ traffic มาก
- ใช้ *Log & Report > Security Events* ดูเหตุการณ์ security ทั้งหมด
- ใช้ `execute log filter device disk` + `category` + `field` + `log display` เพื่อกรอง log แต่ละหมวด
- ใช้ `diagnose sys session list` ดู sessions ที่กำลังเปิดอยู่
- สำหรับบล็อก IP และกักเครื่อง → อ้าง playbook: `fortigate-74-ransomware-response`
- สำหรับตรวจ admin account → อ้าง playbook: `fortigate-74-harden-admin`
- สำหรับ log backup → อ้าง playbook: `fortigate-74-harden-system`
