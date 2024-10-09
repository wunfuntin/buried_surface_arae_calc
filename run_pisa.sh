#!/bin/zsh

# Gain access to PISA and required packages
source /Applications/ccp4-8.0/bin/ccp4.setup-sh

# Create variable from passed arguments
file_name=$1

# Create variable from passed arguments but without the file extension
file_name_no_ext=${file_name%.pdb}

echo "File name: ${file_name}"
echo "File name without extension: ${file_name_no_ext}"


/Applications/ccp4-8.0/bin/pisa design -analyse /Users/rwalker/Documents/TT_lab/python/buried_surface_area_2/"$file_name" /Applications/ccp4-8.0/share/pisa/pisa.cfg
echo "Analysis complete."
/Applications/ccp4-8.0/bin/pisa design -xml interfaces > "${file_name_no_ext}"_out.xml

