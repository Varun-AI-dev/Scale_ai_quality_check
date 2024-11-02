import json
import csv  # Required for writing data to CSV files
import requests  # For downloading images from URLs
import os  # For checking if files exist on disk
from PIL import Image, ImageDraw  # For opening, modifying, and saving images

# Load tasks from a JSON file
def load_tasks(file_path):
    # Open the specified file and load its contents as JSON data
    with open(file_path, 'r') as file:
        return json.load(file)  # Returns the JSON data as a Python dictionary

# Calculate bounding box areas and flag deviations
def calculate_area_deviations(task):
    # This function finds the average area of all bounding boxes
    # and flags any box that deviates from this average by more than 90%
    
    # Step 1: Calculate the area for each bounding box in the task
    areas = []
    for annotation in task["response"]["annotations"]:
        width = abs(annotation["width"])  # Get absolute width
        height = abs(annotation["height"])  # Get absolute height
        
        # Calculate area as width * height and add it to our list of areas
        area = width * height
        areas.append(area)

    # Step 2: Find the average area
    average_area = sum(areas) / len(areas) if areas else 0  # Avoid division by zero

    # Step 3: Check if each bounding box has an area that deviates by more than 90%
    for annotation, area in zip(task["response"]["annotations"], areas):
        # Calculate the percentage deviation from the average area
        deviation = abs(area - average_area) / average_area if average_area > 0 else 0
        if deviation > 0.9:  # Flag if >90% deviation
            annotation["issues"] = "red Bounding box area error"  # Mark issue if deviation > 90%
            annotation["deviation_percent"] = deviation * 100  # Store deviation as a percentage

# Download and annotate the image with bounding boxes
def download_and_annotate_image(task):
    # Retrieve the image URL from the task data
    image_url = task["params"]["attachment"]
    image_filename = f"{task['task_id']}_annotated.png"

    # Download image if it does not already exist
    if not os.path.exists(image_filename):
        response = requests.get(image_url)
        with open(image_filename, 'wb') as f:
            f.write(response.content)  # Save the image locally

    # Open and annotate the image
    image = Image.open(image_filename)  # Open image with PIL
    draw = ImageDraw.Draw(image)
    
    # Draw bounding boxes on the image, marking flagged issues in red and others in blue
    for annotation in task["response"]["annotations"]:
        left, top = annotation["left"], annotation["top"]
        width, height = annotation["width"], annotation["height"]
        # Set box color based on whether the annotation has an issue
        box_color = "red" if "issues" in annotation else "blue"
        # Draw the bounding box with the chosen color
        draw.rectangle([left, top, left + width, top + height], outline=box_color, width=3)

    # Save the annotated image
    annotated_image_path = f"annotated_{image_filename}"
    image.save(annotated_image_path)
    return annotated_image_path  # Return the path to the annotated image

# Calculate and assign ratings for each task
def assign_quality_rating(task):
    # Initialize an empty list to collect any issues found
    issues = []
    # Initialize default ratings to Gold (highest score)
    audit_rating = 1
    area_rating = 1
    label_rating = 1
    occlusion_rating = 1

    # Step 1: Check the audit results to see if the task was rejected multiple times
    rejection_count = sum(1 for audit in task.get("audits", []) if audit["audit_result"] == "rejected")
    total_audits = len(task.get("audits", []))
    audit_issue_percentage = (rejection_count / total_audits) * 100 if total_audits > 0 else 0

    # Set the audit rating based on rejection percentage
    if audit_issue_percentage >= 80:
        audit_rating = 0  # Bronze rating
    elif audit_issue_percentage >= 50:
        audit_rating = 0.5  # Silver rating
    else:
        audit_rating = 1  # Gold rating
    if audit_rating < 1:
        issues.append(f"Audit rejection rate: {audit_issue_percentage:.2f}%")

    # Step 2: Check for bounding box area deviations
    calculate_area_deviations(task)
    area_issues = sum(1 for annotation in task["response"]["annotations"] if "issues" in annotation)
    total_annotations = len(task["response"]["annotations"])
    area_issue_percentage = (area_issues / total_annotations) * 100 if total_annotations > 0 else 0

    # Set area rating based on deviation issues
    if area_issue_percentage >= 80:
        area_rating = 0  # Bronze
    elif area_issue_percentage >= 50:
        area_rating = 0.5  # Silver
    else:
        area_rating = 1  # Gold
    if area_rating < 1:
        issues.append(f"Bounding box area deviation issues: {area_issue_percentage:.2f}%")

    # Step 3: Check label accuracy
    label_issues = sum(1 for annotation in task["response"]["annotations"]
                       if annotation["label"] not in {"traffic_control_sign", "construction_sign", 
                                                      "information_sign", "policy_sign", "non_visible_face"})
    label_issue_percentage = (label_issues / total_annotations) * 100 if total_annotations > 0 else 0

    # Set label rating based on accuracy issues
    if label_issue_percentage >= 80:
        label_rating = 0  # Bronze
    elif label_issue_percentage >= 50:
        label_rating = 0.5  # Silver
    else:
        label_rating = 1  # Gold
    if label_rating < 1:
        issues.append(f"Label accuracy issues: {label_issue_percentage:.2f}%")

    # Step 4: Check occlusion percentage
    occlusion_issues = sum(1 for annotation in task["response"]["annotations"]
                           if annotation["attributes"].get("occlusion", "0%") in ["50%", "75%", "100%"])
    occlusion_issue_percentage = (occlusion_issues / total_annotations) * 100 if total_annotations > 0 else 0

    # Set occlusion rating based on occlusion issues
    if occlusion_issue_percentage >= 80:
        occlusion_rating = 0  # Bronze
    elif occlusion_issue_percentage >= 50:
        occlusion_rating = 0.5  # Silver
    else:
        occlusion_rating = 1  # Gold
    if occlusion_rating < 1:
        issues.append(f"High occlusion rate: {occlusion_issue_percentage:.2f}%")

    # Calculate the final rating based on the average of individual ratings
    final_score = sum([audit_rating, area_rating, label_rating, occlusion_rating]) / 4
    if final_score >= 0.9:
        final_rating = "Gold"
    elif final_score >= 0.8:
        final_rating = "Silver"
    else:
        final_rating = "Bronze"

    # Return all ratings and issues in a dictionary
    return {
        "audit_rating": audit_rating,
        "area_rating": area_rating,
        "label_rating": label_rating,
        "occlusion_rating": occlusion_rating,
        "final_rating": final_rating,
        "issues": issues
    }

# Save the ratings and annotations to a CSV file
def save_ratings_to_csv(tasks, csv_file):
    # Open the CSV file to write
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(["Task ID", "Audit Rating", "Area Rating", "Label Rating", "Occlusion Rating", "Final Rating", "Annotated Image Path", "Issues"])

        for task in tasks:
            # Get ratings and annotated image for each task
            rating_info = assign_quality_rating(task)
            annotated_image_path = download_and_annotate_image(task)
            # Write a row with all relevant information
            writer.writerow([
                task["task_id"],
                rating_info["audit_rating"],
                rating_info["area_rating"],
                rating_info["label_rating"],
                rating_info["occlusion_rating"],
                rating_info["final_rating"],
                annotated_image_path,
                "; ".join(rating_info["issues"])  # Join all issues in a single cell
            ])

# Main execution - load tasks, process ratings, and save to CSV
tasks = load_tasks("all_tasks_data.json")
save_ratings_to_csv(tasks, "task_ratings.csv")
