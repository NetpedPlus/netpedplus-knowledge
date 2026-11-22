---
title: "Sophos SFOS 21.5: ลง hotfix / firmware บนคู่ HA + ตรวจว่า hotfix ลงครบ"
id: "sophos-sfos215-hotfix-firmware-ha"
versions: SFOS 21.5
vendor: Sophos
families: sophos_sfos
triggers: [sophos, sfos, xgs]
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

อ่านผล: ดูรายละเอียด HA ของคู่เครื่อง (เทียบกับหน้า GUI ก่อนและหลังอัปเกรด)

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

### ตรวจสอบ hotfix tag

ตาม KBA-000010589:

1. เข้าถึง **Device Console** ของ firewall
2. รันคำสั่ง `system diagnostic show version-info`
3. ดูค่าในช่อง **Hotfix tag**:

   - ค่าที่ต้องเห็น: **HF071525.1** หรือ tag ที่ออกหลังจากนั้น (ตาม KBA: "or a later value")
   - **หมายเหตุ**: ค่านี้คือเกณฑ์ของ KBA-000010589 สำหรับชุดช่องโหว่ที่ระบุเท่านั้น — สำหรับ advisory อื่น ให้ดูค่า hotfix tag ที่ advisory นั้นระบุ

> **หมายเหตุ**: ตาม advisory [sophos-sa-20250721-sfos-rce](https://www.sophos.com/en-us/security-advisories/sophos-sa-20250721-sfos-rce): SFOS 21.5 GA โดน CVE-2025-6704 / 7624 / 7382 และ Sophos ออก hotfix สำหรับ 21.5 GA (21.5.0.171) — ตรวจว่า hotfix ลงครบด้วย KBA-000010589 (CVE-2024-13974 / 13973 ไม่กระทบ 21.5)

## ช่องโหว่ kernel TCP CVE-2026-98432 กับ SFOS 21.5 (hotfix HF110626.1)

คำค้น: cve-2026-98432, hf110626.1, kernel tcp, ช่องโหว่ kernel, hotfix kernel, sophos hotfix list, ไม่มี hotfix, อัปเกรด sfos 22
อาการ: Sophos ประกาศ advisory sophos-sa-20261102-linux-kernel-tcp (ระดับ High) ต้องรู้ว่าเครื่อง SFOS 21.5 ได้ hotfix หรือไม่
คำสั่งตรวจ:
```
system diagnostic show version-info
```
อ่านผล:
- ดูเวอร์ชัน SFOS ของเครื่อง advisory ระบุว่า hotfix ออกให้เฉพาะ "v23.0 GA, v23.0 EAP1 and v22.0 MR3" (6 พ.ย. 2026) และ "v22.0 GA, v22.0 MR1 and v22.0 MR2" (19 พ.ย. 2026)
- ถ้าเป็น SFOS 21.5: advisory เขียนว่า "If your firewall is running a different version, we recommend upgrading to a supported version (v22.0 or v23.0) to receive the hotfix."
- advisory: "Sophos is not aware of any public reports of this vulnerability being exploited in the wild at this time."
- workaround ปิด MPTCP ในหน้า advisory ใช้กับระบบ Linux อื่น "does not apply to the Sophos products listed above"
วิธีแก้:
- อัปเกรดเป็น v22.0 หรือ v23.0 ตามหัวข้อ "ลำดับการอัปเกรดบนคู่ HA" แล้วตรวจ hotfix ที่ Device Console (เมนู 4) ด้วย `system hotfix list` ต้องเห็น HF110626.1 สถานะ Installed (ใน HA คำสั่งนี้ใช้ได้เฉพาะเครื่อง primary)
- ถ้ายังไม่เปิดติดตั้ง hotfix อัตโนมัติ วางเองที่ Device Console: `system hotfix enable`
- hotfix ผูกกับเวอร์ชันที่ลง: อัปเกรดจาก 22.0 MR3 เป็น 23.0 GA แล้วต้องลง hotfix ใหม่
ระวัง: ต้อง restart firewall เพื่อติดตั้ง hotfix ("interrupts traffic, so schedule it during a maintenance window") บนคู่ HA ให้ restart เครื่อง auxiliary ก่อน แล้วค่อย primary
ที่มา: Sophos Advisory: Linux Kernel TCP Vulnerability (CVE-2026-98432) https://www.sophos.com/en-us/security-advisories/sophos-sa-20261102-linux-kernel-tcp และ Sophos Firewall: Hotfix for CVE-2026-98432 kernel vulnerability https://community.sophos.com/sophos-xg-firewall/b/blog/posts/sophos-firewall-hotfix-for-cve-2026-98432-kernel-vulnerability
