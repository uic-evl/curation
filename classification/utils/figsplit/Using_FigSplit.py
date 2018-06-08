'''
----------------------------------------------------------------------
This code is created for helping users use FigSplit automatically.

To run this code, you can put all images in the input folder. For each image,
segmented panels with their coordinates will be found in the output folder as a
zip file.

Input_path: The path of the folder containing all images that you want to split
Output_path: The path of the folder that will contain all downloaded zip files

You can also change the input path and the output path for your usage.
----------------------------------------------------------------------
Written by Pengyuan LI
Contact: pengyuan@udel.edu
11/14/2017
Modified on 05/28/2018
'''

import os
import requests
from urllib import urlretrieve

input_path = './input'
# Input path
output_path = './output'
# Output path

# Check input and output path
try:
    os.stat(input_path)
except:
    print 'please check your input folder'

try:
    os.stat(output_path)
except:
    print 'please check your input folder'

# Create a Log file to record all exceptions
log_path = os.path.join(input_path, 'FigSplit.log')
logfile = open(log_path, "w")
print 'Log file Gernerated \n'

# Read all images in the input folder
images = os.listdir(input_path)
# For each image send the request to the FigSplit
for image in images:
    # Check the suffix of each file
    if image.endswith((".jpg", ".png", ".jpeg", "bmp", "tif", ".tif")):
        print image
        try:
            # Send the request to FigSplit
            # Questions about Request can be found at http://docs.python-requests.org/en/master/
            # !!!!!  Change the URL HERE !!!!!
            r = requests.post(
                'https://www.eecis.udel.edu/~compbio/FigSplit/modified_uploader', files={
                'file': open(os.path.join(input_path, image), 'rb')})
            if r.status_code == 200:
                print 'Done\n'
                html = r.text.split("\n")
                for line in html:
                    # !!!!!  Change the URL HERE !!!!!
                    if 'download' in line and 'https://www.eecis.udel.edu/~compbio/FigSplit' in line:
                        link_of_zip = line.split('href="')[1].split('" download')[0]
                        # Download the zip file which contains the segmented panels and their coordinates
                        urlretrieve(link_of_zip, os.path.join(output_path,
                                                              image+'.zip'))

            else:
                # Problem occurred in the Request
                print 'Problem occurred\n'
                logfile.write(image + '    Problem occurred\n')
        except:
            # Any other problem occurred
            print 'This program cannot work for' + image + '\n'
            print 'Unexpected error:', sys.exc_info()[0]
            logfile.write(str(sys.exc_info()[0]))

logfile.close()
