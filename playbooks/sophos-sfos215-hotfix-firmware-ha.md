---
title: "Sophos SFOS 21.5: ลง hotfix / firmware บนคู่ HA + ตรวจว่า hotfix ลงครบ"
id: "sophos-sfos215-hotfix-firmware-ha"
versions: SFOS 21.5
vendor: Sophos
families: sophos_sfos
triggers: [sophos, sfos, xgs, hotfix, firmware, ha, upgrade, maintenance]
sources: ["https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html", "https://support.sophos.com/support/s/article/KBA-000010589", "https://docs.sophos.com/nsg/Sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/Firmware/FirmwareFAQs/index.html"]
---

> **หมายเหตุ**: ไฟล์นี้เน้น "ลำดับการอัปเกรดบนคู่ HA + ตรวจ hotfix" — หากต้องการหัวข้ออื่นๆ เช่น "HA status / sync", "สำรองข้อมูล" ให้ดู playbook [`sophos-sfos-21`](../sophos-sfos-21.md)

# Sophos SFOS 21.5: ลง hotfix / firmware บนคู่ HA + ตรวจ hotfix

> **ระวัง**: การลง firmware ทำให้ device รีบูตและมีช่วงที่ traffic สลับเครื่อง — วางแผน maintenance window และตรวจสอบ HA status หลังลง firmware ทุกครั้ง

> **ที่มา**: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html

## ลำดับการอัปเกรดบนคู่ HA

คำค้น: อัพเกรด HA, upgrade firmware HA, primary auxiliary

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html — `The primary device (device A) upgrades the auxiliary device (device B). After the auxiliary device (device B) is upgraded and restarts, it becomes the primary device.`

### คำสั่งตรวจ

คำสั่งตรวจ:
```
system ha show details
```

อ่านผล: ต้องเห็นสถานะ HA

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAConfiguration/HAQuickHAConfigureActivePassive/index.html — `To see the HA details on the CLI, enter the following command: system ha show details`

เมื่ออัพเกรด HA device กระบวนการมีดังนี้ (เอกสาร SFOS 21.5):

1. เริ่มอัพเกรดจาก **primary device** เท่านั้น
2. Primary device (device A) อัพเกรด auxiliary device (device B)
3. Auxiliary device (device B) ที่อัพเกรดแล้วรีบูต และกลายเป็น primary device
4. Former primary (device A) อัพเกรดตัวเองและรีบูต
5. หากตั้งค่า **Preferred primary device** ไว้ failover จะเกิดขึ้น และ device A กลับมาเป็น primary

## ตรวจว่า hotfix ลงครบ

คำค้น: ตรวจ hotfix, verify hotfix, version-info

ที่มา: https://support.sophos.com/support/s/article/KBA-000010589 — `Run the command: system diagnostic show version-info` — `The hotfix is applied if you see HF071525.1 or a later value in the Hotfix tag field.`

### คำสั่งตรวจ

คำสั่งตรวจ:
```
system diagnostic show version-info
```

อ่านผล: ต้องเห็นค่า **Hotfix tag** ในผลลัพธ์

### ตรวจสอบ hotfix tag

ตาม KBA-000010589 (ช่องโหว่ CVE-2025-6704, CVE-2025-7624, CVE-2025-7382, CVE-2024-13974):

1. เข้าถึง **Device Console** ของ firewall
2. รันคำสั่ง `system diagnostic show version-info`
3. ดูค่าในช่อง **Hotfix tag**:

   - ค่าที่ต้องเห็น: **HF071525.1** หรือ hotfix tag ที่ออก **หลังวันที่ 15 ก.ค. 2025** (รูปแบบ `HF<MMDDYY>.n` — อ่าน MMDDYY เป็นวันที่ ไม่ใช่ตัวเลข เช่น HF090125 (ก.ย. 2025) ใหม่กว่า HF071525 (ก.ค. 2025) แม้ค่าตัวเลขจะน้อยกว่า)
   - **หมายเหตุ**: ค่านี้คือเกณฑ์ของ KBA-000010589 สำหรับชุดช่องโหว่ที่ระบุเท่านั้น — สำหรับ advisory อื่น ให้ดูค่า hotfix tag ที่ advisory นั้นระบุ
   - หาก tag เก่ากว่า 15 ก.ค. 2025 = hotfix ของ advisory นั้นยังไม่ได้ติดตั้ง

### ตรวจ hotfix auto-install status

ตรวจสอบว่า hotfix automatic installation เปิดอยู่หรือไม่:

1. ไปที่ **Device Console**
2. รันคำสั่ง `system hotfix show`
3. ค่าที่ต้องเห็น: hotfix auto-install ต้องเป็น **enabled**

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/CommandLineHelp/DeviceConsole/SystemCommands/Hotfix/index.html — `system hotfix [enable | disable | show]` — `The firewall looks for hotfixes every 30 minutes. By default, it installs hotfixes automatically. We recommend that you don't change this setting. Default: enabled.`
