---
id: fortigate-74-breach-investigation
title: FortiGate 7.4: ตรวจว่าตัวเครื่องถูกบุกรุกหรือไม่
families: fortinet_fortios
triggers: fortigate ตรวจถูกบุกรุก, fortigate intrusion investigation, fortigate admin user not known, fortigate psirt advisory investigation
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/13620/config-system-admin
---

# FortiGate 7.4: ตรวจว่าตัวเครื่องถูกบุกรุกหรือไม่

คำค้น: fortigate ตรวจถูกบุกรุก, fortigate intrusion investigation, fortigate admin user not known
อาการ: ต้องตรวจหาหลักฐานว่าตัว FortiGate 7.4 ถูกบุกรุกหรือไม่ โดยตรวจสอบ admin user และตรวจตาม PSIRT advisory

---

## 1. ตรวจหา admin user ที่ไม่รู้จัก

คำค้น: fortigate admin user not known, fortigate list admin accounts
อาการ: ต้องตรวจว่ามี admin account ที่ไม่รู้จักหรือไม่

คำสั่งตรวจ:
```
get system admin
```
อ่านผล:
- ดูว่าทุก admin account เป็นบัญชีที่รู้จักหรือไม่ (ชื่อ, serial ของ token ถ้ามี)
- หากมี account ที่ไม่รู้จัก = ต้องสอบสวนต่อ
ที่มา: [config system admin — FortiGate 7.4.0 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/13620/config-system-admin)
วิธีแก้:
- หากตรวจพบ admin account ที่ไม่รู้จัก ให้ลบ: `config system admin`, `delete "<admin_name>"`, `end`
- ระบุ account ที่ลบและสอบสวนว่ามาจากที่ไหน
ที่มา: [config system admin — FortiGate 7.4.0 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/13620/config-system-admin)

---

## 2. ตรวจตาม Fortinet PSIRT Advisory

คำค้น: fortigate psirt advisory investigation, fortigate vulnerability check, fortigate psirt
อาการ: ต้องตรวจว่ามีช่องโหว่ที่ถูก exploit หรือไม่

คำสั่งตรวจ:
```
get system status
```
อ่านผล:
- ดูว่า FortiGate กำลังใช้เวอร์ชันที่มีช่องโหว่หรือไม่
- ตรวจสอบว่ามีการติดตั้ง hotfix หรือ upgrade แล้วหรือไม่
ที่มา: Fortinet PSIRT — ค้น advisory ที่เกี่ยวกับเวอร์ชันของเครื่อง
วิธีแก้:
- หากตรวจพบช่องโหว่ ให้ดู upgrade path จาก PSIRT advisory
- หากต้อง upgrade คู่ HA ให้ทำตามขั้นตอนใน [Upgrading FortiGates in an HA cluster — FortiGate 7.4.0 Administration Guide](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/247944/upgrading-fortigates-in-an-ha-cluster)
