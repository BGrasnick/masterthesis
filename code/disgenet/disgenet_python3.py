# Copyright [2010-2017] Integrative Biomedical Informatics Group, Research Programme on Biomedical Informatics (GRIB) IMIM-UPF 
# http://ibi.imim.es/
# contact for technical questions support@disgenet.org
# creator: janet.pinero@upf.edu  
# Script to query disgenet using a list of genes or diseases
# requires as input the gene or disease list in a file 
# the output file name
# the type of entity (gene or disease)
# the type of identifier 
###############################################################################

import argparse
import urllib.request, urllib.error, urllib.parse

def main(infile, outfile, entity, identifier):
    fi = open(infile, "r")
    ent = entity
    id = identifier
   
    STR = "" 
    if ent == "gene" :
         if id == "hgnc":
            STR = "c2.symbol = '"
         elif id == "entrez":
            STR = "c2.geneId = '"
         else: 
            print ("the type of identifier must be entrez gene identifiers or gene symbols \n")
    elif ent == "disease" :
        if id == "cui":
            STR = "c1.diseaseId = '"
        elif id == "mesh":
            STR = "c1.MESH = '"
        elif id == "omim":
            STR = "c1.OMIM = '"
        else: 
            print ("the type of identifier must be cui or mesh or omim identifiers\n")
    else: 
        print ("the type of entity must be disease or gene \n")
 
    for line in fi:
        intfield = line.strip() 
        fo = open(outfile + "_" + intfield + ".tsv", "w") 
        fo.write('c1.diseaseId\tc1.name\tc1.diseaseClassName\tc1.STY\tc1.MESH\tc1.OMIM\tc1.type\tc2.geneId\tc2.symbol\tc2.uniprotId\tc2.description\tc2.pantherName\tc0.score\tc0.EI\tc0.Npmids\tc0.Nsnps\n')
        str = "";
        MSG = "" 
        seq1 = ("querying entity :  ", intfield, "  " )
        MSG = str.join( seq1 );
        print (MSG)       

        seq = ( """
        DEFINE
            c0='/data/gene_disease_summary',
    c1='/data/diseases',
    c2='/data/genes',
    c4='/data/sources'
        ON
           'http://www.disgenet.org/web/DisGeNET'
        SELECT
            c1 (diseaseId, name, diseaseClassName, STY, MESH, OMIM, type ),
    c2 (geneId, symbol,   uniprotId, description, pantherName ),
    c0 (score, EI, Npmids, Nsnps)
           
        FROM
            c0
        WHERE
            (
                """ + STR +  intfield+"""'
            AND
                c4 = 'ALL'
            )
        ORDER BY
            c0.score DESC""" ); #

        binary_data = seq.encode("utf-8")

        req = urllib.request.Request("http://www.disgenet.org/oql")
        res = urllib.request.urlopen(req, binary_data)

        data  = res.read().decode("utf-8")
        res.close()
        nres = len(data.splitlines())

        if nres == 1: 
            MSG = "" 
            seq1 = (entity, " " , intfield, " is not in DisGeNET \n " )
            MSG = str.join( seq1 );
            print (MSG)
        else:
            lista = data.splitlines()
            lista = lista[1:]
            for i in lista:
              fo.write(i+'\n')
        fo.close()

    fi.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("infile", metavar="input-file",help="input file")
    parser.add_argument("outfile", metavar="output-file",help="output file")
    parser.add_argument("entity", metavar="entity",help="type of entity: gene or disease")
    parser.add_argument("identifier", metavar="identifier",help="identifier type: \n genes:  hgnc or entrez \n diseases: cui, mesh or omim ")

    args = parser.parse_args()

    main(args.infile, args.outfile, args.entity, args.identifier)
