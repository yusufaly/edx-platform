.. _Peer Assessment Problems:

Peer Assessment Problems
---------------------------------

Introduction to Peer Assessments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning:: **Peer assessment technology is still in beta.** We recommend that
          you test peer assessments thoroughly in a practice course and only add them to
          courses that are **not** already running.

Peer assessments allow instructors to assign questions that may not have definite answers, with students grading each others' responses.  Peer assessment problems can also include self assessments. With peer assessments, students learn by comparing their peers' answers to a rubric that you create. With self assessments, students compare their own responses to the rubric.

For a good experience with peer assessments, you'll need to follow a few guidelines.

-  Do not create a new peer assessment in a running course.
   Only create peer assessments in a test course.
-  If your course will include peer assessments, add and
   thoroughly test all the peer assessments *before* the course
   is live.
-  Set peer assessments to be optional, ungraded, or droppable
   exercises until you've used the technology a few times and have
   become familiar with it.
-  Use peer assessments sparingly at first. Only include a few
   in your course, and make sure that you have contingency plans in case
   you run into problems.

Finally, if you're at an edX consortium university and you plan to
include peer assessments in a MOOC, make sure to notify your
edX project manager (PM).

.. _PA Elements:

Elements of a Peer Assessment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you create a peer assessment problem, you'll specify several elements. For step-by-step instructions, see :ref:`Create a PA Problem`.

- The **number of responses** each student has to grade.

- The **number of grades** each response has to receive.

- The **assessment type or types**. The type of assessment and the order in which the assessments run appears at the top of the problem. In the following example, peers perform peer assessments, and then the student performs a self assessment.

  .. image:: /Images/PA_AssmtTypes-LMS.png
     :alt: Image of peer assessment with assessment types circled

- (optional) The **due dates** for students to submit responses, perform peer assessments, and perform self assessments. You can set different dates for each action, and these dates can overlap. If you don't specify dates, the deadline for all responses, peer assessments, and self assessments is the due date that you set in the subsection that contains the peer assessment. (**SP: We tell people that this is optional, but then include a warning about setting close due dates for response submissions and assessments. Does that mean this _shouldn't_ be optional?**)

  .. note:: We don't recommend that you use the same due date and time for response submissions and assessments. If a student submits a response immediately before the due date, other students will have very little time to assess the response before peer assessment closes. In this case, a student's response may not receive a score.

- The **question** that you want your students to answer. This appears near the top of the component, followed by a field where the student enters a response.

  When you write your question, you can include helpful information for your students, such as:

	* The approximate number of words or sentences that a student's response should have. 
	* What students can expect after they submit responses. 
	* The number of times that a student can submit a response.

	**[Jane: Would you like to add information about wording?]**

- A rubric that you design. The same rubric is used for peer and self assessments, and the rubric appears when students begin grading. Students compare their peers' responses to the rubric. 

  Rubrics are made of *criteria* and *options*. 

  * Each criterion has a *name*, a *prompt*, and two or more *options*. The prompt contains a description of the criterion. The name of the criterion doesn't appear in the student view, but the prompt text does.
  * Each option has a *point value*, a *name*, and an *explanation*. 

	.. image:: /Images/PA_Rubric_LMS.png
	   :alt: Image of rubric in the LMS

  When you create your rubric, decide how many points each option will receive, and make sure that the explanation for each option is as specific as possible. 

  Note that different criteria in the same problem can have different numbers of options. For example, the "Ideas" criterion in the sample problem has three options, while the "Content" criterion has four options.

.. _Create a PA Problem:

Create a Peer Assessment Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning:: Peer assessments are still in beta. To add peer assessments in your course, you'll need to work with your edX program manager.

To create a peer assessment problem, you'll edit the XML code in a Problem component, similar to creating other problems. The following image shows what a peer assessment component looks like when you edit it in Studio, as well as the way that students see that peer assessment in the LMS.

.. image:: /Images/PA_All_XML-LMS_small.png
   :alt: Image of a peer assessment in Studio and LMS views

(**SP: Possibly add prompt, rubric, etc. call-outs to screen shot**)

Creating an open response assessment is a multi-step process.

* :ref:`PA Advanced Settings`
* :ref:`PA Create Component`
* :ref:`PA Specify Name and Assessment Types`
* :ref:`PA Add Due Dates`
* :ref:`PA Add Question`
* :ref:`PA Add Rubric`


Each of these steps is described in detail below.

.. _PA Advanced Settings:

Step 1. Modify the Course Advanced Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before you can create a peer assessment problem, you have to add the Peer Assessment problem component to your course. You do this in the advanced settings in Studio.

#. In Studio, on the **Settings** menu, click **Advanced Settings**.
#. Under **Manual Policy Definition**, locate the **advanced_modules** policy key.
#. In the **Policy Value** field for the **advanced_modules** policy key, type ``"openassessment"``. Make sure to include the quotation marks.

   .. image:: /Images/PA_ModifyAdvancedSettings.png
     :alt: Image of the advanced_modules policy key

#. In the "You've made some changes" message that appears at the bottom of your screen, click **Save Changes**. 

.. _PA Create Component:

Step 2. Create the Component
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. In Studio, open the unit where you want to create the assessment.
#. Under **Add New Component**, click **Advanced**, and then click **openassessment**. [SP: Will this change to "Open Assessment" or "Peer Assessment" or similar?]
#. In the problem component that appears, click **Edit**.
#. The component editor opens. 

   The component editor contains sample code, which includes the assessment type or types as well as a sample question ("prompt") and rubric. You'll replace this sample content with the content for your problem in the next steps. 

.. _PA Specify Name and Assessment Types:

Step 3. Specify the Problem Name and Assessment Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To specify problem data such as the name and assessment types, you'll work with the XML at the top of the problem.

In the example code, locate the following XML near the top of the component editor:

.. code-block:: xml

  <openassessment>
  <title></title>
  <assessments>
    <assessment name="peer-assessment" must_grade="5" must_be_graded_by="3"/>
    <assessment name="self-assessment"/>
  </assessments>

This code specifies four elements:

* The name of the problem.
* The types of assessments that run. 
* The order that the assessments run in. (Assessments run in the order in which they're listed.) 
* For peer assessments, the number of responses that each student must grade.
* For peer assessments, the number of peer assessments each response must receive. 

In this example:

* The problem does not have a specified name.
* The peer assessment runs, and then the student can perform a self assessment.
* Each student must grade five peer responses before he receives the scores that his peers have given him.
* Each response must receive assessments from three students before it can return to the student who submitted it.

To specify your problem data, follow these steps.

#. Between the ``<title>`` tags, add a name for the problem.

#. Make sure that the assessments are listed in the order that you want students to complete them in. 

#. In the ``<assessment>`` tag that contains "**peer-assessment**", replace the values for **must_grade** and **must_be_graded_by** with the numbers that you want.

.. _PA Add Due Dates:

Step 4. Add Due Dates (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To specify due dates and times, you'll add code that includes the date and time inside the XML tags for the problem and for each specific assessment. The date and time must be formatted as ``YYYY-MM-DDTHH:MM:SS``.

.. note:: You must include the "T" between the date and the time, with no spaces. All times are in universal coordinated time (UTC).

* To specify a due date for response submissions, add the ``submissions_due`` attribute with the date and time to the opening ``<assessments>`` tag.

  ``<assessments submissions_due="YYYY-MM-DDTHH:MM:SS">``
  
* To specify start and end times for an assessment, add ``start`` and ``end`` attributes with the date and time to the ``<assessment>`` tag for the assessment.

For example, the code for your problem may resemble the following. 

.. code-block:: xml

  <assessments submissions_due="2014-03-01T00:00:00">
    <assessment name="peer-assessment" must_grade="5" must_be_graded_by="3" start="2014-02-24T00:00:00" end="2014-03-08T00:00:00"/>
    <assessment name="self-assessment" start="2014-02-24T00:00:00" end="2014-03-08T00:00:00"/>
  </assessments>

In this example:

* The problem is set at the subsection level to open on February 24, 2014. (This information does not appear in the code.)
* Students must submit all responses before March 1, 2014 at midnight UTC. 
* Students can begin peer assessments on February 24, 2014 at midnight UTC.
* All peer assessments must be complete by March 8, 2014 at midnight UTC.
* Students can begin self assessments on February 24, 2014 at midnight UTC.
* All self assessments must be complete by March 8, 2014 at midnight UTC.

.. note:: We don't recommend that you use the same due date and time for response submissions and peer assessments. If a student submits a response immediately before the due date, other students will have very little time to assess the response before peer assessment closes. In this case, a student's response may not receive a score.

.. _PA Add Question:

Step 5. Add the Question
^^^^^^^^^^^^^^^^^^^^^^^^
The following image shows a question in the component editor, followed by the way the question appears to students.

#. In the component editor, locate the ``<prompt>`` tags.

#. Replace the sample text between the ``<prompt>`` tags with the text of your question. Note that the component editor respects paragraph breaks inside the ``<prompt>`` tags. You don't have to add ``<p>`` tags to create individual paragraphs.

.. image:: /Images/PA_Question_XML-LMS.png
      :alt: Image of question in XML and the LMS

(**SP: Remove screen shot? Seems unnecessary...**)

.. _PA Add Rubric:

Step 6. Add the Rubric
^^^^^^^^^^^^^^^^^^^^^^^^

To add the rubric, you'll create your criteria and options in XML. The following image shows a highlighted criterion and its options in the component editor, followed by the way the criterion and options appear to students.

.. image:: /Images/PA_RubricSample_XML-LMS.png
      :alt: Image of rubric in XML and the LMS, with call-outs for criteria and options

#. In the component editor, locate the following XML. This XML contains a single criterion and its options. You'll replace the placeholder text with your own content. 

   .. note:: For criteria, the name of each criterion doesn't appear in the student view, but the prompt text does. For options, both the name and the explanation appear in the student view.

   (**SP: Is it possible to have an option that includes a name but not an explanation?**)

	.. code-block:: xml

	      <criterion>
	      <name>Ideas</name>
	      <prompt>Determine if there is a unifying theme or main idea.</prompt>
	      <option points="0">
	        <name>Poor</name>
	        <explanation>Difficult for the reader to discern the main idea.
	                Too brief or too repetitive to establish or maintain a focus.</explanation>
	      </option>
	      <option points="3">
	        <name>Fair</name>
	        <explanation>Presents a unifying theme or main idea, but may
	                include minor tangents.  Stays somewhat focused on topic and
	                task.</explanation>
	      </option>
	      <option points="5">
	        <name>Good</name>
	        <explanation>Presents a unifying theme or main idea without going
	                off on tangents.  Stays completely focused on topic and task.</explanation>
	      </option>
	    </criterion>

#. Under the opening ``<criterion>`` tag, replace the text between the ``<name>`` tags with the name of your criterion. Then, replace the text between the ``<prompt>`` tags with the description of that criterion.

#. Inside the first ``<option>`` tag, replace the value for ``points`` with the number of points that you want this option to receive.

#. Under the ``<option>`` tag, replace the text between the ``<name>`` tags with the name of the first option. Then, replace the text between the ``<explanation>`` tags with the description of that option.

#. Use this format to add as many options as you want. 

You can use the following code as a template:

.. code-block:: xml

	 <criterion>
	   <name>NAME</name>
	   <prompt>PROMPT TEXT</prompt>
	   <option points="NUMBER">
	     <name>NAME</name>
	     <explanation>EXPLANATION</explanation>
	   </option>
	   <option points="NUMBER">
	     <name>NAME</name>
	     <explanation>EXPLANATION</explanation>
	   </option>
	   <option points="NUMBER">
	     <name>NAME</name>
	     <explanation>EXPLANATION</explanation>
	   </option>
	 </criterion>


.. _PA Test Problem:

Step 7. Test the Problem
^^^^^^^^^^^^^^^^^^^^^^^^

Test your problem by adding and grading a response.



