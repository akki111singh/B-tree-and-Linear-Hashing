#!/usr/bin/env python
# coding: utf-8

#Bplustree
#Akhil Singh
#20171210
import sys
import bisect
class Node:
    def __init__(self):
        self.isLeaf = True;
        self.Next = None;
        self.keys = []
        self.childs = []

    def SplitNode(self):

        newNode = Node()
        mid = len(self.keys)//2
        midKey = self.keys[mid]

        if self.isLeaf:
            newNode.isLeaf = True;
            newNode.keys,newNode.childs = self.keys[mid:],self.childs[mid:]
            self.keys,self.childs = self.keys[:mid],self.childs[:mid]

            newNode.Next  = self.Next;
            self.Next = newNode;

        else:
            newNode.isLeaf = False
            newNode.keys,newNode.childs = self.keys[mid+1:],self.childs[mid+1:]
            self.keys,self.childs = self.keys[:mid],self.childs[:mid+1]

        return midKey,newNode


# In[144]:

class BPlusTree:

    def __init__(self,size):
        self.root = Node()

        self.root.isLeaf = True
        self.root.keys,self.root.childs = [],[]

        self.root.Next = None
        self.size = size

    def TreeInsert(self,key,node):
        NodeLength = len(node.keys)

        if node.isLeaf :
            idx = bisect.bisect(node.keys,key)
            node.keys[idx:idx],node.childs[idx:idx] = [key],[key]

            if NodeLength > self.size:
                midKey,newNode = node.SplitNode()
                return midKey,newNode
            else:
                return None,None
        else:
            initialKey,lastKey = node.keys[0],node.keys[-1];

            if key < initialKey:
                midVal,newNode = self.TreeInsert(key,node.childs[0])

            for i in range(0,NodeLength-1):
                currKey = node.keys[i];
                nextKey = node.keys[i+1];

                if key >= currKey and key < nextKey:
                    midVal,newNode = self.TreeInsert(key,node.childs[i+1])

            if key >= lastKey:
                midVal,newNode = self.TreeInsert(key,node.childs[-1])

        if midVal != None    :

            idx = bisect.bisect(node.keys,midVal)
            node.keys[idx:idx],node.childs[idx+1:idx+1] = [midVal],[newNode]

            if len(node.keys) > self.size:
                midKey,newNode = node.SplitNode()
                return midKey,newNode
            else:
                return None,None
        else:
            return None,None


    def QuerySearch(self,key,node):

        if not node.isLeaf:
            initialKey,lastKey = node.keys[0],node.keys[-1];

            if key <= initialKey:
                return self.QuerySearch(key,node.childs[0])

            for i in range(len(node.keys)-1):
                currKey = node.keys[i]
                nextKey = node.keys[i+1]
                if key > currKey and key <= nextKey:
                    return self.QuerySearch(key,node.childs[i+1])

            if key > lastKey:
                return self.QuerySearch(key,node.childs[-1])
        else:
            return node

    def KeysInRange(self,minKey,maxKey,node):
        count = 0
        NodeLength = len(node.keys)

        if NodeLength == 0:
                return 0,None

        for i in range(0,NodeLength):
            if minKey <= node.keys[i] and node.keys[i] <= maxKey:
                count= count+1

        if node.keys[-1] > maxKey:
            return count,None
        else:
            return count,node.Next

    def CountRangeQuery(self,minKey,maxKey):

        startLeaf = self.QuerySearch(minKey,self.root)
        keyCount,nextNode = self.KeysInRange(minKey,maxKey,startLeaf)
        count = 0

        count = count+keyCount
        while nextNode!= None:
            keyCount,nextNode = self.KeysInRange(minKey,maxKey,nextNode)
            count = count+keyCount

        return count

    def INSERT(self,key):
        mid,newNode = self.TreeInsert(key,self.root)
        if mid != None:
            newRoot = Node()
            newRoot.isLeaf = False
            newRoot.keys,newRoot.childs = [mid],[self.root,newNode]

            self.root = newRoot
# In[145]:

outputBuffer = []

def printOutput():
    BufferSize = 10.0
    global outputBuffer
    if len(outputBuffer) >= BufferSize:
        for output in outputBuffer:
            print(output)
        outputBuffer = []

def ExecuteCommand(cmd):
    global outputBuffer

    inp = int(cmd[1])
    if cmd[0] == "INSERT":
        tree.INSERT(inp)

    elif cmd[0] == "COUNT":
        res = tree.CountRangeQuery(inp,inp)
        outputBuffer.append(str(res))


    elif cmd[0] == "FIND":
        res = tree.CountRangeQuery(inp,inp)
        if res == 0:
            outputBuffer.append("NO")
        else:
            outputBuffer.append("YES")

    elif cmd[0] == "RANGE":
        inp2 = int(cmd[2])
        res = tree.CountRangeQuery(inp,inp2);
        outputBuffer.append(str(res))

    printOutput()



# In[149]:

def main():

    BufferSize = 10
    global outputBuffer
    filename  = sys.argv[1]
    inputBuffer = []

    fh = open(filename)

    for line in fh:
        cmd  = line.strip()
        inputBuffer.append(cmd.split())

        if len(inputBuffer) > BufferSize:
            for cmd in inputBuffer:
                ExecuteCommand(cmd)
            inputBuffer  = []

    for cmd in inputBuffer:
        ExecuteCommand(cmd)

    inputBuffer = []

    for res in outputBuffer:
        print(res)
    outputBuffer = []

    fh.close()
if __name__ == "__main__":
    NumKeys = 3
    NumPointers = 4
    tree = BPlusTree(NumKeys)
    main()
