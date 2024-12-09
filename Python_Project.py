
# Import required modules
import csv
from graphics import GraphWin, Line, Rectangle, Text, Point

# Data for available CSV files
available_dates = {
    "15062024": "traffic_data15062024.csv",
    "16062024": "traffic_data16062024.csv",
    "21062024": "traffic_data21062024.csv"
}

# Task A: Validate date input
def validate_date():
    # Loop to get the valid day, month, and year
    while True:
        try:
            # Input day
            day = int(input("Enter the day (DD): "))
            if not (1 <= day <= 31):
                print("Error: Day must be between 1 and 31.")
                continue  # Re-prompt for the day if invalid
            
            # Input month
            month = int(input("Enter the month (MM): "))
            if not (1 <= month <= 12):
                print("Error: Month must be between 1 and 12.")
                continue  # Re-prompt for the month if invalid
            
            # Input year
            year = int(input("Enter the year (YYYY): "))
            if not (2000 <= year <= 2024):
                print("Error: Year must be between 2000 and 2024.")
                continue  # Re-prompt for the year if invalid

            # Construct date string to check if data is available
            date_str = f"{day:02d}{month:02d}{year}"

            # Check if date exists in available dates
            if date_str not in available_dates:
                print("Error: Data not available for this date. Please try again.")
                continue  # Re-prompt for the entire date if it's not available

            # If all inputs are valid, return the corresponding file
            return available_dates[date_str], date_str, day, month, year

        except ValueError:
            print("Error: Please enter a valid number for day, month, or year.")

# Task B: Analyze data
def analyze_data(file_path):
    results = {}
    try:
        with open(file_path, 'r') as file:
            data = list(csv.DictReader(file))
        
        # Total vehicles
        results["Total Vehicles"] = len(data)
        results["Total Trucks"] = sum(1 for row in data if row["VehicleType"] == "Truck")
        results["Electric Vehicles"] = sum(1 for row in data if row["electricHybrid"] == "TRUE")
        results["Two-Wheeled Vehicles"] = sum(1 for row in data if row["VehicleType"] in ["Bike", "Motorbike", "Scooter"])
        results["Buses North"] = sum(1 for row in data if row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["travel_Direction_out"] == "N" and row["VehicleType"] == "Bus")
        results["Non-Turning Vehicles"] = sum(1 for row in data if row["travel_Direction_in"] == row["travel_Direction_out"])
        results["Trucks Percentage"] = round((results["Total Trucks"] / results["Total Vehicles"]) * 100)
        results["Avg Bicycles Per Hour"] = round(sum(1 for row in data if row["VehicleType"] == "Bike") / 24)
        results["Over Speed"] = sum(1 for row in data if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]))
        results["Elm Vehicles"] = sum(1 for row in data if row["JunctionName"] == "Elm Avenue/Rabbit Road")
        results["Hanley Vehicles"] = sum(1 for row in data if row["JunctionName"] == "Hanley Highway/Westway")
        results["Elm Scooters Percentage"] = round(sum(1 for row in data if row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["VehicleType"] == "Scooter") / results["Elm Vehicles"] * 100)
        
        # Peak hour and rain hours
        results["Peak Hour Hanley"], results["Peak Hour Traffic"] = get_peak_hour(data, "Hanley Highway/Westway")
        results["Rain Hours"] = sum(1 for row in data if row["Weather_Conditions"] == "Rain")
    except Exception as e:
        print(f"Error processing data: {e}")
    return results

def get_peak_hour(data, junction):
    hourly_counts = {}
    for row in data:
        if row["JunctionName"] == junction:
            hour = row["timeOfDay"].split(":")[0]
            hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
    peak_hour = max(hourly_counts, key=hourly_counts.get)
    peak_traffic = hourly_counts[peak_hour]
    return f"Between {peak_hour}:00 and {int(peak_hour)+1}:00", peak_traffic

# Task C: Save results to a text file
def save_results(results, date):
    try:
        file_name = f"results_{date}.txt"
        with open(file_name, 'w') as file:
            for key, value in results.items():
                file.write(f"{key}: {value}\n")
        print(f"Results saved to {file_name}.")
    except Exception as e:
        print(f"Error saving results: {e}")

# Task D: Function to plot histogram
from graphics import GraphWin, Line, Rectangle, Text, Point


def color_rgb(r, g, b):
    """Convert RGB values to a hexadecimal color format for graphics.py."""
    return f'#{r:02x}{g:02x}{b:02x}'


# Function to plot histogram
def plot_traffic_histogram(traffic_data, selected_date):
    # Extract hourly data for each junction
    elm_data = [0] * 24
    hanley_data = [0] * 24

    for row in traffic_data:
        hour = int(row["timeOfDay"].split(":")[0])
        if row["JunctionName"] == "Elm Avenue/Rabbit Road":
            elm_data[hour] += 1
        elif row["JunctionName"] == "Hanley Highway/Westway":
            hanley_data[hour] += 1

    # Create GraphWin
    win_width = 1000
    win_height = 700
    win = GraphWin(f"Histogram of Vehicle Frequency per Hour ({selected_date})", win_width, win_height)

    # Define plot dimensions
    margin = 50
    plot_width = win_width - 2 * margin
    plot_height = win_height - 2 * margin
    bar_width = plot_width / 24  # One bar per hour

    # Draw x-axis and y-axis
    x_axis = Line(Point(margin, win_height - margin), Point(win_width - margin, win_height - margin))
    x_axis.draw(win)
    y_axis = Line(Point(margin, margin), Point(margin, win_height - margin))
    y_axis.draw(win)

    # Find maximum y value for scaling
    max_y = max(max(elm_data), max(hanley_data))

    # Draw bars and add labels
    for hour in range(24):
        # Scale values for the plot
        elm_height = (elm_data[hour] / max_y) * plot_height
        hanley_height = (hanley_data[hour] / max_y) * plot_height

        # Draw Elm Avenue bar (dull green)
        elm_bar = Rectangle(
            Point(margin + hour * bar_width, win_height - margin - elm_height),
            Point(margin + hour * bar_width + bar_width / 2, win_height - margin)
        )
        elm_bar.setFill(color_rgb(144, 238, 144))  # Light green
        elm_bar.draw(win)

        # Add frequency label to Elm Avenue bar
        elm_label = Text(
            Point(margin + hour * bar_width + bar_width / 4, win_height - margin - elm_height - 10),
            str(elm_data[hour])
        )
        elm_label.setSize(8)
        elm_label.draw(win)

        # Draw Hanley Highway bar (dull red)
        hanley_bar = Rectangle(
            Point(margin + hour * bar_width + bar_width / 2, win_height - margin - hanley_height),
            Point(margin + (hour + 1) * bar_width, win_height - margin)
        )
        hanley_bar.setFill(color_rgb(240, 128, 128))  # Light red
        hanley_bar.draw(win)

        # Add frequency label to Hanley Highway bar
        hanley_label = Text(
            Point(margin + hour * bar_width + 3 * bar_width / 4, win_height - margin - hanley_height - 10),
            str(hanley_data[hour])
        )
        hanley_label.setSize(8)
        hanley_label.draw(win)

        # Add hour labels
        hour_label = Text(Point(margin + hour * bar_width + bar_width / 2, win_height - margin + 10), str(hour))
        hour_label.setSize(8)
        hour_label.draw(win)

    # Add title
    title = Text(Point(win_width / 2, margin / 2), f"Histogram of Vehicle Frequency per Hour ({selected_date})")
    title.setSize(12)
    title.setStyle("bold")
    title.draw(win)

    # Axis labels
    x_label = Text(Point(win_width / 2, win_height - margin / 3), "Hours 00:00 to 24:00")
    x_label.setSize(10)
    x_label.draw(win)

    # Add legend
    legend_x = margin + 10  # X-coordinate for the legend
    legend_y = margin + 10     # Y-coordinate for the legend
    text_offset = 120          # Increased horizontal spacing between rectangles and labels

    # Draw Elm Avenue/Rabbit Road legend
    legend_el_rect = Rectangle(Point(legend_x, legend_y), Point(legend_x + 30, legend_y + 15))  # Rectangle size adjusted for better visibility
    legend_el_rect.setFill(color_rgb(144, 238, 144))  # Light green
    legend_el_rect.draw(win)

    legend_el_label = Text(Point(legend_x + text_offset, legend_y + 7.5), "Elm Avenue/Rabbit Road")  # Shifted farther to the right
    legend_el_label.setSize(10)
    legend_el_label.draw(win)

    # Draw Hanley Highway/Westway legend
    legend_han_rect = Rectangle(Point(legend_x, legend_y + 30), Point(legend_x + 30, legend_y + 45))  # Adjusted for next line
    legend_han_rect.setFill(color_rgb(240, 128, 128))  # Light red
    legend_han_rect.draw(win)

    legend_han_label = Text(Point(legend_x + text_offset, legend_y + 37.5), "Hanley Highway/Westway")  # Shifted farther to the right
    legend_han_label.setSize(10)
    legend_han_label.draw(win)

    # Keep window open until clicked
    win.getMouse()
    win.close()



# Main function to manage flow
# Task E: Loop to load and process a new dataset
def main():
    while True:
        # Step 1: Get validated date and corresponding file
        file_name, selected_date, day, month, year = validate_date()
    
        # Step 2: Load CSV data
        import csv
        traffic_data = []
        with open(file_name, "r") as file:
            reader = csv.DictReader(file)
            traffic_data = [row for row in reader]
        
        # Step 3: Analyze the data
        print(f"Analyzing data for {selected_date}...")
        results = analyze_data(file_name)
        
        # Step 4: Display results
        for key, value in results.items():
            print(f"{key}: {value}")
        
        # Step 5: Save results
        save_results(results, selected_date)
        
        # Step 6: Generate histogram
        print("Generating histogram...")
        # Combine them into the desired format
        formatted_date = f"{int(day):02d}/{int(month):02d}/{int(year)}"
        plot_traffic_histogram(traffic_data, formatted_date)

        # Step 7: Ask if the user wants to process data for another date
        while True:
            continue_choice = input("Do you want to select a data file for a different date? (Y/N): ").strip().lower()
            if continue_choice == 'y':
                break  # Continue to the next iteration and load a new date
            elif continue_choice == 'n':
                print("Exiting the program.")
                return  # Exit the program
            else:
                print("Invalid input. Please enter 'Y' for yes or 'N' for no.")
                
if __name__ == "__main__":
    main()
