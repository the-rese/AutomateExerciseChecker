# from pushups import PushupClass
# from openpyxl.workbook import Workbook
# import pandas as pd
import os

FOLDER_PATH = r'C:\\Users\\tsg\\Documents\\GitHub\\AutomateExerciseChecker\\test\\crunches'

name_list = []
counter_list = []
correct_rep_list = []
st_list = []
rom_list = []
ave_depth_list = []


def exerciseRater(dir, name_list, counter_list, correct_rep_list, st_list, rom_list, ave_depth_list):
    fileNames = os.listdir(dir)
    for fileName in fileNames:
        gender = fileName[0]
        # create object or instance for Pushup Class
        filepath = os.path.abspath(os.path.join(dir, fileName))
        pushup_instance = PushupClass(filepath)
        # test if mediapipe still works
        pushup_instance.rateExercise()
        pushup_instance.summarizeResult()
        result = pushup_instance.getSummary()

        name_list.append(fileName)

        for item in result:
            # total num of reps
            counter_list.append(item[0])
            # correct num of good reps
            correct_rep_list.append(item[1])
            # standardize test
            st_list.append(item[2])
            # range of motion
            rom_list.append(item[3])
            # ave angle depth
            ave_depth_list.append(item[4])


def main():
    exerciseRater(FOLDER_PATH, name_list, counter_list,
                  correct_rep_list, st_list, rom_list, ave_depth_list)
    columns = ["Student Name", "Total Num of Rep", "Correct Num of Rep", "Standardize Test",
               "Range of Motion", "Average Angle Depth"]

    df = pd.DataFrame(list(zip(name_list, counter_list, correct_rep_list,
                      st_list, rom_list, ave_depth_list)), columns=columns)
    print(df)
    out_filename = 'pushup-summary.xlsx'
    out_path = 'C:\\Users\\Therese Bolabola\\OneDrive\\Desktop\\ExerciseTracker\\summary\\'+out_filename
    df.to_excel(out_path, sheet_name="PE Section")


if __name__ == "__main__":
    main()
