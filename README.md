# ArcheryBowSimulation
Simulation of the brace, draw, and dynamic release phases of the traditional bow.

To run the simulation, simply execute brace_draw.py.

# Introduction
Archery is ancient and the bow and arrow may humanity’s oldest elastic stored-energy tool. Traditional bows have been designed through trial and error, adaptations of traditions, and the needs of food and conflict.  The many traditional designs over the world reflect this.  There are reasons archers may be interested in efficient and powerful bows.  These may be curiosity, hunting, competition, and aesthetics.
The main kinds of bow design are primitive, historical, traditional, and modern.  Primitive bows were those made by pre-agricultural man.  In modern times, making primitive bows can be a survival skill; sometimes bowyers restrict themselves to primitive tools.  Historical bows are strictly historical finds or attempts to recreate them.  Modern bows are designed for modern application, be that sport or hunting.  
Traditional bows are the largest category.  The term covers primitive bows to laminated recurve bows, and typically means anything before the invention of the compound bow.  The materials used for some laminated bows may require a post-industrial society, but the designs are typically thought to be doable with more primitive and natural materials.  Perhaps the most notable feature of traditional archery, is that the archer is forgoing tools that are objectively superior for their task.  The reasons for this may be aesthetic or a desire to connect to a more primitive human experience.     

![image](https://user-images.githubusercontent.com/56926839/161319974-29b8eff3-46a7-4acf-8bd8-ac29356b653a.png)
Figure 1: Left to right, top to bottom:  Nubian Wooden Models.  Asuit, circa 2000 BC [David Tukura, 1994 and Egyptian Museum, Cairo].  “Man on Cloud”, Comanche, circa 1875 [Jim Hamm, 1994 and Panhandle Plains Historical Museum].  Yew Longbow John Strunk, 1992].  Korean Bow [Jeff Schmidt 1992].

This paper will attempt an analysis on traditional bow mechanics and design.  The sections of this paper include a motivation on bow design, a mathematical analysis using techniques from the course book [J. David Logan, 2013], a computational mathematical analysis suitable for simulation, an analysis of bow behavior and mechanics, a review of the history and the state-of-the-art in bow analysis and simulation, and a description of novel bow design.  Unfortunately the analysis section using techniques from this course is underwhelming.  I spent the majority of my mental effort on the analysis for the simulation and a majority of my time programming a simulation based on that analysis.  I will attempt to derive the novel bow design from my analysis of bow behavior but I am sure it is based on intuition not rigorous analysis. The code to go with this can be found here: https://github.com/feildawproton/ArcheryBowSimulation 

# Motivation
Some preliminary work on modeling the traditional bow and arrow before reviewing the history and state-of-the-art of archery modeling and simulation.  This will rely on some traditional archery text.  The first question to ask is: what is the design being optimized for?  A key characteristic of the bow is that it is powered by human muscle.  Below are some force draw-curves that visualize the work that a human being needs to put into a bow.

![image](https://user-images.githubusercontent.com/56926839/161320125-6721cd41-ade9-4629-a715-83af40536370.png)

The actual draw length is on the horizontal axis and force on the vertical axis.  This work will try to analyze what design features lead to the various f-d curves above.  Typically, static tipped recurves achieve high storage, short bows display stack (positive second derivative of force with respect to draw length), and a longbows tend to have a linear f-d curve.  This raises some questions:
Q1.1: Why do some static-recurve bows store more energy?  How can this be quantified so that the effect can be designed on demand?
Q1.2: Why do short bows exhibit stacking?  What design features or properties should be avoided?
One view of bow efficiency is the ratio between the work put into the system and the energy in the arrow after loose.  Upon release of the string, the energy put into the bow will be divided among the arrow, kinetic energy of the bow (moving the limbs), hysteresis or internal heating of the bow, hysteresis of the string (stretching), and other effects such sound and the archers body.

E_draw=E_arrow+E_bowKinetic+E_stringKinetic+E_bowHysteresis+E_stringHysteresis+E_other
E_bowHysteresis,E_other≪E_arrow,E_bowKinetic,E_stringHysteresis,E_stringKinetic

Because the effects of bow hysteresis and other losses (such as sound) are typically so low they are typically not considered in the analysis.  For the traditional bow, an archery will not notice much of an efficiency difference between a horn belly, wood belly, fiberglass, or carbon fiber.  Olympic archers use synthetic materials for the climate stability.  
What engineers might typically care about is the proportion of the energy put into the bow that goes into the arrow, efficiency=E_arrow/Edraw.  

![image](https://user-images.githubusercontent.com/56926839/161320215-1310156e-4e4e-49db-8f72-3f1569603551.png)
However, human beings do not have any locking mechanism to hold the bow back without effort during aiming.  The final weight of the bow must be held by human musculature.  This means continuous use of chemical energy in the human body.

![image](https://user-images.githubusercontent.com/56926839/161320266-b613d92e-eef8-4450-b723-0e7db215429c.png) ![image](https://user-images.githubusercontent.com/56926839/161320277-d035f0c0-d320-4e7b-b3c3-34c0d8a42bd6.png)
From the human point of view, the difference between the effort of the high storage bow and the linear (or even stacking bow) are less noticeable the longer the bow is held at final draw weight.  So E_arrow/(F(StrokeLength))   is a good candidate for maximization.  This is the reason compound bows and crossbows have higher draw weights but are perceived as requiring less effort than traditional bows.

![image](https://user-images.githubusercontent.com/56926839/161320333-7278a80a-7f39-4118-876b-a1947b608d7f.png)

A trigger mechanism takes the draw weight of the crossbow.  This may be why crossbows were more popular among the less archery oriented cultures of Medieval Europe.  Welsh and English archers were said to have trained continually during the time of the longbow in order to pull 90-180 pounds bows.  While crossbows from the same time were much heavier (400 – 1200 pounds) they were drawn with some mechanism and the final draw weight held with a trigger.  
Modern compound bows have a hold weight a fraction of their peak draw weight.  As long as the archer can get past the peak weight, they can then hold and aim the bow in relative leisure.  Compound bows also store more energy that traditional bows.  They do this by manipulating the leverages with cams and cables.  The design disadvantages the string and advantages the limbs during early draw, in order to increase early dray weight.  As the string is pulled, during mid draw, the cams advantage the string and disadvantage the limbs in proportion to the draw length so that peak weight stays nearly constant.  Finally, near the end of the draw the design severely disadvantages the limbs and advantages the string (this is the so call let-off).  A question arises:
Q1.3: Can knowledge of function of compound bows be applied to traditional-style bows?
Optimization Objective: With all that said, the desired optimization function is likely a weighted sum:

max⁡(w_1  E_arrow/E_draw +w_2  E_arrow/F(L_stroke ) )

Since the weights w_1 and w_2 are not known, no single design is likely to be optimal.  However, a Pareto front could be constructed in order to reduce the decision space to a simple tradeoff.  
Traditional bowyer Tim Baker stated in [Baker 1992] that the best bow will contain the follow quantities: (1) Arrow speed, (2) accuracy, (3) comfort of draw and release, (4) durability, (5) suitability for its use environment, (6) beauty, (7) ease of construction, (8) ease of maintenance, (9) cost, or availability of materials, and (10) unobtrusiveness.  
	Arrow speed is handled by the goal [1], since KE_arrow=1/2 M_arrow V_arrow^2 and most of the energy going into our arrow will be in the form of its forward kinetic energy.  Not all of it will be though.  A good chunk of energy may go into vibration and hysteresis caused by the arrow compressing under acceleration and bending around the bow (the archer’s paradox).  However this analysis is limited to the bow and assumes the energy that goes into the arrow is not severely wasted. 
	Accuracy is a function of the archery tackle and the archer.  The bowyer is after precision.  Precision requires consistent behavior of the bow and the arrows and for the bow and arrows to be well matched.  Arrow design and construction are not covered in this report.  Matching the right arrow to the bow requires choosing the right spine.  This analysis cannot account for the consistency of the bow, unless chaotic behavior is noticed during simulation and it is believed that this behavior is caused by the design and not the solver.
	Comfort of the draw usually means two things: the force-draw curve is smooth (to human perception not mathematically) and the final draw weight be as low as possible.  The perception of the f-d curve requires human testing, though if an f-d curve appears erratic it is probably comfortable.  Lowering draw weight is handle by the goal [1], since its inverse is maximized.
	Durability may primarily come from materials, but the optimization can ensure stress and strain are considered with the material indexed constraints:

σ<σ_yield/(SafteryFactor )

(5)	Suitability for its use environment is a kind of durability that this analysis will not capture.  This analysis also skips (6) beauty, (7) ease of construction, (8) ease of maintenance, and (9) cost, or availability of materials.
(10) Unobtrusiveness can be enforced most easily by restricting string length:

L_String=L_(String,max)

Design Goal 1:  Since energy delivered to the arrow is proportional to the work put into the bow and apparent (human) efficiency is inversely proportional to final draw weight, good bows will exhibit high rate of force increase near brace and low (possibly negative force increase) near full draw.  Most smooth, not stacking, bows have a negative second derivative of force with respect to draw.  The force being referred to is the force at the nock in the x direction.

dF/dx  ↑,x→ L_brace=  0
dF/dx  ↓,x→ L_stroke= 1
(d^2 F)/(dx^2 )<0,L_brace<x≤ L_stroke

Design Goal 2:  The portion of energy that goes into the arrow should be much larger that which goes in the bow up release.

E_arrow  ≫ E_Kinetic

# Applied Mathematical Analysis
## Dimensional Analysis
This wasn't particularly successful so I'm not going to include it here.

## Scaling
Archery happens at a familiar, human scale.  First, lengths will be considered.  There are two primary lengths that define the behavior of the bow, the brace height and the draw length.  The Archery Manufactures and Merchants Organization Standard [AMO 2000] defines brace height (L_brace) as the distance from the nocking point the pivot point (the lowest deepest point of the handle).    

![image](https://user-images.githubusercontent.com/56926839/161320702-c10bb906-1e9c-4816-a687-bb934adbd97b.png)
Figure 2:  From AMO Standard [AMO 2000]

The AMO defines the true draw length (L_draw_true) as the distance from the pivot point to the nocking point at full draw, just before release.  The official draw length (L_draw_arrow) accounts for the length of the arrow and is the true draw length plus 1.75 inches.  

![image](https://user-images.githubusercontent.com/56926839/161320771-0d4396b3-e903-4ce6-9a1f-c19209ab9fd0.png)
Figure 3:  Visualization of brace height and draw length with unbraced, braced, and full-drawn profiles.  Underlying images from [Baker 1992].

Values for draw length typically range from 26 to 32 inches (24.25 – 30.25 actually) and brace height from 5.5 to 9 inches.  A typical bow may have a brace height of 7 inches and true draw length of 28 inches.  In this case the power stroke would be 21 inches.  Lengths are scaled by the power stroke, the distance from brace to full draw, in order to graph on a [0,1] scale.
L_stroke=l_stroke/l_stroke =L_draw-L_brace=1
L_brace=l_brace/l_stroke =1/3,L_draw=l_draw/l_stroke =4/3
x ̅=x/l_stroke ,y ̅=y/l_stroke 


The origin of the analysis on the nock (where the arrow meets the string) at the brace position.  So, the center of the rise, at brace, will be (-1/3, 0).  All lengths will be scaled by the stroke length.  

Because actual draw weight is determined by the material, thickness, width, and cross section of the limbs, forces during analysis of profile will be normalized.  The analysis includes varying stiffness, but this is meant to be relative not actual.   

F ̅(x)=F(x)/Fmax

In order to compare the energy store of design with different draw weight, a storage ratio is used.  The storage ratio compares the energy stored in the bow to the energy that would be stored in a perfectly linear bow of the dame draw force. 

R_storage=  E_bow/(1/2 〖*l〗_stroke 〖*f〗_draw )
〖 R〗_storage=   (E_bow ) ̅/(1/2*(f_draw ) ̅ ), 
where   (f_draw ) ̅=f_draw/(f_max )    and    (E_bow ) ̅=  ∫_0^1▒force

## TO DO: Mass Scaling

## Boundary Layer Analysis, Uniform Approximation
Again this isn't particularly helpful, so I am leaving it out of here.

#Computational Analysis and Algorithms
In this section the bow will be analyzed in such a manner that the results can be used for a complex simulation of the bow.  The key features of this analysis is that it is (1) relatively simple and intuitive (2) on relatively small components of the bow (3) components are understood to belong to a complex hierarchy of forces and transformations.  The word complex does not mean complicated, it simply means consisting of many (potentially different) connected parts.  The bow and arrow can be though of as an emergent property of chunks of material that make the limbs (ex: wood and wood fibers), the fibers of the string, the structure of the arrow, and the human whose ingenuity constructs it and whose muscles power it.  

I prefer to avoid trigonometric functions in simulations.  While the overhead of the language I implement these computations in may be considerably higher that the overhead of approximating transcendental trigonometric functions, it is useful practice for moving closer to the metal and typical practice.  With vectors:

cosθ_(A,B)=(A∙B)/|(|A|)||(|B|)| ,〖   sin〗⁡〖θ_(A,B) 〗=  (||A ×B ||)/|(|A|)||(|B|)| , 
recall {█(i×j=k,j×i= -k@j ×k=i,k×j= -i@k ×i=j,i×k=-j)┤
for positive θ only:〖sin⁡θ〗_(A,B)= √(1-cos^2⁡θ )

But it is rarely the case that a simulation needs calculate cosTheta or sinTheta.  For the same reasons I prefer to perform rotations with complex numbers or quaternions.  Since this simulation occurs on the xy-plane, complex numbers can be used for rotations.

(a+bi)(c+di)=(ac-bd+adi+bci)

Complex numbers can rotate each other and rotate vectors.  Treat the vector (x, y) as (x + yi).  Rotations have to be applied to local vectors, not points.  If the points are defined in global space, local vectors can be found with T_(n,i=0)=P_(n+1,i=0)-P_(n,i=0).  Local vectors should only be recalculated if the local profile changes (perhaps due to compression).

Compression and shear forces in the limb are recorded for post hoc analysis (for ex: compression forces to high).  They are not used to deform the limb.

Comp_n= {█(f_i,                                    n≥contactIndx  @F_i∙(P_n-P_(n+1 ))/|(|P_n-P_(n+1 ) |)| ,     n<contactIndx)┤
Shear_n=f_i-(Comp_n)/(||Comp_n ||)

The check for the contact index is for recurves where the string contacts the limb bellow the tip (where it is strung).  There would be some shear and some rotational momentum proportional to the thickness of the limb, but I am just ignoring it for now.

Rotational moments are calculated from the stringing force during brace and draw.

μ_n= {█(0,                                          n≥contactIndx (I_c)  @F_n×(P_n- P_c ),                     n<contactIndx(I_c ) )┤

Where P_C is the contact point where the string meets the limb.  Local rotations are calculated from the rotational moments.  The rotation will be proportional to the stiffness of the limb at that point.  I make a simplification and apply Hooke’s law as such:

b_n=  μ_n/k_n 

Where k_n is the stiffness of the limb at that point.  I make the assumption that all rotations are small.  With this assumption b_n can be treated as the imaginary component of a complex rotation.  Therefore: a_n= √(1-b_n b_n ) and R_(local,n)=(a_n,b_n ).

Rotations are hierarchical.  Rotations occur in the basis of the rotations that precede them in a kinematic chain.  Therefore to calculation global rotations in the limb:

R_(global,n )= ∏_(m=0)^(m=n)▒R_(local,m)   

If global rotations are calculated in order (not parallel), reduce the number of computations with can be reduced with:

R_(global,n ) {█(f_1^N (n),n>0@R_(global,n),n=0),┤ 〖    where f(n)= R〗_(local,n) R_(global,n-1)

With the above information the limb profile can be updated following:

P_(global,n+1)=〖f_0^(N-1) (n+1),where f(n+1)=R〗_(global,n) T_(local,n)+ P_(global,n)

Recall that local translations (T_local_n) are assumed to be static.  They would only change if forces other than rotation were affecting the limb segments, such as more accurate model (bending) and compression or shear effects.   

The force the limb produces on the string needs to be recalculated after every optimization iteration and before the force is incremented.  This is because the change in the string contact or just the contact itself can change the leverage of the limb segments.  It is possible for draw force to go down as the tip geometry gives the string more advantage over the limb.  I tried several attempts at solving systems of linear equations; but in the end, a simple solution built from intuition worked quite well. 

















