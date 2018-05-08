from seq_complexity import file_format_check
from seq_complexity import Seq
import pytest
@pytest.fixture
def fasta():
    #f = open(sys.argv[1],"r")
    f=open('nd3-temp.fasta',"r")
    fasta = f.readlines()
    print("OK")
    return fasta


def test_file_is_Empty(fasta):
    for line in fasta:
        assert line == '\n', "Empty File"


def test_file_format_check(fasta):
    assert file_format_check(fasta) ==True, 'File Not OK'

    for line_number,line in enumerate(fasta):
        if line_number%3==1:
            sequence=line.rstrip()
            for c in sequence:
                assert c in string, 'Sequence must contain only A,C,T,G,R,Y,M'

def test_count_kmers(fasta):
    for line_number,line in enumerate(fasta):
        if line_number%3==1:
            row=0
            df=pd.DataFrame()
            sequence=line.rstrip()
            sequence=sequence.replace("R","A")
            sequence=sequence.replace("Y","T")
            sequence=sequence.replace("M","C")
            seq=Seq(sequence)
            counters={}
            assert len(seq.count_kmers(1,counters))>0
     #        	counter=count_kmers(4,fastq,{})
     #        	assert len(counter)==256
     #        for j in range(1,len(sequence)+1):
     #            counters={}
     #            seq.count_kmers(j,counters)
     #            observed_kmer=len(counters)
     #            if j==1:
     #                possible_kmer=4**j
     #            else:
     #                possible_kmer=len(sequence)-j+1
     #            seq.pdf(j,observed_kmer,possible_kmer,df)
     #            #print(row)
     # return 1

# def test_pdf():
#     return 1
#
# def test_plot():
#     return 1
