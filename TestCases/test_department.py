import unittest
import requests
maKhoa =0
class ApiTest(unittest.TestCase):
    api_url = "http://localhost:8000/api"
    department_url="{}/departments".format(api_url)
    department_new_json={"MAKHOA":"TEST","TENKHOA": "Test Khoa","SODT": "000000000", "EMAIL": "test@test.com"}
    department_update_json = {"MAKHOA":"TEST","TENKHOA": "Test Khoa Updated", "SODT": "000000000", "EMAIL": "test@test.com Updated"}
    def _get_each_deparment_url(self):
        return "{}/departments/{}".format(self.api_url,"TEST")

    def test_1_get_all_department(self):
        r =requests.get(self.department_url)
        self.assertEqual(r.status_code,200)
        self.assertNotEqual(len(r.text),2)
    def test_2_add_new_department(self):
        r=requests.post(self.department_url,json=self.department_new_json)
        self.assertEqual(r.status_code,201)
    def test_3_get_new_department(self):
        r =requests.get(self._get_each_deparment_url())
        self.assertEqual(r.status_code,200)
        self.assertNotEqual(len(r.text),2)

    def test_4_update_department(self):
        r = requests.put(self._get_each_deparment_url(),json=self.department_update_json)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), self.department_update_json)


    def test_5_get_department_after_update(self):
        r = requests.get(self._get_each_deparment_url())
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), self.department_update_json)


    def test_6_delete_deparment(self):
        r=requests.delete(self._get_each_deparment_url())
        self.assertEqual(r.status_code,204)

    @unittest.expectedFailure
    def test_7_get_book_after_delete(self):
        r = requests.get(self._get_each_deparment_url())
        self.assertEqual(r.status_code, 200)