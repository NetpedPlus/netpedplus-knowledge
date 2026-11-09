---
id: f5-bigip-17-ha-upgrade-procedure
title: F5 BIG-IP 17.x -- ขั้นตอนอัปเกรดบนคู่ HA
families: f5_tmsh
triggers: f5 bigip ha upgrade, f5 bigip upgrade standby first, f5 install sys software image, f5 upgrade high availability, f5 post installation bigip
versions: BIG-IP 17.5.x
sources: https://techdocs.f5.com/en-us/bigip-17-5-1-11/big-ip-release-notes/big-ip-install.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_license.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_software_status.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_failover-status.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_sync-status.html
---

# F5 BIG-IP 17.x -- ขั้นตอนอัปเกรดบนคู่ HA

คำค้น: f5 bigip ha upgrade, f5 bigip upgrade standby first, f5 install sys software image, f5 upgrade high availability, f5 post installation bigip

อาการ: ต้องอัปเกรด BIG-IP บน HA pair (Active-Standby) อย่างปลอดภัย โดยอัปเกรด standby unit ก่อน

หมายเหตุ -- Playbook นี้ครอบคลุมเฉพาะขั้นตอนที่เอกสาร F5 17.5 รองรับ (big-ip-install.html 17.5.1.11)

---

## 1. License: ตรวจและ activate ก่อน upgrade

คำค้น: f5 show sys license, f5 update reactivate license service check date, f5 license activation before upgrade

อาการ: ต้องตรวจว่า license ยังใช้งานได้อยู่ก่อนอัปเกรด

คำสั่งตรวจ:
```
show sys license
```

อ่านผล: ดู registration key, licensing dates, platform ID, suggested service check date, และ installed active modules

ที่มา: [sys_license.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_license.html)

อ้างอิง:
- "Display detailed licensing and version information for the system, including the registration key, licensing dates, platform ID, suggested service check date, and the installed active modules." -- tmsh reference v17.0.0 (sys_license.html, DESCRIPTION section)
- "show license -- Displays the system software licensing information." -- tmsh reference v17.0.0 (sys_license.html, EXAMPLES section)

หมายเหตุ:
- "Update/reactivate your system or vCMP host license, if needed, to ensure that you have a valid service check date." -- big-ip-install.html (17.5.1.11, Installation checklist)

---

## 2. Install image: จาก CLI หรือ GUI

คำค้น: f5 install sys software image cli, f5 tmsh install software image volume, f5 install bigip image gui, f5 software management web browser

อาการ: ต้องติดตั้ง BIG-IP software image จาก command line ผ่าน CLI หรือจาก GUI

วิธีดำเนินการ:
1. ติดตั้ง image จาก CLI: "Install to existing volume, migrate source configuration to destination"
   - CLI: `tmsh install sys software image [image name] volume [volume name]`
2. ติดตั้ง image จาก GUI: "Use the Software Management screens in a web browser."

ที่มา: [big-ip-install.html (17.5.1.11)](https://techdocs.f5.com/en-us/bigip-17-5-1-11/big-ip-release-notes/big-ip-install.html)

อ้างอิง:
- "Install to existing volume, migrate source configuration to destination" → `tmsh install sys software image [image name] volume [volume name]` — big-ip-install.html (17.5.1.11, Installing the software)
- "Use the Software Management screens in a web browser." — big-ip-install.html (17.5.1.11, Installing the software)

คำสั่งตรวจ:
```
show sys software status
```

อ่านผล: แสดงสถานะการติดตั้ง software เป็นตาราง

ที่มา: [sys_software_status.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_software_status.html)

อ้างอิง:
- "status - Displays the status of a BIG-IP(r) system software installation." -- tmsh reference v17.0.0 (sys_software_status.html, NAME section)
- "show status -- Displays the status of the software installation in a table." -- tmsh reference v17.0.0 (sys_software_status.html, EXAMPLES)

---

## 3. Monitor install status

คำค้น: f5 monitor install progress, f5 watch tmsh show sys software, f5 install status monitoring, f5 tmsh show sys software every two seconds

อาการ: ต้องการติดตามสถานะการติดตั้ง image ว่าเสร็จหรือยัง

วิธีดำเนินการ:
1. ใช้ `watch tmsh show sys software` เพื่อติดตามสถานะการติดตั้งแบบ real-time
   - "watch tmsh show sys software, which runs the show sys software command every two seconds." -- big-ip-install.html (17.5.1.11, Installation tips and important notes)

ที่มา: [big-ip-install.html (17.5.1.11)](https://techdocs.f5.com/en-us/bigip-17-5-1-11/big-ip-release-notes/big-ip-install.html)

คำสั่งตรวจ:
```
show sys software status
```

อ่านผล: แสดงสถานะการติดตั้ง software เป็นตาราง

ที่มา: [sys_software_status.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_software_status.html)

อ้างอิง:
- "status - Displays the status of a BIG-IP(r) system software installation." -- tmsh reference v17.0.0 (sys_software_status.html, NAME section)
- "show status -- Displays the status of the software installation in a table." -- tmsh reference v17.0.0 (sys_software_status.html, EXAMPLES)

---

## 4. อัปเกรด HA: อัปเกรด standby unit ก่อน

คำค้น: f5 ha upgrade standby first, f5 upgrade standby before active, f5 log on to standby unit first

อาการ: ต้องอัปเกรด BIG-IP บน HA pair โดยอัปเกรด standby unit ก่อน

วิธีดำเนินการ:
1. อัปเกรด image บน standby unit (ขั้นตอนที่ 2)
2. Monitor install status บน standby unit (ขั้นตอนที่ 3)

ที่มา: [big-ip-install.html (17.5.1.11)](https://techdocs.f5.com/en-us/bigip-17-5-1-11/big-ip-release-notes/big-ip-install.html)

คำสั่งตรวจ:
```
show cm failover-status
```

อ่านผล: แสดงสถานะ failover ของเครื่องที่รันคำสั่ง (local device)

ที่มา: [cm_failover-status.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_failover-status.html)

อ้างอิง:
- "failover-status - Display the failover status of the local device." -- tmsh reference v17.0.0 (cm_failover-status.html, NAME section)
- "show failover-status -- Displays the failover status of the local device." -- tmsh reference v17.0.0 (cm_failover-status.html, EXAMPLES)

> **หมายเหตุ**:
> - "Log on to the standby unit, and only upgrade the active unit after the standby upgrade is satisfactory." -- big-ip-install.html (17.5.1.11, Installation checklist)
> - **ขั้นอัปเกรดเครื่องที่สอง/failover/Force to Standby/Traffic Groups: ไม่พบที่มา (ไม่มีหน้า 17.5)**

---

## 5. Post-installation: ตรวจว่าระบบ reboot ไป location ใหม่แล้ว

คำค้น: f5 post upgrade check reboot, f5 system rebooted new location, f5 post installation tasks, f5 ensure rebooted to new installation

อาการ: ต้องตรวจว่าหลัง reboot ระบบ boot ไป installation location ใหม่ (ที่ติดตั้ง image ใหม่) แล้ว

คำสั่งตรวจ:
```
show sys software status
```

อ่านผล: แสดงสถานะการติดตั้ง software เป็นตาราง

ที่มา: [sys_software_status.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_software_status.html)

อ้างอิง:
- "status - Displays the status of a BIG-IP(r) system software installation." -- tmsh reference v17.0.0 (sys_software_status.html, NAME section)
- "show status -- Displays the status of the software installation in a table." -- tmsh reference v17.0.0 (sys_software_status.html, EXAMPLES)

หมายเหตุ:
- "Ensure the system rebooted to the new installation location." -- big-ip-install.html (17.5.1.11, Post-installation tasks)
- ไม่พบที่มา (ไม่มีหน้า 17.5) สำหรับขั้นตอน rollback — big-ip-install.html (17.5.1.11) ไม่มีหัวข้อ rollback

---

## 6. ตรวจหลัง upgrade ทั้งคู่

คำค้น: f5 post upgrade verification, f5 check after upgrade ha, f5 post upgrade check list

อาการ: ตรวจสถานะ configuration synchronization หลัง upgrade ทั้ง 2 เครื่อง

คำสั่งตรวจ:
```
show cm sync-status
```

อ่านผล: แสดงสถานะ configuration synchronization ของเครื่องที่รันคำสั่ง

ที่มา: [cm/sync-status.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_sync-status.html)

อ้างอิง:
- "sync-status - Displays the configuration synchronization status of the local device." -- tmsh reference v17.0.0 (cm/sync-status.html, NAME section)
