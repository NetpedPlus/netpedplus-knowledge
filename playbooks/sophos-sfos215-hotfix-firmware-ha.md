---
title: "Sophos SFOS 21.5: ลง hotfix / firmware บนคู่ HA + ตรวจว่า hotfix ลงครบ"
id: "sophos-sfos215-hotfix-firmware-ha"
versions: SFOS 21.5
families: sophos_sfos
triggers: ["ต้องการลง hotfix / firmware บน Sophos XGS HA pair", "ตรวจว่า hotfix ลงครบหรือไม่"]
sources: ["https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html", "https://support.sophos.com/support/s/article/KBA-000010589", "https://docs.sophos.com/nsg/Sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/Firmware/FirmwareFAQs/index.html"]
---

> **หมายเหตุ**: ไฟล์นี้เน้น "ลำดับการอัปเกรดบนคู่ HA + ตรวจ hotfix" — หากต้องการหัวข้ออื่นๆ เช่น "อัปเกรด firmware", "HA status / sync", "สำรองข้อมูล" ให้ดู playbook [`sophos-sfos-21`](../sophos-sfos-21.md)

> **คำเตือน**: ดำเนินการในหน้าต่างบำรุงรักษา (maintenance window) เสมอ

## 1. เตรียมการก่อนอัพเกรด

คำค้น: เตรียมการอัพเกรด, backup, HA health check, disk space

ที่มา: https://docs.sophos.com/nsg/Sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/Firmware/FirmwareFAQs/index.html — `Recommended checklist for all deployments: 1. Take a fresh backup. 2. Verify the available disk space.`

ก่อนเริ่มกระบวนการอัพเกรด:

1. **สำรองการตั้งค่า**: ไปที่ **Backup and firmware** > **Backup** > **Create backup**
2. **ตรวจสอบพื้นที่ดิสก์**: ต้องมีพื้นที่เพียงพอทั้ง primary และ secondary node
3. **ตรวจสอบ upgrade path**: ยืนยันว่าเป็นการอัพเกรดจาก version ที่รองรับ
4. **ตรวจสอบ HA status**: ต้องเป็น healthy และ synchronized
5. **ตรวจสอบว่าทั้ง 2 node มีพื้นที่ดิสก์เพียงพอ**: แต่ละ node ถูกประเมินแยกกัน

### คำสั่งตรวจ

ตรวจใน GUI: ไปที่ **Backup and firmware** > **Backup**

## 2. ลง hotfix / firmware บนคู่ HA

คำค้น: อัพเกรด HA, upgrade firmware HA, primary auxiliary

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html — `The primary device (device A) upgrades the auxiliary device (device B). After the auxiliary device (device B) is upgraded and restarts, it becomes the primary device.`

### คำสั่งตรวจ

ตรวจใน GUI: ไปที่ **Backup and firmware** > **Firmware**

### 2.1 วิธีการอัพเกรด

เมื่ออัพเกรด HA device กระบวนการมีดังนี้ (เอกสาร SFOS 21.5):

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

### 2.3 การ rollback

สามารถ rollback firmware version ของ HA pair ได้ — กระบวนการ rollback ทำเหมือนการอัพเกรด

## 3. ตรวจว่า hotfix ลงครบ

คำค้น: ตรวจ hotfix, verify hotfix, version-info

ที่มา: https://support.sophos.com/support/s/article/KBA-000010589 — `Run the command: system diagnostic show version-info` — `The hotfix is applied if you see HF071525.1 or a later value in the Hotfix tag field.`

### คำสั่งตรวจ

คำสั่งตรวจ:
```
system diagnostic show version-info
```

อ่านผล: ต้องเห็นค่า **Hotfix tag** ในผลลัพธ์

### 3.1 ตรวจสอบ hotfix tag

ตาม KBA-000010589 (ช่องโหว่ CVE-2025-6704, CVE-2025-7624, CVE-2025-7382, CVE-2024-13974):

1. เข้าถึง **Device Console** ของ firewall
2. รันคำสั่ง `system diagnostic show version-info`
3. ดูค่าในช่อง **Hotfix tag**:

   - ค่าที่ต้องเห็น: **HF071525.1** หรือค่าที่สูงกว่านี้
   - **หมายเหตุ**: ค่านี้คือเกณฑ์ของ KBA-000010589 สำหรับชุดช่องโหว่ที่ระบุเท่านั้น — สำหรับ advisory อื่น ให้ดูค่า hotfix tag ที่ advisory นั้นระบุ
   - หากเห็นค่าน้อยกว่านี้ = hotfix ของ advisory นั้นยังไม่ได้ติดตั้ง

### 3.2 ตรวจ hotfix auto-install status

ตรวจสอบว่า hotfix automatic installation เปิดอยู่หรือไม่:

1. ไปที่ **Device Console**
2. รันคำสั่ง `system hotfix show`
3. ค่าที่ต้องเห็น: hotfix auto-install ต้องเป็น **enabled**

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/22.0/Help/en-us/webhelp/onlinehelp/CommandLineHelp/DeviceConsole/SystemCommands/Hotfix/index.html — `system hotfix [enable | disable | show]` — `The firewall looks for hotfixes every 30 minutes. By default, it installs hotfixes automatically. We recommend that you don't change this setting. Default: enabled.`

## 4. ตรวจ HA status หลังอัพเกรด

คำค้น: HA status healthy, failover verification, primary role

ที่มา: https://docs.sophos.com/nsg/Sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html — `Verify that the HA status is healthy.`

### คำสั่งตรวจ

คำสั่งตรวจ:
```
system ha show details
```

อ่านผล: ต้องเห็นสถานะ HA ในผลลัพธ์

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAConfiguration/HAQuickHAConfigureActivePassive/index.html — `To see the HA details on the CLI, enter the following command: system ha show details`

หลังอัพเกรดเสร็จ ต้องตรวจสอบว่า:

1. HA status เป็น healthy
2. Primary/Auxiliary role ถูกต้อง (ตาม Preferred primary setting)
3. Configuration synchronize อยู่
4. Traffic ทำงานปกติ
