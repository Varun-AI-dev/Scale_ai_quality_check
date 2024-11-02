# Scale_ai_quality_check application for traffic_signals

This project automates quality checks for images with bounding boxes as part of the ObserveSign project. The goal is to help the autonomous vehicle industry identify and understand traffic signals by making sure the labeled data is accurate and reliable. We use the Scale API to pull in data, run checks on the images, and generate a report with any issues. This helps flag errors so they can be quickly corrected.

# Project Overview
ObserveSign is a fictional tech startup working with Scale AI to label around 250,000 images of traffic signals. This data will help train machine learning models. The project has three main parts:

1. Task Retrieval - Get the completed task data from the Scale API.
2. Automated Quality Checks - Write a script that automatically checks for mistakes in the annotations.
3. Future Improvements - Think about how we could make this process better in the long run.
The goal is to make a flexible, reliable script that can handle big batches of images and catch potential issues without too much manual work.

# Table of Contents
Setup

How to Use

What the Script Checks

Using the Scale API

What’s Included

Ideas for Improvement


# Setup
1. Clone the Repository: git clone https://github.com/Varun-AI-dev/Scale_ai_quality_check.git
2. cd observe_sign_quality_check
3. Install Required Libraries: pip install -r requirements.txt
   Key libraries include:
   requests - for downloading images from URLs.
   Pillow - for marking up and saving images.
   Standard libraries like csv and json for handling data.
4. Get Access to the Scale API:
   Log into the Scale dashboard to get your API key.
   Steps:
    1. Click on the user icon in the top right.
    2. Go to "API Key".
    3. Use any API key that starts with "live_" to access data.
# How to Use
Load Task Data:
Save all task data in one file all_tasks_data.json Run: python Api_data_retrieval.py.
Run the Quality Check Script: python quality_check_csv.py
Output:
The script generates a .csv file called task_ratings.csv listing any problems found. Annotated images with flagged issues are also saved, with problem areas marked in red.
What the Script Checks
The script reviews each task based on four key criteria to ensure quality:

Audit Results:

If a task was flagged multiple times during review, it may indicate low quality.
Bounding Box Size Consistency:

It checks if any bounding boxes are unusually large or small compared to others in the image.
Label Accuracy:

The script makes sure each box is labeled correctly. Expected labels include:
traffic_control_sign, construction_sign, information_sign, policy_sign, non_visible_face.
Occlusion:

Boxes with high occlusion (50% or more hidden) are flagged, as they may not be useful for training.
Rating System
The script rates each task based on these criteria:


# What’s Included
Quality Check Script:

This script reads task data, checks for issues, and outputs a .csv with results.
Reflection Document:

A short write-up on how this process could be improved over time.
Demo Presentation:

A brief walkthrough of the script, annotated images, and CSV file. 


# Ideas for Improvement
Here are some ideas to make the script better in the future:

Additional Checks:

Look for bounding boxes that are too close to the edge of the image or overlap other boxes significantly, which may indicate errors.
Severity Levels:

Create different severity levels for issues: "warning" for minor problems, and "error" for serious ones. This makes it easier to prioritize fixes.
Run on the Cloud:

Set up the script to run on cloud servers so it can handle large datasets (like 250,000 images) more efficiently.
Color Analysis with OpenCV:

Use OpenCV to analyze colors inside each bounding box. For example, check if boxes labeled as "Red Traffic Light" actually contain mostly red pixels.
This would add an extra layer of validation for label accuracy and help catch errors in traffic signal labeling.
