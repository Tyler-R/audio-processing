import numpy as np
import matplotlib.pyplot as plot

class WavReader:
    def __init__(self, filePath):
        #guitar_test
        with open(filePath, 'r') as file:
            self.data = []

            fileContents = file.read()

            headerPosition = 0
            headerPosition = self.readRIFFChunk(fileContents)

            headerPosition = self.readFmtChunk(fileContents, headerPosition)

            headerPosition = self.readDataChunk(fileContents, headerPosition)


    def readInteger(self, data, startIndex):
        firstValue = ord(data[startIndex])
        secondValue = ord(data[startIndex + 1])
        thirdValue = ord(data[startIndex + 2])
        fourthValue = ord(data[startIndex + 3])

        return (firstValue << 0) | (secondValue << 8) | (thirdValue << 16) | (fourthValue << 24)

    def read24BitNumber(self, data, startIndex):
        firstValue = ord(data[startIndex])
        secondValue = ord(data[startIndex + 1])
        thirdValue = ord(data[startIndex + 2])

        return (firstValue << 0) | (secondValue << 8) | (thirdValue << 16)

    def readShort(self, data, startIndex):
        firstValue = ord(data[startIndex])
        secondValue = ord(data[startIndex + 1])

        return (firstValue << 0) | (secondValue << 8)

    def readSignedShort(self, data, startIndex):
        firstValue = ord(data[startIndex])
        secondValue = ord(data[startIndex + 1])

        # if firstValue > 127:
            # firstValue = (firstValue - 128) * -1

        # if secondValue > 127:
            # secondValue = (secondValue - 128) * -1

        value = (firstValue << 0) | (secondValue << 8)

        if secondValue > 127:
            value = value - 65536

        return value

    # returns the index in the file that
    def readRIFFChunk(self, file, headerOffset = 0):

        expectedChunkID = "RIFF"
        for i in range(len(expectedChunkID)):
            if file[i] != expectedChunkID[i]:
                print("PROBLEM PARSING FILE")
                return -1

        headerOffset = headerOffset + 4
        print(expectedChunkID)

        self.chunkSize = self.readInteger(file, headerOffset)
        headerOffset = headerOffset + 4

        expectedFormat = "WAVE"
        for i in range(len(expectedFormat)):
            if file[i + headerOffset] != expectedFormat[i]:
                print("file has " + file[i + headerOffset] + " when it should have " + expectedFormat[i])
                print("PROBLEM PARSING FILE")
                return -1

        headerOffset = headerOffset + 4
        print(expectedFormat)

        return headerOffset


    def readFmtChunk(self, file, headerOffset):
        if headerOffset == -1:
            return -1


        expectedSubChunkID = "fmt "
        for i in range(len(expectedSubChunkID)):
            if file[i + headerOffset] != expectedSubChunkID[i]:
                print("PROBLEM PARSING FILE")
                return -1

        headerOffset = headerOffset + 4
        print("")
        print(expectedSubChunkID)

        fmtChunkSize = self.readInteger(file, headerOffset)
        headerOffset = headerOffset + 4

        self.audioFormat = self.readShort(file, headerOffset)
        headerOffset = headerOffset + 2

        self.numberOfChannels =  self.readShort(file, headerOffset)
        headerOffset = headerOffset + 2

        self.sampleRate = self.readInteger(file, headerOffset)
        headerOffset = headerOffset + 4

        self.byteRate = self.readInteger(file, headerOffset)
        headerOffset = headerOffset + 4

        self.blockAlign = self.readShort(file, headerOffset)
        headerOffset = headerOffset + 2

        self.bitsPerSample = self.readShort(file, headerOffset)
        headerOffset = headerOffset + 2

        print("format size: " + str(fmtChunkSize))

        print("audioFormat: " + str(self.audioFormat))
        print("Number of channels: " + str(self.numberOfChannels))
        print("sample rate: " + str(self.sampleRate))
        print("byte rate: " + str(self.byteRate))
        print("block align: " + str(self.blockAlign))
        print("bitsPerSample: " + str(self.bitsPerSample))
        print("")


        return headerOffset



    def readDataChunk(self, file, headerOffset):
        if headerOffset == -1:
            return -1

        expectedSubChunkID = "data"
        for i in range(len(expectedSubChunkID)):
            if file[i + headerOffset] != expectedSubChunkID[i]:
                print("PROBLEM PARSING FILE")
                return -1

        headerOffset = headerOffset + 4

        chunkLength = self.readInteger(file, headerOffset)
        headerOffset = headerOffset + 4

        bytesPerSample = self.bitsPerSample / 8

        chunkLength = chunkLength - 4

        if bytesPerSample == 1:
            while chunkLength >= 0:
                data = data[headerOffset]
                if data >= 128:
                    data = data - 255
                self.data.append(data)
                chunkLength = chunkLength - 1
                headerOffset = headerOffset + 1

        if bytesPerSample == 2:
            while chunkLength >= 0:
                data = self.readSignedShort(file, headerOffset)
                self.data.append(data)
                chunkLength = chunkLength - 2
                headerOffset = headerOffset + 2

        if bytesPerSample == 3:
            while chunkLength >= 0:
                data = self.read24BitNumber(file, headerOffset)

                if data >= 8388608:
                    data = data - 16777216

                self.data.append(data)
                chunkLength = chunkLength - 3
                headerOffset = headerOffset + 3

        if bytesPerSample == 4:
            while chunkLength >= 0:
                data = self.readInteger(file, headerOffset)
                self.data.append(data)
                chunkLength = chunkLength - 4
                headerOffset = headerOffset + 4

        return headerOffset

    def show(self):
        data = np.array(self.data[0:5000])

        fs = self.sampleRate
        size = 5000#data.size

        xAxis = np.arange(size) / float(fs)

        plot.plot(xAxis, data)
        plot.show()

    def showDFT(self):
        N = 5000 #64
        k0 = 7
        data = np.array(self.data[0:5000])
                #np.exp(1j * 2 * np.pi * k0 / N * np.arange(N))
                #np.cos(2 * np.pi * k0 / N * np.arange(N))
        x = np.array([])

        for i in range(N):
            s = np.exp(1j * 2 * np.pi * i / N * np.arange(N))
            x = np.append(x, sum(data * np.conjugate(s)))

        plot.plot(np.arange(N), abs(x))
        plot.show()
