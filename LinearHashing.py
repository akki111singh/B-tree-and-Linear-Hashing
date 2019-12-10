#!/usr/bin/env python
# coding: utf-8
#Linear Hasing
#20171210:AKhil Singh

import sys
class LinearHash:
    def __init__(self):
        self.records = 0
        self.p = 0
        self.b = 2
        self.b_new = 4
        self.blockCount = {}
        self.linHash = {}
        self.totalBlocks = 2
        self.blockCount[0] = 1
        self.blockCount[1] = 1
        self.bucketCount = 2

    def insert(self,num):

        global outputBuffer
        hashValue = num % (self.b)

        if hashValue < self.p :
            hashValue = num % (self.b_new)

        if hashValue not in self.linHash:
            self.linHash[hashValue] = [[] for _ in range(1)]

        flag = 0

        for i in range(self.blockCount[hashValue]):
            if num in self.linHash[hashValue][i]:
                flag = 1

        if flag == 0:
            self.records = self.records + 1
            lastBlockidx = self.blockCount[hashValue] - 1
            if len(self.linHash[hashValue][lastBlockidx]) >= bufferSize * 0.25:
                self.totalBlocks+=1
                lastBlockidx += 1
                self.blockCount[hashValue] +=1
               # print(self.blockCount)
                l = []
                self.linHash[hashValue].append(l)
            self.linHash[hashValue][lastBlockidx].append(num)

            outputBuffer.append(num)

            if len(outputBuffer) >= bufferSize/4:
                for val in outputBuffer:
                    print(str(val))
                outputBuffer = []

        if ((self.records*400.0)/(bufferSize*self.totalBlocks)> 75):
           # print((self.records*400.0)/(bufferSize*self.totalBlocks))
            self.createNewBucket()
           # print(self.blockCount)
    def createNewBucket(self):
        global outputBuffer

        self.bucketCount = self.bucketCount+1
        toUpdate = []
       #
        for i in range(self.blockCount[self.p]):
            for val in self.linHash[self.p][i]:
                toUpdate.append(val)

        self.totalBlocks -= self.blockCount[self.p]
        self.linHash[self.p] = [[] for _ in range(1)]
        self.blockCount[self.p] = 1
        self.totalBlocks += 1

        self.linHash[self.bucketCount - 1] = [[] for _ in range(1)]
        self.blockCount[self.bucketCount -1] = 1
        self.totalBlocks +=1

        for val in toUpdate:
            hashVal = val % (self.b_new)

            if hashVal not in self.linHash:
                self.linHash[hashVal] = [[] for _ in range(1)]
                self.blockCount[hashVal] = 1
                self.totalBlocks += 1
            flag = 0

            for i in range(self.blockCount[hashVal]):
                if val in self.linHash[hashVal][i]:
                    flag = 1

            if flag == 0:
                lastBlockidx = self.blockCount[hashVal] - 1
                if len(self.linHash[hashVal][lastBlockidx]) >= bufferSize*0.25:
                    lastBlockidx += 1
                    self.blockCount[hashVal] +=1
                    self.totalBlocks+=1
                    l = []
                    self.linHash[hashVal].append(l)
                self.linHash[hashVal][lastBlockidx].append(val)

        self.p = self.p+1
        if self.bucketCount == self.b_new:
            self.b = self.b * 2
            self.b_new = 2 * self.b
            self.p = 0

        return 1


def main():
    global outputBuffer
    Lhash = LinearHash()
    input_buffer = []


    inputSize = (numBuffers-1)*(bufferSize/4)
    outputSize = (bufferSize/4)


    fileName = sys.argv[1]
    F = open(fileName)

    for line in F:
        input_buffer.append(int(line.strip()))
        if len(input_buffer) >= inputSize:
            for num in input_buffer:
                Lhash.insert(num)
            input_buffer = []

    for num in input_buffer:
        Lhash.insert(num)
    input_buffer = []

    F.close()

    for num in outputBuffer:
        print(num)
    outputBuffer = []

outputBuffer = []
numBuffers = 2 #Number of buffers must be >=2
bufferSize = 4 #Buffer size must be >=4

main()
