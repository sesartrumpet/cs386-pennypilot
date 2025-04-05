# Description
Penny Pilot is a desktop GUI application built with Python, Tkinter, and MySQL,  
designed to help students plan and track savings for study abroad trips.  
The system focuses on simplicity by only asking for three key inputs: destination,  
current savings, and trip timeline. Once all three fields are filled out,  
the interface transitions to a dedicated “Progress Screen” where users can monitor  
and update their savings over time. The savings goal is automatically calculated  
based on the location and timeline, and a visual breakdown is shown to help users  
stay on track. 
When the user reopens the app, they are brought directly to the Progress Screen  
to continue updating their savings. Whenever savings are updated, both the savings  
breakdown and goal chart dynamically reflect the new data to provide real-time  
feedback. This ensures users can clearly see how their progress has changed and  
what remains to be saved. Only if the user decides to change trip details—such  
as the destination or timeline—does the app return to the initial “Select Trip”  
screen. This streamlined design keeps the user focused on goal progress while  
minimizing distractions, aligning with Penny Pilot’s mission to make trip planning  
straightforward and motivating.    

# Architecture    

# Class Diagrams   

# Sequence Diagrams   

![image](Deliverable5_images/Sequence%20Diagram.png)

| Use Case         | Viewing Trip Details                                                                                                                      |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Summary          | This use case describes the process where the user selects a trip from the dropdown of trips, and then the application returns the trip price breakdown. |
| Actors           | Student                                                                                                                                   |
| Preconditions    | Student is logged into the PennyPilot app and at least one trip exists in the database.                                                   |
| Basic sequence   | 1. **Student** clicks on the trip dropdown in the PennyPilotApp interface.  <br> 2. **PennyPilotApp** sends a request to **Controllers** to retrieve available trips via the `get_trips()` method.  <br> 3. **Controllers** request trip data from the **Database** using the `get_trips()` method.  <br> 4. **Database** returns a list of trips to the **Controllers**.  <br> 5. **Controllers** pass the list of trips to the **PennyPilotApp**.  <br> 6. **PennyPilotApp** displays the list of trips in a dropdown menu.  <br> 7. **Student** selects a specific trip from the dropdown.  <br> 8. **PennyPilotApp** calls the `update_expense_breakdown(location)` function in the **Controllers**.  <br> 9. **Controllers** call the `get_price_breakdown_by_trip_name(location)` function in the **Database**.  <br> 10. **Database** returns the price breakdown to **Controllers**.  <br> 11. **Controllers** return the price breakdown data to the **PennyPilotApp**.  <br> 12. **PennyPilotApp** displays the price breakdown to the **Student**. |
| Alternate Sequence | 1. If no trips are available, the application will throw an error and the user will not be able to select any trips |
| Postconditions   | The user successfully views the detailed price breakdown of the selected trip.                                                           |

# Design Patterns     
Penny Pilot uses two classic software design patterns to enhance modularity, maintainability, and data synchronization: the **Observer Pattern** (Behavioral) and the **Singleton Pattern**(Creational). Each was selected based on its practical application within the savings-tracking architecture of the system.   

- **Observer Pattern(Behavioral)**
The Observer Pattern is used in Penny Pilot to dynamically update the UI whenever the savings value changes. This makes the savings interface reactive and ensures the user always sees up-to-date progress and goal information without manual refresh or reload actions.
https://github.com/sesartrumpet/cs386-pennypilot/blob/main/Reports/Deliverable5_images/Observer%20Pattern.drawio.png

  
- **Singleton Pattern(Creational)**
The Singleton Pattern is used in Penny Pilot to manage the MySQL database connection efficiently. It ensures that the application always uses the same database instance throughout the user session, avoiding the creation of multiple unnecessary connections.
https://github.com/sesartrumpet/cs386-pennypilot/blob/main/Reports/Deliverable5_images/Singleton%20Pattern.drawio.png

 


# Design Principles  git 
