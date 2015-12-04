import matplotlib.pyplot as plt
import random

from sklearn import datasets, svm, metrics

############################################################
# Generates a plot of four predictions in a digits dataset #
# Example taken from scikit-learn.org ######################
#######################################

# The digits dataset
digits = datasets.load_digits()

# The data that we are interested in is made of 8x8 images of digits
# Let's look at the first 3 images, stored in the 'images' attribute of
# the datset. For these images, we know which digit they represent:
# it is given in the 'target' of the dataset
images_and_labels = list(zip(digits.images, digits.target))
for index, (image, label) in enumerate(images_and_labels[:4]):
	plt.subplot(2, 4, index +1)
	plt.axis('off')
	plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
	plt.title('Training: %i' % label)

# To apply a classifier on this data, we need to flatten the image, to
# turn the data in a (samples, feature) matrix:
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.001)

# We learn the digits on the first half of the digits
classifier.fit(data[:n_samples / 2], digits.target[:n_samples / 2])

# Now predict the value of the digit on the second half:
expected = digits.target[n_samples / 2:]
predicted = classifier.predict(data[n_samples / 2:])

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

# Display new predictions every time.
start = random.randint(0, 895)

images_and_predictions = list(zip(digits.images[n_samples / 2:], predicted))
for index, (image, prediction) in enumerate(images_and_predictions[start:start+4]):
    plt.subplot(2, 4, index + 5)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Prediction: %i' % prediction)

plt.show()