# PAGE-pretty_download_GEOS
Pretty Appearance Good Experience (PAGE), a python script downloading GEOS from NCBI with pretty appearance in terminal

# Example
## Prepare GEO sources
### GEOsources_sample.txt
Text contains two columns: file_name file_link
GSM7051124_DNA-100C-BS1.CpG.bw	https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSM7051124&format=file&file=GSM7051124%5FDNA%2D100C%2DBS1%2ECpG%2Ebw

## Run script
### Terminal arguments
pretty_download_geos.py requires an <i>input</i> argument, such as GEOsources_sample.txt.

### Run
Open Terminal in the same folder as the script file, or open Terminal and go to the folder where the script is located

python pretty_download_geos.py -i ./GEOsources_sample.txt
