import numpy as np

marks = np.array([
    [70, 80, 90],
    [60, 75, 85],
    [88, 92, 79],
    [55, 65, 70]
])

print("Shape:", marks.shape)
print("Dtype:", marks.dtype)
print("Size:", marks.size)


sliced_data = marks[:2, -1]
print("\nSliced (First 2 students, last subject):", sliced_data)


student_averages = np.round(marks.mean(axis=1), 2)
subject_averages = np.round(marks.mean(axis=0), 2)

print("Student averages:", student_averages)
print("Subject averages:", subject_averages)


marks_with_grace = marks + 5
print("\nMarks after adding 5 grace marks:\n", marks_with_grace)

weights = np.array([0.3, 0.3, 0.4])
weighted_scores = np.round(marks.dot(weights), 2)
print("Weighted scores:", weighted_scores)


reshaped_arr = np.arange(12).reshape(3, 4)
print("\nReshaped array (3x4):\n", reshaped_arr)