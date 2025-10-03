# Generative AI for Forward and Inverse Design in Architecture and Engineering
Workshop on generative AI during the excursion to Chile: 02-03 of october 2025

*   [Description](#description)
*   [Schedule](#schedule)
*   [Task](#task)
*   [Files](#files)
*   [Instructors](#instructors)

## <a name="description"></a>Description
Machine learning and generative AI are expected to become game-changer for solving design problems. These methods greatly enhance AI-assisted design in architecture, civil and mechanical engineering by providing new ways of exploring and interacting designs.

In this workshop we  equip students with the foundational knowledge on Machine and Deep Learning to formulate learning problems from given design tasks.
During the course, we present how to create and deploy custom Conditional Variational Autoencoder (CVAE) models for design in architecture and engineering. We leverage capabilities of CVAE to perform forward and inverse design, and of the parametric modelling conventionally employed to design an example pedestrian bridge. For forward design, the CVAE serves as a computationally efficient surrogate, streamlining the computational process through sensitivity analysis and uncertainty quantification. In inverse design, the user can specify the desired attributes of a parametric problem, and the CVAE proposes possible design solutions, supporting the designer in exploration of the design space.

Students learn how to formulate a proper parametric design problem, to generate data with that pipeline and then how to set-up, train and evaluate project-specific CVAE models, and deploy them to generate designs with the properties you request! For this, we use our open-source toolkit for AI-eXtended Design (AIXD).

By the end of the course students will develop computational thinking related to the combination of domain knowledge and latest computer science AI technology for scientific machine learning applications within the AEC domain. Specifically, the students will:

*   Gain fundamental understanding on how **AI / ML / DL technology** works and the impact it may have in the AEC industry.
*   Gain understanding on how to **combine specific knowledge from AEC domain with state-of-the-art ML/DL** to deploy CVAE models.
*   **Identify limitations, pitfalls, and bottlenecks** in these applications.
*   Develop **critical thinking** on solutions for the above issues.
*   Acquire **hands-on experience** in creatively thinking and designing an application together with the CVAE approach.
*   Use this course as a **"stepping-stone" to Machine Learning**.


## <a name="schedule"></a>Schedule
The course will be delivered as a two day seminar with several blocks:

<html lang="de">
<head>
  <meta charset="UTF-8">
  <style>
    table {
      border-collapse: collapse;
      width: 100%;
    }
    th, td {
      border: 1px solid #333;
      padding: 8px;
      text-align: left;
      vertical-align: top;
    }
    th {
      background-color: #eee;
    }
  </style>
</head>
<body>
  <h2>Schedule</h2>
  <table>
    <thead>
      <tr>
        <th>Day</th>
        <th>Timeslot</th>
        <th>Activity</th>
      </tr>
    </thead>
    <tbody>
      <!-- Donnerstag -->
      <tr>
        <td rowspan="5">Thursday, 02.10.2025</td>
        <td>9:00 - 10:30</td>
        <td>General Intro AI and AI in AEC</td>
      </tr>
      <tr>
        <td>10:45 - 12:15</td>
        <td>Regression, Classification, Images and Text</td>
      </tr>
      <tr>
        <td>12:15 - 13:15</td>
        <td>Lunch</td>
      </tr>
      <tr>
        <td>13:15 - 14:45</td>
        <td>Introduction to the AIXD toolbox</td>
      </tr>
      <tr>
        <td>15:00 - 16:30</td>
        <td>Introduction to the parametric problem and hands-on</td>
      </tr>
      <!-- Freitag -->
      <tr>
        <td rowspan="5">Friday, 03.10.2025</td>
        <td>9:00 - 10:30</td>
        <td>Data Generation & discussion</td>
      </tr>
      <tr>
        <td>10:45 - 12:15</td>
        <td>Model fitting and evaluation & discussion</td>
      </tr>
      <tr>
        <td>12:15 - 13:15</td>
        <td>Lunch</td>
      </tr>
      <tr>
        <td>13:15 - 14:45</td>
        <td>Design Space Exploration with AIXD toolbox</td>
      </tr>
      <tr>
        <td>15:00 - 16:30</td>
        <td>Final Discussion and Wrap-up</td>
      </tr>
    </tbody>
  </table>
</body>
</html>


## <a name="task"></a>Task

<p>
  First, create a **parametric bridge model** in Rhino/Grasshopper. Provide a full list of your design parameters along with each parameter’s domain and data type.
</p>
<p>
  Then, apply a sampling strategy (for example, **Latin Hypercube Sampling**) to generate an initial ensemble of design candidates. For each sampled design, evaluate performance metrics such as natural frequencies, maximum displacements, mass, and utilization.
</p>
<p>
  Perform an exploratory data analysis on the resulting dataset to assess whether it is suitable for training a conditional variational autoencoder (CVAE). Train the CVAE and evaluate its performance. If the CVAE is accurate and stable enough, use it to perform **inverse design**—i.e. generate new parameter sets from desired performance targets.
</p>
<p>
  Feed those generated parameter sets back into your Rhino/Grasshopper model and inspect multiple design alternatives. Refine the most promising designs, discussing their structural trade-offs and implications.
</p>
<p>
  Finally, prepare a **brief presentation** summarizing your methodology, insights, and results, and engage in the group discussion to compare strategies and findings across teams.
</p>



## <a name="files"></a>Files
Students can use the following files if they do not achieve a subgoal:

[GHFile](https://mkrausai.github.io/lectures/2025_GenDesignInAEC/251002 b parametric setup.gh)

[GHFile3dm](https://mkrausai.github.io/lectures/2025_GenDesignInAEC/251002 parametric setup.3dm)

[LHSNotebook](https://mkrausai.github.io/lectures/2025_GenDesignInAEC/LHS.ipynb)

[CVAENotebook](https://mkrausai.github.io/lectures/2025_GenDesignInAEC/bridge_design.ipynb)

[LHSParameters](https://mkrausai.github.io/lectures/2025_GenDesignInAEC/lhs_samples.csv)

[LHSResults](https://mkrausai.github.io/lectures/2025_GenDesignInAEC/lhs_samples_results.csv)

[AIXDPaper](https://mkrausai.github.io/lectures/2025_GenDesignInAEC/1-s2.0-S001044852500106X-main.pdf)


## <a name="instructors"></a>Instructors
<img src="https://mkrausai.github.io/img/persons/Michael6_3.jpg" width="20%" alt="Michael Kraus" /><br />
**Univ.-Prof. Dr. Michael A. Kraus, M.Sc.(hons)**<br />
Institute für Statik und Konstruktion (ISM+D)<br />
TU Darmstadt<br />
_Co-{Instrucor ; Lecturer}_<br />

<img src="https://mkrausai.github.io/img/persons/LukasVasquez.jpg" width="20%" alt="Lukas Vasquez" /><br />
**Architect Prof. Dr. Lucas Vasquez**<br />
Arquitecto_ Pontificia Universidad Católica, Chile<br />
_Co-{Instrucor ; Lecturer}_<br />

<img src="https://mkrausai.github.io/img/persons/JuanOjeda.jpg" width="20%" alt="Juan Ojeda" /><br />
**Architect Juan Ojeda**<br />
PhD student <br />
Institute für Statik und Konstruktion (ISM+D)<br />
TU Darmstadt<br />
_Co-{Instrucor ; Lecturer}_<br />