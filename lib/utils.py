import xml.etree.ElementTree as ET

import numpy as np
import csv

def logit(p):
    return np.log(p / (1-p))

def logitinv(p):
	return 1.0 / (1 + np.exp(-p))

def convert_xml_to_csv(inp,out,col_names,readings_list,append=False,data_point=None,filezipped=True):
    if append:
        output = open(out,"a")
    else:
        output = open(out,"w")
    csvwriter = csv.writer(output, delimiter=',',quotechar='"')
    if not append:
        csvwriter.writerow(col_names)
    
    if filezipped:
        with zipfile.ZipFile(inp) as myzip:
            xmldata = myzip.read(myzip.namelist()[0])
            root = ET.fromstring(xmldata)
    else:
        with open(inp) as fp:
            xmldata = fp.read()
            root = ET.fromstring(xmldata)
    
    students = root[0][0][0]
    for student in students:
        data_meta_ethnicity = student.attrib['Ethnicity']
        data_meta_iep = student.attrib['IEP']
        data_meta_lep = student.attrib['LEP']
        data_meta_gender = student.attrib['Gender']
        data_meta_vendor_student_id = student.attrib['Vendor_Student_ID']

        student_details = student.findall("./Student_Test_List/Student_Test_Details")[0]
        data_meta_student_grade = student_details.attrib['Grade']
        data_meta_student_test_id = student_details.attrib['Student_Test_ID']
        test = student.findall("./Student_Test_List/Student_Test_Details/Item_List[0]/Item_Details")[0]
        
        data_answer = test.findall("./Item_Response")[0].text.replace("\n","").strip()
        
        scores_reader_id = ['']*len(readings_list)
        scores_values = ['']*len(readings_list)
        scores_condition_codes = ['']*len(readings_list)
        
        try:
            if data_point is None:
                data_final_score = test.findall("./Item_Score_Details/Item_DataPoint_Score_Details")[0].attrib["Final_Score"]
            else:
                data_final_score = test.findall("./Item_Score_Details/Item_DataPoint_Score_Details[@Data_Point='%s']" % (data_point))[0].attrib["Final_Score"]
            for i, reading_id in enumerate(readings_list):
                if data_point is None:
                    score = test.findall("./Item_Score_Details/Item_DataPoint_Score_Details/Score[@Read_Number='%d']" % (reading_id))
                else:
                    score = test.findall("./Item_Score_Details/Item_DataPoint_Score_Details[@Data_Point='%s']/Score[@Read_Number='%d']" % (data_point,reading_id))
                if len(score) > 0:
                    scores_reader_id[i] = score[0].attrib['Reader_ID']
                    if 'Score_Value' in score[0].attrib:
                        scores_values[i] = score[0].attrib['Score_Value']
                    elif 'Condition_Code' in score[0].attrib:
                        scores_condition_codes[i] = score[0].attrib['Condition_Code']
                    else:
                        raise ValueError, "No score or condition code"
        except:
            pass
        
        label = "VALIDATION" if append else "TRAINING"
        row = [label,data_meta_ethnicity,data_meta_iep,data_meta_lep,data_meta_gender,data_meta_vendor_student_id,data_meta_student_grade,data_meta_student_test_id,data_answer]
        row.extend(scores_reader_id)
        row.extend(scores_values)
        row.extend(scores_condition_codes)
        csvwriter.writerow(row)
    output.close()    

