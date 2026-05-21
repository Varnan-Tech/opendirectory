# Neuroscience of Content Hooks (Yeo-7 Networks)

To properly analyze and optimize content hooks using the TRIBE v2 Brain Hook Analyzer, you must understand the underlying neurobiology of engagement. 

Meta's TRIBE v2 model outputs activation data across 20,484 cortical vertices. We map these vertices into the scientifically validated **Yeo-7 Functional Networks** to derive a comprehensive "Engagement Score."

Here is how to interpret the Z-scores returned by the `/analyze` API.

---

## 1. Dorsal Attention Network (DAN)
**Function**: Top-down, voluntary allocation of attention. Focused, goal-directed concentration.
- **High Z-Score (>1.0)**: The hook is highly stimulating and requires the viewer's active focus. It presents complex information, a visual puzzle, or a compelling narrative thread that makes the viewer *choose* to pay attention.
- **Low Z-Score (<0.0)**: The hook is passive. The viewer is not actively engaged with the material.
- **Optimization Strategy**: To increase DAN, add on-screen text, complex visual B-roll, or a puzzle/question that requires the viewer to think actively.

## 2. Ventral Attention Network (VAN)
**Function**: Bottom-up, stimulus-driven attention. The "Circuit Breaker" of the brain.
- **High Z-Score (>1.5)**: **CRITICAL FOR PATTERN INTERRUPT**. A high VAN score means the hook successfully jolted the viewer out of their scrolling habit. Triggered by sudden movements, loud noises, unexpected visuals, or highly controversial opening statements.
- **Low Z-Score (<0.5)**: The hook blends in with the rest of the feed. The user is highly likely to swipe away.
- **Optimization Strategy**: To increase VAN, use faster cuts in the first 1.5 seconds, higher audio volume, sudden visual changes, or extreme close-up angles.

## 3. Limbic Network (Limbic)
**Function**: Emotion, memory, and reward processing.
- **High Z-Score (>1.0)**: The hook elicits a strong emotional response (fear, joy, disgust, surprise, arousal). The viewer *feels* something immediately.
- **Low Z-Score (<0.0)**: The hook is sterile, purely logical, or corporate. 
- **Optimization Strategy**: To increase Limbic activation, use emotionally charged words ("Destroyed," "Secret," "Heartbreaking"), show expressive human faces (especially eyes/mouth), or introduce high stakes.

## 4. Visual Network (Visual)
**Function**: Processing of visual stimuli.
- **High Z-Score (>1.0)**: The scene is visually rich, dynamic, or highly saturated. 
- **Low Z-Score (<0.0)**: The video is visually static (e.g., a person talking to a camera in a dark room with no movement).
- **Optimization Strategy**: Add dynamic lighting, movement, B-roll overlays, or bright contrasting colors.

## 5. Default Mode Network (DMN)
**Function**: Internal mentation, mind-wandering, daydreaming, and thinking about the past/future.
- **High Z-Score (>1.0)**: **DANGER**. If the DMN is highly active while watching a short-form video, the viewer has lost interest and their mind is wandering. They are about to swipe.
- **Low Z-Score (<0.0)**: Excellent. The viewer is "locked in" to the external stimulus and is not distracted by their own thoughts.
- **Optimization Strategy**: To decrease DMN, increase pacing. Remove pauses, 'umms', and 'ahhs'. Ensure every second delivers new information or visual stimulus to keep the external attention networks engaged.

---

## The Engagement Formula
`Engagement Score = Z(DAN) + Z(VAN) + Z(Limbic) + Z(Visual) - Z(DMN)`

**Interpretation**:
- **Score > 3.0**: Exceptional Hook. High likelihood of virality. Extreme pattern interrupt combined with emotional resonance.
- **Score 1.5 to 3.0**: Good Hook. Solid retention expected for the first 5 seconds.
- **Score 0.0 to 1.5**: Average Hook. Typical corporate or informational video. Will lose 50% of audience in 3 seconds.
- **Score < 0.0**: Failed Hook. The Default Mode Network has taken over. Instant swipe.