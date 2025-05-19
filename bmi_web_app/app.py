from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def health_calculator():
    if request.method == 'POST':
        try:
            name = request.form['name']
            age = int(request.form['age'])
            gender = request.form['gender']
            weight = float(request.form['weight'])
            height_m = float(request.form['height'])
            height_cm = height_m * 100
            activity_level = int(request.form['activity'])
            goal = int(request.form['goal'])

            if height_m <= 0 or weight <= 0 or age <= 0:
                return render_template("result.html", error="Height, weight, and age must be greater than zero.")

            bmi = weight / (height_m ** 2)
            if bmi < 18.5:
                bmi_category = "Underweight"
            elif 18.5 <= bmi < 24.9:
                bmi_category = "Normal weight"
            elif 25 <= bmi < 29.9:
                bmi_category = "Overweight"
            else:
                bmi_category = "Obese"

            ideal_min_weight = 18.5 * (height_m ** 2)
            ideal_max_weight = 24.9 * (height_m ** 2)

            activity_factors = {
                1: 1.2,
                2: 1.375,
                3: 1.55,
                4: 1.725,
                5: 1.9
            }

            if gender == 'M':
                bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
            elif gender == 'F':
                bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
            else:
                return render_template("result.html", error="Invalid gender.")

            daily_calories = bmr * activity_factors[activity_level]

            goal_note = "Maintain current weight"
            goal_calories = daily_calories
            exercise_plan = ""

            if goal == 2:
                goal_calories -= 500
                goal_note = "Lose ~0.5 kg/week"
                exercise_plan = "Recommended: Cardio, calorie deficit, 500 kcal/day burn."
            elif goal == 3:
                goal_calories += 500
                goal_note = "Gain ~0.5 kg/week"
                exercise_plan = "Recommended: Strength training, calorie surplus, protein-rich diet."

            return render_template("result.html",
                                   name=name,
                                   age=age,
                                   gender=gender,
                                   height=height_m,
                                   weight=weight,
                                   bmi=round(bmi, 2),
                                   bmi_category=bmi_category,
                                   ideal_min=round(ideal_min_weight, 1),
                                   ideal_max=round(ideal_max_weight, 1),
                                   bmr=round(bmr, 2),
                                   daily_calories=round(daily_calories, 2),
                                   goal_calories=round(goal_calories, 2),
                                   goal_note=goal_note,
                                   exercise_plan=exercise_plan)

        except Exception as e:
            return render_template("result.html", error="Invalid input. Please enter valid numbers.")

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
