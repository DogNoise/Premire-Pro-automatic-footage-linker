
import gzip
import os
import xml.etree.ElementTree as ET

EN_LANG=TRUE

#Send information (also can be expanded for logging purposes)
def sendImpINFO(string):
    print('\x1b[1;30;42m' + str(string) + '\x1b[0m')

def sendINFO(string):
    print('\x1b[0;30;47m' + str(string) + '\x1b[0m')

def sendWARNING(string):
    print('\x1b[6;30;43m' + str(string) + '\x1b[0m')

def sendERROR(string):
    print('\x1b[1;30;41m' + str(string) + '\x1b[0m')
#End of Send information segment

#returns -1 when error
def PremireProLinkMedia(PrprojPath, FootagePath):
    '''
    This function links all media files to PremirePro project file. It dublicated exisitng PremirePro project (just in case)
    and names it "przed linkowaniem"/"before linking". Then it unpackages PremirePro project using gzip. Modyfies media paths to a right ones.
    At the end it puts it again into .prproj file.
    :param PrprojPath: path to Premiere pro project file
    :param FootagePath: path to a folder with footage for that project file
    :return: None

    WARNING:
    This code doesn't have asserts/exceptions in this stripped out version. Be careful!
    '''

    #User info

    sendINFO("\n--PREMIERE PRO AUTOMATIC FOOTAGE LINKER HAS BEEN LAUNCHED---\n" if EN_LANG else "\n--ODPALONO PREMIRE PRO LINK MEDIA---\n")
    sendINFO("Given data: PrprojPath:: |{}| FootagePath: |{}|".format(PrprojPath, FootagePath) if EN_LANG else "Podane dane: PrprojPath: |{}| FootagePath: |{}|".format(PrprojPath, FootagePath))

    adder="-add-" #adder for XML structure inside PremirePro project files.
    ignore_formats=["cfa", "pek","prproj"] #those formats mentioned inside XML PremirePro project file are not medias (videos, photos, mp3)

    file = gzip.open(PrprojPath, 'rb') #open PremirePro project file
    content = str(file.read(), 'utf-8') #reads content
    XMLcontent=ET.fromstring(content) #formats string into XMLcontent
    file.close() #closes original PremirePro project file.

    #rename original PremirePro project file (it's still here just in case something wents wrong)
    os.rename(PrprojPath, PrprojPath.split(".")[0] + " - before linking" if EN_LANG else PrprojPath, PrprojPath.split(".")[0] + " - przed linkowaniem")


    def get_footage_paths(path):
        '''
        This function makes array of filepaths too all files inside footage folder (including subfolders)
        :param path: path to folder
        :return:
        when error: -1
        when all good: array of filepaths
        '''

        # When path does not exist
        #TODO -> Add assert/exception
        if not os.path.isdir(path):
            return -1

        files = []
        for (dirpath, dirnames, filenames) in os.walk(path):

            for filename in filenames:
                if len(str(filename).split("."))>1:
                    files.append([os.path.join(dirpath,filename),filename,str(filename).split(".")[-1].lower()])

        return files


    #Make an array of paths to footage
    footage_array=get_footage_paths(FootagePath)

    #This part processes actual XML content of a Premire Pro project and changes paths to the right onces.
    for media in XMLcontent.findall('Media'): #for all 'media's inside XML
        for title in media:
            if title.tag in ["ActualMediaFilePath","FilePath"]: #go to the place where ActualMediaFilePath is stored

                file_name=str(title.text).split("\\")[-1]

                if len(str(file_name).split("."))<2:
                    #It means that filename doesn't have dot - this is not a real filename
                    #That could be .AE, .MOGRT, .AEGRAPHICS files. Those have no problem with automatic linking to 
                    #new paths. This is why script ignores them
                    continue

                key=False #bool used to see if THAT footage can be found inside new footage folder
                found_ele=[] #Array to store paths to a new footage

                #Check if footage was found in folder
                for ele in footage_array:
                    if(ele[1]==file_name):
                        key=True
                        found_ele=ele
                        break

                if key:
                    #Yay! Footage was found. Now replace it with new path.
                    original_name=found_ele[0]

                    new_name=".".join(str(found_ele[0]).split(".")[:-1])+adder+"."+str(found_ele[0]).split(".")[-1]

                    if os.path.isfile(original_name):
                        os.rename(original_name,new_name)
                        pass
                    elif os.path.isfile(new_name):
                        pass
                    else:
                        print("ERROR")

                    #change original path in project into new path
                    title.text=new_name


    #Put back a Premire Pro project with a new footahe paths linked and close file.
    xmlstr=ET.tostring(XMLcontent,encoding='utf8',method='xml')
    file_out = gzip.open(PrprojPath, 'wb')
    file_out.write(xmlstr)
    file_out.close()
    sendINFO("Premiere Pro Footage Linking Completed" if EN_LANG else "Skończono Linkowanie Premire Pro")

if __name__ == '__main__':
    #TODO Write a command line support
    pass
    

