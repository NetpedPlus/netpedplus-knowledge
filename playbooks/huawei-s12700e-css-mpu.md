---
id: huawei-s12700e-css-mpu
title: Huawei S12700E — MPU switchover และ CSS Fast Upgrade / ISSU
families: huawei_vrp_s
triggers: s12700, s12700e, css, cluster, mpu, switchover, slave switchover, mpu failure, mpu fault, css fast upgrade, css issu, in-service software upgrade, issu, display switchover state, ha
vendor: Huawei
versions: S12700, S12700E (V200R021C00, V200R023C00, V200R024C00)
sources: S12700/S12700E V200R023C00 Config Guide — Master/Standby Switchover, 1+N MPU Backup; V200R021C00/V200R024C10 Command Reference — CSS ISSU/Fast Upgrade commands
---
# Huawei S12700E — MPU switchover และ CSS Fast Upgrade / ISSU

## MPU switchover (manual) / 1+N Backup
คำค้น: mpu, switchover, mpu switchover, slave switchover, master standby switchover, 1+n backup, ha, active standby, display switchover state, ha fsm, mpu failure, mpu fault, mpu replacement, mpu hot backup
อาการ: MPU master ไม่ทำงาน, ต้องการ manual switchover, MPU hot backup ไม่ทำงาน, HA state ไม่เป็น realtime backup, MPU replace ระหว่างทำงาน
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
3. MPU slot ไม่ครบ (standby chassis ต้องมี MPU installed)
4. 1+N backup: standby chassis ไม่มี MPU → CSS ทำงาน single-MPU state (ส่ง alarm เป็นระยะ)
วิธีแก้:
- Enable switchover: `system-view` → `slave switchover enable`
- Trigger switchover: `system-view` → `slave switchover`
- ตรวจสอบ HA state ก่อน switchover: `display switchover state` → ต้องเป็น realtime backup
- Install MPU ใน standby chassis: ถ้าใช้ 1+N backup, ต้องติดตั้ง MPU ใน standby chassis
ระวัง: หลัง switchover, previous master MPU จะ restart และกลายเป็น standby — ทำในช่วง maintenance ไม่กระทบ data forwarding แต่ config changes อาจสูญหายระหว่าง switchover
ที่มา: S12700/S12700E V200R023C00 Config Guide — Configuring a Master/Standby Switchover https://support.huawei.com/enterprise/en/doc/EDOC1100333876/5a1b72e/configuring-a-master-standby-switchover

## CSS Fast Upgrade / ISSU Upgrade
คำค้น: css fast upgrade, css issu, in-service software upgrade, issu, software upgrade, version upgrade, css upgrade, css fast upgrade state, display css issu state, css issu start, css issu switchover, css issu confirm, css issu abort, display patch-information, patch, version rollback
อาการ: ต้องการ upgrade CSS software ระหว่างทำงาน, fast upgrade ไม่สำเร็จ, ISSU switchover timeout, version rollback หลัง upgrade, patch ไม่ติดตั้ง
คำสั่งตรวจ:
```
display css fast upgrade state
display css issu state
display version
display patch-information
```
อ่านผล:
- `display css fast upgrade state`: ดู fast upgrade phase — phase ที่กำลังทำงาน, status
- `display css issu state`: ดู ISSU status — start, switchover, confirm phases
- `display version`: ดู version ปัจจุบัน, next-startup software
- `display patch-information`: ดู patch status, patch name
สาเหตุที่พบบ่อย:
1. Fast upgrade ล้มเหลว — standby chassis rollback (max 1 hour), ports บน standby Down
2. ISSU switchover timeout — ต้อง run `css issu switchover` ก่อน rollback timer expire
3. ISSU confirm timeout — ต้อง run `css issu confirm` หลัง switchover เสร็จ
4. Version ไม่รองรับ fast upgrade — ตรวจ software package support
5. Standby chassis ไม่มี MPU → fast upgrade อาจถูกยกเลิก (ดูเงื่อนไขในหน้า Upgrading CSS Software)
วิธีแก้:
- ตรวจ ISSU feasibility ก่อน upgrade: `css issu check <system-file>`
- Start ISSU: `css issu start <system-file>` (automatic) หรือ `css issu start rollback-timer <timer> <system-file>` (manual)
- Trigger switchover (manual mode): `css issu switchover` (ก่อน rollback timer expire)
- Confirm upgrade: `css issu confirm` (หลัง switchover เสร็จ)
- Abort upgrade: `css issu abort` (ก่อน confirm)
- Fast upgrade: `css fast upgrade` (ถ้า software package รองรับ)
- ตรวจสอบ MAC หลัง upgrade: `set css system-mac chassis <chassis-id>` (ถ้า MAC เปลี่ยน)
ระวัง: ระหว่าง upgrade, services บน master switch ยังทำงานปกติ, standby port Down — อย่าทำ operation บน standby chassis (install, remove, reset, power off boards) ระหว่าง rollback
ที่มา: S12700/S12700E V200R024C00 Config Guide — Upgrading CSS Software https://support.huawei.com/enterprise/en/doc/EDOC1100410571/6ceca878/upgrading-css-software
