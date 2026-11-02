---
title: "Sophos SFOS 21.5: ลง hotfix / firmware บนคู่ HA + ตรวจว่า hotfix ลงครบ"
id: "sophos-sfos215-hotfix-firmware-ha"
version: "SFOS 21.5"
versions: ["21.5.0", "21.5.1", "21.5.2", "21.5.3"]
vendor: "Sophos"
platform: "XGS"
tags:
  - firmware
  - hotfix
  - high-availability
  - upgrade
  - verification
triggers: ["ต้องการลง hotfix / firmware บน Sophos XGS HA pair", "ตรวจว่า hotfix ลงครบหรือไม่"]
sources: ["https://docs.sophos.com/nsg/sophos-firewall/23.0/help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html", "https://support.sophos.com/support/s/article/KBA-000010589?language=en_US", "https://docs.sophos.com/nsg/Sophos-firewall/23.0/help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/Firmware/FirmwareFAQs/index.html"]
---

# Sophos SFOS 21.5: ลง hotfix / firmware บนคู่ HA + ตรวจว่า hotfix ลงครบ

> **คำเตือน**: ดำเนินการในหน้าต่างบำรุงรักษา (maintenance window) เสมอ

## 1. เตรียมการก่อนอัพเกรด

คำค้น: เตรียมการอัพเกรด, backup, HA health check, disk space

ที่มา: https://docs.sophos.com/nsg/Sophos-firewall/23.0/help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/Firmware/FirmwareFAQs/index.html — `Recommended checklist for all deployments: 1. Take a fresh backup. 2. Verify the available disk space.`

### คำสั่งตรวจ

คำสั่งตรวจ:
```
diagnostic system version
```

1. **สำรองการตั้งค่า**: ไปที่ **Backup and firmware** > **Backup** > **Create backup**
2. **ตรวจสอบพื้นที่ดิสก์**: ต้องมีพื้นที่เพียงพอทั้ง primary และ secondary node
3. **ตรวจสอบ upgrade path**: ยืนยันว่าเป็นการอัพเกรดจาก version ที่รองรับ
4. **ตรวจสอบ HA status**: ต้องเป็น healthy และ synchronized
5. **ตรวจสอบว่าทั้ง 2 node มีพื้นที่ดิสก์เพียงพอ**: แต่ละ node ถูกประเมินแยกกัน
6. **ตรวจสอบ SSD firmware**: XGS models บางรุ่นต้องการ SSD firmware upgrade ก่อน

## 2. ลง hotfix / firmware บน HA pair

คำค้น: อัพเกรด HA, upgrade firmware HA, primary auxiliary

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/23.0/help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html — `The primary device (device A) upgrades the auxiliary device (device B). After the auxiliary device (device B) is upgraded and restarts, it becomes the primary device.`

### คำสั่งตรวจ

ตรวจใน GUI: ไปที่ **Backup and firmware** > **Firmware**

### 2.1 วิธีการอัพเกรด

เมื่ออัพเกรด HA device กระบวนการมีดังนี้ (ยืนยันจากเอกสาร Sophos):

1. เริ่มอัพเกรดจาก **primary device** เท่านั้น
2. Primary device (device A) อัพเกรด auxiliary device (device B)
3. Auxiliary device (device B) ที่อัพเกรดแล้วรีบูต และกลายเป็น primary device
4. Former primary (device A) อัพเกรดตัวเองและรีบูต
5. หากตั้งค่า **Preferred primary device** ไว้ failover จะเกิดขึ้น และ device A กลับมาเป็น primary

### 2.2 ขั้นตอนการลง firmware

1. Login ไปที่ **primary device** web admin console
2. ไปที่ **Backup and firmware** > **Firmware**
3. เลือกวิธีใดวิธีหนึ่ง:
   - คลิก **Boot firmware** เพื่อใช้ firmware ที่ดาวน์โหลดไว้
   - คลิก **Upload firmware** เพื่ออัพโหลดไฟล์ firmware ใหม่
4. รอให้ auxiliary device อัพเกรดก่อน (ไม่มีการ downtime ระหว่างกระบวนการ)
5. หลังจาก auxiliary device ทำงานแล้ว traffic จะ failover ไปที่ auxiliary
6. Primary device เดิมจะอัพเกรดตัวเองถัดไป
7. หากตั้งค่า Preferred primary ไว้ จะ failback กลับ

### 2.3 การ rollback

สามารถ rollback firmware version ของ HA pair ได้โดยไม่ต้องปิด HA:

1. กระบวนการ rollback ทำเหมือนการอัพเกรด
2. Configuration จะถูก restore อัตโนมัติเมื่อ rollback

## 3. ตรวจว่า hotfix ลงครบ

คำค้น: ตรวจ hotfix, verify hotfix, version-info

ที่มา: https://support.sophos.com/support/s/article/KBA-000010589 — `Run the command: system diagnostic show version-info` — `The hotfix is applied if you see HF071525.1 or a later value in the Hotfix tag field.`

### คำสั่งตรวจ

คำสั่งตรวจ:
```
system diagnostic show version-info
system hotfix show
```

### 3.1 ตรวจสอบ hotfix tag

ตาม KBA-000010589:

1. เข้าถึง **Device Console** ของ firewall
2. รันคำสั่ง `system diagnostic show version-info`
3. ดูค่าในช่อง **Hotfix tag**:

   - ค่าที่ต้องเห็น: **HF071525.1** หรือค่าที่สูงกว่านี้ (เช่น HF071525.2, HF101025.1)
   - หากเห็นค่าน้อยกว่านี้ = hotfix ยังไม่ลงครบ

### 3.2 ตรวจ hotfix ที่ติดตั้งใน web admin

1. ไปที่ **Backup and firmware** > **Hotfix: Security updates**
2. หน้านี้จะแสดง hotfix security updates ที่ติดตั้งไว้ตั้งแต่ upgrade เป็น SFOS 21.5
3. Hotfix ที่ติดตั้งจะแสดงรายการพร้อมวันที่ติดตั้ง

### 3.3 ตรวจ hotfix auto-install status

ตรวจสอบว่า hotfix automatic installation เปิดอยู่หรือไม่:

1. ไปที่ **Device Console**
2. รันคำสั่ง `system hotfix show`
3. ค่าที่ต้องเห็น: hotfix auto-install ต้องเป็น **enabled**
4. Default value คือ **enabled** — Sophos แนะนำให้คงค่านี้ไว้
5. Firewall จะค้นหา hotfix ใหม่ทุก 30 นาที

## 4. ตรวจ HA status หลังอัพเกรด

คำค้น: HA status healthy, failover verification, primary role

ที่มา: https://docs.sophos.com/nsg/Sophos-firewall/23.0/help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/Firmware/FirmwareFAQs/index.html — `Verify that the HA status is healthy.`

### คำสั่งตรวจ

คำสั่งตรวจ:
```
ha cluster show
ha status
```

หลังอัพเกรดเสร็จ ต้องตรวจสอบว่า:

1. HA status เป็น healthy
2. Primary/Auxiliary role ถูกต้อง (ตาม Preferred primary setting)
3. Configuration synchronize อยู่
4. Traffic ทำงานปกติ

## คำสั่งตรวจ

คำค้น: เอกสาร, แหล่งอ้างอิง, evidence

ที่มา: https://support.sophos.com/support/s/article/KBA-000010589 — `Run the command: system diagnostic show version-info` — `The hotfix is applied if you see HF071525.1 or a later value in the Hotfix tag field.`

### คำสั่งตรวจ

ตรวจใน GUI:

| คำสั่ง / เมนู | URL หน้าคำสั่ง | ข้อความที่คัดจากหน้า |
| --- | --- | --- |
| system diagnostic show version-info | https://support.sophos.com/support/s/article/KBA-000010589 | `Run the command: system diagnostic show version-info` — `The hotfix is applied if you see HF071525.1 or a later value in the Hotfix tag field.` |
| system hotfix show | https://docs.sophos.com/nsg/sophos-firewall/22.0/Help/en-us/webhelp/onlinehelp/CommandLineHelp/DeviceConsole/SystemCommands/Hotfix/index.html | `system hotfix [enable | disable | show]` — `Allows the firewall to automatically install hotfixes when they become available.` |
| Backup and firmware > Firmware | https://docs.sophos.com/nsg/sophos-firewall/23.0/help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html | `Sign in to the primary device's web admin console and go to Backup and firmware > Firmware.` |
| Upgrade จาก primary device เท่านั้น | https://docs.sophos.com/nsg/Sophos-firewall/23.0/help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/Firmware/FirmwareFAQs/index.html | `You must start the upgrade on the Primary device.` |
| Both HA nodes ต้องผ่าน requirement | https://docs.sophos.com/nsg/Sophos-firewall/23.0/help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/Firmware/FirmwareFAQs/index.html | `Yes, both firewalls must meet the firmware requirements. Each firewall in the HA cluster is evaluated independently.` |
