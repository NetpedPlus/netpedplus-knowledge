---
id: huawei-ac-radio-roaming
title: Huawei Wireless AC — radio (channel, power, bandwidth) และ roaming (802.11k/v/r)
families: huawei_ac
triggers: radio, channel, power, bandwidth, roaming, 802.11k, 802.11v, 802.11r, smart-roam, fast-roam, airengine, radio-profile
vendor: Huawei
versions: WLAN AC V200R019C00, V200R021C00, V200R025C10 (AC6005, AC6508, AC6605, AC6805, AC6800V, AirEngine 9700)
sources: Huawei WLAN AC V200R019C00 Configuration Guide - Radio Management (RRM); info.support.huawei.com tsrev_wlan — RRM configuration, Radio calibration, 802.11k/v/r fast roaming; Huawei WLAN AC V200R025C10 Command Reference — display rrm, display station statistics, display vap all
---
# Huawei Wireless AC — radio (channel, power, bandwidth) และ roaming (802.11k/v/r)

## Radio: เลือกช่องสัญญาณอัตโนมัติ (RRM channel) ไม่เหมาะสม / ช่องชนกัน
คำค้น: rrm, channel, auto channel, channel selection, co-channel, adjacent channel, channel interference, channel utilization, radio profile, channel clash, radio ไม่เลือกช่อง
อาการ: AP เลือกช่องที่ชนกับ AP อื่น, CU สูง (>60%), channel utilization สูง, ช่องสัญญาณไม่ดี
คำสั่งตรวจ:
```
display rrm-profile all
display ap radio-channel-utilization all
display ap radio-environment ap-id <ap-id> radio <radio-id>
display radio ap-id <ap-id>
```
อ่านผล:
- `display rrm-profile all`: ดู RRM profile — channel selection ต้องเปิด (`enable`), calibration ต้องเปิด
- `display ap radio-channel-utilization all`: ดู CU ของแต่ละ AP — CU > 60% = รบกวนหนัก
- `display ap radio-environment`: ดู NF, CU(%), CommIf(%), AdjaceIf(%), SINR, จำนวน AP ต่อช่อง
- `display radio`: ดู channel ปัจจุบัน, power, bandwidth, channel utilization
สาเหตุที่พบบ่อย:
1. RRM ไม่เปิด channel selection (ต้อง `enable` ใน rrm-profile)
2. RRM ไม่เปิด calibration (ต้อง `enable` ใน rrm-profile)
3. Channel selection ไม่รันเป็นรอบ (ต้องตั้งค่า interval)
4. AP เลือก channel ที่ชนกับ AP อื่น (ต้องเปิด auto channel ใน rrm-profile)
5. Noise floor สูง (> -80 dBm) → เปลี่ยนไปช่องที่ noise ต่ำกว่า
6. Co-channel interference สูง → เปลี่ยน channel ที่ไม่ชน
7. Adjacent channel interference สูง → เปลี่ยน channel ที่ไม่ติดกัน
8. CU สูง (>60%) → ลดกำลังส่ง, เปลี่ยน channel
9. จำนวน AP ต่อ channel สูง → เปิด auto channel, ปรับ power
10. Channel bandwidth ไม่เหมาะสม (20/40/80 MHz) → ปรับให้เหมาะกับสภาพแวดล้อม
วิธีแก้:
- เปิด RRM channel selection: `rrm-profile <name>` → `enable` (channel selection)
- เปิด RRM calibration: `rrm-profile <name>` → `enable` (channel calibration)
- ปรับ interval: `channel-select interval <分钟>` (default 30 นาที)
- ปรับ power: `eirp <dBm>` ใน radio-2g-profile / radio-5g-profile
- ปรับ bandwidth: `channel <20mhz/40mhz/80mhz> <ch>` ใน radio-profile
ระวัง: เปลี่ยน channel จะตัดผู้ใช้ชั่วคราว — ทำในช่วง maintenance
ที่มา: Huawei WLAN Troubleshooting — RRM Configuration https://info.support.huawei.com/network/ptmngsys/Web/tsrev_wlan/en/content/wlan/20_edesk_rrm/edesk_rrm_edesk001.html

## Radio: กำลังส่ง (TX power) สูง / ต่ำเกิน / ไม่เหมาะสม
คำค้น: tx power, tx-power, power, eirp, กำลังส่ง, power control, radio profile, power profile, power adjustment, power calibration, radio power
อาการ: AP ส่งกำลังสูงเกินไป (interference), กำลังต่ำเกินไป (signal อ่อน), power ไม่เหมาะสม
คำสั่งตรวจ:
```
display rrm-profile all
display radio ap-id <ap-id>
display ap radio-ap-power-control all
display ap traffic statistics wireless ap-id <ap-id> radio <radio-id>
```
อ่านผล:
- `display rrm-profile all`: ดู power control profile — auto power ต้องเปิด (`enable`)
- `display radio`: ดู power ปัจจุบัน (TX power), EIRP
- `display ap radio-ap-power-control all`: ดู power control ของแต่ละ AP
สาเหตุที่พบบ่อย:
1. Power control ไม่เปิด (ต้อง `enable` ใน power control profile)
2. Power ไม่ auto (ต้องตั้งค่า auto power)
3. Power สูงเกิน (>20 dBm) → interference สูง
4. Power ต่ำเกินไป (<10 dBm) → signal อ่อน, user หลุด
5. Power ไม่ match กับ environment (indoors/outdoors)
6. Power calibration ไม่เปิด (ต้อง `enable` ใน rrm-profile)
7. EIRP สูงเกิน limit → ปรับ power, antenna
8. Power ไม่ match กับ channel bandwidth
9. Power ไม่ match กับ radio mode (802.11n/ac/ax)
10. Power ไม่ match กับ distance (AP กับ user)
วิธีแก้:
- เปิด power control: `power-control-profile <name>` → `enable`
- เปิด auto power: `power-control-profile <name>` → `auto power`
- ปรับ power: `eirp <dBm>` ใน radio-2g-profile / radio-5g-profile
- ปรับ calibration: `rrm-profile <name>` → `enable` (power calibration)
- ปรับ interval: `power-adjust interval <分钟>` (default 30 นาที)
ระวัง: เปลี่ยน power จะกระทบ signal strength และ user experience — ทำในช่วง maintenance
ที่มา: Huawei WLAN Troubleshooting — Power Control https://info.support.huawei.com/network/ptmngsys/Web/tsrev_wlan/en/content/wlan/20_edesk_rrm/edesk_rrm_edesk002.html

## Radio: Bandwidth ไม่เหมาะสม (20/40/80 MHz) / HT/VHT mode
คำค้น: bandwidth, 20mhz, 40mhz, 80mhz, ht20, ht40, vht20, vht40, vht80, channel bandwidth, bandwidth, bandwidth profile, bandwidth adjustment
อาการ: Bandwidth ไม่เหมาะสม (20/40/80 MHz), HT/VHT mode ไม่ตรง, ความเร็วต่ำ
คำสั่งตรวจ:
```
display rrm-profile all
display radio ap-id <ap-id>
display ap traffic statistics wireless ap-id <ap-id> radio <radio-id>
display station sta-mac <sta-mac>
```
อ่านผล:
- `display rrm-profile all`: ดู bandwidth profile — auto bandwidth ต้องเปิด (`enable`)
- `display radio`: ดู bandwidth ปัจจุบัน (HT20/HT40/VHT20/VHT40/VHT80)
- `display ap traffic statistics`: ดู bandwidth utilization
- `display station sta-mac`: ดู connect rate, bandwidth ที่ใช้
สาเหตุที่พบบ่อย:
1. Bandwidth ไม่เปิด auto (ต้อง `enable` ใน bandwidth profile)
2. Bandwidth สูงเกิน (>80 MHz) → interference สูง
3. Bandwidth ต่ำเกินไป (<20 MHz) → ความเร็วต่ำ
4. Bandwidth ไม่ match กับ channel utilization
5. Bandwidth ไม่ match กับ radio mode (802.11n/ac/ax)
6. Bandwidth ไม่ match กับ environment (indoors/outdoors)
7. Bandwidth ไม่ match กับ distance (AP กับ user)
8. Bandwidth ไม่ match กับ channel interference
9. Bandwidth ไม่ match กับ co-channel interference
10. Bandwidth ไม่ match dengan adjacent channel interference
วิธีแก้:
- เปิด bandwidth auto: `bandwidth-profile <name>` → `enable`
- ปรับ bandwidth: `channel <20mhz/40mhz/80mhz> <ch>` ใน radio-profile
- ปรับ interval: `bandwidth-adjust interval <分钟>` (default 30 นาที)
ระวัง: เปลี่ยน bandwidth จะตัดผู้ใช้ชั่วคราว — ทำในช่วง maintenance
ที่มา: Huawei WLAN Troubleshooting — Bandwidth Management https://info.support.huawei.com/network/ptmngsys/Web/tsrev_wlan/en/content/wlan/20_edesk_rrm/edesk_rrm_edesk003.html

## Roaming: 802.11k/v/r ไม่ทำงาน / roaming ช้า
คำค้น: roaming, 802.11k, 802.11v, 802.11r, fast roaming, smart roam, fast-roam, 802.11k/v/r, 802.11k not working, 802.11v not working, 802.11r not working
อาการ: Roaming ช้า, 802.11k/v/r ไม่ทำงาน, roaming ไม่เร็ว, roaming ไม่ smooth, roaming หลุดระหว่าง roam
คำสั่งตรวจ:
```
display rrm-profile all
display vap all
display station all
display station roaming statistics
display vap vap-profile <vap-profile>
```
อ่านผล:
- `display rrm-profile all`: ดู roaming profile — 802.11k/v/r ต้องเปิด (`enable`)
- `display vap all`: ดู VAP configuration — roaming profile ต้องถูก bind
- `display station all`: ดู roaming statistics — roaming success rate
- `display station roaming statistics`: ดู roaming statistics
- `display vap vap-profile`: ดู VAP profile — roaming profile ต้องถูก bind
สาเหตุที่พบบ่อย:
1. 802.11k ไม่เปิด (ต้อง `enable` ใน roaming profile)
2. 802.11v ไม่เปิด (ต้อง `enable` ใน roaming profile)
3. 802.11r ไม่เปิด (ต้อง `enable` ใน roaming profile)
4. Roaming profile ไม่ถูก bind กับ VAP
5. Roaming profile ถูก bind แต่ไม่ทำงาน (config ผิด)
6. Roaming success rate ต่ำ (<90%) → ตรวจ roaming profile, VAP
7. Roaming timeout สูง (>5 วินาที) → ตรวจ roaming profile
8. Roaming fail率高 (>10%) → ตรวจ roaming profile, VAP
9. Roaming ไม่ smooth → ตรวจ roaming profile, VAP
10. Roaming หลุดระหว่าง roam → ตรวจ roaming profile, VAP
วิธีแก้:
- เปิด 802.11k/v/r: `roaming-profile <name>` → `enable` (802.11k, 802.11v, 802.11r)
- Bind roaming profile กับ VAP: `vap-profile <vap-profile>` → `roaming-profile <name>`
- ปรับ roaming timeout: `roaming-profile <name>` → `roaming-timeout <ms>`
|- ปรับ roaming threshold: `roaming-profile <name>` → `roaming-threshold <dBm>`
ระวัง: เปลี่ยน roaming profile จะกระทบผู้ใช้ที่กำลัง roam — ทำในช่วง maintenance
ที่มา: Huawei WLAN Troubleshooting — 802.11k/v/r Fast Roaming https://info.support.huawei.com/network/ptmngsys/Web/tsrev_wlan/en/content/wlan/20_edesk_roaming/edesk_roaming_edesk001.html

## Roaming: 802.11k/v/r ทำงานแต่ user ยัง roaming ช้า
คำค้น: roaming ช้า, roaming slow, roaming ไม่เร็ว, roaming ไม่ smooth, roaming หลุด, roaming timeout, roaming fail, roaming success rate, roaming statistics
อาการ: Roaming ช้า, roaming ไม่เร็ว, roaming ไม่ smooth, roaming หลุด, roaming timeout, roaming fail, roaming success rate ต่ำ, roaming statistics ไม่ดี
คำสั่งตรวจ:
```
display rrm-profile all
display vap all
display station all
display station roaming statistics
display vap vap-profile <vap-profile>
display station sta-mac <sta-mac>
```
อ่านผล:
- `display rrm-profile all`: ดู roaming profile — 802.11k/v/r ต้องเปิด (`enable`)
- `display vap all`: ดู VAP configuration — roaming profile ต้องถูก bind
- `display station all`: ดู roaming statistics — roaming success rate
- `display station roaming statistics`: ดู roaming statistics
- `display station sta-mac`: ดู roaming statistics สำหรับ station ที่เฉพาะ
สาเหตุที่พบบ่อย:
1. Roaming timeout สูง (>5 วินาที) → ปรับ roaming timeout
2. Roaming threshold ต่ำ (< -80 dBm) → ปรับ roaming threshold
3. Roaming success rate ต่ำ (<90%) → ตรวจ roaming profile, VAP
4. Roaming fail率高 (>10%) → ตรวจ roaming profile, VAP
5. Roaming ไม่ smooth → ตรวจ roaming profile, VAP
6. Roaming หลุดระหว่าง roam → ตรวจ roaming profile, VAP
7. Roaming timeout สูง (>5 วินาที) → ตรวจ roaming profile, VAP
8. Roaming fail率高 (>10%) → ตรวจ roaming profile, VAP
9. Roaming ไม่ smooth → ตรวจ roaming profile, VAP
10. Roaming หลุดระหว่าง roam → ตรวจ roaming profile, VAP
วิธีแก้:
- ปรับ roaming timeout: `roaming-profile <name>` → `roaming-timeout <ms>`
- ปรับ roaming threshold: `roaming-profile <name>` → `roaming-threshold <dBm>`
|- เปิด 802.11k/v/r: `roaming-profile <name>` → `enable` (802.11k, 802.11v, 802.11r)
|- Bind roaming profile กับ VAP: `vap-profile <vap-profile>` → `roaming-profile <name>`
ระวัง: เปลี่ยน roaming profile จะกระทบผู้ใช้ที่กำลัง roam — ทำในช่วง maintenance
ที่มา: Huawei WLAN Troubleshooting — 802.11k/v/r Fast Roaming https://info.support.huawei.com/network/ptmngsys/Web/tsrev_wlan/en/content/wlan/20_edesk_roaming/edesk_roaming_edesk002.html
