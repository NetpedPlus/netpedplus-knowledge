---
id: fortigate-74-breach-investigation
title: FortiGate 7.4: ตรวจ security event / log / session หลังได้รับแจ้งเหตุ
families: fortinet_fortios
triggers: fortigate security event review, fortigate log filter, fortigate session check, fortigate fortiview browse
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/876272/security-events-log-page, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/668197/log-related-diagnose-commands, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/345190/dashboards-and-monitors, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/562859/using-a-session-table
---

# FortiGate 7.4: ตรวจ security event / log / session หลังได้รับแจ้งเหตุ

คำค้น: fortigate security event review, fortigate log filter, fortigate session check, fortigate fortiview browse
อาการ: ได้รับแจ้งเหตุแล้วต้องตรวจ security event, log, session ว่ามีกิจกรรมผิดปกติในเครือข่ายหรือไม่

---

## 1. ตรวจ FortiView / ภาพรวมเครือข่าย (GUI-only)

คำค้น: fortigate fortiview sources, fortiview sessions
อาการ: ต้องดูภาพรวม network จาก FortiView — ใช้เป็นจุดเริ่มต้นเมื่อได้รับแจ้งเหตุ

คำสั่งตรวจ:
```
# FortiView มีเฉพาะใน GUI ไม่มีคำสั่ง CLI
```

ตรวจใน GUI:
- *Dashboard > FortiView Sources* — ดู source ที่ traffic มากสุด / เรียงตาม Threat Score ได้
- *Dashboard > FortiView Sessions* — ดู sessions ทั้งหมด
- อ้าง playbook: `fortigate-74-ransomware-response` §5 สำหรับการไล่ log ของเครื่องเป้าหมาย

ที่มา: [FortiView monitors — FortiOS 7.4.0](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/433781/fortiview-monitors)

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
- `device disk` = อ่าน log จาก disk
- `category event` = เลือกหมวด event log
- `field action login` = กรองเฉพาะ login events
- `log display` = แสดง log ที่ filter แล้ว

ที่มา: [Log-related diagnostic commands — FortiOS 7.4.4](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/668197/log-related-diagnose-commands)

---

## 4. ตรวจ Active Sessions / Connections ที่น่าสงสัย

คำค้น: fortigate diagnose sys session list, fortigate active sessions check, fortigate suspicious session, fortigate diagnose sys session filter
อาการ: ต้องดูว่า sessions ที่กำลังเปิดอยู่ มี connections จากภายนอกหรือไม่

คำสั่งตรวจ:
```
diagnose sys session filter clear
diagnose sys session list
```

อ่านผล:
- ต้องเห็น session ทั้งหมดที่ open อยู่
- ดูว่า session ใดมาจาก IP ภายนอก
- ดูว่า session ใดมี destination port ที่ไม่ปกติ

ที่มา: [Using a session table — FortiOS 7.4.2](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/562859/using-a-session-table)

---

## 5. สรุป / การอ้างอิง playbook อื่น

คำค้น: fortigate incident response, fortigate block compromised ip
อาการ: เมื่อพบเหตุการณ์ที่น่าสงสัย ต้องดำเนินการอ้างอิง playbook อื่นที่เกี่ยวข้อง

คำสั่งตรวจ:
```
diagnose sys session list
```

อ่านผล:
- ต้องเห็น session ที่กำลังเปิดอยู่ทั้งหมด

ตรวจใน GUI:
- *Dashboard > FortiView Sources* — ดู source ที่ traffic มากสุด

วิธีแก้:
1. **หยุดการแพร่กระจาย** — กักเครื่อง/บล็อก IP: อ้าง playbook: `fortigate-74-ransomware-response` §1
2. **บล็อก IOC** — เพิ่ม Threat Feed: อ้าง playbook: `fortigate-74-ransomware-response` §2
3. **ตรวจสอบการเข้าถึงเพิ่มเติม** — ตรวจ admin account: อ้าง playbook: `fortigate-74-harden-admin` §1
4. **ตรวจสอบ log ย้อนหลัง** — ไล่ log ของเครื่องเป้าหมาย: อ้าง playbook: `fortigate-74-ransomware-response` §5

ที่มา: [Using a session table — FortiOS 7.4.2](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/562859/using-a-session-table)

---

## บทเรียน

คำค้น: fortigate breach investigation lessons
อาการ: บทเรียนจากการตรวจ security event / log / session

คำสั่งตรวจ:
```
diagnose sys session list
```

อ่านผล:
- ต้องเห็น session ที่กำลังเปิดอยู่ทั้งหมด

ที่มา: [Using a session table — FortiOS 7.4.2](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/562859/using-a-session-table)

- FortiView มีเฉพาะใน GUI — ไม่มีคำสั่ง CLI
- ใช้ `Dashboard > FortiView Sources` ดู source ที่ traffic มากสุด / เรียงตาม Threat Score
- ใช้ `Dashboard > FortiView Sessions` ดู sessions ทั้งหมด
- ใช้ *Log & Report > Security Events* ดูเหตุการณ์ security ทั้งหมด
- ใช้ `execute log filter device disk` + `category` + `field` + `log display` เพื่อกรอง log แต่ละหมวด
- ใช้ `diagnose sys session list` ดู sessions ที่กำลังเปิดอยู่
- หากไม่มี log disk / remote log FortiView จะดึงจาก session table และช่วงเวลาค่าเริ่มต้นเป็น Now ([Using the FortiView interface — FortiOS 7.4.1](https://docs.fortinet.com/document/fortigate/7.4.1/administration-guide/96300/using-the-fortiview-interface))
- สำหรับบล็อก IP และกักเครื่อง → อ้าง playbook: `fortigate-74-ransomware-response`
- สำหรับตรวจ admin account → อ้าง playbook: `fortigate-74-harden-admin`
- สำหรับ log backup → อ้าง playbook: `fortigate-74-harden-system`
