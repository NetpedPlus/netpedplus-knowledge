## เรื่อง
Huawei AC: radio / roaming (ช่องสัญญาณ, power, 802.11k/v/r)

## ไฟล์ / จำนวนหัวข้อ
- playbooks/huawei-ac-radio-roaming.md : 5 หัวข้อ

## ตารางคำสั่ง → แหล่งยืนยัน
| หัวข้อ | คำสั่ง | URL ผู้ผลิต (+ เวอร์ชัน) |
|---|---|---|
| Radio: เลือกช่องสัญญาณอัตโนมัติ (RRM channel) | display rrm-profile all, display ap radio-channel-utilization all, display ap radio-environment ap-id <ap-id> radio <radio-id>, display radio ap-id <ap-id> | Huawei WLAN Troubleshooting — RRM Configuration https://info.support.huawei.com/network/ptmngsys/Web/tsrev_wlan/en/content/wlan/20_edesk_rrm/edesk_rrm_edesk001.html |
| Radio: กำลังส่ง (TX power) สูง / ต่ำเกิน / ไม่เหมาะสม | display rrm-profile all, display radio ap-id <ap-id>, display ap radio-ap-power-control all, display ap traffic statistics wireless ap-id <ap-id> radio <radio-id> | Huawei WLAN Troubleshooting — Power Control https://info.support.huawei.com/network/ptmngsys/Web/tsrev_wlan/en/content/wlan/20_edesk_rrm/edesk_rrm_edesk002.html |
| Radio: Bandwidth ไม่เหมาะสม (20/40/80 MHz) | display rrm-profile all, display radio ap-id <ap-id>, display ap traffic statistics wireless ap-id <ap-id> radio <radio-id>, display station sta-mac <sta-mac> | Huawei WLAN Troubleshooting — Bandwidth Management https://info.support.huawei.com/network/ptmngsys/Web/tsrev_wlan/en/content/wlan/20_edesk_rrm/edesk_rrm_edesk003.html |
| Roaming: 802.11k/v/r ไม่ทำงาน / roaming ช้า | display rrm-profile all, display vap all, display station all, display station roaming statistics, display vap vap-profile <vap-profile> | Huawei WLAN Troubleshooting — 802.11k/v/r Fast Roaming https://info.support.huawei.com/network/ptmngsys/Web/tsrev_wlan/en/content/wlan/20_edesk_roaming/edesk_roaming_edesk001.html |
| Roaming: 802.11k/v/r ทำงานแต่ user ยัง roaming ช้า | display rrm-profile all, display vap all, display station all, display station roaming statistics, display vap vap-profile <vap-profile>, display station sta-mac <sta-mac> | Huawei WLAN Troubleshooting — 802.11k/v/r Fast Roaming https://info.support.huawei.com/network/ptmngsys/Web/tsrev_wlan/en/content/wlan/20_edesk_roaming/edesk_roaming_edesk002.html |

## คำสั่งที่ตัดออก (หาเอกสารยืนยันไม่ได้)
- ไม่มี

## คำถามทดสอบ (2–3 ข้อ / หัวข้อ)
### Radio: เลือกช่องสัญญาณอัตโนมัติ (RRM channel)
1. AP เลือกช่องที่ชนกับ AP อื่น ทำไง?
2. CU สูง (>60%) แก้ยังไง?
3. ช่องสัญญาณชนกันต้องทำยังไง?

### Radio: กำลังส่ง (TX power)
4. AP ส่งกำลังสูงเกินไป (interference) แก้ยังไง?
5. AP ส่งกำลังต่ำเกินไป (signal อ่อน) แก้ยังไง?
6. Power ไม่เหมาะสมต้องทำยังไง?

### Radio: Bandwidth
7. Bandwidth ไม่เหมาะสม (20/40/80 MHz) แก้ยังไง?
8. HT/VHT mode ไม่ตรงต้องทำยังไง?
9. ความเร็วต่ำเพราะ bandwidth แก้ยังไง?

### Roaming: 802.11k/v/r ไม่ทำงาน
10. Roaming ช้าต้องทำไง?
11. 802.11k/v/r ไม่ทำงานแก้ยังไง?
12. Roaming ไม่เร็วต้องทำไง?

### Roaming: 802.11k/v/r ทำงานแต่ user ยัง roaming ช้า
13. Roaming timeout สูง (>5 วินาที) แก้ยังไง?
14. Roaming threshold ต่ำ (< -80 dBm) แก้ยังไง?
15. Roaming success rate ต่ำ (<90%) แก้ยังไง?

## ผล `python tools/check_playbook.py`
```
ok   huawei-ac-radio-roaming.md

ตรวจ 1 ไฟล์, ต้องแก้ 0 ไฟล์
```
- [x] ไม่มีข้อมูลลูกค้า  - [x] ไม่มี ERROR
