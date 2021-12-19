from tempfile import NamedTemporaryFile
import shutil
import csv
import numpy as np
import pandas as pd

filename = '../input/style-classifier/Multi_Label_dataset/Tasks/label_studio_200_images.csv'
tempfile = NamedTemporaryFile(mode='w', delete=False)
fields = ['image', 'id', 'Color', 'Palette', 'DoF', 'Composition', 'Type', 'annotator', 'annotation_id', 'created_at', 'updated_at', 'lead_time']

dataColor = np.array([['image', 'Color']])
dataDof = np.array([['image', 'DoF']])
dataPal = np.array([['image', 'Palette']])
dataComp = np.array([['image', 'Composition']])
dataType = np.array([['image', 'Type']])

# Transform initial Label Studio .csv file (fix ids, remove extra strings, 0-1 bool for binary tasks)
with open(filename, 'r') as read_obj, tempfile:
    csv_dict_reader = csv.DictReader(read_obj, fieldnames=fields)
    writer = csv.DictWriter(tempfile, fieldnames=fields)
    writer.writeheader()
    header_mapping = next(csv_dict_reader)
    for row in csv_dict_reader:
        # fix ids
        id = row['image'].split("photo")[1]
        row['image'] = "photo"+id
        # remove extra strings
        if "choices" in row['Palette']:
            row['Palette'] = row['Palette'].split(": ")[1].replace('}', '')
            row = {'image': row['image'], 'id': row['id'], 'Color': row['Color'], 'Palette': row['Palette'], 'DoF': row['DoF'], 'Composition': row['Composition'],
                   'Type': row['Type'], 'annotator': row['annotator'], 'annotation_id': row['annotation_id'], 'created_at': row['created_at'],
                   'updated_at': row['updated_at'], 'lead_time': row['lead_time']}
        if "choices" in row['Composition']:
            row['Composition'] = row['Composition'].split(": ")[1].replace('}', '')
            row = {'image': row['image'], 'id': row['id'], 'Color': row['Color'], 'Palette': row['Palette'], 'DoF': row['DoF'], 'Composition': row['Composition'],
                   'Type': row['Type'], 'annotator': row['annotator'], 'annotation_id': row['annotation_id'], 'created_at': row['created_at'],
                   'updated_at': row['updated_at'], 'lead_time': row['lead_time']}
        if "choices" in row['Type']:
            row['Type'] = row['Type'].split(": ")[1].replace('}', '')
            row = {'image': row['image'], 'id': row['id'], 'Color': row['Color'], 'Palette': row['Palette'], 'DoF': row['DoF'], 'Composition': row['Composition'],
                   'Type': row['Type'], 'annotator': row['annotator'], 'annotation_id': row['annotation_id'], 'created_at': row['created_at'],
                   'updated_at': row['updated_at'], 'lead_time': row['lead_time']}
        if "Deep" in row['DoF']:
            row['DoF'] = "Deep"
            row = {'image': row['image'], 'id': row['id'], 'Color': row['Color'], 'Palette': row['Palette'], 'DoF': row['DoF'], 'Composition': row['Composition'],
                   'Type': row['Type'], 'annotator': row['annotator'], 'annotation_id': row['annotation_id'], 'created_at': row['created_at'],
                   'updated_at': row['updated_at'], 'lead_time': row['lead_time']}
        if "Shallow" in row['DoF']:
            row['DoF'] = "Shallow"
            row = {'image': row['image'], 'id': row['id'], 'Color': row['Color'], 'Palette': row['Palette'], 'DoF': row['DoF'], 'Composition': row['Composition'],
                   'Type': row['Type'], 'annotator': row['annotator'], 'annotation_id': row['annotation_id'], 'created_at': row['created_at'],
                   'updated_at': row['updated_at'], 'lead_time': row['lead_time']}

        # keep info to create new .csv files for the multi-label tasks
        dataColor = np.append(dataColor, np.array([[row['image'], row['Color']]]), axis=0)
        dataDof = np.append(dataDof, np.array([[row['image'], row['DoF']]]), axis=0)
        dataPal = np.append(dataPal, np.array([[row['image'], row['Palette']]]), axis=0)
        dataComp = np.append(dataComp, np.array([[row['image'], row['Composition']]]), axis=0)
        dataType = np.append(dataType, np.array([[row['image'], row['Type']]]), axis=0)

        writer.writerow(row)

shutil.move(tempfile.name, filename)

# Create new .csv files for the multi-labeled tasks (Palette, Composition, Type)
def wrap_eval(x):
    try:
        return eval(x)
    except:
        return [x]

dataFrames = [dataColor, dataDof, dataPal, dataComp, dataType]
csvNames = ['color.csv', 'dof.csv', 'palette.csv', 'composition.csv', 'type.csv']
colOfInterest = ['Color', 'DoF', 'Palette', 'Composition', 'Type']
for j in range(5):
    df = pd.DataFrame(dataFrames[j])
    df.to_csv(csvNames[j], header=None, index=False)
    df = pd.read_csv(csvNames[j])
    df[colOfInterest[j]] = df[colOfInterest[j]].apply(wrap_eval)
    for i, row in df.iterrows():
        for col in row[colOfInterest[j]]:
            try:
                df[col]             # (1) in the steps above.
            except:
                df[col] = 0         # (2)
            finally:
                df.loc[i, col] = 1  # (3)

    fixed = pd.DataFrame(df)
    fixed.to_csv(csvNames[j], index=False)
