---
id: huawei-s5731-access-hardening-port-security-storm-control
title: Huawei S5731 — Port Security + Storm Control (access hardening)
families: huawei_vrp_s
triggers: s5731, port security, port-security, storm control, storm-control, broadcast storm, unknown multicast, unknown unicast, mac limit, mac-security, sticky mac, restrict action, mac flooding, access hardening, access port security
vendor: Huawei
versions: S5731-H, S5731-S, S5731S-H, S5731S-S (V200R0xx)
sources: S Series Switches Security Hardening Guide V200 (EDOC1100038362 — Port Security); S300/S500/S2700/S5700/S6700 V200R024C00 Command Reference (EDOC1100410645 — storm-control)
---
# Huawei S5731 / Port Security + Storm Control (access hardening)

## Port Security / จำกัดจำนวน MAC + ป้องกัน MAC flooding

ที่มา: S Series Switches Security Hardening Guide V200 / Port Security https://support.huawei.com/enterprise/en/doc/EDOC1100038362/c36ae691/port-security
คำค้น: port security, port-security, mac flooding, mac limit, max-mac, secure mac, sticky mac, restrict action, shutdown action, unauthorized mac, unknown mac
อาการ: มี host ใหม่แอบต่อเข้า port ได้, MAC flooding ทำให้ switch เรียน MAC table เต็ม, port เปิดรับ host ไร้จำกัด, ต้องการจำกัด access port ให้เฉพาะ authorized host
คำสั่งตรวจ:
```
display mac-address security interface gigabitethernet 0/0/1
display mac-address sec-config interface gigabitethernet 0/0/1
display mac-address sticky interface gigabitethernet 0/0/1
display mac-address interface gigabitethernet 0/0/1
display current-configuration interface gigabitethernet 0/0/1
```
อ่านผล:
- `display mac-address security`: ดู secure dynamic MAC entries — MAC ที่เรียนมาแล้วจะถูก convert เป็น secure dynamic
- `display mac-address sec-config`: ดู secure static MAC entries — MAC ที่ admin กำหนดเอง
- `display mac-address sticky`: ดู sticky MAC entries — MAC ที่เรียนแล้วแปลงเป็น sticky auto-convert
- `display mac-address interface`: MAC ทั้งหมดที่ port นั้นเรียนอยู่ (เทียบกับ max-mac-num ที่จะตั้ง)
- `display current-configuration interface`: ต้องเห็น `port-security enable`, `port-security max-mac-num`, `port-security protect-action`
สาเหตุที่พบบ่อย:
1. ไม่ได้เปิด port-security — port อนุญาตทุก MAC ที่เข้ามาได้ (ค่า default)
2. เปิด port-security แต่ตั้งค่า max-mac-num สูงเกินไป — ไม่ป้องกัน MAC flooding
3. ไม่รู้ว่า protect-action ทำอะไร: ค่าเริ่มต้นคือ restrict (drop MAC ที่เกิน + แจ้งเตือน) / protect = drop เงียบ / shutdown = ปิด port
วิธีแก้:
- เปิด port-security + จำกัดจำนวน: `system-view` → `interface gigabitethernet 0/0/1` → `port-security enable` → `port-security max-mac-num 3` (หรือจำนวน host จริง)
- กำหนด action เมื่อเกิน limit: `port-security protect-action restrict` (drop + alert log) หรือ `port-security protect-action shutdown` (ปิด port ทันที)
- ใช้ sticky MAC สำหรับ host รู้จัก: `port-security mac-address sticky` → MAC ที่เรียนครั้งแรกจะถูก save เป็น sticky entry
- ตรวจสอบการตั้งค่า: `display current-configuration interface gigabitethernet 0/0/1`
- ระวัง: port ที่มี IP phone + PC หรือต่อ switch / AP ข้างหลัง ต้องนับ MAC ให้พอ (phone + PC = อย่างน้อย 2) ไม่งั้นเครื่องจริงโดน drop
- ระวัง: ใช้กับ port ผู้ใช้เท่านั้น ห้ามใช้กับ uplink / port ที่ต่อ switch หรือ AP
- บันทึก: `save` (S-series V200 มีผลทันที ไม่ต้อง commit)

## Storm Control / ป้องกัน Broadcast/Multicast/Unicast Storm

ที่มา: S300/S500/S2700/S5700/S6700 V200R024C00 Command Reference / storm-control https://support.huawei.com/enterprise/en/doc/EDOC1100410645/8d1da57f/storm-control
คำค้น: storm control, storm-control, broadcast storm, unknown multicast storm, unknown unicast storm, traffic storm, multicast suppression, unicast suppression, cir threshold, percent threshold, storm action, storm block, storm shutdown
อาการ: broadcast storm ทำให้ switch ช้า / หลุด, port รับ broadcast / unknown multicast / unknown unicast สูงผิดปกติ
คำสั่งตรวจ:
```
display storm-control interface gigabitethernet 0/0/1
display current-configuration interface gigabitethernet 0/0/1
display trapbuffer | include storm
```
อ่านผล:
- `display storm-control interface`: ดู storm control config บน port — threshold broadcast/multicast/unicast, action (block/shutdown), logging status
- `display trapbuffer`: ดู storm-related traps — alarm เมื่อเกิด storm control trigger
สาเหตุที่พบบ่อย:
1. ไม่ได้เปิด storm-control — traffic storm กระจายไปทั้ง network ไม่มี limit
2. ตั้ง threshold สูงเกินไป — broadcast storm ผ่าน threshold ได้ก่อน switch ตอบสนอง
3. ไม่ได้เปิด log/trap — ไม่รู้ว่ามี storm control trigger หรือเมื่อไหร่
วิธีแก้:
- ตั้ง storm control สำหรับ broadcast (แนะนำสูงสุด): `system-view` → `interface gigabitethernet 0/0/1` → `storm-control broadcast min-rate 1000 max-rate 2000` (pps)
- สำหรับ multicast (แนะนำปานกลาง): `storm-control multicast min-rate 500 max-rate 1000`
- สำหรับ unicast (แนะนำเมื่อมีปัญหา): `storm-control unicast min-rate 500 max-rate 1000`
- กำหนด action เมื่อเกิน threshold: `storm-control action block` (ทิ้ง packet ชนิดนั้นจนกว่าจะต่ำกว่า min-rate) หรือ `storm-control action error-down` (port เป็น error-down) — production แนะนำ block
- เปิด logging: `storm-control enable log` — บันทึกเหตุการณ์ลง syslog
- ช่วงเวลาตรวจ: `storm-control interval <วินาที>` (ค่าเริ่มต้น 5 วินาที ส่วนใหญ่ไม่ต้องเปลี่ยน)
- ค่าในตัวอย่าง (pps) เป็นค่าตั้งต้น ให้ดูอัตรา broadcast ปกติของ port ก่อน (`display interface gigabitethernet 0/0/1` ดู Broadcast) แล้วตั้งสูงกว่าช่วงพีค
- ตรวจสอบการตั้งค่า: `display storm-control interface gigabitethernet 0/0/1` → ต้องเห็น thresholds, action, log status
ระวัง: action error-down ทำให้ port ล่มจนกว่าจะกู้: เข้า interface แล้ว `shutdown` ตามด้วย `undo shutdown` หรือตั้งกู้เองด้วย `error-down auto-recovery cause storm-control interval <วินาที>`

## Access Hardening / Port Security + Storm Control พร้อมกัน

ที่มา: Port Security: https://support.huawei.com/enterprise/en/doc/EDOC1100038362/c36ae691/port-security / Storm Control: https://support.huawei.com/enterprise/en/doc/EDOC1100410645/8d1da57f/storm-control
คำค้น: access hardening, access port, secure access, edge port security, network access control, guest network security, user isolation, private-vlan, guest isolation
อาการ: ต้องการให้ access port ปลอดภัยทั้ง MAC limit + storm protection, ป้องกันทั้ง unauthorized access และ broadcast storm, edge port hardening, user-facing port security
คำสั่งตรวจ:
```
display storm-control interface gigabitethernet 0/0/1
display current-configuration interface gigabitethernet 0/0/1 | include port-security
display current-configuration interface gigabitethernet 0/0/1 | include storm-control
```
อ่านผล:
- Port security ต้องเห็น `port-security enable` + `max-mac-num` + `protect-action` ใน config
- Storm control ต้อง enabled + มี thresholds + action + log
- `display current-configuration`: ต้องเห็น port-security และ storm-control config ทั้งคู่
วิธีแก้ (เฉพาะ port ผู้ใช้ ไม่ใช่ uplink / AP / IP phone ที่มี PC ต่อพ่วงต้องนับ MAC เพิ่ม):
- `system-view` → `interface gigabitethernet 0/0/1` → `port link-type access` → `port-security enable` → `port-security max-mac-num 3` → `port-security protect-action restrict` → `storm-control broadcast min-rate 1000 max-rate 2000` → `storm-control multicast min-rate 500 max-rate 1000` → `storm-control action block` → `storm-control enable log` → `save`
- ตรวจสอบ: `display current-configuration interface gigabitethernet 0/0/1` → ต้องเห็นทั้ง port-security และ storm-control
