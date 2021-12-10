import matplotlib.pyplot as plt
import math
import pickle

with open("backup_file_Without_StopWords", 'rb') as file_:
    positional_dict = pickle.load(file_)


token_occurences = sorted([val.count for val in positional_dict.values()], reverse=True)
max_ = token_occurences[0]
x_ = []
y1_ = []
y2_ = []
for index, ocurrence in enumerate(token_occurences):
    x_.append(math.log(index + 1, 10))
    y1_.append(math.log(max_ / (index + 1), 10))
    y2_.append(math.log(ocurrence, 10))

plt.suptitle("Containing StopWords")
plt.plot(x_, y1_)
plt.plot(x_, y2_)
plt.show()


with open("backup_file_contain_stopwords", 'rb') as file_:
    positional_dict = pickle.load(file_)

print(positional_dict)

token_occurences = sorted([val.term_frequency for val in positional_dict.values()], reverse=True)
max_ = token_occurences[0]
x_ = []
y1_ = []
y2_ = []
for index, ocurrence in enumerate(token_occurences):
    x_.append(math.log(index + 1, 10))
    y1_.append(math.log(max_ / (index + 1), 10))
    y2_.append(math.log(ocurrence, 10))

plt.suptitle("Without StopWords")
plt.plot(x_, y1_)
plt.plot(x_, y2_)
plt.show()
