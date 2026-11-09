---
id: f5-bigip-17-ucs-backup
title: F5 BIG-IP 17.x — สำรองและจัดการ UCS archive
families: f5_tmsh
triggers: f5 bigip ucs backup, f5 save sys ucs, f5 list ucs, f5 bigip ucs archive
versions: BIG-IP 17.5.x
sources: https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_ucs.html, https://techdocs.f5.com/en-us/bigip-13-1-0/big-ip-secure-vault-administration/working-with-ucs-archives.html
---

# F5 BIG-IP 17.x — สำรองและจัดการ UCS archive

คำค้น: f5 bigip ucs backup, f5 save sys ucs, f5 list ucs, f5 bigip ucs archive

อาการ: ต้องการสำรอง configuration ของ BIG-IP เป็น UCS archive เพื่อฟื้นฟูระบบ

---

## 1. ตรวจ UCS archive ที่มีอยู่

คำค้น: f5 list ucs, f5 bigip ucs files existing

อาการ: ตรวจว่ามี UCS archive ไฟล์ใดอยู่ในระบบก่อนทำ backup ใหม่

คำสั่งตรวจ:
```
list ucs
```
อ่านผล: แสดงรายการ UCS archive files ที่มีอยู่ในไดเรกทอรี `/var/local/ucs/`

ที่มา: [sys_ucs.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_ucs.html)

อ้างอิง:
- "ucs - Loads or saves a UCS (.ucs) file." — tmsh reference v17.0.0 (sys_ucs.html, NAME section)
- "list ucs — Displays existing UCS files in the default directory, /var/local/ucs/." — tmsh reference v17.0.0 (sys_ucs.html, EXAMPLES section)
- "When you save a UCS file, the file is saved to the default directory, /var/local/ucs." — tmsh reference v17.0.0 (sys_ucs.html, DESCRIPTION section)

---

## 2. สำรอง UCS archive

คำค้น: f5 save sys ucs, f5 bigip ucs backup save

อาการ: สำรอง running configuration ของระบบเป็น UCS archive (ไม่เข้ารหัส)

คำสั่งตรวจ:
```
list ucs
```

วิธีแก้: `save sys ucs <ucs name>` — บันทึก running configuration เป็นไฟล์ UCS

อ่านผล: บันทึก running configuration ของระบบเป็นไฟล์ `<ucs name>.ucs` ในไดเรกทอรี `/var/local/ucs/`

ที่มา: [sys_ucs.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_ucs.html)

อ้างอิง:
- "ucs - Loads or saves a UCS (.ucs) file." — tmsh reference v17.0.0 (sys_ucs.html, NAME section)
- "You can use the ucs component to save the running configuration of the system into a UCS file." — tmsh reference v17.0.0 (sys_ucs.html, DESCRIPTION section)
- "save ucs myucs — Saves the running configuration of the system into the file myucs.ucs." — tmsh reference v17.0.0 (sys_ucs.html, EXAMPLES section)

หมายเหตุ: รูปที่เขียนในหน้าคือ `save ucs [file name]` (ตัด module sys) คำสั่ง tmsh เต็มคือ `save sys ucs [file name]`

---

## 3. สำรอง UCS แบบเข้ารหัส

คำค้น: f5 save sys ucs passphrase, f5 bigip ucs encrypted backup

อาการ: ต้องการเข้ารหัส UCS archive ด้วย passphrase ก่อนเก็บ

คำสั่งตรวจ:
```
list ucs
```

วิธีแก้: `save sys ucs <ucs name> passphrase <passphrase>` — บันทึก running configuration เป็นไฟล์ UCS ที่เข้ารหัสด้วย passphrase

อ่านผล: บันทึก running configuration ของระบบเป็นไฟล์ UCS ที่เข้ารหัสด้วย passphrase ที่ระบุ

ที่มา: [sys_ucs.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_ucs.html)

อ้างอิง:
- "passphrase - Specifies the passphrase that is necessary to load the specified UCS file." — tmsh reference v17.0.0 (sys_ucs.html, OPTIONS section)

หมายเหตุ:
- F5 แนะนำให้เข้ารหัส UCS archive เพื่อความปลอดภัย: "The preferred way to store UCS archives securely (encrypts the entire UCS file): `tmsh save sys ucs <ucs name> passphrase <passphrase>`." — [working-with-ucs-archives.html (techdocs 13.1.0)](https://techdocs.f5.com/en-us/bigip-13-1-0/big-ip-secure-vault-administration/working-with-ucs-archives.html) (หัวข้อ "Store UCS archives securely")
- SYNTAX: `save ucs [file name] — options: no-private-key, passphrase` — tmsh reference v17.0.0 (sys_ucs.html, SYNTAX section) — โครงสร้างย่อจาก SYNTAX (ไม่ใช่ประโยคต้นฉบับ)

---

หมายเหตุ — เก็บ passphrase ในที่ปลอดภัย:
- F5 แนะนำให้จดบันทึก passphrase ของ configuration objects ไว้ใน secure location บนเครื่องอื่นที่ไม่ใช่ BIG-IP: "After you encrypt configuration object passwords or passphrases on any BIG-IP system, another system can only decrypt them (during a `tmsh load config` operation) by using the same master key that you used to encrypt them. F5 recommends that you retain a record of each configuration object password or passphrase in a secure location on a system other than the BIG-IP system that uses the password or passphrase." — [working-with-ucs-archives.html (techdocs 13.1.0)](https://techdocs.f5.com/en-us/bigip-13-1-0/big-ip-secure-vault-administration/working-with-ucs-archives.html) (หัวข้อ "Store passwords and passphrases securely")

หมายเหตุ — ไม่พบที่มา:
- ไม่พบที่มาว่าควรเก็บ UCS archive อย่างไรนอก BIG-IP (เช่นที่เก็บ, media, retention policy) — ตรวจแล้ว: working-with-ucs-archives.html, sys_ucs.html
- ไม่พบที่มาของสาเหตุ UCS backup ล้มเหลว (disk ไม่พอ, passphrase ผิด, permission ของ UCS directory) — ตรวจแล้ว: working-with-ucs-archives.html, sys_ucs.html
