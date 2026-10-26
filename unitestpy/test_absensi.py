
import pytest
from unittest.mock import Mock

from absensi import (
    hitung_persentase,
    tentukan_status,
    catat_kehadiran
)


@pytest.fixture
def data_mahasiswa():
    data = {
        "23001": ["Hadir", "Hadir"],
        "23002": ["Hadir"]
    }

    yield data

    data.clear()


def test_hitung_persentase_normal():
    assert hitung_persentase(8, 10) == 80.0


def test_total_pertemuan_nol():
    with pytest.raises(ValueError):
        hitung_persentase(5, 0)


def test_jumlah_hadir_melebihi_total():
    with pytest.raises(ValueError):
        hitung_persentase(11, 10)


def test_jumlah_hadir_negatif():
    with pytest.raises(ValueError):
        hitung_persentase(-1, 10)


@pytest.mark.parametrize(
    "persentase, hasil",
    [
        (74, "Tidak Memenuhi"),
        (75, "Memenuhi"),
        (76, "Memenuhi")
    ]
)
def test_status_bva(persentase, hasil):
    assert tentukan_status(persentase) == hasil


def test_persentase_di_luar_batas():
    with pytest.raises(ValueError):
        tentukan_status(101)


def test_catat_kehadiran_berhasil(data_mahasiswa):
    notifier = Mock()

    jumlah = catat_kehadiran(
        data_mahasiswa, "23001", "Hadir", notifier
    )

    assert jumlah == 3
    assert data_mahasiswa["23001"][-1] == "Hadir"

    notifier.assert_called_once_with(
        "Absensi 23001 berhasil dicatat"
    )


def test_mahasiswa_tidak_ditemukan(data_mahasiswa):
    notifier = Mock()

    with pytest.raises(ValueError):
        catat_kehadiran(
            data_mahasiswa, "99999", "Hadir", notifier
        )


def test_status_kehadiran_tidak_valid(data_mahasiswa):
    notifier = Mock()

    with pytest.raises(ValueError):
        catat_kehadiran(
            data_mahasiswa, "23001", "Terlambat", notifier
        )


def test_catat_status_izin(data_mahasiswa):
    notifier = Mock()

    jumlah = catat_kehadiran(
        data_mahasiswa, "23002", "Izin", notifier
    )

    assert jumlah == 2
    notifier.assert_called_once()


def test_catat_status_sakit(data_mahasiswa):
    notifier = Mock()

    jumlah = catat_kehadiran(
        data_mahasiswa, "23002", "Sakit", notifier
    )

    assert jumlah == 2
    notifier.assert_called_once()


def test_catat_status_alpa(data_mahasiswa):
    notifier = Mock()

    jumlah = catat_kehadiran(
        data_mahasiswa, "23002", "Alpa", notifier
    )

    assert jumlah == 2
    notifier.assert_called_once()
