---
id: f5-bigip-17-pre-upgrade-check-ha
title: F5 BIG-IP 17.x — ตรวจสถานะก่อนอัปเกรดบนคู่ HA
families: f5_tmsh
triggers: f5 bigip pre-upgrade check, f5 ha upgrade standby first, f5 show cm failover-status, f5 list sys provision, f5 show sys software status, f5 save sys ucs
versions: BIG-IP 17.5.x
sources: https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_failover-status.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_provision.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_software_status.html, https://techdocs.f5.com/en-us/bigip-13-1-0/big-ip-secure-vault-administration/working-with-ucs-archives.html
---

# F5 BIG-IP 17.x — ตรวจสถานะก่อนอัปเกรดบนคู่ HA

คำค้น: f5 bigip pre-upgrade check, f5 ha upgrade standby first, f5 show cm failover-status, f5 list sys provision, f5 show sys software status, f5 save sys ucs

อาการ: ก่อนอัปเกรด BIG-IP บน HA pair ต้องการตรวจสถานะ failover, provisioning และ software installation ว่าอยู่ในสภาวะพร้อมก่อนเริ่ม

---

## 1. ตรวจสถานะ failover ของเครื่อง

คำค้น: f5 show cm failover-status, f5 bigip failover status local device
อาการ: ต้องตรวจสถานะ failover ของเครื่องปัจจุบันก่อนอัปเกรดบน HA pair

คำสั่งตรวจ:
```
show cm failover-status
```
อ่านผล: แสดงสถานะ failover ของเครื่องที่รันคำสั่ง (local device)
ที่มา: [cm_failover-status.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_failover-status.html)
อ้างอิง:
- "failover-status - Display the failover status of the local device." — tmsh reference v17.0.0 (cm_failover-status.html, NAME section)
- "show failover-status — Displays the failover status of the local device." — tmsh reference v17.0.0 (cm_failover-status.html, EXAMPLES)

---

## 2. ตรวจ software installation status

คำค้น: f5 show sys software status, f5 bigip software installation status table
อาการ: ต้องตรวจสถานะการติดตั้ง software ว่าแต่ละ volume อยู่ในสถานะใดก่อนอัปเกรด

คำสั่งตรวจ:
```
show sys software status
```
อ่านผล: แสดงสถานะการติดตั้ง software เป็นตาราง
ที่มา: [sys_software_status.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_software_status.html)
อ้างอิง:
- "status - Displays the status of a BIG-IP(r) system software installation." — tmsh reference v17.0.0 (sys_software_status.html, NAME section)
- "show status — Displays the status of the software installation in a table." — tmsh reference v17.0.0 (sys_software_status.html, EXAMPLES)

---

## 3. ตรวจ provisioning ของ module

คำค้น: f5 list sys provision, f5 bigip module provisioning levels
อาการ: ต้องตรวจระดับ provisioning ของ module ทั้งหมดก่อนอัปเกรด

คำสั่งตรวจ:
```
list sys provision
```
อ่านผล: แสดงระดับ provisioning ของแต่ละ module
ที่มา: [sys_provision.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_provision.html)
อ้างอิง:
- "Displays the current provisioning of the system." — tmsh reference v17.0.0 (sys_provision.html, EXAMPLES)

หมายเหตุ — ระดับ provisioning จาก sys_provision.html (OPTIONS):
- dedicated: "Specifies that all resources are dedicated to the module you are provisioning."
- minimum: "Specifies that you want to provision the minimum amount of resources for the module you are provisioning."
- nominal: "Specifies that you want to share all of the available resources equally among all of the modules that are licensed on the unit."
- none: "Specifies that you do not want to provision any resources for this module."
- custom: "F5 Networks does not recommend that you specify this level."

หมายเหตุ — สำรอง UCS:
- F5 แนะนำให้สำรอง config เป็นประจำและเก็บอย่างปลอดภัย:
  - "The preferred way to store UCS archives securely (encrypts the entire UCS file): `tmsh save sys ucs <ucs name> passphrase <passphrase>`."
  - "Make sure that you regularly back up the BIG-IP system configuration and maintain the backup UCS archives in a secure manner."
- แหล่ง: [working-with-ucs-archives.html (techdocs 13.1.0)](https://techdocs.f5.com/en-us/bigip-13-1-0/big-ip-secure-vault-administration/working-with-ucs-archives.html)
