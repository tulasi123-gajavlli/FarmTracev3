# ML Organic Prediction

The core of FarmTracev3's intelligent labeling system is a rule-based Machine Learning algorithm. Its purpose is to quantify the likelihood that a product was grown under organic conditions.

## 1. Features and Inputs

The `predict_organic` function takes five inputs:
- `Temperature` (°C)
- `Humidity` (%)
- `Water Content` (%)
- `Pesticides Used` (Boolean/Category)
- `Fertilizers Used` (Boolean/Category)

## 2. Scoring Algorithm

The algorithm uses a **Point-Based Accumulator** to calculate the final confidence:

### Environmental Scoring (3 Points)
1.  **Temperature**: 18-28°C is considered an optimal organic range.
2.  **Humidity**: 60-80% is considered an ideal organic range.
3.  **Water Content**: 70-90% is considered consistent with organic produce.

### Bio-Chemical Scoring (2 Points)
1.  **Pesticides**: Checked against a blacklist. Only "none", "natural", or "biopesticides" are approved.
2.  **Fertilizers**: Checked for keywords like "compost", "manure", "natural", or "vermicompost".

---

## 3. Confidence Calculation

A product is classified as `Organic` if it meets at least **3 out of 5** criteria.

### Stability Multiplier
The algorithm goes beyond basic thresholds by checking for "stability":
- **Optimal Temperature Bonus**: If the temperature is close to 22°C (±3), it gains a +5% bonus.
- **Optimal Humidity Bonus**: If the humidity is exactly 70% (±10), it gains another +5% bonus.

### Final Logic
```python
is_organic = score >= 3
confidence = min(95, (score * 15) + stability_bonus + 20)
```
- The confidence is capped at 95% to acknowledge that no rule-based system is 100% infallible without physical lab testing.

---

## 4. Reasoning and Feedback

The algorithm provides a list of `reasons` for its decision. For example, if a product is NOT organic, the system will explicitly state:
- *"Temperature 35°C outside organic range (18-28°C)"*
- *"Non-organic pesticides used: Chemical-X"*

This transparency allows consumers to understand the exact factors behind the "Organic" label.
