# Deliverable 7

## Description  
PennyPilot is a personal finance management tool tailored for students preparing to study abroad. The system helps users calculate savings goals by considering their travel timeline, destination, and current financial status. It generates personalized daily, weekly, and monthly savings targets, providing actionable insights and visual feedback to keep users on track. With a focus on simplicity and clarity, PennyPilot empowers users to effectively plan their finances and stay motivated toward achieving their study-abroad dreams.

The application connects to a MySQL database to manage and update trip-related data, tracks savings progress over time, and dynamically refreshes visual charts using Python’s Tkinter for the GUI. PennyPilot ensures an intuitive user experience, making complex financial planning both accessible and engaging.

---

## Verification

### Test Framework  
`pytest` (Python Standard Library)

### GitHub Repository (Unit Tests)  
\[[GitHub Link](https://github.com/sesartrumpet/cs386-pennypilot/tree/main/tests/backend)\]

### Example Test Case with Mock Objects  
Initialization logic for Finance class in [test_utilities.py](https://github.com/sesartrumpet/cs386-pennypilot/blob/main/tests/backend)

### Test Execution Screenshot  
![Test Pass Success](Deliverable7_images/tests_passed.png)
---

## Acceptance Test

### Test Framework
`PyAutoGUI`

### GitHub Repository (Acceptance Tests)
[GitHub Link](https://github.com/sesartrumpet/cs386-pennypilot/tree/main/tests/Frontend)

### Example Acceptance Test
An example acceptance test verifies all major input combinations on the Create Account page. This test ensures proper form validation by automating inputs for blank fields, password mismatches, invalid emails, restricted usernames, and valid submissions.  
[GitHub Link](https://github.com/sesartrumpet/cs386-pennypilot/tree/main/tests/Frontend/test_screenshots/Test1)  
The test uses PyAutoGUI to simulate user actions and captures before/after screenshots to confirm system responses. This ensures the form correctly handles errors and successfully creates valid accounts.  

### Test Execution Screenshot or Video
[Test Video](https://youtu.be/pyZMF5DkXDU?si=EeQ0ZRdHBjp2TWD_)
---

## Validation

### Participant 1 Evaluation (Completed by Victor Rodriguez)

#### Results

**Task Completion Time:**

- Task 1 (Create a New Trip): 3 minutes
- Task 2 (Update Savings): 2 minutes
- Task 3 (View Trip Breakdown): 4 minutes

**Ratings:**

1. Creating a Trip: 8/10
   - *Explanation:* The user found the process intuitive and straightforward, requiring minimal effort to complete. There's still room for improvement in user interface clarity or guidance.

2. Saving Progress Update: 7/10
   - *Explanation:* While the user was able to update their savings, they felt the feature could be more seamless or better integrated with other features. Slight confusion in the savings progress tracking was noted.

3. Trip Breakdown: 9/10
   - *Explanation:* The user found the trip breakdown feature clear and easy to navigate. The expense categories were helpful, and there were no major issues in understanding or interacting with the data.

**Feedback:**

> "The app is pretty easy to use, but it would be great if I could add custom categories for expenses. I think the bar graph could be more prominent."

### Participant 2 Evaluation (Completed by Manjot Kaur)

#### Results

**Task Completion Time:**

- Task 1 (Create a New account): 2 minutes
- Task 2 (Create a New Trip): 1 minutes
- Task 3 (Update Savings): 1 minutes
- Task 4 (View Trip Breakdown): 1 minutes

**Ratings:**

1. Creating a account: 8/10
   - *Explanation:*
   - The user found it easy to create the account but was a bit confused with the login page.
     
2. Creating a Trip: 10/10
   - *Explanation:*
   - The user created the trip easily as it was simple and straightforward.
     
3. Saving Progress Update: 10/10
   - *Explanation:*
   - The user thought the website was helpful and really quick in its calculations. 
     
4. Trip Breakdown: 9/10
   - *Explanation:*
   -  The user was able to get a trip breakdown that was easy to understand. 
**Feedback:**

> "Overall the app is very quick with its processing and very user-friendly, however maybe the tables and charts could be a little confusing and hard to understand for newer users."

#### Reflection

**Observations:**

- The user completed all tasks with little difficulty, indicating that the core features of the app are functional and user-friendly.
- The suggestion to add custom categories for expenses reflects a need for more flexibility in how users manage their trip budgets. This could improve the app's usability for users with diverse needs.
- The user's feedback about the progress bar suggests that a more prominent visual representation of savings could enhance the overall user experience, making it more engaging and easier to track goals.

**What Worked Well:**

- The process of creating a new trip was clear and intuitive, with users able to quickly set up trips with ease.
- The trip breakdown feature received positive feedback, indicating that the categorization of expenses and the data presentation were well-received.

**Areas for Improvement:**

- Custom categories for expenses could make the app more versatile, catering to a broader range of users.
- Enhancing the visibility and prominence of the savings progress bar could improve user engagement and help users track their goals more effectively.

### Participant 3 Evaluation (Completed by Sesar Parra)

#### Results

**Task Completion Time:**

- Task 1 (Create a New account): 1 minute
- Task 2 (Create a New Trip): 2 minutes
- Task 3 (Update Savings): 1 minute
- Task 4 (View Trip Breakdown): 2 minutes

**Ratings:**

1. Creating a Trip: 9/10
   - *Explanation:* The user got the hang of the application pretty quickly. Everything seemed fine to him, although he thought adding symbols to buttons would be nice.

2. Saving Progress Update: 6/10
   - *Explanation:* The user was able to input an amount but was unsure whether he could add increments or he would have to add the total to the savings progress, which was kind of confusing for the user

3. Trip Breakdown: 9/10
   - *Explanation:* Around the same as participant 1, the user was able to understand the breakdown of the trip.

**Feedback:**

> "The app could use some touch ups, but they should be very minor. Overall, I thought the application was understandable and easy to navigate."

#### Reflection

**Observations:**

- The participant completed all three tasks quickly, with the total time being 5 minutes.
- Uncertainty around incrementing versus total savings shows that the labels for savings goal could be more explicit
- The suggestion about adding symbols to symbols to buttons shows that there can still be more to add.

**What Worked Well:**

- User was able to create a new trip without any guidance from me, showing that it is easy to navigate
- Trip Breakdown visualization meets user expectations for clarity and comprehensiveness
- Overall layout and language appears to be user-friendly

**Areas for Improvement:**

- Clarify savings update control, add a label showing what adding savings does.
- Add icon labels to improve user-friendliness.


### Participant 4 Evaluation (Completed by Vikram Singh)

#### Results

**Task Completion Time:**

- Task 1 (Create a New account): 1 minute
- Task 2 (Create a New Trip): 1 minute
- Task 3 (Update Savings): 1 minute
- Task 4 (View Trip Breakdown): 2 minutes

**Ratings:**

1. Creating a Trip: 8/10
   - *Explanation:* The participant was able to create a trip and goal pretty easily. He claimed it was efficient and straightforward.

2. Saving Progress Update: 6/10
   - *Explanation:* Around the same as participant 3, Participant did not know what the savings goal labels meant.
     
3. Trip Breakdown: 9/10
   - *Explanation:* The trip breakdown was easy to read and comprehend by the participant. 

**Feedback:**

> "User interface was clean and organized. I understood what the program was doing."

#### Reflection

**Observations:**

- Participant was able to figure out Penny Pilot pretty quickly, indicating our application has good base functionality and usability
- The confusion on savings goal labels suggests that said labels were not explicit or clear enough
- According to the participant, our program lacked visual components
  
**What Worked Well:**

- Our clean user interface worked pretty well to help the participant understand what the application was doing
- The ease of creating a trip and saving a goal shows that our program is very user-friendly
  
**Areas for Improvement:**

- Add explicit label to show what saving a goal does
- Add more visual components to make program more appealing to use
