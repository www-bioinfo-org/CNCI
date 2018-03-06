'''
Created on 2013-6-7

@author: Tan Chengfu
'''
import re
import os
import sys
import shlex,subprocess
from Table import Table
from sets import Set

class Gtf(object):


    def __init__(self,*filepath):

        self.transcript = {}
        if filepath:
            path = filepath[0]
            global selfGtfFile
            selfGtfFile=path
            f = open(path,'r')
            line = f.readline()
            while line:
                if '#' in line and line.index('#') == 0:
                    line =f.readline()
                    continue
                else:
                    line = line.rstrip()
                    temp_list = line.split("\t")
                    temp_seqname = temp_list[0]
                    temp_source = temp_list[1]
                    temp_feature = temp_list[2]
                    temp_start = int(temp_list[3])
                    temp_end = int(temp_list[4])
                    try:
                        temp_score = int(temp_list[5])
                        score_flag = True
                    except ValueError:
                        temp_score = temp_list[5]
                        score_flag = False
                    temp_strand = temp_list[6]
                    try:
                        temp_frame = int(temp_list[7])
                    except ValueError:
                        temp_frame = temp_list[7]
                    temp_group =temp_list[8]
                    temp_gid = re.findall(r'gene_id.+?"(.+?)"',temp_group)[0]
                    temp_tid = re.findall(r'transcript_id.+?"(.+?)"',temp_group)[0]
                    temp_gname = re.findall(r'gene_name.+?"(.+?)"',temp_group)
                    if temp_gname:
                        temp_gname = temp_gname[0]
                    else:
                        temp_gname = ''
                    if temp_tid in self.transcript:
                        if temp_feature == 'exon':
                            self.transcript[temp_tid]['exon'].append([temp_start,temp_end])
                            self.transcript[temp_tid]['exon'].sort()
                        elif temp_feature == 'CDS':
                            self.transcript[temp_tid]['CDS_flag'] = True
                            self.transcript[temp_tid]['CDS'] = [temp_start,temp_end]
                        else:
                            continue
                        if(self.transcript[temp_tid]['score_flag']):
                            self.transcript[temp_tid]['score'] = (
                            float(sum(self.transcript[temp_tid]['scores']))
                            /len(self.transcript[temp_tid]['scores']))
                        else:
                            self.transcript[temp_tid]['score'] = '.'
                        if(not self.transcript[temp_tid]['CDS_flag']):
                            exon_start = self.transcript[temp_tid]['exon'][0][0]
                            exon_end = self.transcript[temp_tid]['exon'][-1][-1]
                            self.transcript[temp_tid]['CDS'] = [exon_start,exon_end]
                    else:
                        self.transcript[temp_tid] = {}
                        self.transcript[temp_tid]['gid'] = temp_gid
                        self.transcript[temp_tid]['gname'] = temp_gname
                        self.transcript[temp_tid]['seqname'] = temp_seqname
                        self.transcript[temp_tid]['exon'] = []
                        self.transcript[temp_tid]['score_flag'] = score_flag
                        self.transcript[temp_tid]['source'] = temp_source
                        self.transcript[temp_tid]['strand'] = temp_strand
                        self.transcript[temp_tid]['scores'] = []
                        self.transcript[temp_tid]['scores'].append(temp_score)
                        self.transcript[temp_tid]['CDS_flag'] = False
                        if(self.transcript[temp_tid]['score_flag']):
                            self.transcript[temp_tid]['score'] = (
                            float(sum(self.transcript[temp_tid]['scores']))
                            /len(self.transcript[temp_tid]['scores']))
                        else:
                            self.transcript[temp_tid]['score'] = '.'
                        self.transcript[temp_tid]['frame'] = temp_frame
                        if temp_feature == 'exon':
                            self.transcript[temp_tid]['exon'].append([temp_start,temp_end])
                        elif temp_feature == 'CDS':
                            self.transcript[temp_tid]['CDS_flag'] = True
                            self.transcript[temp_tid]['CDS'] = [temp_start,temp_end]
                    line = f.readline()

    @staticmethod
    def simple_read(*filepath):
        self=Gtf()
        if filepath:
            path = filepath[0]
            global selfGtfFile
            selfGtfFile=path
            f = open(path,'r')
            line = f.readline()
            while line:
                if '#' in line and line.index('#') == 0:
                    line =f.readline()
                    continue
                else:
                    line = line.rstrip()
                    temp_list = line.split("\t")
                    temp_seqname = temp_list[0]
                    temp_source = temp_list[1]
                    temp_feature = temp_list[2]
                    temp_start = int(temp_list[3])
                    temp_end = int(temp_list[4])
                    try:
                        temp_score = int(temp_list[5])
                        score_flag = True
                    except ValueError:
                        temp_score = temp_list[5]
                        score_flag = False
                    temp_strand = temp_list[6]
                    try:
                        temp_frame = int(temp_list[7])
                    except ValueError:
                        temp_frame = temp_list[7]
                    temp_group =temp_list[8]
                    temp_gid = re.findall(r'gene_id.+?"(.+?)"',temp_group)[0]
                    temp_tid = re.findall(r'transcript_id.+?"(.+?)"',temp_group)[0]
                    if temp_tid in self.transcript:
                        if temp_feature == 'exon':
                            self.transcript[temp_tid]['exon'].append([temp_start,temp_end])
                            self.transcript[temp_tid]['exon'].sort()
                        elif temp_feature == 'CDS':
                            self.transcript[temp_tid]['CDS_flag'] = True
                            self.transcript[temp_tid]['CDS'] = [temp_start,temp_end]
                        else:
                            line = f.readline()
                            continue
                        if(self.transcript[temp_tid]['score_flag']):
                            self.transcript[temp_tid]['score'] = (
                            float(sum(self.transcript[temp_tid]['scores']))
                            /len(self.transcript[temp_tid]['scores']))
                        else:
                            self.transcript[temp_tid]['score'] = '.'
                        if(not self.transcript[temp_tid]['CDS_flag']):
                            exon_start = self.transcript[temp_tid]['exon'][0][0]
                            exon_end = self.transcript[temp_tid]['exon'][-1][-1]
                            self.transcript[temp_tid]['CDS'] = [exon_start,exon_end]
                    else:
                        self.transcript[temp_tid] = {}
                        self.transcript[temp_tid]['gid'] = temp_gid
                        self.transcript[temp_tid]['gname'] = ''
                        self.transcript[temp_tid]['seqname'] = temp_seqname
                        self.transcript[temp_tid]['exon'] = []
                        self.transcript[temp_tid]['score_flag'] = score_flag
                        self.transcript[temp_tid]['source'] = temp_source
                        self.transcript[temp_tid]['strand'] = temp_strand
                        self.transcript[temp_tid]['scores'] = []
                        self.transcript[temp_tid]['scores'].append(temp_score)
                        self.transcript[temp_tid]['CDS_flag'] = False
                        if(self.transcript[temp_tid]['score_flag']):
                            self.transcript[temp_tid]['score'] = (
                            float(sum(self.transcript[temp_tid]['scores']))
                            /len(self.transcript[temp_tid]['scores']))
                        else:
                            self.transcript[temp_tid]['score'] = '.'
                        self.transcript[temp_tid]['frame'] = temp_frame
                        if temp_feature == 'exon':
                            self.transcript[temp_tid]['exon'].append([temp_start,temp_end])
                        elif temp_feature == 'CDS':
                            self.transcript[temp_tid]['CDS_flag'] = True
                            self.transcript[temp_tid]['CDS'] = [temp_start,temp_end]
                    line = f.readline()
        return self

    def getTranscriptNumber(self):

        return len(self.transcript)

    def getLociNumber(self):

        temp_dic = {}
        for key in self.transcript:
            gid = self.transcript[key]['gid']
            if gid in temp_dic:
                continue
            else:
                temp_dic[gid] = 1
        return len(temp_dic)

    def getLen(self):

        result = Table()
        result.key = "tracking_id"
        result.colNames.append("lenth")
        key_list = self.transcript.keys()
        key_list.sort()
        for key in key_list:
            result.rowNames.append(key)
            temp_len = 0
            for item in self.transcript[key]['exon']:
                temp_len += item[1]-item[0]
            result.data.append([temp_len,])
        return result

    def getExon(self):

        result = Table()
        result.key = 1
        result.col_names.append('tid')
        result.col_names.append('exon_number')
        key_list = self.transcript.keys()
        key_list.sort()
        for key in key_list:
            result.data.append([key,len(self.transcript[key]['exon'])])
            result.row_names[key]=len(result.row_names)
        return result

    def transToBed(self):

        from Bed import Bed
        result = Bed()
        for tid in self.transcript:
            result.transcript[tid] = {}
            result.transcript[tid]['chrom'] = self.transcript[tid]['seqname']
            result.transcript[tid]['chromStart'] = self.transcript[tid]['exon'][0][0]-1
            result.transcript[tid]['chromEnd'] = self.transcript[tid]['exon'][-1][-1]
            if not self.transcript[tid]['score_flag']:
                result.transcript[tid]['score'] = int(0)
            else:
                result.transcript[tid]['score'] = self.transcript[tid]['score']
            if self.transcript[tid]['CDS_flag']:
                result.transcript[tid]['thickStart'] = self.transcript[tid]['CDS'][0]-1
                result.transcript[tid]['thickEnd'] = self.transcript[tid]['CDS'][1]
            else:
                result.transcript[tid]['thickStart'] = self.transcript[tid]['exon'][0][0]-1
                result.transcript[tid]['thickEnd'] = self.transcript[tid]['exon'][-1][-1]
            result.transcript[tid]['strand'] = self.transcript[tid]['strand']
            result.transcript[tid]['itemRgb'] = 0
            result.transcript[tid]['blockCount'] = len(self.transcript[tid]['exon'])
            result.transcript[tid]['blockSizes'] = []
            result.transcript[tid]['blockStarts'] = []
            start_line = self.transcript[tid]['exon'][0][0]
            for each_exon in self.transcript[tid]['exon']:
                length = each_exon[1]-each_exon[0]+1
                start_with = each_exon[0]-start_line
                result.transcript[tid]['blockSizes'].append(length)
                result.transcript[tid]['blockStarts'].append(start_with)
        return result

    def write_to_file(self,filepath):

        f = open(filepath,'w')
        transcript = self.transcript.keys()
        transcript.sort()
        for tid in transcript:
            sequence = 1
            for each_exon in self.transcript[tid]['exon']:
                f.write(self.transcript[tid]['seqname']+'\t')
                f.write(self.transcript[tid]['source']+'\t')
                f.write('exon'+'\t')
                f.write(str(each_exon[0])+'\t')
                f.write(str(each_exon[1])+'\t')
                if self.transcript[tid]['score'] == '.':
                    f.write(self.transcript[tid]['score']+'\t')
                else:
                    f.write(str(self.transcript[tid]['score'])+'\t')
                f.write(self.transcript[tid]['strand']+'\t')
                f.write(str(self.transcript[tid]['frame'])+'\t')
                if self.transcript[tid]['gid'] =='':
                    self.transcript[tid]['gid']=tid
                f.write("gene_id \""+self.transcript[tid]['gid']+"\"; ")
                f.write("transcript_id \""+tid+"\"; ")
                f.write("exon_number \""+str(sequence)+"\"; ")
                if self.transcript[tid]['gname'] != '':
                    f.write("gene_name \""+self.transcript[tid]['gname']+"\"; ")
                f.write('\n')
                sequence += 1
            if self.transcript[tid]['CDS_flag']:
                f.write(self.transcript[tid]['seqname']+'\t')
                f.write(self.transcript[tid]['source']+'\t')
                #f.write(self.transcript[tid]['source']+'\t')
                f.write('CDS'+'\t')
                f.write(str(self.transcript[tid]['CDS'][0])+'\t')
                f.write(str(self.transcript[tid]['CDS'][1])+'\t')
                if self.transcript[tid]['score'] == '.':
                    f.write(self.transcript[tid]['score']+'\t')
                else:
                    f.write(str(self.transcript[tid]['score'])+'\t')
                f.write(self.transcript[tid]['strand']+'\t')
                f.write(str(self.transcript[tid]['frame'])+'\t')
                f.write("gene_id \""+self.transcript[tid]['gid']+"\"; ")
                f.write("transcript_id \""+tid+"\"; ")
                f.write("exon_number \""+str(len(self.transcript[tid]['exon']))+"\"; ")
                if self.transcript[tid]['gname'] != '':
                    f.write("gene_name \""+self.transcript[tid]['gname']+"\"; ")
                f.write('\n')
        f.close()


    def getFasta(self,fasta2bitFile,geneFastaFile,LogDir):
        from Bed import Bed
        selfBed=self.transToBed()
        selfBed.writeToFile(selfGtfFile+'.bed')
        geneFastaFile_tmp=geneFastaFile+'.tmp'
        getFasta_cmd='twoBitToFa -bed='+selfGtfFile+'.bed '+fasta2bitFile+' '+geneFastaFile_tmp
        getFasta_cmd=shlex.split(getFasta_cmd)
        stdoutfile=LogDir+'twoBitToFa.log'
        stderrfile=LogDir+'twoBitToFa.err'
        p = subprocess.call(getFasta_cmd,stdout=open(stdoutfile,'w'),stderr=open(stderrfile,'w'))
        faH=open(geneFastaFile_tmp,"r")
        faOH=open(geneFastaFile,"w")
        seq_str=''
        seqname=''
        for line in faH:
            line=line.strip()
            if line[0]=='>':
                if seq_str!='':
                    print >>faOH,seqname+'\n'+seq_str
                seqname=line
                seq_str=''
            else:
                seq_str+=line
        print >>faOH,seqname+'\n'+seq_str
        faH.close()
        faOH.close()

    def get_tid_gid(self):
        result=Table()
        result.key=1
        result.col_names=['tid','gid']
        for tid in self.transcript:
            gid=self.transcript[tid]['gid']
            row_data=[tid,gid]
            result.row_names[tid]=len(result.row_names)
            result.data.append(row_data)
        return result

    def sub_gtf(self,id_list):
        result=Gtf()
        for id in id_list:
            if self.transcript.has_key(id):
                result.transcript[id]=self.transcript[id]
            else:
                exit("Error: ID: '"+id+"' not fould in gtf")
        return result
    def get_tid(self,gid_list):
        tid_array=[]
        for tid in self.transcript:
            gid=self.transcript[tid]['gid']
            if gid in gid_list:
                tid_array.append(tid)
        return tid_array

    def get_gid(self,tid_list):
        gid_array=[]
        for tid in tid_list:
            if tid in self.transcript:
                gid=self.transcript[tid]['gid']
                gid_array.append(gid)
        return gid_array

    def getGid(self,tid):
        if tid in self.transcript:
            return self.transcript[tid]['gid']

    def getTid(self,gid):
        tid_array=[]
        for tid in self.transcript:
            if gid == self.transcript[tid]['gid']:
                tid_array.append(tid)
        return tid_array



