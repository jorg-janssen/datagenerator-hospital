
import json
import random
import datetime
import py2sql

         
def __main__():
   
    
    # BASE TABLES
    # departments - get from file
    # medicine - get from file
    # diagnoses - get from file
    # rooms - generate
    # generalphysicians - generate    

    # OTHER
    # beds - generate
    # specialists - generate
    # patients - generate

    # FACT TABLES
    # hospitalization - generate
    # medication - generate
    # other_diagnoses - generate

    # import files for some base tables
    departments = json.load(open('datafiles/departments.json', 'r'))
    medicines = json.load(open('datafiles/medicines.json', 'r'))
    diagnoses = json.load(open('datafiles/diagnoses.json', 'r'))
    
    # import helper files
    firstnames = json.load(open('datafiles/firstnames.json', 'r'))
    lastnames = json.load(open('datafiles/lastnames.json', 'r'))
    
    # generate helper lists
    birthdates = [datetime.date(1920, 1, 1)]
    while birthdates[-1] != datetime.date(2021, 12, 31):
        new = birthdates[-1] + datetime.timedelta(days=1)
        birthdates.append(new)
        
    hospitalizationdates = [datetime.date(2000, 1, 1)]
    while hospitalizationdates[-1] != datetime.date(2021, 12, 31):
        new = hospitalizationdates[-1] + datetime.timedelta(days=1)
        hospitalizationdates.append(new)    

    # Generate other base tables
    print("Rooms: ")
    rooms = []
    for room in random.sample(range(100, 700), 500):
        mydict = {}
        mydict["roomnumber"] = int(room)
        mydict["department"] = random.choice(departments)["departmentname"]
        rooms.append(mydict)
    print(len(rooms))
    print("---")
    
    print("General physicians: ")    
    generalphysicians = []
    for physician in range(100):
        mydict = {}
        firstname = random.choice(firstnames)
        mydict["initials"] = firstname[0]
        mydict["lastname"] = random.choice(lastnames)
        mydict["gpcode"] = (getConsonants(mydict["lastname"][0:mydict["lastname"].find(",")][0:5] ) + mydict["initials"]).upper()
        counter = 1
        while mydict["gpcode"] in dicts2list(generalphysicians, "gpcode"): 
            mydict["gpcode"] = mydict["gpcode"] + str(counter)
            counter += 1
        generalphysicians.append(mydict)
    print(len(generalphysicians))
    print("---")    
        
    print("Beds: ")
    beds = []
    for room in random.sample(rooms, k = int(len(rooms)* 0.9)):
        for bedno in range (1,random.randint(2,5)):
            bed = {}
            bed["room"] = room["roomnumber"]
            bed["bednumber"] = bedno
            beds.append(bed)
    print(len(beds))
    print("---")
            
    print("Specialists: ")
    specialists = []
    for x in range(100):
        specialist = {}
        firstname = random.choice(firstnames)
        specialist["initials"] = firstname[0]
        specialist["lastname"] = random.choice(lastnames)
        specialist["departmentname"] = random.choice(departments)["departmentname"]
        specialist["specialistcode"] = (getConsonants(specialist["lastname"][0:specialist["lastname"].find(",")][0:5] ) + specialist["initials"]).upper()
        counter = 1
        while specialist["specialistcode"] in dicts2list(specialists, "specialistcode"): 
            specialist["specialistcode"] = specialist["specialistcode"] + str(counter)
            counter += 1
        specialists.append(specialist)      
    print(len(specialists))        
    print("---")
    
    print("Patients: ")    
    patients = []
    for x in range(10061, 400000, 3):
      patient = {} 
      patient["patientnumber"] = x  
      patient["gpcode"] = random.choice(generalphysicians)["gpcode"]
      patient["firstname"] = random.choice(firstnames)
      patient["initials"] = patient["firstname"][0]
      patient["lastname"] = random.choice(lastnames)
      patient["gender"] = random.choice(["M","V"])
      patient["birthdate"] = random.choice(birthdates)
      patient["bloodtype"] = random.choice(["AA", "AB", "A0", "BB", "B0", "00", None])
      patients.append(patient)
    print(len(patients))
    print("---")

    # Generate fact tables
    print("Hospitalizations: ")
    hospitalizations = []
    for patient in random.sample(patients, k = int(len(patients)*0.8)):
        newdate = random.choice(hospitalizationdates)
        for x in range(1, random.randint(1,6)):        
            hospitalization = {}
            hospitalization["patient"] = patient["patientnumber"]
            hospitalization["hospitalizationdate"] = newdate 
            hospitalization["department"] = random.choice(departments)["departmentname"]
            hospitalization["specialist"] = random.choice(specialists)["specialistcode"]        
            hospitalization["maindiagnosis"] = random.choice(diagnoses)["diagnosiscode"]
            hospitalization["maindiagnosisdate"] = newdate + datetime.timedelta(days=random.randint(0,2))
            hospitalization["enddate"] = hospitalization["maindiagnosisdate"] + datetime.timedelta(days=random.randint(0,30))            
            # build list of beds of this department:
            department_beds = []
            for room in rooms:
                if room["department"] == hospitalization["department"]:
                    for bed in beds:
                        if bed["room"] == room["roomnumber"]:
                            department_beds.append(bed)
            bed = random.choice(department_beds)
            # check wether the bed is occupied in period
            #   - build list of hospitalizations for this department:
            department_hospitalizations = []            
            for h in hospitalizations:
                if h["department"] == hospitalization["department"]:
                    department_hospitalizations.append(h)
            occupied = True
            counter = 1
            while occupied:
                occupation_found = False
                for other_hospitalization in department_hospitalizations:
                    print 
                    if bed["room"] == other_hospitalization["room"] and bed["bednumber"] == other_hospitalization["bed"] and checkPeriodOverlap(hospitalization["hospitalizationdate"], hospitalization["enddate"], other_hospitalization["hospitalizationdate"], other_hospitalization["enddate"]):
                        occupation_found = True
                        counter += 1
                        bed = random.choice(beds)
                        break
                occupied = occupation_found   
            #print("Found bed in", counter, "tries")
            hospitalization["room"] = bed["room"]
            hospitalization["bed"] = bed["bednumber"]        
            
            if hospitalization["enddate"].year >= 2021:
               hospitalization["enddate"] = None
               hospitalizations.append(hospitalization)
               break
            else:                
                hospitalizations.append(hospitalization)
                newdate = hospitalization["enddate"] + datetime.timedelta(days=random.randint(6,500))
    print(len(hospitalizations))
    print("---")
    
    print("Medications: ")
    medications = []
    for hospitalization in random.sample(hospitalizations, k = int(len(hospitalizations)*0.8)):
        for medicine in random.sample(medicines, k = random.randint(0,6)):
            medication = {}
            medication["patient"] = hospitalization["patient"]
            medication["hospitalizationdate"] = hospitalization["hospitalizationdate"]
            medication["medicine"] = medicine["medicinecode"]
            medication["startdate"] = hospitalization["hospitalizationdate"] + datetime.timedelta(days=random.randint(0,2))
            medication["enddate"] = medication["startdate"] + datetime.timedelta(days=random.randint(0,7))
            if random.random() > 0.1: 
                medication["hourly_dosage"] = None
                if medicine["pack_unit"] in ('pcs'):
                    medication["daily_dosage"] = random.randint(0,int(medicine["pack_quantity"]/random.randint(10,20))+1)
                else:
                    medication["daily_dosage"] = random.choice([0,25,50,100,150,200,250])
            else:
                medication["daily_dosage"] = None
                if medicine["pack_unit"] in ('pcs'):
                    medication["hourly_dosage"] = random.randint(0,5)
                else:
                    medication["hourly_dosage"] = random.choice([0,25,50,100,150,200,250])
            medications.append(medication)
    print(len(medications))
    print("---")

    print("Other diagnoses: ")
    other_diagnoses = []
    for hospitalization in random.sample(hospitalizations, k = int(len(hospitalizations)*0.5)):
        for diagnosis in random.sample(diagnoses, k = random.randint(0,5)):
            other_diagnosis = {}
            if diagnosis["diagnosiscode"] != hospitalization["maindiagnosis"]:
                other_diagnosis["patient"] = hospitalization["patient"]
                other_diagnosis["hospitalizationdate"] = hospitalization["hospitalizationdate"]
                other_diagnosis["diagnosis"] = diagnosis["diagnosiscode"]
                other_diagnosis["diagnosisdate"] = hospitalization["hospitalizationdate"] + datetime.timedelta(days=random.randint(0,2))
                other_diagnoses.append(other_diagnosis)
    print(len(other_diagnoses))
    print("---")   

    print("Writing file...")
    file = open("inserts.sql", "w")
    file.write("SET NOCOUNT ON\ngo\n")     

    py2sql.list2sql("Department", departments, file)
    py2sql.list2sql("Medicine", medicines, file)
    py2sql.list2sql("Diagnosis", diagnoses, file)
    py2sql.list2sql("Room", rooms, file)
    py2sql.list2sql("GeneralPhysician", generalphysicians, file) 
    py2sql.list2sql("Bed", beds, file)
    py2sql.list2sql("Specialist", specialists, file)
    py2sql.list2sql("Patient", patients, file)
    py2sql.list2sql("Hospitalization", hospitalizations, file)
    py2sql.list2sql("Medication", medications, file)
    py2sql.list2sql("OtherDiagnoses", other_diagnoses, file)

    file.close()
    
def dicts2list(listOfDicts, item):
    list = []
    for dict in listOfDicts:
        list.append(dict[item])
    return list
    
def getConsonants(string):
  return ''.join([each for each in string if each not in "aeiouAEIOU"])
  
def checkPeriodOverlap(begindate1, enddate1, begindate2, enddate2):
    #print (begindate1, enddate1, begindate2, enddate2);
    result = False
    if date_in(begindate1, begindate2, enddate2):
        result =  True
    elif date_in(enddate1, begindate2, enddate2):
        result =  True
    elif date_in(begindate2, begindate1, enddate1):
        result =  True
    elif date_in(enddate2, begindate1, enddate1):
        result =  True
    elif enddate2 == None and enddate1 >= begindate2:
        result =  True
    elif enddate1 == None and begindate1 <= enddate2:
        result =  True
    #print(result)
    return result

def date_in(thedate, begindate, enddate):
    if thedate == None:
        return False
    elif begindate == None or thedate >= begindate: 
        if enddate == None or thedate <= enddate:
            return True
        else:
            return False
    else:
        return False

def tupels2dicts(name, listOfTupels):
    list = []
    for tupel in listOfTupels:
        mydict = {name: tupel}
        list.append(mydict)
    return list

__main__()

