## 🚀 Deep Learning Operations Where GPUs Shine

These operations are **highly parallel**, **memory-intensive**, or **compute-heavy**, making them ideal for GPU acceleration.

---

### 🧮 Core Tensor Operations

- **Matrix Multiplication** (`matmul`, `dot`, `einsum`, `bmm`)
- **Tensor Contractions** (e.g., attention via `einsum`)
- **Batch Matrix Multiplication** (`bmm`)
- **Element-wise Operations**:
  - Add, Subtract, Multiply, Divide
  - Activations: ReLU, GELU, Sigmoid, Tanh, etc.
- **Broadcasting Operations**
- **Reductions**:
  - `sum`, `mean`, `max`, `min` over dimensions

---

### 🧠 Model Layers / Primitives

- **Convolutional Layers**:
  - 1D / 2D / 3D convolutions (stride, padding, dilation)
- **Pooling**:
  - MaxPool, AvgPool (1D/2D/3D)
- **Normalization Layers**:
  - BatchNorm, LayerNorm, GroupNorm
- **Dropout** *(for large-scale GPU frameworks)*
- **Embedding Lookups** *(large vocabularies benefit most)*
- **Fully Connected / Dense Layers**
- **Recurrent Layers**:
  - RNN, LSTM, GRU (GPU kernels help a lot)
- **Attention Mechanisms** (esp. self-attention in transformers)

---

### 🔁 Training-Specific Operations

- **Gradient Computation (Backpropagation)**
- **Loss Function Backpropagation**:
  - Cross-Entropy, MSE, KL-Divergence, etc.
- **Optimizer Updates**:
  - SGD, Adam, RMSProp, etc.
- **Mixed Precision Casting**:
  - Float32 ↔ Float16 (AMP, bfloat16, etc.)

---

### 📦 Data & Memory Operations

- **Tensor Copying / Shuffling / Slicing**
- **Reshaping / Transposing / Permuting**
- **Multi-GPU Synchronization**:
  - `all_reduce`, `broadcast`, etc.

---

### ⚡ Advanced / Niche Ops

- **Fourier Transforms** (`fft`, used in signal models)
- **Sparse Matrix Operations** (e.g., sparse attention, GNNs)
- **Custom CUDA Kernels** (e.g. fused operations, quantization)
- **Quantization / Dequantization**

---

### ❌ Typically Not GPU-Accelerated

- **Data loading & augmentation** (CPU-bound unless optimized)
- **Logging, metric computation**
- **Model saving / serialization**
- **Compilation (JIT, XLA)**

---

### 💡 Summary

If an operation involves:

- **Large tensor sizes**
- **Batch-wise parallelism**
- **Linear algebra or deep matrix ops**
- **Forward/backward computation**

...you **absolutely want it on the GPU**.


## GPU-Relevant Deep Learning Ops: Memory vs Compute Complexity

This table maps common deep learning operations to their **memory** and **compute complexity**, showing where GPUs make the most impact.

---

### 🔢 Legend
- **Memory Complexity**: RAM/VRAM consumption (activations, weights, intermediates).
- **Compute Complexity**: Number of floating-point operations (FLOPs).

| **Operation**                            | **Memory Complexity**                | **Compute Complexity**               | **Comments**                                                                 |
|-----------------------------------------|--------------------------------------|--------------------------------------|------------------------------------------------------------------------------|
| **Matrix Multiplication** (`matmul`)    | `O(n²)` or `O(nm)`                   | `O(n³)` or `O(nmk)`                  | High throughput op, GPU-optimized via cuBLAS, central to all DL models.     |
| **Element-wise Ops**                    | `O(n)`                               | `O(n)`                               | Cheap compute, but done on huge tensors → GPU helps due to parallelism.     |
| **Broadcasting Ops**                    | `O(n)`                               | `O(n)`                               | Similar to element-wise. Easily parallelized.                               |
| **Reductions (sum, mean, max)**         | `O(n)`                               | `O(log n)` to `O(n)`                 | Compute is minimal, but memory reads/writes matter.                         |
| **Conv Layers (2D, 3D)**                | `O(n·k²·c)`                           | `O(n·k²·c·h·w)`                       | Heavy compute & memory. GPU acceleration via cuDNN.                         |
| **Pooling (max/avg)**                   | `O(n)`                               | `O(n)`                               | Fast and parallel. Low compute intensity.                                   |
| **Normalization (BatchNorm, LayerNorm)**| `O(n)`                               | `O(n)`                               | Includes mean/var calculation + affine transform.                           |
| **Embedding Lookup**                    | `O(batch_size × emb_dim)`            | `O(batch_size × emb_dim)`            | Memory-bound if vocab is large. GPU helps with parallel lookup.            |
| **RNN / LSTM / GRU**                    | `O(t·h²)`                             | `O(t·h²)`                             | Less parallel than transformers, still heavy in large seqs.                 |
| **Attention / Self-Attention**          | `O(n²·d)`                             | `O(n²·d)`                             | Extremely compute-heavy (quadratic). Scales badly in sequence length.      |
| **Softmax**                             | `O(n)`                               | `O(n)`                               | Often fused with attention or loss layers.                                  |
| **Loss functions (cross-entropy, MSE)** | `O(n)`                               | `O(n)`                               | Light compute. No GPU needed *unless batched*.                              |
| **Gradient Computation (backprop)**     | `O(n)` (activations)                 | same as forward pass or more         | Duplicate memory use from activations + heavier compute.                    |
| **Optimizers (Adam, SGD, etc.)**        | `O(n)`                               | `O(n)`                               | Slightly more memory (momentum, etc), minor compute.                        |
| **Dropout**                             | `O(n)`                               | `O(n)`                               | Minor, often negligible in compute.                                         |
| **Tensor reshaping / transpose**        | `O(n)`                               | negligible                           | Memory copy or pointer rearrangement.                                      |
| **Data transfer (CPU↔GPU)**             | `O(n)`                               | None                                  | Major bottleneck if mismanaged.                                             |
| **Fourier Transform**                   | `O(n)`                               | `O(n log n)`                         | Heavy compute, used in niche models (e.g., FFTConv).                        |
| **Quantization / Dequantization**       | `O(n)`                               | `O(n)`                               | Light compute, high impact on deployment.                                   |
| **Sparse ops (e.g., sparse attention)** | `O(nnz)` (non-zero entries)          | `O(nnz)`                              | Memory-efficient, compute-efficient if sparsity is high.                    |

---

### 🧠 Observations:

- **High Compute + High Memory Ops**:
  - `matmul`, `conv`, `attention`, backprop — *must be on GPU*.
- **High Memory, Low Compute**:
  - Embeddings, normalization, softmax — GPU helps mainly due to batch size.
- **Low Memory + Low Compute**:
  - Reshapes, dropout, simple arithmetic — *GPU is optional*.
- **Sparse Ops / FFT**:
  - Can be **super efficient**, but require specialized kernels or libraries.

---

### ⚡ TL;DR:

| **Put on GPU if...**                           |
|------------------------------------------------|
| You're doing matrix ops on big tensors         |
| You're training models with large activations  |
| You're running transformers, CNNs, or LSTMs    |
| You're dealing with attention or gradients     |
| You're trying to reduce training/inference time|
