# TO-DO replace this with label map
# These must match the label map file in the annotations directory
def class_text_to_int(row_label):
    if row_label == 'dog':
        return 1
    elif row_label == 'cat':
        return 2
    else:
        None