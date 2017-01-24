# The MIT License (MIT)
# 
# Copyright(c) 2017 Raphael Menges
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions :
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Import modules
import xdf.xdf as xdf
import collections
import sys
import easygui

# Variable to store printed text
text = []

###############################################################################
### LOAD XDF FILE
###############################################################################

# Get filepath from user
filepath = easygui.fileopenbox("Path to XDF file", "Open")

# Load file
streams = xdf.load_xdf(filepath, None, False)[0]

text.append("--------------------")

###############################################################################
### PARSE INFORMATION
###############################################################################

text.append("Stream Count: " + str(len(streams)))
text.append("--------------------")

# Go over streams
for i in range(len(streams)):
    
    text.append("######### " + str(i) + " ########")
    
    # Fetch stream info
    streamInfo = streams[i]['info']
    
    # Extract info
    name        = streamInfo['name'][0]
    dataType    = streamInfo['type'][0]
    cannelCount = streamInfo['channel_count'][0]
    dataRate    = streamInfo['nominal_srate'][0]
    dataFormat  = streamInfo['channel_format'][0]
    identifier  = streamInfo['source_id'][0]
    
    # Print resuls
    text.append("Name: "          + name)
    text.append("Data Type: "     + dataType)
    text.append("Channel Count: " + cannelCount)
    text.append("Data Rate: "     + dataRate)
    text.append("Data Format: "   + dataFormat)
    text.append("Identifier: "    + identifier)
    
    # Announce extraction of child values
    text.append("Child Values:")
    
     # Extract child values
    children = streamInfo['desc'][0]
    
    # Go over values
    for childKey in children:
        
        # Fetch value by key
        childValue = children[childKey][0]
        
        # Is value a sequence ("append_child_value")
        if(isinstance(childValue, collections.Sequence)):
            text.append("   " + childKey + ": " + childValue)
            
        # Is value a mapping ("append_child")
        elif(isinstance(childValue, collections.Mapping)):
            text.append("   " + childKey)
            
            # Value of child is a dictionary that has to be traversed
            for childValueKey in childValue: # go over all collected unique children
                
                # The XDF structure seams to collect all inner children with the same name
                # and then creates a dictionary to distinguish between the children. Here
                # we are inside one of those unified structures                
                for innerChildValues in childValue[childValueKey]: # go over data sets of unified children
                    
                    # Add new inner child to the info header
                    text.append("   " + "   " + childValueKey)
                    
                    # Now go over information of single asset within unified structure (like information about one channel)
                    for innerChildKey in innerChildValues: # go over extracted data set
                        text.append("   " + "   " + "   " + innerChildKey + ": " + innerChildValues[innerChildKey][0])
                        
    # Aquired data
    text.append("Data:")
    text.append("   " + "Time Stamp Count:  " + str(len(streams[i]['time_stamps'])))
    text.append("   " + "Sample Data Count: " + str(len(streams[i]['time_series'])))
    
    # Check aquired data in detail
    timeSeries = streams[i]['time_series']
    dataChannelCount = len(timeSeries[0])
    text.append("   " + "Channel Count: " + str(dataChannelCount))
    
    # Go over data and extract information for each channel
    text.append("   " + "Channel Data:")
    for j in range(dataChannelCount): # go over channels
        text.append("   " + "   " + "Channel " + str(j) + ":")
        
        # Go over all entries for that channel
        meanValue = 0
        minValue = sys.maxint
        maxValue = -sys.maxint - 1
        for k in range(len(timeSeries)): # go over times
            
            # Update Values
            value = timeSeries[k][j] # first row, then column
            meanValue += value # mean
            minValue = value if minValue > value else minValue # min
            maxValue = value if maxValue < value else maxValue # max
            
        # Print results
        meanValue = meanValue / len(timeSeries)
        text.append("   " + "   " + "   " + "Mean: " + str(meanValue))
        text.append("   " + "   " + "   " + "Min:  " + str(minValue)) 
        text.append("   " + "   " + "   " + "Max:  " + str(maxValue)) 
                        
    text.append("--------------------")
    
easygui.codebox("Output for file: " + filepath, "XDF Printer", '\n'.join(text))