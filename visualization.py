import libfmp.b
import matplotlib

def calculate_accuracy(real_ann, predicted_ann): 
    intersection = 0
    i1 = i2 = 0
    while i1 < len(real_ann) and i2 < len(predicted_ann):
        if real_ann[i1][1] < predicted_ann[i2][0]:
            i1 += 1
        elif predicted_ann[i2][1] < real_ann[i1][0]:
            i2 += 1
        else:
            if real_ann[i1][2] == predicted_ann[i2][2]:
                start = max(real_ann[i1][0], predicted_ann[i2][0]) 
                end = min(real_ann[i1][1], predicted_ann[i2][1])
                intersection += end - start
            if real_ann[i1][1] < predicted_ann[i2][1]:
                i1 += 1
            else:
                i2 += 1
 
    return intersection / real_ann[-1][1]

def show_annotation(annotation):
    libfmp.b.plot_segments(annotation)