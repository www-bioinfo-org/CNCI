'''
created on 2014-2-18

@author: Dechao Bu(dechao.bu@qq.com)
'''

import copy
import re
import itertools
from sets import Set

def sub_array(A,B):
    x=Set(A)
    y=Set(B)
    return list(x - y)

def intersect_array(A,B):
    x=Set(A)
    y=Set(B)
    return list(x & y)


def union_array(A,B):
    x=Set(A)
    y=Set(B)
    return list(x | y)

def de_redundency(A):
    return list(Set(A))

def io(join,a,b):
    X=[]
    if len(a) != len(b):
        exit("length is not equal, intersect operation quit")
    for index in range(len(a)):
        if join == 'intersect':
            bool_x = a[index] and b[index]
        elif join == 'union':
            bool_x = a[index] or b[index]
        else:
            exit("join could only be intersect/union")
        X.append(bool_x)
    return X

def gets(A,cols):
    result=[]
    for col in cols:
        result.append(get(A,col))
    return result

def get(A,col):
    if isinstance(col,int):
        return A[col-1]
    elif isinstance(col,str):
        if col in A:
            return col
        else:
            exit("Col:'" + col + "' not found!")
    else:
        exit("Unkown type of '"+col+"'")


def split_array(A,index,sign):
    B=[]
    for i in range(len(A)):
        if i == index:
            B.extend(A[index].split(sign))
        else:
            B.append(A[i])
    return B

def disabond_array(A,index,sign):
    B=[]
    abondoned_terms=A[index].split(sign)
    pre=A[0:index]
    post=A[index+1:]
    for i in abondoned_terms:
        C=[]
        C.extend(pre)
        C.append(i)
        C.extend(post)
        B.append(C)
    return B



class Table(object):

    '''
    Build a class contains all the data in the specified file(a table)
    with two vectors which contains the row and column data
    and one two-dimensional array contains the value of the table

    Offer n methods:
        Table.showData(self)
        Table.set(self,rownames,colnames,data)
        Table.get(self, row, col)
        Table.getRow(self, augment)
        Table.getCol(self, augment)
        Table.leftJoin(self, Table_O)
        Table.innerJoin(self, Table_O)
        Table.sub(self, Table_O)
        Table.paste(List)
        Table.writeToFile(self, filePath)

    .__doc__ the method to get more information
    '''


    def __init__(self,*args):



        '''
        Initialize the class depends on the filepath inputed
        without input will initialize an empty instance
        Example:
            A = Table()
            B = Table(filepath)
            C = Table(filepath,key_index,True/False)
            Note: key_index could be 0~N, 0 for no key column defined
        '''

        self.row_names = {}
        self.col_names= []
        self.data = []
        self.key=0
        header=False
        if len(args) == 0:
            return
        elif len(args) == 1:
            path = args[0]
        elif len(args) == 3:
            path = args[0]
            self.key = args[1]
            header=args[2]
        f = open(path,'r')
        if header:
            lable = f.readline()
            lable = lable.rstrip("\n")
            self.col_names = lable.split("\t")
        line=f.readline()
        while line:
            line = line.rstrip("\n")
            row_data = line.split("\t")
            self.data.append(row_data)
            if self.key > 0 :
                row_index = row_data[self.key-1]
                self.row_names[row_index]=len(self.row_names)
            line=f.readline()

    @staticmethod
    def build_table(key,col_names,data):
        result=Table()
        result.key=key
        result.col_names=col_names
        if isinstance(data,list):
            for row_data in data:
                if not isinstance(row_data,list):
                    row_data=[row_data]
                result.data.append(row_data)
                if result.key > 0:
                    result.row_names[row_data[result.key-1]]=len(result.row_names)
        else:
            exit('Error: Data should be list!')
        return result

    def show_data(self):

        '''
        Print all data of the table
        Example:
            A = Table(filepath)
            A.show_data()
        '''

        line_out = ""
        if self.col_names:
            for i in self.col_names:
                line_out = line_out + str(i)+'\t'
            line_out = line_out[0:len(line_out)-1]
            print line_out
        for row_data in self.data:
            line_out = ""
            for j in row_data:
                line_out = line_out + str(j)+"\t"
            line_out = line_out[0:len(line_out)-1]
            print line_out


    def set(self,*argument):

        '''
        Fill a vacancy table with four arguments
        Example:
            A = Table()
            A.set(key_index,row_names,col_names,data)
        '''

        if self.key!=0:
            print "Warning:The table has been initialized. "
        if len(argument) ==4:
            valid = True
            if len(argument[1]) == len(argument[3]):
                for each_row in argument[3]:
                    if len(each_row) == len(argument[2]):
                        continue
                    else:
                        valid = False
            else:
                valid = False
            if valid:
                self.key = int(argument[0])
                self.row_names = argument[1]
                self.col_names = argument[2]
                self.data = argument[3]
            else:
                exit("Error:The given three lists should be formated")
        else:
            exit("Error:There should be three lists")

    def set_colnames(self,*argument):

        '''
        Undate column names of the table
        Example:
            A = Table()
            A.set_colnames(col_names)
        '''

        if len(self.col_names) != 0:
            len_colnames=len(self.col_names)
        if len(argument) != len_colnames:
            exit("Error : Lenth of the input array is wrong. Can't update the coloumn names!")
        else:
            self.col_names=[]
            for item in argument:
                self.col_names.append(item)
            return self

    def get(self,row,col):

        '''
        Get the specified Value depends on the given augument:row and column
        Both index and name of row and column is accepted
        Example:
            A = Table(filepath)
            A.get("rowname","colname")
            A.get(3,4)
        '''

        result=self.get_row(row).get_col(col)
        return result.data[0][0]

    def getRowIndex(self,row_input):
        if isinstance(row_input,str):
            if self.key < 1:
                print "Error:Key col is not defined, try get_row(row_index)"
                exit()
            else:
                if self.row_names.has_key(row_input):
                    index=self.row_names[row_input]
                else:
                    print "Error: input row '"+ row_input +"' can not be fetched"
                    exit()
        else:
            index = int(row_input)-1
        row_number=index+1
        return row_number

    def get_row_index(self,*rows):
        result=[]
        for row in rows:
            result.append(self.getRowIndex(row))
        return result

    def getRow(self,row_input):

        '''
        Get the specified Row
        Both index and name of row is accepted
        Example:
            A = Table(filepath)
            A.getRow("name")
            A.getRow(3)
        '''

        return self.data[self.getRowIndex(row_input)-1]

    def get_row(self,*rows):

        '''
        Get a table from the original instance
        depends on the given rows/index
        Example:
            A = Table(filepath)
            B = A.getRow(1,2,3,"row_name")
        '''

        result = Table()
        result.key = self.key
        result.col_names=copy.copy(self.col_names)
        for row_input in rows:
            row_data=self.getRow(row_input)
            if self.row_names:
                result.row_names[row_data[self.key-1]]=len(result.row_names)
            result.data.append(row_data)
        return result

    def get_row_by_func(self,f):

        '''
        Get a table from the original instance
        depends on the given rows/index
        Example:
            A = Table(filepath)
            B = A.getRow(1,2,3,"row_name")
        '''

        result = Table()
        result.key = self.key
        result.col_names=copy.copy(self.col_names)
        for row_data in self.data:
            if f(row_data):
                if result.key>1:
                    result.row_names[row_data[self.key-1]]=len(result.row_names)
                result.data.append(row_data)
        return result

    def getColIndex(self,col_input):
        if isinstance(col_input,str):
            if self.col_names  and (col_input in self.col_names):
                the_number = self.col_names.index(col_input)
            else:
                print "Error: Column '"+ col_input + "' can not be fetched!"
                exit()
        else:
            the_number = int(col_input)-1
        col_number=the_number+1
        return col_number

    def get_col_index(self,*cols):
        result=[]
        for col in cols:
            result.append(self.getColIndex(col))
        return result

    def getCol(self,col_input):

        '''
        Get the specified Col
        Both index and name of column is accepted
        Example:
            A = Table(filepath)
            A.getCol("name")
            A.getCol(3)
        '''

        tempCol=[]
        the_number = self.getColIndex(col_input)-1
        for i in self.data:
            tempCol.append(i[the_number])
        return tempCol

    def get_col(self,*cols):

        '''
        Get a table from the original instance
        depends on the given columns/column_index
        Example:
            A = Table(filepath)
            B = A.getCol(1,2,3,"col_name")
        '''

        result = Table()
        if self.key > 0:
            if self.key in cols:
                result.key = cols.index(self.key)+1
            elif self.col_names and self.col_names[self.key-1] in cols:
                result.key = cols.index(self.col_names[self.key-1])+1
        result.row_names=self.row_names.copy()
        data=[]
        for col_input in cols:
            col_data=self.getCol(col_input)
            if self.col_names:
                if isinstance(col_input,str):
                    result.col_names.append(col_input)
                elif isinstance(col_input,int):
                    result.col_names.append(self.col_names[int(col_input)-1])
            data.append(col_data)
        row_length=len(data[0])
        for i in range(row_length):
            row_tmp=[]
            for col in data:
                row_tmp.append(col[i])
            result.data.append(row_tmp)
        return result

    def update_row(self,row_input,new_value):

        '''
        Undate one column of a table to the new_value,  the new_value can be constant or list
        Example:
            A = Table(filepath)
            A.update_row(2,[1,2,3])
            A.update_row(2,3)
            A.update_row('row_name',3)
        '''

        if isinstance(row_input,str):
            if self.row_names  and (row_input in self.row_names):
                the_number = self.row_names[row_input]
            else:
                exit("Error: Column '"+ row_input + "' can not be fetched!")
        else:
            the_number = int(row_input)-1
        if isinstance(new_value,list):
            self.data[the_number]=new_value
        else:
            col_number=len(self.data[the_number])
            self.data[the_number]=[new_value]*col_number
        return self

    def update_col(self,col_input,new_value):

        '''
        Undate one column of a table to the new_value,  the new_value can be constant or list
        Example:
            A = Table(filepath)
            A.update_col(2,[1,2,3])
            A.update_col(2,3)
            A.update_col('col_name',3)
        '''

        if isinstance(col_input,str):
            if self.col_names  and (col_input in self.col_names):
                the_number = self.col_names.index(col_input)
            else:
                exit("Error: Column '"+ col_input + "' can not be fetched!")
        else:
            the_number = int(col_input)-1
        if isinstance(new_value,list):
            len_origin=len(self.data)
            len_new_value=len(new_value)
            if len_origin != len_new_value:
                exit("Error: the column '"+col+"' can not be updated for wrong new values provided ")
            for index in range(len_origin):
                self.data[index][the_number]=new_value[index]
        else:
            for index in range(len(self.data)):
                self.data[index][the_number]=new_value
        return self

    def insert_row(self,row_index,new_value):

        '''
        Insert a new row at the row_index, with input new_value
        Example:
            A = Table(filepath)
            A.insert_row(2,[1,2,3])
            A.insert_row(2,3)
            A.insert_row('col_name',3)
        '''

        if isinstance(row_index,str):
            if self.row_names  and (row_index in self.row_names):
                the_number = self.row_names[row_index]
            else:
                exit("Error: Column '"+ row_index + "' can not be fetched!")
        else:
            the_number = int(row_index)-1+1
        if isinstance(new_value,list):
            self.data.insert(the_number,new_value)
        else:
            col_number=len(self.data[the_number])
            new_value=[new_value]*col_number
            self.data.insert(the_number,new_value)

        if self.row_names and self.key>0:
            for key in self.row_names.keys():
                if self.row_names[key] >= the_number:
                    self.row_names[key]=self.row_names[key]+1
            self.row_names[new_value[self.key-1]]=the_number
        return self

    def insert_row_by_func(self,row_input,f):
        self.insert_row(row_input,self.cal(f,'row'))
        return self

    def append_row(self,value):
        total_row=len(self.data)
        self.insert_row(total_row,value)
        return self

    def append_row_by_func(self,f):
        total_row=len(self.data)
        self.insert_row_by_func(total_row,f)
        return self

    def insert_col(self,col_input,col_name,new_value):
        if isinstance(col_input,str):
            if self.col_names  and (col_input in self.col_names):
                the_number = self.col_names.index(col_input)
            else:
                print "Error: Column '"+ col_input + "' can not be fetched!"
                exit()
        else:
            the_number = int(col_input)-1+1 ## insert after the col_input
        if isinstance(new_value,list):
            len_origin=len(self.data)
            len_new_value=len(new_value)
            if len_origin != len_new_value:
                exit("Error: the column '"+col+"' can not be updated for wrong new values provided ")
            for index in range(len_origin):
                self.data[index].insert(the_number,new_value[index])
        else:
            for index in range(len(self.data)):
                self.data[index].insert(the_number,new_value)
        if self.col_names:
            self.col_names.insert(the_number,col_name)
        return self

    def insert_col_by_func(self,col_input,col_name,f):
        self.insert_col(col_input,col_name,self.cal(f,'row'))
        return self

    def append_col(self,col_name,value):
        total_col=len(self.data[0])
        self.insert_col(total_col,col_name,value)
        return self

    def append_col_by_func(self,col_name,f):
        total_col=len(self.data[0])
        self.insert_col_by_func(total_col,col_name,f)
        return self


    def de_redundency(self,*args):
        if self.key >=1:
            print("Key has been defined, the table should be uniq")
            return self
        result=Table()
        result.col_names=copy.copy(self.col_names)
        result.key=self.key
        item_hash={}
        for i in self.data:
            if len(args)==0:
                item=":".join(i)
            else:
                cols=self.get_col_index(*args)
                item=":".join(gets(i,cols))
            if item not in item_hash:
                item_hash[item]=1
                result.data.append(i)
        return result


    def eget(self,join,*args):
        if len(args) < 1:
            print("Waring:No regex is provided ")
            return self
        result=Table()
        result.key=self.key
        result.col_names=copy.copy(self.col_names)
        if join == "intersect":
            kept = [True] * len(self.data)
        else:
            kept = [False] * len(self.data)
        regex="!~|~|!=|="
        for arg in args:
            m = re.search(regex,arg)
            if m:
                col=arg[0:m.start()]
                oper=arg[m.start():m.end()]
                value=arg[m.end():]
                kept_col=self.__echeck(col,oper,value)
                if join == "intersect":
                    kept = io('intersect',kept,kept_col)
                elif join == "union":
                    kept = io('union',kept,kept_col)
                else:
                    exit("Join is intersect or union!")
            else:
                exit("Regex: '" + arg + "'could not be resolved")
        for index in range(len(kept)):
            kept_bool=kept[index]
            if kept_bool:
                result.data.append(self.data[index])
                if result.key > 0:
                    result.row_names[result.key-1]=len(result.row_names)
        return result

    def __echeck(self,col,oper,value):
        kept_col = [False] * len(self.data)
        if col.startswith("_"):
            col=col.lstrip("_")
            if self.col_names and (col in self.col_names):
                index=self.col_names.index(col)
            else:
                exit("col: '"+col+"' could not be fetched!")
        elif isinstance(int(col),int):
            index=int(col)-1
        else:
            exit("col: '" + col + "' format error")
        for row_index in range(len(self.data)):
            row_data=self.data[row_index]
            if oper == "=":
                kept_col[row_index] = (row_data[index] == value and True) or False
            elif oper == "!=":
                kept_col[row_index] = (row_data[index] != value and True) or False
            elif oper == "~":
                kept_col[row_index] = (value in row_data[index] and True) or False
            elif oper == "!~":
                kept_col[row_index] = (value not in row_data[index] == value and True) or False
            else:
                exit("Error: operator'" + oper + "' is not defined!")
        return kept_col

    def x_cat(self,Table_o):
        result=Table()
        result.key=self.key
        result.row_names=self.row_names.copy()
        result.col_names=copy.copy(self.col_names)
        result.data=copy.copy(self.data)
        if result.key > 0 and Table_o.key > 0:
            for key_term in Table_o.row_names.keys:
                result.row_names[key_term]=len(result.row_names)
                result.data.append(Table_o.getRow(key_term))
        else:
            for data in Table_o.data:
                result.data.append(data)
        return result

    def y_cat(self,Table_o):
        result=Table()
        result.key=self.key
        if result.col_names and Table_o.col_names:
            result.col_names=copy.copy(self.col_names).extend(Table_o.col_names)
        result.row_names=self.row_names.copy()
        for index in range(len(self.data)):
            A=self.data[index]
            B=Table_o.data[index]
            result.data.append(copy.copy(A).extend(copy.copy(B)))
        return result

    def group_by(self,id_cols,value_cols):
        result=Table()
        if not isinstance(id_cols,list):
            id_cols=[id_cols]
        if not isinstance(value_cols,list):
            value_cols=[value_cols]
        id_cols=self.get_col_index(*id_cols)
        value_cols=self.get_col_index(*value_cols)
        if len(id_cols) == 1:
            result.key=int(id_cols[0])-1
        if self.col_names:
            result.col_names.extend(gets(self.col_names,id_cols))
            result.col_names.extend(gets(self.col_names,value_cols))
        data=copy.copy(self.data)
        keyfunc = lambda t: (gets(t,id_cols))
        data.sort(key=keyfunc)
        for key, rows in itertools.groupby(data, keyfunc):
            row_data=[]
            row_data.extend(key)
            group_data=[]
            for r in rows:
                group_data.append(r)
            for v in value_cols:
                group_out=(','.join(str(g[v-1]) for g in group_data))
                row_data.append(group_out)
            result.data.append(row_data)
            if result.key > 0 and len(key) == 1:
                result.row_names[key[0]]=len(result.row_names)
        return result

    def group_by_func(self,id_cols,value_cols,f):
        result=Table()
        if not isinstance(id_cols,list):
            id_cols=[id_cols]
        if not isinstance(value_cols,list):
            value_cols=[value_cols]
        if len(id_cols) == 1:
            result.key=int(id_cols[0])-1
        if self.col_names:
            result.col_names.extend(gets(self.col_names,id_cols))
            result.col_names.extend(gets(self.col_names,value_cols))
        data=copy.copy(self.data)
        keyfunc = lambda t: (gets(t,id_cols))
        data.sort(key=keyfunc)
        for key, rows in itertools.groupby(data, keyfunc):
            row_data=[]
            row_data.extend(key)
            group_data=[]
            for r in rows:
                group_data.append(r)
            for v in value_cols:
                data_col=(list)(g[v-1] for g in group_data)
                group_out=f(data_col)
                row_data.append(group_out)
            result.data.append(row_data)
            if result.key > 0 and len(key) == 1:
                result.row_names[key[0]]=len(result.row_names)
        return result

    def key_by(self,id_cols,value_cols):
        result=Table()
        result.key=1
        if not isinstance(id_cols,list):
            id_cols=[id_cols]
        if not isinstance(value_cols,list):
            value_cols=[value_cols]
        id_cols=self.get_col_index(*id_cols)
        value_cols=self.get_col_index(*value_cols)
        if self.col_names:
            result.col_names.append(":".join(gets(self.col_names,id_cols)))
            result.col_names.extend(gets(self.col_names,value_cols))
        data=copy.copy(self.data)
        keyfunc = lambda t: (gets(t,id_cols))
        data.sort(key=keyfunc)
        for key, rows in itertools.groupby(data, keyfunc):
            row_data=[]
            key_new=":".join(key)
            row_data.append(key_new)
            group_data=[]
            for r in rows:
                group_data.append(r)
            for v in value_cols:
                group_out=(','.join(str(g[v-1]) for g in group_data))
                row_data.append(group_out)
            result.data.append(row_data)
            if result.key > 0 :
                result.row_names[key_new]=len(result.row_names)
        return result

    def key_by_func(self,id_cols,value_cols,f):
        result=Table()
        result.key=1
        if not isinstance(id_cols,list):
            id_cols=[id_cols]
        if not (value_cols,list):
            value_cols=[value_cols]
        id_cols=self.get_col_index(*id_cols)
        value_cols=self.get_col_index(*value_cols)
        if self.col_names:
            result.col_names.append(":".join(gets(self.col_names,id_cols)))
            result.col_names.extend(gets(self.col_names,value_cols))
        data=copy.copy(self.data)
        keyfunc = lambda t: (gets(t,id_cols))
        data.sort(key=keyfunc)
        for key, rows in itertools.groupby(data, keyfunc):
            row_data=[]
            key_new=":".join(key)
            row_data.append(key_new)
            group_data=[]
            for r in rows:
                group_data.append(r)
            for v in value_cols:
                data_col=(list)(g[v-1] for g in group_data)
                group_out=f(data_col)
                row_data.append(group_out)
            result.data.append(row_data)
            if result.key > 0 :
                result.row_names[key_new]=len(result.row_names)
        return result

    @staticmethod
    def sub(A,A_key,B,B_key):
        result=Table()
        if not isinstance(A_key,list):
            A_key=[A_key]
        if not isinstance(B_key,list):
            B_key=[B_key]
        A_key=A.get_col_index(*A_key)
        B_key=B.get_col_index(*B_key)
        A_value=sub_array(range(1,len(A.data[0])+1),A_key)
        B_value=sub_array(range(1,len(B.data[0])+1),B_key)
        if len(A_key)==1 and A.key >0 and A.key==A_key[0]:
                if A.key==1:
                    A_group=A
                else:
                    cols_new_order=[]
                    cols_new_order.extend(A_key)
                    cols_new_order.extend(A_value)
                    A_group=A.get_col(*cols_new_order)
        else:
            A_group=A.key_by(A_key,A_value)
        if len(B_key)==1 and B.key >0 and B.key==B_key[0]:
                if B.key==1:
                    B_group=B
                else:
                    cols_new_order=[]
                    cols_new_order.extend(B_key)
                    cols_new_order.extend(B_value)
                    B_group=B.get_col(*cols_new_order)
        else:
            B_group=B.key_by(B_key,B_value)
        result.key=A_group.key
        result.col_names.append(A_group.col_names)
        for a in A_group.row_names.keys():
            if not B_group.row_names.has_key(a):
                row_data=[]
                row_data.extend(A_group.data[A_group.row_names[a]])
                result.data.append(row_data)
                result.row_names[a]=len(result.row_names)
        return result

    def left_join(self,A_key,B,B_key):
        if isinstance(A_key,list):
            if len(A_key) != 1:
                exit("Error: the first table should be leftjoined by one column!")
            else:
                A_key=A_key[0]
        if not isinstance(B_key,list):
            B_key=[B_key]
        B_key=B.get_col_index(*B_key)
        B_value=sub_array(range(1,len(B.data[0])+1),B_key)
        if len(B_key)==1 and B.key >0 and B.key==B_key[0]:
                if B.key==1:
                    B_group=B
                else:
                    cols_new_order=[]
                    cols_new_order.extend(B_key)
                    cols_new_order.extend(B_value)
                    B_group=B.get_col(*cols_new_order)
        else:
            B_group=B.key_by(B_key,B_value)
        querys=self.getCol(A_key)
        for index in range(len(querys)):
            query_item=querys[index]
            B_row=B_group.getRow(query_item)
            for col_index in range(1,len(B_row)):
                self.data[index].append(B_row[col_index])
        if self.col_names:
            if B.col_names:
                for value_index in B_value:
                    self.col_names.append(B.col_names[value_index-1])
            else:
                for value_index in B_value:
                    self.col_names.append("")
        return self


    @staticmethod
    def fuzzy_leftjoin(*args):
        args_len=len(args)
        if args_len < 4 or args_len % 2 != 0:
            exit("Error:paste needs at least two tables, with at least four arguments")
        result=Table()
        result.key=1
        key_array=[]
        key_origin={}
        values=[]
        for index in range(0,args_len,2):
            value_T={}
            A=args[index]
            key_cols=args[index+1]
            if not isinstance(key_cols,list):
                key_cols=[key_cols]
            key_cols=A.get_col_index(*key_cols)
            value_cols=sub_array(range(1,len(A.data[0])+1),key_cols)
            B=A.key_by(key_cols,value_cols)
            if B.col_names:
                if index == 0:
                    result.col_names.extend(B.col_names)
                else:
                    result.col_names.extend(B.col_names[1:])
            else:
                if index == 0:
                    result.col_names.append('Key')
                result.col_names.extend([""]*(len(B.data[0])-1))
            for k in B.row_names.keys():
                KK=str(k).upper()
                key_array.append(KK)
                key_origin[KK]=k
                value_T[KK]=B.data[B.row_names[k]][1:]
            values.append(value_T)
        key_set=list(Set(key_array))
        for s in key_set:
            result.data.append([key_origin[s]])
        for index in range(len(key_set)):
            key=key_set[index]
            for v_hash in values:
                if v_hash.has_key(key):
                    value=v_hash[key]
                    if len(value)!=0:
                        result.data[index].extend(value)
                else:
                    result.data[index].extend([""]*len(v_hash.values()[0]))
            result.row_names[key]=len(result.row_names)
        return result


    @staticmethod
    def paste(*args):
        args_len=len(args)
        if args_len < 4 or args_len % 2 != 0:
            exit("Error:paste needs at least two tables, with at least four arguments")
        result=Table()
        result.key=1
        key_array=[]
        values=[]
        for index in range(0,args_len,2):
            value_T={}
            A=args[index]
            key_cols=args[index+1]
            if isinstance(key_cols,int):
                key_cols=[key_cols]
            value_cols=sub_array(range(1,len(A.data[0])+1),key_cols)
            if len(key_cols)==1 and A.key >0 and A.key==key_cols[0]:
                if A.key==1:
                    B=A
                else:
                    cols_new_order=[]
                    cols_new_order.extend(key_cols)
                    cols_new_order.extend(value_cols)
                    B=A.get_col(*cols_new_order)
            else:
                B=A.key_by(key_cols,value_cols)
            if B.col_names:
                if index == 0:
                    result.col_names.extend(B.col_names)
                else:
                    result.col_names.extend(B.col_names[1:])
            else:
                if index == 0:
                    result.col_names.append('Key')
                result.col_names.extend([""]*(len(B.data[0])-1))
            for k in B.row_names.keys():
                key_array.append(k)
                value_T[k]=B.data[B.row_names[k]][1:]
            values.append(value_T)
        key_set=list(Set(key_array))
        for s in key_set:
            result.data.append([s])
        for index in range(len(key_set)):
            key=key_set[index]
            for v_hash in values:
                if v_hash.has_key(key):
                    value=v_hash[key]
                    if len(value)!=0:
                        result.data[index].extend(value)
                else:
                    result.data[index].extend([""]*len(v_hash.values()[0]))
            result.row_names[key]=len(result.row_names)
        return result

    @staticmethod
    def fuzzy_paste(*args):
        args_len=len(args)
        if args_len < 4 or args_len % 2 != 0:
            exit("Error:paste needs at least two tables, with at least four arguments")
        result=Table()
        result.key=1
        key_array=[]
        key_origin={}
        values=[]
        for index in range(0,args_len,2):
            value_T={}
            A=args[index]
            key_cols=args[index+1]
            if isinstance(key_cols,int):
                key_cols=[key_cols]
            value_cols=sub_array(range(1,len(A.data[0])+1),key_cols)
            if len(key_cols)==1 and A.key >0 and A.key==key_cols[0]:
                if A.key==1:
                    B=A
                else:
                    cols_new_order=[]
                    cols_new_order.extend(key_cols)
                    cols_new_order.extend(value_cols)
                    B=A.get_col(*cols_new_order)
            else:
                B=A.key_by(key_cols,value_cols)
            if B.col_names:
                if index == 0:
                    result.col_names.extend(B.col_names)
                else:
                    result.col_names.extend(B.col_names[1:])
            else:
                if index == 0:
                    result.col_names.append('Key')
                result.col_names.extend([""]*(len(B.data[0])-1))
            for k in B.row_names.keys():
                KK=str(k).upper()
                key_array.append(KK)
                key_origin[KK]=k
                value_T[KK]=B.data[B.row_names[k]][1:]
            values.append(value_T)
        key_set=list(Set(key_array))
        for s in key_set:
            result.data.append([key_origin[s]])
        for index in range(len(key_set)):
            key=key_set[index]
            for v_hash in values:
                if v_hash.has_key(key):
                    value=v_hash[key]
                    if len(value)!=0:
                        result.data[index].extend(value)
                else:
                    result.data[index].extend([""]*len(v_hash.values()[0]))
            result.row_names[key]=len(result.row_names)
        return result

    def concat_col(self,*cols):
        result=Table()
        if self.key > 0:
            if self.key in cols:
                result.key = cols.index(self.key)+1
            elif self.col_names and self.col_names[self.key-1] in cols:
                result.key = cols.index(self.col_names[self.key-1])+1
        result.row_names=self.row_names.copy()
        data=[]
        for col_input in cols:
            col_data=self.getCol(col_input)
            if self.col_names:
                if isinstance(col_input,str):
                    result.col_names.append(col_input)
                elif isinstance(col_input,int):
                    result.col_names.append(self.col_names[int(col_input)-1])
            data.append(col_data)
        row_length=len(data[0])
        for i in range(row_length):
            row_tmp=[]
            for col in data:
                row_tmp.append(col[i])
            result.data.append(row_tmp)
        return result

    def split_col(self,col,sign):
        result=Table()
        if col!=self.key:
            result.key=self.key
        else:
            result.key=0
        if self.col_names:
            result.col_names=split_array(self.col_names,col-1,sign)
        result.row_names=self.row_names.copy()
        for row_data in self.data:
            result.data.append(split_array(row_data,col-1,sign))
        return result

    def disabond_col(self,col,sign):
        result=Table()
        result.col_names=copy.copy(self.col_names)
        for row_data in self.data:
            for disabonded in disabond_array(row_data,col-1,sign):
                result.data.append(disabonded)
                if result.key > 0:
                    result.row_names[disabonded[result.key-1]]=len(result.row_names)
        return result

    def cal(self,f,flag):
        result=[]
        if flag=='row':
            for data in self.data:
                result.append(f(data))
        elif flag=='col':
            for index in range(len(self.data[0])):
                data=self.getCol(index)
                result.append(f(data))
        else:
            exit("Error: the flag should only be row or col!")
        return result


    def transpose(self):
        result=Table()
        if self.col_names:
            for index in range(len(self.col_names)):
                result.data.append(self.col_names[index])
            for row_data in self.data:
                for item_index in range(len(row_data)):
                   result.data[item_index].append(row_data[index])
        else:
            for index in range(len(self.col_names)):
                result.data.append([])
            for row_data in self.data:
                for item_index in range(len(row_data)):
                    result.data[item_index].append(row_data[index])
        return result

    def write_to_file(self,file_path):

        '''
        Output the table to specified path with given name
        Example:
            A = Table(filepath_A)
            A.writeToFile(filepath_B)
        '''

        f = open(file_path,"w")
        if self.col_names:
            line_out = ""
            for i in self.col_names:
                line_out = line_out + str(i)+'\t'
            line_out = line_out[0:len(line_out)-1]
            f.write(line_out + "\n")
        for row_data in self.data:
            line_out = ""
            for j in row_data:
                line_out = line_out + str(j)+"\t"
            line_out = line_out[0:len(line_out)-1]
            f.write(line_out + "\n")
        f.close()