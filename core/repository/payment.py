from sqlalchemy.orm import Session
from core.model.models import MedicalRecordModel,DetailArrangeRoomBedModel,DetailServiceModel,AdvancesModel,MedicalHistory,ServiceModel
from core.model.models import BedModel,RoomModel,DetailRoomBedModel,MedicineModel,DetailPrescriptionModel,PrescriptionModel
from datetime import datetime
from ..utility import dateconverter
from ..model.database import get_engine
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

def get_borrow_bed(roombeds,detail_room_bed,bed,room):
    for room_bed in roombeds:
        detail =isBorrow(room_bed.CTPHONGGIUONG_ID, detail_room_bed)

    if not detail:
        return {}
    else:
        number_room=get_number_room(room, detail)
        number_bed=get_number_bed(bed,detail)
        total_day = caculator_room_fee(room_bed.NGAYTRA, room_bed.NGAYTHUE)
        total_room_fee=total_day*room_bed.DONGIA
        date_checkin=round(dateconverter.convertDateTimeToLong(str(room_bed.NGAYTHUE)), 0)
        date_checkout=round(dateconverter.convertDateTimeToLong(str(room_bed.NGAYTRA)), 0)
        room = {"number_room": number_room, "number_bed": number_bed, "price": room_bed.DONGIA,"date_checkin":date_checkin, "date_checkout":date_checkout, "total_day": total_day, "total_room_fee":total_room_fee}
        return room


def get_all_services(services_raw,detailservices,service_dict):
    services=[]
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
def get_all_medicine(medicine_raws,db,CMND):
    r_dict = {}
    medicines=[]
    query = 'select SUM("SOLUONG") as "SOLUONG" ,"MATHUOC", "DONGIA" from public."CHITIETTOATHUOC" as CT ' + ' where "MATOA" in (select "MATOA" from "TOATHUOC" where "CTKHAM_ID" in' \
            + ' (select "CTKHAM_ID" from "CHITIETKHAM" where "MABA" = (select "MABA" from "BENHAN" where "CMND"=\'' + CMND + '\' and "NGAYLAP"= ' \
            + ' ( SELECT  MAX( "NGAYLAP")FROM "BENHAN" where "CMND"=\'' + CMND + '\')))) group by "MATHUOC", "DONGIA" '
    print(query)
    result = db.execute(query)
    for r in result:
        r_dict = dict(r.items())  # convert to dict keyed by column names
        name = get_name_medicine(r_dict['MATHUOC'],medicine_raws)
        medicine={"name":name,"price":r_dict["DONGIA"],"quantity":r_dict["SOLUONG"]}
        medicines.append(medicine)
    return medicines
def get_hospital_fee(CMND,db:Session):
    total_advances = 0
    medicalRecords = db.query(MedicalRecordModel).filter(MedicalRecordModel.CMND==CMND).all()
    medicalRecords = sorted(medicalRecords, key=lambda i: i.NGAYLAP, reverse=True)
    medicalRecord=medicalRecords[0]
    roombeds = db.query(DetailArrangeRoomBedModel).filter(DetailArrangeRoomBedModel.MABA==medicalRecord.MABA).all()
    detailservices = db.query(DetailServiceModel).filter(DetailServiceModel.MABA==medicalRecord.MABA).all()
    advances = db.query(AdvancesModel).filter(AdvancesModel.MABA==medicalRecord.MABA).all()
    services_raw = db.query(ServiceModel).all()
    bed = db.query(BedModel).all()
    room= db.query(RoomModel).all()
    detail_room_bed = db.query(DetailRoomBedModel).all()
    medicines=db.query(MedicineModel).all()
    #thong ke thue phong
    room=get_borrow_bed(roombeds,detail_room_bed,bed,room)

    #tinh tong tien tam ung
    for advance in advances:
        total_advances=total_advances+advance.SOTIEN

    #thong ke dich vu
    service_dict=count_service(services_raw,detailservices)
    services=get_all_services(services_raw,detailservices,service_dict)

    #Tinh thuoc
    medicines=get_all_medicine(medicines, db, CMND)

    return {"advances":total_advances,"room":room,"service":services,"medicine":medicines}
