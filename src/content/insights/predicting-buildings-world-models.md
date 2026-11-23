---
title: "Predicting Buildings That Don’t Exist Yet: World Models and Architecture"
standfirst: "Architecture has embraced AI for illustrating and writing. World models, a resurgent class of AI, point to something more valuable: testing what a design will do before it is built."
author: conor-black
authorBio: "Conor Black is a Computational Design Specialist at HOK and a Research Fellow in Emerging Technologies at the Centre for Technology and Society, University of Oxford. He works across architecture and computational design, and his research covers architectural geometry, machine learning for human experience, and AI in architectural education."
date: 2026-11-23
themes: ["methods"]
series: "AI and the built environment"
description: "Conor Black asks what world models, a resurgent class of AI, could mean for architecture: predicting how buildings will perform before they are built, and how architects learn design judgement."
---
<p>Every architect carries a world model. Long before a line is drawn, a designer is running small simulations in their head. If this wall moves, does the room get darker? If the stair goes here, where will the queue form? In 1943 the psychologist Kenneth Craik described the mind as carrying a “small-scale model” of reality, used to try out alternatives before acting on them.<sup class="fn"><a href="#fn-1" id="fnref-1">1</a></sup> Antoni Gaudí built one out of string: a hanging model of cords and small weighted bags that let gravity work out the shape of his arches before a stone was laid.</p>
<!-- Lead slideshow photos (resized only, shown uncropped); 1, 2 and 4 from Wikimedia Commons, 3 from Pexels:
1. Sagrada Família exterior, April 2026. Photo: Wikipsico43, CC BY-SA 4.0
https://commons.wikimedia.org/wiki/File:Sagrada_Fam%C3%ADlia_exterior_Barcelona_2026.jpg
2. Reconstruction of Gaudí's hanging model for the Colònia Güell church, Sagrada Família museum. Photo: Canaan, CC BY-SA 4.0
https://commons.wikimedia.org/wiki/File:Maqueta_funicular.jpg
3. Nave columns of the Sagrada Família. Photo: AXP Photography, Pexels License (free to use; attribution optional)
https://www.pexels.com/photo/the-ceiling-of-sagrada-familia-in-barcelona-spain-27348442/
4. Ceiling of the Sagrada Família. Photo: Alvesgaspar, CC BY-SA 4.0 (Wikimedia Commons Featured Picture)
https://commons.wikimedia.org/wiki/File:Sagrada_Familia_March_2015-10a.jpg -->
<figure class="slideshow slideshow--lead" id="lead-ss" aria-roledescription="carousel" aria-label="Gaudí's hanging model and the Sagrada Família">
<div class="ss-frame">
<div class="ss-track">
<div class="ss-slide is-active" role="group" aria-roledescription="slide" aria-label="1 of 4"><img src="{{ "/assets/img/insights/world-models/sagrada-exterior.jpg" | url }}" alt="The Sagrada Família's spires against a clear blue sky, with a large cross on the central tower and a construction crane alongside, above trees"></div>
<div class="ss-slide" role="group" aria-roledescription="slide" aria-label="2 of 4" aria-hidden="true"><img src="{{ "/assets/img/insights/world-models/gaudi-hanging-model.jpg" | url }}" alt="Hundreds of strings and small weighted bags hanging from a frame, forming an upside-down outline of a church's arches and vaults, reflected in a mirror below"></div>
<div class="ss-slide" role="group" aria-roledescription="slide" aria-label="3 of 4" aria-hidden="true"><img src="{{ "/assets/img/insights/world-models/sagrada-nave.jpg" | url }}" alt="Looking up into the Sagrada Família's nave: tall columns branch like trees into a vaulted ceiling of gold and white sunburst shapes, with blue stained glass to one side"></div>
<div class="ss-slide" role="group" aria-roledescription="slide" aria-label="4 of 4" aria-hidden="true"><img src="{{ "/assets/img/insights/world-models/sagrada-vaults.jpg" | url }}" alt="Looking straight up into the Sagrada Família's vaults: branching, tree-like columns open into a ceiling of star-shaped openings"></div>
</div>
<button class="ss-btn ss-prev" type="button" aria-label="Previous image">‹</button>
<button class="ss-btn ss-next" type="button" aria-label="Next image">›</button>
<button class="ss-toggle" type="button" aria-pressed="false">Pause</button>
<span class="ss-count">1 / 4</span>
</div>
<div class="ss-bar">
<p class="ss-caption" aria-live="off">The Sagrada Família, Barcelona, in April 2026. A century after Gaudí’s death, it is still being built.</p>
<div class="ss-dots" role="group" aria-label="Choose image"></div>
</div>
<p class="ss-credit">Photo: <span class="ss-photo"><a href="https://commons.wikimedia.org/wiki/File:Sagrada_Fam%C3%ADlia_exterior_Barcelona_2026.jpg">Wikipsico43</a>, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>, via Wikimedia Commons</span></p>
</figure>
<p>AI is now being built to do something similar. Architecture has adopted these tools quickly, but their use has so far focused largely on visualisation and content generation rather than predicting how buildings will perform. In the 2026 survey by the Royal Institute of British Architects (RIBA), a self-selecting sample of more than 1,100 respondents, 74% of practices used AI on at least some projects, up from 41% in 2024. The most common use was early-stage design visualisation, by 56% of AI-using practices; only 7% used AI for building performance simulation, and 6% for environmental impact modelling.<sup class="fn"><a href="#fn-2" id="fnref-2">2</a></sup></p>
<figure class="embed" id="fig-riba">
<div class="fig-card">
<div class="fig-head">
<h3>Architects use AI to illustrate and write, rarely to predict</h3>
<p>Share of AI-using practices applying AI in each area, 2026. Respondents could choose several areas.</p>
</div>
<div class="fig-controls">
<button class="chip" id="riba-hl" type="button" aria-pressed="true">Highlight uses that predict performance</button>
<button class="chip" id="riba-sort" type="button" aria-pressed="false">Sort A–Z</button>
</div>
<div style="position:relative">
<ul class="bars hl" id="riba-bars" aria-label="Bar chart of AI uses"></ul>
<div class="tooltip" id="riba-tip" role="status"></div>
</div>
<div class="legend"><span class="lg-pred">Predicts how a building will perform</span><span>Other uses</span></div>
</div>
<figcaption>Practices already using AI, UK and international; survey of more than 1,100 self-selecting respondents, March–April 2026. Chart: Conor Black. Data: RIBA <em>AI Report 2026</em>, p.20.<sup class="fn"><a href="#fn-2" id="fnref-2-2">2</a></sup> Hover over or tap a bar for its value.</figcaption>
</figure>
<p>The profession is also unconvinced by the results. Only 17% of RIBA respondents said their designs were better because of AI, while 42% disagreed.<sup class="fn"><a href="#fn-2" id="fnref-2-3">2</a></sup> Tom Holberton, writing in the same report, suggests one reason: “Architecture does not encode all its intelligence through a syntax of language or photos”, yet those are what most AI has been trained on.<sup class="fn"><a href="#fn-3" id="fnref-3">3</a></sup></p>
<figure class="insight-quote"><blockquote><p>Buildings are made of space, matter and time. Our tools have learned from text and images.</p></blockquote></figure>
<h2>World models</h2>
<p>World models are designed to learn how an environment changes over time. Given a description of its current state, and sometimes an action, they predict a subsequent state. The idea has roots in research from around 1990, but became more prominent in deep learning following work such as Ha and Schmidhuber’s <em>World Models</em> in 2018.<sup class="fn"><a href="#fn-4" id="fnref-4">4</a>,<a href="#fn-5" id="fnref-5">5</a>,<a href="#fn-6" id="fnref-6">6</a></sup></p>
<p>Since 2024–25, world models have become a major frontier in AI research, broadly along two lines. Generative approaches, such as Google DeepMind’s Genie 3, render predicted worlds as images and interactive environments.<sup class="fn"><a href="#fn-7" id="fnref-7">7</a></sup> Latent-predictive approaches, such as Yann LeCun’s JEPA, predict in a learned internal representation rather than reconstructing every visual detail.<sup class="fn"><a href="#fn-8" id="fnref-8">8</a></sup> For architecture, that matters: designers need predicted consequences, not pictures.</p>
<p>Robotics is already testing this. Meta’s V-JEPA 2, pre-trained on over a million hours of internet video and then adapted with less than 62 hours of robot footage, let robot arms pick and place objects in labs they had never seen.<sup class="fn"><a href="#fn-9" id="fnref-9">9</a></sup> Action-conditioning is particularly relevant to design. A model could be given an existing design and asked to predict what changes when a wall is moved, a circulation route is altered or a space is made larger. The analogy with robotics is not exact: robots act within an environment, while architects are changing the environment itself, often with consequences for the people who will use it.</p>
<figure class="photowide" id="fig-vjepa">
<!-- Sprite: 24 frames in an 8 x 3 grid (three trials, eight frames each, read left to right),
from Figure 10 of Assran et al. (2025), arXiv:2506.09985, CC BY 4.0. Cropped to remove the
highlight borders. Embedded below as a data URI; it can be saved out and hosted as a file. -->
<div class="flip" id="flip" data-src="{{ "/assets/img/insights/world-models/vjepa-frames.jpg" | url }}" data-cols="8" data-rows="3" role="img" aria-label="Animated sequence of three trials: a robot arm picks up and moves a pink cup, a green box and a beige cup">
<div class="flip__frame" id="flip-frame"></div>
<p class="flip__fallback" id="flip-fallback">Loading the robot sequence…</p>
</div>
<div class="flip__controls">
<button class="chip" type="button" id="flip-play" aria-pressed="true">Pause</button>
<div class="flip__ticks" id="flip-ticks" role="group" aria-label="Choose frame"></div>
<span class="flip__count" id="flip-count">Trial 1 · 1 / 8</span>
</div>
<figcaption>Meta’s V-JEPA 2-AC world model planning pick-and-place tasks on a Franka robot arm, working towards a series of goal images with no task-specific training. Three trials, two with cups and one with a box. Frames from Figure 10 of Assran et al. (2025), arXiv:2506.09985, CC BY 4.0; cropped and animated.</figcaption>
</figure>
<h2>How could world models change the design process?</h2>
<p>Design has always worked as a loop. Donald Schön called it a “reflective conversation with the situation”: the designer makes a move, sees what it does, and adjusts.<sup class="fn"><a href="#fn-10" id="fnref-10">10</a></sup> The slow and expensive part has always been seeing what the move does. Sketches, physical models and simulations all exist to answer that.</p>
<p>The evidence designers rely on today is not as strong as one might think. Innovate UK’s Building Performance Evaluation programme studied 49 modern non-domestic buildings. On average they used 3.5 times the energy they were designed to use, and only one matched its predicted emissions.<sup class="fn"><a href="#fn-11" id="fnref-11">11</a></sup> The problems it reported were operational ones, from over-complicated controls to poorly integrated building management systems.</p>
<p>Architecture already has prediction tools. Physics-based simulation computes daylight, energy and airflow from first principles; agent-based models simulate crowds person by person; statistical models and optimisation workflows search for better options; digital twins, live digital copies fed by sensors, track buildings already in use. Each predicts selected outcomes under defined assumptions. Machine learning surrogates accelerate those predictions, usually within one domain, by learning to reproduce a particular simulator; some already ship in commercial software.<sup class="fn"><a href="#fn-12" id="fnref-12">12</a></sup> None of these is technically a world model.</p>
<p>An architectural world model would do something different. Rather than mapping a design to one output, it would learn a representation of an environment and how its state changes, from simulation, operational data and observations of buildings in use. That would add four things existing tools lack: generalisation across buildings, rather than one project or one twin; prediction across domains, so that light, movement, sound and use are read from the same model; action-conditioning, so that any intervention, by a designer or by an occupant, can be tested for its consequences; and a model of the environment itself, not just of individual outputs.</p>
<p>Narrow but promising steps towards this already exist. My case study with James Ward (Arup) describes research that used office sensor data, from entry logs to meeting bookings, to build behavioural personas and simulate a full working day. A machine learning model trained on the results then predicts movement through a new layout in under a second, where a full-day simulation can take hours.<sup class="fn"><a href="#fn-13" id="fnref-13">13</a></sup> Strictly, it is a surrogate rather than a world model: it learns from a simulator, not from the building itself. But because it works through personas, it can in principle represent people an average plan overlooks, such as neurodiverse staff or those with different mobility needs, and test whether a layout works for them before it is built.</p>
<figure class="photowide" id="fig-scosa">
<img src="{{ "/assets/img/insights/world-models/heatmap-arup.jpg" | url }}" alt="Two heat maps of the same office floorplate: on the left, movement from an agent-based simulation shown in blue; on the right, the machine learning model's predicted movement shown from blue (low) to red (high)" loading="lazy">
<figcaption>Left: movement across a workplace floorplate from an agent-based simulation, which took around 30 minutes to compute. Right: the machine learning model’s prediction for the same floorplate, produced in around a second. From the author’s case study in the SCOSA AI Working Group report (2025). Image: Arup.</figcaption>
</figure>
<h2>How will architects learn design judgement?</h2>
<p>Earlier waves of design technology took on routine work. Computer-aided design (CAD) took over drafting; building information modelling (BIM) structured coordination. World models are among the first technologies aimed squarely at the prediction step in design judgement. A BIM model records the outcome of a design, not the rationale behind it; the reasoning stays with the people and practices that produced it.<sup class="fn"><a href="#fn-14" id="fnref-14">14</a>,<a href="#fn-15" id="fnref-15">15</a></sup></p>
<figure class="embed" id="fig-bim">
<div class="fig-card">
<div class="fig-head">
<h3>A BIM model records what each element is, not what it does</h3>
<p>Select an element to see some of the information attached to it.</p>
</div>
<div class="fig-controls" id="bim-chips" role="group" aria-label="Choose an element"></div>
<div class="bim">
<svg class="bim-svg" viewBox="80 76 312 352" role="img" aria-label="Isometric drawing of a simple building with selectable door, window, wall, floor slab and roof">
<polygon class="bim-el" data-el="roof" points="200,250 373,150 269,90 96,190" fill="#ffffff" stroke="#9aaabb" stroke-width="1.25"/>
<polygon class="bim-el" data-el="wall" points="200,410 96,350 96,190 200,250" fill="#e8edf2" stroke="#9aaabb" stroke-width="1.25"/>
<polygon points="200,410 373,310 373,150 200,250" fill="#ffffff" stroke="#9aaabb" stroke-width="1.25"/>
<g stroke="#d8e0e8" stroke-width="1" fill="none">
<line x1="200" y1="370" x2="373" y2="270"/><line x1="200" y1="290" x2="373" y2="190"/>
<line x1="243.25" y1="385" x2="243.25" y2="225"/><line x1="286.5" y1="360" x2="286.5" y2="200"/><line x1="329.75" y1="335" x2="329.75" y2="175"/>
<line x1="200" y1="370" x2="96" y2="310"/><line x1="200" y1="290" x2="96" y2="230"/>
<line x1="165.68" y1="390.2" x2="165.68" y2="230.2"/><line x1="130.32" y1="369.8" x2="130.32" y2="209.8"/>
</g>
<path class="bim-el" data-el="slab" d="M200,333 L373,233 L373,227 L200,327 Z M200,333 L96,273 L96,267 L200,327 Z" fill="#c7d2dc" stroke="#9aaabb" stroke-width="1"/>
<polygon class="bim-el" data-el="window" points="243.25,305 286.5,280 286.5,240 243.25,265" fill="#dbe8f2" stroke="#9aaabb" stroke-width="1.25"/>
<polygon class="bim-el" data-el="door" points="295.15,355 312.45,345 312.45,313 295.15,323" fill="#c7d2dc" stroke="#9aaabb" stroke-width="1.25"/>
</svg>
<div class="bim-panel" aria-live="polite">
<p class="bim-panel__kicker">Selected element</p>
<p class="bim-panel__name" id="bim-name"></p>
<table><tbody id="bim-rows"></tbody></table>
<p class="bim-panel__note">Illustrative values, not from a real project.</p>
</div>
</div>
</div>
<figcaption>Illustration: Conor Black. A simplified building information model; real models attach many more properties to each element.</figcaption>
</figure>
<p>That design judgement is not taught directly, but acquired through repeated encounters with consequences: a section that left a room too dark, a stair that created a queue, a detail that failed on site. Schön observed that design students cannot simply be told what designing is. They have to start doing it, under a tutor’s eye, before they fully understand what they are learning.<sup class="fn"><a href="#fn-16" id="fnref-16">16</a></sup></p>
<p>This is why design education is not mainly about producing drawings or modelling geometry (drawings are just the by-product). What the studio teaches is the loop itself: propose, test, fail, revise and understand why. Practice continues that education. Junior designers are given high-volume analysis “precisely because those tasks are how expertise is built”.<sup class="fn"><a href="#fn-17" id="fnref-17">17</a></sup></p>
<p>Architects already build internal world models through experience. The paradox is that, by automating the very predictive loop through which architects acquire judgement, computational world models could either accelerate expertise or prevent it from forming.</p>
<p>A student who can test a hundred variations of a plan in an afternoon, and see how light, movement and use respond to each, could meet more consequences in a term than an earlier generation met in years. However, a model that returns an answer without its reasoning shows the outcome but not the mechanism, and the step that builds judgement is skipped. As Mario Carpo puts it, “computers do not need theories, we do”.<sup class="fn"><a href="#fn-18" id="fnref-18">18</a></sup></p>
<p>None of this is fixed by the technology: a world model used as an oracle, which returns a verdict, is likely to deskill. One used as a partner, which asks the designer to predict first, shows its reasoning and makes its uncertainty visible, could build judgement faster. Robert Aish, a pioneer of architectural design computation, and his co-authors describe the field’s future as “a conversation between human reasoning and machine intelligence”. That conversation, they argue, needs a language precise about units, uncertainty and tolerances, so that design decisions and their consequences can be explained to everyone they affect.<sup class="fn"><a href="#fn-15" id="fnref-15-2">15</a></sup></p>
<p>Des Fagan, who leads the Standing Conference of Schools of Architecture (SCOSA) AI Working Group, asks how schools can keep rigour and critical reflection when AI tools produce outputs that are “fast, plausible, and persuasive”.<sup class="fn"><a href="#fn-19" id="fnref-19">19</a></sup> The answer will lie in how studios assess work, how practices structure junior roles, and whether the RIBA’s planned AI Overlay to its Plan of Work, the UK industry’s standard map of a project’s stages, expects predictions to be explained, not just produced.<sup class="fn"><a href="#fn-2" id="fnref-2-4">2</a></sup></p>
<h2>What is missing?</h2>
<p><strong>Plausible is not the same as correct.</strong> A team including Fei-Fei Li found that multimodal models (AI systems that take in images and video as well as text) show spatial intelligence that is competitive but still below human level, with spatial reasoning the main bottleneck.<sup class="fn"><a href="#fn-20" id="fnref-20">20</a></sup> Foster + Partners’ applied research group makes the point from practice: for daylight, structure or acoustics, “we need physically accurate results, not statistically likely approximations”.<sup class="fn"><a href="#fn-21" id="fnref-21">21</a></sup></p>
<p><strong>World models learn the world as it is.</strong> Architecture is about worlds that do not exist yet. A model trained on existing buildings will predict best for buildings like the ones it has seen, nudging design towards precedent. And every building is built only once: a model can never observe the design that was not chosen, so it cannot check its predictions against the very alternatives it is meant to help compare.</p>
<p><strong>General models, private data.</strong> A general world model would learn what buildings share: how light falls, crowds move and rooms are used. But a model of everyone’s buildings predicts the average one, pulling design towards the generic. Distinctive architecture is more likely to come from the private data a practice, client or operator holds about its own buildings and their occupants, from post-occupancy studies to a venue’s crowd records. The V-JEPA 2 recipe, a large general model adapted with a little local data, shows how the two could combine.</p>
<p>That makes building data a scarce strategic asset. Few buildings are measured once occupied, much of the data tracks individuals, and only some is public, such as the energy certificates large public buildings in England and Wales must display.<sup class="fn"><a href="#fn-22" id="fnref-22">22</a></sup> Exclusivity cuts both ways: if every practice guards its evidence, the profession’s shared knowledge of how buildings perform stays thin. The companies building world models do not hold this data; owners, operators and practices do, and whoever brings the two together will shape whose interests these models serve.</p>
<p><strong>Someone has to be accountable.</strong> In England, the Building Safety Act, passed after the Grenfell Tower fire, requires new higher-risk buildings to pass Gateway 2, a regulator’s check of the design, before construction starts.<sup class="fn"><a href="#fn-23" id="fnref-23">23</a></sup> Any AI prediction entering that process will need to be auditable. In practice, responsibility will rest with the professional who relied on the prediction, and a prediction nobody can explain will be indefensible.</p>
<h2>Predicting buildings that don’t exist yet</h2>
<p>World models change the question architects should be asking of AI. For years the profession has asked what AI can <em>make</em>: images, text, options. The more important questions are what AI can <em>predict</em>, how we would know if it was wrong, and who answers for it when it is.</p>
<p>My own view is that the first useful architectural world models will be narrow rather than general: trained largely on simulation, checked against occupancy data, and built for particular building types such as offices, schools and venues. They will be built by whoever controls the data, and today that is rarely architects. The profession can shape these models now, by insisting that they show their reasoning and uncertainty, are tested against public benchmarks of real building performance, and are clearly labelled as exploration or evidence. Otherwise it will receive them later as finished products.</p>
<p class="closing-q">If world models do learn to predict how buildings behave, who should own the model of the world they predict from, and whose world will it be?</p>
<section class="footnotes" aria-label="Notes">
<h2 class="footnotes__title">Notes</h2>
<ol>
<li id="fn-1">Craik, K. J. W. (1943) <em>The Nature of Explanation</em>. Cambridge: Cambridge University Press. <a class="fn-back" href="#fnref-1" aria-label="Back to text">↩</a></li>
<li id="fn-2">Royal Institute of British Architects (2026) <em>AI Report 2026</em>. London: RIBA. Survey of more than 1,100 self-selecting respondents, March–April 2026; figures from pp.4, 16, 20, 25 and 31. <a href="https://www.riba.org/news/ai-adoption-reaches-tipping-point-across-uk-architecture/">riba.org/news/ai-adoption-reaches-tipping-point-across-uk-architecture</a> <a class="fn-back" href="#fnref-2" aria-label="Back to text">↩</a></li>
<li id="fn-3">Holberton, T. (2026) ‘Describing, deriving, doing’, in RIBA, <em>AI Report 2026</em>, pp.33–38. <a class="fn-back" href="#fnref-3" aria-label="Back to text">↩</a></li>
<li id="fn-4">Schmidhuber, J. (1990) ‘Making the World Differentiable: On Using Self-Supervised Fully Recurrent Neural Networks for Dynamic Reinforcement Learning and Planning in Non-Stationary Environments’, Technical Report FKI-126-90, Technische Universität München. <a href="https://people.idsia.ch/~juergen/FKI-126-90ocr.pdf">people.idsia.ch/~juergen/FKI-126-90ocr.pdf</a> <a class="fn-back" href="#fnref-4" aria-label="Back to text">↩</a></li>
<li id="fn-5">Sutton, R. S. (1990) ‘Integrated Architectures for Learning, Planning, and Reacting Based on Approximating Dynamic Programming’, <em>Proceedings of the Seventh International Conference on Machine Learning (ICML)</em>. <a href="http://incompleteideas.net/papers/sutton-90.pdf">incompleteideas.net/papers/sutton-90.pdf</a> <a class="fn-back" href="#fnref-5" aria-label="Back to text">↩</a></li>
<li id="fn-6">Ha, D. and Schmidhuber, J. (2018) ‘World Models’, arXiv:1803.10122. <a href="https://arxiv.org/abs/1803.10122">arxiv.org/abs/1803.10122</a>; interactive version at <a href="https://worldmodels.github.io/">worldmodels.github.io</a> <a class="fn-back" href="#fnref-6" aria-label="Back to text">↩</a></li>
<li id="fn-7">Google DeepMind (2025) ‘Genie 3: A New Frontier for World Models’, August 2025. <a href="https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/">deepmind.google/blog/genie-3-a-new-frontier-for-world-models</a> <a class="fn-back" href="#fnref-7" aria-label="Back to text">↩</a></li>
<li id="fn-8">LeCun, Y. (2022) ‘A Path Towards Autonomous Machine Intelligence’, OpenReview, version 0.9.2. <a href="https://openreview.net/pdf?id=BZ5a1r-kVsf">openreview.net/pdf?id=BZ5a1r-kVsf</a> <a class="fn-back" href="#fnref-8" aria-label="Back to text">↩</a></li>
<li id="fn-9">Assran, M. et al. (2025) ‘V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning’, arXiv:2506.09985, June 2025. <a href="https://arxiv.org/abs/2506.09985">arxiv.org/abs/2506.09985</a> <a class="fn-back" href="#fnref-9" aria-label="Back to text">↩</a></li>
<li id="fn-10">Schön, D. A. (1983) <em>The Reflective Practitioner: How Professionals Think in Action</em>. New York: Basic Books. <a class="fn-back" href="#fnref-10" aria-label="Back to text">↩</a></li>
<li id="fn-11">Innovate UK (2016) <em>Building Performance Evaluation Programme: Findings from Non-Domestic Projects</em>. Reported in <em>CIBSE Journal</em>, 3 March 2016: <a href="https://www.cibsejournal.com/news/buildings-use-3-5-times-more-energy-than-expected/">cibsejournal.com/news/buildings-use-3-5-times-more-energy-than-expected</a> <a class="fn-back" href="#fnref-11" aria-label="Back to text">↩</a></li>
<li id="fn-12">Autodesk (2023) ‘Forma Site Design’s AI-powered rapid noise analysis offers instant insights into noise conditions’, Autodesk Forma blog, 3 July 2023. <a href="https://blogs.autodesk.com/forma/2023/07/03/game-changing-rapid-noise-analysis-comes-to-forma-2/">blogs.autodesk.com/forma</a> <a class="fn-back" href="#fnref-12" aria-label="Back to text">↩</a></li>
<li id="fn-13">Black, C. (2025) ‘The Architecture of Behaviour: Predicting Human Movement with AI’, in SCOSA AI Working Group, <em>AI and the Future of Architectural Education in the UK</em>, ed. D. Fagan, September 2025, pp.76–79. The author is a co-author of this report. <a class="fn-back" href="#fnref-13" aria-label="Back to text">↩</a></li>
<li id="fn-14">Day, M. (2026) ‘The agentic future of BIM’, <em>AEC Magazine</em>, 7 March 2026. <a href="https://aecmag.com/features/the-agentic-future-of-bim/">aecmag.com/features/the-agentic-future-of-bim</a> <a class="fn-back" href="#fnref-14" aria-label="Back to text">↩</a></li>
<li id="fn-15">Aish, R., Fisher, A., Orchard, D. and Torry, J. (2024) ‘Programming Languages for the Future of Design Computation’, in <em>Proceedings of the 2024 ACM SIGPLAN International Symposium on New Ideas, New Paradigms, and Reflections on Programming and Software (Onward! ’24)</em>, pp.241–265. <a href="https://doi.org/10.1145/3689492.3689812">doi.org/10.1145/3689492.3689812</a> <a class="fn-back" href="#fnref-15" aria-label="Back to text">↩</a></li>
<li id="fn-16">Schön, D. A. (1987) <em>Educating the Reflective Practitioner: Toward a New Design for Teaching and Learning in the Professions</em>. San Francisco: Jossey-Bass. <a class="fn-back" href="#fnref-16" aria-label="Back to text">↩</a></li>
<li id="fn-17">Stobs-Stobart, O. (2026) ‘People first, technology second: lessons from AI use in design management’, in RIBA, <em>AI Report 2026</em>, pp.10–14. <a class="fn-back" href="#fnref-17" aria-label="Back to text">↩</a></li>
<li id="fn-18">Carpo, M. (2017) <em>The Second Digital Turn: Design Beyond Intelligence</em>. Cambridge, MA: MIT Press. Quotation as given in Bernstein, P. (2020) ‘The Second Digital Turn: Design Beyond Intelligence’ (review), <em>Journal of Architectural Education</em>, 25 September 2020. <a href="https://jaeonline.org/issue-article/second-digital-turn/">jaeonline.org/issue-article/second-digital-turn</a> <a class="fn-back" href="#fnref-18" aria-label="Back to text">↩</a></li>
<li id="fn-19">Fagan, D. (2025) ‘Framing the current moment’, in SCOSA AI Working Group, <em>AI and the Future of Architectural Education in the UK</em>, ed. D. Fagan, September 2025, pp.6–7. <a class="fn-back" href="#fnref-19" aria-label="Back to text">↩</a></li>
<li id="fn-20">Yang, J., Yang, S., Gupta, A. W., Han, R., Li, F.-F. and Xie, S. (2025) ‘Thinking in Space: How Multimodal Large Language Models See, Remember, and Recall Spaces’, CVPR 2025. <a href="https://arxiv.org/abs/2412.14171v1">arxiv.org/abs/2412.14171</a> <a class="fn-back" href="#fnref-20" aria-label="Back to text">↩</a></li>
<li id="fn-21">Tsigkari, M. and Tarabishy, S. (2025) Foster + Partners case study, in SCOSA AI Working Group, <em>AI and the Future of Architectural Education in the UK</em>, pp.58–61. <a class="fn-back" href="#fnref-21" aria-label="Back to text">↩</a></li>
<li id="fn-22">Department for Communities and Local Government (2015) ‘A guide to display energy certificates and advisory reports for public buildings’, GOV.UK. <a href="https://www.gov.uk/government/publications/display-energy-certificates-and-advisory-reports-for-public-buildings/a-guide-to-display-energy-certificates-and-advisory-reports-for-public-buildings">gov.uk/government/publications/display-energy-certificates-and-advisory-reports-for-public-buildings</a> <a class="fn-back" href="#fnref-22" aria-label="Back to text">↩</a></li>
<li id="fn-23">CMS (2023) ‘New High Risk Buildings approval regime comes into force on 1 October 2023’. <a href="https://cms.law/en/gbr/legal-updates/new-high-risk-buildings-approval-regime-comes-into-force-on-1-october-2023">cms.law/en/gbr/legal-updates/new-high-risk-buildings-approval-regime</a> <a class="fn-back" href="#fnref-23" aria-label="Back to text">↩</a></li>
</ol>
</section>
<script src="{{ "/assets/js/insight-world-models.js" | url }}" defer></script>
