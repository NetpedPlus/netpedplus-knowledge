---
id: f5-bigip-ucs-restore-master-key
title: F5 BIG-IP 17.5.x — UCS Restore และ Master Key
families: f5_tmsh
triggers: f5 bigip ucs restore, f5 bigip ucs load, f5 bigip master key decrypt failure, f5 bigip rma hardware, f5 bigip ucs no-license, f5 bigip ucs backup best practices, f5 f5mku master key
versions: BIG-IP 17.5.x
sources: https://techdocs.f5.com/en-us/bigip-13-1-0/big-ip-secure-vault-administration/working-with-ucs-archives.html,https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_license.html,https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_sync-status.html
---

# F5 BIG-IP 17.5.x — UCS Restore และ Master Key

คำค้น: f5 bigip ucs restore, f5 bigip ucs load, f5 bigip master key decrypt failure, f5 bigip rma hardware, f5 bigip ucs no-license, f5 bigip ucs backup best practices, f5 f5mku master key
อาการ: BIG-IP เครื่องใหม่หรือเครื่อง RMA ต้อง restore UCS, เครื่อง HA pair ไม่ sync หลัง restore, master key ไม่ตรงทำให้ decrypt ล้มเหลว

อ้างอิง playbook อื่น:
- `f5-bigip-17-security-upgrade-assessment-ha` -> อัปเกรด HA ทั่วไป, สำรอง UCS ก่อน upgrade
- `f5-bigip-17-5-advanced-waf-upgrade-precautions` -> Cookie, Provisioning, Device Group หลัง upgrade
- `f5-bigip-asm-false-positive-staging` -> ASM False Positive / Staging / Learning

---

## 1 Restore UCS ไปเครื่องใหม่หรือ RMA

คำค้น: f5 bigip restore ucs no-license, f5 bigip ucs hardware platform mismatch
อาการ: restore ล้มเหลว, unlicensed state, master key ไม่ตรง — เกิดจาก device license ผิด hardware, master key ไม่ตรง, หรือ hardware platform ไม่เข้ากัน

คำสั่งตรวจ:
```
show sys license
```
อ่านผล:
- ดู license status หลัง restore

วิธีแก้ (ทำด้วยตนเอง):
- (bash) `f5mku -K` — ตรวจสอบ master key ปัจจุบันด้วยตนเอง **ห้ามใส่ในบล็อกคำสั่งตรวจ**

ระวัง:
- ค่า master key จาก f5mku -K เป็นความลับ — ห้ามวางในแชต / ticket / log / เอกสาร ใครมีค่านี้ + ไฟล์ UCS จะถอดรหัสผ่านทั้งหมดในเครื่องได้

วิธีแก้:
1. ใช้ `tmsh load sys ucs <file>.ucs no-license` (ต้องมี flag no-license — ถ้าไม่มีจะเข้า unlicensed state และ restore ล้มเหลว)
2. Reset master key ถ้าไม่มี key เดิม: `modify sys crypto master-key prompt-for-password`
3. หรือ copy master key จากเครื่องเดิม: `f5mku -r <key_value>`
4. RMA hardware: อ้าง K82540512 (เปิดไม่ได้)

ที่มา: [Working with UCS Archives (13.1.0)](https://techdocs.f5.com/en-us/bigip-13-1-0/big-ip-secure-vault-administration/working-with-ucs-archives.html)

อ้างอิง:
- "Because the original device license was created using device-specific information and specific license registration key(s), any attempt to restore the UCS archive without specifying the no-license flag places the device in the unlicensed state, causing the restore operation to fail."
- "Display detailed licensing and version information for the system, including the registration key, licensing dates," — tmsh reference v17.0.0 (sys_license.html, DESCRIPTION)


---

## 2 Restore UCS บน HA Sync ไป Secondary

คำค้น: f5 bigip restore ucs ha sync, f5 bigip device group sync leader config-sync
อาการ: restore แล้ว peer device ไม่ sync, config ไม่ไป — เกิดจาก UCS restore บน primary device แต่ไม่ sync ไป secondary, master key ไม่ตรง

คำสั่งตรวจ:
```
show cm sync-status
```
อ่านผล:
- ดู sync status หลัง restore (ตรวจว่า connected หรือ disconnected)

วิธีแก้ (ทำด้วยตนเอง):
- (bash) `f5mku -K` — ตรวจสอบ master key ด้วยตนเอง **ห้ามใส่ในบล็อกคำสั่งตรวจ**

ระวัง:
- ค่า master key จาก f5mku -K เป็นความลับ — ห้ามวางในแชต / ticket / log / เอกสาร ใครมีค่านี้ + ไฟล์ UCS จะถอดรหัสผ่านทั้งหมดในเครื่องได้

วิธีแก้:
**ตาม UCS 13.1.0 Solution 2:**
1. บนเครื่องเดิม: `f5mku -K` เพื่อดู master key
2. บนเครื่องใหม่: `f5mku -r <key_value>` เพื่อใส่ key เดิม
3. `f5mku -K` ตรวจว่า master key ตรงกัน
4. `tmsh load sys ucs <file>.ucs no-license`
5. `tmsh save sys config` บนเครื่องใหม่
6. `tmsh load sys config` บนเครื่องใหม่
7. บนเครื่องเดิม: `tmsh modify cm device-group <device_group> devices modify { <existing_BIG-IP> { set-sync-leader } }`
8. `tmsh run cm config-sync to-group <device_group>`
9. `tmsh show cm sync-status`
10. ตรวจสอบว่า connected

ที่มา: [Working with UCS Archives (13.1.0)](https://techdocs.f5.com/en-us/bigip-13-1-0/big-ip-secure-vault-administration/working-with-ucs-archives.html)

อ้างอิง:
- "After you perform this task, the BIG-IP system configuration is successfully loaded on the new system, and the new system has the same master key as the existing system."
- "sync-status - Displays the configuration synchronization status of the local device." — tmsh reference v17.0.0 (cm_sync-status.html, NAME section)
- "Confirm that the two systems are in sync by typing this command: tmsh show cm sync-status."

---

## 3 แก้ไข Master Key Decrypt Failure หลัง Restore

คำค้น: f5 bigip master key decrypt failure, f5 bigip 0107102b 01071769, f5 bigip master key mismatch
อาการ: restore แล้วเกิด error `Master Key decrypt failure`, config load ล้มเหลว — เกิดจาก master key ไม่ตรงระหว่าง source และ target

ตรวจใน GUI:
— ดูข้อความ error 0107102b / 01071769 ตอน load config (ตามหน้า UCS 13.1.0)

วิธีแก้:
1. ถ้ามี master key เดิม: `f5mku -r <key_value>`
2. ถ้าไม่มี: reset master key ใหม่ `modify sys crypto master-key prompt-for-password`
3. หรือแก้ `/config/bigip.conf` โดยตรง: แก้ encrypted password เป็น plain text

ระวัง:
- วิธีแก้ bigip.conf เป็น plain text (วิธีแก้ 3) ทำให้รหัสผ่านอยู่ในไฟล์แบบอ่านออกได้ — ใช้เมื่อไม่มีทางอื่น

ที่มา: [Working with UCS Archives (13.1.0)](https://techdocs.f5.com/en-us/bigip-13-1-0/big-ip-secure-vault-administration/working-with-ucs-archives.html)

อ้างอิง:
- "0107102b:3: Master Key decrypt failure - decrypt failure - final"
- "01071769:3: Decryption of the field (pvalue) for object (/Common/http_monitor_example 1 PASSWORD=) failed."

