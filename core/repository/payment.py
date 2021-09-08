import pytz as pytz
from sqlalchemy.orm import Session
from core.model.models import MedicalRecordModel,DetailArrangeRoomBedModel,DetailServiceModel,AdvancesModel,ServiceModel
from core.model.models import BedModel,RoomModel,DetailRoomBedModel,MedicineModel,ReceiptModel
from ..schema import schemas
from ..utility import dateconverter
from fastapi import  status, HTTPException
def caculator_room_fee(NGAYTRA,NGAYTHUE):
    total_day = 1
    ngaythue = "{:%m/%d/%Y}".format(NGAYTHUE)
    ngaytra = "{:%m/%d/%Y}".format(NGAYTRA)
    if (ngaytra != ngaythue):
        ngaytra_obj = datetime.strptime(ngaytra, '%m/%d/%Y')
        ngaythue_obj = datetime.strptime(ngaythue, '%m/%d/%Y')
        total_day = ((ngaytra_obj - ngaythue_obj)).days

    return total_day

#def caculator_services(services):

def count_service(services,detailservices):
    service_dict = {}
    for service in services:
        count = 0
        for detailservice in detailservices:
            if service.MADV == detailservice.MADV:
                count += 1
        service_dict[service.MADV] = count
    return service_dict


def isBorrow(ID,detail_room_bed):
    for i in detail_room_bed:
        if i.CTPHONGGIUONG_ID==ID and i.TRANGTHAI==True:
            return i
    return None

def get_number_room(room,detail):
    for i in room:
        if i.MAPHONG == detail.MAPHONG:
            return i.SOPHONG

def get_number_bed(bed,detail):
    for i in bed:
        if i.MAGIUONG== detail.MAGIUONG:
            return i.SOGIUONG

def get_borrow_bed(MABA,db):
    query ='select "DONGIA","NGAYTHUE","NGAYTRA" from "CHITIETXEPGIUONG" where "MABA"=\'' + MABA + '\''
    result = db.execute(query)
    rooms=[]
    for r in result:
        r_dict = dict(r.items())  # convert to dict keyed by column names
        total_day = caculator_room_fee(r_dict["NGAYTRA"], r_dict["NGAYTHUE"])
        date_checkin = round(dateconverter.convertDateTimeToLong(str(r_dict["NGAYTHUE"])), 0)
        date_checkout = round(dateconverter.convertDateTimeToLong(str(r_dict["NGAYTRA"])), 0)
        room = {"price": r_dict["DONGIA"], "date_checkin": date_checkin, "date_checkout": date_checkout,
                "total_day": total_day}
        rooms.append(room)



    return rooms


def get_all_services(services_raw,detailservices,service_dict):
    services=[]
    quantity=0
    if len(service_dict)>0:
        for service_raw in services_raw:
            for detailservice in detailservices:
                if service_raw.MADV==detailservice.MADV:
                    price=detailservice.DONGIA
                    quantity=service_dict[service_raw.MADV]
                    day= round(dateconverter.convertDateTimeToLong(str(detailservice.NGAY)),0)
                    break
            if quantity>0:
                service = {"name": service_raw.TENDV, "quantity": quantity, "price": price,"day":day}
                services.append(service)
                price=0
                day=0
                quantity=0
    return services

def get_name_medicine(MATHUOC, medicines):
    for medicine in medicines:
        if MATHUOC==medicine.MATHUOC:
            return medicine.TENTHUOC
def get_all_medicine(medicine_raws,db,MABA):
    medicines=[]
    query = 'select SUM("SOLUONG") as "SOLUONG" ,"MATHUOC", "DONGIA" from public."CHITIETTOATHUOC" as CT '+\
            'where "MATOA" in (select "MATOA" from "TOATHUOC" where "CTKHAM_ID" in (select "CTKHAM_ID" ' +\
            'from "CHITIETKHAM" where "MABA"=\''+MABA+'\' )) group by "MATHUOC","DONGIA"'
    print(query)
    result = db.execute(query)
    for r in result:
        r_dict = dict(r.items())  # convert to dict keyed by column names
        name = get_name_medicine(r_dict['MATHUOC'],medicine_raws)
        medicine={"name":name,"price":r_dict["DONGIA"],"quantity":r_dict["SOLUONG"]}
        medicines.append(medicine)
    return medicines
def get_hospital_fee(MABA,db:Session):
    total_advances = 0

    detailservices = db.query(DetailServiceModel).filter(DetailServiceModel.MABA==MABA).all()
    advances = db.query(AdvancesModel).filter(AdvancesModel.MABA==MABA).all()
    services_raw = db.query(ServiceModel).all()
    medicines=db.query(MedicineModel).all()
    receipt= db.query(ReceiptModel).filter(ReceiptModel.MABA==MABA).all()
    if not detailservices and not advances and not services_raw  and not medicines:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không có dữ liệu")
    #thong ke thue phong
    rooms=get_borrow_bed(MABA,db)

    #tinh tong tien tam ung
    for advance in advances:
        total_advances=total_advances+advance.SOTIEN

    #thong ke dich vu
    service_dict=count_service(services_raw,detailservices)
    services=get_all_services(services_raw,detailservices,service_dict)

    #Tinh thuoc
    medicines=get_all_medicine(medicines, db, MABA)
    if not receipt:
        sta=0
    else:
        sta=1
    return {"medical_record":MABA,"status":sta,"advances":total_advances,"rooms":rooms,"services":services,"medicines":medicines}
import random
from datetime import datetime

now  = datetime.now(tz=pytz.timezone('Asia/Bangkok'))
def create_receiptment(request: schemas.ReceiptModel,db):
    id_list=[]
    result = db.execute('select "MAHD" from "HOADON"')
    for r in result:
        r_dict = dict(r.items())  # convert to dict keyed by column names
        r_value= r_dict["MAHD"]
        pr, id = r_value.split('-')
        id_list.append(int(id))
    if len(id_list) >0:
        max_value =max(id_list)
        max_value+=1
        MAHD = 'HD-' + str(max_value)
    else:
        MAHD = 'HD-1'
    new_rep = ReceiptModel(MAHD=MAHD, NGAYLAP=now, TONGTIEN=request.TONGTIEN, GHICHU=request.GHICHU,
                           MANV='NV-10101010', MABA=request.MABA, TIENTHUOC=request.TIENTHUOC, TIENDICHVU=request.TIENDICHVU,
                           TIENGIUONG=request.TIENGIUONG, TONGTAMUNG=request.TONGTAMUNG, THUCTRA=request.THUCTRA)
    db.add(new_rep)
    db.commit()
    db.refresh(new_rep)
    return new_rep









