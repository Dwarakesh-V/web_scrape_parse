## **1. `temperature`**

**Definition:**
Controls the randomness of token selection during generation.

**Mechanism:**
At each generation step, the model computes a probability distribution over the vocabulary.
`temperature` rescales these probabilities *prior to sampling*:

* **T < 1** → sharpens the distribution, favoring high-probability tokens.
* **T > 1** → flattens the distribution, increasing randomness.

**Practical effect:**

* `temperature=0.2`: highly deterministic, factual output.
* `temperature=0.7`: balanced diversity and coherence.
* `temperature=1.2`: high variability, suitable for creative text.

**Example:**
Prompt: “The cat sat on the”

* T=0.2 → “mat.”
* T=1.0 → “sofa.”
* T=1.5 → “spaceship and purred softly under the stars.”

---

## **2. `top_p` (Nucleus Sampling)**

**Definition:**
Restricts sampling to the smallest subset of tokens whose cumulative probability is at least `p`.

**Mechanism:**
Tokens are sorted by probability in descending order.
Only the top tokens whose cumulative probability ≥ `top_p` are retained; the rest are discarded.

**Practical effect:**

* `top_p=1.0`: no filtering (pure temperature-based sampling).
* `top_p=0.9`: balanced focus, removes low-probability outliers.
* `top_p=0.5`: highly conservative, strongly favors common tokens.

**Primary use:**
Controls diversity while maintaining semantic coherence.

---

## **3. `top_k`**

**Definition:**
Limits sampling to the top `k` most probable tokens.

**Mechanism:**
The vocabulary is ranked by probability, and only the top `k` tokens are kept.
Sampling is then performed (optionally with temperature) over this reduced set.

**Practical effect:**

* `top_k=0`: disabled (all tokens allowed).
* `top_k=10`: very restrictive.
* `top_k=100`: broader diversity.

**`top_k` vs `top_p`:**

* `top_k`: fixed number of candidate tokens.
* `top_p`: variable number based on probability mass.

In practice, most implementations use **either** `top_p` **or** `top_k`, with `top_p` being more adaptive.

---

## **4. `max_new_tokens`**

**Definition:**
Specifies the maximum number of tokens generated *after* the input prompt.

**Purpose:**

* Prevents excessively long outputs.
* Controls compute time and memory usage.

**Example:**

```python
model.generate(inputs, max_new_tokens=100)
```

This allows up to 100 newly generated tokens beyond the input.
If the prompt contains 20 tokens and the context window is 2048, the total remains within bounds.

**Notes:**

* Too low → output may terminate mid-sentence.
* Too high → unnecessary latency and resource usage.

---

## **5. `repetition_penalty`**

**Definition:**
Penalizes tokens that have already appeared in the generated sequence.

**Mechanism:**
Probabilities of previously generated tokens are scaled down multiplicatively before sampling.

**Practical effect:**

* `1.0`: no penalty (default).
* `1.1–1.5`: reduces repetitive phrasing.
* `>2.0`: overly aggressive; may degrade fluency.

**Example:**
Without penalty:

> “Hello! Hello! Hello! How are you? Hello!”

With `repetition_penalty=1.3`:

> “Hello! How are you doing today?”

---

## **6. `do_sample`**

**Definition:**
Determines whether generation uses sampling or greedy decoding.

**Mechanism:**

* `do_sample=False`: selects the most probable token at each step (greedy decoding).
* `do_sample=True`: samples from the probability distribution using `temperature`, `top_p`, or `top_k`.

**Practical effect:**

* `False`: deterministic and repeatable outputs.
* `True`: diverse and non-deterministic outputs.

If `do_sample=False`, parameters such as `temperature`, `top_p`, and `top_k` are ignored.

---

## **7. `eos_token_id` (End-of-Sequence Token)**

**Definition:**
Specifies the token ID that signals termination of generation.

**Effect:**
When the model outputs this token, generation stops immediately.

**Importance:**

* Prevents unbounded generation.
* Ensures clean termination for chat and Q&A systems.

Incorrect configuration can cause premature stopping or runaway generation.

Example:

```json
"eos_token": "</s>"
```

---

## **8. `pad_token_id` (Padding Token)**

**Definition:**
Identifies the token used to pad sequences to equal length in batched inputs.

**Purpose:**
Ensures tensor shape consistency while allowing the model to ignore padded positions during attention and loss computation.

**Example:**

```
Input 1: [The, cat, sat, on, the, mat]
Input 2: [Birds, fly]

After padding:
[
 [The, cat, sat, on, the, mat],
 [Birds, fly, <pad>, <pad>, <pad>, <pad>]
]
```

If incorrectly set, the model may attend to padding tokens, degrading performance.

---

## **Putting It All Together**

```python
output = model.generate(
    inputs,
    temperature=0.8,
    top_p=0.9,
    max_new_tokens=128,
    repetition_penalty=1.2,
    do_sample=True,
    eos_token_id=2,
    pad_token_id=0
)
```

**Execution flow:**

1. The model encodes the input.
2. Token generation proceeds step by step.
3. At each step:

   * Token probabilities are computed.
   * `temperature`, `top_p`, and `repetition_penalty` are applied.
   * If `do_sample=True`, a token is sampled.
   * If the token matches `eos_token_id`, generation stops.
4. Generation halts upon reaching EOS or `max_new_tokens`.

This configuration balances coherence, diversity, and controlled termination.
