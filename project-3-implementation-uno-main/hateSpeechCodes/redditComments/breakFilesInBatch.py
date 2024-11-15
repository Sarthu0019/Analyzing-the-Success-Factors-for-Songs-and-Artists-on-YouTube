import os
import csv

def splitCsv(inputCsv, outputDir, chunkSize=100):
    with open(inputCsv, 'r', encoding='utf-8-sig') as inFile:
        reader = csv.reader(inFile)
        header = next(reader)
        for index, row in enumerate(reader):
            if index % chunkSize == 0:
                outputCsv = os.path.join(outputDir, f"{os.path.splitext(os.path.basename(inputCsv))[0]}_{index // chunkSize + 1}.csv")
                with open(outputCsv, 'w', newline='', encoding='utf-8') as outFile:
                    writer = csv.writer(outFile)
                    writer.writerow(header)
                    writer.writerow(row)
            else:
                with open(outputCsv, 'a', newline='', encoding='utf-8') as outFile:
                    writer = csv.writer(outFile)
                    writer.writerow(row)

def processDirectory(inputDir, outputParentDir):
    for root, dirs, files in os.walk(inputDir):
        for file in files:
            if file.endswith('.csv'):
                inputCsv = os.path.join(root, file)
                outputDir = os.path.join(outputParentDir, os.path.relpath(root, inputDir))
                os.makedirs(outputDir, exist_ok=True)
                splitCsv(inputCsv, outputDir)

# Example usage
inputDirectory = './Reddit/comments'
outputParentDirectory = './Reddit/splitData'
processDirectory(inputDirectory, outputParentDirectory)
