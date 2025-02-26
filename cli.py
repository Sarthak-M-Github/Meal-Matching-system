import requests

def main():
    print("Welcome to the Meal Matching System!")
    while True:
        print("\nPlease enter your nutritional preferences (0 = low, 1 = high):")
        calories = float(input("Calories (0 to 1): "))
        protein = float(input("Protein (0 to 1): "))
        fat = float(input("Fat (0 to 1): "))
        sat_fat = float(input("Saturated Fat (0 to 1): "))
        fiber = float(input("Fiber (0 to 1): "))
        carbs = float(input("Carbs (0 to 1): "))

        # Create user_preferences array
        user_preferences = [calories, protein, fat, sat_fat, fiber, carbs]

        # Send request to Flask API
        response = requests.post('http://127.0.0.1:5000/recommend', json={
            'user_preferences': user_preferences
        })

        if response.status_code == 200:
            recommendations = response.json()
            print("\nHere are your meal recommendations:")
            for meal in recommendations:
                print(f"- {meal['Food']} ({meal['Measure']}): {meal['Calories']} calories, {meal['Protein']}g protein, {meal['Fat']}g fat, {meal['Carbs']}g carbs")
        else:
            print("Error fetching recommendations. Please try again.")

        if input("\nDo you want to continue? (yes/no): ").lower() != 'yes':
            break

if __name__ == '__main__':
    main()