
class EditDistance(object):
    
    __COST_COPY = 0.0
    __COST_INSERT = 1.0
    __COST_DELETE = 1.0
    __COST_SUBST = 2.0
    
    def __init__(self,trg,src,func=None):
        self.source = src
        self.target = trg
        self.func = func
        self.n = len(trg)
        self.m = len(src)
        self.distMatrix = [[0.0 for i in range(self.m+1)] for j in range(self.n+1)]
        self.__initFirstColAndRow()
        self.distance = self.minEditDistance()
        self.bestAlignment = []
        
    def __str__(self):
        return 'EditDistance source [%s] target [%s] distance [%d]' % (self.source, self.target, self.distance)
    
    def costInsert(self,s):
        return self.__COST_INSERT
    
    def costDelete(self,s):
        return self.__COST_DELETE
    
    def costSubstitution(self,trg,src):
        if self.func == "sent":
            return (self.__COST_COPY if src == trg else (0.5 + EditDistance(trg,src,"chars").distance))
        else: 
            return (self.__COST_COPY if src == trg else self.__COST_SUBST)
    
    def __initFirstColAndRow(self):
        for i in range(1,self.n+1):
            self.distMatrix[i][0] = self.distMatrix[i-1][0] + self.costInsert(self.target[i-1])
        for j in range(1,self.m+1):
            self.distMatrix[0][j] = self.distMatrix[0][j-1] + self.costDelete(self.source[j-1])
        
    def minEditDistanceStep(self,i,j):
        #skip a character
        a = self.distMatrix[i-1][j]+1.0
        b = self.distMatrix[i][j-1]+1.0
        #determin substitution
        c = self.distMatrix[i-1][j-1]+self.costSubstitution(self.target[i-1],self.source[j-1])
        
        #select the minimum value
        self.distMatrix[i][j] = min(a,b,c)
        
    def minEditDistance(self):
        #iterate over the distance matrix array
        if self.n == 0 and self.m == 0:
            return 0.0
        
        for i in range(1,self.n+1):
            for j in range(1,self.m+1):
                self.minEditDistanceStep(i, j)
        
        #return edit distance 
        return self.distMatrix[self.n][self.m]/(self.n+self.m)
    
    def alignText(self,n,m):
        if n == 0 and m == 0:
            return None
        
        i = n
        j = m
        
        distances = []
        distances.append(self.distMatrix[i-1][j])
        distances.append(self.distMatrix[i][j-1])
        distances.append(self.distMatrix[i-1][j-1])
        minIdx = distances.index(min(distances))
        
        if minIdx == 0:
            self.bestAlignment.append((self.source[j],round(self.distMatrix[i-1][j]/(i+j),4),self.target[i-1]))
            self.alignText(i-1,j)
        elif minIdx == 1:
            self.bestAlignment.append((self.source[j-1],round(self.distMatrix[i][j-1]/(i+j),4),self.target[i]))
            self.alignText(i,j-1)
        elif minIdx == 2:
            self.bestAlignment.append((self.source[j-1],round(self.distMatrix[i-1][j-1]/(i+j),4),self.target[i-1]))
            self.alignText(i-1,j-1)
        else:
            print("ERROR")
                
        return None
        
    def printEditDistance(self):
        print("Overall edit distance is: {0}".format(self.distance))
    
    def printAlignment(self):
        print(self.prettyPrint(self.bestAlignment))
   
    # Pretty Print table in tabular format
    def prettyPrint(self, table, justify = "R", columnWidth = 0):
    # Not enforced but
        # if provided columnWidth must be greater than max column width in table!
        if columnWidth == 0:
            # find max column width
            for row in table:
                for col in row:
                    width = len(str(col))
                    if width > columnWidth:
                        columnWidth = width

        outputStr = ""
        for row in table:
            rowList = []
            source = row[0]
            dist = row[1]
            target = row[2]
            rowList.append(str(source).rjust(columnWidth))
            rowList.append(str(dist).center(len(str(dist))+4))
            rowList.append(str(target).ljust(columnWidth))
           
            outputStr += ' '.join(rowList) + "\n"
        return outputStr


    