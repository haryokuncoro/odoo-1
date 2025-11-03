### Custom module Odoo 19 untuk menambah fitur di **Sale Order** dan **Purchase Order**

---

## Fitur

### Sale Order

* **Request Vendor** → pilih vendor untuk PO.
* **No Kontrak** → unik, dicek saat Confirm SO.
* **With PO** → centang agar tombol **Create PO** muncul.
* **Purchase Orders** → link ke PO yang dibuat dari SO.

### Tombol Create PO

* Membuat PO otomatis dari SO.
* Vendor → Request Vendor, Reference → SO Name.
* PO Lines → dibuat dari SO Lines.

### Validasi No Kontrak

* Saat Confirm SO, jika No Kontrak sudah dipakai → muncul error.

### Import SO Lines

* Upload file Excel untuk menambahkan SO Lines.
* Format: `Product Code | Quantity | Unit Price`.

### Download Template

* Download file Excel template untuk import SO Lines.

---

## Dependensi

* Python library: `openpyxl`

```bash
pip install openpyxl
```

---

## Cara Tes

1. Install modul `custom_haryo`.
2. Centang **With PO**, isi **Request Vendor**, klik **Create PO**.
3. Confirm SO dengan No Kontrak sama → cek validasi muncul.
4. Gunakan tombol **Import SO Lines** dan **Download Template**.

---
