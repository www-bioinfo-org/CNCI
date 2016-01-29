#!/usr/bin/python
#-*-coding : utf-8-*-
#Copyright(c) 2013 - SunLiang <sunliang@bioinfo.ac.cn>
import struct
import math
import cmath
import re
import string
import os
import random
import decimal
import sys
import optparse
import subprocess
import time
from multiprocessing import Process
import shutil
######################### define input and output######################################
#FileName = raw_input('Please enter your a file name: ')
parse=optparse.OptionParser()
parse.add_option('-f','--file',dest='file',action='store',metavar='input files',help='enter your transcript (sequence or gtf)')
parse.add_option('-o','--out',dest='outfile',action='store',metavar='output files',help='assign your output file')
parse.add_option('-p','--parallel',dest='parallel',action='store',metavar='prallel numbers',help='please enter your specified speed ratio')
parse.add_option('-m','--model',dest='model',action='store',metavar='model types',default='ve',help='please enter your specified classification model')
parse.add_option('-g','--gtf',dest='gtf',action='store_true',metavar='gtf file name',help='please enter your gtf files')
parse.add_option('-d','--directory',dest='directory',action='store',metavar='',help='if your input file is gtf type please enter RefGenome directory')
(options,args) = parse.parse_args()
inPutFileName = options.file
outPutFileName = options.outfile
Parallel = options.parallel
ClassModel = options.model
FileType = options.gtf
Directory = options.directory

CNCIPATH = os.path.split(os.path.realpath(__file__))[0]
print CNCIPATH
################################################################
if ClassModel == 've':
    MatrixPath = CNCIPATH + "/CNCI_Parameters/CNCI_matrix"
    inMatrix = open(MatrixPath)
    Matrix = inMatrix.read()
    inMatrix.close()
if ClassModel == 'pl':
    MatrixPath = CNCIPATH + "/CNCI_Parameters/CNCI_matrix"
    inMatrix = open(MatrixPath)
    Matrix = inMatrix.read()
    inMatrix.close()
#################################### 64 alphabet and hash dictionary ############################################
Alphabet = ['ttt','ttc','tta','ttg','tct','tcc','tca','tcg','tat','tac','tgt','tgc','tgg','ctt','ctc','cta','ctg','cct','ccc','cca','ccg','cat','cac','caa','cag','cgt','cgc','cga','cgg','att','atc','ata','atg','act','acc','aca','acg','aat','aac','aaa','aag','agt','agc','aga','agg','gtt','gtc','gta','gtg','gct','gcc','gca','gcg','gat','gac','gaa','gag','ggt','ggc','gga','ggg']
Matrix_hash = {}
Matrix_Arr=Matrix.split('\n')
length = len(Matrix_Arr) - 1
del Matrix_Arr[length]
for line in Matrix_Arr :
    each = line.split('\t')
    key = each[0]
    value = each[1]
    Matrix_hash[key] = value
######################################## main method###############################################################3
def count (CNCI_files,number):
    File_Counts = []
    for i in range(1,int(number)+1):
        temp_inPutFileNum = ''+CNCI_files+'/CNCI_file' + str(i)
        CNCI_FILES = open(temp_inPutFileNum)
        sub_cnci_files = CNCI_FILES.read()
        sub_cnci_array = sub_cnci_files.split('\n')
        sub_cnci_array_len = int(len(sub_cnci_array) / 2)
        File_Counts.append(sub_cnci_array_len)
        CNCI_FILES.close()
    return File_Counts
def check(ScoreFile,DetilFile):
    SUB_SCORE_FILE = open(ScoreFile)
    SUB_DETIL_FILE = open(DetilFile)
    sub_score_string = SUB_SCORE_FILE.read()
    sub_detil_string = SUB_DETIL_FILE.read()
    sub_score_array = sub_score_string.split('\n')
    sub_score_array_length = int(len(sub_score_array) - 1)
    sub_detil_array = sub_detil_string.split('\n')
    sub_detil_array_length = int(len(sub_detil_array) - 1)
    SUB_SCORE_FILE.close()
    SUB_DETIL_FILE.close()
    return (sub_score_array_length,sub_detil_array_length)
########################################################################
def InitCodonSeq(num,length,step,Arr):
    TempStrPar = ''
    for w in range(num,length,step):
        index = w
        code1 = Arr[index]
        index += 1
        code2 = Arr[index]
        index += 1
        code3 = Arr[index]
        Temp = code1+code2+code3
        TempStrPar = TempStrPar+Temp+' '
    return TempStrPar
##############################################################
def split(files,number,out):
    file_num = len(files) / 2
    split_step = int(int(file_num) / int(number))
    split_step = split_step * 2
    title = ''+out+'/CNCI_file'
    start = 0
    end = split_step
    for i in range(1,int(number) + 1):
        if i < int(number):
            temp_title = title + str(i)
            TEMP_FILE = open(temp_title,'w')
            for j in range(start,end):
                Tmp = files[j]
                Tmp = str(Tmp) + '\n'
                TEMP_FILE.write(Tmp)
            TEMP_FILE.close()
            start += split_step
            end += split_step
        else:
            temp_title = title + str(number)
            TEMP_FILE = open(temp_title,'w')
            for j in range(start,len(files)):
                Tmp = files[j]
                Tmp = str(Tmp) + '\n'
                TEMP_FILE.write(Tmp)
###################################################################################################3
def Add_Svm_Label(rec,FileName):
    SVM_arr_store = []
    SVM_FILE_ONE = open(FileName,'w')
    #SVM_FILE_ONE = open('SVM_FILE','w')
    for i in range(len(rec)):
        temp_str = rec[i]
        temp_arr = temp_str.split(' ')
        for j in range(len(temp_arr)):
            index = j + 1
            temp_arr[j] = str(index)+':'+str(temp_arr[j])
        str_temp = ' '.join(temp_arr)
        SVM_arr_store.append(str_temp)
        str_temp = str_temp + '\n'
        SVM_FILE_ONE.write(str_temp)
    return SVM_arr_store
    SVM_FILE_ONE.close()
###################################################################
def PutResult(detil_array):
    File = open(SvmFile)
    file_arr_temp = File.read()
    File.close()
    classify_index = 0
    file_Arr = file_arr_temp.split('\n')
    index_coding = '1'
    index_noncoding = '-1'
    Temp_Result_Arr = []
    for i in range(len(detil_array)):
        temp_label_str = detil_array[i]
        temp_label_arr_label = temp_label_str.split(";;;;;")
        Label = temp_label_arr_label[0]
        temp_label_arr = temp_label_arr_label[1].split(" ")
        sub_temp_label_arr = temp_label_arr[1:]
        sub_temp_label_str = ' '.join(sub_temp_label_arr)
        length = temp_label_arr[1]
        score = temp_label_arr[2]
        if file_Arr[classify_index] == index_coding:
            Label = str(Label) + ';;;;; ' + 'coding'
        else:
            Label = str(Label) + ';;;;; ' + 'noncoding'
        classify_index = classify_index + 1
        Temp_Result_str = str(Label) + ' ' + sub_temp_label_str
        Temp_Result_Arr.append(Temp_Result_str)

    return Temp_Result_Arr
#####################################################################
def PringResult(result,svmfinal):
    #OutFile = open('filename','w')
    OutFileResult = open(svmfinal,'w')
    Tabel = 'Transcript ID' + '\t' + 'index' + '\t' + 'score' + '\t' + 'start' + '\t' + 'end' + '\t' + 'length' + '\n'
    OutFileResult.write(Tabel)
    Out_Hash = {}
    for i in range(len(result)):
        out_label = result[i]
        out_label_arr_label = out_label.split(';;;;;')
        out_label_arr = out_label_arr_label[1].split(' ')
        T_label = out_label_arr_label[0]
        Tabel_label = T_label[1:]
        property = out_label_arr[1]
        start_position = out_label_arr[2]
        stop_position = out_label_arr[3]
        value = out_label_arr[4]
	out_value = value[0:5]
	out_value = string.atof(out_value)
        T_length = out_label_arr[5]
	if out_value == 0:
	    out_value = out_value + 0.001
        #if out_value == 0:
        #    while True:
        #        out_value = random.randint(0.1,1)
        #        if Out_Hash[out_value] != 1:
        #            break
        #    Out_Hash[out_value] = 1
        #    out_value = out_value * -1
        if property == 'noncoding':
            out_value = string.atof(0.64) * out_value
            out_value = 0.64 * out_value
            if out_value > 0:
                if out_value > 1:
                    out_value = -1 / out_value
                    temp_out_str = str(Tabel_label)+'\t'+str(property)+'\t'+str(out_value)+'\t'+str(start_position)+'\t'+str(stop_position)+'\t'+str(T_length)
                    temp_out_str = temp_out_str + '\n'
                    OutFileResult.write(temp_out_str)
                else:
                    out_value = -1 * out_value
		    temp_out_str = str(Tabel_label)+'\t'+str(property)+'\t'+str(out_value)+'\t'+str(start_position)+'\t'+str(stop_position)+'\t'+str(T_length)
                    temp_out_str = temp_out_str + '\n'
                    OutFileResult.write(temp_out_str)
            else:
	        temp_out_str = str(Tabel_label)+'\t'+str(property)+'\t'+str(out_value)+'\t'+str(start_position)+'\t'+str(stop_position)+'\t'+str(T_length)
                temp_out_str = temp_out_str + '\n'
                OutFileResult.write(temp_out_str)
        if property == 'coding':
            if out_value <= 0:
                if out_value <= - 1:
                    out_value = -1 / out_value
		    temp_out_str = str(Tabel_label)+'\t'+str(property)+'\t'+str(out_value)+'\t'+str(start_position)+'\t'+str(stop_position)+'\t'+str(T_length)
                    temp_out_str = temp_out_str + '\n'
                    OutFileResult.write(temp_out_str)
                else:
                    out_value = -1 * out_value
		    temp_out_str = str(Tabel_label)+'\t'+str(property)+'\t'+str(out_value)+'\t'+str(start_position)+'\t'+str(stop_position)+'\t'+str(T_length)
                    temp_out_str = temp_out_str + '\n'
                    OutFileResult.write(temp_out_str)
            else:
	        temp_out_str = str(Tabel_label)+'\t'+str(property)+'\t'+str(out_value)+'\t'+str(start_position)+'\t'+str(stop_position)+'\t'+str(T_length)
                temp_out_str = temp_out_str + '\n'
                OutFileResult.write(temp_out_str)
def TwoLineFasta (Seq_Array):
    Tmp_sequence_Arr = []
    Tmp_trans_str = ''
    for i in range(len(Seq_Array)):
        if '>' in Seq_Array[i]:
            if i == 0:
                Tmp_sequence_Arr.append(Seq_Array[i])
            else:
                Tmp_sequence_Arr.append(Tmp_trans_str)
                Tmp_sequence_Arr.append(Seq_Array[i])
                Tmp_trans_str = ''
        else:
            if i == len(Seq_Array) - 1:
                Tmp_trans_str = Tmp_trans_str + str(Seq_Array[i])
                Tmp_sequence_Arr.append(Tmp_trans_str)
            else:
                Tmp_trans_str = Tmp_trans_str + str(Seq_Array[i])
    return Tmp_sequence_Arr
def Tran_checkSeq (input_arr,Temp_Log):
    label_Arr = []
    FastA_seq_Arr = []
    for n in range(len(input_arr)):
        if n == 0 or n % 2 == 0:
            label = input_arr[n]
            label_Arr.append(label)
        else :
            seq = input_arr[n]
            FastA_seq_Arr.append(seq)
    LogResult = Temp_Log + '.log'
    LOG_FILE = open(LogResult,'w')
    num = 0
    for i in range(len(label_Arr)):
        Label = label_Arr[num]
        Seq = FastA_seq_Arr[num]
        tran_fir_seq = Seq.lower()
        tran_sec_seq_one = tran_fir_seq.replace('u','t')
        tran_sec_seq = tran_sec_seq_one.replace('\r','')
        if 'n' in tran_sec_seq:
            LogString = Label + ' ' + 'contain unknow nucleotide (n),please checkout your sequence again' + '\n'
            LOG_FILE.write(LogString)
            del label_Arr[num]
            del FastA_seq_Arr[num]
            continue
        if 'w' in tran_sec_seq:
            LogString = Label + ' ' + 'contain unknow nucleotide (w),please checkout your sequence again' + '\n'
            LOG_FILE.write(LogString)
            del label_Arr[num]
            del FastA_seq_Arr[num]
            continue
        if 'd' in tran_sec_seq:
            LogString = Label + ' ' + 'contain unknow nucleotide (d),please checkout your sequence again' + '\n'
            LOG_FILE.write(LogString)
            del label_Arr[num]
            del FastA_seq_Arr[num]
            continue
        if 'r' in tran_sec_seq:
            LogString = Label + ' ' + 'contain unknow nucleotide (r),please checkout your sequence again' + '\n'
            LOG_FILE.write(LogString)
            del label_Arr[num]
            del FastA_seq_Arr[num]
            continue
        if 's' in tran_sec_seq:
            LogString = Label + ' ' + 'contain unknow nucleotide (s),please checkout your sequence again' + '\n'
            LOG_FILE.write(LogString)
            del label_Arr[num]
            del FastA_seq_Arr[num]
            continue
        if 'y' in tran_sec_seq:
            LogString = Label + ' ' + 'contain unknow nucleotide (y),please checkout your sequence again' + '\n'
            LOG_FILE.write(LogString)
            del label_Arr[num]
            del FastA_seq_Arr[num]
            continue
        if 'm' in tran_sec_seq:
            LogString = Label + ' ' + 'contain unknow nucleotide (m),please checkout your sequence again' + '\n'
            LOG_FILE.write(LogString)
            del label_Arr[num]
            del FastA_seq_Arr[num]
            continue
        num = int(num) + int(1)
    LOG_FILE.close()
    return (label_Arr,FastA_seq_Arr)
######################################################################
def mainProcess(input,codonArr,hash_matrix,output,number):
    temp_score = ''+output+'/CNCI_file_score' + str(number)
    temp_detil = ''+output+'/CNCI_file_detil' + str(number)
    SCORE = open(temp_score,'w')
    DETIL = open(temp_detil,'w')
    sequence_Arr = input.split('\n')
    sLen = len(sequence_Arr) - 1
    del sequence_Arr[sLen]
######################################################################
    label_Arr_tmp = []
    FastA_seq_Arr_tmp = []
    for n in range(len(sequence_Arr)):
        if n == 0 or n % 2 == 0:
            label = sequence_Arr[n]
            label_Arr_tmp.append(label)
        else :
            seq = sequence_Arr[n]
            FastA_seq_Arr_tmp.append(seq)
###########################################################
    PROPERTY_ARR = []
    DETIL_ARR = []
    for i in range(len(label_Arr_tmp)):
        Label = label_Arr_tmp[i]
        Seq = FastA_seq_Arr_tmp[i]
        Detil_len = len(Seq)
        tran_fir_seq = Seq.lower()
        tran_sec_seq = tran_fir_seq.replace('u','t')
        sequence_process_Arr = list(tran_sec_seq)
        r_sequence_process_Arr = sequence_process_Arr[:]
        r_sequence_process_Arr.reverse()
        Seq_len = len(sequence_process_Arr) - 1
        max_Value = []
        max_String = []
        score_array = []
        length_store_array = []
        Pos = []
        for o in range(0,6): #six kinds of open reading frame of each sequence
            CodonScore = []  # coden information array
            RelScore = []    # relate acid information array /
            TempStr = ''
            if o < 3 :
                TempStr = InitCodonSeq(o,Seq_len-1,3,sequence_process_Arr)
            if 2 < o < 6 :
                TempStr = InitCodonSeq(o-3,Seq_len-1,3,r_sequence_process_Arr)
            TempArray = TempStr.split(' ') # construct codon array
            TempArray.pop()
            seqLength = len(TempArray)
            WindowStep = 50
            WinLen = seqLength - WindowStep
            if seqLength > WindowStep:
                for EachCodon in range(WinLen):
                    num = 0
                    SingleArray = []
                    for t in range(EachCodon,WindowStep+EachCodon):
                        SingleArray.append(TempArray[t])
                    SinLen = len(SingleArray) - 1
                    for n in range(0,SinLen):
                        temp1 = SingleArray[n]+SingleArray[n+1]
                        temple1 = re.compile('[atcg]{6}')
                        if temple1.match(temp1):
                            num = string.atof(num) + string.atof(hash_matrix[temp1])
                    num = num / WindowStep
                    CodonScore.append(num)

                Start = 0
                End = 0
	        Max = 0
                Position = ''
                for r in range(len(CodonScore)):
                    sum = 0
                    CodonLength = len(CodonScore)
                    for e in range(r,CodonLength):
                        sum = sum + string.atof(CodonScore[e])
                        if sum > Max:
                            Start = r
                            End = e
                            Max = sum
                    OutStr = ''
                for out in range(Start,End+1):
                    OutStr = OutStr+TempArray[out]+' '
                Start = Start * 3
                End = End *3
                Position = str(Start)+' '+str(End)
                Pos.append(Position)
                max_Value.append(Max)
                max_String.append(OutStr)
                OutParray = OutStr.split(' ')
                max_length = len(OutParray) - 1
                Onum = 0
                for n in range(max_length):
                    temp1 = OutParray[n]+OutParray[n+1]
                    temple = re.compile('[atcg]{6}')
                    if temple.match(temp1):
                        Onum = string.atof(Onum) + string.atof(hash_matrix[temp1])
                score_array.append(Onum)
                length_store_array.append(max_length)
            else:
                num = 0
                for n in range(seqLength-1):
                    temp1 = TempArray[n]+TempArray[n+1]
                    temple2 = re.compile('[atcg{6}]')
                    if temple2.match(temp1):
                        num = string.atof(num) + string.atof(hash_matrix[temp1])
                OutStr = ' '.join(TempArray)
                Pos.append('Full Length')
                max_Value.append(num)
                max_String.append(OutStr)
                score_array.append(num)
                length_store_array.append(seqLength)
        r_max_Value = max_Value[:]
        r_max_Value.sort(reverse=True)
        M = r_max_Value[0] # property number one
        orf_index = 0
        for o in range(len(max_Value)):
            temp = max_Value[o]
            if temp == M:
                orf_index = o
        detil_index = orf_index # The selected reading frame
        o_arr = max_String[orf_index].split(' ') ## MLCDS sequence
        o_arr.pop()
        SequenceLen = len(o_arr) - 1
        M_score = 0
        for j in range(SequenceLen):
            temp_trip = o_arr[j]+o_arr[j+1]
            temple3 = re.compile('[atcg]{6}')
            if temple3.match(temp_trip):
                M_score = string.atof(M_score) + string.atof(hash_matrix[temp_trip])
        SequenceLen = SequenceLen + 2
        M_score = M_score / SequenceLen  ### M_score
        MLCDS_str = ''.join(o_arr)
        MLCDS_sequence = list(MLCDS_str)
        rMLCDS_sequence = MLCDS_sequence[:]
        rMLCDS_sequence.reverse()
        MLCDS_seq_length = len(MLCDS_sequence) - 1
        other_CDS_array = []
        for o in range(1,6):
            MLCDS_TempStr = ''
            if o < 3:
                 MLCDS_TempStr = InitCodonSeq(o,MLCDS_seq_length-1,3,MLCDS_sequence)
            if 2 < o < 6 :
                 MLCDS_TempStr = InitCodonSeq(o,MLCDS_seq_length-1,3,rMLCDS_sequence)
            MLCDS_array = MLCDS_TempStr.split(' ') ## codon array
            MLCDS_array.pop()
            other_num = 0
            MLCDS_array_Len = len(MLCDS_array) - 1
            for j in range(MLCDS_array_Len):
                temp2 = MLCDS_array[j]+MLCDS_array[j+1]
                temple4 = re.compile('[atcg]{6}')
                if temple4.match(temp2):
                    other_num = string.atof(other_num) + string.atof(hash_matrix[temp2])
            MLCDS_array_Len = MLCDS_array_Len + 2
            other_num = other_num / MLCDS_array_Len
            other_CDS_array.append(other_num)

        score_distance = 0
        for m in range(len(other_CDS_array)):
            score_distance += M_score - other_CDS_array[m]
        score_distance = score_distance / 5 ####### score_distance
########################################################################################
        out_pos = Pos[orf_index]
        M_length = length_store_array[orf_index]
        length_total_score = 0
        for p in range(len(length_store_array)):
            length_total_score = string.atof(length_total_score) + string.atof(length_store_array[p])
        length_precent = string.atof(M_length) / string.atof(length_total_score) ## length_precent
########################################################################################3
        detil_other_length_array = []
        for p in range(len(length_store_array)):
            temp = length_store_array[p]
            if temp != M_length:
                detil_other_length_array.append(temp)
        r_detil_other_length_array = detil_other_length_array[:]
        r_detil_other_length_array.sort(reverse=True)
############################################################################################3
        dicodon_hash = {}
        Coding_Array_one = []
        keys_Coding_Array = []
        for i in range(len(codonArr)):
            temp = codonArr[i]
            dicodon_hash[temp] = 0
        for n in range(len(o_arr)):
            temp1 = o_arr[n]
            tep1 = re.compile('[atcg{3}]')
            if tep1.match(temp1) and temp1 != 'taa' and temp1 != 'tag' and temp1 != 'tga':
                dicodon_hash[temp1] = dicodon_hash[temp1] + 1
        for (key,value) in dicodon_hash.items():
            Coding_Array_one.append(value)
            keys_Coding_Array.append(key)
#############################################################################################
        C_num1 = 0
        for i in range(len(Coding_Array_one)):
            C_num1 = string.atof(C_num1) + string.atof(Coding_Array_one[i])
        if C_num1 == 0:
            C_num1 = 1
        for i in range(len(Coding_Array_one)):
            Coding_Array_one[i] = str(Coding_Array_one[i] / C_num1)
        Array_Str = ' '.join(Coding_Array_one)
        GC_string = ' '.join(o_arr)
        GC_array = GC_string.split(' ')
        GC_number = 0
        for c in range(len(GC_array)):
            temp = GC_array[c]
            if temp == 'g' or temp == 'c':
               GC_number = GC_number + 1
        GC_precent = GC_number / len(GC_array)# GC precent
###############################################################################################
        PROPERTY_STR = str(M)+' '+str(M_length)+' '+str(M_score)+' '+str(length_precent)+' '+str(score_distance)+' '+str(Array_Str) + '\n'
        DETIL_STR = str(Label)+';;;;; '+str(out_pos)+' '+str(M_score) + ' ' + str(Detil_len) + '\n'
        SCORE.write(PROPERTY_STR)
        DETIL.write(DETIL_STR)
        PROPERTY_ARR.append(PROPERTY_STR)
        DETIL_ARR.append(DETIL_STR)
    return(PROPERTY_ARR,DETIL_ARR)
#######################################################################################################################
if FileType:
    inGtfFiles = inPutFileName + '.bed'
    fastaFiles = inPutFileName + '.fa'
    os.system('perl ' + CNCIPATH + '/gtf2Bed.pl '+inPutFileName+' > '+inGtfFiles+'')
    time.sleep(10)
    os.system('twoBitToFa -bed='+inGtfFiles+' '+Directory+' '+fastaFiles+' ')
    GtfInFiles = open(fastaFiles)
    inFilesArr = GtfInFiles.read()
    inFileNum = inFilesArr.split('\n')
    inFileLen = len(inFileNum) - 1
    GtfInFiles.close()
else:
    inFiles = open(inPutFileName)
    inFilesArr = inFiles.read()
    inFileNum = inFilesArr.split('\n')
    inFileLen = len(inFileNum) - 1
    inFiles.close()
#################################################################
Compute_time = time.time()
sequence_Arr = inFilesArr.split('\n')
sLen = len(sequence_Arr) - 1
del sequence_Arr[sLen]
ARRAY =  TwoLineFasta(sequence_Arr)
temp_log = outPutFileName
Label_Array,FastA_Seq_Array = Tran_checkSeq(ARRAY,temp_log)
inFileLength = len(Label_Array)
TOT_STRING = []
for i in range(len(Label_Array)):
    tmp_label_one = Label_Array[i]
    tmp_label = tmp_label_one.replace('\r','')
    tmp_seq = FastA_Seq_Array[i]
    Temp_Seq = tmp_seq.replace('\r','')
    TOT_STRING.append(tmp_label)
    TOT_STRING.append(Temp_Seq)
############################################################
if Parallel == 1:
    (Result_Pro,Result_Detil) = mainProcess(inFilesArr,Alphabet,Matrix_hash,outPutFileName,1,)
    Temp_Dir = outPutFileName + '_Temp_Dir'
    subprocess.call('mkdir '+Temp_Dir+'' , shell=True)
    SvmoutPutFile = Temp_Dir + '/pro'
    SvmPutFileName = Temp_Dir + '/svm'
    SvmFile = Temp_Dir + '/file'
    svm_tmp = Temp_Dir + '/temp'
    SVM_STORE = Add_Svm_Label(Result_Pro,SvmoutPutFile)
################################################################################################
    if ClassModel == 've':
        os.system(CNCIPATH + '/libsvm-3.0/svm-scale -r '+ CNCIPATH + '/CNCI_Parameters/python_scale '+SvmoutPutFile+' > '+SvmPutFileName+'')
        os.system(CNCIPATH + '/libsvm-3.0/svm-predict '+SvmPutFileName+' ' + CNCIPATH + '/CNCI_Parameters/python_model '+SvmFile+' > '+svm_tmp+'')
    if ClassModel == 'pl':
        os.system(CNCIPATH + '/libsvm-3.0/svm-scale -r ' + CNCIPATH + '/CNCI_Parameters/plant_scale '+SvmoutPutFile+' > '+SvmPutFileName+'')
        os.system(CNCIPATH + '/libsvm-3.0/svm-predict '+SvmPutFileName+' ' + CNCIPATH + '/CNCI_Parameters/plant_model '+SvmFile+' > '+svm_tmp+'')
##########################################################################################################
    FirResult = PutResult(Result_Detil)
    Out_Dir = outPutFileName
    subprocess.call('mkdir '+Out_Dir+'' , shell=True)
    SvmFinalResutl = ''+Out_Dir+'/CNCI.index'
    PringResult(FirResult,SvmFinalResutl)
    #subprocess.call('rm '+SvmPutFileName+' ', shell=True)
    #subprocess.call('rm '+SvmFile+' ', shell=True)
    #subprocess.call('rm '+svm_tmp+' ', shell=True)
    #subprocess.call('rm '+outPutFileName+' ', shell=True)
    print 'CNCI classification were completely done!'
    print "%f second for" % (time.time() - Compute_time) + ' ' + str(inFileLength) + ' ' + "transcript's computation."
    shutil.rmtree(Temp_Dir,True)
if Parallel > 1:
    Proc_Thread = []
    Temp_Dir = outPutFileName + '_Tmp_Dir'
    Out_Dir = outPutFileName
    subprocess.call('mkdir '+Temp_Dir+'' , shell=True)
    subprocess.call('mkdir '+Out_Dir+'' , shell=True)
    split(TOT_STRING,Parallel,Temp_Dir)
    Con_ARRAY = count(Temp_Dir,Parallel)
    for i in range(1,int(Parallel)+1):
        temp_inPutFileName = ''+Temp_Dir+'/CNCI_file' + str(i)
        temp_inFiles = open(temp_inPutFileName)
        temp_inFilesArr = temp_inFiles.read()
        Proc_Thread.append(Process(target=mainProcess, args=(temp_inFilesArr,Alphabet,Matrix_hash,Temp_Dir,str(i))))
    for p in Proc_Thread:
        p.start()
    for i in Proc_Thread:
        p.join()

    for i in range(1,int(Parallel)+1):
        n = int(i) - 1
        Score_string = ''+Temp_Dir+'/CNCI_file_score' + str(i)
        Detil_string = ''+Temp_Dir+'/CNCI_file_detil' + str(i)
        SUB_SCORE_LEN = 0
        SUB_DETIL_LEN = 0
#########################################################################
        SUB_SCORE_LEN,SUB_DETIL_LEN  = check(Score_string,Detil_string)
        while int(SUB_SCORE_LEN) < Con_ARRAY[n] or int(SUB_DETIL_LEN) < Con_ARRAY[n]:
            SUB_SCORE_LEN,SUB_DETIL_LEN = check(Score_string,Detil_string)
#######################################################################
        subprocess.call('cat '+Score_string+' >> '+Temp_Dir+'/CNCI_score', shell=True)
        subprocess.call('cat '+Detil_string+' >> '+Temp_Dir+'/CNCI_detil', shell=True)
    Score_File_Path = ''+Temp_Dir+'/CNCI_score'
    Detil_File_Path = ''+Temp_Dir+'/CNCI_detil'
    SCORE_FILE = open(Score_File_Path)
    DETIL_FILE = open(Detil_File_Path)
    score_string = SCORE_FILE.read()
    detil_string = DETIL_FILE.read()
    score_array = score_string.split('\n')
    scoreSLength = int(len(score_array) - 1)
    del score_array[scoreSLength]
    detil_array = detil_string.split('\n')
    detilSLength = int(len(detil_array) - 1)
    del detil_array[detilSLength]
    #######################################################################
    SvmoutPutFile = Temp_Dir + '/pro'
    SvmPutFileName = Temp_Dir + '/svm'
    SvmFile = Temp_Dir + '/file'
    svm_tmp = Temp_Dir + '/temp'
    SVM_STORE = Add_Svm_Label(score_array,SvmoutPutFile)
    #################################################################################################
    if ClassModel == 've':
        os.system(CNCIPATH + '/libsvm-3.0/svm-scale -r ' + CNCIPATH + '/CNCI_Parameters/python_scale '+SvmoutPutFile+' > '+SvmPutFileName+'')
        os.system(CNCIPATH + '/libsvm-3.0/svm-predict '+SvmPutFileName+' ' + CNCIPATH + '/CNCI_Parameters/python_model '+SvmFile+' > '+svm_tmp+'')
    if ClassModel == 'pl':
        os.system(CNCIPATH + '/libsvm-3.0/svm-scale -r ' + CNCIPATH + '/CNCI_Parameters/plant_scale '+SvmoutPutFile+' > '+SvmPutFileName+'')
        os.system(CNCIPATH + '/libsvm-3.0/svm-predict '+SvmPutFileName+' ' + CNCIPATH + '/CNCI_Parameters/plant_model '+SvmFile+' > '+svm_tmp+'')
    ##########################################################################################################
    FirResult = PutResult(detil_array)
    SvmFinalResutl = Out_Dir + '/CNCI.index'
    PringResult(FirResult,SvmFinalResutl)
    #subprocess.call('rm '+SvmPutFileName+' ', shell=True)
    #subprocess.call('rm '+SvmFile+' ', shell=True)
    #subprocess.call('rm '+svm_tmp+' ', shell=True)
    #subprocess.call('rm '+outPutFileName+' ', shell=True)
    #subprocess.call('rm '+inGtfFiles+' ', shell=True)
    #subprocess.call('rm '+fastaFiles+' ', shell=True)
##############################################################################################################
    print 'CNCI classification were completely done!'
    print "%f second for" % (time.time() - Compute_time) + ' ' + str(inFileLength) + ' ' + "transcript's computation."
    shutil.rmtree(Temp_Dir,True)
