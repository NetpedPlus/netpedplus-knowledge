---
id: f5-bigip-ucs-restore-master-key
title: F5 BIG-IP 17.5.x — UCS Restore และ Master Key
families: f5_tmsh
triggers: f5 bigip ucs restore, f5 bigip ucs load, f5 bigip master key decrypt failure, f5 bigip rma hardware, f5 bigip ucs no-license, f5 bigip ucs backup best practices, f5 f5mku master key
versions: BIG-IP 17.5.x (17.5.1.8–17.5.1.11)
sources: https://techdocs.f5.com/en-us/bigip-16-0-0/big-ip-secure-vault-administration/working-with-ucs-archives.html,https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-secure-vault-administration/working-with-ucs-archives/best-practices-ucs-installation.html
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

ตรวจใน GUI:
- System > License — ดู license status หลัง restore
- (bash) `f5mku -K` — ตรวจสอบ master key ปัจจุบัน (ต้องทำบนเครื่องใหม่)

ระวัง:
- ค่า master key จาก f5mku -K เป็นความลับ — ห้ามวางในแชต / ticket / log / เอกสาร anyone ที่มีค่านี้ + ไฟล์ UCS จะถอดรหัสผ่านทั้งหมดในเครื่องได้

วิธีแก้:
1. ใช้ `tmsh load sys ucs <file>.ucs no-license` (ต้องมี flag no-license — ถ้าไม่มีจะเข้า unlicensed state และ restore ล้มเหลว)
2. Reset master key ถ้าไม่มี key เดิม: `modify sys crypto master-key prompt-for-password`
3. หรือ copy master key จากเครื่องเดิม: `f5mku -r <key_value>`
4. RMA hardware: อ้าง K82540512 (เปิดไม่ได้)

ที่มา: [Working with UCS Archives (16.0)](https://techdocs.f5.com/en-us/bigip-16-0-0/big-ip-secure-vault-administration/working-with-ucs-archives.html)


---

## 2 Restore UCS บน HA Sync ไป Secondary

คำค้น: f5 bigip restore ucs ha sync, f5 bigip device group sync leader config-sync
อาการ: restore แล้ว peer device ไม่ sync, config ไม่ไป — เกิดจาก UCS restore บน primary device แต่ไม่ sync ไป secondary, master key ไม่ตรง

ตรวจใน GUI:
- `show cm sync-status` — ดู sync status หลัง restore (ตรวจว่า connected หรือ disconnected)
- (bash) `f5mku -K` — ตรวจสอบ master key ปัจจุบัน (ต้องทำบนเครื่องเดิมเพื่อเปรียบเทียบกับเครื่องใหม่)

ระวัง:
- ค่า master key จาก f5mku -K เป็นความลับ — ห้ามวางในแชต / ticket / log / เอกสาร anyone ที่มีค่านี้ + ไฟล์ UCS จะถอดรหัสผ่านทั้งหมดในเครื่องได้

วิธีแก้:
**ตาม UCS 16.0 Solution 2:**
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

ที่มา: [Working with UCS Archives (16.0)](https://techdocs.f5.com/en-us/bigip-16-0-0/big-ip-secure-vault-administration/working-with-ucs-archives.html)

อ้างอิง:
- "After you perform this task, the BIG-IP system configuration is successfully loaded on the new system, and the new system has the same master key as the existing system."
- "Confirm that the two systems are in sync by typing this command: tmsh show cm sync-status."

---

## 3 แก้ไข Master Key Decrypt Failure หลัง Restore

คำค้น: f5 bigip master key decrypt failure, f5 bigip 0107102b 01071769, f5 bigip master key mismatch
อาการ: restore แล้วเกิด error `Master Key decrypt failure`, config load ล้มเหลว — เกิดจาก master key ไม่ตรงระหว่าง source และ target

ตรวจใน GUI:
- (bash) `f5mku -K` — ตรวจสอบ master key ปัจจุบัน

วิธีแก้:
1. ถ้ามี master key เดิม: `f5mku -r <key_value>`
2. ถ้าไม่มี: reset master key ใหม่ `modify sys crypto master-key prompt-for-password`
3. หรือแก้ `/config/bigip.conf` โดยตรง: แก้ encrypted password เป็น plain text

ระวัง:
- วิธีแก้ bigip.conf เป็น plain text (วิธีแก้ 3) ทำให้รหัสผ่านอยู่ในไฟล์แบบอ่านออกได้ — ใช้เมื่อไม่มีทางอื่น

ที่มา: [Working with UCS Archives (16.0)](https://techdocs.f5.com/en-us/bigip-16-0-0/big-ip-secure-vault-administration/working-with-ucs-archives.html)

อ้างอิง:
- "0107102b:3: Master Key decrypt failure - decrypt failure - final"
- "01071769:3: Decryption of the field (pvalue) for object (/Common/http_monitor_example 1 PASSWORD=) failed."

