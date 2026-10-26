import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Class 1: Store one fitness record

class FitnessActivity:
    def __init__(self, date, steps, minutes, calories):
        self.date = date
        self.steps = steps
        self.minutes = minutes
        self.calories = calories


# Class 2: Manage and analyze records

class FitnessAnalyzer:
    def __init__(self):
        self.filename = "fitness_data.csv"
        self.activities = []
        self.load_data()

    # Check date format
    def valid_date(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # Load saved records from CSV
    def load_data(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    activity = FitnessActivity(
                        row["date"],
                        int(row["steps"]),
                        int(row["minutes"]),
                        float(row["calories"])
                    )
                    self.activities.append(activity)

            print("Saved fitness data loaded successfully.")

        except (ValueError, KeyError, OSError, csv.Error):
            print("Could not load the CSV file. Check its contents.")

    # Save records permanently
    def save_data(self):
        with open(self.filename, "w", newline="") as file:
            fields = ["date", "steps", "minutes", "calories"]
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

            for activity in self.activities:
                writer.writerow({
                    "date": activity.date,
                    "steps": activity.steps,
                    "minutes": activity.minutes,
                    "calories": activity.calories
                })

    # Find a record by date
    def find_activity(self, date):
        for activity in self.activities:
            if activity.date == date:
                return activity
        return None

    # Read and validate fitness values
    def get_values(self):
        try:
            steps = int(input("Enter steps walked: "))
            minutes = int(input("Enter exercise minutes: "))
            calories = float(
                input("Enter estimated calories burned: ")
            )

            if steps < 0 or minutes < 0 or calories < 0:
                print("Values cannot be negative.")
                return None

            return steps, minutes, calories

        except ValueError:
            print("Please enter valid numeric values.")
            return None

    # Add a new record
    def add_activity(self):
        print("\n--- Add Fitness Record ---")
        date = input("Enter date (YYYY-MM-DD): ").strip()

        if not self.valid_date(date):
            print("Invalid date. Use YYYY-MM-DD format.")
            return

        if self.find_activity(date):
            print("A record for this date already exists.")
            return

        values = self.get_values()
        if values is None:
            return

        steps, minutes, calories = values
        self.activities.append(
            FitnessActivity(date, steps, minutes, calories)
        )
        self.save_data()
        print("Record added and saved successfully!")

    # Display all records
    def view_activities(self):
        print("\n--- All Fitness Records ---")

        if not self.activities:
            print("No records found.")
            return

        print(
            f"{'Date':<15}{'Steps':<12}"
            f"{'Minutes':<12}{'Calories':<12}"
        )

        for a in sorted(self.activities, key=lambda x: x.date):
            print(
                f"{a.date:<15}{a.steps:<12}"
                f"{a.minutes:<12}{a.calories:<12.1f}"
            )

    # Search by date
    def search_activity(self):
        date = input("Enter date to search (YYYY-MM-DD): ").strip()
        activity = self.find_activity(date)

        if activity:
            print("\nRecord found:")
            print("Date:", activity.date)
            print("Steps:", activity.steps)
            print("Exercise minutes:", activity.minutes)
            print("Estimated calories:", activity.calories)
        else:
            print("No record found for this date.")

    # Update a record
    def update_activity(self):
        date = input("Enter date to update (YYYY-MM-DD): ").strip()
        activity = self.find_activity(date)

        if not activity:
            print("Record not found.")
            return

        print("Enter the new values:")
        values = self.get_values()

        if values is None:
            return

        activity.steps, activity.minutes, activity.calories = values
        self.save_data()
        print("Record updated successfully!")

    # Delete a record
    def delete_activity(self):
        date = input("Enter date to delete (YYYY-MM-DD): ").strip()
        activity = self.find_activity(date)

        if not activity:
            print("Record not found.")
            return

        confirm = input("Delete this record? (y/n): ").strip().lower()

        if confirm == "y":
            self.activities.remove(activity)
            self.save_data()
            print("Record deleted successfully.")
        else:
            print("Deletion cancelled.")

    # Display statistics
    def show_summary(self):
        print("\n--- Fitness Summary ---")

        if not self.activities:
            print("No records available.")
            return

        total_steps = sum(a.steps for a in self.activities)
        total_minutes = sum(a.minutes for a in self.activities)
        total_calories = sum(a.calories for a in self.activities)
        count = len(self.activities)

        average_steps = total_steps / count
        average_minutes = total_minutes / count

        most_active = max(self.activities, key=lambda a: a.steps)

        print("Number of recorded days:", count)
        print("Total steps:", total_steps)
        print(f"Average steps per recorded day: {average_steps:.2f}")
        print("Total exercise minutes:", total_minutes)
        print(f"Average exercise minutes per day: {average_minutes:.2f}")
        print(f"Total estimated calories burned: {total_calories:.1f}")
        print(
            f"Most active day: {most_active.date} "
            f"({most_active.steps} steps)"
        )

    # Draw four visualizations
    def show_graphs(self):
        if not self.activities:
            print("No records available to plot.")
            return

        records = sorted(self.activities, key=lambda x: x.date)
        dates = [a.date for a in records]
        steps = [a.steps for a in records]
        minutes = [a.minutes for a in records]
        calories = [a.calories for a in records]

        fig, axes = plt.subplots(2, 2, figsize=(13, 9))

        # Graph 1: Steps by date
        axes[0, 0].bar(dates, steps)
        axes[0, 0].set_title("Daily Steps")
        axes[0, 0].set_ylabel("Steps")

        # Graph 2: Exercise duration
        axes[0, 1].plot(dates, minutes, marker="o")
        axes[0, 1].set_title("Exercise Duration")
        axes[0, 1].set_ylabel("Minutes")

        # Graph 3: Estimated calories
        axes[1, 0].bar(dates, calories)
        axes[1, 0].set_title("Estimated Calories Burned")
        axes[1, 0].set_ylabel("Calories")

        # Graph 4: Activity distribution
        axes[1, 1].pie(
            minutes,
            labels=dates,
            autopct="%1.1f%%",
            startangle=90
        )
        axes[1, 1].set_title("Share of Recorded Exercise Time")

        for ax in [axes[0, 0], axes[0, 1], axes[1, 0]]:
            ax.tick_params(axis="x", rotation=45)
            ax.grid(axis="y", linestyle="--", alpha=0.4)

        fig.suptitle("Fitness Activity Analysis", fontsize=16)
        fig.tight_layout()
        plt.show()

    # Main menu
    def run(self):
        while True:
            print("\n====== ADVANCED FITNESS ANALYZER ======")
            print("1. Add Fitness Record")
            print("2. View All Records")
            print("3. Search Record")
            print("4. Update Record")
            print("5. Delete Record")
            print("6. View Fitness Summary")
            print("7. Show Graphs")
            print("8. Exit")

            choice = input("Enter your choice (1-8): ").strip()

            if choice == "1":
                self.add_activity()
            elif choice == "2":
                self.view_activities()
            elif choice == "3":
                self.search_activity()
            elif choice == "4":
                self.update_activity()
            elif choice == "5":
                self.delete_activity()
            elif choice == "6":
                self.show_summary()
            elif choice == "7":
                self.show_graphs()
            elif choice == "8":
                print("Thank you for using Fitness Analyzer!")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 8.")


# Start the application
if __name__ == "__main__":
    analyzer = FitnessAnalyzer()
    analyzer.run()

