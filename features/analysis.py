import numpy as np
import cv2
import matplotlib.pyplot as plt


def mask_size(mask):
    # Count number of pixels in a mask
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]  # Set all pixels = 1, 0;
    pixels = cv2.countNonZero(thresh)  # Basically just a sum of all pixels
    return pixels


def saturation_histogram(image, hsvize=True):
    if hsvize is True:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    x = image.flatten()

    filter = x > 50

    fil = x[filter]

    counts, bins = np.histogram(fil, density=True)
    plt.hist(bins[:-1], bins, weights=counts)
    plt.xlabel('Saturation')
    plt.ylabel('Probability')
    plt.show()


def errors(deposit, amask, image, is_auto=True):
    dep_masked = cv2.bitwise_and(image, image, mask=deposit)
    sobel = amask.sobel_mask(dep_masked)  # Get sobel mask
    edges = amask.edge_sobel_mask(dep_masked)
    if is_auto:
        final_mask = cv2.threshold(sobel-edges, 120, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
    else:
        final_mask = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
        print("Manual Mask Confirmed")
    return final_mask


def show_errors(mask, image):
    result = image.copy()

    green = np.zeros(result.shape, np.uint8)
    green[:] = (57, 255, 20)
    dst = cv2.bitwise_and(green, result, mask=mask)

    return dst


def percent_imp(errors_mask, original_mask, image):
    result = image.copy()
    white= np.zeros(result.shape, np.uint8)
    white[:] = (255, 255, 255)
    errors_masked = cv2.bitwise_and(white, white, mask=errors_mask)
    dep_masked = cv2.bitwise_and(white, white, mask=original_mask)

    error_size = mask_size(errors_masked)
    deposit_size = mask_size(dep_masked)
    ratio = error_size / deposit_size

    ratio_string = "{0:.5f}%".format(ratio * 100)



    return ratio_string