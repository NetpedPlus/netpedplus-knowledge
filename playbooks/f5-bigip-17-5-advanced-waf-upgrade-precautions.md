---
id: f5-bigip-17-5-advanced-waf-upgrade-precautions
title: F5 BIG-IP 17.5.x — ข้อควรระวังตอนอัปเกรด Advanced WAF
families: f5_tmsh
triggers: f5 advanced waf upgrade precautions, f5 asm cookie violation upgrade, f5 datasync-global-dg, f5 asm provisioning wait 5 minutes, f5 advanced waf upgrade
versions: BIG-IP 17.5.x (17.5.1.8–17.5.1.11)
sources: https://techdocs.f5.com/en-us/bigip-17-5-1-11/big-ip-release-notes/big-ip-upgrade.html,https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_provision.html,https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_device-group.html
---

# F5 BIG-IP 17.5.x — ข้อควรระวังตอนอัปเกรด Advanced WAF

คำค้น: f5 advanced waf upgrade precautions, f5 asm cookie violation upgrade, f5 datasync-global-dg, f5 asm provisioning wait 5 minutes, f5 advanced waf upgrade
อาการ: เมื่ออัปเกรด BIG-IP ที่มี Advanced WAF (ASM) provision อยู่ อาจเกิดปัญหาจาก cookie, provisioning state และ device group หากไม่ปฏิบัติตามขั้นตอนที่ F5 กำหนด

อ้างอิง playbook อื่น:
- `f5-bigip-17-security-upgrade-assessment-ha` -> ขั้นตอนอัปเกรด HA ทั่วไป, สำรอง UCS, rollback
- `f5-ops-advanced` -> HA setup, device trust, ConfigSync

---

## 1. ตรวจสอบสถานะ Advanced WAF ก่อนอัปเกรด

คำค้น: f5 asm check provision status, f5 tmsh list sys provision asm
อาการ: ต้องตรวจว่า BIG-IP มี Advanced WAF (ASM) provision อยู่หรือไม่ ก่อนเริ่มอัปเกรด

ตรวจใน GUI:
- ดูเวอร์ชันของ BIG-IP

ตรวจใน CLI:
- `tmsh list sys provision` -> ตรวจ module ที่ provision
- `tmsh list cm device-group` -> ตรวจ device group ที่มี

อ่านผล:
- **ถ้า `asm: none`** -> ไม่ได้ provision Advanced WAF ไม่ต้องทำข้อ 2-4
- **ถ้า `asm: nominal` หรือมากกว่า** -> ต้องทำข้อ 2-4 ทั้งหมด

ที่มา: [BIG-IP System: Provisioning - TMSH Reference](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_provision.html), [BIG-IP 17.5.1.11 Upgrading](https://techdocs.f5.com/en-us/bigip-17-5-1-11/big-ip-release-notes/big-ip-upgrade.html)
- "Displays the current provisioning of the system." — tmsh reference v17.0.0 (sys_provision.html, EXAMPLES — list provision)

---

## 2. จัดการ cookie security ก่อน clean upgrade (เฉพาะ Clean Upgrade)

คำค้น: f5 advanced waf cookie security upgrade, f5 asm cookie violation pre-upgrade
อาการ: Clean upgrade อาจทำให้ cookie violation -> traffic ถูกบล็อก เนื่องจาก F5 เปลี่ยนการลงลายเซ็นของ Advanced WAF cookies

ตรวจใน GUI:
- **System -> Software Management** -> เลือก image -> Activate (Clean Upgrade)
- ถ้าเลือก Install Configuration = Yes -> อาจเกิด cookie violation ได้

**ข้อควรระวัง (คัดจากหน้า Upgrading ของ F5):**
> "As a result of changes made to the signing of Advanced WAF cookies, performing a clean upgrade may result in cookie violations and blocked traffic."

**วิธีป้องกัน - ทำก่อน upgrade:**
1. ปิด modified domain cookie violation
2. หากไม่มี wildcard cookie ให้เพิ่ม Advanced WAF allowed cookie ชื่อ `TS*`
3. ให้ทุก client ปิด/เปิด browser ใหม่หลัง upgrade
4. **สำคัญ:** เปิด modified domain cookie violation กลับหลังจากผ่านไปอย่างน้อย 24 ชั่วโมง

**วิธีดำเนินการหลัง upgrade:**
1. ให้ทุก client ปิด/เปิด browser ใหม่
2. **สำคัญ:** เปิด modified domain cookie violation กลับหลังจากผ่านไปอย่างน้อย 24 ชั่วโมง

ที่มา: [BIG-IP 17.5.1.11 Upgrading - Advanced WAF Cookie Security](https://techdocs.f5.com/en-us/bigip-17-5-1-11/big-ip-release-notes/big-ip-upgrade.html#advanced-waf-cookie-security)

---

## 3. รอ 5 นาทีหลังตั้งค่า resource provisioning level ของ Advanced WAF

คำค้น: f5 asm provisioning wait 5 minutes, f5 asm not ready, f5 asm started successfully
อาการ: หลัง upgrade ต้องตั้ง resource provisioning level เป็น Nominal แล้วรอ 5 นาทีก่อนตั้งค่าอื่น ๆ มิฉะนั้นระบบจะ override การตั้งค่าทั้งหมด

คำสั่งตรวจ:
```
show sys provision
```
อ่านผล: บรรทัด asm ต้องเป็น level nominal ก่อนเริ่มนับ 5 นาที — ข้อความ "ASM started successfully" ดูใน log /var/log/asm (ขั้นที่ 3 ด้านล่าง)

**ข้อควรระวัง (คัดจากหน้า Upgrading ของ F5):**
> "After upgrading or installing a new version, before you can use the Advanced WAF, you must set the Advanced WAF resource provisioning level to Nominal if it is not already set to Nominal."

> "**Important:** Wait 5 minutes after you set the resource provisioning level before making any configuration changes to the Advanced WAF. The system overrides all configuration changes that were made before this process is completed."

**วิธีดำเนินการ - ทำหลัง upgrade (หลัง reboot แล้ว):**
1. ตั้งค่า resource provisioning level เป็น **Nominal** (แก้ config - ไม่ได้อยู่ในคำสั่งตรวจ)
2. **รอ 5 นาที** - ห้ามตั้งค่าอื่น ๆ เกี่ยวข้องกับ Advanced WAF ในช่วงนี้
3. ตรวจว่า ASM พร้อมใช้งานแล้ว:
   - ตรวจ log ที่ `/var/log/asm` -> ต้องมีบรรทัด: `ASM started successfully.`

ที่มา: [sys provision — TMSH Reference](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_provision.html), [BIG-IP 17.5.1.11 Upgrading - About changing the resource provisioning level of the Advanced WAF](https://techdocs.f5.com/en-us/bigip-17-5-1-11/big-ip-release-notes/big-ip-upgrade.html#about-changing-the-resource-provisioning-level-of-the-advanced-waf)

---

## 4. ห้ามลบ device group datasync-global-dg

คำค้น: f5 datasync-global-dg, f5 asm device group sync scripts
อาการ: Advanced WAF จะสร้าง device group `datasync-global-dg` อัตโนมัติ - ห้ามลบเด็ดขาด เพราะใช้ sync client-side scripts และ cryptographic keys ทั่วทั้ง trust-domain

ตรวจใน GUI:
- ตรวจสอบว่า Scripts Package ถูก sync ไปยังทุก device ใน trust-domain หรือยัง

ตรวจใน CLI:
- `tmsh list cm device-group` -> ตรวจว่ามี `datasync-global-dg` ในรายการ

**ข้อควรระวัง (คัดจากหน้า Upgrading ของ F5):**
> "When Advanced WAF is provisioned, the **datasync-global-dg** device-group is automatically created (even if there are no device-groups on the unit)"

> "The **datasync-global-dg** device group must not be removed; it is essential for consistency of client-side scripts and keys across the devices."

**วิธีดำเนินการ - ทำหลัง upgrade:**
1. ตรวจว่า device group `datasync-global-dg` ยังอยู่ (อ่านอย่างเดียว)
2. ตรวจว่า Scripts Package ถูก sync ไปยังทุก device ใน trust-domain (อ่านอย่างเดียว)
3. หากยังไม่ได้ sync -> เลือก device หลัก -> sync ไปยัง device อื่น (แก้ config - ไม่ได้อยู่ในคำสั่งตรวจ)

**สิ่งที่ F5 กำหนด:**
- Device group นี้สร้างอัตโนมัติเมื่อมี Advanced WAF provisioned
- สร้างแม้เป็น standalone device
- เพิ่มทุก device ใน trust-domain อัตโนมัติ
- **ห้ามลบ** - จำเป็นสำหรับความสอดคล้องของ scripts และ keys
- ต้อง sync ด้วยตนเอง (manual sync) -> เลือก device หลักที่จะเก็บ master scripts/keys

ที่มา: [BIG-IP 17.5.1.11 Upgrading - About working with device groups](https://techdocs.f5.com/en-us/bigip-17-5-1-11/big-ip-release-notes/big-ip-upgrade.html#about-working-with-device-groups)
- "device-group - Configures device groups." — tmsh reference v17.0.0 (cm_device-group.html, NAME section — list device-group)
