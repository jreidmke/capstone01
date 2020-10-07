## About IEP+

IEP+ is a small lightweight Flask Application to help special education teachers connect to the parents and guardians of the students they serve. 

## Usage

There are two sides to IEP+, the teacher facing side and the guardian facing side. Although they continually interact, they are securely separated through frontend and backend protection. 

## Teacher Facing  

If you are a first time user, register as a teacher by entering the correct school code. You will arrive at the your student list, containing a list of student objects as well as the teacher navbar.

### Teacher Navbar

The teacher navbar features routing to the **Add Student**, **Add Family**, **Messages**, and **Logout**. 

##### Add Student:
To add a student, simply fill out the form and submit the student to the database by hitting the **Add Student** button.

##### Add Family:
To add a family, fill out the form using the data displayed in the Guardian Information/Student Information dropdowns. Make sure you are committing the correct information before submitting.

##### Messages:
Click here to see your most recent messages.

##

###Student List

##### Send a Message:
To send a message to a student's guardian, select the **Contact Guardian** under the student's name. This will direct you to a message input screen. If your message is about a goal from this student's most recent IEP, select the goal from the top dropdown menu. Select the recipients from the student guardian list and finally, select the urgency level. 

##### Inspect Student Details:
To see more about a student and their IEPs, select the **Student Details** button under neath the student's name. 
##
###Student Details
On the student detail page, you will see information about the student, including their family relations, IEPs and current goals. 

##### Current Goals:
The current goals also include the student's *baseline*, *current*, and *level of attainment*. To edit the students current level, select the **Edit Current Data** button and update the students current level of achievement. 

##### IEPs:
To view a student's previous IEP's click on the link of the IEP Date. To create a new IEP, click **Create New IEP+**.

##
###Creating a New IEP

First, enter the student's goal text. Then select the subject the goal falls under. Complete the baseline data and select **Add Goal**. Next you will be prompted to select the standard set from which you will pulling you standard. And finally, you will select the aligned standard.

When you have completed your goal, you will be redirected to the page you originally started your goal writing on. To edit the goal you just wrote, select it from the IEP display on the right.

If you have more goals to add, simply redo the above listed process. When you have entered all goals, select **Commit Goals and Data**. This will **lock** the IEP and prevent further edits.

## Guardian Facing

If you are a first time user, register as a guardian. You will probably not have any students at this time as a **Family Object** has not been created yet. The teacher will do this soon and your student will show up in your student list. Besides this, you can see your Guardian Navbar. 

### Guardian Navbar

##### Messages:
Click here to see your most recent messages.

##### Student IEPs:
Click on your student's IEPs to view their IEP details. To contact their teacher, select the **Contact this Student's Teacher** and complete the message form. 

