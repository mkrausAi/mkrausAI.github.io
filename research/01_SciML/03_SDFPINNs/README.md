<!--https://mkrausai.github.io/research/01_SciML/03_SDFPINNs-->
<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=default'></script>


# SDF-PINNs: Joining Physics-Informed Neural Networks with Neural Implicit Geometry Representation

<!-- A repository of structural information on the design of pedestrian bridges
============================== -->

*   [Abstract](#Abstract)
*   [Methods](#methods)
*   [SDF-PINN Framework](#MLmodel)
*   [Results and Discussions](#Results)
*   [Conclusions](#Conclusions)
*   [References](#References)
*   [Contributors](#contributors)


<!-- -->
<!-- *   [Citation](#citation)-->

## <a name="Abstract"></a>Abstract
This paper presents an advanced method for solving boundary value problems of differential equations over arbitrary spatial domains using Physics-Informed Neural Networks (PINNs) augmented with Signed Distance Functions (SDF). Our approach builds on the framework where the solution to the differential equation is decomposed into two parts: one that inherently satisfies the boundary conditions without any adjustable parameters, and a second that incorporates a physics-informed neural network with adjustable parameters. We propose to use a neural network approximation of the SDF for representation of boundary conditions to model complex geometries accurately in an efficient manner. This novel combination allows for the precise enforcement of Dirichlet boundary conditions and improved solution accuracy over traditional PINN methods. We demonstrate the effectiveness of our approach through an illustrative example of a Poisson equation over a domain bound by the TUM logo. Our results indicate that this method not only preserves the benefits of neural networks in handling various types of differential equations but also leverages the geometric flexibility of SDFs to address complex boundary conditions effectively.

The publication can be found <a href="https://onlinelibrary.wiley.com/doi/10.1002/cepa.2587" target="_blank">here</a>.


## <a name="methods"></a>Methods

<p>We are interested in solving stationary PDEs of the form</p>

<p>
    <em>Lu</em> = <em>f</em>, &nbsp;&nbsp;&nbsp; <em>x</em> &isin; &Omega; &nbsp;&nbsp;&nbsp; (1)<br>
    <em>Bu</em> = <em>g</em>, &nbsp;&nbsp;&nbsp; <em>x</em> &isin; &Gamma; &sub; &part;&Omega; &nbsp;&nbsp;&nbsp; (2)
</p>

<p>where <em>L</em> is a differential operator, <em>f</em> a forcing function, <em>B</em> a boundary operator, and <em>g</em> the boundary data. The domain of interest is &Omega; &sub; &#8477;<sup><em>N</em></sup>, &part;&Omega; denotes its boundary, and &Gamma; is the part of the boundary where boundary conditions should be imposed. Specifically in the context of this paper, we assume <em>B</em> to be the identity operator, which implies PDEs with Dirichlet boundary conditions. The extension to other operator types will be discussed in an upcoming paper.</p>

Physics Informed Neural Networks (PINNs) leverage neural networks to approximate solutions to differential equations while incorporating physics-based constraints into the loss function, allowing them to generate accurate and physically consistent models with no or limited data (Bischof et al., 2022; Bischof et al., 2023). This paper sticks to the no-data forward only setting of time-independent PINNs, which implies loss functions for the boundary and the governing PDE only. The solution is obtained via tuning the trainable parameters (weights and biases) of the fully connected feed-forward neural network via numerical optimization of the scalarized combined losses.

Neural shape representation refers to representing 3D geometry using neural networks, e.g., to compute a signed distance or occupancy value at a specific spatial position (Jeske et al., 2023). After training on the discretely represented samples, the estimated geometry signal is implicitly encoded in the network, where recent works have shown the ability to capture intricate details of 3D geometry with ever increasing fidelity. However, discrete representations comes with a significant drawback: They only contain a discrete amount of information regarding the signal.

Neural shape representation employs neural networks to encode 3D geometry, typically by computing signed distance (SDF) or occupancy values at given spatial coordinates (Jeske et al., 2023). This approach has recently demonstrated remarkable capability in capturing intricate geometric details of complex 3D shapes with high fidelity. The neural network, once trained on discretely represented samples, implicitly encodes the estimated geometry signal within its parameters. Neural signed distance functions (SDFs) offer several key advantages, including the ability to represent complex 3D shapes with infinite resolution, arbitrary topology, and continuous, differentiable surfaces, while providing a compact and memory-efficient encoding of geometry that can be easily manipulated and rendered.

# <a name="sec:MLmodel"></a> SDF-PINN Framework
<p>In order to solve the PDE defined by equations (1-2), we propose to combine neural SDF and PINN within the following ansatz, which by construction automatically fulfills the boundary constraints:</p>

<p style="text-align: center;">
    <em>û</em>(<em>x</em>) = <em>v</em>(<em>x</em>)<em>d</em>(<em>x</em>) + <em>h</em>(<em>x</em>) &nbsp;&nbsp;&nbsp; (3)
</p>

<div style="text-align:center; white-space: nowrap;">
  <img src="https://mkrausai.github.io/research/01_SciML/03_SDFPINNs/figs/Figure_01.jpg" width="50%" alt="cVAE_Model" /><br />
  Figure 1: Proposed Network for combining a Neural Signed Distance Function with a Physics-Informed Neural Network to solve Partial Differential Equations.<br />
</div>
<br />

<p>Here <em>v</em> is a smooth function carefully chosen to vanish on &Gamma; and not to vanish anywhere inside the region, hence we suggest it to be a smooth distance function for <em>x</em> &isin; &Omega; to &Gamma; (specifically in the context of this paper we chose the signed distance function / SDF). <em>h</em> is also a smooth, globally defined function. Specifically note, that we can precompute <em>v</em> and <em>h</em> using either analytical formulae (in simple cases) or small neural networks on a subset of collocation points, as the exact form of both functions is not important. <em>d</em> is a PINN and needs to be trained on a discrete grid of collocation points in the region &Omega; via minimizing the induced cost function as shown in Fig. 1.</p>

<div style="text-align: center;">
    <table style="border-collapse: collapse; margin: 0 auto;">
        <caption>Table 1: Hyperparameters together with their final values of the neural SDF as well as PINN.</caption>
        <thead>
            <tr>
                <th style="border: 1px solid black; padding: 5px;">Hyperparameter</th>
                <th style="border: 1px solid black; padding: 5px;">Neural SDF <em>v</em>(<em>x</em>)</th>
                <th style="border: 1px solid black; padding: 5px;">PINN <em>d</em>(<em>x</em>)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">Number of Layers N<sub>L</sub></td>
                <td style="border: 1px solid black; padding: 5px;">6</td>
                <td style="border: 1px solid black; padding: 5px;">6</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">Number of Neurons per Layer N<sub>N</sub></td>
                <td style="border: 1px solid black; padding: 5px;">512</td>
                <td style="border: 1px solid black; padding: 5px;">512</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">Activation Function</td>
                <td style="border: 1px solid black; padding: 5px;">relu</td>
                <td style="border: 1px solid black; padding: 5px;">tanh</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">Fourier Feature map size</td>
                <td style="border: 1px solid black; padding: 5px;">256</td>
                <td style="border: 1px solid black; padding: 5px;">256</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;">B sampled from isotropic Gaussian with</td>
                <td style="border: 1px solid black; padding: 5px;">&sigma; = 1</td>
                <td style="border: 1px solid black; padding: 5px;">&sigma; = 1</td>
            </tr>
        </tbody>
    </table>
</div>


## <a name="Results"></a> Results and Discussions
<p>To study the proposed method, we investigate a membrane structure with prescribed deflection on the boundary &Gamma; over a domain &Omega; in form of the TUM logo using Poisson's equation:</p>

<p style="text-align: center;">
    -&nabla;<sup>2</sup> <em>u</em> = 100, &nbsp;&nbsp;&nbsp; <em>x</em> &isin; &Omega; &nbsp;&nbsp;&nbsp; (4)<br>
    <em>u</em> = 0, &nbsp;&nbsp;&nbsp; <em>x</em> &isin; &Gamma; &sub; &part;&Omega; &nbsp;&nbsp;&nbsp; (5)
</p>

<p>The FEM reference solution data for <em>u</em> were obtained via the MATLAB 2024 PDE toolbox with a mesh of max 0.01 size. The SDF-PINN implementation is using Tensorflow 2.</p>

<p>As both, the input domain &Omega; and boundary geometry &Gamma; are quite complex, we employ Fourier Features (Tancik et al., 2020) within a custom Keras layer for the SDF network <em>v</em>(<em>x</em>) specified in Table 1, the Dirichlet boundary network is trivial <em>h</em>(<em>x</em>) &equiv; 0. The PINN architecture <em>d</em>(<em>x</em>) is also provided in Table 1. Figure 2 shows the FEM solution <em>u</em><sub>FEM</sub> next to the SDF-PINNs solution <em>u</em><sub>(SDF-PINN)</sub> for the Poisson Equation over the domain &Omega; in form of the TUM logo</p>


<div style="text-align:center; white-space: nowrap;">
  <img src="https://mkrausai.github.io/research/01_SciML/03_SDFPINNs/figs/Figure_02.jpg" width="50%" alt="cVAE_Model" /><br />
  Figure 2: Poisson Equation over the TUM logo with Dirichlet boundary condition: (i) FEM reference, (ii) SDF-PINNs result, (iii) Absolute Error.<br />
</div>
<br />

As can be seen from Figure 2, there is almost excellent agreement between the FEM reference and the SDF-PINNs solution. 

## <a name="Conclusions"></a> Conclusions
In this paper, we introduced a novel method for solving PDEs with Dirichlet boundary conditions in arbitrarily complex geometries using a combination of PINNs and neural SDFs. The effectiveness of our method is demonstrated via a Poisson problem on the TUM logo versus a standard FEM solution. We found a very good agreement between the two solution methods, where the SDF-PINNs approach comes with the promise of transfer learning to other domains. Future work will focus on extending the approach to other boundary conditions such as Neuman or Robin conditions as well as to inspect the SDF computation and the neural SDF representation with techniques such as convolutional layers, dropout, and batch normalization.

## <a name="References"></a> References
Bischof, R., & Kraus, M., 2021. Multi-objective loss balancing for physics-informed deep learning. arXiv preprint arXiv:2110.09813.
Bischof, R., & Kraus, M., 2022. Mixture-of-experts-ensemble meta-learning for physics-informed neural networks. In Proceedings of 33. Forum Bauinformatik, pp. 317-324.
Jeske, S. R., Klein, J., Michels, D. L., & Bender, J. (2023). Zero-Level-Set Encoder for Neural Distance Fields. arXiv preprint arXiv:2310.06644.
Tancik, M., Srinivasan, P., Mildenhall, B., Fridovich-Keil, S., Raghavan, N., Singhal, U., Ramamoorthi, R., Barron, J. & Ng, R., 2020. Fourier features let networks learn high frequency functions in low dimensional domains. Advances in neural information processing systems, 33, 7537-7547.



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
<div style="display:flex; justify-content: center;">
  <div style="flex:1">
    <img src="https://mkrausai.github.io/img/persons/Michael6_3.jpg" alt="Michael" style="width:40%">
    <div style="text-align:center"> Univ.-Prof. Dr.-Ing. Michael A. Kraus, M.Sc.(hons) <br />
    Professor for Structural Analysis, TU Darmstadt <br /></div>
  </div>
  <div style="flex:1">
    <img src="https://mkrausai.github.io/img/persons/konstantinos_tatsis.jpg" alt="Konsti" style="width:62%">
    <div style="text-align:center">Dr. Konstantinos Tatsis<br />
Data Scientist at Swiss Data Science Center (SDSC), Zurich <br /></div>
  </div>
</div>


# Contact
Univ.-Prof. Dr.-Ing. Michael A. Kraus, M.Sc.(hons)
Institut für Statik und Konstruktion (ISMD)
TU Darmstadt
kraus@ismd.tu-darmstadt.de
<a href="https://www.ismd.tu-darmstadt.de/das_institut_ismd/mitarbeiter_innen_ismd/team_ismd_details_109888.de.jsp">Visit Prof. Dr. Michael Anton Kraus</a>

------------
Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

