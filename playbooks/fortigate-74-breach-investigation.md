---
id: fortigate-74-breach-investigation
title: FortiGate 7.4: ตรวจว่าตัวเครื่องถูกบุกรุกหรือไม่
families: fortinet_fortios
triggers: fortigate ตรวจถูกบุกรุก, fortigate intrusion investigation, fortigate admin user not known, fortigate unauthorized config change, fortigate abnormal admin login, fortigate psirt advisory investigation
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortios/7.4.0/administration-guide/480747/administration-logs, https://docs.fortinet.com/document/fortios/7.4.0/cli-reference/77317/log-feature-table, https://docs.fortinet.com/document/fortios/7.4.0/cli-reference/001620/config-system-admin, https://www.fortiguard.com/psirt
---

# FortiGate 7.4: ตรวจว่าตัวเครื่องถูกบุกรุกหรือไม่

คำค้น: fortigate ตรวจถูกบุกรุก, fortigate intrusion investigation, fortigate admin user not known
อาการ: ต้องตรวจหาหลักฐานว่าตัว FortiGate 7.4 ถูกบุกรุกหรือไม่ โดยตรวจสอบ admin user, การเปลี่ยน config ที่ผิดปกติ, และการ login ที่ผิดปกติ

---

## 1. ตรวจหา admin user ที่ไม่รู้จัก

คำค้น: fortigate admin user not known, fortigate list admin accounts, fortigate show system admin
อาการ: ต้องตรวจว่ามี admin account ที่ไม่รู้จักหรือไม่

คำสั่งตรวจ:
```
get system admin
```
อ่านผล:
- ดูว่าทุก admin account เป็นบัญชีที่รู้จักหรือไม่ (ชื่อ, serial ของ token ถ้ามี)
- หากมี account ที่ไม่รู้จัก = ต้องสอบสวนต่อ
- บัญชีฉุกเฉิน (break-glass) ที่ไม่เปิด MFA ต้องมี trusthost จำกัด และเก็บรหัสไว้ใน vault
ที่มา: [config system admin — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortios/7.4.0/cli-reference/001620/config-system-admin)
วิธีแก้:
- หากตรวจพบ admin account ที่ไม่รู้จัก ให้ลบทันที: `config system admin`, `delete "<admin_name>"`, `end`
- หากบัญชีนั้นจำเป็น แต่ลืมลงทะเบียน ให้เพิ่มข้อมูล: `edit "<admin_name>"`, `set two-factor fortitoken`, `set fortitoken <serial>`, `end`
- บัญชี break-glass ต้องมี trusthost จำกัดเสมอ

---

## 2. ตรวจการเปลี่ยน config ที่ผิดปกติ

คำค้น: fortigate config change log, fortigate abnormal config change, fortigate log admin action
อาการ: ต้องตรวจว่ามี config change ที่ผิดปกติหรือไม่

คำสั่งตรวจ:
```
diagnose log console logfilter table log_event logtype config 2>/dev/null || log show
```
อ่านผล:
- ดูว่ามี config change ที่ไม่เป็นที่รู้จักหรือไม่ (เปลี่ยนชื่อ, เพิ่ม rule, เปิด service)
- หากมี config change จาก admin account ที่ไม่รู้จัก = เป็นสัญญาณการถูกบุกรุก
ที่มา: [Log Feature Table — FortiOS 7.4 Administration Guide](https://docs.fortinet.com/document/fortios/7.4.0/administration-guide/480747/administration-logs)
วิธีแก้:
- หากตรวจพบ config change ที่ผิดปกติ ให้กู้คืนจาก backup: `execute restore full <ucs_file>`, `end`
- ระบุ admin account ที่ทำการ change และสอบสวนบัญชีนั้น
- หากเป็น admin account ที่ถูกบุกรุก ให้เปลี่ยนรหัสผ่านทันที

---

## 3. ตรวจการ login admin ที่ผิดปกติ

คำค้น: fortigate abnormal admin login, fortigate login history investigation, fortigate admin login log
อาการ: ต้องตรวจว่าการ login admin เป็นไปอย่างปกติหรือไม่

คำสั่งตรวจ:
```
log display logtype event logsource admin sourceip 2>/dev/null || log show
```
อ่านผล:
- ดูว่ามีการ login จาก IP ที่ไม่เป็นที่รู้จักหรือไม่
- หากมีการ login จาก IP ที่ไม่เป็นที่รู้จัก = เป็นสัญญาณการถูกบุกรุก
ที่มา: [Log Feature Table — FortiOS 7.4 Administration Guide](https://docs.fortinet.com/document/fortios/7.4.0/administration-guide/480747/administration-logs)
วิธีแก้:
- หากตรวจพบ login จาก IP ที่ผิดปกติ ให้บล็อก IP นั้น: `config firewall address`, `edit "BLOCKED-IP"`, `set subnet <IP> 255.255.255.255`, `next`, `end`
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
- หากตรวจพบช่องโหว่ ให้ upgrade เป็นเวอร์ชันล่าสุด: `execute firmware-download latest`, `execute firmware-reboot`
- หากมีการ exploit แล้ว ให้กู้คืนจาก backup

---
