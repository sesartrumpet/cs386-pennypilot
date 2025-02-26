# System Description
Provide a brief textual description of your system. The first paragraph of the description must contain the problem statement, the product position statement, and the value proposition of your system (you can refine/update what you presented in D.2). The following paragraphs should describe the key requirements of the system. This description should be consistent with D.2 stakeholders, requirements, use cases, and user stories. Again, refinements/updates are welcome since your understanding of the system is constantly evolving. 

Use Bold every time that you use a noun that is a class in your model. Use Italic every time that you use a noun that is an attribute in your model. Use Bold and Italic every time that you use a noun or verb that is an association in your model. 

Grading criteria (5 points): The description should be clear, concise, and well-written, free of typos and grammar problems. The use of bold, italic, and underline should be coherent with the model presented in Section 2---all classes, attributes, and associations from the model should appear in the text and their role in the system, as described in the text, should be consistent with the model.  

Model
Provide the conceptual model of your system as a UML class diagram. Represent proper cardinalities (multiplicities) for all associations. Also include the association names. 
 
Some points to consider:

Use UML adequately. Do not use graphical elements that are not part of the language. Represent compositions and aggregations when relevant.
This model is not an ER diagram (entity-relationship model), which is focused on relational database systems. However, both diagrams have similarities.
Do not overcomplicate how you represent the elements of your model (e.g., using inheritance or an association when they are not necessary). Pay attention to simplicity, maintainability, unnecessary repetition, cohesion, and coupling.
Do not represent actions that don’t need to be registered in the system.
Do not represent technical elements, such as user interface or programming language libraries in the model. At this point, we are modeling the business logic/domain of your system. During the design phase, the model will be refined to include technology-specific elements and decisions.
Do not represent "System" as a class in your model. Everything that you are modeling is part of the system.
If you feel the need to justify your decisions, you can write your rationale in this section or as UML comments in the diagram.
The model must have at least 8 classes. You can add requirements in the system description if you need more classes. 
Grading criteria (25 points): You should correctly use the UML specification. Your model should have the minimum number of classes. Your domain should be adequately modeled. The model should avoid unnecessary complexity, repetition, lack of cohesion, and coupling. The classes should be at an adequate abstraction level.