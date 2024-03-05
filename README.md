
# EconScope :money_with_wings:

> The project, currently in development!

## Project Description

The project  aims to address the limitations of existing financial management software by enhancing automation and accessibility. Existing solutions have been insufficient in their automation capabilities, leading to significant time consumption for end-users. Furthermore, the prevalence of software designed exclusively for mobile platforms has left a gap for personal computer users, necessitating a more versatile solution.

To fill this gap, the project is developing a financial web application that revolutionizes personal finance management. This innovative application leverages optical character recognition (OCR) technology to extract information from uploaded receipt images, automatically generating expense records. This process minimizes the need for manual data entry, significantly reducing the time and effort required by users. Users may still need to review and adjust the extracted information, but the application significantly streamlines the expense tracking process.

This project represents a significant advancement in financial management software, aiming to bridge the gap between automation, accessibility, and user-friendliness. By focusing on personal computers and incorporating OCR technology, the application is set to provide a more efficient and accessible tool for managing personal finances.

## Functionality

### Automatic borders detection and segmentation of the receipt image

To enhance the automated generation of expense entries from receipt images, the project incorporates a sophisticated segmentation process to ensure optimal image quality and accurate text recognition. Given the common distortions in receipts, such as perspective deformation, which can lead to inaccurate character recognition by neural networks, it is crucial to accurately identify and align the receipt area within the image. This involves determining the receipt's border, aligning its orientation, and flipping the image to ensure correct alignment of characters.

The segmentation component of the project employs advanced machine learning models, specifically leveraging the Swin Transformer architecture for its ability to handle shifted windows, enabling the network to learn different neighboring information for all patches. The Mask R-CNN model, combined with the Feature Pyramid Network (FPN) from the MMDetection library, is utilized to identify and segment the receipt area within the image. This combination allows for the precise localization and extraction of the receipt's content, facilitating the subsequent text recognition process.

The model training (Google Colab Link: https://colab.research.google.com/drive/1R8dc9FsnUTHIkfuxSYmzeOTqT8ZWALqp?usp=sharing) was conducted on a proprietary dataset, which was created using Roboflow (https://universe.roboflow.com/myworkspace-cvgyw/segrec), augmented with a total of approximately 3354 images, including 800 (https://huggingface.co/datasets/mychen76/receipt_cord_ocr_v2) and 1140 (https://huggingface.co/datasets/mychen76/ds_receipts_v2_train) from the HuggingFace platform and around 333 from the project team's own collection. These images underwent augmentation procedures, such as rotation within a 15-degree range and scaling along one axis, to enhance the model's robustness and generalizability. The PyTesseract (Google Colab Link: https://colab.research.google.com/drive/1dn8IGUG0dWtYuafVFBwQh8nenCOS3utP?usp=sharing) library is employed image flipping to correct the orientation of the image, ensuring that text recognition is as accurate as possible.

This segmentation process is a pivotal component of the project, aiming to overcome the challenges posed by receipt image distortions.

<p align="center">
  <img src="https://github.com/dumonten/EconScope/assets/92388475/a33619d3-07cc-458d-9a55-bada393a76eb" alt="segImg1" height="400"/>
</p>

---

<p align="center">
  <img src="https://github.com/dumonten/EconScope/assets/92388475/a3f19a28-f10b-4998-b16d-8b67c29aa7d9" alt="segImg2" height="400"/>
</p>

---

<p align="center">
  <img src="https://github.com/dumonten/EconScope/assets/92388475/e685cd88-fe65-4b63-9bdd-09db5e0e04ab" alt="segImg3" height="400"/>
</p>

<p align="center"><i>Example of segmentation of the receipt image</i></p>

### Image quality improvement

> This algorithm was found in solutions on StackOverflow: https://stackoverflow.com/questions/56905592/automatic-contrast-and-brightness-adjustment-of-a-color-photo-of-a-sheet-of-pape.

To enhance the quality of receipt images for optimal text extraction, the project employs a dual binarization approach. Initially, Niblack binarization is applied to establish a clear contrast between the black characters on the receipt and the white background, thereby improving the visibility and readability of the text. This method is particularly effective in images with varying lighting conditions, enhancing the overall image quality.

<p align="center">
  <img src="https://github.com/dumonten/EconScope/assets/92388475/6d337225-fdd4-43cf-b6df-a9fe0ce74989" alt="imgQualityBoost" height="400"/>
</p>

<p align="center"><i>The resulting image after applying the mask algorithm</i></p>

Following Niblack binarization, Otsu binarization is utilized based on pixel intensities for each channel to generate masks. This dual approach not only enhances the contrast between text and background but also preserves color information in the image, which is crucial for maintaining the visual integrity of the original receipt while ensuring that text is accurately recognized.

<p align="center">
  <img src="https://github.com/dumonten/EconScope/assets/92388475/f05d5ed3-7a3f-462b-b070-60be3bace3cc" alt="mask1" height="400"/>
</p>

---

<p align="center">
  <img src="https://github.com/dumonten/EconScope/assets/92388475/2d2337c2-bde3-4957-bcba-c2a404f92631" alt="mask2" height="400"/>
</p>

<p align="center"><i>Image of background and foreground masks</i></p>

For the application's requirements, the Niblack binarization is sufficient, but future developments aim to incorporate an algorithm capable of eliminating creases and dents in the image. This would further improve the image quality, especially for receipts with complex textures or deformities that could otherwise hinder text recognition.

The application of these binarization techniques is demonstrated through the use of two masks: one for the background (text), and the second for the foreground (colored areas of the image). To generate the second mask, the first one is inverted, ensuring that the text is easily distinguishable from the background and any other elements in the image.

The effectiveness of these binarization methods is supported by empirical evidence from the literature, where they have been shown to significantly improve the accuracy of text recognition in various document images.

### Text recognition

The project utilizes the PaddleOCR library for the purpose of text recognition, which is a dual-model architecture comprising a character detection component and a character recognition component. The character detection model employs DBNet++, while the character recognition model is based on SVTR. To train the model, a custom dataset was developed using the TRDG (https://github.com/Belval/TextRecognitionDataGenerator) software tool. This tool facilitates the generation of images with text, leveraging a dictionary and selecting fonts that closely mimic machine printing. A dataset of 100,000 images was generated for training (Google Colab Link: https://colab.research.google.com/drive/1S4ksVrUqW0zjvYm5es-eZMldXrnmBZhH?usp=sharing), although this figure is deemed insufficient, necessitating further augmentation in future iterations to address the model's under-training status.

<p align="center">
  <img src="https://github.com/dumonten/EconScope/assets/92388475/bf7268aa-7763-41cb-942c-be443f7434bb" alt="recImg" height="400"/>
</p>

---

<p align="center">
  <img src="https://github.com/dumonten/EconScope/assets/92388475/fd64039c-67a3-4033-8f4c-5c3c8b87eece" alt="recText" height="400"/>
</p>


<p align="center"><i> Input image and recognized text</i></p>

### Text data analysis

For the analysis of textual data extracted from receipts, the project employs the GPT model to generate a structured JSON output and categorize each product item based on a predefined list of categories. The JSON structure template, along with the guidelines for its population, are communicated to the model within the request to ensure consistency across responses.

This approach includes the submission of the list of categories, the text extracted from the receipt and JSON-template. Given the GTP models meta-learning capabilities, there is no necessity for direct retraining, as it inherently adapts to the task. The models utilized are sourced from the g4f (https://github.com/xtekky/gpt4free) library.


<p align="center">
  <img src="https://github.com/dumonten/EconScope/assets/92388475/6c4a8250-6d88-46fe-8777-7dff5080b6e7" alt="analysisImg" height="400"/>
</p>

---

<p align="center">
  <img src="https://github.com/dumonten/EconScope/assets/92388475/0f5e80d4-1dc6-4d90-a86a-373db81c3df9" alt="analysisText " height="400"/>
</p>


<p align="center"><i> Input image and analyzed text</i></p>


## The main technologies used

- Python

- Google Colab

- MMDetection

- Roboflow

- PyTesseract

- PaddleOCR

- GPT4Free

## Authors

- *dumonten (Yankova Nastassia)* - https://github.com/dumonten

- *AlabaAclydiem (Pastukhou Kirill)* - https://github.com/AlabaAclydiem
