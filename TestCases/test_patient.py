import unittest
import requests

maKhoa = 0


class ApiTest(unittest.TestCase):
    api_url = "http://localhost:8000/api"
    employee_url = "{}/patients".format(api_url)
    patient_new_json = {
      "CMND": "241718850",
      "HOTEN": "string ho ten",
      "GIOITINH": "Nữ",
      "NGAYSINH": "2021-08-10",
      "DIACHI": "string dia chi",
      "DOITUONG": "string doi tuong",
      "BHYT": "string",
      "SODIENTHOAI": "string",
      "EMAIL": "string",
      "HINHANH": "string",
      "USERNAME": "string",
      "PASSWORD": "string"
    }
    patient_update_json = {
            "CMND": "241718850",
            "HOTEN": "string updated",
            "GIOITINH": "Nam",
            "NGAYSINH": "2021-08-09",
            "DIACHI": "string updated",
            "DOITUONG": "string updated",
            "BHYT": "string",
            "SODIENTHOAI": "string",
            "EMAIL": "string updated",
            "HINHANH": "string updated",
            "USERNAME": "string updated",
            "PASSWORD": "string updated"
        }

    def _get_each_patient_url(self):
        return "{}/patients/{}".format(self.api_url, "241718850")

    def test_1_get_all_patient(self):
        r = requests.get(self.employee_url)
        self.assertEqual(r.status_code, 200)

    def test_2_add_new_patient(self):
        r = requests.post(self.employee_url, json=self.patient_new_json)
        self.assertEqual(r.status_code, 201)

    def test_3_get_new_patient(self):
        r = requests.get(self._get_each_patient_url())
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(len(r.text), 2)

    def test_4_update_patient(self):
        r = requests.put(self._get_each_patient_url(), json=self.patient_update_json)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['CMND'], self.patient_update_json['CMND'])
        self.assertEqual(r.json()['HOTEN'], self.patient_update_json['HOTEN'])
        self.assertEqual(r.json()['GIOITINH'], self.patient_update_json['GIOITINH'])
        self.assertEqual(r.json()['NGAYSINH'], self.patient_update_json['NGAYSINH'])
        self.assertEqual(r.json()['DIACHI'], self.patient_update_json['DIACHI'])
        self.assertEqual(r.json()['DOITUONG'], self.patient_update_json['DOITUONG'])
        self.assertEqual(r.json()['SODIENTHOAI'], self.patient_update_json['SODIENTHOAI'])
        self.assertEqual(r.json()['CMND'], self.patient_update_json['CMND'])
        self.assertEqual(r.json()['EMAIL'], self.patient_update_json['EMAIL'])
        self.assertEqual(r.json()['HINHANH'], self.patient_update_json['HINHANH'])
        self.assertEqual(r.json()['BHYT'], self.patient_update_json['BHYT'])
    def test_5_get_patient_after_update(self):
        r = requests.get(self._get_each_patient_url())
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['CMND'], self.patient_update_json['CMND'])
        self.assertEqual(r.json()['HOTEN'], self.patient_update_json['HOTEN'])
        self.assertEqual(r.json()['GIOITINH'], self.patient_update_json['GIOITINH'])
        self.assertEqual(r.json()['NGAYSINH'], self.patient_update_json['NGAYSINH'])
        self.assertEqual(r.json()['DIACHI'], self.patient_update_json['DIACHI'])
        self.assertEqual(r.json()['DOITUONG'], self.patient_update_json['DOITUONG'])
        self.assertEqual(r.json()['SODIENTHOAI'], self.patient_update_json['SODIENTHOAI'])
        self.assertEqual(r.json()['CMND'], self.patient_update_json['CMND'])
        self.assertEqual(r.json()['EMAIL'], self.patient_update_json['EMAIL'])
        self.assertEqual(r.json()['HINHANH'], self.patient_update_json['HINHANH'])
        self.assertEqual(r.json()['BHYT'], self.patient_update_json['BHYT'])
#(CMND, HOTEN, GIOITINH, NGAYSINH, DIACHI, DOITUONG, BHYT,SODIENTHOAI, EMAIL, HINHANH )
    def test_6_delete_patient(self):
        r = requests.delete(self._get_each_patient_url())
        self.assertEqual(r.status_code, 204)

    @unittest.expectedFailure
    def test_7_get_book_after_delete(self):
        r = requests.get(self._get_each_patient_url())
        self.assertEqual(r.status_code, 200)
