import os


class ApplicationProperty:
    #shared variables
    currentModelDirectory = ""

    screenWidth = 1366
    screenHeight = 768

    #shared functions
    @staticmethod
    def getScriptPath():
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def getScreenWidth():
        if ApplicationProperty.screenWidth > 0: return ApplicationProperty.screenWidth
        else: return None

    @staticmethod
    def getScreenHeight():
        if ApplicationProperty.screenHeight > 0: return ApplicationProperty.screenHeight
        else: return None

    @staticmethod
    def get_absolute_path(relative_path, reference_directory):
        ref_list, tar_list = [], []

        while reference_directory:
            if reference_directory == '/':
                ref_list.append('/')
                break
            temp = os.path.split(reference_directory)
            reference_directory = temp[0]
            if temp[1]: ref_list.append(temp[1])


        while relative_path:
            temp = os.path.split(relative_path)
            relative_path = temp[0]
            if temp[1]: tar_list.append(temp[1])
            if relative_path == '/': break

        abs_path = ''

        try:
            for i in reversed(range(len(tar_list))):
                if tar_list[i] == '..':
                    ref_list.pop(0)
                    tar_list.pop(i)

            for i in reversed(range(len(ref_list))): abs_path = os.path.join(abs_path, ref_list[i])
            for i in reversed(range(len(tar_list))): abs_path = os.path.join(abs_path, tar_list[i])
        except: return None

        return abs_path

class dummy:
    model_graph = None