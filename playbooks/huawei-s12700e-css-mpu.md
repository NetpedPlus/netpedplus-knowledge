---
id: huawei-s12700e-css-mpu
title: Huawei S12700E — CSS (Cluster) และ MPU switchover
families: huawei_vrp_s
triggers: s12700, s12700e, css, cluster, mpu, css-split, css-port, css fast upgrade, css issu, css split upgrade, slave switchover, css status, css port
vendor: Huawei
versions: S12700, S12700E (V200R021C00, V200R023C00, V200R024C00)
sources: S12700/S12700E V200R023C00 Config Guide — Master/Standby Switchover, 1+N MPU Backup; V200R021C00/V200R024C10 Command Reference — CSS commands; S12700/V200 CSS Split Upgrade Guide
---
# Huawei S12700E — CSS (Cluster) และ MPU switchover

## CSS ไม่ขึ้น / CSS Split / CSS Port Down
คำค้น: css, cluster, css-split, css split, css port, css port down, css port up, css member, css enable, css status, css priority, css mode, css card, css css-port, CSS ไม่ขึ้น, CSS แตก, CSS ไม่ join, member switch ไม่ join, CSS port down, CSS port up
อาการ: CSS ไม่ขึ้น, CSS Split, CSS Port Down, member switch ไม่ join, CSS port ไม่เห็น status
คำสั่งตรวจ:
```
display css status
display css status saved
display css port
display css css-port
display css system-mac
```
อ่านผล:
- `display css status`: ดู CSS status — CSS Enable, Chassis Id, CSS Status (Master/Standby), CSS Mode (CSS card / LPU)
- `display css status saved`: ดู saved CSS config — Current Id, Saved Id, CSS Enable, Priority
- `display css port`: ดู CSS port status (CSS card mode) — port status, packet statistics
- `display css css-port`: ดู CSS port configuration (service port mode) — S12700E เท่านั้น
- `display css system-mac`: ดู CSS MAC address — หลัง restart หรือ replace MPU, MAC อาจเปลี่ยน
สาเหตุที่พบบ่อย:
1. CSS ไม่ enable (ต้อง `css enable` ใน system view)
2. CSS priority ไม่ตรง (master ต้อง priority สูงกว่า)
3. CSS port down — ตรวจ cable, SFP, port configuration
4. CSS mode ไม่ตรง (S12700 ใช้ CSS card, S12700E ใช้ service port / LPU)
5. MAC address เปลี่ยนหลัง upgrade — ต้อง `set css system-mac chassis <chassis-id>`
วิธีแก้:
- Enable CSS: `system-view` → `css enable`
- ตั้ง priority: `system-view` → `set css priority <1-255>` (master ต้องสูงกว่า)
- ตรวจ CSS port: `display css css-port` (S12700E) → ตรวจ cable, SFP, interface status
- ตั้ง MAC CSS ใหม่: `system-view` → `set css system-mac chassis <chassis-id>`
- Restart member switch หลัง config: `reboot`
ระวัง: CSS split จะทำให้ services ขาดหาย — ตรวจ CSS port ก่อน restart, ทำในช่วง maintenance
ที่มา: S12700/S12700E V200R021C00 Command Reference — CSS configuration commands https://support.huawei.com/enterprise/en/doc/EDOC1100214492/48610b6b/css-configuration-commands

## MPU switchover (manual) / 1+N Backup
คำค้น: mpu, switchover, mpu switchover, slave switchover, master standby switchover, 1+n backup, ha, active standby, display switchover state, HA FSM, MPU failure, mpu fault, mpu replacement, mpu hot backup
อาการ: MPU master故障, ต้องการ manual switchover, MPU hot backup ไม่ทำงาน, HA state ไม่เป็น realtime backup, MPU replace ระหว่างทำงาน
คำสั่งตรวจ:
```
display switchover state
display css status
display device
```
อ่านผล:
- `display switchover state`: ดู switchover status — HA FSM State(master) ต้องเป็น **realtime or routine backup**, HA FSM State(slave) ต้องเป็น **receiving realtime or routine data**
- `display css status`: ดู CSS status — CSS status, member switch roles
- `display device`: ดู device health — MPU status, power, fan, temperature
สาเหตุที่พบบ่อย:
1. MPU standby ไม่อยู่ใน hot backup state (ต้องเป็น realtime backup ก่อน switchover)
2. Master/Standby switchover ถูก disable (ต้อง `slave switchover enable`)
3. Switchover prohibit ถูก enable (ต้อง `undo switchover-prohibit enable`)
4. MPU slot ไม่ครบ (standby chassis ต้องมี MPU installed)
5. 1+N backup: standby chassis ไม่มี MPU → CSS ทำงาน single-MPU state (ส่ง alarm ทุก 30 นาที)
วิธีแก้:
- Enable switchover: `system-view` → `slave switchover enable`
- Trigger switchover: `system-view` → `slave switchover`
- ตรวจสอบ HA state ก่อน switchover: `display switchover state` → ต้องเป็น realtime backup
- Install MPU ใน standby chassis: ถ้าใช้ 1+N backup, ต้องติดตั้ง MPU ใน standby chassis
- ตรวจสอบ alarm: `display alarm active` → hwCssStandbyError (CSSM_1.3.6.1.4.1.2011.5.25.183.3.3.2.16)
ระวัง: หลัง switchover, previous master MPU จะ restart และกลายเป็น standby — ทำในช่วง maintenance ไม่กระทบ data forwarding แต่ config changes อาจสูญหายระหว่าง switchover
ที่มา: S12700/S12700E V200R023C00 Config Guide — Configuring a Master/Standby Switchover https://support.huawei.com/enterprise/en/doc/EDOC1100333876/5a1b72e/configuring-a-master-standby-switchover

## CSS Fast Upgrade / ISSU Upgrade
คำค้น: css fast upgrade, css issu, in-service software upgrade, issu, css split upgrade, software upgrade, version upgrade, css upgrade, css fast upgrade state, display css issu state, css issu start, css issu switchover, css issu confirm, css issu abort, css rollback
อาการ: ต้องการ upgrade CSS software ระหว่างทำงาน, fast upgrade ไม่สำเร็จ, ISSU switchover timeout, version rollback หลัง upgrade
คำสั่งตรวจ:
```
display css fast upgrade state
display css issu state
display version
display patch state
```
อ่านผล:
- `display css fast upgrade state`: ดู fast upgrade phase — phase ที่กำลังทำงาน, status
- `display css issu state`: ดู ISSU status — start, switchover, confirm phases
- `display version`: ดู version ปัจจุบัน, next-startup software
- `display patch state`: ดู patch status, patch name
สาเหตุที่พบบ่อย:
1. Fast upgrade ล้มเหลว — standby chassis rollback (max 1 hour), ports บน standby Down
2. ISSU switchover timeout — ต้อง run `css issu switchover` ก่อน rollback timer expire
3. ISSU confirm timeout — ต้อง run `css issu confirm` หลัง switchover เสร็จ
4. Version ไม่รองรับ fast upgrade — ตรวจ software package support
5. Standby chassis ไม่มี MPU → fast upgrade หยุด max 10 นาที, cancel หลัง 10 นาที
วิธีแก้:
- ตรวจ ISSU feasibility ก่อน upgrade: `css issu check <system-file>`
- Start ISSU: `css issu start <system-file>` (automatic หรือ manual mode)
- Trigger switchover (manual mode): `css issu switchover` (ก่อน rollback timer expire)
- Confirm upgrade: `css issu confirm` (หลัง switchover เสร็จ)
- Abort upgrade: `css issu abort` (ก่อน confirm)
- Fast upgrade: `css fast upgrade` (ถ้า software package รองรับ)
- ตรวจสอบ MAC หลัง upgrade: `set css system-mac chassis <chassis-id>` (ถ้า MAC เปลี่ยน)
ระวัง: ระหว่าง upgrade, services บน master switch ยังทำงานปกติ, standby port Down — อย่าทำ operation บน standby chassis (install, remove, reset, power off boards) ระหว่าง rollback
ที่มา: CSS Split Upgrade Guide for S Series Switches (V200) https://support.huawei.com/enterprise/en/doc/EDOC1100199066
