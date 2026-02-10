# Unreal Particle Audio Visualizer (Project Design Specifications)
## Introduction
In this report, we describe our project in detail, provide a timeline with specific objectives, describe required tools and datasets, conduct a review of relevant academic literature and assign responsibilities to each team member. As this is an initial report, some aspects of the project are preliminary and will be refined as development progresses, resulting in a more detailed and well-defined plan.

## Project description
The “Unreal Particle Audio Visualizer” is a system designed to to parse an audio track into separate components, such as vocals, bass, and instrumental stems and visualize these components within the Unreal Engine (UE) environment using the Niagara particle system [1]. Each audio component will drive distinct visual behaviours, creating an expressive, audio-responsive image. 

The project consists of two manually connected units. The first is audio preprocessing, in which the input track is divided into individual stems. The second is visualization within UE, where the separated audio components are imported and individually mapped to Niagara particle effects based on audio features such as beat, frequency, and amplitude. This approach enables the creation of a complex system that visually represents the sounds perceived when listening to a given melody. 

Our goal is to create a complex system that can visually represent any soundtrack. While this system can be used as a fun and engaging visual experience, it can also serve a broader purpose by helping people with hearing impairments enjoy music and mimic the auditory perception that hearing individuals experience when listening to songs.

## Literature review
Many recent works show that deep learning based music source separation on MUSDB18 is a mature and widely adopted approach, which supports our choice to build the separation stage of the project on Spleeter and this dataset [2], [3]. Spleeter provides pretrained 2, 4, and 5 stem U-net models trained on large multitrack collections and evaluated on MUSDB18, achieving high quality of separation while running up to 100 times faster than real time on a single GPU, which makes it well suited for offline stem generation that can be imported into Unreal Engine [4], [5]. Documentation for Unreal Engine demonstrates how Niagara and the Audio Synesthesia system can drive particle attributes such as spawn rate, size, and colour from per-band amplitude or submix data [6], [7], [8].

Moreover, from a perceptual perspective, relationships between sound and colours has been an actively explored topic since 1704 [9]. For example, multiple studies attempt to map colour parameters such as hue, saturation and luminance to properties of sound such as pitch, loudness and noisiness [10], [11]. Furthermore, Vickery L. suggests that certain instruments can be represented by specific ranges of colour [10]. While pure sound waves demonstrate relatively stable cross-mappings, visually representing more complex sounds remains significantly more challenging [10]. Despite the large amount of published research, there is still no existing one-to-one mapping between sound and colour, as perception varies between individuals and is strongly influenced by the emotional aspects [12] [13]. Therefore, our implementation will not follow a fixed mapping chart, but instead draws inspiration from existing studies.

## Required Tools 
We plan to develop a custom audio separation model using Python’s Spleeter library [4]. Spleeter offers a proven architecture for music source separation and significantly reduces implementation complexity, allowing the project to build on established research rather than starting from scratch. This approach helps address the difficulty of visually representing complex musical structures identified through Literature Review. By separating a song into individual components, the system can represent different elements of the audio more accurately. After training, our model will be used as the first component of the system to generate separated audio stems from a single input track.

The resulting audio stems will then be manually imported into the UE, where a basic scene and multiple Niagara particle systems will be configured, each responsible for a specific visual behavior. For example, round yellow beams may appear in response to increase of the vocal amplitude, and square black particles may abruptly emit on detected beats. These visual mappings will be defined in advance. As a result, while the system cannot be fully classified as real-time, it does not require manual remapping of visuals for each audio track. 

Our focus will remain mainly on perfecting the Niagara particle effects rather than constructing a complex game environment. Since the project is developed on our own laptops, we do not have enough computational power to render very dense and detailed scenes.

## Datasets and Audio Material
To train and evaluate the audio source separation component of the project, we will use a collection of music tracks spanning multiple genres (e.g., pop, electronic, rock). The primary dataset for this project will be MUSDB18 [3], a widely used benchmark dataset for music source separation research.

MUSDB18 contains 150 full-length music tracks, each provided as a mixture along with isolated stems for vocals, bass, drums, and other instruments. This structure makes it well suited for supervised training and evaluation of source separation models. The diversity of musical genres in MUSDB18 supports the project’s goal of creating a system that generalizes across different musical styles. 

This dataset is officially recommended in the Spleeter documentation [14] and has been used extensively in prior source separation research [15] and model training, ensuring compatibility with our chosen framework and reliable performance in practice.

## Timeline and Milestones

## Roles and Responsibilities

## Future Extensions
Possible extensions include real-time audio input, user controlled visual mappings, or alternative source separation models. These are considered stretch goals beyond the current scope. Another potential development is integration with a VR headset within the Unreal Engine environment. VR integration could provide a more immersive multisensory experience by allowing users to perceive sound through spatial and visual cues, which may be particularly beneficial for individuals with hearing impairments.

## Olivia's objectives

## Sofiia's objectives 

## Kedan's objectives

## References

[1]	“Creating Visual Effects in Niagara for Unreal Engine | Unreal Engine 5.7 Documentation | Epic Developer Community,” Epic Games Developer. Accessed: Feb. 08, 2026. [Online]. Available: https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-visual-effects-in-niagara-for-unreal-engine  
[2]	G. Keerthi, “A Survey on Music Source Separation using Deep Learning,” Int. J. Res. Publ. Rev., vol. 5, Nov. 2024, [Online]. Available: https://ijrpr.com/uploads/V5ISSUE11/IJRPR35780.pdf  
[3]	Z. Rafii, A. Liutkus, F.-R. Stöter, S. I. Mimilakis, and R. Bittner, “MUSDB18-HQ-SigSep.” Zenodo, Aug. 01, 2019. doi: 10.5281/ZENODO.3338373. 
[4]	deezer/spleeter. (Feb. 09, 2026). Python. Deezer. Accessed: Feb. 08, 2026. [Online]. Available: https://github.com/deezer/spleeter  
[5]	R. Hennequin, A. Khlif, F. Voituret, and M. Moussallam, “Spleeter: a fast and efficient music source separation tool with pre-trained models,” J. Open Source Softw., vol. 5, no. 50, p. 2154, Jun. 2020, doi: 10.21105/joss.02154. 
[6]	“How to Create Audio Effects in Niagara for Unreal Engine | Unreal Engine 5.7 Documentation | Epic Developer Community,” Epic Games Developer. Accessed: Feb. 08, 2026. [Online]. Available: https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-create-audio-effects-in-niagara-for-unreal-engine  
[7]	“Audio Synesthesia in Unreal Engine | Unreal Engine 5.7 Documentation | Epic Developer Community,” Epic Games Developer. Accessed: Feb. 08, 2026. [Online]. Available: https://dev.epicgames.com/documentation/en-us/unreal-engine/audio-synesthesia-in-unreal-engine 
[8]	“Overview of submixes in Unreal Engine | Unreal Engine 5.7 Documentation | Epic Developer Community,” Epic Games Developer. Accessed: Feb. 08, 2026. [Online]. Available: https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-submixes-in-unreal-engine  
[9]	I. Newton, Opticks. London : Printed for Sam Smith, and Benj. Walford, printers to the Royal Society, at the prince’s Arms in St. paul’s Church-yard, 1704. Accessed: Feb. 09, 2026. [Online]. Available: http://archive.org/details/opticksortreatis00newt  
[10]	L. Vickery, “Some approaches to representing sound with colour and shape,” Res. Outputs 2014 2021, Jan. 2018, [Online]. Available: https://ro.ecu.edu.au/ecuworkspost2013/6410  
[11]	G. Hamilton-Fletcher, C. Witzel, D. Reby, and J. Ward, “Sound Properties Associated With Equiluminant Colours,” Jan. 2017, doi: 10.1163/22134808-00002567. 
[12]	C. Spence and N. Di Stefano, “Coloured hearing, colour music, colour organs, and the search for perceptually meaningful correspondences between colour and sound,” -Percept., vol. 13, no. 3, p. 20416695221092802, May 2022, doi: 10.1177/20416695221092802. 
[13]	L. Wilms and D. Oberfeld, “Color and emotion: effects of hue, saturation, and brightness,” Psychol. Res., vol. 82, no. 5, pp. 896–914, Sep. 2018, doi: 10.1007/s00426-017-0880-8. 
[14]	“Getting started,” GitHub. Accessed: Feb. 08, 2026. [Online]. Available: https://github.com/deezer/spleeter/wiki/2.-Getting-started  
[15]	S. S. Parvathi and D. Chandrasekar, “Feature separation of music across diverse dataset: a comparative perspective,” Bull. Electr. Eng. Inform., vol. 14, no. 5, pp. 3903–3912, Oct. 2025, doi: 10.11591/eei.v14i5.9962. 

