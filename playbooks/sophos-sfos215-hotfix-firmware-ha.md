---
title: "Sophos SFOS 21.5: ลง hotfix / firmware บนคู่ HA + ตรวจว่า hotfix ลงครบ"
id: "sophos-sfos215-hotfix-firmware-ha"
versions: SFOS 21.5
vendor: Sophos
families: sophos_sfos
triggers: [sophos, sfos, xgs, hotfix, firmware, ha, upgrade, maintenance]
sources: ["https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html", "https://support.sophos.com/support/s/article/KBA-000010589", "https://docs.sophos.com/nsg/Sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/Firmware/FirmwareFAQs/index.html", "https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAConfiguration/HAQuickHAConfigureActivePassive/index.html"]
---

> **หมายเหตุ**: ไฟล์นี้เน้น "ลำดับการอัปเกรดบนคู่ HA + ตรวจ hotfix" — หากต้องการหัวข้ออื่นๆ เช่น "HA status / sync", "สำรองข้อมูล" ให้ดูหัวข้อใน `sophos-sfos-21` ข้อ 'HA (Active-Passive) สถานะ / สลับเครื่อง / sync' และ 'อัปเกรด firmware / สำรองข้อมูล'

# Sophos SFOS 21.5: ลง hotfix / firmware บนคู่ HA + ตรวจ hotfix

> **ระวัง**: การลง firmware ทำให้ device รีบูตและมีช่วงที่ traffic สลับเครื่อง — วางแผน maintenance window และตรวจสอบ HA status หลังลง firmware ทุกครั้ง

## ลำดับการอัปเกรดบนคู่ HA

คำค้น: อัพเกรด HA, upgrade firmware HA, primary auxiliary

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/HighAvailablityStartupGuide/HAManage/HAFirmwareUpgrade/index.html — `The primary device (device A) upgrades the auxiliary device (device B). After the auxiliary device (device B) is upgraded and restarts, it becomes the primary device.`

### คำสั่งตรวจ

คำสั่งตรวจ:
```
system ha show details
```

อ่านผล: ต้องเห็นสถานะ HA

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

### ตรวจสอบ hotfix tag

ตาม KBA-000010589:

1. เข้าถึง **Device Console** ของ firewall
2. รันคำสั่ง `system diagnostic show version-info`
3. ดูค่าในช่อง **Hotfix tag**:

   - ค่าที่ต้องเห็น: **HF071525.1** หรือค่าที่สูงกว่านี้
   - **หมายเหตุ**: ค่านี้คือเกณฑ์ของ KBA-000010589 สำหรับชุดช่องโหว่ที่ระบุเท่านั้น — สำหรับ advisory อื่น ให้ดูค่า hotfix tag ที่ advisory นั้นระบุ
   - หากเห็นค่าน้อยกว่านี้ = hotfix ของ advisory นั้นยังไม่ได้ติดตั้ง

> **คำเตือน**: KBA-000010589 ระบุ hotfix สำหรับชุดช่องโหว่ CVE-2025-6704, CVE-2025-7624, CVE-2025-7382, CVE-2024-13974 — ตรวจสอบว่า CVE เหล่านี้ยังเกี่ยวข้องกับ SFOS 21.5 หรือไม่ (บาง CVE อาจถูกแก้ไขมาใน SFOS 21.5 GA แล้ว)
