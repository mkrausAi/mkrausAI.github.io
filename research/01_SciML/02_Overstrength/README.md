<!--https://mkrausai.github.io/research/01_SciML/02_Overstrength-->
<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=default'></script>


# Predictive modelling and latent space exploration of steel profile overstrength factors using multi-head autoencoder-regressors

<!-- A repository of structural information on the design of pedestrian bridges
============================== -->

*   [Abstract](#Abstract)
*   [Introduction](#intro)
*   [Methods](#methods)
*   [Content](#content)
*   [Contributors](#contributors)

<!-- -->
<!-- *   [Citation](#citation)-->

## <a name="Abstract"></a>Abstract
This research investigates the suitability and interpretability of a data-driven deep learning algorithm for multi cross sectional overstrength factor prediction. For this purpose, we first compile datasets consisting of experiments from litera-ture on the overstrength factor of circular, rectangular and square hollow sec-tions as well as I- and H-sections. We then propose a novel multi-head en-coder architecture consisting of three input heads (one head per section type represented by respective features), a shared embedding layer as well as a subsequent regression tail for predicting the overstrength factor. By construc-tion, this multi-head architecture simultaneously allows for (i) the exploration of the nonlinear embedding of different cross-sectional profiles towards the overstrength factor within the shared layer, and (ii) a forward prediction of the overstrength factor given profile features. Our framework enables for the first time an exploration of cross-section similarity w.r.t. the overstrength factor across multiple sections and hence provides new domain insights in bearing capacities of steel cross-sections, a much wider data exploration, since the encoder-regressor can serve as meta model predictor. We demonstrate the quality of the predictive capabilities of the model and gain new insights of the latent space of different steel sections w.r.t. the overstrength factor. Our pro-posed method can easily be transferred to other multi-input problems of Scientific Machine Learning.

The publication can be found <a href="https://mkrausai.github.io/ResearchWork/published/20230422_Kraus_Mueller_Bischof_Taras_Overstrength.pdf" target="_blank"> here</a>.


## <a name="intro"></a>Introduction
The performance of steel structures is influenced by the behavior of their load-bearing components, particularly the flexural characteristics. Designing steel constructions that can provide sufficient local ductility for the development of plastic hinges while maintaining moment capacity is crucial for ensuring a global dissipative mechanism. In the context of bending steel beams, two key parameters, rotation capacity ($$r$$) and flexural overstrength ($$s$$), play a decisive role. Understanding these parameters is essential for achieving safe and reliable structural designs, especially when considering seismic codes such as EN 1998. While empirical methods exist to estimate the rotation capacity $$r$$ and flexural overstrength $$s$$ of steel members, there is a need for comprehensive analytical estimation, specifically for circular (CHS), rectangular (RHS), and square (SHS) hollow sections, as well as I and H profiles. This study aims to develop a precise and efficient deep learning technique for predicting the flexural overstrength factor of steel beams with different cross sections under pure bending. This technique will enable the identification of latent correlations and provide a better understanding of cross-sectional similarities concerning flexural overstrength $$s$$.

## <a name="methods"></a>Methods

# <a name="sec:Overstrength"></a> The Flexural Overstrength Factor $$s$$
The flexural overstrength factor $$s$$ is a non-dimensional parameter used for characterizing the ultimate bending capacity of steel beams exceeding the plastic bending strength due to the strain hardening [2]. It is originally ([3],[4]) computed by the ratio of the stress fLB corresponding to complete local buckling development or the lateral torsional buckling to the yield stress $$fy$$: <br />
$$s = \frac{f_LB}{f_y} = \frac{M_u}{M_p} $$ <br />
or by the more practical relation using the maximum moment $$M_u$$ to the theoretical full plastic moment $$M_p$$. The ultimate bearing capacity of steel beams can be significantly greater than the plastic bending strength because of strain hardening before complete local buckling or fractures as given in Figure 1 by the generalized moment-rotation curves. The overstrength factor is used for seismic design in the Italian codes OPCM 3274 (2003) and NTC 2018 but neglected for cross-section classes in Eurocode 3 (EN 1993:1-1).

<div style="text-align:center;">
  <img src="https://mkrausai.github.io/research/01_SciML/02_Overstrength/figs/Figure_01.png" alt="Generalized moment–rotation curve for a steel beam and EN 1993:1-1 classification criteria." />
  </a>
</div>



# <a name="sec:data"></a> Database
The training of the deep latent generative model is collected in a two-stage approach: a central Latin Hypercube Sampling of the design space is launched at first. At second, the sampled design features $$\mathbf{x}$$ are handed to performance simulators to obtain the performance metrics $$\mathcal{P}(\mathbf{x})$$ as defined before, where analytical formoluae as well as the Finite-Element-Analysis software "Sofistik" is utilised. A parametric template for the FEA-based structural analysis was developed and connected to Revit via zero-touch nodes inside Dynamo for the FEA performance simulator to be able to evaluate the vast amounts of parameter samples in a standardised way.

# <a name="sec:MLmodel"></a> Deep Learning Model
The ML model used in this study is a variation of Conditional Variational Autoencoders (CVAE) \cite{cvae_sohn}. In light of having to solve both a forward as well as an inverse problem, we forgo feeding the conditional $$\mathbf{y}$$ to the encoder and instead let it predict the performance metrics together with a latent vector in two separate heads as shown below.

**cVAE Model**<br />
<img src="https://mkrausai.github.io/research/01_SciML/01_BH_PedestrianBridge_XAI/figs/cvae.JPG" width="50%" alt="cVAE_Model" /><br />
 Architecture of our CVAE network acting both as surrogate as well as generative model<br />


# <a name="sec:sensitivity"></a> Explainability through Design Sensitivity Analysis
This research adopts the idea of Sensitivity Analysis (SA), which is well-known in Finite-Element-Analysis by taking the derivative of the performance metrics w.r.t. the design variables Computing these derivatives in established solvers such as the FEM is expensive, while deep learning models, such as the proposed CVAE of this project, deliver these very efficiently through Automatic Differentiation (AD). When inspecting the sensitivity of a performance metric $$\frac{\partial \mathbf{\hat{y}_i}}{\partial \mathbf{x}}$$ for a certain design $$\mathbf{x}$$, the designer receives information in which direction the design variables should be changed in order to improve the particular performance attribute. Furthermore, the distribution of sensitivities over a large set of designs yields information about the network's decision-making. An expert designer with prior knowledge in the design, analysis and construction of bridges can therefore, to a certain extent, estimate the model's reliability based on the relations it found between the features.
%

## <a name="sec:Results"></a> Results and Discussion

The results of the hyperparameter tuning can be found at our Weights&Biases <a href="https://wandb.ai/ai4structeng_ethz/Multihead_AE_forward_overstrength_full/reports/Predictive-modelling-and-latent-space-exploration-of-steel-profile-overstrength-factors-using-multi-head-autoencoder-regressors--Vmlldzo0NTQyNTU5" target="_blank"> project homepage </a>.



We sampled 18'000 instances of the pedestrian bridges together with their performances within the generative design as described before to form the dataset for subsequent CVAE training. While the Latin-Hypercube-Sampling of the Design space was conducted in a few seconds, obtaining performances of a batch of 600 design instances via FEA took on average around 55 minutes.

Below we show the prototype of a user interface for the inverse design situation developed within Revit Dynamo. It provides the user with sliders and check-boxes, allowing to set desired performance metrics such as ranges for costs or the maximum structural utilisation in the ultimate as well as serviceability limit state. More fine grained requests for different objectives, as well as an additional visualisation of the latent space and the mapping of the objectives, is also possible, yet has been omitted for the sake of clearness. The right hand side of the user interface displays the sensitivity plots as well as a scatter plot for finding the Pareto front. Finally, a rendering of the generated bridge is shown, which can be inspected either on the screen in 2D, or in 3D through virtual reality on smartphones or dedicated devices.

We demonstrated our developments to a selected group of researchers and practitioners (15 persons) within a hands-on session. The collected feedback towards ergonomics, efficiency and quality prove our framework to be intuitive, efficient, reliable and to bear a great potential for applications in practice.

<img src="https://mkrausai.github.io/research/01_SciML/01_BH_PedestrianBridge_XAI/figs/XAI_Overview.PNG" width="80%" alt="XAI_Overview" /><br />
[![Explainable AI Interface for Forward and Inverse Pedestrian Bridge Design](https://youtu.be/6pVvFye_5ko/0.jpg)](https://youtu.be/GbXYkEoFv9Q "Explainable AI Interface for Forward and Inverse Pedestrian Bridge Design")

## <a name="sec:Conclusions"></a> Conclusions
Our proposed framework for design subspace learning establishes a new paradigm for performance-conditioned exploration of design spaces, which is neither an optimisation setting nor a random process. Rather, it provides an intuitive and efficient cartography of the vastness of these design spaces. Instead of replacing human intuition with predefined, deterministic, quantitative rules, the AI acts as a design collaborator/co-pilot that augments the human designer's intuition on the problem at hand.

This research provides a variation of CVAEs tailored to forward and inverse design situations. We showed the potential of our CVAE in meta-modelling (i) the forward problem by providing a surrogate to estimate more efficiently and quickly design performances given design features, (ii) compression of complex design spaces into continuous, smooth, low-dimensional design subspaces. With a forward pass through our CVAE being extremely efficient, it can provide performance conditioned designs in quasi real-time and thus augment human designers by providing instant feedback and proposals during the iterative prototyping phase. Furthermore, with analytical derivatives inherently provided in neural networks, we demonstrated that the sensitivity analysis serves as powerful tool for both design optimisation as well as model interpretability. The latter is crucial for building trust and achieving wide acceptance of this kind of design augmentation tools in the AEC domain. The collected user responses prove our framework possesses the potential to find wide application in industry and research as a co-pilot for conceptual design studies in the AEC domain beyond pedestrian bridges.


## <a name="sec:WebApp"></a> Web Application
Now it is turn to try out our neural network overstrength predictors yourself. Just follow these steps:
1) 




<!--
## <a name="citation"></a>Citation

[xxx](http://www.sciencedirect.com/science/article/pii/S1876610217330047) 

[ResearchGate](https://ww)

```
BibTex:
@article{xxx,
title = "xxx ",
journal = "xx"
}
```
 -->
## <a name="contributors"></a>Contributors
<div style="display:flex">
  <div style="flex:1; margin-right:10px">
    <img src="https://mkrausai.github.io/img/persons/Michael6_3.jpg" alt="Michael" style="width:100%">
    <div style="text-align:center"> Dr. Michael A. Kraus, M.Sc.(hons) <br />
    Senior Researcher in SciML4AEC and Co-Leader of the Immersive Design Lab of Design++ at ETH Zurich <br /></div>
  </div>
  <div style="flex:1; margin-right:10px">
    <img src="https://mkrausai.github.io/img/persons/andreasmueller.jpeg" alt="Mueller" style="width:100%">
    <div style="text-align:center">M.Sc. Andreas Müller<br />
Doctoral Researcher in Steel Structures and SciML4AEC at ETH Zurich <br /></div>
  </div>
  <div style="flex:1; margin-right:10px">
    <img src="https://mkrausai.github.io/img/persons/Rafael-Bischof.png" alt="Rafi" style="width:100%">
    <div style="text-align:center">M.Sc. Rafael Bischof <br /> Doctoral Researcher in SciML4AEC at ETH Zurich</div>
  </div>
  <div style="flex:1">
    <img src="https://mkrausai.github.io/img/persons/AndreasTaras.jpg" alt="Taras" style="width:95%">
    <div style="text-align:center"> Prof. Dr. Andreas Taras <br /> Professor for Steel Construction and Composite Structures at ETH Zurich </div>
  </div>
</div>

# Contact
Dr. Michael A. Kraus, M.Sc.(hons)
Institute für Baustatik und Konstruktion (IBK)
ETH Zürich
kraus@ibk.baug.ethz.ch
https://kaufmann.ibk.ethz.ch/de/personen/mitarbeitende/dr-michael-anton-kraus.html


------------
Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

