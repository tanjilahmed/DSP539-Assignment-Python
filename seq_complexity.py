import sys
import pandas as pd
import os
import matplotlib.pyplot as plt

class Seq(object):
    def __init__ (self,sequence):
        self.sequence=sequence
    def count_kmers(self,k,counters):
        seq1=self.sequence
        for i in range(len(seq1) - k + 1):
            kmer=seq1[i:i+k]
            if not kmer in counters:
                counters[kmer]=0
            counters[kmer]+=1
    def pdf(self,ksize,observed_kmer,possible_kmer,df):
        global row
        proportion=observed_kmer/possible_kmer
        df[row]=[ksize,observed_kmer,possible_kmer,proportion]
        row=row+1
    def plot(self,df,fname):
        print(df)
        plt.plot(df['ksize'],df['Observed_proportion'])
        plt.xlabel('Kmer Size')
        plt.ylabel('Proportion of observed Kmer')
        plt.title(fname)
        gname=fname+".png"
        dir = os.getcwd()
        plotfolder='\\Plot'
        path=dir+plotfolder
        if not os.path.exists(path):
            os.makedirs(path)
        gname=os.path.join(path,gname)
        plt.savefig(gname)
        #plt.show()
        #print(df['ksize'])
    def ling_complexity(self,val1,val2):
        complexity=val1/val2
        return complexity


f = open(sys.argv[1],"r")
fasta = f.readlines()
lc=pd.DataFrame()
row_lc=0
dir = os.getcwd()
dffolder='\\Panda DataFrame'
lcfolder='\\Linguistic Complexity'
plotfolder='Plot'
for line_number,line in enumerate(fasta):
    if line_number%3==0:
        fname=line.strip('>')
        fname=fname.strip('\n')
        print(fname)
    if line_number%3==1:
        row=0
        df=pd.DataFrame()
        sequence=line.rstrip()
        print(sequence)
        seq=Seq(sequence)
        for j in range(1,len(sequence)+1):
            counters={}
            seq.count_kmers(j,counters)
            observed_kmer=len(counters)
            if j==1:
                possible_kmer=4**j
            else:
                possible_kmer=len(sequence)-j+1
            seq.pdf(j,observed_kmer,possible_kmer,df)
            #print(row)

        #print(counters)
        #seq.pdf()
        df=df.T
        df.columns=['ksize','observed_kmers','possible_kmers','Observed_proportion']
        filename=fname+".txt"
        #dir1 = os.path.join(dir,dffolder)
        #print(dir1)
        dfpath=dir+dffolder
        if not os.path.exists(dfpath):
            os.makedirs(dfpath)
        filename=os.path.join(dfpath,filename)
        df.to_csv(filename, index=False, sep=' ', header=True)
        #print(df)
        column1_sum=df['observed_kmers'].sum()
        column2_sum=df['possible_kmers'].sum()
        print(column1_sum)
        print(column2_sum)
        seq.plot(df,fname)
        lcomplexity=seq.ling_complexity(column1_sum,column2_sum)
        lc[row_lc]=[fname,lcomplexity]
        row_lc=row_lc+1
lc=lc.T
lc.columns=['Species','Linguistic Complexity']
lcpath=dir+lcfolder
if not os.path.exists(lcpath):
    os.makedirs(lcpath)
lcfile=os.path.join(lcpath,"linguistic_complexity.txt")
lc.to_csv(lcfile, index=False, sep=' ', header=True)
