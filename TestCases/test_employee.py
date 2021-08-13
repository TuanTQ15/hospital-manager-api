import unittest
import requests

maKhoa = 0


class ApiTest(unittest.TestCase):
    api_url = "http://localhost:8000/api"
    employee_url = "{}/employees".format(api_url)
    employee_new_json = {
        "MANV": "NVTEST",
        "MAKHOA": "NTLAMSANG",
        "HOTEN": "string",
        "GIOITINH": "Nam",
        "DIACHI": "string",
        "CMND": "9321754",
        "NGAYSINH": "2021-08-10",
        "HINHANH": "string",
        "CHUCVU": "string",
        "SODIENTHOAI": "0969261026",
        "EMAIL": "string",
        "MALOAINV": "BS",
        "USERNAME": "string",
        "PASSWORD": "string"
    }
    employee_update_json = {
        "MANV": "NVTEST",
        "MAKHOA": "NTLAMSANG",
        "HOTEN": "string updated",
        "GIOITINH": "Nam",
        "DIACHI": "string updated",
        "CMND": "93217587",
        "NGAYSINH": "2021-08-10",
        "HINHANH": "string updated",
        "CHUCVU": "string updated",
        "SODIENTHOAI": "0969261026",
        "EMAIL": "string updated",
        "MALOAINV": "YT",
        "USERNAME": "string",
        "PASSWORD": "stringupdated"
    }

    def _get_each_employee_url(self):
        return "{}/employees/{}".format(self.api_url, "NVTEST")

    def test_1_get_all_employee(self):
        r = requests.get(self.employee_url)
        self.assertEqual(r.status_code, 200)

    def test_2_add_new_employee(self):
        r = requests.post(self.employee_url, json=self.employee_new_json)
        self.assertEqual(r.status_code, 201)

    def test_3_get_new_employee(self):
        r = requests.get(self._get_each_employee_url())
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(len(r.text), 2)

    def test_4_update_employee(self):
        r = requests.put(self._get_each_employee_url(), json=self.employee_update_json)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['MANV'], self.employee_update_json['MANV'])
        self.assertEqual(r.json()['GIOITINH'], self.employee_update_json['GIOITINH'])
        self.assertEqual(r.json()['NGAYSINH'], self.employee_update_json['NGAYSINH'])
        self.assertEqual(r.json()['DIACHI'], self.employee_update_json['DIACHI'])
        self.assertEqual(r.json()['CHUCVU'], self.employee_update_json['CHUCVU'])
        self.assertEqual(r.json()['SODIENTHOAI'], self.employee_update_json['SODIENTHOAI'])
        self.assertEqual(r.json()['CMND'], self.employee_update_json['CMND'])
        self.assertEqual(r.json()['EMAIL'], self.employee_update_json['EMAIL'])
        self.assertEqual(r.json()['HINHANH'], self.employee_update_json['HINHANH'])
        self.assertEqual(r.json()['MALOAINV'], self.employee_update_json['MALOAINV'])
        self.assertEqual(r.json()['MAKHOA'], self.employee_update_json['MAKHOA'])

    def test_5_get_employee_after_update(self):
        r = requests.get(self._get_each_employee_url())
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['MANV'], self.employee_update_json['MANV'])
        self.assertEqual(r.json()['HOTEN'], self.employee_update_json['HOTEN'])
        self.assertEqual(r.json()['GIOITINH'], self.employee_update_json['GIOITINH'])
        self.assertEqual(r.json()['NGAYSINH'], self.employee_update_json['NGAYSINH'])
        self.assertEqual(r.json()['DIACHI'], self.employee_update_json['DIACHI'])
        self.assertEqual(r.json()['CHUCVU'], self.employee_update_json['CHUCVU'])
        self.assertEqual(r.json()['SODIENTHOAI'], self.employee_update_json['SODIENTHOAI'])
        self.assertEqual(r.json()['CMND'], self.employee_update_json['CMND'])
        self.assertEqual(r.json()['EMAIL'], self.employee_update_json['EMAIL'])
        self.assertEqual(r.json()['HINHANH'], self.employee_update_json['HINHANH'])
        self.assertEqual(r.json()['MALOAINV'], self.employee_update_json['MALOAINV'])
        self.assertEqual(r.json()['MAKHOA'], self.employee_update_json['MAKHOA'])

    def test_6_delete_employee(self):
        r = requests.delete(self._get_each_employee_url())
        self.assertEqual(r.status_code, 204)

    @unittest.expectedFailure
    def test_7_get_book_after_delete(self):
        r = requests.get(self._get_each_employee_url())
        self.assertEqual(r.status_code, 200)
