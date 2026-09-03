---
layout: page
title: Splyce
description: SIMD Vectorization of Sparse Coiteration
img: assets/img/publication_preview/splyce.png
importance: 1
category: Work
related_publications: true
---
 
Sparse tensor contractions are bottlenecked by coiteration loops that resist standard loop vectorization. We present Splyce, an auto-vectorization framework in MLIR that overcomes this through a dual-path execution model. 
By decoupling coordinate intersection from pointer management via selective predication, Splyce inherently eliminates data-dependent branches as a side-effect, allowing modern superscalar engines to maximize instruction-level parallelism and hide memory latency. 
Beyond simple branch elimination, our transformation enables high-throughput speculative execution by saturating parallel functional units previously starved by sequential dependencies. 
Evaluation across foundational sparse tensor kernels demonstrates performance ranging from 1.94× to 2.86× on synthetic inputs, with consistent speedups sustained across a vast majority of irregular real-world datasets from the SuiteSparse collection. 
Ultimately, Splyce demonstrates that by converting unpredictable control-flow into a predictable data stream, compiler-driven speculation can effectively reconcile the memory efficiency of compressed storage with the execution-unit throughput of modern superscalar architectures.

Project repository can be found here: <a href="https://github.com/KabilanMA/Splyce">https://github.com/KabilanMA/Splyce</a>