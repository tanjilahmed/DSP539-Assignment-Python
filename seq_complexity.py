#!/usr/bin/python
#title           :seq_complexity.py
#description     :This will calculate linguistic complexity a DNA sequences in a file.
#author          :Tanjil Ahmed
#date            :05/08/2018
#version         :1.0
#usage           :python seq_complexity.py <filename.fasta>
#==============================================================================
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
        return counters
    def pdf(self,ksize,observed_kmer,possible_kmer,df):
        global row
        proportion=observed_kmer/possible_kmer
        df[row]=[ksize,observed_kmer,possible_kmer,proportion]
        row=row+1
    def plot(self,df,fname):
        #print(df)
        plt.plot(df['ksize'][1:50],df['Observed_proportion'][1:50])
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
        plt.text(15,.1,'Propotion of observed kmer is 1 for kmer size>10')
        plt.savefig(gname)
        plt.clf()

    def ling_complexity(self,df):
        column1_sum=df['observed_kmers'].sum()
        column2_sum=df['possible_kmers'].sum()
        complexity=column1_sum/column2_sum
        return complexity



def file_format_check(fasta):
        string="ACTGRYM"
        for line_number,line in enumerate(fasta):
            if line_number%3==1:
                sequence=line.rstrip()
                if any(c not in string for c in sequence):
                    return 0
        return 1


if __name__=="__main__":
    if len(sys.argv) == 1:
        f=open("nd2.fasta","r")
    else:
        f = open(sys.argv[1],"r")
    fasta = f.readlines()
    lc=pd.DataFrame()
    row_lc=0
    dir = os.getcwd()
    dffolder='\\Panda DataFrame'
    lcfolder='\\Linguistic Complexity'
    plotfolder='\\Plot'
    if file_format_check(fasta)==True:
        print("File contains appropriate character")
        for line_number,line in enumerate(fasta):
            if line_number%3==0:
                fname=line.strip('>')
                fname=fname.strip('\n')
                print(fname)
            if line_number%3==1:
                row=0
                df=pd.DataFrame()
                sequence=line.rstrip()
                sequence=sequence.replace("R","A")
                sequence=sequence.replace("Y","T")
                sequence=sequence.replace("M","C")
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

                df=df.T
                df.columns=['ksize','observed_kmers','possible_kmers','Observed_proportion']
                filename=fname+".txt"
                dfpath=dir+dffolder
                if not os.path.exists(dfpath):
                    os.makedirs(dfpath)
                filename=os.path.join(dfpath,filename)
                df.to_csv(filename, index=False, sep=' ', header=True)
                seq.plot(df,fname)
                lcomplexity=seq.ling_complexity(df)
                lc[row_lc]=[fname,lcomplexity]
                row_lc=row_lc+1
        lc=lc.T
        lc.columns=['Species','Linguistic Complexity']
        lcpath=dir+lcfolder
        if not os.path.exists(lcpath):
            os.makedirs(lcpath)
        lcfile=os.path.join(lcpath,"linguistic_complexity.txt")
        lc.to_csv(lcfile, index=False, sep=' ', header=True)
    else:
        print ("File doesn't contain appropriate base")
