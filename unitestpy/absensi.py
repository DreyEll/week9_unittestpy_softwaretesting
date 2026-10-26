
def hitung_persentase(hadir, total_pertemuan):
    if total_pertemuan <= 0:
        raise ValueError("Total pertemuan harus lebih dari 0")

    if hadir < 0 or hadir > total_pertemuan:
        raise ValueError("Jumlah hadir tidak valid")

    return (hadir / total_pertemuan) * 100


def tentukan_status(persentase):
    if persentase < 0 or persentase > 100:
        raise ValueError("Persentase harus antara 0 dan 100")

    if persentase >= 75:
        return "Memenuhi"
    else:
        return "Tidak Memenuhi"


def catat_kehadiran(data, nim, status, notifier):
    if nim not in data:
        raise ValueError("Mahasiswa tidak ditemukan")

    if status not in ["Hadir", "Izin", "Sakit", "Alpa"]:
        raise ValueError("Status kehadiran tidak valid")

    data[nim].append(status)
    notifier(f"Absensi {nim} berhasil dicatat")

    return len(data[nim])
