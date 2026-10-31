---
id: huawei-ac-radio-roaming
title: Huawei Wireless AC — radio (RRM channel) และ roaming (802.11k/v/r/smart-roam)
families: huawei_ac
triggers: radio, channel, power, bandwidth, roaming, 802.11k, 802.11v, 802.11r, smart-roam, fast-roam, airengine, radio-profile, rrm-profile, vap-profile, ap-group
vendor: Huawei
versions: WLAN AC V200R019C00, V200R021C00, V200R025C00 (AC6005, AC6508, AC6605, AC6805, AC6800V, AirEngine 9700)
sources: WLAN AC V200R019C00 Command Reference — RRM, display rrm-profile, display station roam-track; Configuring Intra-AC Roaming — 802.11r Fast Roaming; Common WLAN Configuration Errors (V200) — CAC, smart-roam thresholds
---
# Huawei Wireless AC — radio (RRM channel) และ roaming (802.11k/v/r/smart-roam)

## Radio: RRM ไม่เปิด / channel selection ไม่ทำงาน / channel clash
คำค้น: rrm, channel, auto channel, channel selection, co-channel, adjacent channel, channel interference, channel utilization, radio profile, channel clash, radio ไม่เลือกช่อง, rrm-profile, calibrate, auto-channel-select, auto-txpower-select
อาการ: AP เลือกช่องที่ชนกับ AP อื่น, RRM ไม่เปิด channel selection, calibration ไม่ทำงาน, channel selection ไม่รันเป็นรอบ
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
3. Channel selection ไม่รันเป็นรอบ (ต้องตั้งค่า interval)
4. AP เลือก channel ที่ชนกับ AP อื่น (ต้องเปิด auto channel ใน rrm-profile)
5. Noise floor สูง → เปลี่ยนไปช่องที่ noise ต่ำกว่า
6. Co-channel interference สูง → เปลี่ยน channel ที่ไม่ชน
7. Adjacent channel interference สูง → เปลี่ยน channel ที่ไม่ติดกัน
วิธีแก้:
- เปิด auto channel: `rrm-profile <name>` → `undo calibrate auto-channel-select disable`
- เปิด auto txpower: `rrm-profile <name>` → `undo calibrate auto-txpower-select disable`
- ปรับ interval: `channel-select interval <minutes>`
- Bind RRM profile กับ radio profile: `radio-2g-profile <name>` → `rrm-profile <name>`
ระวัง: เปลี่ยน channel จะตัดผู้ใช้ชั่วคราว — ทำในช่วง maintenance
ที่มา: WLAN AC V200R019C00 Command Reference — WLAN Radio Resource Management https://support.huawei.com/enterprise/en/doc/EDOC1100156629/a9f0fb2d/wlan-radio-resource-management-configuration-commands-

## Roaming: 802.11k/v/r ไม่ทำงาน / roaming ช้า / roaming หลุด
คำค้น: roaming, 802.11k, 802.11v, 802.11r, fast roaming, smart roam, fast-roam, 802.11k/v/r, roaming ไม่เร็ว, roaming หลุด, roaming timeout, roaming fail, roam-track, dot11r, intra-ac roaming, inter-ac roaming, mobility group, pmk-cache, layer3-roam, smart-roam
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
- `display rrm-profile name <profile>`: ดู smart-roam config — smart-roam, quick-kickoff-threshold, roam-threshold
- `display station roam-track sta-mac <sta-mac>`: ดู roaming track ของ STA — ถ้า roaming บ่อย = แปรปรวน
- `display vap-profile name <profile>`: ดู VAP config — layer3-roam, service-vlan
- `display ssid-profile name <profile>`: ดู SSID config — dot11r, dot11r proprietary, dot11r reassociate-timeout
สาเหตุที่พบบ่อย:
1. 802.11r ไม่เปิด (ต้อง `dot11r enable` ใน ssid-profile)
2. Smart-roam ไม่เปิด (ต้อง `smart-roam enable` ใน rrm-profile)
3. Roaming profile ไม่ถูก bind กับ VAP
4. Roaming profile ถูก bind แต่ไม่ทำงาน (config ผิด)
5. STA roaming บ่อย (flapping) → ตรวจ roaming track, signal coverage
6. Layer3 roaming ถูก disable → ต้อง `undo layer3-roam disable` ใน vap-profile
7. PMK cache ไม่ enable → roaming ช้า
วิธีแก้:
- เปิด 802.11r: `ssid-profile <name>` → `dot11r enable`
- เปิด 802.11r proprietary: `ssid-profile <name>` → `dot11r proprietary`
- เปิด smart-roam: `rrm-profile <name>` → `smart-roam enable`
- เปิด layer3 roaming: `vap-profile <name>` → `undo layer3-roam disable`
- เปิด enhanced PMK cache: `ssid-profile <name>` → `pmk-cache-roam enhancement enable`
- Bind VAP profile กับ radio: `vap-profile <name> wlan <wlan-id> radio { <radio-id> | all }` (wlan-id = VAP ID, integer 1-16)
ระวัง: เปลี่ยน roaming profile จะกระทบผู้ใช้ที่กำลัง roam — ทำในช่วง maintenance
ที่มา: Configuring Intra-AC Roaming — 802.11r Fast Roaming https://info.support.huawei.com/enterprise/en/doc/EDOC1100511825/a8dd847e/configuring-intra-ac-roaming

## Roaming: STA roaming บ่อย / roaming ไม่ smooth / signal แปรปรวน
คำค้น: roaming flapping, roaming แปรปรวน, roaming บ่อย, roaming track, roaming instability, signal fluctuation, roaming ไม่ smooth, roam-track, sta-mac, roaming boundary, roaming trigger, smart-roam threshold, quick-kickoff
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
- `display rrm-profile all`: ดู smart-roam config — roaming threshold, SNR margin
- `display rrm-profile name <profile>`: ดู smart-roam thresholds — standing SNR threshold, quick-kickoff threshold, rate threshold
- `display station roam-track sta-mac <sta-mac>`: ดู roaming track — ถ้า roaming บ่อย = flapping
- `display station all`: ดู station ทั้งหมด — ดู signal strength, connect rate
- `display vap-profile name <profile>`: ดู VAP config — roaming profile ถูก bind ไหม
สาเหตุที่พบบ่อย:
1. Smart-roam SNR threshold สูงเกินไป → STA ถูก kick off บ่อย (ตั้งค่า default 20 dB, สูงสุด 45 dB)
2. Smart-roam rate threshold สูงเกินไป → STA ถูก kick off บ่อย
3. Signal coverage ไม่ต่อเนื่อง → STA roam ระหว่าง AP ที่ signal ใกล้กัน
4. Roaming boundary ไม่ชัดเจน → STA roam เข้า-ออกบ่อย
5. AP deployment ไม่เหมาะสม → coverage ซ้ำซ้อน
วิธีแก้:
- ลด SNR threshold: `rrm-profile <name>` → `smart-roam quick-kickoff-threshold snr <threshold>` (แนะนำ 15-20 dB ใน coverage ดี)
- ลด rate threshold: `rrm-profile <name>` → `smart-roam quick-kickoff-threshold rate <threshold>` (แนะนำ 20% ใน coverage ดี)
- วาง AP ใหม่ → ลด overlap, เพิ่ม distance gap ระหว่าง AP
- ปรับ roaming boundary: `rrm-profile <name>` → `smart-roam roam-threshold snr <threshold>` (range 15-45 dB, default 20 dB)
ระวัง: ปรับ threshold ต่ำเกินไปอาจทำให้ STA ถูก kick off บ่อย — ปรับทีละน้อย
ที่มา: Common WLAN Configuration Errors (V200) — smart-roam thresholds https://support.huawei.com/enterprise/en/doc/EDOC1100253982
