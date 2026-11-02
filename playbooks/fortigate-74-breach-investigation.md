---
id: fortigate-74-breach-investigation
title: FortiGate 7.4: ตรวจว่าตัวเครื่องถูกบุกรุกหรือไม่
families: fortinet_fortios
triggers: fortigate ตรวจถูกบุกรุก, fortigate intrusion investigation, fortigate admin user not known, fortigate unauthorized config change, fortigate abnormal admin login, fortigate psirt advisory investigation
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/668197/log-related-diagnose-commands, https://www.fortiguard.com/psirt
---

# FortiGate 7.4: ตรวจว่าตัวเครื่องถูกบุกรุกหรือไม่

คำค้น: fortigate ตรวจถูกบุกรุก, fortigate intrusion investigation, fortigate admin user not known
อาการ: ต้องตรวจหาหลักฐานว่าตัว FortiGate 7.4 ถูกบุกรุกหรือไม่ โดยตรวจสอบ admin user, การเปลี่ยน config ที่ผิดปกติ, และการ login ที่ผิดปกติ

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
ที่มา: [config system admin — FortiGate 7.4.0 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/13620/config-system-admin) (ดูคำสั่งที่เกี่ยวข้องในหน้า config system admin)
วิธีแก้:
- **ก่อนลบ ต้องสำรอง config และ log** เพื่อเก็บเป็นหลักฐาน: `execute backup full tftp <server-ip> backup-$(date).bak`
- แล้วลบ: `config system admin`, `delete "<admin_name>"`, `end`
- ระบุ account ที่ลบและสอบสวนว่ามาจากที่ไหน
- หากบัญชีนั้นจำเป็น แต่ลืมลงทะเบียน ให้เพิ่มข้อมูล: `edit "<admin_name>"`, `set two-factor fortitoken`, `set fortitoken <serial>`, `end`
ที่มา: [config system admin — FortiGate 7.4.0 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/13620/config-system-admin)

---

## 2. ตรวจการเปลี่ยน config ที่ผิดปกติ

คำค้น: fortigate config change log, fortigate abnormal config change
อาการ: ต้องตรวจว่ามี config change ที่ผิดปกติหรือไม่

คำสั่งตรวจ:
```
execute log filter device disk
execute log filter category event
execute log filter field action login
execute log display
```
อ่านผล:
- ดูว่ามี config change ที่ไม่เป็นที่รู้จักหรือไม่ (เปลี่ยน rule, เพิ่ม service, เปิด feature)
- หากมี config change จาก admin account ที่ไม่รู้จัก = เป็นสัญญาณการถูกบุกรุก
ที่มา: [Log-related diagnostic commands — FortiGate 7.4.0 Administration Guide](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/668197/log-related-diagnose-commands)
วิธีแก้:
- หากตรวจพบ config change ที่ผิดปกติ ให้กู้คืนจาก backup ที่สำรองไว้
- **คำเตือน:** `execute restore` จะทำให้เครื่อง reboot — หากเป็น HA ต้องวางแผนหยุดบริการล่วงหน้า และทำบน secondary ก่อนแล้วค่อย failover
- ระบุ admin account ที่ทำการ change และสอบสวนบัญชีนั้น

---

## 3. ตรวจการ login admin ที่ผิดปกติ

คำค้น: fortigate abnormal admin login, fortigate login history investigation
อาการ: ต้องตรวจว่าการ login admin เป็นไปอย่างปกติหรือไม่

คำสั่งตรวจ:
```
execute log filter device disk
execute log filter category event
execute log filter field action login
execute log display
```
อ่านผล:
- ดูว่ามีการ login จาก IP ที่ไม่เป็นที่รู้จักหรือไม่
- หากมีการ login จาก IP ที่ไม่เป็นที่รู้จัก = เป็นสัญญาณการถูกบุกรุก
ที่มา: [Log-related diagnostic commands — FortiGate 7.4.0 Administration Guide](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/668197/log-related-diagnose-commands)
วิธีแก้:
- หากตรวจพบ login จาก IP ที่ผิดปกติ ให้บล็อก IP โดยอ้างอิงขั้นตอนจาก `fortigate-74-harden-admin.md` ข้อ 1 (Trusted Hosts) และข้อ 5 (Local-in Policy)
- ตรวจสอบ admin account ที่ใช้ login และเปลี่ยนรหัสผ่านทันที

---

## 4. ตรวจตาม Fortinet PSIRT Advisory

คำค้น: fortigate psirt advisory investigation, fortigate vulnerability check, fortigate psirt
อาการ: ต้องตรวจว่ามีช่องโหว่ที่ถูก exploit หรือไม่

คำสั่งตรวจ:
```
get system status
```
อ่านผล:
- ดูว่า FortiGate กำลังใช้เวอร์ชันที่มีช่องโหว่หรือไม่
- ตรวจสอบว่ามีการติดตั้ง hotfix หรือ upgrade แล้วหรือไม่
ที่มา: [Fortinet PSIRT](https://www.fortiguard.com/psirt)
วิธีแก้:
- **คำเตือนเกี่ยวกับ HA:** หากเป็นคู่ HA ต้อง upgrade ตามลำดับ — ทำบน secondary ก่อน, รอให้ sync เสร็จ, ทำ failover, แล้วค่อย upgrade unit ที่กลายเป็น secondary
- หากตรวจพบช่องโหว่ ให้ดู upgrade path จาก PSIRT advisory
- หากมีการ exploit แล้ว ให้กู้คืนจาก backup

---
