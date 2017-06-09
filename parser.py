import json
import csv
import datetime
import os

class Parser(object):
    def __init__(self):
        self.count1 = 0
        self.count2 = 0

    #####################################################################################################################
    ############################################## Read json files (input) ##############################################
    #####################################################################################################################

    def loadData(self, filename):
        with open (filename) as infile:
            data = infile.read()
            # print data
            jsondata = json.loads(data) #convert data into a dictionary
            item = jsondata["e2e"] # get json object named 'e2e'

        infile.close()
        return item

    ######################################################################################################################################
    ############################################## write query data into csv file (output1) ##############################################
    ######################################################################################################################################
    # with open ('testOutput.csv', 'wb') as outfile:
        # csv_file = csv.writer (outfile)
        # csv_file.writerow(item['testName'] + "\n")  # add rows into the file
    def writeQuery(self, filename):
        item = self.loadData(filename)
        # check if it is the first time creating csv file, set headers
        if self.count1 == 0:
            row_0 = 'query_id' + ',' + 'query_testName' + '\n'
            csv_file = open('my_query_file.csv' , 'w')
            csv_file.write(row_0)
            csv_file.close()
        row =  'query_' + str(self.count1) + ',' + item['testName'] + '\n'
        csv_file = open('my_query_file.csv', 'a')
        csv_file.write(row)
        csv_file.close()
        self.count1 += 1

    ######################################################################################################################################
    ############################################## write json data into csv file (output2) ##############################################
    ######################################################################################################################################

    def writeOutput(self,filename):
        item = self.loadData(filename)

        # create and format the current datetime
        date = datetime.datetime.now()
        date = date.strftime("%m/%d/%y %H:%M")
        print 'this is date: ' + date

        # check if it is the first time creating csv file, set headers
        if self.count2 == 0:
            row_0 = 'query_id' + ',' + 'answerRendering.TABLE-MODE'+ ',' + 'answerRendering.CHART-MODE' + ',' + 'answerMetadataRpc.callosum.postgres.duration' + ',' + 'answerMetadataRpc.duration' + ',' + 'answerDataRpc.CHART.duration' + ',' + 'answerDataRpc.CHART.callosum.postgres.duration' + ',' + 'answerDataRpc.CHART.callosum.falcon.duration' + ',' + 'answerDataRpc.HEADLINE+TABLE.duration' + ',' + 'answerDataRpc.HEADLINE+TABLE.callosum.postgres.duration' + ',' + 'answerDataRpc.HEADLINE+TABLE.callosum.falcon.duration' + ',' + 'sageRpc.duration' + '\n'
            csv_file = open('my_output.csv' , 'w')
            csv_file.write(row_0)
            csv_file.close()

        column = 0
        # Print queries
        for key, value in item.iteritems():
            if key == 'answerRendering':
                if len(value) == 0:
                    column = -1
                    print column

            if key == 'answerMetadataRpc':
                if len(value) == 0:
                    column3 = -1
                column3 = str(value['callosum']['postgres']['duration'])
                column4 = str(value['duration'])
                print column4

            if key == 'answerDataRpc':
                for i, v in value.iteritems():
                    try:
                        column8 = str(v['duration'])
                        column9 = str(v['callosum']['postgres']['duration'])
                        column10 = str(v['callosum']['falcon']['duration'])
                    except:
                        column = -1

            if key == 'sageRpc':
                if len(value) == 0:
                    column11 = -1
                column11 = str(value['duration'])
                print column11

        column = str(column)
        row =  'query_' + str(self.count2) + ',' + column + ',' + column + ',' + column3 + ',' + column4 + ',' + column + ',' + column + ',' + column + ',' + column8 + ',' + column9 + ',' + column10 + ',' + column11 + ',' + date +'\n'
        csv_file = open('my_output.csv', 'a')
        csv_file.write(row)
        csv_file.close()
        self.count2 += 1

##############################################################################################################
################################################### Tester ###################################################
##############################################################################################################

parser = Parser() # Create an object of the parser class
for filename in os.listdir('./perf_output'):  # iterate files through dictionary
    if filename.endswith(".out"):
        filepath = './perf_output/' + filename
        parser.writeQuery(filepath)
        parser.writeOutput(filepath)
