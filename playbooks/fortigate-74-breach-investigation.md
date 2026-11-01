---
id: fortigate-74-breach-investigation
title: FortiGate 7.4 — ตรวจว่าอุปกรณ์ขอบเครือข่ายโดนเจาะแล้วหรือยัง
families: fortinet_fortios
triggers: fortigate breach investigate, fortigate compromised check, fortigate threat detection, fortigate security event review
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/668197/log-related-diagnose-commands
---

# FortiGate 7.4 — ตรวจว่าอุปกรณ์ขอบเครือข่ายโดนเจาะแล้วหรือยัง

คำค้น: fortigate breach investigate, fortigate compromised check, fortigate threat detection, fortigate security event review
อาการ: ได้รับแจ้งว่าอุปกรณ์ขอบเครือข่ายอาจโดนโจมตีหรือเจาะระบบ — ต้องตรวจสอบ security event, log, session ว่ามีเหตุการณ์ผิดปกติหรือไม่

---

## 1. ตรวจ FortiView / ภาพรวมการโจมตี

คำค้น: fortigate fortiview top threats, fortigate security events dashboard, fortigate top talkers
อาการ: ต้องดูภาพรวมการโจมตีจาก FortiView — ใช้เป็นจุดเริ่มต้นที่ดีสุด

คำสั่งตรวจ:
```
# FortiView มีเฉพาะใน GUI ไม่มีคำสั่ง CLI
```

ตรวจใน GUI:
- *Dashboard > FortiView > Top Threats* — ดู top 10 threats ทั้งหมด
- *FortiView > Sources* — ดู source IP ที่เป็น top attacker
- *FortiView > Top Talkers* — ดู top IP ที่ส่ง traffic มากที่สุด (อาจเป็น compromised host)
- *FortiView > Top Applications* — ดู application ที่ใช้ traffic มากที่สุด

ที่มา: [FortiGate / FortiOS 7.4 Administration Guide — Dashboards and Monitors](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/345190/dashboards-and-monitors)

---

## 2. ตรวจ Security Events Log / Malware, IPS, Web Filter

คำค้น: fortigate security events log page, fortigate log viewer security, fortigate fortiview security log
อาการ: ต้องดู security events (Malware, IPS, Web Filter, Email) ทั้งหมดจาก log viewer

คำสั่งตรวจ:
```
# Security Events Log มีเฉพาะใน GUI ไม่มีคำสั่ง CLI
```

ตรวจใน GUI:
- *Log & Report > Security Events* — ดูเหตุการณ์ security ทั้งหมด
- *Summary* tab — ดู 5 เหตุการณ์ที่พบบ่อยที่สุด
- *Logs* tab — ดูรายละเอียดแต่ละเหตุการณ์
- ดูว่า event ใดที่ถูก `action=block` (ดี) หรือ `action=passthrough` (อาจหลุด)

ที่มา: [Security Events log page — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/876272/security-events-log-page)

---

## 3. ตรวจ Log แต่ละหมวดด้วย Execute Log Filter / Traffic, IPS, AV, Web Filter, Event

คำค้น: fortigate execute log filter field, fortigate log filter category, fortigate log viewer CLI
อาการ: ต้องตรวจ log แต่ละหมวดแยกกันด้วย CLI

คำสั่งตรวจ:
```
execute log filter field logtype all
```

อ่านผล:
- ต้องเห็น log ทุกหมวด (traffic, event, virus, webfilter, ips, emailfilter, anomaly)
- logtype=all = แสดง log ทุกหมวด

ที่มา: [Log-related diagnostic commands — FortiOS 7.4.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/668197/log-related-diagnose-commands)

---

## 4. ตรวจ FortiView / Top Talkers และ Sessions

คำค้น: fortigate fortiview top talkers, fortigate top source ip, fortigate active session investigation
อาการ: ต้องดูว่า host ใดใน network คุยกับ IP ภายนอกที่ผิดปกติ — อาจเป็น compromised host ที่กำลังส่งข้อมูลออก

คำสั่งตรวจ:
```
diagnose sys session filter clear
```

อ่านผล:
- ต้องเห็น session ทั้งหมดที่ปิด filter

ที่มา: [Log-related diagnostic commands — FortiOS 7.4.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/668197/log-related-diagnose-commands)

---

## 5. ตรวจ Active Sessions / Connections ที่น่าสงสัย

คำค้น: fortigate diagnose sys session list, fortigate active sessions check, fortigate suspicious session
อาการ: ต้องดูว่า sessions ที่กำลังเปิดอยู่ มี connections จากภายนอกที่ไม่ได้รับอนุญาต หรือ connections ที่ผิดปกติหรือไม่

คำสั่งตรวจ:
```
diagnose sys session filter clear
diagnose sys session list
```

อ่านผล:
- ต้องเห็น session ที่มาจาก IP ภายนอก และไป destination port ที่ไม่ปกติ
- ต้องเห็น session ที่มี source port สูง (อาจเป็น reverse shell)
- ต้องเห็น session ที่มี duration ยาว (>1 ชม.) จาก IP ภายนอก
- ต้องเห็น session จาก IP ที่ไม่น่าเชื่อถือ

ที่มา: [Log-related diagnostic commands — FortiOS 7.4.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/668197/log-related-diagnose-commands)

---

## 6. สรุป / การตอบสนองเบื้องต้น

คำค้น: fortigate incident response, fortigate block compromised ip, fortigate quarantine infected
อาการ: เมื่อพบเหตุการณ์ที่น่าสงสัย ต้องดำเนินการตอบสนองทันที

คำสั่งตรวจ:
```
diagnose sys session list
```

อ่านผล:
- ต้องเห็น session ที่กำลังเปิดอยู่ทั้งหมด
- ใช้สรุปว่า host ใดกำลังคุยกับ IP ที่ผิดปกติ

วิธีแก้:
1. **หยุดการแพร่กระจาย** — กักเครื่องทันที: `diagnose user quarantine add src4 <IP-CLIENT> <expiry> admin` — อ้าง playbook: `fortigate-74-ransomware-response` §1
2. **บล็อก IOC** — เพิ่ม Threat Feed: อ้าง playbook: `fortigate-74-ransomware-response` §2
3. **ตรวจสอบการเข้าถึงเพิ่มเติม** — เปลี่ยน password admin, ตรวจสอบ admin accounts: อ้าง playbook: `fortigate-74-harden-admin` §1
4. **ตรวจสอบความเสียหาย** — ตรวจสอบว่าข้อมูลสำคัญถูกลักลอบออกไปหรือไม่ — ดู FortiView > Top Talkers > ดู destination IP

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

ที่มา: [Log-related diagnostic commands — FortiOS 7.4.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/668197/log-related-diagnose-commands)

- การตรวจว่าอุปกรณ์โดนเจาะหรือไม่ ต้องดู FortiView เป็นจุดเริ่มต้น (GUI-only)
- ใช้ FortiView > Top Threats และ Top Talkers ดูภาพรวมการโจมตี
- ใช้ FortiView > Security Events ดูเหตุการณ์ security ทั้งหมด (GUI-only)
- ใช้ `execute log filter field` เพื่อกรอง log แต่ละหมวด
- ใช้ `diagnose sys session list` ดู sessions ที่กำลังเปิดอยู่
- สำหรับบล็อก IP และกักเครื่อง → อ้าง playbook: `fortigate-74-ransomware-response`
- สำหรับตรวจ admin account → อ้าง playbook: `fortigate-74-harden-admin`
- สำหรับ log backup → อ้าง playbook: `fortigate-74-harden-system`
