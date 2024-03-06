from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import random

class FitnessChatbot(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fitness_responses = {
            "workout": ["Exercise is important for maintaining good health.", 
                        "What type of workout are you interested in?"],
            "diet": ["Eating a balanced diet is essential for overall health.",
                     "Are you looking for information on a specific diet?"],
            "weight loss": ["Weight loss is often achieved through a combination of diet and exercise.",
                            "Have you considered consulting a nutritionist or personal trainer?"],
            "workout": ["Exercise is important for maintaining good health.", 
                "What type of workout are you interested in?"],
            "diet": ["Eating a balanced diet is essential for overall health.",
                    "Are you looking for information on a specific diet?"],
            "weight loss": ["Weight loss is often achieved through a combination of diet and exercise.",
                            "Have you considered consulting a nutritionist or personal trainer?"],
            "muscle building": ["Strength training exercises can help build muscle mass.",
                                "Are you interested in bodyweight exercises or weightlifting?"],
            "cardio": ["Cardiovascular exercises like running, cycling, and swimming can improve endurance.",
                    "How often do you currently engage in cardio exercises?"],
            "How can I lose weight?":["To lose weight, focus on a balanced diet and regular exercise. Consider a mix of cardio and strength training."],
            "What are good protein sources for muscle building?":["Foods like chicken, fish, eggs, and beans are excellent sources of protein for muscle building."],
            "What should I eat before a workout?":["Consume a mix of carbohydrates and protein about 2-3 hours before a workout. Opt for easily digestible foods, such as a banana with yogurt or whole-grain toast with nut butter, if eating closer to exercise."],
            "Can you recommend a balanced meal plan for weight loss?":["•	Focus on a calorie deficit by incorporating whole foods like lean proteins, vegetables, fruits, and whole grains. Balance macronutrients and stay hydrated."],
            "How much protein do I need in a day?":["Aim for 0.8 to 1 gram of protein per pound of body weight for general fitness. Athletes and those engaging in intense workouts may need more."],
            "What are good snacks for post-workout recovery?":['Opt for a combination of protein and carbohydrates, such as a protein shake with a piece of fruit or Greek yogurt with berries.'],
            "Are there any specific foods that can boost metabolism?":["•	Foods like green tea, spicy peppers, and lean proteins may have a slight impact on metabolism, but overall, building muscle through exercise contributes more to a higher metabolism."],
            "How do I perform a proper squat?":["•	Stand with feet shoulder-width apart, lower your body as if sitting back into a chair, keeping your back straight. Lower until your thighs are parallel to the ground."],
            "What's the correct form for a push-up?":["•	Keep your body in a straight line from head to heels, engage your core, and lower your chest to the ground, then push back up."],
            "Can you explain the benefits of high-intensity interval training (HIIT)?":["•	HIIT alternates between short bursts of intense exercise and rest, promoting calorie burn, cardiovascular health, and efficiency in a shorter workout time."],
            "What's the best way to stretch before exercising?":["•	Dynamic stretches like leg swings and arm circles are ideal before a workout. Save static stretches for after your workout."],
            "How can I improve my flexibility?":["•	Incorporate regular stretching and yoga into your routine. Focus on major muscle groups and hold stretches for at least 15-30 seconds."],
            "What's a good beginner's weightlifting routine?":["•	Start with compound exercises like squats, deadlifts, and bench presses. Begin with lighter weights and gradually increase as you become comfortable."],
            "How often should I change my strength training routine?":["•	Change routines every 8-12 weeks to prevent plateaus. Modify exercises, sets, and repetitions for continuous progress."],
            "Can you recommend exercises for building specific muscle groups?":["For chest: bench press, for legs: squats, for back: rows, for arms: bicep curls and tricep dips."],
            "What's the importance of rest days in a workout plan?":["•	Rest days allow muscles to recover and grow. Overtraining can lead to fatigue, increased risk of injury, and stalled progress"],
            "How much cardio should I include in my weekly workout routine?":["•	Aim for at least 150 minutes of moderate-intensity cardio or 75 minutes of vigorous-intensity cardio per week, along with strength training"],
            "What are effective cardio exercises I can do at home?":["•	Jumping jacks, high knees, burpees, and dance workouts are effective home cardio exercises"],
            "Is it better to do cardio before or after weightlifting?":["Generally, it's better to do cardio after weightlifting to preserve energy for strength training."],
            "Can you suggest a running plan for beginners?":["Start with a run/walk routine, gradually increasing running time. For example, run for 1 minute, walk for 2 minutes, repeat."],
            "What are the benefits of getting enough sleep for fitness?":["Sleep aids muscle recovery, hormone regulation, and overall physical and mental well-being"],
            "How can I prevent and treat muscle soreness?":["Stay hydrated, engage in a proper warm-up and cool-down, consider foam rolling, and get adequate protein.Are there any supplements you recommend "],
            "Are there any supplements you recommend for fitness enthusiasts":['•	Consider supplements like protein powder, creatine, and omega-3 fatty acids, but consult with a healthcare professional first.'],
            "What's the importance of hydration during and after exercise?":['•	Hydration is crucial for performance, preventing dehydration, and supporting recovery. Drink water before, during, and after exercise.'],
            "How can I set realistic fitness goals?":["Set specific, measurable, achievable, relevant, and time-bound (SMART) goals. Start with small milestones and adjust as needed."],
            "Can you recommend a fitness app for tracking workouts?":["Popular fitness apps include MyFitnessPal, Strava, and Nike Training Club"],
            "How often should I reassess my fitness goals?":["Reassess every 8-12 weeks to evaluate progress and adjust goals accordingly."],
            "How do I stay motivated to exercise regularly?":["Set realistic goals, find activities you enjoy, work out with a friend, and vary your routine."],
            "What are some tips for overcoming workout plateaus?":["Change your routine, increase intensity, try new exercises, and ensure adequate rest."],
            "Can you suggest ways to make workouts more enjoyable?":["Choose activities you love, listen to music, join group classes, or exercise outdoors."],
            "How important is consistency in a fitness routine?":["•	Consistency is crucial for long-term success. Regular exercise yields more benefits than sporadic intense workouts."],
            "Can you provide workout suggestions for seniors?":['•	Seniors should focus on low-impact activities like walking, swimming, and gentle strength training. Always consult with a healthcare professional.'],
            "Are there specific considerations for fitness during menstruation?":["•	Adjust intensity as needed, stay hydrated, and choose exercises that alleviate discomfort. Listen to your body and rest when necessary."],


    # Add more responses as needed
        }

    def build(self):
        Window.clearcolor = (0.5, 0, 1, 1)  # Set background color to purple
        layout = BoxLayout(orientation='vertical')

        # Chatbot response label
        self.chatbot_label = Label(text="Chatbot", size_hint=(1, 0.9), color=(1, 1, 1, 1))
        layout.add_widget(self.chatbot_label)

        # Search button
        search_button = Button(text="Search", size_hint=(1, 0.1), on_press=self.search)
        layout.add_widget(search_button)

        return layout

    def search(self, instance):
        user_input = "How can I lose weight?"  # You can replace this with actual user input from a text input field
        response = None
        for query, answers in self.fitness_responses.items():
            if query in user_input:
                response = random.choice(answers)
                break
        if response:
            self.chatbot_label.text = response
        else:
            self.chatbot_label.text = "I'm sorry, I didn't understand that."

if __name__ == "__main__":
    FitnessChatbot().run()
