---
id: huawei-ac-radio-roaming
title: Huawei Wireless AC — radio (RRM channel) และ roaming (802.11k/v/r/smart-roam)
families: huawei_ac
triggers: radio, channel, power, bandwidth, roaming, 802.11k, 802.11v, 802.11r, smart-roam, fast-roam, airengine, radio-profile, rrm-profile, vap-profile, ap-group
vendor: Huawei
versions: WLAN AC V200R019C00, V200R021C00, V200R025C00 (AC6005, AC6508, AC6605, AC6805, AC6800V, AirEngine 9700)
sources: WLAN AC V200R019C00 Command Reference — RRM, display rrm-profile, display station roam-track; Configuring Intra-AC Roaming — 802.11r Fast Roaming
---
# Huawei Wireless AC — radio (RRM channel) และ roaming (802.11k/v/r/smart-roam)

## Radio: RRM ไม่เปิด / channel selection ไม่ทำงาน / channel clash
คำค้น: rrm, channel, auto channel, channel selection, co-channel, adjacent channel, channel interference, channel utilization, radio profile, channel clash, radio ไม่เลือกช่อง, rrm-profile, calibrate, auto-channel-select, auto-txpower-select
อาการ: AP เลือกช่องที่ชนกับ AP อื่น, RRM ไม่เปิด channel selection, calibration ไม่ทำงาน
คำสั่งตรวจ:
```
display rrm-profile all
display rrm-profile name <profile-name>
display references rrm-profile
```
อ่านผล:
- `display rrm-profile all`: ดู RRM profile ทั้งหมด — ดูว่า profile ถูก bind กับ radio profile ไหน
- `display rrm-profile name <profile>`: ดู config ของ RRM profile — auto channel select, auto txpower-select ต้อง enable
- `display references rrm-profile`: ดูว่า RRM profile ถูก reference โดยใคร (radio profile, ap-group)
สาเหตุที่พบบ่อย:
1. RRM ไม่เปิด auto channel selection (ต้อง `undo calibrate auto-channel-select disable`)
2. RRM ไม่เปิด auto txpower selection (ต้อง `undo calibrate auto-txpower-select disable`)
3. AP เลือก channel ที่ชนกับ AP อื่น (ต้องเปิด auto channel ใน rrm-profile)
4. Noise floor สูง → เปลี่ยนไปช่องที่ noise ต่ำกว่า
5. Co-channel interference สูง → เปลี่ยน channel ที่ไม่ชน
6. Adjacent channel interference สูง → เปลี่ยน channel ที่ไม่ติดกัน
วิธีแก้:
- เปิด auto channel: `rrm-profile <name>` → `undo calibrate auto-channel-select disable`
- เปิด auto txpower: `rrm-profile <name>` → `undo calibrate auto-txpower-select disable`
- Bind RRM profile กับ radio profile: `radio-2g-profile <name>` → `rrm-profile <name>`
ระวัง: เปลี่ยน channel จะตัดผู้ใช้ชั่วคราว — ทำในช่วง maintenance
ที่มา: WLAN AC V200R019C00 Command Reference — WLAN Radio Resource Management https://support.huawei.com/enterprise/en/doc/EDOC1100156629/a9f0fb2d/wlan-radio-resource-management-configuration-commands-

## Roaming: 802.11k/v/r ไม่ทำงาน / roaming ช้า / roaming หลุด
คำค้น: roaming, 802.11k, 802.11v, 802.11r, fast roaming, smart roam, fast-roam, 802.11k/v/r, roaming ไม่เร็ว, roaming หลุด, roaming timeout, roaming fail, roam-track, dot11r, intra-ac roaming, inter-ac roaming, smart-roam
อาการ: Roaming ช้า, 802.11r ไม่ทำงาน, roaming ไม่เร็ว, roaming หลุดระหว่าง roam, roaming timeout สูง, roaming fail
คำสั่งตรวจ:
```
display rrm-profile all
display rrm-profile name <profile-name>
display station roam-track sta-mac <sta-mac>
display vap-profile name <vap-profile-name>
display ssid-profile name <ssid-profile-name>
```
อ่านผล:
- `display rrm-profile all`: ดู RRM profile ทั้งหมด — ดู smart-roam config
- `display rrm-profile name <profile>`: ดู smart-roam config — smart-roam, quick-kickoff-threshold
- `display station roam-track sta-mac <sta-mac>`: ดู roaming track ของ STA — ถ้า roaming บ่อย = แปรปรวน
- `display vap-profile name <profile>`: ดู VAP config — service-vlan, profile ที่ bind
- `display ssid-profile name <profile>`: ดู SSID config — dot11r
สาเหตุที่พบบ่อย:
1. 802.11r ไม่เปิด (ต้อง `dot11r enable` ใน ssid-profile)
2. Smart-roam ไม่เปิด (ต้อง `smart-roam enable` ใน rrm-profile)
3. VAP profile ไม่ได้ bind กับ radio ของ AP ที่ STA roam ไปหา
4. STA roaming บ่อย (flapping) → ตรวจ roaming track, signal coverage (หัวข้อถัดไป)
วิธีแก้:
- เปิด 802.11r: `ssid-profile <name>` → `dot11r enable`
- เปิด smart-roam: `rrm-profile <name>` → `smart-roam enable`
- Bind VAP profile กับ radio: `vap-profile <name> wlan <wlan-id> radio { <radio-id> | all }` (wlan-id = VAP ID, integer 1-16)
ระวัง: เปลี่ยน ssid-profile / vap-profile จะกระทบผู้ใช้ที่เชื่อมต่ออยู่ — ทำในช่วง maintenance
ที่มา: Configuring Intra-AC Roaming — 802.11r Fast Roaming https://info.support.huawei.com/enterprise/en/doc/EDOC1100511825/a8dd847e/configuring-intra-ac-roaming

## Roaming: STA roaming บ่อย / roaming ไม่ smooth / signal แปรปรวน
คำค้น: roaming flapping, roaming แปรปรวน, roaming บ่อย, roaming track, roaming instability, signal fluctuation, roaming ไม่ smooth, roam-track, sta-mac, roaming trigger, smart-roam threshold, quick-kickoff
อาการ: STA roaming บ่อยเกินไป, roaming ไม่ smooth, signal แปรปรวน, roaming boundary ไม่ชัดเจน
คำสั่งตรวจ:
```
display rrm-profile all
display rrm-profile name <profile-name>
display station roam-track sta-mac <sta-mac>
display station all
display vap-profile name <vap-profile-name>
```
อ่านผล:
- `display rrm-profile all`: ดู RRM profile ทั้งหมด
- `display rrm-profile name <profile>`: ดู smart-roam / quick-kickoff threshold ที่ตั้งไว้
- `display station roam-track sta-mac <sta-mac>`: ดู roaming track — ถ้า roaming บ่อย = flapping
- `display station all`: ดู station ทั้งหมด — ดู signal strength, connect rate
- `display vap-profile name <profile>`: ดู VAP config ที่ STA ใช้
สาเหตุที่พบบ่อย:
1. Smart-roam SNR threshold สูงเกินไป → STA ถูก kick off บ่อย
2. Signal coverage ไม่ต่อเนื่อง → STA roam ระหว่าง AP ที่ signal ใกล้กัน
3. Roaming boundary ไม่ชัดเจน → STA roam เข้า-ออกบ่อย
4. AP deployment ไม่เหมาะสม → coverage ซ้ำซ้อน
วิธีแก้:
- ปรับ SNR threshold: `rrm-profile <name>` → `smart-roam quick-kickoff-threshold snr <threshold>` (ค่าเริ่มต้น / ช่วงค่า ดู Command Reference ของเวอร์ชันที่ใช้)
- วาง AP ใหม่ → ลด overlap, เพิ่ม distance gap ระหว่าง AP
ระวัง: ปรับ threshold ทีละน้อยแล้วดูผลด้วย roam-track — ค่าสูงขึ้น = STA ถูกเตะให้ roam เร็วขึ้น
ที่มา: WLAN AC V200R019C00 Command Reference — WLAN Radio Resource Management (smart-roam) https://support.huawei.com/enterprise/en/doc/EDOC1100156629/a9f0fb2d/wlan-radio-resource-management-configuration-commands-
