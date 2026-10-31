# คู่มือสำหรับ Hermes: เขียนความรู้ (Playbook) ให้ AI ในโปรแกรม NetPED+

## เป้าหมาย
NetPED+ มี AI ในเครื่อง (Ollama โมเดลเล็ก ใช้ออฟไลน์ใน IDC) ช่วยไล่ปัญหาอุปกรณ์ network
AI ตอบได้แม่นเฉพาะเรื่องที่มีอยู่ใน **playbook** (ไฟล์ `.md`) ซึ่งโปรแกรมค้นจากบรรทัด `คำค้น:` แล้วส่งให้ AI ทีละ ≤ 3 หัวข้อ
งานของคุณ: ค้นข้อมูลจากเอกสารผู้ผลิต แล้วเขียนเป็น playbook ตามรูปแบบด้านล่าง **ทุกคำสั่งต้องมีแหล่งอ้างอิงจริง**

> ห้ามแก้ `runbooks.yaml` — ไฟล์นั้นเป็นชุดคำสั่งที่โปรแกรมรันกับอุปกรณ์ (ต้องเซ็นลายเซ็น) AI ไม่ได้อ่านเป็นความรู้

---

## 1. ที่วางไฟล์
- Mac: `~/NetPEDPlus/playbooks/`
- Windows: `%LOCALAPPDATA%\Programs\NetPEDPlus\playbooks\`
- ชื่อไฟล์: ตัวเล็ก ใช้ `-` เช่น `huawei-s5731-poe.md` (ห้ามขึ้นต้นด้วย `_` เพราะโปรแกรมจะข้าม)
- **ห้ามใช้ชื่อหรือ id ซ้ำกับ playbook ที่มากับโปรแกรม** (รายการในข้อ 6) ถ้าจะเพิ่มเรื่องของยี่ห้อเดิม ให้ทำไฟล์ใหม่ เช่น `fortigate-7.4-extra.md` / id `fortigate-74-extra`

## 2. หัวไฟล์ (บังคับ)
```
---
id: huawei-s5731-poe
title: Huawei S5731 / S5735 (VRP V200R021+) PoE และพลังงาน
families: huawei_vrp_s
models: S5731, S5735
triggers: huawei, s5731, s5735, poe
vendor: Huawei
versions: V200R021C00, V200R022C00
sources: Huawei S300, S500, S2700, S5700, and S6700 V200R022C00 Configuration Guide - Device Management (PoE); info.support.huawei.com tsrev_s
---
# หัวเรื่องของไฟล์ (บรรทัดเดียว)
```
- `families` = ชื่อ family ในโปรแกรม (ตารางข้อ 5) ใช้เมื่อเคสผูกอุปกรณ์ไว้
- `triggers` = คำที่ถ้าอยู่ในคำถาม/เคส จะหยิบ playbook นี้ (ชื่อยี่ห้อ / รุ่น / ชื่อระบบ) **ต้องมีเสมอ** — เคสส่วนใหญ่พิมพ์ถามโดยไม่ผูกอุปกรณ์
- ระบบที่ไม่ใช่อุปกรณ์ใน catalog (เช่น QRadar, Windows, NCE) ให้เว้น `families` ว่าง แล้วใช้ `triggers` + `vendor`
- `versions` / `sources` ต้องเป็นของจริงที่ใช้ตรวจ

## 3. รูปแบบแต่ละหัวข้อ
```
## PoE ไม่จ่ายไฟให้ AP (อาการ / เรื่อง)
คำค้น: poe, ไม่จ่ายไฟ, ap ไม่ติด, power over ethernet, poe budget, poe max-power
อาการ: ...
คำสั่งตรวจ:
```
display poe power-state interface <interface>
display poe information
```
อ่านผล:
- ค่าที่ปกติ / ผิดปกติ หมายถึงอะไร (ใส่ตัวเลขเกณฑ์ถ้าเอกสารมี)
สาเหตุที่พบบ่อย:
1. ...
วิธีแก้:
- ...
ระวัง: ผลกระทบของคำสั่งที่เปลี่ยน config
ที่มา: <ชื่อบทความ/หัวข้อในคู่มือ> <URL ของผู้ผลิต>
```

กฎของหัวข้อ
1. ขึ้นต้นด้วย `## ` ชื่อหัวข้อเป็นอาการหรือเรื่อง **ห้ามมี " — " (em dash)** ในชื่อ
2. **`คำค้น:`** บรรทัดเดียว คั่นด้วย `,` ใส่ทั้งคำไทยที่คนพิมพ์จริง ("เน็ตหลุด", "ช้า") และคำอังกฤษ / ข้อความ error / ชื่อคำสั่ง — นี่คือสิ่งที่ทำให้ AI หาเจอ
3. **`ที่มา:`** ทุกหัวข้อ ชื่อบทความ + URL ของผู้ผลิต (ถ้า flow หลายหน้า ใส่หน้าแรก + "ขั้นถัดไปกด Next ในหน้า")
4. ยาว **ไม่เกิน ~2,500 ตัวอักษร** ต่อหัวข้อ ยาวกว่านั้นให้แยกหัวข้อ (เช่น พอร์ตทองแดง / พอร์ตแสง)
5. ค่าที่ต้องแทนเขียนใน `< >` เช่น `<interface>`, `<vlan-id>`
6. บล็อก "คำสั่งตรวจ" ใส่ **เฉพาะคำสั่งอ่านอย่างเดียว** (display / show / get / diagnose ที่ไม่เปลี่ยนค่า) คำสั่งที่เปลี่ยน config ให้อยู่ใน "วิธีแก้" พร้อม "ระวัง:"
7. คำสั่งที่มีรหัสผ่านในบรรทัด (เช่น `test-aaa`) ห้ามอยู่ในบล็อกคำสั่งตรวจ
8. ภาษาไทย ศัพท์เทคนิคเป็นอังกฤษได้ ไม่ต้องเกริ่นยาว

## 4. กฎแหล่งอ้างอิง (สำคัญที่สุด)
- **ทุกคำสั่งต้องเจอในเอกสารผู้ผลิตของเวอร์ชันนั้น** ห้ามเขียนจากความจำ ห้ามเดา syntax ห้ามแต่งชื่อคู่มือ
- **หลักฐานต่อคำสั่ง**: ใน PR ต้องแนบ (1) ลิงก์หน้าของคำสั่งนั้น (2) บรรทัด syntax ที่คัดลอกจากเอกสารตรงๆ — ไม่มีทั้งสองอย่าง = ลบคำสั่งนั้น
- ตัวเลข (ค่าเริ่มต้น, ช่วงค่า, เกณฑ์, "แนะนำ") ใส่ได้เฉพาะที่คัดลอกจากเอกสาร พร้อมลิงก์
- อ่าน `LESSONS.md` ก่อนเริ่มงาน และหลังแก้ไฟล์ต้องยืนยันด้วย `git diff --stat` ก่อนรายงาน
- ไม่เจอเอกสารยืนยัน = **ไม่ต้องใส่** ดีกว่าใส่ผิด (เคยมี AI แต่งคำสั่ง tmsh ของ F5 ที่ไม่มีจริง)
- แหล่งบุคคลที่สาม (blog, forum) ใช้ได้เฉพาะเมื่อไม่มีของผู้ผลิต และต้องเขียนกำกับในหัวข้อว่า "(แหล่งบุคคลที่สาม)"
- แหล่งที่ดึงได้ / ไม่ได้ (จากประสบการณ์):

| ผู้ผลิต | ใช้ได้ | ดึงไม่ได้ / ระวัง |
|---|---|---|
| Huawei | info.support.huawei.com (tsrev_s, tsrev_wlan, WLAN troubleshooting) | support.huawei.com/enterprise, hedex (ต้องล็อกอิน/JS) — หน้า index ของ tsrev โหลดด้วย JS ต้องหา URL หัวข้อผ่านการค้นหา |
| F5 | techdocs.f5.com, clouddocs.f5.com | my.f5.com (K article) เป็นหน้า JS — ต้องเปิดผ่านเบราว์เซอร์ |
| Fortinet | docs.fortinet.com, community.fortinet.com (Technical Tip) | |
| Palo Alto | docs.paloaltonetworks.com, knowledgebase.paloaltonetworks.com | |
| Sophos | docs.sophos.com, support.sophos.com | |
| IBM QRadar | ibm.com/docs | ibm.com/support/pages ต้องล็อกอิน |
| Microsoft | learn.microsoft.com (troubleshoot) | |
| Kaspersky | support.kaspersky.com (บางหน้า) | |

## 5. ชื่อ family ในโปรแกรม (ใช้ใน `families:`)
arista_eos, aruba_aos8, aruba_aos_switch, aruba_aoscx, checkpoint_gaia, cisco_asa, cisco_ios, cisco_nxos, cisco_sb, dell_os10, extreme_exos, f5_tmsh, fortinet_fortios, hpe_comware (H3C ด้วย), huawei_ac, huawei_ce, huawei_vrp_s, juniper_junos, juniper_srx, linux, mikrotik_ros7, paloalto_panos, ruckus_fastiron, ruijie_rgos, sonicwall_sonicos, sophos_sfos, tplink_jetstream

## 6. Playbook ที่มีอยู่แล้ว (อย่าเขียนซ้ำ เขียนเรื่องที่ยังไม่มี)
f5-bigip-17, f5-ltm-asm-build, f5-ops-advanced, fortigate-7.4, huawei-ac-wlan, huawei-vrp-switch, imaster-nce-campus, kaspersky-scan-engine, paloalto-panos, qradar-7.5, routing-concepts, sophos-sfos-21, windows-ad-dhcp-dns
**ก่อนเลือกเรื่องต้องเปิด `EXISTING_TOPICS.md` (หัวข้อทั้งหมดที่โปรแกรมมีแล้ว) — ซ้ำ = PR ถูกปิด** (PR #4 / #5 ถูกปิดเพราะซ้ำ)

## 7. ห้ามเด็ดขาด
- ข้อมูลลูกค้า: IP, hostname, config, SNMP community, ชื่อหน่วยงาน, รหัสผ่าน — ตัวอย่างใช้ค่าสมมติ (`10.0.0.1`, `SW-CORE`, `<community>`)
- คัดลอกบทความผู้ผลิตยาวๆ ทั้งก้อน — สรุปเป็นขั้นตอนด้วยคำของตัวเอง ใส่ลิงก์แทน
- คำแนะนำที่ทำให้ระบบล่ม (reboot, reset, delete) โดยไม่มีบรรทัด "ระวัง:"

## 8. ส่งงาน
ต่อไฟล์ ให้รายงาน:
1. ชื่อไฟล์ + จำนวนหัวข้อ
2. ตาราง: หัวข้อ → คำสั่งที่ใช้ → URL ที่ยืนยันคำสั่งนั้น (เพื่อให้ตรวจซ้ำได้)
3. คำสั่งที่หาเอกสารยืนยันไม่ได้ (ตัดออกแล้ว) — แยกไว้ให้ดู
4. ตัวอย่างคำถาม 2–3 ข้อต่อหัวข้อ ที่ควรได้หัวข้อนี้ (ใช้ทดสอบใน NetPED+)

## 9. ตรวจก่อนส่ง (checklist)
`tools/check_playbook.py` ขึ้น ERROR อัตโนมัติเมื่อ: ไม่มีบล็อก คำสั่งตรวจ / มีบล็อกโค้ดอื่นนอกจาก คำสั่งตรวจ / มี 'ตัวอย่าง output' / มีอักษรจีน-ญี่ปุ่น / มี `commit` ใน playbook Huawei S series (huawei_vrp_s)
- [ ] หัวไฟล์มี id / title / triggers / versions / sources
- [ ] ทุก `## ` มี `คำค้น:` และ `ที่มา:` + URL
- [ ] ไม่มี " — " ในชื่อหัวข้อ
- [ ] ทุกหัวข้อ ≤ ~2,500 ตัวอักษร
- [ ] บล็อกคำสั่งตรวจเป็นอ่านอย่างเดียวทั้งหมด
- [ ] ไม่มี IP / ชื่อเครื่อง / ข้อมูลลูกค้าจริง
- [ ] ไม่ซ้ำหัวข้อใน playbook ที่มีอยู่แล้ว
