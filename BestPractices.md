# LLD Interivew tips
Structure should look like:
1. Identify *entites* (nouns).  
Example: **User**, **Order**, **Product**
2. Model a stable core as an *entity*: Create classes for core-nouns that are relatively stable. 
3. Identify *behaviours* (Axes for different actions).  
 Pinpoint those that change independently (PaymentMethod, NotificationType)
3. *Plug-in behaviours* like policy, strategy. (Composition)
4. *Interfaces/ ABCs(Protocol)* for contracts.
5. Avoid huge constructors. Use *Factory* for object creation.

This setup helps us have *high cohesion* and *low coupling* 

### Coupling and Cohesion
**Coupling** refers how close two different parts of the system are interdependent.  
Loose coupling means more isolation.   
**Cohesion** refers to how well the code within a part sits together with it. It means there is more meaningful connections between different sections of a part of our system.   

Usecases:
1. Easier to maintain. 
2. Flexible, we can also swap parts.   

There are tradeoffs based on our problem statement, most times we dont need to over engineer.  
![alt text](/Python-LLD/docs/image.png)