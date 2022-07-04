#!/bin/bash

while IFS="," read -r Name	GC	Created_Date	Description	Imported_From_Filename	Imported_From_Path	Modified	Molecular_Weight_kDa	Molecule_Type	Rough_Temperature	Sequence	Sequence_Length	Sequence_List_Name	Size	Topology	URN

do
    IFS="." read -r -a array <<< "$Name"
    echo "${array[0]}"
    curl --silent "http://h-invitational.jp/hinv/spsoup/transcript_view?hit_id=${array[0]}&status=disease" | grep -Po "Disease name"
done < test.csv
